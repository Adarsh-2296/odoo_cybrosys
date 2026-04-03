# -*- coding: utf-8 -*-
from odoo import fields,models,api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def redirect_to_company_transfer(self):
        """Create transfer from Machine form"""
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'employee.transfer',
            'view_mode': 'form',
            'target': 'self',
            'context': {
                'default_employee_id': self.id,
            },
        }