import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

patch(ProductScreen.prototype, {
    async setup(){
        this.pos = usePos();
        this.is_clear_order_line = this.pos.config.is_clear_order_line_button
        return (
                    super.setup(...arguments)
                );
    },
    async clearLines(){
        this.pos.getOrder().update({ lines : [] })


        // this.selected = 0;
        // for (var i=0;i<this.props.order.lines.length;i++){
        //     if (this.props.order.lines[i].isSelected() == true){
        //         this.props.order.lines[i].delete()
        //         this.selected = 1;
        //     }
        // }
        // if (this.selected == 0){
        //     this.props.order.update({ lines : [] })
        // }
    }
});