/** @odoo-module **/
import { registry } from "@web/core/registry";
import {Component, useState} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DateTimeInput } from "@web/core/datetime/datetime_input";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";

const actionRegistry = registry.category("actions");
class InventoryDashboard extends Component {
    static components = { Dropdown, DateTimeInput, DropdownItem };
    setup() {
        super.setup();
        this.orm = useService('orm')
        this.state = useState({
            selectedyear : 2026,
            selectedmonth : String,
            filter : false,
        });
        this._fetch_data();
  }
  async getYear(){
        console.log(this.state.selectedyear,this.state.selectedmonth)
        this.state.filter = true
        this._fetch_data()
  }
  async getMonth(){
        console.log(this.state.selectedmonth,this.state.selectedyear)
        this.state.filter = true
        this._fetch_data()
  }
  async _fetch_data(){
        if (this.state.filter == false) {
            var result = await this.orm.call("stock.picking", "get_tiles_data", [], {'month' : false, 'year': false});
        }
        else{
            var result = await this.orm.call("stock.picking", "get_tiles_data", [], {'month' : this.state.selectedmonth, 'year': this.state.selectedyear});
        }
        await  loadJS(["/web/static/lib/Chart/Chart.js"]);
        var incoming = document.getElementById('incoming_data').getContext('2d');
        var myChart = new Chart(incoming, {
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
        var myChart = new Chart(outgoing, {
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
        var myChart = new Chart(outgoing, {
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
        var myChart = new Chart(outgoing, {
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
        var myChart = new Chart(outgoing, {
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
        var myChart = new Chart(outgoing, {
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
        var myChart = new Chart(outgoing, {
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
        var myChart = new Chart(outgoing, {
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
}
InventoryDashboard.template = "inventory_dashboard.InventoryDashboard";
actionRegistry.add("stock_dashboard_tag", InventoryDashboard);
