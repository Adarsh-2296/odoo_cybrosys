# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_is_clear_order_line_button = fields.Boolean(string="Clear Order Line Button",related="pos_config_id.is_clear_order_line_button",readonly=False)