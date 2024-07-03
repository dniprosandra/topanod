/** @odoo-module **/

import {ActivityMenu} from "@mail/core/web/activity_menu";
import {session} from "@web/session";
import {patch} from "@web/core/utils/patch";

patch(ActivityMenu.prototype, {
    openActivityGroup(group, filter = "all") {
        const context = {};
        if (group.model === "quotation.calculation") {
            document.body.click(); // hack to close dropdown
            if (filter === "my") {
                alert("my")
                context["search_default_activities_overdue"] = 1;
                context["search_default_activities_today"] = 1;
            } else {
                context["search_default_activities_" + filter] = 1;
            }
            // Necessary because activity_ids of mail.activity.mixin has auto_join
            // So, duplicates are faking the count and "Load more" doesn't show up
            context["force_search_count"] = 1;
            let domain = [
                ['activity_user_id', '=', session.uid],
            ]
            console.log(context)
            console.log("fiter - " + filter)

            this.action.doAction({
                type: 'ir.actions.act_window',
                name: "Quotation Calculation",
                res_model: group.model,
                views: [[false, 'list'], [false, 'form']],
                search_view_id: [false],
                domain: domain,
            }, {
                additionalContext: context,
                clearBreadcrumbs: true,
            });
        } else {
            return super.openActivityGroup(group, filter);
        }
    }
});
