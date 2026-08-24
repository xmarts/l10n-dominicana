# Generado desde el esquema real de la base migrada, no del codigo v13.
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"
    l10n_do_dgii_tax_payer_type = fields.Char(readonly=True)  # 14.747 registros en el origen
    l10n_do_expense_type = fields.Char(readonly=True)  # 1.247 registros en el origen
