from odoo import http, Command
from odoo.http import request

class CreateService(http.Controller):
    @http.route(['/website/customer/form'], type='http', auth="public", website=True)
    def website_machine_service_form(self, **kw):
        country = self.env['res.country'].sudo().search([])
        datas = {
            'country': country,
        }
        return request.render('machine_management.create_customer_template',datas)
    @http.route(['/website/customer/create'], type='http', auth="public", methods=['POST'], website=True, csrf=True)
    def create_service(self, **post):
        request.env['res.partner'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'company_type': post.get('company_type'),
            'street': post.get('street'),
            'street2': post.get('street2'),
            'city': post.get('city'),
            'zip': post.get('zip'),
            'country_id': post.get('country'),
        })
        return request.redirect('/contactus-thank-you')
