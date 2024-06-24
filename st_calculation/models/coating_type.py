from odoo import fields, models


class CoatingType(models.Model):
    _name = 'coating.type'
    _description = 'Coating Type'

    name = fields.Char(required=True, translate=True)
    # cost = fields.Float()
