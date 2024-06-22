from odoo import fields, models, api


class QuotationCalculationLine(models.Model):
    _name = 'quotation.calculation.line'
    _description = 'Quotation Calculation Line'

    #  Relations fields
    quotation_calculation_id = fields.Many2one(comodel_name="quotation.calculation")
    partner_id = fields.Many2one(related='quotation_calculation_id.partner_id')
    product_id = fields.Many2one(
        comodel_name="product.template"
    )
    coating_type = fields.Many2one(comodel_name="coating.type", required=True)
    additional_service_ids = fields.Many2many(comodel_name="additional.service", required=True)
    color = fields.Many2one(comodel_name='service.color', required=True)
    currency_id = fields.Many2one(
        related='quotation_calculation_id.currency_id'
    )

    #  Char/Selection fields
    name = fields.Char(
        required=True,
        # related='product_id.name'
    )
    shape = fields.Char()
    product_code = fields.Char(
        # related="product_id.default_code",
        compute='_compute_product_data',
        string="Product Code"
    )

    # Integer/Float fields
    qty = fields.Integer(required=True, default=1)
    length = fields.Float(required=True)
    height = fields.Float(required=True)
    width = fields.Float(required=True)
    area = fields.Float(
        # compute="_compute_area", store=True
    )
    weight = fields.Float()

    # Monetary fields
    coating_cost = fields.Monetary(currency_field="currency_id")
    additional_service_cost = fields.Monetary(currency_field="currency_id")
    amount = fields.Monetary(
        # compute="_compute_amount",
        currency_field="currency_id"
    )
    total_amount = fields.Monetary(
        compute="_compute_total_amount",
        currency_field="currency_id"
    )

    @api.depends('product_id')
    def _compute_product_data(self):
        for rec in self:
            if rec.product_id:
                rec.product_code = rec.product_id.default_code
                rec.name = rec.product_id.name
            else:
                rec.product_code = ""
                rec.name = ""

    @api.depends('length', "width")
    def _compute_area(self):
        for rec in self:
            rec.area = rec.length * rec.width

    @api.depends('coating_cost', 'additional_service_cost')
    def _compute_amount(self):
        for rec in self:
            rec.amount = rec.additional_service_cost + rec.coating_cost

    @api.depends('amount', 'qty')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = rec.amount * rec.qty
