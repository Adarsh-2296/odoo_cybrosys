# -*- coding: utf-8 -*-
from odoo import fields,models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_vip = fields.Boolean(string='Vip')
    vip_discount = fields.Float(string='Vip Discount')
    is_vip_discount = fields.Boolean(string='Vip Discount',compute='_compute_is_vip_discount')

    def _compute_is_vip_discount(self):
        """To get the value of the field(is_vip_discount) in the settings of sales """
        self.is_vip_discount = self.env['ir.config_parameter'].sudo().get_param('sale.is_vip_discount')