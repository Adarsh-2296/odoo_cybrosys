from odoo import http, Command
from odoo.http import request

class CreateService(http.Controller):
    @http.route(['/website/service/form'], type='http', auth="public", website=True)
    def website_machine_service_form(self, **kw):
        machines = self.env['machine.management'].sudo().search([])
        partner = self.env['res.partner'].sudo().search([])
        user = self.env['res.users'].sudo().search([('share','=',False),('active','=',True)])
        datas = {
            'machine' : machines,
            'partner' : partner,
            'user' : user,
        }
        return request.render('machine_management.create_service_template',datas)

    @http.route(['/website/service/form/<int:machine_id>'], type='http', auth="public", website=True)
    def create_service_from_machine_form(self,machine_id, **kw):
        print(machine_id)
        machine = self.env['machine.management'].sudo().browse(machine_id)
        machines = self.env['machine.management'].sudo().search([])
        partner = self.env['res.partner'].sudo().search([])
        user = self.env['res.users'].sudo().search([('share', '=', False), ('active', '=', True)])
        datas = {
            'machine_id' : machine,
            'machine': machines,
            'partner': partner,
            'user': user,
        }
        return request.render('machine_management.create_service_template', datas)

    @http.route(['/website/service/create'], type='http', auth="public", methods=['POST'], website=True, csrf=True)
    def create_service(self, **post):
        request.env['machine.service'].sudo().create({
            'machine_id': post.get('machine'),
            'partner_id': post.get('partner'),
            'tech_person_ids': [(Command.link(post.get('user')))],
            'date': post.get('date'),
            'description': post.get('description'),
        })
        return request.redirect('/contactus-thank-you')
