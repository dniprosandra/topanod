import os
import base64

from odoo import fields, models, _
from odoo.tools import human_size


class ImportProductWizard(models.Model):
    _name = 'st.import.product.wizard'
    _description = 'Import Product Wizard'

    calculation_id = fields.Many2one(comodel_name='quotation.calculation')
    attachment_ids = fields.One2many(
        comodel_name='ir.attachment', inverse_name='res_id',
        domain=[('res_model', '=', 'st.import.product.wizard')],
        string='Attachments'
    )

    def import_product(self):
        counter = 0
        for file in self.attachment_ids:
            if self._add_product_to_calculation(file):
                counter += 1
        return self._get_notification(counter)

    def _add_product_to_calculation(self, file):
        file_name = self.get_file_name(file.name)
        product_vals = {
            'name': file_name,
            'partner_id': self.calculation_id.partner_id.id,
        }
        product_id = self._create_product_from_pdf(product_vals)
        if product_id:
            # Create document for a product
            document = self._create_document(product_id, file)

            #  Add product to calculation
            result = self.calculation_id.calculation_line_ids = ([(0, 0, {
                'product_id': product_id.id,
                'file_url': document.local_url,
            })])
            if result:
                return result
        file.unlink()

    def _create_document(self, product_id, file):
        """ Create attached document fo the product template """
        product_doc = self.env['product.document'].create({
            'datas': file.datas,
            'ir_attachment_id': file.id,
            'type': 'binary',
            'res_id': product_id.product_tmpl_id.id,
            'res_model': product_id.product_tmpl_id._name,
        })
        return product_doc

    def _create_product_from_pdf(self, data: dict):
        """ Create product document from file name """
        product = self.env['product.template']
        product_search = product.search_count([('name', '=', data['name'])])
        if not product_search:
            product_tmpl_id = self.env['product.template'].create(data)
            product_id = self.env['product.product'].search([
                ('product_tmpl_id', '=', product_tmpl_id.id)
            ], limit=1)
            return product_id

    def get_file_name(self, file_name: str) -> str:
        """ Get file name without extension """
        name = os.path.splitext(file_name)[0]
        return name

    def _get_notification(self, counter: int) -> dict:
        """ Create notification action """
        # TODO: Write condition to change notification text for success or not import.
        attach_count = len(self.attachment_ids)
        msg = _("Imported %s product from %s" % (counter, attach_count))
        notify_type = 'warning' if attach_count != counter else 'success'
        title = _("Product Import")

        # Wizard stay opened
        # notification = {
        #     'type': 'ir.actions.client',
        #     'tag': 'display_notification',
        #     'params': {
        #         'title': title,
        #         'type': notify_type,
        #         'message': msg,
        #         'sticky': True,
        #     },
        # }

        # Wizard closed
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': title,
                'message': msg,
                'type': notify_type,
                'sticky': True,  # True/False will display for few seconds if false
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }
        return notification
