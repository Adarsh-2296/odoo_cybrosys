# -*- coding: utf-8 -*-
from odoo import fields,models,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_vip = fields.Boolean(string='Vip',related='partner_id.is_vip')
    vip_discount = fields.Float(string='Vip Discount',related='partner_id.vip_discount')
    is_vip_discount = fields.Boolean(string='Vip Discount', compute='_compute_is_vip_discount')

    def _compute_is_vip_discount(self):
        """To get the value of the field(is_vip_discount) in the settings of sales """
        self.is_vip_discount = self.env['ir.config_parameter'].sudo().get_param('sale.is_vip_discount')

    @api.onchange('order_line','partner_id')
    def onchange_vip_discount(self):
            if self.is_vip_discount:
                products = self.partner_id.mapped('product_ids')
                order_line = self.mapped('order_line')
                if self.is_vip:
                    if products:
                        products_in_product_id = order_line.filtered(lambda i: i.product_id in products)
                        products_in_product_id.write({ 'discount' : self.vip_discount })
                        products_in_product_id_is_vip_product = order_line.filtered(lambda i: i.product_id in products and i.product_id.vip_discount > self.vip_discount)
                        for rec in range(len(products_in_product_id_is_vip_product)):
                            products_in_product_id_is_vip_product[rec].write({ 'discount' : products_in_product_id_is_vip_product[rec].product_id.vip_discount})
                        products_not_in_product_id = order_line.filtered(lambda i: i.product_id not in products)
                        products_not_in_product_id.write({ 'discount' : 0 })
                    else:
                        self.order_line.write({ 'discount' : self.vip_discount })
                else:
                    self.order_line.write({ 'discount' : 0 })

