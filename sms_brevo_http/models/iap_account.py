# Copyright 2022 Moka Tourisme (https://www.mokatourisme.fr).
# @author Pierre Verkest <pierreverkest84@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class IapAccount(models.Model):
    _inherit = "iap.account"

    provider = fields.Selection(
        selection_add=[("sms_brevo_http", "SMS Sendinblue")],
        ondelete={"sms_brevo_http": "cascade"},
    )
    sms_brevo_http_api_key = fields.Char(string="API KEY")
    sms_brevo_http_from = fields.Char(string="Expeditor")

    def _get_service_from_provider(self):
        if self.provider == "sms_brevo_http":
            return "sms"
        return super()._get_service_from_provider()

    @api.model
    def get_credits_url(self, service_name, base_url="", credit=0, trial=False):
        first_account = self.search([("service_name", "=", service_name)], limit=1)
        if first_account.provider == "sms_brevo_http" and service_name == "sms":
            return "https://app.brevo.com/billing/addon/customize/sms"
        return super().get_credits_url(
            service_name, base_url=base_url, credit=credit, trial=trial
        )
