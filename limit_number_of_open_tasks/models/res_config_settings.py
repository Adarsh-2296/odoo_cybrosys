# -*- coding: utf-8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_limit_tasks = fields.Boolean(config_parameter="project.is_limit_tasks",string="Limit Tasks")