# Generado desde el codigo v13: campos sin logica ni vistas.
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"
    l10n_do_expense_type = fields.Char(string='Cost & Expense Type', readonly=True)
    l10n_do_cancellation_type = fields.Char(string='Cancellation Type', readonly=True)
    l10n_do_income_type = fields.Char(string='Income Type', readonly=True)
    l10n_do_origin_ncf = fields.Char(string='Modifies', readonly=True)
    ncf_expiration_date = fields.Date(string='Valid until', readonly=True)
    is_debit_note = fields.Boolean(readonly=True)
    cancellation_type = fields.Char(string='Cancellation Type (deprecated)', readonly=True)
    is_ecf_invoice = fields.Boolean(readonly=True)
    l10n_do_ecf_modification_code = fields.Char(string='e-CF Modification Code', readonly=True)
    l10n_do_ecf_security_code = fields.Char(string='e-CF Security Code', readonly=True)
    l10n_do_ecf_sign_date = fields.Datetime(string='e-CF Sign Date', readonly=True)
    l10n_do_electronic_stamp = fields.Char(string='Electronic Stamp', readonly=True)
    l10n_do_company_in_contingency = fields.Boolean(string='Company in contingency', readonly=True)
    is_l10n_do_internal_sequence = fields.Boolean(string='Is internal sequence', readonly=True)
    l10n_do_ecf_edi_file = fields.Binary(string='ECF XML File', readonly=True)
    l10n_do_ecf_edi_file_name = fields.Char(string='ECF XML File Name', readonly=True)

    # El informe de facturas de PSI (accion 894) llama a este metodo en la
    # plantilla: <t t-set="l10n_do_amounts" t-value="o._get_l10n_do_amounts()"/>.
    # Sin el, el PDF no se puede generar.
    #
    # El original calcula bases e importes de ITBIS e ISR agrupando por
    # tax_group_id. Eso es logica, y este dummy no repone logica: devuelve la
    # misma estructura con las doce claves a cero, para que la vista resuelva
    # sin inventar cifras fiscales.
    #
    # Cuando entre la localizacion definitiva, su implementacion sustituye a
    # esta y los importes pasan a ser los reales.
    def _get_l10n_do_amounts(self):
        self.ensure_one()
        return {
            "base_amount": 0.0,
            "exempt_amount": 0.0,
            "itbis_0_base_amount": 0.0,
            "itbis_0_tax_amount": 0.0,
            "itbis_16_base_amount": 0.0,
            "itbis_16_tax_amount": 0.0,
            "itbis_18_base_amount": 0.0,
            "itbis_18_tax_amount": 0.0,
            "itbis_withholding_amount": 0.0,
            "itbis_withholding_base_amount": 0.0,
            "isr_withholding_amount": 0.0,
            "isr_withholding_base_amount": 0.0,
        }
