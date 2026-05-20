{
    'name': 'Remove Order Line POS',
    'version': "19.0.1.0",
    'summary': """buttons to delete order line in pos separately and all at once""",
    'description': """buttons to delete order line in pos separately and all at once""",
    'category': 'Point of Sale',
    'author': "Adarsh",
    'website': "www.cybrosys.com",
    'license': "LGPL-3",
    'sequence':-6,
    'installable': True,
    'application': True,
    'auto_install': True,
    'depends': ['point_of_sale','base'],
    'data': [
        'views/res_config_settings.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'remove_order_line_pos/static/src/**/*'
        ]
    }
}