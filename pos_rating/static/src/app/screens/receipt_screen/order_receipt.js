import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { patch } from "@web/core/utils/patch";

patch(OrderReceipt.prototype, {
   get PosRatingReceipt(){
       let products = this.props.order._prices.original.baseLines
       let result = []
       for(var i =0;i<products.length;i++){
           result.push(i)
       }
       let datas = {
           "products" : products,
           "result" : result,
       }
       return datas
   },
});