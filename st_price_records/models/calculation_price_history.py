from odoo import fields, models


class CalculationHistory(models.Model):
    _name = 'calculation.price.history'
    _description = 'Line History'
    _rec_name = 'line_id'
    _order = "create_date DESC"

    line_id = fields.Many2one(
        string="Calculation Line", comodel_name="quotation.calculation.line",
    )
    product_tmpl_id = fields.Many2one(comodel_name="product.template")
    calculation_id = fields.Many2one(related="line_id.quotation_calculation_id")
    currency_id = fields.Many2one(related="calculation_id.currency_id")
    user_id = fields.Many2one(comodel_name="res.users", string="Manager")
    price_change_date = fields.Date()
    price = fields.Monetary()
    qty = fields.Integer()
    loaded_qty = fields.Integer()
    state = fields.Char(string="Status")
    active = fields.Boolean(string="Active", default=True)
