{
    'name': "Custom Training",
    'summary': "Module for managing training dates and assigned employees in sales orders",
    'description': """
        Long description of module's purpose
    """,
    'author': "DAOUBI Younes",
    'category': 'Sales',
    'version': '0.1',
    'depends': ['sale', 'hr','calendar'],
    'data': [
        'views/sale_order_views.xml',
        'views/hr_employee_views.xml',
        'security/security.xml',

    ],
    'security': [
        'security/ir.model.access.csv',
       
    ],
    'demo': [
        # Fichiers de données de démonstration
    ],
}
