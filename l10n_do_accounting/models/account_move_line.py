# Historico v13: Jenrax calcula el ITBIS al vuelo y no tiene columna propia.
from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    l10n_do_itbis_amount = fields.Monetary(string="Importe ITBIS (v13)", currency_field="currency_id", readonly=True)
