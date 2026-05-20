/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

const actionRegistry = registry.category("actions");
class InventoryDashboard extends Component {
    setup() {
        super.setup();
        this.orm = useService('orm');
        this._fetch_data();
  }
  async _fetch_data(){
        let result = await this.orm.call("stock.picking", "get_tiles_data", [], {});
        // document.getElementById('inventory_data').innerHTML = `<t t-foreach="${result}.result" t-as="re" t-key="re" t-out="re"></t>`;
      for (var i =0;i<result.result.length;i++) {
          document.getElementById('inventory_data').innerHTML += `<tr>${result.result[i]}</tr>`;
      }
    }
}
InventoryDashboard.template = "inventory_dashboard.InventoryDashboard";
actionRegistry.add("inventory_dashboard_tag", InventoryDashboard);
