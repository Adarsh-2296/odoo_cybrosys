from odoo import http
from odoo.http import request

class CreateService(http.Controller):
    @http.route(['/website/machine'], type='http', auth="public", website=True)
    def website_machine_form(self, **kw):
        machine = self.env['machine.management'].sudo().search([])
        url = '/website/machine/'
        datas = {
            'url': url,
            'machine' : machine,
        }
        return request.render('machine_management.portal_machine_details',datas)

    @http.route(['/website/machine/<int:machine_id>'], type='http', auth="public", website=True)
    def website_machine_details_form(self,machine_id,**kw):
        machine = self.env['machine.management'].sudo().browse(machine_id)
        image = '/web/image/%s/%s/image' % (machine._name, machine.id)
        datas = {
            'image': image,
            'machine': machine,
        }

        return request.render('machine_management.website_machine_details',datas)
