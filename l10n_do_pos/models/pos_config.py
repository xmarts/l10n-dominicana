# Generado desde el codigo v13: campos sin logica ni vistas.
from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"
    l10n_do_default_partner_id = fields.Many2one(comodel_name='res.partner', string='Default partner', readonly=True)
    l10n_do_order_loading_options = fields.Char(string='Loading options', readonly=True)
    l10n_do_number_of_days = fields.Integer(string='Last Days (invoices)', readonly=True)
    l10n_latam_use_documents = fields.Boolean(readonly=True)
    l10n_do_credit_notes_number_of_days = fields.Integer(string='Last Days (refunds)', readonly=True)
    l10n_latam_country_code = fields.Char(help='Technical field used to hide/show fields regarding the localization', readonly=True)
