{
    'name': 'Restrict Vendors',
    'version': "19.0.1.0",
    'summary': """Set a limit to count of Purchase order line for vendors""",
    'description': """Set a limit to count of Purchase order line for vendors""",
    'category': 'Purchase',
    'author': "Adarsh",
    'website': "www.cybrosys.com",
    'license': "LGPL-3",
    'sequence':-2,
    'installable': True,
    'application': True,
    'auto_install': True,
    'depends': ['purchase'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/res_partner_views.xml',
        'views/purchase_order_views.xml'
    ]
}