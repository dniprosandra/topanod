from odoo import fields, models


class QuotationCalculationLine(models.Model):
    _inherit = 'quotation.calculation.line'

    file_url = fields.Char(string='URL')

    # TODO: write method for deleting url if file was deleted

    def open_doc(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self.file_url
        }
