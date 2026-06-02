import requests
from odoo import http
from odoo.http import request

class PaymentMultiSafePayPostProcessing(http.Controller):

    @http.route(['/payment/done'], type='http', auth='public', website=True,  methods=['GET'])
    def multisafepay__simulate_payment(self, **data):
        print(self)
        print(data)
        reference = data.get('transactionid')
        url = "https://testapi.multisafepay.com/v1/json/orders/"+reference+"?api_key=97fa6f38e6ceda008884712c849b42b0a34d0409"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers).json()
        transaction = self.env['payment.transaction'].sudo().browse(int(response['data']['custom_info']['custom_1']))
        print(response)
        if response['success'] == True:
            print(response['data'])
            if response['data']['payment_methods'][0]['status'] == 'completed':
                transaction.write({'state': 'done'})
                return request.redirect('/payment/status')
            else:
                return request.redirect('/payment/status')