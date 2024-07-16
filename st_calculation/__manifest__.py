# -*- coding: utf-8 -*-

{
    'name': 'Calculation',
    'version': '17.0.0.1.0',
    'summary': 'Calculation',
    'sequence': 10,
    'description': """

""",
    'category': 'Sales/CRM',
    'website': 'https://smarttek.solutions/',
    'depends': [
        'crm',
        'hr',
        'contacts',
        'sale_management',
        'st_unique_code',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',

        #  Data
        'data/calculation_sequence.xml',
        'data/color_data.xml',
        'data/coating_type_data.xml',
        'data/additional_service_data.xml',
        'data/mail_template.xml',

        #  Views
        'views/sale_order_views.xml',
        'views/quotation_calculation.xml',
        'views/additional_service_views.xml',
        'views/coating_type_views.xml',
        'views/service_color_views.xml',
        'views/crm_lead.xml',

        'views/st_calculation_menus.xml'
    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'st_calculation/static/src/xml/list_render.xml',
    #         'st_calculation/static/src/js/list_renderer.js',
    #     ],
    # },
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
