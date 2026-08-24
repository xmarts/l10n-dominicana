# Generado desde el esquema real de la base migrada, no del codigo v13.
from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    l10n_do_itbis_amount = fields.Float(readonly=True)  # 72.689 registros en el origen
