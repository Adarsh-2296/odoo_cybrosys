# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_is_restrict_payment = fields.Boolean(related='pos_config_id.is_restrict_payment', readonly=False)

