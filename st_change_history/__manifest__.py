# -*- coding: utf-8 -*-

{
    'name': 'Change History',
    'version': '17.0.0.0.0',
    'summary': 'Calculation Change History',
    'sequence': 10,
    'description': """

""",
    'category': 'Sales/CRM',
    'website': 'https://smarttek.solutions/',
    'depends': [
        'st_calculation',
    ],
    'data': [
        'security/ir.model.access.csv',
        # 'security/security.xml',

        #  Data
        # 'data/mail_template.xml',

        #  Views
        'views/product_template_views.xml',
        'views/quotation_calculation_line.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
