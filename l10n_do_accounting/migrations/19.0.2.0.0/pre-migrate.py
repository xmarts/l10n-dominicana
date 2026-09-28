"""Fase 0 del puente hacia la localizacion de Jenrax.

Por que existe
--------------
Jenrax (l10n_do_ncf, l10n_do_dgii_reports, l10n_do_ecf) crea columnas nuevas
en tablas que ya tienen el historico de PSI. Al crearlas, Odoo:

  * rellena los `default` en todas las filas (`_init_column`):
    income_type='01' en las 110.130 facturas, l10n_do_ecf_send_mode='automatic'
    (envio automatico de e-CF), l10n_do_ecf_invoice con un solo valor para
    todas, l10n_do_tax_type='none' en todos los impuestos...
  * recalcula los `compute` + `store`: al crear withholding_itbis recalcula
    `_compute_withholding_taxes`, que reescribe tambien income_withholding e
    isr_withholding_type (columnas con dato v13) y fiscal_status; y
    `_compute_sale_fiscal_type_id` asigna por heuristica el tipo fiscal de los
    14.756 contactos.

Si la columna ya existe, Odoo no hace ninguna de las dos cosas. Este script
las crea antes, pobladas desde el dato v13.

Por que aqui
------------
Tiene que correr ANTES de que Odoo instale Jenrax. Este modulo no depende de
Jenrax, asi que Odoo lo carga en la fase 1 del grafo; Jenrax (`to install`)
va en la fase 2 y dgii_reports (que depende de Jenrax) en la 3
(odoo/modules/module_graph.py, `phase`). Un pre-migrate de dgii_reports ya
llegaria tarde.

Solo SQL. Idempotente: cada columna se crea y se puebla una sola vez; si ya
existe (segunda pasada, o Jenrax ya instalado) no se toca.
"""
import logging

_logger = logging.getLogger(__name__)


def _table_exists(cr, table):
    cr.execute("SELECT to_regclass(%s) IS NOT NULL", (f"public.{table}",))
    return cr.fetchone()[0]


def _column_exists(cr, table, column):
    cr.execute(
        "SELECT 1 FROM information_schema.columns WHERE table_schema = 'public' AND table_name = %s AND column_name = %s",
        (table, column),
    )
    return bool(cr.fetchone())


def _crear(cr, table, column, pgtype, poblar_sql=None, requiere=()):
    """Crea table.column si no existe y la puebla con poblar_sql.

    `requiere` son columnas de origen que deben existir para poblar. Si falta
    alguna, la columna se crea vacia y se avisa.
    """
    if not _table_exists(cr, table):
        _logger.info("puente fase 0: %s no existe, se omite %s", table, column)
        return
    if _column_exists(cr, table, column):
        _logger.info("puente fase 0: %s.%s ya existe, no se toca", table, column)
        return
    cr.execute(f'ALTER TABLE "{table}" ADD COLUMN "{column}" {pgtype}')
    faltan = [c for c in requiere if not _column_exists(cr, table, c)]
    if poblar_sql and not faltan:
        cr.execute(poblar_sql)
        _logger.info("puente fase 0: %s.%s creada y poblada (%s filas)", table, column, cr.rowcount)
    elif faltan:
        _logger.warning("puente fase 0: %s.%s creada VACIA, faltan columnas de origen %s", table, column, faltan)
    else:
        _logger.info("puente fase 0: %s.%s creada sin datos", table, column)


def _conteos_base(cr):
    """Guarda los conteos que la verificacion final (dgii_reports, end-) compara."""
    cr.execute(
        "CREATE TABLE IF NOT EXISTS psi_mig_conteo (clave varchar PRIMARY KEY, valor bigint, fecha timestamp DEFAULT now())"
    )
    consultas = {
        "account_move.l10n_do_income_type": "SELECT count(*) FROM account_move WHERE l10n_do_income_type IS NOT NULL",
        "account_move.l10n_do_expense_type": "SELECT count(*) FROM account_move WHERE l10n_do_expense_type IS NOT NULL",
        "account_move.annulation_origen": "SELECT count(*) FROM account_move WHERE coalesce(l10n_do_cancellation_type, cancellation_type) IS NOT NULL",
        "account_move.l10n_do_origin_ncf": "SELECT count(*) FROM account_move WHERE nullif(trim(l10n_do_origin_ncf), '') IS NOT NULL",
        "account_move.ncf_expiration_date": "SELECT count(*) FROM account_move WHERE ncf_expiration_date IS NOT NULL",
        "account_move.is_ecf_invoice": "SELECT count(*) FROM account_move WHERE is_ecf_invoice",
        "account_move.l10n_latam_document_type_id": "SELECT count(*) FROM account_move WHERE l10n_latam_document_type_id IS NOT NULL",
        "account_move_line.l10n_latam_document_type_id": "SELECT count(*) FROM account_move_line WHERE l10n_latam_document_type_id IS NOT NULL",
        "account_move.income_withholding": "SELECT count(*) FROM account_move WHERE income_withholding <> 0",
        "account_move.isr_withholding_type": "SELECT count(*) FROM account_move WHERE nullif(isr_withholding_type, '') IS NOT NULL",
        "account_move.withholded_itbis": "SELECT count(*) FROM account_move WHERE withholded_itbis <> 0",
        "account_move.fiscal_status": "SELECT count(*) FROM account_move WHERE nullif(fiscal_status, '') IS NOT NULL",
        "account_move.payment_form": "SELECT count(*) FROM account_move WHERE nullif(payment_form, '') IS NOT NULL",
        "account_move.hash_id_ref": "SELECT ('x' || substr(md5(string_agg(id::text || '|' || coalesce(ref, ''), ',' ORDER BY id)), 1, 15))::bit(60)::bigint FROM account_move",
        "res_partner.l10n_do_dgii_tax_payer_type": "SELECT count(*) FROM res_partner WHERE l10n_do_dgii_tax_payer_type IS NOT NULL",
        "res_partner.l10n_do_expense_type": "SELECT count(*) FROM res_partner WHERE l10n_do_expense_type IS NOT NULL",
        "account_journal.l10n_latam_use_documents": "SELECT count(*) FROM account_journal WHERE l10n_latam_use_documents",
        "account_journal.l10n_do_payment_form": "SELECT count(*) FROM account_journal WHERE nullif(l10n_do_payment_form, '') IS NOT NULL",
        "l10n_latam_document_type.xmlid_l10n_do_accounting": "SELECT count(*) FROM ir_model_data WHERE module = 'l10n_do_accounting' AND model = 'l10n_latam.document.type'",
        "dgii_reports": "SELECT count(*) FROM dgii_reports",
        "dgii_reports.sent": "SELECT count(*) FROM dgii_reports WHERE state = 'sent'",
        "dgii_reports_purchase_line": "SELECT count(*) FROM dgii_reports_purchase_line",
        "dgii_reports_sale_line": "SELECT count(*) FROM dgii_reports_sale_line",
        "dgii_reports_sale_summary": "SELECT count(*) FROM dgii_reports_sale_summary",
        "dgii_reports_cancel_line": "SELECT count(*) FROM dgii_reports_cancel_line",
        "dgii_reports_exterior_line": "SELECT count(*) FROM dgii_reports_exterior_line",
        "invoice_service_type_detail": "SELECT count(*) FROM invoice_service_type_detail",
        "account_move.x_studio_di_numero_de_comprobante": "SELECT count(*) FROM account_move WHERE nullif(x_studio_di_numero_de_comprobante, '') IS NOT NULL",
        "account_move.x_studio_rf_tipo_de_contribuyente": "SELECT count(*) FROM account_move WHERE x_studio_rf_tipo_de_contribuyente IS NOT NULL",
        "account_move.itbis_to_cost": "SELECT count(*) FROM account_move WHERE itbis_to_cost",
        "payment_invoice_line": "SELECT count(*) FROM payment_invoice_line",
    }
    for clave, sql in consultas.items():
        cr.execute("SAVEPOINT psi_conteo")
        try:
            cr.execute(sql)
            valor = cr.fetchone()[0]
        except Exception as e:  # tabla o columna que no existe en esta base
            cr.execute("ROLLBACK TO SAVEPOINT psi_conteo")
            _logger.info("puente fase 0: conteo %s omitido (%s)", clave, str(e).splitlines()[0])
            continue
        cr.execute("RELEASE SAVEPOINT psi_conteo")
        # ON CONFLICT DO NOTHING: la primera medicion es la que vale.
        cr.execute(
            "INSERT INTO psi_mig_conteo (clave, valor) VALUES (%s, %s) ON CONFLICT (clave) DO NOTHING",
            (clave, valor),
        )


def migrate(cr, version):
    if not version:
        return
    _logger.info("puente fase 0: desde %s", version)

    _conteos_base(cr)

    # --- account.move -----------------------------------------------------
    _crear(cr, "account_move", "withholding_itbis", "numeric", """
        UPDATE account_move SET withholding_itbis = CASE
            WHEN move_type IN ('in_invoice', 'in_refund') THEN coalesce(withholded_itbis, 0)
            WHEN move_type IN ('out_invoice', 'out_refund') THEN coalesce(third_withheld_itbis, 0)
            ELSE 0 END
    """, requiere=("withholded_itbis", "third_withheld_itbis"))
    _crear(cr, "account_move", "is_l10n_do_fiscal_invoice", "boolean", """
        UPDATE account_move am SET is_l10n_do_fiscal_invoice = coalesce(aj.l10n_latam_use_documents, false)
          FROM account_journal aj WHERE aj.id = am.journal_id
    """)
    _crear(cr, "account_move", "fiscal_sequence_id", "int4")
    _crear(cr, "account_move", "income_type", "varchar",
           "UPDATE account_move SET income_type = l10n_do_income_type WHERE l10n_do_income_type IS NOT NULL",
           requiere=("l10n_do_income_type",))
    _crear(cr, "account_move", "expense_type", "varchar",
           "UPDATE account_move SET expense_type = l10n_do_expense_type WHERE l10n_do_expense_type IS NOT NULL",
           requiere=("l10n_do_expense_type",))
    _crear(cr, "account_move", "annulation_type", "varchar", """
        UPDATE account_move SET annulation_type = coalesce(l10n_do_cancellation_type, cancellation_type)
         WHERE coalesce(l10n_do_cancellation_type, cancellation_type) IS NOT NULL
    """, requiere=("l10n_do_cancellation_type", "cancellation_type"))
    _crear(cr, "account_move", "origin_out", "varchar", """
        UPDATE account_move SET origin_out = nullif(trim(l10n_do_origin_ncf), '')
         WHERE nullif(trim(l10n_do_origin_ncf), '') IS NOT NULL
    """, requiere=("l10n_do_origin_ncf",))
    # En Jenrax l10n_do_ecf_invoice NO es "es un e-CF": es "esta factura la
    # envia PSI a la DGII" (lo fija fiscal_type_id.is_send_ecf,
    # l10n_do_ecf/models/account_move.py constrain_fiscal_type_id). Los 4.668
    # is_ecf_invoice de v13 son e-CF RECIBIDOS de proveedores (E31/E33/E34 en
    # facturas de compra): PSI no emitia e-CF. Nace en False; dgii_reports lo
    # deriva despues del tipo fiscal. El dato v13 sigue en is_ecf_invoice.
    _crear(cr, "account_move", "l10n_do_ecf_invoice", "boolean",
           "UPDATE account_move SET l10n_do_ecf_invoice = false")

    # --- res.partner --------------------------------------------------------
    # Los tipos fiscales (m2o a account.fiscal.type) los rellena dgii_reports
    # cuando la tabla de Jenrax ya existe. Aqui solo se evita el compute.
    _crear(cr, "res_partner", "sale_fiscal_type_id", "int4")
    _crear(cr, "res_partner", "purchase_fiscal_type_id", "int4")
    _crear(cr, "res_partner", "expense_type", "varchar",
           "UPDATE res_partner SET expense_type = l10n_do_expense_type WHERE l10n_do_expense_type IS NOT NULL",
           requiere=("l10n_do_expense_type",))

    # base_vat entra como dependencia de l10n_do_ncf. Su vies_valid es
    # compute + store sobre `vat`: al crear la columna Odoo lo recalcula en los
    # 14.756 contactos (a False, VIES no esta activo) y les cambia write_date a
    # todos. Se crea ya con el valor que Odoo le daria.
    _crear(cr, "res_partner", "vies_valid", "boolean", "UPDATE res_partner SET vies_valid = false")

    # --- res.company --------------------------------------------------------
    # 'manual' hasta que PSI configure sus credenciales e-CF: con el default de
    # Jenrax ('automatic') cualquier factura publicada se enviaria a la DGII.
    _crear(cr, "res_company", "l10n_do_ecf_send_mode", "varchar",
           "UPDATE res_company SET l10n_do_ecf_send_mode = 'manual'")
    # Y que Jenrax no lo pise: su res.company._auto_init (l10n_do_ecf,
    # models/res_company.py) "migra" un booleano antiguo que al instalarse
    # esta vacio y pone 'automatic' a todas las companias, salvo que exista
    # este parametro.
    cr.execute("""
        INSERT INTO ir_config_parameter (key, value, create_uid, create_date, write_uid, write_date)
        VALUES ('l10n_do_ecf.send_mode_migrated', 'true', 1, now(), 1, now())
        ON CONFLICT (key) DO NOTHING
    """)

    # --- account.journal ----------------------------------------------------
    _crear(cr, "account_journal", "l10n_do_fiscal_journal", "boolean",
           "UPDATE account_journal SET l10n_do_fiscal_journal = coalesce(l10n_latam_use_documents, false)")
    _crear(cr, "account_journal", "payment_form", "varchar", """
        UPDATE account_journal SET payment_form = CASE nullif(l10n_do_payment_form, '')
            WHEN 'bond' THEN 'others' ELSE nullif(l10n_do_payment_form, '') END
         WHERE nullif(l10n_do_payment_form, '') IS NOT NULL
    """, requiere=("l10n_do_payment_form",))

    # --- account.tax --------------------------------------------------------
    # v13 marcaba en purchase_tax_type las retenciones; el ITBIS, ISC, otros y
    # propina los reconocia por el nombre del grupo de impuestos.
    _crear(cr, "account_tax", "l10n_do_tax_type", "varchar", """
        UPDATE account_tax t SET l10n_do_tax_type = CASE
            WHEN t.purchase_tax_type IN ('itbis', 'ritbis', 'isr', 'isc', 'other', 'tip', 'rext') THEN t.purchase_tax_type
            WHEN coalesce(g.name->>'es_DO', g.name->>'en_US') = 'ITBIS' THEN 'itbis'
            WHEN coalesce(g.name->>'es_DO', g.name->>'en_US') = 'ISC' THEN 'isc'
            WHEN coalesce(g.name->>'es_DO', g.name->>'en_US') = 'Otros Impuestos' THEN 'other'
            WHEN coalesce(g.name->>'es_DO', g.name->>'en_US') = 'Propina' THEN 'tip'
            ELSE 'none' END
          FROM account_tax_group g WHERE g.id = t.tax_group_id
    """, requiere=("purchase_tax_type",))

    # --- dgii.reports -------------------------------------------------------
    _crear(cr, "dgii_reports", "csmr_ncf_total_other", "numeric",
           "UPDATE dgii_reports SET csmr_ncf_total_other = csmr_ncf_total_othr WHERE csmr_ncf_total_othr IS NOT NULL",
           requiere=("csmr_ncf_total_othr",))
    _crear(cr, "dgii_reports_cancel_line", "annulation_type", "varchar",
           "UPDATE dgii_reports_cancel_line SET annulation_type = anulation_type WHERE anulation_type IS NOT NULL",
           requiere=("anulation_type",))

    # --- Tipos de servicio: que Jenrax actualice los 25 y no cree duplicados --
    # l10n_do_dgii_reports carga los mismos 25 registros (mismos nombres de
    # XML-ID) bajo su modulo. Si el XML-ID ya existe apuntando al registro de
    # PSI, Odoo lo actualiza en vez de crear otro.
    cr.execute("""
        INSERT INTO ir_model_data (module, name, model, res_id, noupdate)
        SELECT 'l10n_do_dgii_reports', d.name, d.model, d.res_id, false
          FROM ir_model_data d
         WHERE d.module = 'dgii_reports' AND d.model = 'invoice.service.type.detail'
           AND NOT EXISTS (SELECT 1 FROM ir_model_data x
                            WHERE x.module = 'l10n_do_dgii_reports' AND x.name = d.name)
    """)
    _logger.info("puente fase 0: %s XML-ID de invoice.service.type.detail preasignados a l10n_do_dgii_reports", cr.rowcount)
