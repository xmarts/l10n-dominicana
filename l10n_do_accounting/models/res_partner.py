# Generado desde el codigo v13: campos sin logica ni vistas.
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"
    l10n_do_dgii_tax_payer_type = fields.Char(string='Taxpayer Type', readonly=True)
    l10n_do_expense_type = fields.Char(string='Cost & Expense Type', readonly=True)
    country_id = fields.Many2one(readonly=True)
