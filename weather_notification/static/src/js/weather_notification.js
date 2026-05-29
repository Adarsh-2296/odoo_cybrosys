/** @odoo-module **/
import { registry } from "@web/core/registry";
import {Component, onWillStart} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { rpc } from "@web/core/network/rpc";

class MySystrayIcon extends Component {
    static components = { Dropdown };
   setup() {
   this.dialogService = useService("dialog");
   onWillStart(async () => {
            this.result = await rpc("/weather/notification");
                });
   }
}
MySystrayIcon.template = "weather_notification.systray_icon";
export const systrayItem = {
   Component: MySystrayIcon,
};
registry.category("systray").add(
   "MySystrayIcon",
   systrayItem,
   { sequence: 10 }
);
