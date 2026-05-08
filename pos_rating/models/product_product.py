# -*- coding: utf-8 -*-
from odoo import fields,models,api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    pos_rating = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5')],default='1',string="Pos Rating")

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pos_rating = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5')],default='1',string="Pos Rating")

    @api.model
    def _load_pos_data_fields(self, config_id):
        """
        Adds the 'pos_rating' field to the list of fields loaded into the POS.
        """
        data = super()._load_pos_data_fields(config_id)
        data += ['pos_rating']
        return data