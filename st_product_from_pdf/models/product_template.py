from odoo import models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', _('Unique product template name')),
    ]
