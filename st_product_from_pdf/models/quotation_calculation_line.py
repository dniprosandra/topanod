from odoo import fields, models, api


class QuotationCalculationLine(models.Model):
    _inherit = 'quotation.calculation.line'

    file_url = fields.Char(string='URL', compute="_compute_file_url")

    @api.depends('product_id.product_tmpl_id.attached_file')
    def _compute_file_url(self):
        for rec in self:
            file = rec.product_id.attached_file
            if file:
                rec.file_url = file.local_url
            else:
                rec.file_url = ""

    def open_doc(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self.file_url
        }
