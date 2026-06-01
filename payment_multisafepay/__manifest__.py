# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Payment Provider: MultiSafePay',
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': -5,
    'summary': "A Dutch payment provider covering several European countries.",
    'description': " ",  # Non-empty string to avoid loading the README file.
    'author': 'Adarsh',
    'website': 'https://docs.multisafepay.com',
    'depends': ['payment'],
    'data': [
        'views/payment_multisafepay_templates.xml',
        'views/payment_provider_views.xml',

        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
    ],
'assets': {
        'web.assets_frontend': [
            'payment_multisafepay/static/src/js/payment_form.js',
        ],
    },
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'license': 'LGPL-3'
}
