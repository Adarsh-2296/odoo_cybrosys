import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { DiscountLimitPopup } from "@pos_category_wise_discount/core/discount_limit_popup"
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";

patch(ProductScreen.prototype, {
    async onNumpadClick(buttonValue){
        var line = this.pos.getOrder().lines.filter((f) => f.isSelected() == true);
        var linediscount = this.numberBuffer.state.buffer+buttonValue
        if (this.pos.numpadMode == 'discount') {
            var discount = line[0].product_id.product_tmpl_id.pos_categ_ids[0].discount_limit
            if (discount < Number(linediscount)) {
                this.pos.env.services.dialog.add(AlertDialog, {
                    title: _t("Alert"),
                    body: _t(
                        "Discount exceeds the maximum that can be given to this product! " +
                        "Consider an amount lower than " + discount + ' percentage.'
                    ),
                });
            } else {
                return (
                    super.onNumpadClick(...arguments)
                );
            }
        }
        else{
            return (
                    super.onNumpadClick(...arguments)
                );
        }
    }
});

patch(PosStore.prototype, {
    async pay(){
        if (this.getOrder().discountLines[0]) {
            var lines = this.getOrder().lines
            var disount_limit = []
            var products = []

            var price = (this.getOrder().discountLines[0].displayPrice * -1) + this.getOrder().displayPrice
            var percentage = ((this.getOrder().discountLines[0].displayPrice * -1) / price) * 100
            var category = {}
            var category_ids = {}
            for (var j=0;j<this.config.pos_category_ids.length;j++){
                category_ids[this.config.pos_category_ids[j].id] ='1';
            }
            for (var i = 0; i < lines.length; i++) {
                if (lines[i].product_id.product_tmpl_id.pos_categ_ids[0] && String(lines[i].product_id.product_tmpl_id.pos_categ_ids[0].id) in category_ids) {
                    disount_limit.push(lines[i].product_id.product_tmpl_id.pos_categ_ids[0].discount_limit)
                    if (percentage > lines[i].product_id.product_tmpl_id.pos_categ_ids[0].discount_limit && !(lines[i].product_id.product_tmpl_id.pos_categ_ids[0].name in category)){
                            products.push(lines[i].product_id);
                            category[lines[i].product_id.product_tmpl_id.pos_categ_ids[0].name] = '1';
                    }

                }
            }
            if (disount_limit.sort()[0] < percentage) {
                const payload = await makeAwaitable(this.dialog, DiscountLimitPopup, {
                    title: _t("Limit Exceeded!"),
                    body: _t("Discount exceeds the maximum that can be given to this product! " +
                        "Consider an amount lower than " + disount_limit.sort()[0] + " percentage."),
                    lines: products,
                    discount: percentage
                });
            } else {
                return (
                    super.pay(...arguments)
                );
            }
        }
        else {
                return (
                    super.pay(...arguments)
                );
            }
    },

});
