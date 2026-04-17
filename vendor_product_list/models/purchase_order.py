# -*- coding: utf-8 -*-
from odoo import fields,models,api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_vendor_products = fields.Boolean(string="Vendor Products")
    is_vendor_products_settings = fields.Boolean(compute='_compute_is_vendor_products_settings')

    def _compute_is_vendor_products_settings(self):
        """To get the value of the field(is_vendor_products_settings) in the settings of purchase"""
        self.is_vendor_products_settings = self.env['ir.config_parameter'].sudo().get_param(
            'purchase.is_vendor_products_settings')