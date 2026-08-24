# Generado desde el codigo v13: campos sin logica ni vistas.
from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    l10n_do_itbis_amount = fields.Monetary(string='ITBIS Amount', currency_field='currency_id', readonly=True)
