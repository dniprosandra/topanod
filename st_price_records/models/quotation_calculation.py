from odoo import models


class QuotationCalculation(models.Model):
    _inherit = 'quotation.calculation'

    def write(self, vals):
        result = super().write(vals)
        if result and 'active' in vals:
            for rec in self:
                rec._arch_line_price_history(vals["active"])
        return result

    def _arch_line_price_history(self, is_active):
        history = self._get_line_price_history(is_active)
        if history:
            return history.write({"active": is_active})

    def unlink(self):
        for rec in self:
            history = rec._get_line_price_history()
            history.unlink()
        return super().unlink()

    def _get_line_price_history(self, is_active=None):
        domain = [("calculation_id", "=", self.id)]
        if is_active is not None:
            active = False if is_active else True
            domain.append(("active", "=", active))
        history = self.env["calculation.price.history"].search(domain)
        return history
