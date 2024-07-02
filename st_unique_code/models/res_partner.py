from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_ext_id = fields.Char(string='External ID', readonly=True)

    _sql_constraints = [
        ('partner_ext_id_unique', 'unique(partner_ext_id)', "External ID must be unique!"),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['partner_ext_id'] = self._get_partner_code()
        return super(ResPartner, self).create(vals_list)

    def _get_partner_code(self):
        code = self.env['ir.sequence'].next_by_code('partner.unique.code')
        return code.lstrip("0")
