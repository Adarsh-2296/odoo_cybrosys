# -*- coding: utf-8 -*-
from odoo import models,fields,Command,api

class ProjectTemplate(models.Model):
    _name = 'task.template'
    _description = 'Task Template'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    project_template_id = fields.Many2one('project.template',string='Project Template')
    user_ids = fields.Many2many('res.users',string='Assignees',domain=[('share','=',False)])
    partner_id = fields.Many2one('res.partner', string='Customer', )
    date_deadline = fields.Datetime(string='Deadline')
    task_count = fields.Integer(string='Tasks',compute='_compute_task_count')
    task_ids = fields.One2many('project.task', 'task_template_id', string='Tasks')
    priority = fields.Selection([
        ('0', 'Low priority'),
        ('1', 'Medium priority'),
        ('2', 'High priority'),
        ('3', 'Urgent'),
    ], default='0', index=True, string="Priority", tracking=True)
    description = fields.Html(string='Description')
    parent_id = fields.Many2one('task.template', string='Parent Task', index=True,
                                domain="['!', ('id', 'child_of', id)]", tracking=True)
    child_ids = fields.One2many('task.template', 'parent_id', string="Sub-tasks")

    def action_create_task(self):
        task_template_dict = {}
        if self.project_template_id:
            project = self.env['project.project'].create({'name':self.project_template_id.name})
            task = self.env['project.task'].sudo().create({
                'task_template_id': self.id,
                'name': self.name,
                'user_ids': [Command.link(user.id) for user in self.user_ids],
                'project_id': project.id,
                'partner_id': self.partner_id.id,
                'date_deadline': self.date_deadline,
                'priority': self.priority,
                'description': self.description,
            })
            if self.child_ids:
                child_ids = [Command.create({'name': task.name,
                                             'user_ids': [Command.link(user.id) for user in task.user_ids],
                                             'partner_id': task.partner_id.id,
                                             'date_deadline': task.date_deadline,
                                             'project_id': project.id,
                                             'priority': task.priority,
                                             'description': task.description, }) for task in self.child_ids]
                task.update({'child_ids': child_ids})
                for rec in range(len(self.child_ids)):
                    if self.child_ids[rec].child_ids:
                        flag = True
                        task_template_dict.update({task.child_ids[rec]: self.child_ids[rec].child_ids})
                        print('child', self.child_ids[rec].child_ids)
            sub_dict = task_template_dict
            print(task_template_dict)
            while (flag):
                flag = False
                task_template_dict = sub_dict
                sub_dict = {}
                for rec in range(len(list(task_template_dict.keys()))):
                    print(list(task_template_dict.keys()))
                    print(task_template_dict[list(task_template_dict.keys())[rec]])
                    child_templates = [Command.create({'name': task.name,
                                                       'user_ids': [Command.link(user.id) for user in task.user_ids],
                                                       'partner_id': task.partner_id.id,
                                                       'project_id': project.id,
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
            self.env['project.task'].sudo().create({
                'task_template_id': self.id,
                'name': self.name,
                'user_ids': [Command.link(user.id) for user in self.user_ids],
                'partner_id': self.partner_id.id,
                'date_deadline': self.date_deadline,
                'priority': self.priority,
                'description': self.description,
            })
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'project.task',
            'res_id': task.id,
        }

    @api.depends('task_ids')
    def _compute_task_count(self):
            """To compute Project count for a particular Template"""
            for record in self:
                record.task_count = len(record.task_ids)

    def task_smart_button(self):
        """list of Tasks created by this template"""
        return {
                'type': 'ir.actions.act_window',
                'name': 'task',
                'view_mode': 'list,form',
                'res_model': 'project.task',
                'domain': [('task_template_id', '=', self.id)],
                'context': "{'create': False}"
            }
