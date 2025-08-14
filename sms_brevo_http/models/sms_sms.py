# Copyright 2022 Moka Tourisme (https://www.mokatourisme.fr).
# @author Pierre Verkest <pierreverkest84@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

# from odoo.addons.sms.models.sms_sms import SmsSms


class SmsSms(models.Model):
    _inherit = "sms.sms"

    @api.model
    def _get_brevo_sms_error_state_mapping(self):
        return {
            "not_enough_credits": "sms_credit",
            "unauthorized": "sms_acc",
            "invalid_parameter": "sms_brevo_invalid_parameter",
            "missing_parameter": "sms_brevo_missing_parameter",
            "out_of_range": "sms_brevo_out_of_range",
            "campaign_processing": "sms_brevo_campaign_processing",
            "campaign_sent": "sms_brevo_campaign_sent",
            "document_not_found": "sms_brevo_document_not_found",
            "reseller_permission_denied": "sms_brevo_reseller_permission_denied",
            "permission_denied": "sms_brevo_permission_denied",
            "duplicate_parameter": "sms_brevo_duplicate_parameter",
            "duplicate_request": "sms_brevo_duplicate_request",
            "method_not_allowed": "sms_brevo_method_not_allowed",
            "account_under_validation": "sms_brevo_account_under_validation",
            "not_acceptable": "sms_brevo_not_acceptable",
        }

    @property
    def IAP_TO_SMS_STATE(self):
        sms_mapping_error_state = super().IAP_TO_SMS_STATE
        sms_mapping_error_state.update(self._get_brevo_sms_error_state_mapping())
        return sms_mapping_error_state

    failure_type = fields.Selection(
        selection_add=[
            ("sms_brevo_invalid_parameter", "Invalid parameter"),
            ("sms_brevo_missing_parameter", "Missing parameter"),
            ("sms_brevo_out_of_range", "Out of range"),
            ("sms_brevo_campaign_processing", "Campaign processing"),
            ("sms_brevo_campaign_sent", "Campaign sent"),
            ("sms_brevo_document_not_found", "Document not found"),
            ("sms_brevo_reseller_permission_denied", "Reseller permission denied"),
            ("sms_brevo_permission_denied", "Permission denied"),
            ("sms_brevo_duplicate_parameter", "Duplicate parameter"),
            ("sms_brevo_duplicate_request", "Duplacate request"),
            ("sms_brevo_method_not_allowed", "Method not allowed"),
            ("sms_brevo_account_under_validation", "Account under validation"),
            ("sms_brevo_not_acceptable", "Not acceptable"),
        ],
    )
    error_detail = fields.Text(readonly=True)

    def _split_batch(self):
        if self.env["sms.api"]._is_sent_with_brevo():
            # to send batch using Sendinblue we should probably consider
            # `SMS Campaingns
            # <https://developers.brevo.com/reference/getsmscampaigns-1>`_
            for record in self:
                yield [record.id]
        else:
            yield from super()._split_batch()
