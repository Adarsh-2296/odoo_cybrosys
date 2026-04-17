# -*- coding: utf-8 -*-
from odoo import fields,models,api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_id_domain_ids = fields.Many2many('product.product',string='Products',compute='_compute_product_id_domain_ids')
    is_vendor_products_settings = fields.Boolean(compute='_compute_is_vendor_products_settings')

    def _compute_is_vendor_products_settings(self):
        """To get the value of the field(is_vendor_products_settings) in the settings of purchase"""
        self.is_vendor_products_settings = self.env['ir.config_parameter'].sudo().get_param('purchase.is_vendor_products_settings')

    @api.depends('order_id.partner_id','order_id.is_vendor_products')
    def _compute_product_id_domain_ids(self):
        print(self)
        for rec in self:
            rec.product_id_domain_ids = self.env['product.product'].search([('purchase_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', self.company_id)])
            if rec.order_id.is_vendor_products and rec.is_vendor_products_settings:
                supplier_info_line = self.env['product.supplierinfo'].search([('partner_id','=',self.partner_id)])
                rec.product_id_domain_ids = supplier_info_line.mapped('product_tmpl_id.product_variant_ids')
