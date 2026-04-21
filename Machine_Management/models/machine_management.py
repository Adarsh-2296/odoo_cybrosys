# -*- coding: utf-8 -*-
from odoo import fields,models,api, _
from odoo.exceptions import ValidationError,UserError
from datetime import date


class MachineManagement(models.Model):
    _name = 'machine.management'
    _description = 'Machine Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _unique_serial_no = models.Constraint(
        'UNIQUE(serial_no)',
        'This Serial Number already exists!'
    )

    name = fields.Char(required=True , help="Machine Name", tracking=True)
    date_of_purchase = fields.Date(required=True, help="Purchase date of the machine", tracking=True,default=fields.Date.today())
    currency_id = fields.Many2one('res.currency',default=1)
    purchase_value = fields.Monetary(required=True, help="Purchase value of the machine", tracking=True)
    partner_id = fields.Many2one('res.partner', help="Customer of the machine", tracking=True,readonly=True,store=True)
    state = fields.Selection(selection=[('active', 'Active'),('in_service', 'In Service'),], default='active', help="State of the machine", tracking=True)
    image = fields.Binary( string="Image")
    description = fields.Text(required=True, help="Description of the machine", tracking=True)
    warranty = fields.Selection(selection=[('yes', 'Yes'),('no', 'No')], default='no', help="If the machine has warranty or not", tracking=True)
    machine_instruction = fields.Html(help="Instructions to use the machine")
    active = fields.Boolean(default=True, help="If the machine is active or not", tracking=True)

    serial_no = fields.Char(required=True, help="Serial No of the machine", tracking=True, copy=False)
    machine_type_id  = fields.Many2one('machine.type',string="Machine Type")
    company_id = fields.Many2one('res.company',default=lambda self: self.env.company)
    transfer_ids = fields.One2many('machine.transfer','machine_id',string="Transfers")
    transfer_count = fields.Integer(compute='_compute_transfer_count')
    service_ids = fields.One2many('machine.service', 'machine_id', string="Service")
    service_count = fields.Integer(compute='_compute_service_count')
    sequence_number = fields.Char( readonly=True, tracking=True,copy=False)
    machine_age = fields.Float(compute='_compute_machine_age')

    order_line_ids = fields.One2many(
        'machine.management.order.line',
        'order_id',
        string="Order Lines",
        copy=True)
    tag_ids = fields.Many2many('machine.tag',tracking=True)
    total_units = fields.Float(compute='_compute_total_units')
    product_filtered_ids = fields.Many2many('product.product',tracking=True)
    service_frequency = fields.Selection([('weeks', 'Weekly'), ('months', 'Monthly'), ('years', 'Yearly')],
                                         string='Service Frequency', tracking=True)
    last_service_date = fields.Date(string='Last Service Date', tracking=True, compute='_compute_last_service_date')

    @api.model
    def recurring_service_creation(self):
        """To create recurring services for machines"""
        machine=self.search([('state','=','in_service')])
        for rec in machine:
            if ('open' in   rec.mapped('service_ids.state')) or ('started' in rec.mapped('service_ids.state') ):
                pass
            else:
                self.env['machine.service'].create({
                    'machine_id': int(rec),
                    'partner_id': rec.partner_id.id,
                    'date': fields.Date.today(),
        })

    @api.depends('service_ids.date')
    def _compute_last_service_date(self):
        """To compute the last service date for a machine"""
        for record in self:
            if record.service_ids:
                last_service_date=sorted(record.mapped('service_ids.date'))
                record.last_service_date = last_service_date[-1]
            else:
                record.last_service_date = False

    @api.depends('date_of_purchase')
    def _compute_machine_age(self):
        """To compute the age of machine according to purchase date"""
        day = date.today().day
        month = date.today().month
        year = date.today().year
        purchase_day = self.date_of_purchase.day
        purchase_year = self.date_of_purchase.year
        purchase_month = self.date_of_purchase.month
        machine_age = year - purchase_year
        if month < purchase_month :
            machine_age-=1
        elif month == purchase_month and day < purchase_day :
            machine_age-=1
        self.machine_age=machine_age

    @api.depends('transfer_ids')
    def _compute_transfer_count(self):
        """To compute transfers count for a particular machine"""
        for record in self:
            record.transfer_count = len(record.transfer_ids)

    @api.depends('transfer_ids')
    def _compute_service_count(self):
        """To compute service count for a particular machine"""
        for record in self:
            record.service_count = len(record.service_ids)

    @api.depends('order_line_ids.quantity','product_filtered_ids')
    def _compute_total_units(self):
        """To compute the total units of products added in the product_filtered_ids field"""
        for record in self:
            if record.product_filtered_ids:
                products = record.order_line_ids.filtered(lambda i: i.product_id in record.product_filtered_ids)
                Qunatity = products.mapped('quantity')
                record.total_units = sum(Qunatity)
            else:
                quantity = record.order_line_ids.mapped('quantity')
                record.total_units = sum(quantity)

    @api.constrains('purchase_value')
    def _check_purchase_value(self):
        """Purchase value should be greater than Zero"""
        for record in self:
            if record.purchase_value <= 0:
                raise ValidationError('Purchase value should be greater than Zero')

    def redirect_to_transfer(self):
        """Create transfer from Machine form"""
        return {
            'type': 'ir.actions.act_window',
            'res_model':'machine.transfer',
            'view_mode': 'form',
            'target':'self',
            'context': {
                'default_machine_id': self.id,
                'default_serial_no': self.serial_no,
            },
        }

    def redirect_to_service(self):
        """Create service from Machine form"""
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'machine.service',
            'view_mode': 'form',
            'target': 'self',
            'context': {
                'default_machine_id': self.id,
            },
        }


    def machine_transfers_smart_button(self):
        """list of transfer of a Machine"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'transfers',
            'view_mode': 'list,form',
            'res_model': 'machine.transfer',
            'domain': [('machine_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def machine_service_smart_button(self):
        """list of service of a Machine"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'service',
            'view_mode': 'list,form',
            'res_model': 'machine.service',
            'domain': [('machine_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def action_archive(self):
        """Archive the services and transfers if machine is Archived and only manager can archive a machine"""
        open_services=self.service_ids.search([('state', '=', 'started')])
        if not self.env.user.has_group('machine_management.group_machine_management_manager'):
                raise UserError("You don't have the access to Archive a Machine, Contact Your Administrator")
        elif self.state == 'in_service':
            raise UserError(_('Can only archive machines in active state'))
        elif open_services:
            open_services.write({'state': 'cancel'})
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': ('The services in open state will be cancelled.'),
                    'type': 'warning',
                    'next':self.action_archive()
                }
            }
        self.service_ids.action_archive()
        self.transfer_ids.action_archive()
        return super().action_archive()

    def action_unarchive(self):
        """Unarchive the services and transfers if machine is unarchived"""
        inactive_ser = self.service_ids.search([('active', '=', False),('machine_id.id', '=', self.id)])
        inactive_transfer = self.transfer_ids.search([('active', '=', False),('machine_id.id', '=', self.id)])
        inactive_ser.action_unarchive()
        inactive_transfer.action_unarchive()
        return super().action_unarchive()

    @api.model_create_multi
    def create(self, vals_list):
        """Create sequence number"""
        for vals in vals_list:
            if vals.get('sequence_number', _('New')) == _('New'):
                vals['sequence_number'] = (self.env['ir.sequence'].next_by_code('machine.management'))
        return super().create(vals_list)


class MachineType(models.Model):
    """Machine Type model"""
    _name = 'machine.type'
    _description = 'Machine Type'

    name = fields.Char(required=True, string="Machine Type")

class MachineTags(models.Model):
    """Machine Tag model"""
    _name = 'machine.tag'
    _description = 'Machine Tag'

    name = fields.Char(required=True, string="Machine Tag")
    color = fields.Integer(string="Colour")




