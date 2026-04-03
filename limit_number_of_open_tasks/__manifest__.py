{
    'name': 'Limit Number Of Open Tasks',
    'version': "19.0.1.0",
    'summary': """To set limti to the number of tasks assigned to a user""",
    'description': """To set limti to the number of tasks assigned to a user""",
    'category': 'Services',
    'author': "Adarsh",
    'website': "www.cybrosys.com",
    'license': "LGPL-3",
    'sequence':-3,
    'installable': True,
    'application': True,
    'auto_install': True,
    'depends': ['project'],
    'data':[
        'views/res_config_settings_views.xml',
        'views/res_users_views.xml'
    ]
}