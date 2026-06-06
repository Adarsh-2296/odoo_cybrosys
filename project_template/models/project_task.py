# -*- coding: utf-8 -*-
from odoo import models,Command,fields

class ProjectTemplate(models.Model):
    _inherit = 'project.task'

    task_template_id = fields.Many2one('task.template',string='Task Template')


    def action_create_task_template(self):
        task_template = self.env['task.template'].create({
            'name': self.name,
            'user_ids': [Command.link(user.id) for user in self.user_ids],
            'partner_id': self.partner_id.id,
            'date_deadline': self.date_deadline,
            'priority': self.priority,
            'description': self.description,
        })
        if self.child_ids:
            for rec in self.child_ids:
                print(rec)
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'task.template',
            'res_id': task_template.id,
        }