from odoo import models, _


class QuotationCalculationLine(models.Model):
    _inherit = 'quotation.calculation'

    def write(self, vals):
        result = super().write(vals)
        state = vals.get('state', False)
        if result and state in ['in_production', 'calculated', 'new']:
            for line in self:
                line._create_user_activity(state)
        return result

    def _create_user_activity(self, state):
        if state == 'in_production':
            department_id = self.assigned_department_id.id
            dep_employee_ids = self.env['hr.employee'].search([('department_id', '=', department_id)])
            self._unlink_activity()
            for employee in dep_employee_ids:
                self._create_activity(employee.user_id.id)
        elif state == 'calculated' or 'new':
            self._unlink_activity()
            self._create_activity(self.assigned_id.id)

    def _unlink_activity(self):
        return self.activity_unlink(['st_calculation_activity.st_calculation_notification_activity'])

    def _create_activity(self, user_id):
        self.ensure_one()
        calc_ref = self._get_html_link()
        customer_ref = self.partner_id._get_html_link()
        self.activity_schedule(
            'st_calculation_activity.st_calculation_notification_activity',
            user_id=user_id,
            note=_("Calculation %(calc)s for customer %(customer)s", calc=calc_ref, customer=customer_ref)
        )


