# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_vip_discount = fields.Boolean(config_parameter="sale.is_vip_discount",string="VIP Discount")