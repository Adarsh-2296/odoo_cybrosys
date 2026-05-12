import { PosStore } from "@point_of_sale/app/services/pos_store";
import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";


patch(PosStore.prototype, {
    async pay(){
        var order = this.getOrder()
        if (order.lines.length ==1 && order.lines[0].product_id.pos_rating ==1){
            console.log(order.lines[0].product_id.pos_rating)
            this.env.services.dialog.add(AlertDialog, {
                    title: _t("Alert"),
                    body: _t(
                        "Add another product or select a product with more than one star!"
                    ),
                });

            }
        else {
            return (
                super.pay(...arguments)
            );
        }
    },
});