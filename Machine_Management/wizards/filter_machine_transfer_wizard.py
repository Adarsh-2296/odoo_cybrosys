from odoo import fields, models
from odoo.exceptions import UserError
from odoo.tools import SQL


class MachineTransferWizard(models.AbstractModel):
    _name = 'machine.transfer.wizard'
    _description = 'Machine Transfer Wizard'

    machine_ids = fields.Many2many('machine.management', String='Machine')
    transfer_date = fields.Date(string="Transfer Date", tracking=True)
    transfer_type = fields.Selection(selection=[('install', 'Install'), ('remove', 'Remove')])
    transfer_to_date = fields.Date(string="Transfer Till", tracking=True)
    partner_ids = fields.Many2many('res.partner', string="Customer")


class FilterMachineTransferWizard(models.TransientModel):
    _name = 'filter.machine.transfer.wizard'
    _inherit = 'machine.transfer.wizard'

    def action_filter_machine_transfer(self):
       """Creates a Report based on the Filter Applied in the Wizard"""
       machine = list(self.mapped('machine_ids.id')) or None
       transfer_type = self.transfer_type or None
       partner = list(self.mapped('partner_ids.id')) or None
       transfer_date = self.transfer_date or None
       transfer_to_date = self.transfer_to_date or None

       sql_query = SQL("""SELECT mt.id
                         FROM machine_transfer mt
                         WHERE (%(transfer_type)s IS NULL OR mt.transfer_type = %(transfer_type)s)
                         AND (%(machine_id)s IS NULL OR mt.machine_id = ANY(%(machine_id)s))
                         AND (%(partner_id)s IS NULL OR mt.partner_id = ANY(%(partner_id)s))
                         AND (%(transfer_date)s IS NULL OR mt.transfer_date = %(transfer_date)s)
                         AND (%(transfer_to_date)s IS NULL OR mt.transfer_to_date = %(transfer_to_date)s)""",
                       transfer_type=transfer_type, machine_id=machine, partner_id=partner, transfer_date=transfer_date,
                       transfer_to_date=transfer_to_date)

       self.env.cr.execute(sql_query)
       result = self.env.cr.fetchall()
       if not result:
           raise UserError('No Record Matches the Filter')
       machine = []
       partner = []
       for i in result:
           transfers = self.env['machine.transfer'].browse(i)
           machine.append(transfers.machine_id)
           partner.append(transfers.partner_id)

       if len(set(machine)) == 1:
           print(machine)
           result.append(0)
       elif len(set(partner)) == 1:
           result.append(1)
       else:
           result.append(2)
       return self.env.ref('machine_management.machine_transfer_report_table').report_action(result)






