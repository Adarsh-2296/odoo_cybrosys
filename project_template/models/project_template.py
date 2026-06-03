# -*- coding: utf-8 -*-
from odoo import models,fields,Command

class ProjectTemplate(models.Model):
    _name = 'project.template'
    _description = 'Project Template'

    name = fields.Char(required=True)
    task_ids = fields.One2many('task.template', 'project_template_id', string='Tasks')
    partner_id = fields.Many2one('res.partner', string='Customer', bypass_search_access=True, tracking=True,
                                 domain="['|', ('company_id', '=?', company_id), ('company_id', '=', False)]",
                                 index='btree_not_null')
    date_start = fields.Date(string='Start Date', copy=False)
    date = fields.Date(string='Expiration Date', copy=False, index=True, tracking=True,
                       help="Date on which this project ends. The timeframe defined on the project is taken into account when viewing its planning.")
    allow_task_dependencies = fields.Boolean('Task Dependencies',)
    allow_milestones = fields.Boolean('Milestones', )
    allow_recurring_tasks = fields.Boolean('Recurring Tasks', )
    tag_ids = fields.Many2many('project.tags', string='Tags')
    task_properties_definition = fields.PropertiesDefinition('Task Properties')

    def action_create_project(self):
        print('done')
        lines = []
        if self.task_ids:
            for i in self.mapped('task_ids.name'):
                lines.append(self.env['project.task'].create({"name": i}).id)
        project = self.env['project.project'].create({
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
            'res_model': 'project.project',
            'res_id': project.id,
        }