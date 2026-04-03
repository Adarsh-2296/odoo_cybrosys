{
    'name': 'Employee Transfer',
    'version': "19.0.1.0",
    'summary': """To enable transfer request for users between companies""",
    'description': """To enable transfer request for users between companies""",
    'category': 'Human Resources',
    'author': "Adarsh",
    'website': "www.cybrosys.com",
    'license': "LGPL-3",
    'sequence':-3,
    'installable': True,
    'application': True,
    'auto_install': True,
    'depends': ['hr','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/employee_transfer_sequence.xml',
        'views/hr_employee_views.xml',
        'views/employee_transfer_views.xml',
        'views/employee_transfer_menu.xml'
    ],
}