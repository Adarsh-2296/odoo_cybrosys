/** @odoo-module */
import { Dialog } from "@web/core/dialog/dialog";
import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";

export class PopupPos extends Component {
    static template = "pos_rating.PopupPos";
    static components = { Dialog, Dropdown, DropdownItem };

    setup() {
        this.pos = usePos();
        this.payment = 0;
    }

    async forcepay(){
        if (this.pos.user._role == 'manager'){
            this.payment = 1;
        }
        else {
            this.payment = 2;
        }

    }
    async cancel(){
        this.payment = 0;
    }
    async confirm() {
        if(this.payment == 1){
            this.pos.pay();
            console.log(this.pos.pay);

        }
        if (this.payment == 2){
            this.pos.env.services.dialog.add(AlertDialog, {
                    title: _t("Alert"),
                    body: _t(
                        "You don't have permission for this action!" +
                        "Contact your administrator."
                    ),
            });
        }
        if(this.payment == 0){
            console.log(this.pos.user._role)
            this.props.close();
        }

    }
}
