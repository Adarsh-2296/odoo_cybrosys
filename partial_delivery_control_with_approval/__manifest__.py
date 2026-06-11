{
    'name': 'Partial Delivery Control with Approval',
    'version': "19.0.1.0",
    'summary': """Partial Delivery Control with Approval""",
    'description':  """Partial Delivery Control with Approval""",
    'category': 'Inventory',
    'author': "Adarsh",
    'website': "www.cybrosys.com",
    'license': "LGPL-3",
    'sequence':-10,
    'installable': True,
    'application': True,
    'depends': ['stock'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/product_product_views.xml',
        'views/stock_picking_views.xml',
    ],
}