from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    partner_id = fields.Many2one(comodel_name='res.partner', string="Customer")
    unique_code = fields.Char(string="Unique Code", compute="_compute_unique_code", store=True, readonly=True)

    @api.depends('partner_id')
    def _compute_unique_code(self):
        for product in self:
            product.unique_code = self._get_unique_code() if product.partner_id else ""

    def _get_unique_code(self):
        partner_ext_id = self.partner_id.partner_ext_id
        if partner_ext_id:
            next_code = self._get_next_code()
            code = f"{partner_ext_id}-{next_code}"
        else:
            code = ""
        return code

    def _get_next_code(self):
        next_code = self.env['ir.sequence'].next_by_code('product.unique.code')
        return next_code.lstrip("0")



