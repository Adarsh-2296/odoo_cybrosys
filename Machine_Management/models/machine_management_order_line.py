# -*- coding: utf-8 -*-
from odoo import models,fields,api

class MachineManagementOrderLine(models.Model):
    _name = 'machine.management.order.line'
    _description = 'Machine Management parts Order Line'

    order_id = fields.Many2one(
        'machine.management',
        string="Order Reference",
        required=True,copy=False,bypass_access=True)
    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Product")
    quantity = fields.Integer(required=True)
    product_uom_id = fields.Many2one('uom.uom', string='Unit', required=True, default=1)