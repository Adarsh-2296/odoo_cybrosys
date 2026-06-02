# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[
        ('multisafepay',        'MultiSafePay Online'),
    ], ondelete={
        'multisafepay':        'set default',
    })
    multisafepay_api_key = fields.Char(string='MultiSafePay API Key',
                                       help="The Test or Live API Key depending on the configuration of the provider",
                                       required_if_provider='multisafepay',
                                       copy=False,
                                       groups='base.group_system',)