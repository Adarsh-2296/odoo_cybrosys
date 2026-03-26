{
    'name': 'Restrict Users',
    'version': "19.0.1.0",
    'summary': """Set a limit to sale order, for certain users""",
    'description': """Sale order cannot be confirmed by users other than administrator, if it is above the specified amount in the settings""",
    'category': 'Sale',
    'author': "Adarsh",
    'website': "www.cybrosys.com",
    'license': "LGPL-3",
    'sequence':-2,
    'installable': True,
    'application': True,
    'auto_install': True,
    'depends': ['sale_management'],
    'data': [
        'views/res_config_settings_views.xml'
    ]
}