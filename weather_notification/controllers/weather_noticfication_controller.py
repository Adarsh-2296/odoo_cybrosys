from odoo import http
import requests

class CreateService(http.Controller):
    @http.route(['/weather/notification'], type='json', auth="user", methods=['POST'], csrf=False)
    def website_machine_service_form(self):
        city = self.env['ir.config_parameter'].sudo().get_param('weather_notification.current_location')
        forecast = requests.get('http://api.weatherapi.com/v1/forecast.json?key=4354396c5c004838a6c90453263005&q='+city).json()
        print(forecast)
        if 'location' in forecast.keys():
            if forecast['location']['name'].lower() != city.lower():
                forecast = {}
        return forecast