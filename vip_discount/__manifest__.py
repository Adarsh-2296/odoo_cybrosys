{
    'name': 'VIP Discount',
    'version': "19.0.1.0",
    'summary': """To set discount for vip partners""",
    'description': """To set discount for vip partners in sale order""",
    'category': 'Sales',
    'author': "Adarsh",
    'website': "www.cybrosys.com",
    'license': "LGPL-3",
    'sequence':-3,
    'installable': True,
    'application': True,
    'auto_install': True,
    'depends': ['sale_management'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml'
    ]
}