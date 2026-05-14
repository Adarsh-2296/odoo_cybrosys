import { PosStore } from "@point_of_sale/app/services/pos_store";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { PopupPos } from "@pos_rating/core/popup_pos/popup_pos";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";

patch(PosStore.prototype, {
    async pay(){
        var is_payment_restricted = this.config.is_restrict_payment
        if (is_payment_restricted) {
            var orders = this.getOrder()
            console.log(this)
            var result = await orders.lines.filter((f) => f.product_id.pos_rating == 1);
            console.log(result)
            if (result.length >=1) {
                const payload = await makeAwaitable(this.dialog, PopupPos, {
                    title: _t("Add More!"),
                    body: _t("Add another product or select a product with more than one star!")
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