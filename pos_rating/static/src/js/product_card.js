/** @odoo-module */
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";
import { patch } from "@web/core/utils/patch";

patch(ProductCard.prototype, {
    get PosRating() {
        return String(this.props.product.pos_rating);
    },
});

// class POSRating extends ProductCard{
//
// }
// publicWidget.registry.get_product_tab = publicWidget.Widget.extend({
//     selector: '.js_product_pos_rating',
//     async willStart() {
//         let result = await rpc('/get/pos_rating', {});
//         this.$el.find('#courosel').html(
//             renderToElement('pos_rating.dynamic_filter_template_machine', {
//                 result: result,
//             })
//         );
//     }
//
// });