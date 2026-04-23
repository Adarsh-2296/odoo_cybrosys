# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
class WebsiteProduct(http.Controller):
   @http.route('/get_machine', auth="public", type='jsonrpc',
               website=True)
   def get_product_category(self):
       """Get the machines for the snippet."""
       machine = request.env['machine.management'].sudo().search_read(fields=['name', 'image', 'id','purchase_value'])
       values = {
           'machine': machine,
       }
       print(values)
       return values
