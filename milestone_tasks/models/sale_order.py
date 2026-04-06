# -*- coding: utf-8 -*-
from odoo import fields,models

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def create_project(self):
        """Button creates a project with sale order name and tasks on the basis of sale order line and the new field milestone"""
        is_project_created = self.env['project.project'].search([('project_sale_order_id','=',self.id)])
        if is_project_created:
            existing_tasks = is_project_created[0].task_ids
            order_lines_milestone = set(self.mapped('order_line.milestone'))
            order_lines_milestone = list(order_lines_milestone)
            for rec in order_lines_milestone:
                self.env['project.task'].create({
                    'name': 'Milestone ' + str(rec),
                    'project_id': is_project_created[0].id,
                    'partner_id': self.partner_id.id,
                    'task_sale_order_id': self.id,
                })

            for rec in order_lines_milestone:
                milestone = self.mapped('order_line').filtered(lambda x: x.milestone == rec)
                tasks = is_project_created[0].task_ids.filtered(lambda x: x not in existing_tasks)
                print(is_project_created[0].task_ids)
                print('tasks', tasks)
                for record in milestone:
                    for task in tasks:
                        if task.name == 'Milestone ' + str(record.milestone):
                            self.env['project.task'].create({
                                'name': 'Milestone ' + str(rec) + ' - ' + record.product_id.name,
                                'project_id': is_project_created[0].id,
                                'partner_id': self.partner_id.id,
                                'parent_id': task.id
                            })
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'project.project',
                    'view_mode': 'form',
                    'res_id': is_project_created[0].id,
                    'target': 'self',
                }
        else:
            project = self.env['project.project'].create({
            'name': self.name,
            'allow_billable': True,
            'project_sale_order_id' : self.id,
            })
            order_lines_milestone = set(self.mapped('order_line.milestone'))
            order_lines_milestone = list(order_lines_milestone)
            for rec in order_lines_milestone:
                self.env['project.task'].create({
                'name' : 'Milestone ' + str(rec),
                'project_id': project.id,
                'partner_id' : self.partner_id.id,
                'task_sale_order_id': self.id,
            })

            for rec in order_lines_milestone:
                milestone = self.mapped('order_line').filtered(lambda x: x.milestone == rec)
                print(project.task_ids)
                for record in milestone:
                    for task in project.task_ids:
                        if task.name == 'Milestone ' + str(record.milestone):
                            self.env['project.task'].create({
                            'name': 'Milestone ' + str(rec) + ' - ' + record.product_id.name,
                            'project_id': project.id,
                            'partner_id': self.partner_id.id,
                            'parent_id' : task.id
                        })
            return {
            'type': 'ir.actions.act_window',
            'res_model': 'project.project',
            'view_mode': 'form',
            'res_id': project.id,
            'target': 'current',

        }
