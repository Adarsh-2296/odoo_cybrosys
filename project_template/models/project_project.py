# -*- coding: utf-8 -*-
from odoo import models,Command,fields

class ProjectTemplate(models.Model):
    _inherit = 'project.project'

    project_template_id = fields.Many2one('project.template',string="Project")


    def action_create_project_template(self):
        """button action to create project template"""
        tasks = [Command.create({"name": i.name,
                         'user_ids': [Command.link(user.id) for user in
                                      i.user_ids],
                         'partner_id': i.partner_id.id,
                         'date_deadline': i.date_deadline,
                         'priority': i.priority,
                         'description': i.description,
                         }) for i in self.task_ids.filtered(lambda task: not task.parent_id)]
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
            'task_ids': tasks,
        })

        def create_child_tasks(self,task_template_dict):
            """Function to create child tasks"""
            task_template_dict_2 = task_template_dict
            task_template_dict = {}
            for rec in list(task_template_dict_2.keys()):
                child = [Command.create({'name' : task.name,
                                             'user_ids': [Command.link(user.id) for user in task.user_ids],
                                             'partner_id': task.partner_id.id,
                                             'project_template_id': project_template.id,
                                             'date_deadline': task.date_deadline,
                                             'priority': task.priority,
                                             'description': task.description,}) for task in task_template_dict_2[rec]]
                rec.update({'child_ids': child })
                for i in range(len(task_template_dict_2[rec])):
                    if task_template_dict_2[rec][i].child_ids:
                        task_template_dict.update({rec.child_ids[i]: task_template_dict_2[rec][i].child_ids})
            if task_template_dict:
                create_child_tasks(self, task_template_dict)

        if self.task_ids:
            task_template_dict = {}
            task_no_parent = self.task_ids.filtered(lambda task: not task.parent_id)
            for rec in range(len(task_no_parent)):
                if task_no_parent[rec].child_ids:
                    task_template_dict.update({project_template.task_ids[rec] : task_no_parent[rec].child_ids})
            if task_template_dict:
                create_child_tasks(self, task_template_dict)

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'project.template',
            'res_id': project_template.id,
        }