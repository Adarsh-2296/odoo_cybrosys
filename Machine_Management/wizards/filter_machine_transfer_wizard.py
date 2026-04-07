from odoo import fields, models
from odoo.tools import SQL

class FilterMachineTransferWizard(models.TransientModel):
   _name = 'filter.machine.transfer.wizard'
   _description = 'Filter Machine Transfer Wizard'

   machine_id = fields.Many2many('machine.management', String='Machine')
   transfer_date = fields.Date(string="Transfer Date", tracking=True)
   transfer_type = fields.Selection(selection=[('install', 'Install'), ('remove', 'Remove')])
   transfer_to_date = fields.Date(string="Transfer Till")
   partner_id = fields.Many2many('res.partner', string="Customer")

   def action_filter_machine_transfer(self):
       """Creates a Report based on the Filter Applied"""
       sql_query = SQL("""Select * FROM machine_transfer WHERE transfer_type = 'install' """)
       self.env.cr.execute(sql_query)
       result = self.env.cr.fetchall()
       print(result)
       print(self.env.ref('machine_management.machine_transfer_report').report_action(docids=result[0]))
       return self.env.ref('machine_management.machine_transfer_report').report_action(docids=result)
       # rec = self.machine_id.transfer_ids.filtered(lambda x: x.partner_id == self.partner_id)
       # rec = rec.filtered(lambda x: x.transfer_type == self.transfer_type)
       # print(rec)

       # return {'type': 'ir.actions.act_window',
       #         'name': 'Filter Machine Transfer',
       #         'res_model': 'machine.transfer',
       #         'target': 'new',
       #         'view_mode': 'list',
       #         'domain' : [('machine_id.id', '=', self.machine_id.id),('partner_id.id', '=', self.partner_id.id),('transfer_type', '=', self.transfer_type)]
       #         }
