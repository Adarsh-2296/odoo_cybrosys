# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Payment Provider: MultiSafePay',
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': -5,
    'summary': "A payment provider covering several countries.",
    'description': "A payment provider covering several countries",
    'author': 'Adarsh',
    'website': 'https://docs.multisafepay.com',
    'depends': ['payment'],
    'data': [
        'views/payment_provider_views.xml',
        'views/payment_multisafepay_templates.xml',

        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'license': 'LGPL-3'
}
