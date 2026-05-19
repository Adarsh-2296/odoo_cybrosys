# -*- coding: utf-8 -*-
from odoo import fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    is_clear_order_line_button = fields.Boolean(string="Clear Order Line")