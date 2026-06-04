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
            created_tasks = tasks_child_ids = self.task_ids.filtered(lambda task: task.child_ids)
            tasks_parent_id = self.task_ids.filtered(lambda task: not task.child_ids)
            print(tasks_child_ids)
            print(tasks_parent_id)
            task_template_dict = {}
            count = 1
            for i in tasks_child_ids:
                    created_tasks += i.child_ids.filtered(lambda task: not task.child_ids)
                    task_template = self.env['task.template'].create({"name": i.name,
                                                  'user_ids': [Command.link(user.id) for user in i.user_ids],
                                                  'partner_id': i.partner_id.id,
                                                  'project_template_id': project_template.id,
                                                  'date_deadline': i.date_deadline,
                                                  'priority': i.priority,
                                                  'description': i.description,
                                                  'child_ids': [Command.create({'name' : task.name,
                                                                                'user_ids': [Command.link(user.id) for
                                                                                             user in task.user_ids],
                                                                                'partner_id': task.partner_id.id,
                                                                                'project_template_id': project_template.id,
                                                                                'date_deadline': task.date_deadline,
                                                                                'priority': task.priority,
                                                                                'description': task.description,
                                                                                }) for task in i.child_ids.filtered(lambda task: not task.child_ids)]})
                    task_template_dict.update({task_template.id: len(i.child_ids)})
            print(task_template_dict)
            print(created_tasks)
            for i in tasks_parent_id:
                keys = list(task_template_dict.keys())
                first_key = keys[0]
                task_template = self.env['task.template'].create({"name": i.name,
                                                                  'user_ids': [Command.link(user.id) for user in
                                                                               i.user_ids],
                                                                  'parent_id': task_template_dict[first_key],
                                                                  'partner_id': i.partner_id.id,
                                                                  'project_template_id': project_template.id,
                                                                  'date_deadline': i.date_deadline,
                                                                  'priority': i.priority,
                                                                  'description': i.description,
                                                                  'child_ids': [Command.create({'name': task.name,
                                                                                                'user_ids': [
                                                                                                    Command.link(
                                                                                                        user.id) for
                                                                                                    user in
                                                                                                    task.user_ids],
                                                                                                'partner_id': task.partner_id.id,
                                                                                                'project_template_id': project_template.id,
                                                                                                'date_deadline': task.date_deadline,
                                                                                                'priority': task.priority,
                                                                                                'description': task.description,
                                                                                                }) for task in
                                                                                i.child_ids.filtered(
                                                                                    lambda task: not task.child_ids)]})
                count += 1
                if count == task_template_dict[first_key]:
                    count = 1
                    task_template_dict.pop(first_key)

                if i.child_ids:
                    task_template_dict.update({task_template.id: len(i.child_ids)})

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'project.template',
            'res_id': project_template.id,
        }