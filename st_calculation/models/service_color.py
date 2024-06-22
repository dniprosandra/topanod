from odoo import fields, models, api


class ServiceColor(models.Model):
    _name = 'service.color'
    _description = 'Service Color'

    name = fields.Char()
