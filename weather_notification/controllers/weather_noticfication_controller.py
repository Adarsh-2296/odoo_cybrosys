from odoo import http
import json
import requests

class CreateService(http.Controller):
    @http.route(['/weather/notification'], type='json', auth="user", methods=['POST'], csrf=False)
    def website_machine_service_form(self):
        response = requests.get(
            'http://api.weatherapi.com/v1/current.json?key=e688c6af209f4f6ba7383407262905&q=Kozhikode').json()
        print(response)
        return response
