from odoo import models, api

class StockPicking(models.Model):
   _inherit = 'stock.picking'
   @api.model
   def get_tiles_data(self):
       company_id = self.env.company
       stock = self.search([('company_id', '=', company_id)])

       """Location wise"""
       location_id = self.env['stock.location'].search([('company_id', '=', company_id)])
       location = {}
       for i in location_id:
           value = i.mapped('quant_ids.product_id.name')
           location.update({i.name: len(value)})
       location_name = list(location.keys())
       location_product = list(location.values())

       """Group based on picking type"""
       picking_type_id = self.env['stock.picking.type'].search([('company_id', '=', company_id)])
       picking_type_dict = {}
       print(picking_type_id)
       for i in picking_type_id:
           value = stock.filtered(lambda j: j.picking_type_id.id == i.id)
           picking_type_dict.update({i.warehouse_id.name + ' : ' + i.name : len(value)})
       picking_type_name = list(picking_type_dict.keys())
       picking_type_count = list(picking_type_dict.values())
       print(picking_type_name)
       print(picking_type_count)

       """incoming and outgoing"""
       incoming = stock.filtered(lambda i: i.picking_type_code == "incoming")
       outgoing = stock.filtered(lambda i: i.picking_type_code == "outgoing")
       incoming_dict = {}
       outgoing_dict = {}
       for i in incoming.move_ids:
           if i.product_id.name not in incoming_dict:
               incoming_dict.update({i.product_id.name : i.product_uom_qty })
           else:
               qty = incoming_dict[i.product_id.name]
               incoming_dict.update({i.product_id.name: i.product_uom_qty + qty})
       for i in outgoing.move_ids:
           if i.product_id.name not in outgoing_dict:
               outgoing_dict.update({i.product_id.name : i.product_uom_qty })
           else:
               qty = outgoing_dict[i.product_id.name]
               outgoing_dict.update({i.product_id.name: i.product_uom_qty + qty})
       outgoing_product = list(outgoing_dict.keys())
       outgoing_qty = list(outgoing_dict.values())
       incoming_product = list(incoming_dict.keys())
       incoming_qty = list(incoming_dict.values())

       """Internal transfers (Product wise)"""
       internal = picking_type_id.filtered(lambda rec: rec.code == "internal")
       internal_transfers = stock.filtered(lambda rec: rec.picking_type_id in internal)
       internal_transfers_dict = {}
       for i in internal_transfers.move_ids:
           if i.product_id.name not in internal_transfers_dict:
               internal_transfers_dict.update({i.product_id.name : i.product_uom_qty })
           else:
               qty = internal_transfers_dict[i.product_id.name]
               internal_transfers_dict.update({i.product_id.name: i.product_uom_qty + qty})
       internal_transfers_product = list(internal_transfers_dict.keys())
       internal_transfers_qty = list(internal_transfers_dict.values())

       """Warehouse and its location"""
       warehouse_id = self.env['stock.warehouse'].search([('company_id', '=', company_id)])
       warehouse_dict = {}
       for i in warehouse_id:
           value = location_id.filtered(lambda rec: rec.warehouse_id.id == i.id).mapped('name')
           warehouse_dict.update({i.name : len(value)})
       warehouse_name = list(warehouse_dict.keys())
       warehouse_location = list(warehouse_dict.values())

       """Average expense of  a product(purchase cost + landed cost)"""
       products = self.env['product.product'].search([('is_storable', '=', True)])
       products_dict = {}
       for i in products:
           products_dict.update({ i.name : i.avg_cost })
       product_names = list(products_dict.keys())
       product_avg_cost = list(products_dict.values())

       """Inventory valuation"""
       products_dict = {}
       for i in products:
           products_dict.update({i.name: i.total_value})
       product_val_names = list(products_dict.keys())
       product_val_avg_cost = list(products_dict.values())

       return {
                'outgoing_product' : outgoing_product,
                'outgoing_qty' : outgoing_qty,
                'incoming_product' : incoming_product,
                'incoming_qty' : incoming_qty,
                'location_name' : location_name,
                'location_product' : location_product,
                'picking_type_name' : picking_type_name,
                'picking_type_count' : picking_type_count,
                'internal_transfers_product' : internal_transfers_product,
                'internal_transfers_qty' : internal_transfers_qty,
                'warehouse_name' : warehouse_name,
                'warehouse_location' : warehouse_location,
                'product_names' : product_names,
                'product_avg_cost' : product_avg_cost,
                'product_val_names' : product_val_names,
                'product_val_avg_cost' : product_val_avg_cost,
               }
