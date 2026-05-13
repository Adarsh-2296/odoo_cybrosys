{
    'name': 'POS Rating',
    'version': "19.0.1.0",
    'summary': """Adds a rating field in the product form and displays in the pos""",
    'description': """Adds a rating field in the product form and displays in the pos""",
    'category': 'Point of Sale',
    'author': "Adarsh",
    'website': "www.cybrosys.com",
    'license': "LGPL-3",
    'sequence':-5,
    'installable': True,
    'application': True,
    'auto_install': True,
    'depends': ['point_of_sale','base'],
    'data': [
        'views/product_product_views.xml',
        'views/res_config_settings.xml',
    ],
'assets': {
        'point_of_sale._assets_pos': [
            'pos_rating/static/src/**/*',
        ],
},
}