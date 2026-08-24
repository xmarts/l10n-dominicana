# Generado desde el esquema real de la base migrada, no del codigo v13.
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"
    cancellation_type = fields.Char(readonly=True)
    is_debit_note = fields.Boolean(readonly=True)  # 22.727 registros en el origen
    is_ecf_invoice = fields.Boolean(readonly=True)  # 46.481 registros en el origen
    l10n_do_cancellation_type = fields.Char(readonly=True)  # 1.493 registros en el origen
    l10n_do_ecf_edi_file_name = fields.Char(readonly=True)
    l10n_do_ecf_modification_code = fields.Char(readonly=True)
    l10n_do_ecf_security_code = fields.Char(readonly=True)
    l10n_do_ecf_sign_date = fields.Datetime(readonly=True)
    l10n_do_electronic_stamp = fields.Char(readonly=True)
    l10n_do_expense_type = fields.Char(readonly=True)  # 18.422 registros en el origen
    l10n_do_income_type = fields.Char(readonly=True)  # 110.089 registros en el origen
    l10n_do_origin_ncf = fields.Char(readonly=True)  # 643 registros en el origen
    ncf_expiration_date = fields.Date(readonly=True)  # 19.239 registros en el origen
