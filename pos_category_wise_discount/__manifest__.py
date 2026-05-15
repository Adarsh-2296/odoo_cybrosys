{
    'name': 'POS Category Wise Discount',
    'version': "19.0.1.0",
    'summary': """To set maximum amount discount for each category in point of sale""",
    'description': """To set maximum amount discount for each category in point of sale""",
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
        'views/res_config_settings.xml',
        'views/pos_category.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_category_wise_discount/static/src/**/*',
        ]
    }
}