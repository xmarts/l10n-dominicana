# Generado desde el codigo v13: campos sin logica ni vistas.
from odoo import fields, models


class IrSequence(models.Model):
    _inherit = "ir.sequence"
    expiration_date = fields.Date(string='NCF Expiration date', readonly=True)
