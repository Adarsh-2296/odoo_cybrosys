# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_restrict_payment = fields.Boolean(config_parameter="pos_rating.is_restrict_payment",string="Restrict Payment")