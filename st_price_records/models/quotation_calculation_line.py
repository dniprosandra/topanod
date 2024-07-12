from datetime import date

from odoo import models, api


class QuotationCalculationLine(models.Model):
    _inherit = 'quotation.calculation.line'

    @api.model_create_multi
    def create(self, vals_list):
        result = super(QuotationCalculationLine, self).create(vals_list)
        for rec in result if result else []:
            if rec.product_id and rec.amount > 0:
                rec._add_price_history_record()
        return result

    def write(self, vals):
        result = super().write(vals)
        if result and 'amount' in vals:
            for rec in self:
                if rec.product_id:
                    rec._add_price_history_record()
        return result

    def unlink(self):
        for rec in self:
            history = rec._get_line_price_history()
            if history:
                history.unlink()
        return super().unlink()

    def _get_line_price_history(self):
        domain = [("line_id", "=", self.id)]
        history = self.env["calculation.price.history"].search(domain)
        return history

    def _add_price_history_record(self):
        """ Add new record. """
        history = self.env['calculation.price.history']
        record_data = {
            'line_id': self.id,
            'product_tmpl_id': self.product_id.product_tmpl_id.id,
            'calculation_id': self.quotation_calculation_id.id,
            'user_id': self.quotation_calculation_id.assigned_id.id,
            'price_change_date': date.today(),
            'price': self.amount,
            'qty': self.qty,
            'loaded_qty': self.loaded_qty,
            'state': self.quotation_calculation_id.state,
        }
        history_record = history.create(record_data)
        return history_record
