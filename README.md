# l10n-dominicana — rama `19.0-dummy-pre13`

Versiones **neutralizadas, de solo lectura**, de los módulos de la localización
dominicana, para bases migradas de Odoo 13 a Odoo 19.

Fork de `indexa-git/l10n-dominicana`. Parte de `13.0` (commit `0431370`,
versión `13.0.1.13.2`).

**Correspondencia 1 a 1 con la rama `13.0`**: mismos nombres de módulo, mismos
`depends`, mismos campos. Lo único que se quita es la lógica Python y las
vistas.

## Para qué sirve

Odoo Upgrade convierte la base pero no porta los módulos de terceros. Eso deja
los datos huérfanos: las columnas siguen en la base pero Odoo 19 no las conoce,
así que la información no se puede consultar, filtrar ni exportar.

Peor aún: los módulos quedan en estado `to upgrade`. Odoo los da por instalados
y espera su código; sin él, la base arrastra estados inconsistentes.

Estos módulos declaran los campos para que el ORM los reconozca. Nada más.

## Los módulos

| Módulo | Campos | Qué preserva |
|---|---:|---|
| `l10n_do_accounting` | **30** | ~308.500 valores fiscales, y los **22 tipos de documento** (NCF) |
| `l10n_do_pos` | **24** | Campos de POS y el modelo `pos.order.payment.credit.note` |
| `l10n_do_debit_note` | 0 | Solo su grupo de seguridad: no declara campos propios |
| `l10n_do_purchase` | 0 | Nada: no declara campos ni datos |

Se conservan los cuatro aunque dos no tengan campos, para que la
correspondencia con `13.0` sea exacta y los `depends` resuelvan solos.

### Campos con más volumen (medidos en la base de PSI)

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

Se declaran **todos los campos del código v13**, tengan dato o no: el módulo es
fiel al original y sirve en cualquier cliente, no solo donde se midió.

## Qué se quita, y qué NO

**Se quita:**

- Toda la lógica: `compute`, `default`, `related`, `onchange`, `constrains`,
  `create`/`write`/`unlink`. Verificable:

  ```bash
  grep -rcE "@api\.|compute=|default=|related=|def (create|write|unlink)" */models/*.py
  # 0
  ```

- Todas las vistas (`views/`): son interfaz, no dato.
- Los **wizards**: son `TransientModel`, no guardan histórico. Verificado: sus
  tablas tienen 0 filas.
- Los `One2many`: su inverso pertenece al otro lado de la relación.

**Se conserva:**

- `data/` y `security/`: **crean registros con XML-ID propio**. Quitarlos hace
  que Odoo los borre por huérfanos al actualizar.
- Los `depends` originales, sin tocar.
- Los nombres de campo, su tipo y su `string`.

> ⚠️ **La lección más cara de esta rama.** En una primera versión se quitó
> `data/l10n_latam.document.type.csv` por considerarlo "datos, no estructura".
> Al actualizar, Odoo borró los **22 tipos de documento** —eran suyos por
> XML-ID— y con ellos **36.289 referencias en `account.move` y 176.204 en
> `account.move.line`** quedaron a NULL. Un dummy que borra lo que pretende
> preservar es peor que no tenerlo.

## Adaptaciones obligadas a Odoo 19

- Los `Selection` se declaran como `Char`: si la base tuviera un valor fuera de
  la lista v13, un `Selection` lo ocultaría en la interfaz.
- `l10n_do_itbis_amount` usaba `currency_field="always_set_currency_id"`, campo
  que **no existe en Odoo 19**. Se apunta a `currency_id`.
- `pos.order.payment.credit.note.currency_id` era un `related`; al quitar la
  lógica se queda sin `comodel_name`, pero el `Monetary` del mismo modelo lo
  necesita. Se declara como `Many2one` a `res.currency`.

## Instalación

**Con la instancia parada.** Un `-i`/`-u` contra una base en uso son dos
procesos escribiendo el registry a la vez.

Si los módulos vienen del upgrade en estado `to upgrade`, la operación es `-u`
y no `-i`: Odoo los reconoce y solo les pone el código encima.

```bash
sudo systemctl stop odona-<dominio>.service
odoo -c <conf> -u l10n_do_accounting,l10n_do_debit_note,l10n_do_purchase --stop-after-init
sudo systemctl start odona-<dominio>.service
```

> `l10n_do_pos` **arrastra `point_of_sale`** por su `depends`. No lo instales en
> una base que no usa POS.

## Validado

Sobre clones del dump original de Odoo Upgrade (PSI, ticket 4558031), 2026-08-24:

- Los tres módulos en `to upgrade` pasan a `installed`, exit 0.
- **Ningún conteo cambió**: comparación campo por campo antes/después, idéntica.
- Los 22 tipos de documento intactos, con su XML-ID de `l10n_do_accounting`.
- Lecturas reales por ORM: `BILL/2026/1892` → income `01`, expense `02`,
  `is_ecf_invoice` True, tipo "Crédito Fiscal Electrónica"; línea 652439 →
  ITBIS 754,02 DOP; diario "Banco Popular / 7902" → `bank`.
- `search_count`: 110.089 en `l10n_do_income_type`, 176.204 en
  `account.move.line.l10n_latam_document_type_id`.
- `l10n_do_pos` instala limpio por separado (exit 0).

## Retirada

Es **temporal**, para el periodo de migración. Se desinstala cuando el paquete
definitivo de la localización declare estos mismos campos.

Al llevar los **nombres originales**, el reemplazo es directo: se sustituye el
código del dummy por el funcional y se actualiza el módulo.

> `l10n_do_pos` crea el modelo `pos.order.payment.credit.note`, con **tabla
> propia**. Si algún día tiene filas, desinstalarlo se las llevaría: haría falta
> un `uninstall_hook`. Hoy está a 0 y no lo lleva.

## Ramas de este repositorio

| Rama | Contenido |
|---|---|
| `13.0` | Los módulos funcionales originales |
| `19.0-dummy-pre13` | **Esta**: versiones neutralizadas para bases ex-v13 |
