# -*- coding: utf-8 -*-
from odoo import api, fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    is_restrict_payment = fields.Boolean(string='Restrict Payments for Users',)