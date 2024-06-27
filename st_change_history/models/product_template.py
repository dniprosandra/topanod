from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    history_ids = fields.One2many(
        comodel_name='calculation.history', inverse_name="product_tmpl_id",
        string="Change History"
    )
