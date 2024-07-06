from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.constrains('partner_id')
    def _is_product_in_use(self):
        calc = self.env['quotation.calculation.line']
        calc_line_count = calc.sudo().search_count([
            ('product_id.product_tmpl_id', '=', self.id)
        ])
        if calc_line_count > 0:
            raise ValidationError(
                _("The product already exists in records. "
                  "You may delete these records and change the customer or create a new product instead")
            )
