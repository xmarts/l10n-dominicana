# Generado desde el esquema real de la base migrada, no del codigo v13.
from odoo import fields, models


class IrSequence(models.Model):
    _inherit = "ir.sequence"
    expiration_date = fields.Date(readonly=True)  # 346 registros en el origen
