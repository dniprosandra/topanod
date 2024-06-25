# -*- coding: utf-8 -*-

{
    'name': 'Unique Code',
    'version': '17.0.0.0.0',
    'summary': 'Generate unique code',
    'sequence': 10,
    'description': """
Generate unique code for partner and for product
""",
    'category': 'Sales/CRM',
    'website': 'https://smarttek.solutions/',
    'depends': [
        # 'crm',
        'hr',
        'contacts',
        'sale_management',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/security.xml',

        #  Views
        # 'views/sale_order_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}