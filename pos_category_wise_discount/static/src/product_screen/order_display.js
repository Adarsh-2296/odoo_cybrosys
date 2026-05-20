import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { useState } from "@odoo/owl";

patch(ProductScreen.prototype, {
    async setup(){
        super.setup(...arguments)
        this.pos = usePos();
        this.state.is_clear_order_line = this.pos.config.is_clear_order_line_button;
    },
    async clearLines(){
        this.pos.getOrder().update({ lines : [] })
    }
});