# -*- coding: utf-8 -*-
from addons.website_sale_loyalty.controllers import delivery
from odoo import fields,models,_,Command

class ResPartner(models.Model):
    _inherit = 'account.move'

    delivery_count = fields.Integer(string='Delivery Count',compute='_compute_delivery_count')

    def _compute_delivery_count(self):
        source_orders = self.line_ids.sale_line_ids.order_id
        for rec in self:
            rec.delivery_count = len(source_orders.picking_ids)

    def delivery_invoice_smart_button(self):
        source_orders = self.line_ids.sale_line_ids.order_id
        delivery_id = source_orders.mapped('picking_ids.id')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Delivery',
            'view_mode': 'list,form',
            'res_model': 'stock.picking',
            'domain': [('id', 'in', delivery_id)],
            'context': "{'create': False}"
        }

