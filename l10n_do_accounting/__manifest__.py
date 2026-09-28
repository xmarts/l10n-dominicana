{
    "name": "Fiscal Accounting (Rep. Dominicana) - puente v13",
    "summary": "Conserva en solo lectura el historico de l10n_do_accounting v13 y prepara la base para la localizacion de Jenrax",
    "version": "19.0.2.0.0",
    "category": "Accounting/Localizations",
    "license": "LGPL-3",
    "author": "Xmarts",
    # Sin dependencia de Jenrax A PROPOSITO: asi Odoo lo carga en la fase 1
    # del grafo, antes de instalar Jenrax, y su pre-migrate prepara las
    # columnas que Jenrax recalcularia o rellenaria sobre el historico.
    # Ver migrations/19.0.2.0.0/pre-migrate.py y PUENTE_LOCALIZACION_JENRAX.md.
    "depends": ["l10n_latam_invoice_document", "l10n_do"],
    "data": ["data/l10n_latam.document.type.csv", "security/res_groups.xml"],
    "installable": True,
    "auto_install": False,
}
