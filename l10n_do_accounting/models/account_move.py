# Historico v13 de l10n_do_accounting, en solo lectura y sin logica.
#
# No se declaran aqui los campos que la localizacion de Jenrax ya declara
# (ncf_expiration_date, is_debit_note, l10n_do_ecf_modification_code): la
# columna es la misma y Jenrax la gobierna. Tampoco _get_l10n_do_amounts, que
# l10n_do_ncf implementa.
#
# Donde Jenrax tiene el equivalente con otro nombre, pre-migrate copia el dato:
#   l10n_do_income_type        -> income_type
#   l10n_do_expense_type       -> expense_type
#   l10n_do_cancellation_type  -> annulation_type
#   l10n_do_origin_ncf         -> origin_out
#   is_ecf_invoice             -> l10n_do_ecf_invoice
# El original se conserva aqui como referencia.
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_do_expense_type = fields.Char(string="Tipo de costo y gasto (v13)", readonly=True)
    l10n_do_cancellation_type = fields.Char(string="Tipo de anulacion (v13)", readonly=True)
    l10n_do_income_type = fields.Char(string="Tipo de ingreso (v13)", readonly=True)
    l10n_do_origin_ncf = fields.Char(string="NCF modificado (v13)", readonly=True)
    cancellation_type = fields.Char(string="Tipo de anulacion antiguo (v13)", readonly=True)
    is_ecf_invoice = fields.Boolean(string="Factura e-CF (v13)", readonly=True)
    l10n_do_ecf_security_code = fields.Char(string="Codigo de seguridad e-CF (v13)", readonly=True)
    l10n_do_ecf_sign_date = fields.Datetime(string="Fecha de firma e-CF (v13)", readonly=True)
    l10n_do_electronic_stamp = fields.Char(string="Sello electronico (v13)", readonly=True)
    l10n_do_company_in_contingency = fields.Boolean(string="Compania en contingencia (v13)", readonly=True)
    is_l10n_do_internal_sequence = fields.Boolean(string="Secuencia interna (v13)", readonly=True)
    l10n_do_ecf_edi_file = fields.Binary(string="XML e-CF (v13)", readonly=True)
    l10n_do_ecf_edi_file_name = fields.Char(string="Nombre del XML e-CF (v13)", readonly=True)
