{
    'name': 'Clear Cart',
    'version': "19.0.1.0",
    'summary': """Adds a button in the shop cart to clear all the items in the cart with a single click""",
    'description': """Adds a button in the shop cart to clear all the items in the cart with a single click""",
    'category': 'Website',
    'author': "Adarsh",
    'website': "www.cybrosys.com",
    'license': "LGPL-3",
    'sequence':-2,
    'installable': True,
    'application': True,
    'auto_install': True,
    'depends': ['website'],
    'data': [
        'static/src/xml/clear_cart_views.xml'
    ],
'assets': {
        'web.assets_frontend': [
            'clear_cart/static/src/interactions/**/*',
       ],
    },
}