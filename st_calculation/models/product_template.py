from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    partner_id = fields.Many2one(comodel_name='res.partner', string="Customer")
