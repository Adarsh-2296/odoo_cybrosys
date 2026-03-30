# -*- coding: utf-8 -*-
from odoo import fields,models,api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    machine_ids = fields.One2many('machine.management','partner_id')
    machine_count = fields.Integer(compute='_compute_machine_count')

    @api.depends()
    def _compute_machine_count(self):
        """To compute machine count of a partner"""
        for record in self:
            record.machine_count = len(record.machine_ids)

    def action_machine_smart_button(self):
        """list of machines of a customer"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'machines',
            'view_mode': 'list,form',
            'res_model': 'machine.management',
            'domain': [('partner_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def action_archive(self):
        """Archive the machines if customer is Archived"""
        self.machine_ids.action_archive()
        return super().action_archive()

    def action_unarchive(self):
        """Unarchive the machines if customer is unarchived"""
        inactive_macs = self.machine_ids.search([('active', '=', False),('partner_id.id', '=', self.id)])
        inactive_macs.action_unarchive()
        return super().action_unarchive()




