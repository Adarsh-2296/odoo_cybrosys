# -*- coding: utf-8 -*-
from odoo import fields, models,api,_
import io
import json
from odoo.tools import json_default
from odoo.exceptions import UserError
from odoo.tools import SQL
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class FilterMachineTransferWizard(models.TransientModel):
    _name = 'filter.machine.transfer.wizard'
    _description = 'Filter Machine Transfer Wizard'

    machine_ids = fields.Many2many('machine.management', String='Machine')
    transfer_date = fields.Date(string="Transfer Date", tracking=True)
    transfer_type = fields.Selection(selection=[('install', 'Install'), ('remove', 'Remove')])
    transfer_to_date = fields.Date(string="Transfer Till", tracking=True)
    partner_ids = fields.Many2many('res.partner', string="Customer")

    def action_filter_machine_transfer(self):
        """button action to print pdf report on the wizard returns the values in the wizard"""
        data = {
            'machine_id': self.mapped('machine_ids.id'),
            'transfer_date': self.transfer_date,
            'transfer_type': self.transfer_type,
            'transfer_to_date': self.transfer_to_date,
            'partner_id': self.mapped('partner_ids.id'),
        }
        return self.env.ref('machine_management.machine_transfer_report_table').report_action(None, data=data)

    def action_print_transfer_xlsx(self):
        """Button action to print xlsx file on wizard returns the values in the wizard"""
        data = {
            'machine_ids': self.mapped('machine_ids.id'),
            'transfer_date': self.transfer_date,
            'transfer_type': self.transfer_type,
            'transfer_to_date': self.transfer_to_date,
            'partner_ids': self.mapped('partner_ids.id'),
        }

        return {
            'type': 'ir.actions.report',
            'data': {'model': 'report.machine_management.transfer_table',
                     'options': json.dumps(data, default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Transfer Report',
                     },
            'report_type': 'xlsx',
        }


class MachineTransferWizard(models.AbstractModel):
    _name = 'report.machine_management.transfer_table'

    @api.model
    def _get_report_values(self, docids, data=None):
        """Creates a Report based on the Filter Applied in the Wizard"""
        sql_query = SQL("""SELECT mt.id
                             FROM machine_transfer mt
                             WHERE (%(transfer_type)s IS NULL OR mt.transfer_type = %(transfer_type)s)
                             AND (%(machine_id)s IS NULL OR mt.machine_id = ANY(%(machine_id)s))
                             AND (%(partner_id)s IS NULL OR mt.partner_id = ANY(%(partner_id)s))
                             AND (%(transfer_date)s IS NULL OR mt.transfer_date = %(transfer_date)s)
                             AND (%(transfer_to_date)s IS NULL OR mt.transfer_to_date = %(transfer_to_date)s)""",
                           transfer_type=data['transfer_type'] if data['transfer_type'] else None,
                           machine_id=data['machine_id'] if data['machine_id'] else None,
                           partner_id=data['partner_id'] if data['partner_id'] else None,
                           transfer_date=data['transfer_date'] if data['transfer_date'] else None,
                           transfer_to_date=data['transfer_to_date'] if data['transfer_to_date'] else None)
        self.env.cr.execute(sql_query)
        result = self.env.cr.fetchall()
        if not result:
            raise UserError('No Record Matches the Filter')
        machine = []
        partner = []
        transfer_type = []
        machine_transfers = []
        for i in result:
            transfers = self.env['machine.transfer'].browse(i)
            machine_transfers.append(transfers)
            machine.append(transfers.machine_id)
            partner.append(transfers.partner_id)
            transfer_type.append(transfers.transfer_type)
        print('m', machine, 'p', partner,'t', machine_transfers)
        if len(set(machine)) == 1:
            machine_transfers.append(0)
        elif len(set(partner)) == 1:
            machine_transfers.append(1)
        else:
            machine_transfers.append(2)
        if 'install' in transfer_type:
            machine_transfers.insert(0, 1)
        else:
            machine_transfers.insert(0, 0)
        if 'remove' in transfer_type:
            machine_transfers.insert(0, 0)
        else:
            machine_transfers.insert(0, 1)
        print(machine_transfers)

        return {
              'doc_ids': docids,
              'doc_model': 'machine.transfer',
              'docs': machine_transfers,
              'data': data,
        }
    def get_xlsx_report(self, data, response):
        """Get and Print XLSX Report"""
        sql_query = SQL("""SELECT mt.id, mt.machine_id, mt.partner_id, mt.transfer_type, mt.transfer_date, mt.transfer_to_date
                                     FROM machine_transfer mt
                                     WHERE (%(transfer_type)s IS NULL OR mt.transfer_type = %(transfer_type)s)
                                     AND (%(machine_id)s IS NULL OR mt.machine_id = ANY(%(machine_id)s))
                                     AND (%(partner_id)s IS NULL OR mt.partner_id = ANY(%(partner_id)s))
                                     AND (%(transfer_date)s IS NULL OR mt.transfer_date = %(transfer_date)s)
                                     AND (%(transfer_to_date)s IS NULL OR mt.transfer_to_date = %(transfer_to_date)s)""",
                        transfer_type=data['transfer_type'] if data['transfer_type'] else None,
                        machine_id=data['machine_ids'] if data['machine_ids'] else None,
                        partner_id=data['partner_ids'] if data['partner_ids'] else None,
                        transfer_date=data['transfer_date'] if data['transfer_date'] else None,
                        transfer_to_date=data['transfer_to_date'] if data['transfer_to_date'] else None)
        self.env.cr.execute(sql_query)
        docs = self.env.cr.fetchall()
        doc_id = []
        heading = ' Transfer Report'
        flag = 0
        for doc in docs:
            doc_id.append(doc[0])
        transfers = self.env['machine.transfer'].browse(doc_id)
        machine = transfers.mapped('machine_id')
        partner = transfers.mapped('partner_id')
        if len(set(machine)) == 1:
            heading = machine[0].name
            flag =1
        elif len(set(partner)) == 1:
            heading = partner[0].name
            flag =2
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        border = workbook.add_format({'border': 2, 'align': 'center','font_size': 10.5})
        sheet = workbook.add_worksheet('docs')
        head = workbook.add_format({'bold': True, 'font_size': 30, 'align': 'center'})
        bold = workbook.add_format({'bold': True, 'align': 'center','border': 2})
        sheet.merge_range('C2:G4', heading +  ' Install',head )
        sheet.set_column(2, 2, 20)
        sheet.set_column(3, 3, 15)
        sheet.set_column(6, 6, 20)
        sheet.set_column(5, 5, 15)
        sheet.set_column(4, 4, 15)
        sheet.set_column(8, 8, 20)
        sheet.set_column(9, 9, 15)
        sheet.set_column(10, 10, 15)
        sheet.set_column(11, 11, 15)
        if flag != 1:
            sheet.merge_range('C6:C7', 'Machine', bold)
        if flag != 2:
            sheet.merge_range('G6:G7', 'Customer',bold)
        sheet.merge_range('D6:D7', 'Transfer Type',bold)
        sheet.merge_range('E6:E7', 'Transfer Date',bold)
        sheet.merge_range('F6:F7', 'Transfer Till',bold)
        i = j = 8
        is_merge = 0
        for rec in docs:
            if rec[3] == 'remove':
                if is_merge == 0:
                    sheet.merge_range('I2:L4', heading + ' Remove', head)
                if flag != 1:
                    if is_merge == 0:
                        sheet.merge_range('I6:I7', 'Machine', bold)
                    sheet.write('I' + str(j), self.env['machine.management'].browse(rec[1]).name, border)
                if is_merge == 0:
                    sheet.merge_range('J6:J7', 'Transfer Type', bold)
                    sheet.merge_range('K6:K7', 'Transfer Date', bold)
                    sheet.merge_range('L6:L7', 'Transfer Till', bold)
                    is_merge += 1
                sheet.write('J' + str(j), rec[3].title(), border)
                sheet.write('K' + str(j), rec[4].strftime('%Y-%m-%d'), border)
                sheet.write('L' + str(j), rec[5].strftime('%Y-%m-%d'), border)
                j += 1
            else:
                if flag != 1:
                    sheet.write('C'+str(i), self.env['machine.management'].browse(rec[1]).name, border)
                if flag != 2:
                    sheet.write('G'+str(i), self.env['res.partner'].browse(rec[2]).name, border)
                sheet.write('D'+str(i), rec[3].title(), border)
                sheet.write('E'+str(i), rec[4].strftime('%Y-%m-%d'), border)
                sheet.write('F'+str(i), rec[5].strftime('%Y-%m-%d'), border)
                i += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()








