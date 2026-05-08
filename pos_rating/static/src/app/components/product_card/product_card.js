/** @odoo-module */
import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";
import { patch } from "@web/core/utils/patch";

patch(ProductCard.prototype, {
   get PosRating(){
       var pos_rating = this.props.product.pos_rating;
       return pos_rating
   },
});

