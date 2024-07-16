from odoo import fields, models, api


class QuotationCalculationLine(models.Model):
    _name = 'quotation.calculation.line'
    _description = 'Quotation Calculation Line'

    quotation_calculation_id = fields.Many2one(comodel_name="quotation.calculation")
    partner_id = fields.Many2one(related='quotation_calculation_id.partner_id')
    product_id = fields.Many2one(comodel_name="product.product")
    product_template_id = fields.Many2one(
        comodel_name='product.template',
        compute='_compute_product_tmpl'
    )
    coating_type = fields.Many2one(comodel_name="coating.type")
    additional_service_ids = fields.Many2many(
        comodel_name="additional.service"
    )
    color = fields.Many2one(comodel_name='service.color')
    currency_id = fields.Many2one(
        related='quotation_calculation_id.currency_id'
    )
    name = fields.Char(
        required=True, precompute=True,
        compute="_compute_name",
        store=True, readonly=False
    )
    shape = fields.Char()
    product_code = fields.Char(
        related='product_id.product_tmpl_id.unique_code',
        string="Product Code"
    )
    qty = fields.Integer(default=1)
    length = fields.Float()
    height = fields.Float()
    width = fields.Float()
    area = fields.Float(
        # compute="_compute_area", store=True
    )
    weight = fields.Float()
    loaded_qty = fields.Integer(compute="_compute_loaded_qty", readonly=False, store=True)
    calculated_qty = fields.Integer(compute="_compute_calculated_qty", readonly=True, store=True)
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
    def _compute_product_tmpl(self):
        for line in self:
            line.product_template_id = line.product_id.product_tmpl_id.id

    @api.depends('product_template_id')
    def _compute_name(self):
        for rec in self:
            if rec.product_template_id:
                rec.name = rec.product_template_id.name

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

    @api.depends('qty')
    def _compute_calculated_qty(self):
        for rec in self:
            if rec.qty > 0:
                #  Need formula for calculation

                #  Added for example
                rec.calculated_qty = rec.qty

    @api.depends('calculated_qty')
    def _compute_loaded_qty(self):
        for rec in self:
            #  By default, loaded_qty equal calculated_qty.
            #  User can change loaded_qty value
            rec.loaded_qty = rec.calculated_qty
