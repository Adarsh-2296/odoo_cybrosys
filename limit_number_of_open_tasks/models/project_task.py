# -*- coding: utf-8 -*-
from odoo import fields,models,api
from odoo.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    is_limit_tasks = fields.Boolean(compute='_compute_is_limit_tasks')

    @api.constrains('user_ids')
    def _check_users_tasks(self):
        if self.is_limit_tasks:
            users = self.mapped('user_ids')
            for rec in users:
                if rec.number_of_tasks > users.max_tasks:
                    raise UserError('This User Already has '+ str(rec.number_of_tasks) + ' Cannot assign more tasks. The limit is '+ str(rec.max_tasks))

    def _compute_is_limit_tasks(self):
        """To get the value of the field(is_limit_tasks) in the settings of project """
        self.is_limit_tasks = self.env['ir.config_parameter'].sudo().get_param('project.is_limit_tasks')