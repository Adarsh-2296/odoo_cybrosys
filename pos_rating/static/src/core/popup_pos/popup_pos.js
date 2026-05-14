/** @odoo-module */
import { Dialog } from "@web/core/dialog/dialog";
import { Component, useState} from "@odoo/owl";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";
import { redirect } from "@web/core/utils/urls";
import { Input } from "@point_of_sale/app/components/inputs/input/input";

export class PopupPos extends Component {
    static template = "pos_rating.PopupPos";
    static components = { Dialog, Input };

    setup() {
        this.pos = usePos();
        this.state = useState({
            selectedvalue : String,
        });
    }
    async confirm() {
        if(this.state.selectedvalue == 'Force Payment') {
            if (this.pos.user._role == 'manager') {
                var path = this.pos.router.path
                redirect('/pos/ui/' + path.slice(8, 10) + 'payment' + path.slice(17))
            }
            else {
                this.pos.env.services.dialog.add(AlertDialog, {
                    title: _t("Alert"),
                    body: _t(
                        "You don't have permission for this action!" +
                        "Contact your administrator."
                    ),
                });
            }
        }
        else{
            this.props.close();
    }
    }
    }
