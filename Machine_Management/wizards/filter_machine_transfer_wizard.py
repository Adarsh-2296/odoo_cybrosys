from odoo import fields, models
from odoo.exceptions import UserError
from odoo.tools import SQL

class FilterMachineTransferWizard(models.TransientModel):
   _name = 'filter.machine.transfer.wizard'
   _description = 'Filter Machine Transfer Wizard'

   machine_ids = fields.Many2many('machine.management', String='Machine')
   transfer_date = fields.Date(string="Transfer Date", tracking=True)
   transfer_type = fields.Selection(selection=[('install', 'Install'), ('remove', 'Remove')])
   transfer_to_date = fields.Date(string="Transfer Till", tracking=True)
   partner_ids = fields.Many2many('res.partner', string="Customer")

   def action_filter_machine_transfer(self):
       """Creates a Report based on the Filter Applied in the Wizard"""

       machine = self.mapped('machine_ids.id')
       transfer_type = tuple(self.mapped('transfer_type'))
       partner = tuple(self.mapped('partner_ids.id'))
       transfer_date = tuple(self.mapped('transfer_date'))
       transfer_to_date = tuple(self.mapped('transfer_to_date'))
       transfers = self.env['machine.transfer'].search([])

       # if not self.transfer_type:
       #     transfer_type = ('install', 'remove')
       # else:
       #     transfer_type = tuple((self.transfer_type + ' a').split())
       #
       # if not self.machine_ids:
       #     machine = transfers.mapped('machine_id.id')
       #
       # if not self.transfer_date:
       #    transfer_date = tuple(transfers.mapped('transfer_date'))
       #
       # if not self.transfer_to_date:
       #    transfer_to_date = tuple(transfers.mapped('transfer_to_date'))
       #
       # if not self.partner_ids:
       #     partner = transfers.mapped('partner_id.id')
       print(machine,'a')
       sql_query = SQL("""SELECT mt.id FROM machine_transfer mt
                          WHERE mt.transfer_type in %(transfer_type)s
                          AND mt.machine_id in %(machine_id)s
                          AND mt.partner_id in %(partner_id)s
                          AND mt.transfer_date in %(transfer_date)s
                          AND mt.transfer_to_date in %(transfer_to_date)s
        """,transfer_type = transfer_type, machine_id= tuple(machine), partner_id= tuple(partner), transfer_date = transfer_date, transfer_to_date = transfer_to_date )
       # sql_query = SQL("""SELECT mt.id FROM machine_transfer as mt
       # (CASE WHEN mt.transfer_date IS NULL THEN mt.transfer_date ELSE mt.transfer_date END)
       #
       #         """, transfer_type=transfer_type, machine_id=machine, partner_id=tuple(partner),
       #                 transfer_date=transfer_date, transfer_to_date=transfer_to_date)

       self.env.cr.execute(sql_query)
       result = self.env.cr.fetchall()
       if not result:
           raise UserError('No Record Matches the Filter')
       print(result)
       return self.env.ref('machine_management.machine_transfer_report').report_action(result)

