from odoo import models, fields, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', _('Unique product template name')),
    ]

    attached_file = fields.Many2one(comodel_name='product.document', string='Attached file')