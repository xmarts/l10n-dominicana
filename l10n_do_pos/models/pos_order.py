# Generado desde el codigo v13: campos sin logica ni vistas.
from odoo import fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"
    l10n_latam_document_number = fields.Char(string='Fiscal Number', readonly=True)
    l10n_latam_document_type_id = fields.Many2one(comodel_name='l10n_latam.document.type', string='Document Type', readonly=True)
    l10n_latam_sequence_id = fields.Many2one(comodel_name='ir.sequence', string='Fiscal Sequence', readonly=True)
    l10n_do_ncf_expiration_date = fields.Date(string='NCF expiration date', readonly=True)
    l10n_latam_use_documents = fields.Boolean(readonly=True)
    state = fields.Char(readonly=True)
    l10n_do_origin_ncf = fields.Char(string='Modified NCF', readonly=True)
    l10n_do_is_return_order = fields.Boolean(string='Return order', readonly=True)
    l10n_do_return_order_id = fields.Many2one(comodel_name='pos.order', string='Modifies', readonly=True)
    l10n_do_return_status = fields.Char(string='Return status', readonly=True)
    l10n_latam_country_code = fields.Char(help='Technical field used to hide/show fields regarding the localization', readonly=True)


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"
    l10n_do_line_qty_returned = fields.Integer(string='Return line', readonly=True)
    l10n_do_original_line_id = fields.Many2one(comodel_name='pos.order.line', string='Original line', readonly=True)


class PosOrderPaymentCreditNote(models.Model):
    _name = "pos.order.payment.credit.note"
    _description = "pos.order.payment.credit.note"
    name = fields.Char(readonly=True)
    amount = fields.Monetary(currency_field='currency_id', readonly=True)
    account_move_id = fields.Many2one(comodel_name='account.move', string='Credit note', readonly=True)
    currency_id = fields.Many2one(comodel_name='res.currency', readonly=True)
    pos_order_id = fields.Many2one(comodel_name='pos.order', string='order', readonly=True)
