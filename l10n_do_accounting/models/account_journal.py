# Generado desde el codigo v13: campos sin logica ni vistas.
from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"
    l10n_do_payment_form = fields.Char(string='Payment Form', readonly=True)
