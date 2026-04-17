{
    'name': 'Vendor Product List',
    'version': "19.0.1.0",
    'summary': """To restrict products in the product line according to the vendor""",
    'description': """To restrict products in the product line according to the vendor""",
    'category': 'Purchase',
    'author': "Adarsh",
    'website': "www.cybrosys.com",
    'license': "LGPL-3",
    'sequence':-3,
    'installable': True,
    'application': True,
    'auto_install': True,
    'depends': ['purchase','product'],
    'data': [
        'views/purchase_order_views.xml',
        'views/res_config_views.xml',
    ]
}