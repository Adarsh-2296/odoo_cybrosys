# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    restrict_user = fields.Boolean("Sale",config_parameter="sale.restrict_user")
    amount_limit = fields.Float(string="Amount",default=5000,store=True,config_parameter="sale.amount_limit")

