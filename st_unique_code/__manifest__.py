# -*- coding: utf-8 -*-

{
    'name': 'Unique Code',
    'version': '17.0.0.1.0',
    'summary': 'Generate unique code',
    'sequence': 10,
    'description': """
Generate unique code for partner and for product
""",
    'category': 'Sales',
    'website': 'https://smarttek.solutions/',
    'depends': [
        'product',
    ],
    'data': [
        #  Data
        'data/code_sequence.xml',

        #  Views
        'views/res_partner_views.xml',
        'views/product_template_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'st_unique_code/static/src/js/on_record_saved.js',
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
