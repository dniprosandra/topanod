from datetime import date

from odoo import fields, models


class QuotationCalculationLine(models.Model):
    _inherit = 'quotation.calculation.line'

    comment = fields.Text(string='Comment')

    def write(self, vals):
        result = super().write(vals)
        if result and vals.get('comment', False):
            self._add_history_record(vals.get('comment'))
        return result

    def _add_history_record(self, comment: str):
        """ Add new record or update existing record. """
        history = self.env['calculation.history']
        record = history.search([('line_id', '=', self.id)])
        record_data = {
            'author_id': self.env.user.id,
            'comment': comment,
            'comment_date': date.today(),
        }
        if record:
            record.write(record_data)
        else:
            record_data.update({'line_id': self.id,})
            record = history.create(record_data)
        return record
