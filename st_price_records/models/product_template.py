from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    price_rec_ids = fields.One2many(
        comodel_name='calculation.price.history', inverse_name="product_tmpl_id",
        string="Price History"
    )
