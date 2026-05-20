import { Orderline } from "@point_of_sale/app/components/orderline/orderline";
import { patch } from "@web/core/utils/patch";
import { useState } from "@odoo/owl";

patch(Orderline.prototype, {
    async setup(){
        this.state = useState({
            is_clear_order_line : this.__owl__.app.env.services.pos.config.is_clear_order_line_button,
        });
        return (
                    super.setup(...arguments)
                );
    },
    async removeLine(){
        this.props.line.delete()
    }
});