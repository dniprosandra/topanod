from odoo import fields, models


class ServiceColor(models.Model):
    _name = 'service.color'
    _description = 'Service Color'

    name = fields.Char(required=True, translate=True)
    # cost = fields.Float()
