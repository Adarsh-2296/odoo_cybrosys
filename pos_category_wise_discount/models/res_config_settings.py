# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_is_discount_limit = fields.Boolean(config_parameter="pos_category_wise_discount.pos_is_discount_limit",string="Discount Limit",related="pos_config_id.is_discount_limit",readonly=False)
    pos_category_id = fields.Many2many('pos.category',config_parameter="pos_category_wise_discount.pos_category_id",related='pos_config_id.pos_category_id',relation='rel_point_of_sale_pos_category_rel',
                                        column1 = 'pos_category_id',
                                        column2 = 'point_of_sale_id',
                                        readonly=False,string="Category")