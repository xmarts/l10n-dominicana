# Historico v13.
#
# l10n_do_dgii_tax_payer_type va como Selection, no como Char: tres campos de
# Studio (x_studio_{rf,cl,pro}_tipo_de_contribuyente en factura, venta y
# compra) son `related` de tipo selection a este campo, y con un Char Odoo los
# descarta. Jenrax no declara este campo. Valores: los de v13
# (l10n_do_accounting/models/res_partner.py de la rama 13.0).
#
# country_id no se toca: es del core.
from odoo import fields, models

TAX_PAYER_TYPES = [
    ("taxpayer", "Contribuyente"),
    ("non_payer", "No contribuyente"),
    ("nonprofit", "Sin fines de lucro"),
    ("special", "Regimen especial"),
    ("governmental", "Gubernamental"),
    ("foreigner", "Extranjero"),
]


class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_do_dgii_tax_payer_type = fields.Selection(TAX_PAYER_TYPES, string="Tipo de contribuyente (v13)", readonly=True)
    l10n_do_expense_type = fields.Char(string="Tipo de costo y gasto (v13)", readonly=True)
