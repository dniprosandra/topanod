from datetime import date

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class QuotationCalculation(models.Model):
    _name = 'quotation.calculation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Quotation Calculation'

    #  Relations fields
    sale_order_id = fields.Many2one(
        string="Quotation",
        comodel_name='sale.order',
        domain=[('state', '=', 'draft')]
    )
    partner_id = fields.Many2one(
        string='Customer',
        related='sale_order_id.partner_id',
        store=True
    )
    assigned_id = fields.Many2one(
        comodel_name='res.users', default=lambda self: self.env.user,
        tracking=True, string="Assigned Manager"
    )
    assigned_department_id = fields.Many2one(comodel_name="hr.department", tracking=True)
    calculation_line_ids = fields.One2many(
        comodel_name='quotation.calculation.line', inverse_name="quotation_calculation_id"
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        compute='_compute_currency_id',
        store=True,
        precompute=True,
        ondelete='restrict'
    )

    #  Char/Selection/Text fields
    name = fields.Char()
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('new', 'New'),
            ('in_production', 'In Production'),
            ('calculated', 'Calculated'),
            ('sent', 'Calculation sent'),
            ('confirmed', 'Confirmed'),
        ],
        default='draft',
        tracking=True
    )
    partner_ext_id = fields.Char(related="partner_id.external_id")
    rq_number = fields.Char(string="RQ")
    note = fields.Text()

    # Integer/Float/Monetary fields
    total_product_amount = fields.Monetary(compute="_compute_total_amount", currency_field="currency_id")
    total_amount = fields.Monetary(compute="_compute_total_amount", currency_field="currency_id")
    delivery_cost = fields.Monetary(currency_field="currency_id")

    #  Date fields
    calculation_create_date = fields.Date(required=True)
    calculation_date = fields.Date(string='Calculation Date')
    in_production_date = fields.Date(string='In Production Date')

    # Boolean fields
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('rq_number_unique', 'unique(rq_number)', "RQ Number must be unique!"),
        ('partner_ext_id_unique', 'unique(partner_ext_id)', "Customer external id must be unique!")
    ]

    @api.model
    def create(self, vals_list):
        vals_list['rq_number'] = f"{self.env['ir.sequence'].next_by_code('st.calculation')}"
        vals_list['name'] = f"C{vals_list['rq_number']}"
        vals_list['state'] = 'new'
        vals_list['calculation_create_date'] = date.today()
        return super(QuotationCalculation, self).create(vals_list)

    @api.depends('sale_order_id.currency_id')
    def _compute_currency_id(self):
        for rec in self:
            if rec.sale_order_id:
                rec.currency_id = rec.sale_order_id.currency_id.id
            else:
                rec.currency_id = False

    @api.depends('calculation_line_ids.total_amount', 'delivery_cost')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_product_amount = sum([line.total_amount for line in rec.calculation_line_ids])
            rec.total_amount = rec.total_product_amount + rec.delivery_cost

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        if self.env.context.get('mark_qc_as_sent'):
            self.filtered(lambda qc: qc.state == 'calculated').with_context().write({'state': 'sent'})
        qc_ctx = {'mail_post_autofollow': self.env.context.get('mail_post_autofollow', True)}
        if self.env.context.get('mark_qc_as_sent') and 'mail_notify_author' not in kwargs:
            kwargs['notify_author'] = self.env.user.partner_id.id in (kwargs.get('partner_ids') or [])
        return super(QuotationCalculation, self.with_context(**qc_ctx)).message_post(**kwargs)

    def button_calculation_sent(self):
        """ Opens a wizard to compose an email, with relevant mail template loaded by default """
        self.ensure_one()
        ctx = {
            'default_model': 'quotation.calculation',
            'default_subject': _("%s, Calculation(s) - %s") % (self.env.company.name, self.name),
            'default_partner_ids': [self.partner_id.id],
            'default_res_ids': self.ids,
            'default_template_id': False,
            'default_composition_mode': 'comment',
            'mark_qc_as_sent': True,
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'force_email': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def button_reset_to_new(self):
        self.write({
            'state': 'new',
            'calculation_date': False,
            'in_production_date': False
        })

    def button_to_production(self):
        self.ensure_one()
        if not self.assigned_department_id:
            raise ValidationError(
                _("You can not move status to 'in_production' with out assigned department.")
            )
        self.write({
            'state': 'in_production',
            'in_production_date': date.today()
        })

    def button_calculate(self):
        # Some validation before write
        self.write({
            'state': 'calculated',
            'calculation_date': date.today()
        })

    def button_confirm_calculation(self):
        self.ensure_one()
        res = self.sale_order_id.write({'order_line': [
            (0, 0, {
                'product_id': line.product_id.id,
                'product_uom_qty': line.qty,
                'price_unit': line.amount,
                'calculation_id': self.id,
            })
            for line in self.calculation_line_ids]})
        if res:
            self.write({'state': 'confirmed'})
