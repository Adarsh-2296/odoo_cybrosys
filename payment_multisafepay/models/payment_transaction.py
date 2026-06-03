from odoo import models
import requests
from odoo import http
class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """Provides the values needed to render the QWeb redirect form."""
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'multisafepay':
            return res
        web_url = http.request.env['ir.config_parameter'].get_param('web.base.url')
        url = "https://testapi.multisafepay.com/v1/json/orders?api_key="+self.provider_id.multisafepay_api_key
        currency = self.env['res.currency'].browse([processing_values['currency_id']]).name
        payload = {
            "type": "redirect",
            "order_id": processing_values['reference'],
            "currency": currency,
            "amount": processing_values['amount'] * 100,
            "description": "Test Order Description",
            "payment_options": {
                "notification_method": "POST",
                "notification_url": web_url+"/payment/update",
                "redirect_url": web_url+"/payment/done/"+str(self.id),
                "cancel_url": web_url+"/payment/cancel/"+str(self.id),
                "close_window": False
            },
            "customer": {
                "locale": "en_US",
                "disable_send_email": False
            },
            "checkout_options": {"validate_cart": False},
            "days_active": 30,
            "seconds_active": 2592000
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers).json()

        return {
            'api_url':   response['data']['payment_url'],
            'reference': self.reference,
            'provider' : self.provider_id
        }
