import logging
from datetime import date

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


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
    company_id = fields.Many2one(
        string='Company', related='sale_order_id.company_id',
        store=True, readonly=True
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
        comodel_name='quotation.calculation.line',
        inverse_name="quotation_calculation_id",
        copy=True
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
    partner_ext_id = fields.Char(related="partner_id.partner_ext_id")
    rq_number = fields.Char(string="RQ")
    note = fields.Text()

    # Integer/Float/Monetary fields
    total_product_amount = fields.Monetary(
        compute="_compute_total_amount", currency_field="currency_id"
    )
    total_amount = fields.Monetary(compute="_compute_total_amount", currency_field="currency_id")
    delivery_cost = fields.Monetary(currency_field="currency_id")

    #  Date fields
    calculation_create_date = fields.Date(required=True, copy=False)
    calculation_date = fields.Date(string='Calculation Date', copy=False)
    in_production_date = fields.Date(string='In Production Date', copy=False)

    # Boolean fields
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('rq_number_unique', 'unique(rq_number)', "RQ Number must be unique!"),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['rq_number'] = f"{self.env['ir.sequence'].next_by_code('st.calculation')}"
            vals['name'] = f"C{vals['rq_number']}"
            vals['state'] = 'new'
            vals['calculation_create_date'] = date.today()
        return super(QuotationCalculation, self).create(vals_list)

    def write(self, vals):
        result = super().write(vals)
        # Send notification when assigned manager or assigned department changed
        # assigned_id = vals.get('assigned_id', False)
        # department_id = vals.get('assigned_department_id', False)
        # if result and assigned_id or department_id:
        #     for line in self:
        #         notify_data = line._get_assignee_data(assigned_id, department_id)
        #         line._notify_assignee(notify_data)
        return result

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

    def button_calculation_sent(self) -> dict:
        """ Opens a wizard to compose an email,
        with relevant mail template loaded by default
        """
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
        """ Move Calculation state to 'New' """
        self.with_context(mail_auto_subscribe_no_notify=True).write({
            'state': 'new',
            'calculation_date': False,
            'in_production_date': False
        })

        # Notify assigned manager about state bin reset to 'New'
        # mail_vals = self._get_assignee_data(assigned_id=True)
        # self._notify_assignee(mail_vals, 'state')

    def button_to_production(self):
        """ Move Calculation state to 'In Production' """
        self.ensure_one()
        if not self.assigned_department_id:
            raise ValidationError(
                _("You can not move status to 'In Production' without assigned department.")
            )
        if not self._is_line_ids():
            raise ValidationError(
                _("You can not move status to 'In Production' without calculation lines.")
            )
        self.with_context(mail_auto_subscribe_no_notify=True).write({
            'state': 'in_production',
            'in_production_date': date.today()
        })

        # Notify assigned department about state change to 'In Production'
        # mail_vals = self._get_assignee_data(department_id=True)
        # self._notify_assignee(mail_vals, 'state')

    def button_calculate(self):
        """ Move Calculation status to 'Calculated' """
        if not self._is_line_ids():
            raise ValidationError(
                _("You can not move status to 'Calculated' without calculation lines.")
            )
        if not self.assigned_department_id:
            raise ValidationError(
                _("You can not move status to 'In Production' without assigned department.")
            )
        self.with_context(mail_auto_subscribe_no_notify=True).write({
            'state': 'calculated',
            'calculation_date': date.today()
        })

        # Notify assigned manager about state change to 'Calculated'
        # mail_vals = self._get_assignee_data(assigned_id=True)
        # self._notify_assignee(mail_vals, 'state')

    def button_confirm_calculation(self):
        """ Confirm Calculation and move state to 'Confirmed' """
        for rec in self:
            rec._no_product_in_line_create()
            rec._add_line_to_quotation()
            rec.with_context(mail_auto_subscribe_no_notify=True).write({'state': 'confirmed'})

    def _is_line_ids(self) -> bool:
        if self.calculation_line_ids:
            return True

    def _no_product_in_line_create(self):
        """
        Create a new product if the item product_id field is not
        filled in some calculation lines
        """
        for line in self.calculation_line_ids:
            if not line.product_id:
                product_tmpl_id = self.env['product.template'].create({
                    'name': line.name,
                    "partner_id": line.partner_id.id,
                })
                product_id = self.env['product.product'].search([
                    ('product_tmpl_id', '=', product_tmpl_id.id)
                ], limit=1)
                line.product_id = product_id.id
                _logger.info(_("Created product '%s' for calculation '%s'.") % (product_id.name, self.name))

    def _add_line_to_quotation(self):
        """ Add a lines to the quotation """
        quotation_line = [(0, 0, {
                'order_id': self.sale_order_id.id,
                'product_id': line.product_id.id,
                'product_uom_qty': line.qty,
                'price_unit': line.amount,
                'calculation_id': self.id,
            }) for line in self.calculation_line_ids]
        self.sale_order_id.write({'order_line': quotation_line})

    #  Email notification
    # def _notify_assignee(self, mail_vals: list, tmpl_type=None) -> int:
    #     """ Prepare assignee data for sending email notifications """
    #     counter = 0
    #
    #     #  Get values to put it into template
    #     tmpl_values = self._tmpl_values()
    #
    #     #  Prepare email data one-by-one. We have 2 emails max
    #     for val in mail_vals:
    #         tmpl_values.update({'assignee_name': val['name']})
    #         if tmpl_type is None:
    #             tmpl_type = 'assignee'
    #         tmpl_values.update({'partner_ids': val['partner_ids']})
    #
    #         #  Sending email
    #         self._send_email_notification(tmpl_values, tmpl_type)
    #         counter += 1
    #     return counter

    # def _send_email_notification(self, tmpl_values: dict, tmpl_type: str):
    #     """ Send email notification """
    #     record_name = tmpl_values['name']
    #     subject = _('You have been assigned to %s') % record_name
    #     if tmpl_type == 'state':
    #         state = self.state.capitalize().replace('_', ' ')
    #         subject = _("Calculation status has been change to %s") % state
    #         tmpl_values.update({'state': state})
    #     assignation_msg = self.env['ir.qweb']._render(
    #         template=self._get_template_id(tmpl_type), values=tmpl_values
    #     )
    #     assignation_msg = self.env['mail.render.mixin']._replace_local_links(assignation_msg)
    #     self.message_notify(
    #         subject=_(subject),
    #         body=assignation_msg,
    #         partner_ids=tmpl_values['partner_ids'],
    #         email_layout_xmlid='mail.mail_notification_layout',
    #         model_description=tmpl_values['model_description'],
    #         mail_auto_delete=False
    #     )

    # def _tmpl_values(self) -> dict:
    #     """ Return values to set in template"""
    #     tmpl_values = {
    #         'model_description': self.env['ir.model']._get(self._name).display_name,
    #         'access_link': self._notify_get_action_link('view'),
    #         'name': self.display_name,
    #     }
    #     return tmpl_values

    # def _get_assignee_data(self, assigned_id=False, department_id=False) -> list:
    #     """ Get the `email` and `name` for email notifications. """
    #     data = []
    #     if assigned_id:
    #         data.append({
    #             "partner_ids": self.assigned_id.partner_id.ids,
    #             'name': self.assigned_id.sudo().name
    #         })
    #     if department_id:
    #         data.append({
    #             "partner_ids": self.assigned_department_id.manager_id.user_partner_id.ids,
    #             'name': _("Department %s") % self.assigned_department_id.sudo().name
    #         })
    #     return data
    #
    # def _get_template_id(self, tmpl_type: str) -> str:
    #     if tmpl_type == 'state':
    #         tmpl = 'st_calculation.calculation_message_user_assigned_status_change'
    #     else:
    #         tmpl = 'st_calculation.calculation_message_user_assigned'
    #     return tmpl
