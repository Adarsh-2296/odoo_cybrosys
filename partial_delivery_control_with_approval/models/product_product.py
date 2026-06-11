from odoo import fields, models,api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_allow_partial_delivery = fields.Boolean(string='Allow Partial Delivery')