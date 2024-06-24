from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    partner_id = fields.Many2one(comodel_name='res.partner', string="Customer")

    def create(self, vals):
        vals['default_code'] = self.env['ir.sequence'].next_by_code('calculation.product.code')
        return super(ProductTemplate, self).create(vals)
