# Los 22 tipos de documento de v13 los carga data/l10n_latam.document.type.csv
# con su XML-ID: siguen referenciados por 36.289 facturas y 176.204 apuntes.
# internal_type es del core (Selection): no se redeclara.
from odoo import fields, models


class L10nLatamDocumentType(models.Model):
    _inherit = "l10n_latam.document.type"

    l10n_do_ncf_type = fields.Char(string="Tipo NCF (v13)", readonly=True)
    is_vat_required = fields.Boolean(string="Requiere RNC (v13)", readonly=True)
