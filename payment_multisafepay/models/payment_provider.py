# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[
        ('multisafepay',        'MultiSafePay Online'),
        ('multisafepay_direct', 'MultiSafePay Direct'),
    ], ondelete={
        'multisafepay':        'set default',
        'multisafepay_direct': 'set default',
    })
    multisafepay_api_key = fields.Char(string='MultiSafePay API Key',
                                       help="The Test or Live API Key depending on the configuration of the provider",
                                       required_if_provider='multisafepay',
                                       copy=False,
                                       groups='base.group_system',)
    # mollie_api_key = fields.Char(
    #     string="Mollie API Key",
    #     help="The Test or Live API Key depending on the configuration of the provider",
    #     required_if_provider='mollie',
    #     copy=False,
    #     groups='base.group_system',
    # )
    def _get_default_payment_method_codes(self):
        res = super()._get_default_payment_method_codes()
        if self.code == 'multisafepay':        return {'multisafepay'}
        if self.code == 'multisafepay_direct': return {'multisafepay_direct'}
        return res

#
# from odoo import _, fields, models, service
# from odoo.tools import urls
#
# from odoo.addons.payment.logging import get_payment_logger
#
#
# _logger = get_payment_logger(__name__)
#
#
# class PaymentProvider(models.Model):
#     _inherit = 'payment.provider'
#
#     code = fields.Selection(
#         selection_add=[('multisafepay', 'MultiSafePay')], ondelete={'multisafepay': 'set default'}
#     )
#     multisafepay_api_key = fields.Char(
#         string="MultiSafePay API Key",
#         help="The Test or Live API Key depending on the configuration of the provider",
#         required_if_provider='multisafepay',
#         copy=False,
#         groups='base.group_system',
#     )