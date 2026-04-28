/** @odoo-module */
import { renderToFragment } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.product_quantity = publicWidget.Widget.extend({
    selector: '.product_quantity_near_cart',
});

