# -*- coding: utf-8 -*-
from odoo import fields, models,api
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
        """button action on the wizard returns the values in the wizard"""
        data = {
            'machine_id': self.mapped('machine_ids.id'),
            'transfer_date': self.transfer_date,
            'transfer_type': self.transfer_type,
            'transfer_to_date': self.transfer_to_date,
            'partner_id': self.mapped('partner_ids.id'),
        }
        return self.env.ref('machine_management.machine_transfer_report_table').report_action(None, data=data)


class MachineTransferWizard(models.AbstractModel):
    _name = 'report.machine_management.transfer_table'

    @api.model
    def _get_report_values(self, docids, data=None):
        """Creates a Report based on the Filter Applied in the Wizard"""
        print('a')
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
        print(result[0])
        machine = []
        partner = []
        machine_transfers = []
        for i in result:
            transfers = self.env['machine.transfer'].browse(i)
            machine_transfers.append(transfers)
            machine.append(transfers.machine_id)
            partner.append(transfers.partner_id)
        print('m', machine, 'p', partner,'t', machine_transfers)
        if len(set(machine)) == 1:
            print(machine)
            machine_transfers.append(0)
        elif len(set(partner)) == 1:
            machine_transfers.append(1)
        else:
            machine_transfers.append(2)

        return {
              'doc_ids': docids,
              'doc_model': 'machine.transfer',
              'docs': machine_transfers,
              'data': data,
        }
    # def action_filter_machine_transfer(self):
    #    """Creates a Report based on the Filter Applied in the Wizard"""
    #    machine = list(self.mapped('machine_ids.id')) or None
    #    transfer_type = self.transfer_type or None
    #    partner = list(self.mapped('partner_ids.id')) or None
    #    transfer_date = self.transfer_date or None
    #    transfer_to_date = self.transfer_to_date or None
    #
    #    sql_query = SQL("""SELECT mt.id
    #                      FROM machine_transfer mt
    #                      WHERE (%(transfer_type)s IS NULL OR mt.transfer_type = %(transfer_type)s)
    #                      AND (%(machine_id)s IS NULL OR mt.machine_id = ANY(%(machine_id)s))
    #                      AND (%(partner_id)s IS NULL OR mt.partner_id = ANY(%(partner_id)s))
    #                      AND (%(transfer_date)s IS NULL OR mt.transfer_date = %(transfer_date)s)
    #                      AND (%(transfer_to_date)s IS NULL OR mt.transfer_to_date = %(transfer_to_date)s)""",
    #                    transfer_type=transfer_type, machine_id=machine, partner_id=partner, transfer_date=transfer_date,
    #                    transfer_to_date=transfer_to_date)
    #
    #    self.env.cr.execute(sql_query)
    #    result = self.env.cr.fetchall()
    #    if not result:
    #        raise UserError('No Record Matches the Filter')
    #    machine = []
    #    partner = []
    #    for i in result:
    #        transfers = self.env['machine.transfer'].browse(i)
    #        machine.append(transfers.machine_id)
    #        partner.append(transfers.partner_id)
    #
    #    if len(set(machine)) == 1:
    #        print(machine)
    #        result.append(0)
    #    elif len(set(partner)) == 1:
    #        result.append(1)
    #    else:
    #        result.append(2)
    #    return self.env.ref('machine_management.machine_transfer_report_table').report_action(result)






