# Historico v13. Jenrax usa account.journal.payment_form; pre-migrate copia
# el dato alli.
from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    l10n_do_payment_form = fields.Char(string="Forma de pago (v13)", readonly=True)
