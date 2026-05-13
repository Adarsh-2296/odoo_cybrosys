from odoo import http
from odoo.http import request
class WebsiteProduct(http.Controller):
   @http.route('/get/is_payment_restricted', auth="user", type='jsonrpc',)
   def get_is_payment_restricted(self):
       """Get the field is_payment_restricted from the pos settings."""
       is_payment_restricted = self.env['ir.config_parameter'].sudo().get_param('pos_rating.is_restrict_payment')
       print(is_payment_restricted)
       return is_payment_restricted