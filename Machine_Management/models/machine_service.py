# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, Command
from odoo.exceptions import UserError

class MachineService(models.Model):
    _name = 'machine.service'
    _description = 'Model for managing Machine Service'
    _rec_name = 'sequence_no_service'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    machine_id = fields.Many2one('machine.management',string='Machine',required=True,tracking=True)
    sequence_no_service = fields.Char(string='Sequence',readonly=True)
    partner_id = fields.Many2one('res.partner',string='Customer',required=True,tracking=True)
    date = fields.Date(string='Date',required=True,tracking=True,default=fields.Date.today())
    description = fields.Text(string='Description',tracking=True)
    internal_note = fields.Text(string='Internal Note',tracking=True)
    tech_person_ids = fields.Many2many('res.users',string='Tech Person',tracking=True,required=True,domain="[('share','=',False),('active','=',True)]")
    state = fields.Selection([('open','Open'),('started','Started'),('done','Done'),('invoiced','Invoiced'),('cancel','Cancel')],default='open',tracking=True)
    company_id = fields.Many2one('res.company',string='Company',tracking=True,default=lambda self: self.env.company)
    parts_line_ids = fields.Many2many(
        'machine.management.order.line',
        string="Order Lines",domain="[('order_id','=',machine_id)]",
        copy=True)
    invoice_count = fields.Integer(string='Invoice Count',tracking=True,compute='_compute_invoice_count')
    active = fields.Boolean(string='Active',tracking=True,default=True)
    invoice_ids = fields.One2many('account.move','service_ids')

    @api.depends()
    def _compute_invoice_count(self):
        """To compute invoice count for a particular service"""
        for record in self:
            record.invoice_count = self.env['account.move'].search_count([('service_ids','=',record.id)])

    @api.model_create_multi
    def create(self, vals_list):
        """Create sequence number for service"""
        for vals in vals_list:
            if vals.get('sequence_no_service', _('New')) == _('New'):
                vals['sequence_no_service'] = (self.env['ir.sequence'].next_by_code('machine.service'))
        return super().create(vals_list)

    def service_invoice_smart_button(self):
        """list of invoices of the service Machine"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'invoice',
            'view_mode': 'list,form',
            'res_model': 'account.move',
            'domain': [('service_ids', '=', self.id)],
            'context': "{'create': False}"
        }

    def action_start_case(self):
        """To Start Case"""
        self.write({'state': 'started'})

    def action_close_case(self):
            """To close the case,send email on closing the case"""
            self.write({'state': 'done'})
            template = self.env.ref('machine_management.email_template_service')
            email_values = {'email_from': 'odoouser38@gmail.com'}
            template.send_mail(self.id, force_send=True, email_values=email_values)

    def action_cancel_case(self):
        """To cancel the case"""
        self.write({'state': 'cancel'})

    def action_create_invoice_line(self):
        """To create invoice for Machine Service"""
        self.write({'state': 'invoiced'})
        """To find if there are any invoices in draft state """
        invoiced_in_draft = self.env['account.move'].search([('status_in_payment','=','draft'),('partner_id','=',self.partner_id)])
        line = [Command.create({'product_id': self.env.ref('machine_management.machine_service_charge_product').product_variant_ids.id, 'quantity': 1, 'price_unit': 100})]
        product = self.parts_line_ids.mapped('product_id.id')
        quantity = self.parts_line_ids.mapped('quantity')
        price = self.parts_line_ids.mapped('product_id.list_price')
        if invoiced_in_draft:
            invoice_line_products = invoiced_in_draft[0].invoice_line_ids.mapped('product_id.id')
        else:
            invoice_line_products = []
        for i in range(len(product)):
            if product[i] in invoice_line_products:
                invoiced_in_draft[0].invoice_line_ids[i+1].quantity += quantity[i]
            else:
                lines = (
                [Command.create({
                'product_id': product[i],
                'quantity': quantity[i],
                'price_unit': price[i],
            }) for rec in self])
                line.extend(lines)
        if invoiced_in_draft:
            invoiced_in_draft[0].update({
                'invoice_line_ids': line,
                'service_ids' : [Command.link(self.id)],
            })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': invoiced_in_draft[0].id,
                'target': 'self',
            }
        else:
                invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': self.partner_id.id,
                'invoice_date': fields.Datetime.today(),
                'service_ids' : [Command.link(self.id)],
                'invoice_line_ids': line
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'target': 'self',
        }

    def action_archive(self):
        """Only manager can archive a service"""
        if not self.env.user.has_group('machine_management.group_machine_management_manager'):
                raise UserError("You don't have the access to Archive a Service, Contact Your Administrator")
        return super().action_archive()

    class AccountMove(models.Model):
        _inherit = 'account.move'

        service_ids = fields.Many2many('machine.service',string='Machine Service')

