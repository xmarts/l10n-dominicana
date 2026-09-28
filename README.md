# l10n-dominicana — rama `19.0-puente-jenrax`

Puente entre el histórico de la localización dominicana de **Odoo 13
(Indexa)** y la localización de **Jenrax para Odoo 19** (`l10n-do`,
`l10n-do-ecf`, `l10n_do_jenrax`), para bases migradas con Odoo Upgrade.

Parte de `19.0-dummy-pre13`. Fork de `indexa-git/l10n-dominicana` (`13.0`,
commit `0431370`, versión `13.0.1.13.2`).

## Qué hace `l10n_do_accounting` 19.0.2.0.0

1. **Conserva en solo lectura** el histórico v13 que Jenrax no tiene
   (etiquetas "(v13)"): `l10n_do_itbis_amount`, datos e-CF de v13,
   `expiration_date` de las secuencias, los 22 tipos de documento LatAm con su
   XML-ID, y `l10n_do_dgii_tax_payer_type`.
2. **No declara nada que Jenrax declare**: ni modelos, ni campos, ni métodos
   (`ncf_expiration_date`, `is_debit_note`, `l10n_do_ecf_modification_code`,
   `_get_l10n_do_amounts`…). Esas columnas las gobierna Jenrax.
3. **Prepara la base antes de que se instale Jenrax** (fase 0, en
   `migrations/19.0.2.0.0/pre-migrate.py`): crea ya pobladas las columnas que
   Jenrax rellenaría con valores por defecto o recalcularía sobre el
   histórico, deja el envío de e-CF en `manual` y guarda una línea base de
   conteos (`psi_mig_conteo`).

Por eso **no depende de Jenrax**: así Odoo lo carga en la fase 1 del grafo,
antes de instalar Jenrax. El mapeo de datos a los modelos de Jenrax lo hace
`dgii_reports` 19.0.2.0.0 (repo `xmarts/declaraciones_dgii`, misma rama), que
sí depende de Jenrax.

`l10n_do_dgii_tax_payer_type` va como `Selection` con los valores de v13:
hay campos de Studio *related* de tipo selection que apuntan a él.

## Cómo se ejecuta

Con la instancia parada, y los repos de Jenrax en el `addons_path`:

```bash
odoo -c <conf> -u l10n_do_accounting,dgii_reports -i l10n_do_jenrax --stop-after-init
```

Sirve igual desde el dump de Odoo Upgrade (módulos en `13.0.x`) que desde los
dummies ya instalados (`19.0.1.0.0`). Hay que **nombrar los dos módulos en el
`-u`**: `dgii_reports` trae dependencias nuevas y, si no se nombra, Odoo lo
descarta del grafo.

## Los módulos de esta rama

| Módulo | Estado |
|---|---|
| `l10n_do_accounting` | Puente, 19.0.2.0.0 |
| `l10n_do_debit_note` | Dummy sin campos (19.0.1.0.0), no choca con Jenrax |
| `l10n_do_purchase` | Dummy sin campos (19.0.1.0.0), no choca con Jenrax |
| `l10n_do_pos` | **Retirado**: no estaba instalado en v13 y tiene el mismo nombre que el `l10n_do_pos` de Jenrax |

## Documentación

Diseño, mapeo campo a campo, riesgos y resultado de la prueba:
`SEGUIMIENTO/migracion/PUENTE_LOCALIZACION_JENRAX.md` del proyecto PSI.
