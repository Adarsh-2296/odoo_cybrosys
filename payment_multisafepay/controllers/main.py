import requests
from odoo import http
from odoo.http import request

class PaymentMultiSafePayPostProcessing(http.Controller):

    @http.route(['/payment/done/<int:transaction_id>'], type='http', auth='public', website=True,  methods=['GET'])
    def multisafepay__simulate_payment(self, transaction_id,**data):
        print(data)
        reference = data.get('transactionid')
        transaction = self.env['payment.transaction'].sudo().browse(transaction_id)
        url = "https://testapi.multisafepay.com/v1/json/orders/"+reference+"?api_key="+transaction.provider_id.multisafepay_api_key
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers).json()
        print(response)
        if response['success'] == True:
            print(response['data'])
            if response['data']['payment_methods'][0]['status'] == 'completed':
                transaction.write({'state': 'done'})
                return request.redirect('/payment/status')
            elif response['data']['payment_methods'][0]['status'] == 'uncleared':
                transaction.write({'state': 'pending'})
                return request.redirect('/payment/status')
            elif response['data']['payment_methods'][0]['status'] in ['cancelled','expired']:
                transaction.write({'state': 'cancel'})
                return request.redirect('/payment/status')
            else:
                transaction.write({'state': 'error'})
                return request.redirect('/payment/status')
    @http.route(['/payment/cancel/<int:transaction_id>'], type='http', auth='public', website=True,  methods=['GET'])
    def multisafepay__cancel_payment(self, transaction_id,**data):
        print(data)
        transaction = self.env['payment.transaction'].sudo().browse(transaction_id)
        transaction.write({'state': 'cancel'})
        return request.redirect('/payment/status')
