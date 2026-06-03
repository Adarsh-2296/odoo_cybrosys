# -*- coding: utf-8 -*-
from odoo import models,fields

class ProjectTemplate(models.Model):
    _name = 'task.template'
    _description = 'Task Template'

    name = fields.Char(required=True)
    project_template_id = fields.Many2one('project.template',string='Project Template')

    def action_create_task(self):
        print('done')
        task = self.env['project.task'].create({
            'name': self.name,
        })
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'project.task',
            'res_id': task.id,
        }