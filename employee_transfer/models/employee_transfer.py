# -*- coding: utf-8 -*-
from odoo import fields,models,api,_
from openpyxl.worksheet import related


class EmployeeTransfer(models.Model):
    _name = 'employee.transfer'
    _description = 'Employee Transfer'
    _rec_name = 'sequence_number'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence_number = fields.Char( readonly=True, tracking=True,copy=False,default='New')
    company_from_id = fields.Many2one('res.company',string='Company From',required=True,related='employee_id.company_id')
    user_company_id = fields.Many2one('res.company',string='Company To',related='employee_id.company_id')
    company_to_id = fields.Many2one('res.company',string='Company To',required=True, domain ="[('id', 'not in', user_company_id)]",tracking=True)
    state = fields.Selection([('draft','Draft'),('to_approve','To Approve'),('approved','Approved'),('rejected','Rejected')],default='draft',tracking=True)
    employee_id = fields.Many2one('hr.employee',string='Employee',required=True)
    approver = fields.Many2one('res.users',string='Approver',required=True,tracking=True)
    date = fields.Date(string='Date', default=fields.Date.today(),compute='_compute_date_',store=True,tracking=True)
    approved_date = fields.Date(string='Approved Date',compute='_compute_approved_date',store=True,tracking=True)

    @api.depends('state')
    def _compute_date_(self):
        """compute date of employee transfer"""
        for record in self:
            if record.state == 'to_approve':
                record.date = fields.Date.today()
            else:
                pass

    @api.depends('state')
    def _compute_approved_date(self):
        """compute approved date of employee transfer"""
        for record in self:
            if record.state == 'approved':
                record.approved_date = fields.Date.today()
            elif record.state == 'to_approve':
                record.approved_date = False
            else:
                pass


    def action_approve(self):
        """Approve the employee's transfer request"""
        self.write({'state' : 'approved' })
        filtered_companies = self.company_to_id
        print(filtered_companies)
        self.employee_id.write({ 'company_id' : filtered_companies})

    def action_reject(self):
        """Reject the employee's transfer request"""
        self.write({'state' : 'rejected' })

    def action_submit(self):
        """Submit the transfer request"""
        self.write({'state' : 'to_approve' })

    @api.model_create_multi
    def create(self, vals_list):
        """Create sequence number"""
        for vals in vals_list:
            if vals.get('sequence_number', _('New')) == _('New'):
                vals['sequence_number'] = (self.env['ir.sequence'].next_by_code('employee.transfer'))
        return super().create(vals_list)