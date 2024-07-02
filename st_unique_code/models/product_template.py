from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    partner_id = fields.Many2one(comodel_name='res.partner', string="Customer")
    unique_code = fields.Char(string="Unique Code", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'partner_id' in vals and vals['partner_id']:
                vals['unique_code'] = self._get_unique_code(vals['partner_id'])
        return super(ProductTemplate, self).create(vals_list)

    def write(self, vals):
        if 'partner_id' in vals:
            for rec in self:
                partner_id = vals.get('partner_id')
                if partner_id:
                    if partner_id != rec.partner_id:
                        vals['unique_code'] = rec._get_unique_code(partner_id)
                else:
                    vals['unique_code'] = ""
        return super(ProductTemplate, self).write(vals)

    def _get_unique_code(self, partner_id: int) -> str:
        """ Create unique code for product based on partner_ext_id """
        partner_ext_id = self.env['res.partner'].browse(partner_id).partner_ext_id
        if partner_ext_id:
            next_code = self._get_next_code()
            code = f"{partner_ext_id}-{next_code}"
        else:
            code = ""
        return code

    def _get_next_code(self) -> str:
        next_code = self.env['ir.sequence'].next_by_code('product.unique.code')
        return next_code.lstrip("0")
