# -*- coding: utf-8 -*-
from odoo import fields,models,api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        if self._approval_allowed():
            return super().action_confirm()
        else:
            limit = self.env['ir.config_parameter'].sudo().get_param(
                'sale.amount_limit')
            raise UserError("You cannot approve this order because the sale order limit is "+str(limit)+" But the current sale order has an amount of "+str(self.amount_total))

    def _approval_allowed(self):
        """Returns whether the order qualifies to be approved by the current user"""
        limit = self.env['ir.config_parameter'].sudo().get_param(
            'sale.amount_limit')
        is_restrict_user = self.env['ir.config_parameter'].sudo().get_param(
            'sale.restrict_user')
        print(limit,is_restrict_user,self.env.user.has_group('sales_team.group_sale_manager'))
        if is_restrict_user=='True':
            return (
                (self.amount_total < float(limit))
                or self.env.user.has_group('sales_team.group_sale_manager'))
        else:
            return True