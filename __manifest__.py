{
    'name': 'smart_form',
    'version': '1.0',
    'depends': ['base'],
    'author': 'Baamtu Sarl Senegal',
    'website': 'http://www.baamtu.com',
    'description': "beauty salon point of sale",
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/symptom_view.xml',
        'views/diagnostic_view.xml',
        'views/disease_view.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
