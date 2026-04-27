{
    'name': 'Add To Cart Quantity',
    'version': "19.0.1.0",
    'summary': """Adds a Quantity field near the cart button in the shop view""",
    'description': """Adds a Quantity field near the cart button in the shop view""",
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
        'views/shop_template_views.xml',
    ]
}