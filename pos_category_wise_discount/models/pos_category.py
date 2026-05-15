# -*- coding: utf-8 -*-
from odoo import fields, models, api

class PosCategory(models.Model):
    _inherit = 'pos.category'

    discount_limit = fields.Integer(string="Discount Limit")
    is_discount_limit = fields.Boolean(string="Discount Limit",compute="_compute_is_discount_limit")

    def _compute_is_discount_limit(self):
        self.is_discount_limit = False
        shops = self.env['pos.config'].search([])
        category = shops.mapped('pos_category_ids.id')
        if self.id in category:
            self.is_discount_limit = True

    @api.model
    def _load_pos_data_fields(self, config_id):
        """
        Adds the 'pos_rating' field to the list of fields loaded into the POS.
        """
        data = super()._load_pos_data_fields(config_id)
        data += ['discount_limit']
        return data
