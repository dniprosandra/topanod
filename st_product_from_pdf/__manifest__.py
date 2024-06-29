# -*- coding: utf-8 -*-

{
    'name': 'Product From PDF',
    'version': '17.0.0.0.0',
    'summary': 'Generate products from PDF ',
    'sequence': 10,
    'description': """
Generate unique code for partner and for product
""",
    'category': 'Sales',
    'website': 'https://smarttek.solutions/',
    'depends': [
        'st_calculation',
    ],
    'data': [
        #  Data
        'security/ir.model.access.csv',
        # 'data/code_sequence.xml',

        #  Views
        'views/quotation_calculation.xml',
        'wizard/import_product_wizard.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
