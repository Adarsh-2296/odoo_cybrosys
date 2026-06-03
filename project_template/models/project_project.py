# -*- coding: utf-8 -*-
from odoo import models

class ProjectTemplate(models.Model):
    _inherit = 'project.project'


    def action_create_project_template(self):
        print('done')
        lines = []
        if self.task_ids:
            for i in self.mapped('task_ids.name'):
                lines.append(self.env['task.template'].create({"name": i}).id)
        project_template = self.env['project.template'].create({
            'name': self.name,
            'tasks': lines,
            'date_start': self.date_start,
            'date': self.date,
            'allow_task_dependencies': self.allow_task_dependencies,
            'allow_milestones': self.allow_milestones,
            'allow_recurring_tasks': self.allow_recurring_tasks,
            'tag_ids': self.tag_ids,
            'task_properties_definition': self.task_properties_definition,
        })
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'project.template',
            'res_id': project_template.id,
        }