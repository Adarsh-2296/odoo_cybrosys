# -*- coding: utf-8 -*-
from odoo import fields,models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_restricted = fields.Boolean(string="Restricted")
    restricted_count = fields.Integer(string="Restricted Count")
    is_vendor_restricted = fields.Boolean(compute='_compute_order_line_limit',string="Order Line Count")

    def _compute_order_line_limit(self):
        """To get the value of the field(order_line_limit) in the settings of purchase """
        self.is_vendor_restricted = self.env['ir.config_parameter'].sudo().get_param('purchase.order_line_limit')







