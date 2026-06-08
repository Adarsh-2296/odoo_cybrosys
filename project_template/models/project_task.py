# -*- coding: utf-8 -*-
from odoo import models,Command,fields

class ProjectTemplate(models.Model):
    _inherit = 'project.task'

    task_template_id = fields.Many2one('task.template',string='Task Template')


    def action_create_task_template(self):
        task_template_dict = {}
        flag = False
        if self.project_id:
            project_template = self.env['project.template'].create({'name': self.project_id.name,})
            task_template = self.env['task.template'].create({
                'name': self.name,
                'user_ids': [Command.link(user.id) for user in self.user_ids],
                'partner_id': self.partner_id.id,
                'project_template_id': project_template.id,
                'date_deadline': self.date_deadline,
                'priority': self.priority,
                'description': self.description,
            })
            if self.child_ids:
                child_ids = [Command.create({'name': task.name,
                                         'user_ids': [Command.link(user.id) for user in task.user_ids],
                                         'partner_id': task.partner_id.id,
                                         'date_deadline': task.date_deadline,
                                         'project_template_id': project_template.id,
                                         'priority': task.priority,
                                         'description': task.description, }) for task in self.child_ids]
                task_template.update({'child_ids': child_ids})
                for rec in range(len(self.child_ids)):
                    if self.child_ids[rec].child_ids:
                        flag = True
                        task_template_dict.update({task_template.child_ids[rec] : self.child_ids[rec].child_ids})
                        print('child', self.child_ids[rec].child_ids)
            sub_dict = task_template_dict
            print(task_template_dict)
            while(flag):
                flag = False
                task_template_dict = sub_dict
                sub_dict = {}
                for rec in range(len(list(task_template_dict.keys()))):
                    print(list(task_template_dict.keys()))
                    print(task_template_dict[list(task_template_dict.keys())[rec]])
                    child_templates = [Command.create({'name': task.name,
                                                       'user_ids': [Command.link(user.id) for user in task.user_ids],
                                                       'partner_id': task.partner_id.id,
                                                       'project_template_id': project_template.id,
                                                       'date_deadline': task.date_deadline,
                                                       'priority': task.priority,
                                                       'description': task.description, })
                                       for task in task_template_dict[list(task_template_dict.keys())[rec]]]
                    list(task_template_dict.keys())[rec].update({'child_ids': child_templates})
                    for i in task_template_dict[list(task_template_dict.keys())[rec]]:
                        if i.child_ids:
                            flag = True
                            task = list(task_template_dict.keys())[rec].child_ids.filtered(
                                lambda task: task.name == i.name)
                            sub_dict.update({task: i.child_ids})
        else:
            self.env['task.template'].create({
                'name': self.name,
                'user_ids': [Command.link(user.id) for user in self.user_ids],
                'partner_id': self.partner_id.id,
                'date_deadline': self.date_deadline,
                'priority': self.priority,
                'description': self.description,
            })
        print(task_template_dict)
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'task.template',
            'res_id': task_template.id,
        }