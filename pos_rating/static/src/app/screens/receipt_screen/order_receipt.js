import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { patch } from "@web/core/utils/patch";

patch(OrderReceipt.prototype, {
   get PosRatingReceipt(){
       let pos_rating = this.props.order
       console.log(pos_rating)
       let result = []
       for(var i =1;i<=4;i++){
           result.push(i)
       }
       return result
   },
});