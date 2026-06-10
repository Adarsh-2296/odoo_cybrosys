{
    'name': 'Delivery Order In Invoice',
    'version': "19.0.1.0",
    'summary': """Adds a button in the Invoice to show the delivery order""",
    'description':  """Adds a button in the Invoice to show the delivery order""",
    'category': 'Website',
    'author': "Adarsh",
    'website': "www.cybrosys.com",
    'license': "LGPL-3",
    'sequence':-10,
    'installable': True,
    'application': True,
    'depends': ['account','stock','sale'],
    'data': [
        'views/account_move.xml',
    ],
}