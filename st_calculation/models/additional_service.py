from odoo import fields, models


class AdditionalService(models.Model):
    _name = 'additional.service'
    _description = 'Additional Service'

    name = fields.Char(required=True, translate=True)
    cost = fields.Float()
