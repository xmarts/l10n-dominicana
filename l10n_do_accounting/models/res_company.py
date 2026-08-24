# Generado desde el codigo v13: campos sin logica ni vistas.
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"
    l10n_do_country_code = fields.Char(string='Country Code', readonly=True)
    l10n_do_dgii_start_date = fields.Date(string='Activities Start Date', readonly=True)
    l10n_do_default_client = fields.Char(string='Default Customer', readonly=True)
    l10n_do_ecf_issuer = fields.Boolean(string='Is e-CF issuer', help='When activating this field, NCF issuance is disabled.', readonly=True)
    l10n_do_ecf_deferred_submissions = fields.Boolean(string='Deferred submissions', help='Identify taxpayers who have been previously authorized to have sales through offline mobile devices such as sales with Handheld, enter others.', readonly=True)
