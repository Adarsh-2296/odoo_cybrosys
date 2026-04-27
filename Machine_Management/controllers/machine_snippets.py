# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
class WebsiteProduct(http.Controller):
   @http.route('/get_machine', auth="public", type='json',
               website=True)
   def get_machine_details(self):
       """Get the machines for the snippet."""
       machine = request.env['machine.management'].sudo().search_read(fields=['name', 'image', 'id','purchase_value'],limit=8)
       values = {
           'machine': machine,
       }
       return values

   @http.route(['/website/machine/home/<int:machine_id>'], type='http', auth="public", website=True)
   def machine_details_form(self, machine_id, **kw):
       machine = self.env['machine.management'].sudo().browse(machine_id)
       image = '/web/image/%s/%s/image' % (machine._name, machine.id)
       datas = {
           'image': image,
           'machine': machine,
       }
       return request.render('machine_management.website_machine_home_details', datas)
