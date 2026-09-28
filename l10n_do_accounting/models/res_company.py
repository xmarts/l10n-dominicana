# Historico v13. l10n_do_country_code, l10n_do_ecf_issuer y
# l10n_do_ecf_deferred_submissions los declara l10n_do_ecf (Jenrax).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_do_dgii_start_date = fields.Date(string="Inicio de actividades (v13)", readonly=True)
    l10n_do_default_client = fields.Char(string="Cliente por defecto (v13)", readonly=True)
