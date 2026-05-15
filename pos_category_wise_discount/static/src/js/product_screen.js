import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";

patch(ProductScreen.prototype, {
    async onNumpadClick(buttonValue){
        var discount = 20
        console.log(this)
        var linediscount = this.numberBuffer.state.buffer+buttonValue
        console.log(this.numberBuffer.state.buffer+buttonValue)
            if (this.pos.numpadMode == 'discount' && discount < Number(linediscount)) {
                alert('hi')
            }
            else {
                return (
                    super.onNumpadClick(...arguments)
                );
            }


    }
});