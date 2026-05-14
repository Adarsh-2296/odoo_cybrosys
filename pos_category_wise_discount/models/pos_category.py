# -*- coding: utf-8 -*-
from odoo import fields, models

class PosCategory(models.Model):
    _inherit = 'pos.category'

    discount_limit = fields.Integer(string="Discount Limit")
    is_discount_limit = fields.Boolean(string="Discount Limit",compute="_compute_is_discount_limit")

    def _compute_is_discount_limit(self):
        """To get the value of the field(order_line_limit) in the settings of purchase """
        pos_category_id = self.env['ir.config_parameter'].sudo().get_param('pos_category_wise_discount.pos_category_id')
        pos_is_discount_limit = self.env['ir.config_parameter'].sudo().get_param('pos_category_wise_discount.pos_is_discount_limit')
