/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import {Orderline} from "@point_of_sale/app/components/orderline/orderline";

patch(Orderline.prototype, {
   get PosRatingOrder(){
       let pos_rating = this.props.line.product_id.pos_rating
       let result = []
       for(var i =1;i<=pos_rating;i++){
           result.push(i)
       }
       return result
   },
});