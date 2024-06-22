from odoo import fields, models, api


class CoatingType(models.Model):
    _name = 'coating.type'
    _description = 'Coating Type'

    name = fields.Char(required=True)
    # sequence = fields.Integer(required=True)
