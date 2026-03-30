# -*- coding: utf-8 -*-
from odoo import fields,models,api,_

class MachineTransfer(models.Model):
    _name = 'machine.transfer'
    _description = 'Machine Transfer'
    _rec_name = 'sequence_no_transfer'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence_no_transfer = fields.Char(readonly=True, tracking=True,copy=False)
    machine_id = fields.Many2one('machine.management',string="Machine",tracking=True,ondelete='restrict')
    alternate_ids = fields.Many2many('machine.management',compute='_compute_alternate_ids')
    serial_no = fields.Char(string="Serial No.",readonly=True, store=True,related="machine_id.serial_no",tracking=True)
    transfer_date = fields.Date(required=True, string="Transfer Date",tracking=True,default=fields.Date.today())
    transfer_type = fields.Selection(selection=[('install','Install'),('remove','Remove')],default='install',tracking=True)
    partner_id = fields.Many2one('res.partner',string="Customer",tracking=True)
    internal_notes = fields.Text(string="Internal Notes",tracking=True)
    status = fields.Selection([('draft','Draft'),('done','Done')],default='draft',tracking=True)
    active = fields.Boolean(string='Active',tracking=True,default=True)

    @api.model_create_multi
    def create(self, vals_list):
        print('vals_list')
        """Create sequence number for transfer"""
        for vals in vals_list:
            if vals.get('sequence_no_transfer', _('New')) == _('New'):
                vals['sequence_no_transfer'] = (self.env['ir.sequence'].next_by_code('machine.transfer'))

        return super().create(vals_list)

    @api.depends('transfer_type')
    def _compute_alternate_ids(self):
        """To set the domain of machine_id field according to the transfer type"""
        for record in self:
            if record.transfer_type == 'install':
                record.alternate_ids = record.machine_id.search([('state','=','active')])
            elif record.transfer_type == 'remove':
                record.alternate_ids = record.machine_id.search([('state','=','in_service')])
            else:
                record.alternate_ids = record.machine_id.search([])

    def transfer_machine_button(self):
        """Button to confirm the transfer"""
        self.machine_id.write({'partner_id': self.partner_id,'state': 'in_service'})
        self.write({'status': 'done'})
