# -*- coding: utf-8 -*-
from odoo import fields,models

class ResUsers(models.Model):
    _inherit = 'res.users'

    max_tasks = fields.Integer(string='Maximum Number of Tasks')
    number_of_tasks = fields.Integer(compute='_compute_number_of_tasks', string='Number of Tasks')

    def _compute_number_of_tasks(self):
        self.number_of_tasks = self.env['project.task'].search_count([('user_ids','in',self.ids),('is_closed', '=', False)])




