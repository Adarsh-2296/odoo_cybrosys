# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_vendor_products_settings = fields.Boolean(config_parameter="purchase.is_vendor_products_settings",string="PO Line Domain")