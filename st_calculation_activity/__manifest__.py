# -*- coding: utf-8 -*-

{
    'name': 'Calculation Activity',
    'version': '17.0.0.0.1',
    'summary': 'Calculation Activity',
    'sequence': 10,
    'description': """
""",
    'category': 'Sales',
    'website': 'https://smarttek.solutions/',
    'depends': [
        'st_calculation',
    ],
    'data': [
        'data/activity_type_data.xml',
        'views/quotation_calculation_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'st_calculation_activity/static/src/js/inherit_systray_activity_menu.js',
        ]
    },
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
