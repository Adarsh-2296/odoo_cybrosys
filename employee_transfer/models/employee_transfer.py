# -*- coding: utf-8 -*-
from odoo import fields,models,api,_
from odoo.exceptions import  AccessError


class EmployeeTransfer(models.Model):
    _name = 'employee.transfer'
    _description = 'Employee Transfer'
    _rec_name = 'sequence_number'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence_number = fields.Char( readonly=True, tracking=True,copy=False,default='New')
    company_from_id = fields.Many2one('res.company',string='Company From',compute='_compute_company_from_id',store=True)
    company_to_id = fields.Many2one('res.company',string='Company To',required=True, domain ="[('id', 'not in', company_from_id)]",tracking=True)
    state = fields.Selection([('draft','Draft'),('to_approve','To Approve'),('approved','Approved'),('rejected','Rejected')],default='draft',tracking=True)
    employee_id = fields.Many2one('hr.employee',string='Employee',required=True)
    user_id = fields.Many2one('res.users',string='Approver',tracking=True,required=True,domain="[('share','=',False),('active','=',True)]")
    date = fields.Date(string='Date', default=fields.Date.today(),compute='_compute_date_',store=True,tracking=True)
    approved_date = fields.Date(string='Approved Date',compute='_compute_approved_date',store=True,tracking=True)
    active = fields.Boolean(string='Active',default=True)

    @api.depends('employee_id')
    def _compute_company_from_id(self):
        """compute employee's company"""
        for record in self:
            record.company_from_id = False
            if record.employee_id:
                record.company_from_id = record.employee_id.company_id

    @api.depends('state')
    def _compute_date_(self):
        """compute date of employee transfer"""
        for record in self:
            if record.state == 'to_approve':
                record.write({ 'date' : fields.Date.today() })
            else:
                pass

    @api.depends('state')
    def _compute_approved_date(self):
        """compute approved date of employee transfer"""
        for record in self:
            if record.state == 'approved':
                record.write({ 'approved_date' : fields.Date.today() })
            elif record.state == 'to_approve':
                record.write({ 'approved_date' : False })
            else:
                record.write({'approved_date': False})

    def action_approve(self):
        """Approve the employee's transfer request"""
        if self.env.user == self.user_id:
            self.write({'state' : 'approved' })
            filtered_companies = self.company_to_id
            self.employee_id.write({ 'company_id' : filtered_companies})
        else:
            raise AccessError("You are not allowed to approve this employee transfer.")

    def action_reject(self):
        """Reject the employee's transfer request"""
        if self.env.user == self.user_id:
            self.write({'state' : 'rejected' })
        else:
            raise AccessError("You are not allowed to approve this employee transfer.")

    def action_submit(self):
        """Submit the transfer request"""
        self.write({'state' : 'to_approve' })
        template = self.env.ref("employee_transfer.email_template_employee_transfer")
        email_values = {'email_from': self.env.user.email}
        print(email_values)
        template.send_mail(self.id, force_send=True, email_values=email_values)

    @api.model_create_multi
    def create(self, vals_list):
        """Create sequence number"""
        for vals in vals_list:
            if vals.get('sequence_number', _('New')) == _('New'):
                vals['sequence_number'] = (self.env['ir.sequence'].next_by_code('employee.transfer'))
        return super().create(vals_list)