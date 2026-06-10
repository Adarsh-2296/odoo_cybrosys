# -*- coding: utf-8 -*-
from odoo import fields,models,_,Command

class ResPartner(models.Model):
    _inherit = 'account.move'

    delivery_count = fields.Integer(string='Delivery Count',compute='_compute_delivery_count')
    delivery_ids = fields.Many2many('stock.picking', string='Delivery')

    def _compute_delivery_count(self):
        source_orders = self.line_ids.sale_line_ids.order_id
        for rec in self:
            rec.delivery_count = len(self.delivery_ids)

    def delivery_invoice_smart_button(self):
        source_orders = self.line_ids.sale_line_ids.order_id
        delivery_id = self.mapped('delivery_ids.id')
        print(delivery_id)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Delivery',
            'view_mode': 'list,form',
            'res_model': 'stock.picking',
            'domain': [('id', 'in', delivery_id)],
            'context': "{'create': False}"
        }