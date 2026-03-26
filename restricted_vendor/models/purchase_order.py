# -*- coding: utf-8 -*-
from odoo import fields,models,api
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_restricted = fields.Boolean(string="Purchase Restricted")
    restricted_count = fields.Integer(related='partner_id.restricted_count',string="Restricted Count")
    is_vendor_restricted = fields.Boolean(compute='_compute_order_line_limit', string="Order Line Count")

    @api.depends('is_vendor_restricted')
    def _compute_order_line_limit(self):
        print('test')
        """To get the value of the field(order_line_limit) in the settings of purchase """
        self.is_vendor_restricted = self.env['ir.config_parameter'].sudo().get_param('purchase.order_line_limit')

    def button_confirm(self):
        """Raise User Error if the order line has more items than specified amount"""
        if self.partner_id.is_restricted:
            if self.is_vendor_restricted:
                if self.is_restricted:
                    order_line_count = len(self.order_line)
                    if order_line_count > self.restricted_count:
                        raise UserError('Cannot add more than ' +str(self.restricted_count) + ' items in the order line, Right now there is '+ str(order_line_count))
                    else:
                        return super().button_confirm()
        return super().button_confirm()


