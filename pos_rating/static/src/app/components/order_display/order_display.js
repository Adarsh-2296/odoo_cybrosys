/** @odoo-module */
import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";
import { patch } from "@web/core/utils/patch";
import {Orderline} from "@point_of_sale/app/components/orderline/orderline";
import { ProductTemplate } from "@point_of_sale/app/models/product_template";

export class PosRatingOrderLine extends Orderline {
    static props = {
        product: ProductTemplate,
    };
}

patch(Orderline.prototype, {
   get PosRatingOrder(){
       console.log(this.props.product)
       console.log(this)

       return this
   },
});