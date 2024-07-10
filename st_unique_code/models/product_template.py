from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    partner_id = fields.Many2one(comodel_name='res.partner', string="Customer")
    unique_code = fields.Char(string="Unique Code", readonly=True, copy=False)
    upn = fields.Char(string="Unique Product Number", readonly=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['upn'] = self._get_upn_next_num()
            if 'partner_id' in vals and vals['partner_id']:
                vals['unique_code'] = self._get_unique_code(vals['partner_id'])
        return super(ProductTemplate, self).create(vals_list)

    def write(self, vals):
        if 'partner_id' in vals:
            for rec in self:
                partner_id = vals.get('partner_id')
                if partner_id:
                    if partner_id != rec.partner_id.id:
                        vals['unique_code'] = rec._get_unique_code(partner_id)
                else:
                    vals['unique_code'] = ""
        return super(ProductTemplate, self).write(vals)

    def _get_unique_code(self, partner_id: int) -> str:
        """ Create unique code for product based on partner_ext_id """
        partner = self.env['res.partner'].browse(partner_id)
        partner_ext_id = partner.partner_ext_id
        partner_product_seq_code = partner.product_seq_id.code
        if not partner_product_seq_code:
            partner.product_seq_id = partner._create_partner_seq()
            partner_product_seq_code = partner.product_seq_id.code
        next_product_code = partner.product_seq_id.next_by_code(partner_product_seq_code).lstrip("0")
        return f"{partner_ext_id}-{next_product_code}"

    def _get_upn_next_num(self) -> str:
        """ Create unique product number """
        next_code = self.env['ir.sequence'].next_by_code('product.upn.code')
        return next_code.lstrip("0")
