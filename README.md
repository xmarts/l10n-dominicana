# l10n-dominicana — rama `19.0-dummy-pre13`

Esta rama **no contiene los módulos funcionales** de la localización dominicana.
Contiene `l10n_do_accounting_legacy`: una versión **neutralizada, de solo
lectura**, para bases migradas de Odoo 13 a Odoo 19.

Fork de `indexa-git/l10n-dominicana`. Parte de `13.0` (commit `0431370`,
versión `13.0.1.13.2`).

## Para qué sirve

Odoo Upgrade convierte la base pero no porta los módulos de terceros.
`l10n_do_accounting` añadía columnas a **tablas nativas** (`account_move`,
`res_partner`, `account_journal`…): tras el upgrade esas columnas siguen en la
base con sus datos, pero Odoo 19 no las conoce y la información es inaccesible
desde la interfaz.

Este módulo solo las declara para que el ORM las reconozca. Sin lógica que
pueda alterar el dato histórico.

## Qué preserva

**26 campos en 7 modelos**, generados desde el esquema real de la base migrada,
no del código v13. Se declaran **todos los campos del módulo original, tengan
dato o no**: 13 con dato, 13 vacíos.

Medido sobre el dump de origen de PSI (ticket 4558031):

| Campo | Modelo | Registros |
|---|---|---:|
| `l10n_do_income_type` | `account.move` | **110.089** |
| `l10n_do_itbis_amount` | `account.move.line` | **72.689** |
| `is_ecf_invoice` | `account.move` | **46.481** |
| `is_debit_note` | `account.move` | **22.727** |
| `ncf_expiration_date` | `account.move` | **19.239** |
| `l10n_do_expense_type` | `account.move` | **18.422** |
| `l10n_do_dgii_tax_payer_type` | `res.partner` | **14.747** |
| `l10n_do_cancellation_type` | `account.move` | 1.493 |
| `l10n_do_expense_type` | `res.partner` | 1.247 |
| `l10n_do_origin_ncf` | `account.move` | 643 |
| `expiration_date` | `ir.sequence` | 346 |
| `l10n_do_payment_form` | `account.journal` | 76 |
| `l10n_do_ncf_type` | `l10n_latam.document.type` | 21 |
| e-CF y moneda | `res.company` | 6 |
| **Total** | | **~308.500** |

## Qué NO trae, a propósito

- **Cero lógica**: sin `compute`, `default`, `onchange` ni `constrains`.
  Verificable:

  ```bash
  grep -cE "@api\.(depends|onchange|constrains)|compute=|default=|def (create|write|unlink)" */models/*.py
  # 0
  ```

- Todos los campos `readonly=True`.
- Los `Selection` se declaran como `Char`: si la base tuviera un valor fuera de
  la lista v13, un `Selection` lo ocultaría en la interfaz.
- **Excluidos los campos `l10n_latam_*`**: pertenecen a
  `l10n_latam_invoice_document`, **nativo en Odoo 19**, que ya los declara.
  Redeclararlos impediría instalar el módulo.

## Los otros tres módulos del repo

Revisados uno por uno; ninguno justifica una versión dummy:

| Módulo | Campos propios | Motivo |
|---|---|---|
| `l10n_do_debit_note` | **ninguno** | Solo lógica y vistas |
| `l10n_do_purchase` | **ninguno** | Solo lógica y vistas |
| `l10n_do_pos` | 26 declarados | Sus tablas y columnas **no existen** en la base: PSI no usó POS |

## Caso B: cuándo tiene sentido instalarlo

Es un módulo de **campos heredados**, no de tablas propias:

- **No necesita `uninstall_hook`**: las columnas son de tablas nativas, así que
  desinstalarlo no las borra.
- **Pero solo sirve si la columna ya existe con datos.** Si no existe,
  instalarlo **la crea vacía** en lugar de exponer nada — y al desinstalarlo
  Odoo se la lleva.

Antes de darlo por útil en una base, medir:

```sql
SELECT count(*) FROM account_move WHERE l10n_do_income_type IS NOT NULL;
```

> **Esto no es teórico.** En el staging de PSI se desinstaló un predecesor de
> este módulo dando por hecho que sus campos estaban vacíos. No lo estaban: se
> perdieron ~308.500 valores. La lección: **contar siempre contra el dump de
> origen restaurado**, nunca contra la base en la que se va a operar.

## Instalación

**Con la instancia parada.** Un `-i`/`-u` contra una base en uso son dos
procesos escribiendo el registry a la vez.

```bash
sudo systemctl stop odona-<dominio>.service
odoo -c <conf> -i l10n_do_accounting_legacy --stop-after-init
sudo systemctl start odona-<dominio>.service
```

## Validado

Sobre un clon del dump original de Odoo Upgrade (2026-08-24):

- Instalación exit 0, sin errores.
- **Ningún conteo cambió** tras instalar: las 26 columnas conservan sus valores.
- Lecturas reales por ORM: `BILL/2026/1892` → income `01`, expense `02`,
  `is_ecf_invoice` True; partner `00112944400` → `taxpayer`; línea 652439 →
  ITBIS 754,02.
- `search_count` sobre `l10n_do_income_type` → 110.089.
- Ninguno de los 26 campos existe ya en el core de Odoo 19 ni en enterprise:
  cero conflictos.

## Retirada

Es **temporal**, para el periodo de migración. Se desinstala cuando el paquete
definitivo de la localización declare estos mismos campos.

## Ramas de este repositorio

| Rama | Contenido |
|---|---|
| `13.0` | Los módulos funcionales originales |
| `19.0-dummy-pre13` | **Esta**: versión neutralizada para bases ex-v13 |
