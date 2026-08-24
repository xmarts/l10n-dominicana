# Generado desde el esquema real de la base migrada, no del codigo v13.
from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"
    l10n_do_payment_form = fields.Char(readonly=True)  # 76 registros en el origen
