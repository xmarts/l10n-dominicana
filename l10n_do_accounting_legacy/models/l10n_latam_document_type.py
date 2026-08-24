# Generado desde el esquema real de la base migrada, no del codigo v13.
from odoo import fields, models


class L10n_latamDocumentType(models.Model):
    _inherit = "l10n_latam.document.type"
    l10n_do_ncf_type = fields.Char(readonly=True)  # 21 registros en el origen
