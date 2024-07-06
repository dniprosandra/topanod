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
            # company_type = vals.get('company_type', "")
            vals['partner_ext_id'] = self._get_partner_code()
            # if company_type == 'person':
            vals['product_seq_id'] = self._get_partner_seq(vals)
        return super(ResPartner, self).create(vals_list)

    def _get_partner_code(self) -> str:
        code = self.env['ir.sequence'].next_by_code('partner.unique.code')
        return code.lstrip("0")

    def _get_partner_seq(self, vals: dict) -> int:
        seq_model = self.env['ir.sequence']
        ext_id = vals['partner_ext_id']
        seq_vals = {
            'name': f"Product Sequence {ext_id} - {vals['name']}",
            'code': self._get_seq_code(vals),
            'padding': 5,
            'number_increment': 1
        }
        seq = seq_model.create(seq_vals)
        return seq.id

    @staticmethod
    def _get_seq_code(vals: dict) -> str:
        ext_id = vals['partner_ext_id']
        name = vals['name'].replace(' ', '_').lower()
        code = f"{ext_id}_{name}"
        return code

