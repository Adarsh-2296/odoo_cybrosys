from odoo import models
import requests
class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'
    def _get_specific_rendering_values(self, processing_values):
        """Provides the values needed to render the QWeb redirect form."""
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'multisafepay':
            return res
        print(processing_values)
        url = "https://testapi.multisafepay.com/v1/json/orders?api_key=97fa6f38e6ceda008884712c849b42b0a34d0409"
        currency = self.env['res.currency'].browse([processing_values['currency_id']]).name
        payload = {
            "type": "redirect",
            "order_id": processing_values['reference'],
            "currency": currency,
            "amount": processing_values['amount'] * 100,
            "description": "Test Order Description",
            "payment_options": {
                "notification_method": "POST",
                "notification_url": "https://www.example.com/webhooks/payment",
                "redirect_url": "http://localhost:8019/payment/done",
                "cancel_url": "http://localhost:8019/shop/payment",
                "close_window": False
            },
            'custom_info': {'custom_1': self.id, 'custom_2': None, 'custom_3': None},
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
        }
