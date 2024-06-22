from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    external_id = fields.Char(string='External ID')
