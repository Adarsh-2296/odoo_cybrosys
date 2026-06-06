# -*- coding: utf-8 -*-
from odoo import models,Command,fields

class ProjectTemplate(models.Model):
    _inherit = 'project.project'

    project_template_id = fields.Many2one('project.template',string="Project")


    def action_create_project_template(self):
        project_template = self.env['project.template'].create({
            'name': self.name,
            'date_start': self.date_start,
            'partner_id': self.partner_id.id,
            'date': self.date,
            'allow_task_dependencies': self.allow_task_dependencies,
            'allow_milestones': self.allow_milestones,
            'allow_recurring_tasks': self.allow_recurring_tasks,
            'tag_ids': [Command.link(tag.id) for tag in self.tag_ids],
            'user_id': self.user_id.id,
            'company_id': self.company_id.id,
            'description': self.description,
            'privacy_visibility': self.privacy_visibility,
            'type_ids': [Command.link(stage.id) for stage in self.type_ids],
            'is_favorite': self.is_favorite,
        })
        if self.task_ids:
            tasks_no_parent = self.task_ids.filtered(lambda task: not task.parent_id)
            task_template_dict = {}
            flag = False
            for i in tasks_no_parent:
                child_ids = [Command.create({'name' : task.name,
                                             'user_ids': [Command.link(user.id) for user in task.user_ids],
                                             'partner_id': task.partner_id.id,
                                             'project_template_id': project_template.id,
                                             'date_deadline': task.date_deadline,
                                             'priority': task.priority,
                                             'description': task.description,}) for task in i.child_ids]
                task_template = self.env['task.template'].create({"name": i.name,
                                                  'user_ids': [Command.link(user.id) for user in i.user_ids],
                                                  'partner_id': i.partner_id.id,
                                                  'project_template_id': project_template.id,
                                                  'date_deadline': i.date_deadline,
                                                  'priority': i.priority,
                                                  'description': i.description,
                                                  'child_ids': child_ids})
                for child in range(len(i.child_ids)):
                    if i.child_ids[child].child_ids:
                        task_template_dict.update({task_template.child_ids[child] : i.child_ids[child].child_ids})
                        flag = True
            sub_dict = task_template_dict
            while (flag):
                flag = False
                task_template_dict = sub_dict
                sub_dict = {}
                for rec in range(len(list(task_template_dict.keys()))):
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
                                task = list(task_template_dict.keys())[rec].child_ids.filtered(lambda task: task.name == i.name)
                                sub_dict.update({task : i.child_ids})
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'project.template',
            'res_id': project_template.id,
        }