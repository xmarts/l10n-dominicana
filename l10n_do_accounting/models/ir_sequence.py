# Historico v13: vencimiento de las secuencias NCF de Indexa. Jenrax lo guarda
# en account.fiscal.sequence.
from odoo import fields, models


class IrSequence(models.Model):
    _inherit = "ir.sequence"

    expiration_date = fields.Date(string="Vencimiento NCF (v13)", readonly=True)
