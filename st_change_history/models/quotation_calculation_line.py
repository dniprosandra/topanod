from datetime import date

from odoo import fields, models, api, _


class QuotationCalculationLine(models.Model):
    _inherit = 'quotation.calculation.line'

    comment = fields.Text(string='Comment')

    @api.model_create_multi
    def create(self, vals_list):
        result = super(QuotationCalculationLine, self).create(vals_list)
        for vals in vals_list:
            if 'comment' in vals:
                result._add_history_record(vals['comment'])
        return result

    def write(self, vals):
        result = super().write(vals)
        if result and 'comment' in vals:
            self._add_history_record(vals['comment'])
        return result

    def _add_history_record(self, comment: str):
        """ Add new record or update existing record. """
        history = self.env['calculation.history']
        history_record = history.search([('line_id', '=', self.id)])
        record_data = {
            'author_id': self.env.user.id,
            'comment_date': date.today(),
        }
        if history_record:
            comment = comment if comment else _('[Deleted]')
            record_data.update({'comment': comment})
            history_record.write(record_data)
        elif comment and not history_record:
            record_data.update({'line_id': self.id, 'comment': comment})
            history_record = history.create(record_data)
        if history_record:
            return history_record
