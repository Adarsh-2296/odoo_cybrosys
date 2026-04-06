# -*- coding: utf-8 -*-
from odoo import fields,models

class ProjectProject(models.Model):
    _inherit = 'project.project'

    project_sale_order_id = fields.Many2one('sale.order',string='Sale Order',readonly=True)