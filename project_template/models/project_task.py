# -*- coding: utf-8 -*-
from odoo import models

class ProjectTemplate(models.Model):
    _inherit = 'project.task'


    def action_create_task_template(self):
        print('done')
        task_template = self.env['task.template'].create({
            'name': self.name,
        })
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'task.template',
            'res_id': task_template.id,
        }