# -*- coding: utf-8 -*-
from odoo import fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    is_discount_limit = fields.Boolean(string="Discount Limit")
    pos_category_id = fields.Many2many('pos.category',relation='rel_point_of_sale_pos_category_rel',
                                        column1 = 'pos_category_id',
                                        column2 = 'point_of_sale_id',)