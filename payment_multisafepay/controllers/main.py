from odoo import http
from odoo.http import request
class MultiSafePayController(http.Controller):
    # -- MultiSafePay Direct (JSON-RPC, inline flow) ------------------
    @http.route('/payment/multisafepay/direct/simulate_payment',
                type='jsonrpc', auth='public')
    def multisafepay_direct_simulate_payment(self, **data):
        payment_data = {
            'reference': data.get('reference'),
            'status':    data.get('simulated_state', 'done'),
        }
        request.env['payment.transaction'].sudo() \
               ._process('multisafepay_direct', payment_data)
    # -- MultiSafePay Online (HTTP POST, redirect flow) ----------------
    @http.route('/payment/multisafepay/simulate_payment',
                type='http', auth='public',
                methods=['POST'], csrf=False)
    def multisafepay_simulate_payment(self, **data):
        payment_data = {
            'reference': data.get('reference'),
            'status':    data.get('status', 'done'),
        }
        request.env['payment.transaction'].sudo() \
               ._process('multisafepay', payment_data)
        return request.redirect('/payment/status')
