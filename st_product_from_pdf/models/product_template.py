from odoo import models, fields, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    attached_file = fields.Many2one(comodel_name='product.document', string='Attached file')
