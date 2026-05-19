import { Orderline } from "@point_of_sale/app/components/orderline/orderline";
import { patch } from "@web/core/utils/patch";

patch(Orderline.prototype, {
    async setup(){
        this.is_clear_order_line_button = this.__owl__.app.env.services.pos.config.is_clear_order_line_button
        return (
                    super.setup(...arguments)
                );
    },
    async removeLine(){
        this.props.line.delete()
    }
});