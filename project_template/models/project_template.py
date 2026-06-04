# -*- coding: utf-8 -*-
from odoo import models,fields,Command,api

class ProjectTemplate(models.Model):
    _name = 'project.template'
    _description = 'Project Template'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    task_ids = fields.One2many('task.template', 'project_template_id', string='Tasks')
    partner_id = fields.Many2one('res.partner', string='Customer',)
    user_id = fields.Many2one('res.users', string='Project Manager',domain=[('share','=',False),('active','=',True)])
    date_start = fields.Date(string='Start Date', copy=False)
    date = fields.Date(string='Expiration Date', copy=False, index=True, tracking=True,
                       help="Date on which this project ends. The timeframe defined on the project is taken into account when viewing its planning.")
    allow_task_dependencies = fields.Boolean('Task Dependencies',)
    allow_milestones = fields.Boolean('Milestones',)
    allow_recurring_tasks = fields.Boolean('Recurring Tasks',)
    tag_ids = fields.Many2many('project.tags', string='Tags')
    company_id = fields.Many2one('res.company', string='Company', tracking=True)
    description = fields.Html(string='Description')
    privacy_visibility = fields.Selection([
        ('followers', 'Invited internal users'),
        ('invited_users', 'Invited internal and portal users'),
        ('employees', 'All internal users'),
        ('portal', ' All internal users and invited portal users'),
    ],
        string='Visibility', required=True,
        default='portal',
        tracking=True,)
    project_count = fields.Integer(string='Project Count',compute='_compute_project_count')
    project_ids = fields.One2many('project.project', 'project_template_id', string='Projects')
    allow_billable = fields.Boolean(string='Billable',)
    type_ids = fields.Many2many('project.task.type', 'project_template_task_type_rel', 'project_template_id', 'type_template_id',
                                string='Tasks Stages')
    is_favorite = fields.Boolean(string='Show Project on Dashboard')


    def action_create_project(self):
        project = self.env['project.project'].create({
            'project_template_id': self.id,
            'name': self.name,
            'user_id': self.user_id.id,
            'date_start': self.date_start,
            'date': self.date,
            'partner_id': self.partner_id.id,
            'allow_task_dependencies': self.allow_task_dependencies,
            'allow_milestones': self.allow_milestones,
            'allow_recurring_tasks': self.allow_recurring_tasks,
            'tag_ids': [Command.link(tag.id) for tag in self.tag_ids],
            'company_id': self.company_id.id,
            'description': self.description,
            'privacy_visibility': self.privacy_visibility,
            'allow_billable': self.allow_billable,
            'type_ids': [Command.link(stage.id) for stage in self.type_ids],
            'is_favorite': self.is_favorite,
        })
        if self.task_ids:
            tasks = self.task_ids.filtered(lambda task: not task.parent_id)
            for i in tasks:
                self.env['project.task'].create({"name": i.name,
                                                               'task_template_id': i.id,
                                                               'user_ids': [Command.link(user.id) for user in i.user_ids],
                                                               'project_id': project.id,
                                                               'partner_id': i.partner_id.id,
                                                               'date_deadline': i.date_deadline,
                                                               'priority': i.priority,
                                                               'description': i.description,
                                                               'child_ids': [Command.create(task.name) for task in i.child_ids],
                                                               })
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'project.project',
            'res_id': project.id,
        }

    @api.depends('project_ids')
    def _compute_project_count(self):
        """To compute Project count for a particular Template"""
        for record in self:
            record.project_count = len(record.project_ids)


    def project_smart_button(self):
        """list of Projects created by this template"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'project',
            'view_mode': 'list,form',
            'res_model': 'project.project',
            'domain': [('project_template_id', '=', self.id)],
            'context': "{'create': False}"
        }