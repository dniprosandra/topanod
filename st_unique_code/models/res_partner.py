from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_ext_id = fields.Char(string='External ID', readonly=True, copy=False)
    product_seq_id = fields.Many2one(comodel_name='ir.sequence', readonly=True, copy=False)

    _sql_constraints = [
        ('partner_ext_id_unique', 'unique(partner_ext_id)', "External ID must be unique!"),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['partner_ext_id'] = self._get_partner_code()
        result = super(ResPartner, self).create(vals_list)
        for rec in result:
            rec.product_seq_id = rec._create_partner_seq()
        return result

    def _get_partner_code(self) -> str:
        code = self.env['ir.sequence'].next_by_code('partner.unique.code')
        return code.lstrip("0")

    def _create_partner_seq(self) -> int:
        seq_model = self.env['ir.sequence']
        seq_vals = {
            'name': f"Product Sequence ext_id_{self.partner_ext_id}",
            'code': self._get_seq_code(),
            'padding': 5,
            'number_increment': 1
        }
        seq = seq_model.sudo().create(seq_vals)
        return seq.id

    def _get_seq_code(self) -> str:
        ext_id = self.partner_ext_id
        code = f"tpn_ext_id{ext_id}_id{self.id}"
        return code
