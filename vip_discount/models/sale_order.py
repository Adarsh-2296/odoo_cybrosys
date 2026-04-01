# -*- coding: utf-8 -*-
from odoo import fields,models,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_vip = fields.Boolean(string='Vip',related='partner_id.is_vip')
    vip_discount = fields.Float(string='Vip Discount',related='partner_id.vip_discount')
    is_vip_discount = fields.Boolean(string='Vip Discount', compute='_compute_is_vip_discount')

    def _compute_is_vip_discount(self):
        """To get the value of the field(is_vip_discount) in the settings of sales """
        self.is_vip_discount = self.env['ir.config_parameter'].sudo().get_param('sale.is_vip_discount')

    def onchange_vip_discount(self):
        for rec in self:
            if rec.is_vip_discount:
                if rec.is_vip:
                    order_line_discount = rec.mapped('order_line.discount')
                    for i in range(len(order_line_discount)):
                        rec.order_line.discount = rec.partner_id.vip_discount
