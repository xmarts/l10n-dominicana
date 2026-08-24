# Generado desde el codigo v13: campos sin logica ni vistas.
from odoo import fields, models


class L10nLatamDocumentType(models.Model):
    _inherit = "l10n_latam.document.type"
    l10n_do_ncf_type = fields.Char(string='NCF types', help='NCF types defined by the DGII that can be used to identify the documents presented to the government and that depends on the operation type, the responsibility of both the issuer and the receptor of the document', readonly=True)
    internal_type = fields.Char(readonly=True)
    is_vat_required = fields.Boolean(readonly=True)
