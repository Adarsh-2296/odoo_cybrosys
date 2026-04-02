# -*- coding: utf-8 -*-
from odoo import models,api
from odoo.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.onchange('user_ids')
    def onchange_user_ids(self):
        a = self.mapped('user_ids')
        for i in range(len(a)):
            if a[i].number_of_tasks > a[i].max_tasks:
                raise UserError('This User Already has '+ str(a[i].number_of_tasks) + ' Cannot assign more tasks')
