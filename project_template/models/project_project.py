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
            created_tasks = []
            print('tasks_child_ids',tasks_no_parent)
            task_template_dict = {}
            count = 1
            task_template = False
            flag = False
            for i in tasks_no_parent:
                child_ids = [Command.create({'name' : task.name,
                                             'user_ids': [Command.link(user.id) for user in task.user_ids],
                                             'partner_id': task.partner_id.id,
                                             'project_template_id': project_template.id,
                                             'date_deadline': task.date_deadline,
                                             'priority': task.priority,
                                             'description': task.description,}) for task in i.child_ids]
                print('child_ids',child_ids)
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
                        print('child ids',task_template.child_ids[child])
                        # task_template.child_ids[child].update({'child_ids': [Command.create({'name' : task.name,
                        #                      'user_ids': [Command.link(user.id) for user in task.user_ids],
                        #                      'partner_id': task.partner_id.id,
                        #                      'project_template_id': project_template.id,
                        #                      'date_deadline': task.date_deadline,
                        #                      'priority': task.priority,
                        #                      'description': task.description,}) for task in i.child_ids[child].child_ids]})
                        task_template_dict.update({task_template.child_ids[child] : i.child_ids[child].child_ids})
                        flag = True
            print('task_template_dict',task_template_dict)
            for rec in range(len(list(task_template_dict.keys()))):
                    print(rec)
                    print(task_template_dict[list(task_template_dict.keys())[rec]])
                    child_templates = [Command.create({'name': task.name,
                                                    'user_ids': [Command.link(user.id) for user in task.user_ids],
                                                   'partner_id': task.partner_id.id,
                                                   'project_template_id': project_template.id,
                                                   'date_deadline': task.date_deadline,
                                                   'priority': task.priority,
                                                   'description': task.description, })
                                   for task in task_template_dict[list(task_template_dict.keys())[rec]]]
                    task_template.child_ids[rec].update({'child_ids': child_templates})
                    print(child_templates)
                # if child_templates:
                #     for i in child_templates:
                #         if i.child_ids:
                #         print(i)



            #         task_template_dict.update({task_template.id: len(i.child_ids.filtered(lambda task: not task.child_ids))})
            # print('task_template_dict',task_template_dict)
            # print('created_tasks',created_tasks)
            # tasks_parent_id = self.task_ids.filtered(lambda task: task.parent_id and (task not in created_tasks))
            # print('tasks_parent_id',tasks_parent_id)
            # for i in tasks_parent_id:
            #     keys = list(task_template_dict.keys())
            #     first_key = keys[0]
            #     print(first_key)
            #     task_template = self.env['task.template'].create({"name": i.name,
            #                                                       'user_ids': [Command.link(user.id) for user in
            #                                                                    i.user_ids],
            #                                                       'parent_id': int(first_key),
            #                                                       'partner_id': i.partner_id.id,
            #                                                       'project_template_id': project_template.id,
            #                                                       'date_deadline': i.date_deadline,
            #                                                       'priority': i.priority,
            #                                                       'description': i.description,
            #                                                       'child_ids': [Command.create({'name': task.name,
            #                                                                                     'user_ids': [
            #                                                                                         Command.link(
            #                                                                                             user.id) for
            #                                                                                         user in
            #                                                                                         task.user_ids],
            #                                                                                     'partner_id': task.partner_id.id,
            #                                                                                     'project_template_id': project_template.id,
            #                                                                                     'date_deadline': task.date_deadline,
            #                                                                                     'priority': task.priority,
            #                                                                                     'description': task.description,
            #                                                                                     }) for task in
            #                                                                     i.child_ids.filtered(
            #                                                                         lambda task: not task.child_ids)]})
            #     if i.child_ids:
            #         task_template_dict.update({task_template.id: len(i.child_ids.filtered(lambda task: not task.child_ids))})
            #         print(task_template_dict)
            #     if count == task_template_dict[first_key]:
            #         print(count)
            #         count = 0
            #         print(task_template_dict)
            #         task_template_dict.pop(first_key)
            #     count += 1
            #     if i.child_ids:
            #         task_template_dict.update({task_template.id: len(i.child_ids)})

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'project.template',
            'res_id': project_template.id,
        }