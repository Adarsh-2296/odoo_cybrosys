from odoo import http
from odoo.http import request

class CreateService(http.Controller):
    @http.route(['/website/service/form'], type='http', auth="public", website=True)
    def website_machine_service_form(self, **kw):
        machines = self.env['machine.management'].search([])
        print(machines)
        partner = self.env['res.partner'].search([])
        print(partner)
        user = self.env['res.users'].search([('share','=',False),('active','=',True)])
        datas = {
            'machine' : machines,
            'partner' : partner,
            'user' : user,
        }
        return request.render('machine_management.create_service_template',datas)
    @http.route(['/website/service/create'], type='http', auth="public", methods=['POST'], website=True, csrf=True)
    def create_service(self, **post):
        user = []
        user.append(post.get('user'))
        request.env['machine.service'].sudo().create({
            'machine_id': post.get('machine'),
            'partner_id': post.get('partner'),
            'tech_person_ids':a,
            'date': post.get('date'),
            'description': post.get('description'),
        })
        return request.render('machine_management.create_success_template')
