from odoo import fields, models, api


class AdditionalService(models.Model):
    _name = 'additional.service'
    _description = 'Additional Service'

    name = fields.Char()
    cost = fields.Float()
