from odoo import http
from odoo.http import request

class CreateService(http.Controller):
    @http.route(['/website/machine/details'], type='http', auth="public", website=True)
    def website_machine_details_form(self, **kw):
        machine = self.env['machine.management'].search([])
        id = machine.mapped('id')
        name = machine.mapped('name')

        datas = {
            'id': id,
            'name': name,
        }
        print(datas)
        return request.render('machine_management.machine_management_details',datas)