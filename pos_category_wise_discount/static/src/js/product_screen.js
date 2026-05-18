import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";
import { PosStore } from "@point_of_sale/app/services/pos_store";

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
                        "Discount exceeds the maximum that can be given to this product!" +
                        "Consider an amount lower than " + discount + '.'
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
        var lines = this.getOrder().lines
        var disount_limit = []
        var products = []
        for(var i = 0;i<lines.length;i++){
            if(lines[i].product_id.product_tmpl_id.pos_categ_ids[0]) {
                disount_limit.push(lines[i].product_id.product_tmpl_id.pos_categ_ids[0].discount_limit)
                products.push(lines[i].product_id)
            }
        }
        console.log(products[0].display_name)
        console.log(products[0].product_tmpl_id.pos_categ_ids[0].discount_limit)
        console.log(products[0].display_name)
        var price = (this.getOrder().discountLines[0].displayPrice * -1) + this.getOrder().displayPrice
        var percentage = ((this.getOrder().discountLines[0].displayPrice * -1)/price)*100
        if (disount_limit.sort()[0] < percentage){
            this.env.services.dialog.add(AlertDialog, {
                    title: _t("Alert"),
                    body: _t(
                        "Discount exceeds the maximum that can be given to this product!" +
                        "Consider an amount lower than " + disount_limit.sort()[0] + ' percentage.'
                    ),
                });
        }
        else{
            return (
                    super.pay(...arguments)
                );
        }
    },

});
