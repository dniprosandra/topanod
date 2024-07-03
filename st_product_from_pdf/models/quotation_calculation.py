from odoo import models


class QuotationCalculationLine(models.Model):
    _inherit = 'quotation.calculation'

    def button_open_file_import_wizard(self):
        return self._open_file_import_wizard()

    def _open_file_import_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'st.import.product.wizard',
            'target': 'new',
            'context': {'default_calculation_id': self.id},
        }
