/** @odoo-module */
import { Dialog } from "@web/core/dialog/dialog";
import { Component } from "@odoo/owl";

export class DiscountLimitPopup extends Component {
    static template = "pos_category_wise_discount.DiscountLimitPopup";
    static components = { Dialog };

    async confirm() {
        this.props.close();
    }
    }
