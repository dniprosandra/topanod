import os

from odoo import fields, models, _


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
        attachment_len = len(self.attachment_ids)
        exist_product = ""
        attachment = self.attachment_ids
        for file in attachment:
            file_name = self.get_file_name(file.name)
            if file_name:
                # TODO: Find another way to search existing products
                product_search = self.env['product.template'].search_count([('name', '=', file_name)])
                # Delete attachment if product exist
                if product_search:
                    exist_product += f"{file_name};\n "
                    self._delete_attachment(file.id)
                    continue
                if self._add_product_to_calculation(file):
                    counter += 1
            else:
                # Delete attachment if no name
                self._delete_attachment(file.id)

        return self._get_notification(counter, attachment_len, exist_product)

    def _add_product_to_calculation(self, file):
        file_name = self.get_file_name(file.name)
        product_vals = {
            'name': file_name,
            'partner_id': self.calculation_id.partner_id.id,
        }
        product_id = self._create_product_from_pdf(product_vals)

        # Attach document to the product
        document = self._create_document(product_id, file)
        product_id.attached_file = document.id

        #  Add product to calculation
        result = self.calculation_id.calculation_line_ids = ([(0, 0, {
            'product_id': product_id.id,
        })])
        if result:
            return result

    def _create_document(self, product_id, file):
        """ Create attached document fo the product template """
        product_doc = self.env['product.document'].create({
            'datas': file.datas,
            'ir_attachment_id': file.id,
            'type': 'binary',
            'res_id': product_id.id,
            'res_model': product_id._name,
        })
        return product_doc

    def _create_product_from_pdf(self, data: dict):
        """ Create product document from file name """
        product_id = self.env['product.product'].create(data)
        return product_id

    def get_file_name(self, file_name: str) -> str:
        """ Get file name without extension """
        name = os.path.splitext(file_name)[0]
        return name

    def _get_notification(self, counter: int, attach_count: int, exist_product: str) -> dict:
        """ Create notification action """
        msg = _("Imported %s product from %s . \n") % (counter, attach_count)
        notify_type = 'warning' if counter == 0 or exist_product else 'success'
        title = _("Product Import")
        if exist_product:
            msg += _("\n Product(s) already exist: \n")
            msg += exist_product

        # Wizard closed
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': title,
                'message': msg,
                'type': notify_type,
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }
        return notification

    def _delete_attachment(self, attachment_id):
        attach = self.env['ir.attachment'].search([('id', '=', attachment_id)])
        return attach.unlink()
