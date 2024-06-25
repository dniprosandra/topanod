# -*- coding: utf-8 -*-

{
    'name': 'Calculation',
    'version': '17.0.0.0.0',
    'summary': 'Calculation',
    'sequence': 10,
    'description': """

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
        'security/ir.model.access.csv',
        'security/security.xml',

        #  Data
        'data/calculation_sequence.xml',
        'data/color_data.xml',
        'data/coating_type_data.xml',
        'data/additional_service_data.xml',

        #  Views
        'views/sale_order_views.xml',
        'views/quotation_calculation.xml',
        'views/additional_service_views.xml',
        'views/coating_type_views.xml',
        'views/service_color_views.xml',
        'views/res_partner_views.xml',
        'views/product_template_views.xml',

        'views/st_calculation_menus.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
}
