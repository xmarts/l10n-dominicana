# Generado desde el codigo v13: campos sin logica ni vistas.
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"
    l10n_do_expense_type = fields.Char(string='Cost & Expense Type', readonly=True)
    l10n_do_cancellation_type = fields.Char(string='Cancellation Type', readonly=True)
    l10n_do_income_type = fields.Char(string='Income Type', readonly=True)
    l10n_do_origin_ncf = fields.Char(string='Modifies', readonly=True)
    ncf_expiration_date = fields.Date(string='Valid until', readonly=True)
    is_debit_note = fields.Boolean(readonly=True)
    cancellation_type = fields.Char(string='Cancellation Type (deprecated)', readonly=True)
    is_ecf_invoice = fields.Boolean(readonly=True)
    l10n_do_ecf_modification_code = fields.Char(string='e-CF Modification Code', readonly=True)
    l10n_do_ecf_security_code = fields.Char(string='e-CF Security Code', readonly=True)
    l10n_do_ecf_sign_date = fields.Datetime(string='e-CF Sign Date', readonly=True)
    l10n_do_electronic_stamp = fields.Char(string='Electronic Stamp', readonly=True)
    l10n_do_company_in_contingency = fields.Boolean(string='Company in contingency', readonly=True)
    is_l10n_do_internal_sequence = fields.Boolean(string='Is internal sequence', readonly=True)
    l10n_do_ecf_edi_file = fields.Binary(string='ECF XML File', readonly=True)
    l10n_do_ecf_edi_file_name = fields.Char(string='ECF XML File Name', readonly=True)
