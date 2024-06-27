from odoo import fields, models, api


class CalculationHistory(models.Model):
    _name = 'calculation.history'
    _description = 'Line History'

    name = fields.Char()
    line_id = fields.Many2one(
        string="Calculation Line", comodel_name="quotation.calculation.line",
        # ondelete='cascade'
    )
    calculation_id = fields.Many2one(related="line_id.quotation_calculation_id")
    product_tmpl_id = fields.Many2one(related="line_id.product_template_id")
    author_id = fields.Many2one(comodel_name="res.users")
    qty = fields.Integer(related="line_id.qty")
    # loaded_qty = fields.Integer(related="line_id.loaded_qty")
    comment_date = fields.Date()
    comment = fields.Text()

