# Generado desde el esquema real de la base migrada, no del codigo v13.
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"
    l10n_do_currency_interval_unit = fields.Char(readonly=True)
    l10n_do_currency_next_execution_date = fields.Date(readonly=True)
    l10n_do_currency_provider = fields.Char(readonly=True)
    l10n_do_default_client = fields.Char(readonly=True)
    l10n_do_dgii_start_date = fields.Date(readonly=True)
    l10n_do_ecf_deferred_submissions = fields.Boolean(readonly=True)
    l10n_do_ecf_issuer = fields.Boolean(readonly=True)
