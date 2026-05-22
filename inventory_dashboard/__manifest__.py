{
    'name': 'Inventory Dashboard',
    'version': "19.0.1.0",
    'summary': """Creates a dashboard in the Inventory module""",
    'description': """Creates a dashboard in the Inventory module""",
    'category': 'Supply Chain',
    'author': "Adarsh",
    'website': "www.cybrosys.com",
    'license': "LGPL-3",
    'sequence':-6,
    'installable': True,
    'application': True,
    'auto_install': True,
    'depends': ['stock','spreadsheet'],
    'data': [
        'views/inventory_dashboard_views.xml',
    ],
'assets': {
   'web.assets_backend': [
       'inventory_dashboard/static/src/js/dashboard.js',
       'inventory_dashboard/static/src/xml/dashboard.xml',
   ],
},

}