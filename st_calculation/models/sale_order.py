from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    quotation_calculation_ids = fields.One2many(
        comodel_name="quotation.calculation", inverse_name='sale_order_id',
        string='Calculation'
    )
    calculation_count = fields.Integer(compute="_compute_calculation_count")

    def _compute_calculation_count(self):
        """ Compute calculation_count related to current order """
        for order in self:
            order.calculation_count = self.env['quotation.calculation'].search_count([
                ('sale_order_id', '=', order.id)
            ])

    def action_view_calculation(self):
        return self._action_view_calculation()

    def _action_view_calculation(self):
        """ """
        action = self.env['ir.actions.actions']._for_xml_id(
            'st_calculation.st_quotation_calculation_act_window'
        )
        action['domain'] = [('sale_order_id', '=', self.id)]
        action['context'] = {
            "default_sale_order_id": self.id,
            "default_partner_id": self.partner_id.id,
            "default_assigned_id": self.env.user.id
        }
        return action

    def button_create_calculation(self):
        """ """
        return self._action_create_calculation()

    def _action_create_calculation(self):
        """ """
        view = self.env.ref('st_calculation.st_quotation_calculation_form_view')
        action = {
            'view_mode': 'form',
            'res_model': 'quotation.calculation',
            'type': 'ir.actions.act_window',
            'view_id': view.id,
            'context': {
                "default_sale_order_id": self.id,
                "default_partner_id": self.partner_id.id,
                "default_assigned_id": self.env.user.id,
            },
        }
        return action


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    calculation_id = fields.Many2one(comodel_name='quotation.calculation', string='Calculation')
