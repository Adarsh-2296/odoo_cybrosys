# -*- coding: utf-8 -*-
import io
import json
from odoo import fields, models, _
from odoo.tools import SQL
from odoo.tools import json_default
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class MachineTransferWizard(models.TransientModel):
    _name = 'machine.transfer.wizard'
    _description = 'Machine Transfer Wizard'

    machine_ids = fields.Many2many('machine.management', String='Machine')
    transfer_date = fields.Date(string="Transfer Date", tracking=True)
    transfer_type = fields.Selection(selection=[('install', 'Install'), ('remove', 'Remove')])
    transfer_to_date = fields.Date(string="Transfer Till", tracking=True)
    partner_ids = fields.Many2many('res.partner', string="Customer")

    def action_print_transfer_xlsx(self):
        data = {
            'machine_ids': self.mapped('machine_ids.id'),
            'transfer_date': self.transfer_date,
            'transfer_type': self.transfer_type,
            'transfer_to_date': self.transfer_to_date,
            'partner_ids': self.mapped('partner_ids.id'),
        }

        return {
            'type': 'ir.actions.report',
            'data': {'model': 'machine.transfer.wizard',
                     'options': json.dumps(data, default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Transfer Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        """Print XLSX Report"""
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
        print(docs[0][1])
        transfers = self.env['machine.transfer'].browse(doc_id)
        machine = transfers.mapped('machine_id')
        partner = transfers.mapped('partner_id')
        if len(set(machine)) == 1:
            heading = machine[0].name + heading
            flag =1
        elif len(set(partner)) == 1:
            heading = partner[0].name + heading
            flag =2

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('docs')
        head = workbook.add_format({'bold': True, 'font_size': 30, 'align': 'center'})
        bold = workbook.add_format({'bold': True, 'align': 'center'})
        sheet.merge_range('C2:G4', heading,head )
        sheet.set_column(3, 3, 15)
        sheet.set_column(6, 6, 15)
        sheet.set_column(5, 5, 15)
        sheet.set_column(4, 4, 15)
        sheet.set_column(7, 7, 15)
        if flag != 1:
            sheet.merge_range('C6:D6', 'Machine', bold)
        if flag != 2:
            sheet.merge_range('C6:D6', 'Customer',bold)
        sheet.write('E6', 'Transfer Type',bold)
        sheet.write('F6', 'Transfer Date',bold)
        sheet.write('G6', 'Transfer Till',bold)
        i = 7
        for rec in docs:
            if flag != 1:
                sheet.write('C'+str(i), self.env['machine.management'].browse(rec[1]).name)
            if flag != 2:
                sheet.write('D'+str(i), self.env['res.partner'].browse(rec[2]).name)
            sheet.write('E'+str(i), rec[3])
            sheet.write('F'+str(i), rec[4].strftime('%Y-%m-%d'))
            sheet.write('G'+str(i), rec[5].strftime('%Y-%m-%d'))
            i = i + 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
