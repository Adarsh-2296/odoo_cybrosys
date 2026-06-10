# -*- coding: utf-8 -*-
from odoo import models,_,Command

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def create_invoices(self):
        res = super().create_invoices()
        invoice = self.env['account.move'].browse(res.get('res_id'))
        all_delivery = self.sale_order_ids.invoice_ids.mapped('delivery_ids.id')
        delivery = self.sale_order_ids.picking_ids.filtered(lambda rec: rec.id not in all_delivery)
        invoice.update({'delivery_ids' : delivery })
        return res