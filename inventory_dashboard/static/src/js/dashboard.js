/** @odoo-module **/
import { registry } from "@web/core/registry";
import {Component, useState, onWillStart} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";
import { redirect } from "@web/core/utils/urls";
import { FormViewDialog } from "@web/views/view_dialogs/form_view_dialog";


const actionRegistry = registry.category("actions");
class InventoryDashboard extends Component {
    setup() {
        super.setup();
        this.orm = useService('orm')
        this.actionService = useService("action");
        this.dialog = useService("dialog")
        onWillStart(async () => {
            this.result = await this.orm.call("stock.picking", "get_products_data", [],{});
                });
        this.state = useState({
            selectedyear : 2026,
            selectedmonth : false,
            selectedweek : false,
            filter : false,
            weekfilter : false,
            change : false,
            start : 0,
            stop : 10,

        });
        this._fetch_data();
  }
  async clearFilter(){
        redirect('/odoo/action-678')
  }
  async getYear(){
        this.state.filter = true
        this.incomingchart.destroy()
        this.groupchart.destroy()
        this.outgoingchart.destroy()
        this.locationchart.destroy()
        this.internalchart.destroy()
        this.warehousechart.destroy()
        this.averagechart.destroy()
        this.inventorychart.destroy()
        this._fetch_data()
  }
  async getWeek(){
        this.state.filter = true
        this.incomingchart.destroy()
        this.groupchart.destroy()
        this.outgoingchart.destroy()
        this.locationchart.destroy()
        this.internalchart.destroy()
        this.warehousechart.destroy()
        this.averagechart.destroy()
        this.inventorychart.destroy()
        this.state.weekfilter = true
        this._fetch_data()
  }
  async getMonth(){
        this.state.filter = true
        this.incomingchart.destroy()
        this.groupchart.destroy()
        this.outgoingchart.destroy()
        this.locationchart.destroy()
        this.internalchart.destroy()
        this.warehousechart.destroy()
        this.averagechart.destroy()
        this.inventorychart.destroy()
        this._fetch_data()
  }
  async _fetch_data(){
        console.log(this.result)
        if (this.state.filter == false) {
            var result = await this.orm.call("stock.picking", "get_tiles_data", [], {'month' : false, 'year': false, 'week' : false});
        }
        else if (this.state.weekfilter == false){
            var result = await this.orm.call("stock.picking", "get_tiles_data", [], {'month' : this.state.selectedmonth, 'year': this.state.selectedyear,'week' : false});
        }
        else {
            var result = await this.orm.call("stock.picking", "get_tiles_data", [], {'month' : this.state.selectedmonth, 'year': this.state.selectedyear,'week' : this.state.selectedweek});
        }
        this.state.change = true
        await  loadJS(["/web/static/lib/Chart/Chart.js"]);
        var incoming = document.getElementById('incoming_data').getContext('2d');
        this.incomingchart = new Chart(incoming, {
            type: 'line',
            data: {
                labels: result.incoming_product,
                datasets: [{
                    label: 'Quantity',
                    data: result.incoming_qty,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                   beginAtZero: true
               }
           }
       }
   });

        var outgoing = document.getElementById('outgoing_data').getContext('2d');
        this.outgoingchart = new Chart(outgoing, {
            type: 'doughnut',
            data: {
                labels: result.outgoing_product,
                datasets: [{
                    label: 'Quantity',
                    data: result.outgoing_qty,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                   beginAtZero: true
               }
           }
       }
   });
        var outgoing = document.getElementById('location_wise').getContext('2d');
        this.locationchart = new Chart(outgoing, {
            type: 'pie',
            data: {
                labels: result.location_name,
                datasets: [{
                    label: 'Count',
                    data: result.location_product,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                   beginAtZero: true
               }
           }
       }
   });
        var outgoing = document.getElementById('group_based').getContext('2d');
        this.groupchart = new Chart(outgoing, {
            type: 'pie',
            data: {
                labels: result.picking_type_name,
                datasets: [{
                    label: 'Count',
                    data: result.picking_type_count,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                   beginAtZero: true
               }
           }
       }
   });
        var outgoing = document.getElementById('internal_transfers').getContext('2d');
        this.internalchart = new Chart(outgoing, {
            type: 'bar',
            data: {
                labels: result.internal_transfers_product,
                datasets: [{
                    label: 'Count',
                    data: result.internal_transfers_qty,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                   beginAtZero: true
               }
           }
       }
   });
        var outgoing = document.getElementById('warehouse_location').getContext('2d');
        this.warehousechart = new Chart(outgoing, {
            type: 'bar',
            data: {
                labels: result.warehouse_name,
                datasets: [{
                    label: 'Count',
                    data: result.warehouse_location,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                   beginAtZero: true
               }
           }
       }
   });
         var outgoing = document.getElementById('avg_expense').getContext('2d');
         this.averagechart = new Chart(outgoing, {
            type: 'line',
            data: {
                labels: result.product_names,
                datasets: [{
                    label: 'Count',
                    data: result.product_avg_cost,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                   beginAtZero: true
               }
           }
       }
   });
         var outgoing = document.getElementById('inventory_valuation').getContext('2d');
        this.inventorychart = new Chart(outgoing, {
            type: 'doughnut',
            data: {
                labels: result.product_val_names,
                datasets: [{
                    label: 'Count',
                    data: result.product_val_avg_cost,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                   beginAtZero: true
               }
           }
       }
   });
    }
    async nextProducts(){
        if (this.result.products.length > this.state.stop) {
                this.state.start += 10
                this.state.stop += 10
        }
    }
    async previousProducts(){
        if (this.state.start > 0){
            this.state.start -= 10
            this.state.stop -= 10
        }
    }
    async productBackend(id){
        // this.dialog.add(FormViewDialog, {
        //         resId: id,
        //         resModel: 'product.template',
        //     })
        this.actionService.doAction({
            res_model: "product.template",
            res_id: id,
            type: "ir.actions.act_window",
            views: [[false, "form"]],
            target: "new",
        });
    }
}
InventoryDashboard.template = "inventory_dashboard.InventoryDashboard";
actionRegistry.add("stock_dashboard_tag", InventoryDashboard);
