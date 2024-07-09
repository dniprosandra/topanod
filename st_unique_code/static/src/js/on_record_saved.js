/** @odoo-module **/

import {FormController} from "@web/views/form/form_controller";
import {patch} from "@web/core/utils/patch";
import {_t} from "@web/core/l10n/translation";
import {useService} from "@web/core/utils/hooks";

patch(FormController.prototype, {

    setup() {
        super.setup()
        this.notification = useService("notification");
    },

    async onWillSaveRecord(record) {
        this.savingRecordId = record.resId;
        return super.onWillSaveRecord(...arguments);
    },

    async onRecordSaved(record) {
        if (record.resId !== this.savingRecordId) {
            if (record.model.config.resModel === 'product.template' && !record.data.partner_id) {
                this.notification.add(_t(
                        "Please pay attention that the product does not have a customer. \n" +
                        "The product number has not been generated."
                    ),
                    {
                        title: _t("Product created"),
                        type: "warning",
                        sticky: false
                    }
                );
            }
        }
        return super.onRecordSaved(...arguments);
    },

})
