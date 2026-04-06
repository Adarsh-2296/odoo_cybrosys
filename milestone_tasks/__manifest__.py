{
    'name': 'Milestone Tasks',
    'summary': """Create milestone and tasks""",
    'description': """Create milestone and tasks""",
    'version': "19.0.1.0",
    'category': 'Sales',
    'author': "Adarsh",
    'website': "www.cybrosys.com",
    'license': "LGPL-3",
    'sequence':-6,
    'installable': True,
    'application': True,
    'auto_install': True,
    'depends': ['sale_management','project'],
    'data': [
        'views/project_task.xml',
        'views/project_project.xml',
        'views/sale_order_line_views.xml'
    ]
}