from markupsafe import Markup

from odoo import models, _


class QuotationCalculationLine(models.Model):
    _inherit = 'quotation.calculation.line'

    def write(self, vals):
        msg_vals = dict()
        for key, val in vals.items():
            if key in self._get_tracking_fields():
                msg_vals[key] = val
        if msg_vals:
            self._update_line_track(msg_vals)
        result = super().write(vals)
        return result

    def _update_line_track(self, values):
        """ Build message for lognote tracking """
        calculations = self.mapped('quotation_calculation_id')
        for calc in calculations:
            calc_lines = self.filtered(lambda x: x.quotation_calculation_id == calc)
            msg = Markup("<b>%s</b><ul>") % _("The calculated line has been updated.")
            for line in calc_lines:
                if 'product_id' in values and values['product_id'] != line.product_id.id:
                    # tracking is meaningless if the product is changed as well.
                    continue
                msg += Markup("<li><b> %s: </b><br/>") % line.display_name
                if 'qty' in values:
                    msg += _(
                        "Q-ty: %(old)s ➔ %(new)s",
                        old=self.format_number(line.qty),
                        new=self.format_number(values["qty"])
                    ) + Markup("<br/>")
                if 'additional_service_cost' in values:
                    msg += _(
                        "Additional service cost: %(old)s ➔ %(new)s",
                        old=self.format_number(line.additional_service_cost),
                        new=self.format_number(values["additional_service_cost"])
                    ) + Markup("<br/>")
                if 'coating_cost' in values:
                    msg += _(
                        "Coating cost: %(old)s ➔ %(new)s",
                        old=self.format_number(line.coating_cost),
                        new=self.format_number(values["coating_cost"])
                    ) + Markup("<br/>")
                if 'amount' in values:
                    msg += _(
                        "Amount: %(old)s ➔ %(new)s",
                        old=self.format_number(line.amount),
                        new=self.format_number(values["amount"])
                    ) + Markup("<br/>")
                if 'qty' or 'amount' in values:
                    msg += _(
                        "Total amount: %(old)s ➔ %(new)s",
                        old=self.format_number(line.total_amount),
                        new=line._get_new_total(values)
                    ) + Markup("<br/>")

            msg += Markup("</ul>")
            calc.message_post(body=msg)

    def _get_tracking_fields(self):
        track_list = [
            'qty', 'coating_cost', 'additional_service_cost',
            'amount', 'total_amount'
        ]
        return track_list

    def _get_new_total(self, values):
        """ Return the new total amount of calculation line"""
        qty = values.get('qty', 0) or self.qty
        # asc = values.get('additional_service_cost', 0) or self.additional_service_cost
        # coating_cost = values.get('coating_cost', 0) or self.coating_cost
        amount = values.get('amount', 0) or self.amount
        new_total = amount * qty
        return self.format_number(new_total)

    def format_number(self, number):
        """ Format number for display """
        return f'{number:,}'
