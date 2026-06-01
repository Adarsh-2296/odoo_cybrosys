from odoo import models
import requests
class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'
    def _get_specific_rendering_values(self, processing_values):
        """Provides the values needed to render the QWeb redirect form."""
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'multisafepay':
            return res
        print(processing_values['amount'])
        print(res)
        url = "https://testapi.multisafepay.com/v1/json/orders?api_key=97fa6f38e6ceda008884712c849b42b0a34d0409"
        currency = self.env['res.currency'].browse([processing_values['currency_id']]).name
        customer = self.env['res.partner'].browse([processing_values['partner_id']]).name
        payload = {
            "type": "redirect",
            "order_id": "my-order-id-1",
            "currency": "EUR",
            "amount": 4523,
            "description": "Test Order Description",
            "payment_options": {
                "notification_method": "POST",
                "notification_url": "https://www.example.com/webhooks/payment",
                "redirect_url": "http://localhost:8019/payment/status",
                "cancel_url": "http://localhost:8019/shop/payment",
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
        print(response)
        print(response['data'])
        print(response['data']['payment_url'])
        print(response['success'])
        return {
            'api_url':   response['data']['payment_url'],
            'reference': self.reference,
            'next': self._get_orders()
        }

    def _get_orders(self):
        url = "https://testapi.multisafepay.com/v1/json/orders/my-order-id-1?api_key=97fa6f38e6ceda008884712c849b42b0a34d0409"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        print(response.text)
    def _extract_amount_data(self, payment_data):
        """Skip amount validation for simulated providers."""
        if self.provider_code in ('multisafepay', 'multisafepay_direct'):
            return None
        return super()._extract_amount_data(payment_data)
    def _apply_updates(self, payment_data):
        """Set the transaction state based on the simulated status."""
        super()._apply_updates(payment_data)
        if self.provider_code not in ('multisafepay', 'multisafepay_direct'):
            return
        status = payment_data.get('status')
        if status == 'done':   self._set_done()
        elif status == 'cancel': self._set_canceled()
