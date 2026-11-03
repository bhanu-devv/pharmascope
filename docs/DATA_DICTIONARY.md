# Data dictionary

All data is generated locally with seed `20261103`. Dollars are illustrative; no real currency/FX master is modeled. CSV dates are ISO strings; SQLite stores dates as text. Identifiers/flags/counts are integers; financial fields are decimal-like floating values rounded to cents.

## suppliers

50 rows. Unique grain: **supplier_id**.

| Field | Definition | Example |
|---|---|---|
| `supplier_id` | Supplier dimension key | 1 |
| `supplier_name` | Fictional supplier display name | Supplier 01 — North America |
| `region` | Assigned supplier region | North America |
| `target_lead_days` | Supplier promise offset in days | 10 |
| `quality_rating` | Random synthetic score 80–100; not measured defect rate | 89 |

## materials

500 rows. Unique grain: **material_id**.

| Field | Definition | Example |
|---|---|---|
| `material_id` | Material dimension key | 1 |
| `material_name` | Fictional material display name | Material 001 |
| `category` | Material grouping: API, Excipient, Packaging, Lab Supplies, Consumables | API |
| `standard_unit_price` | Material reference price, dollars per unit | 42.79 |
| `reorder_point` | Illustrative unit threshold | 1441 |

## purchase_orders

20,000 rows. Unique grain: **po_id**.

| Field | Definition | Example |
|---|---|---|
| `po_id` | Unique modeled purchase order/line identifier | 1 |
| `order_date` | Order date (ISO date) | 2026-11-06 |
| `supplier_id` | Supplier dimension key | 26 |
| `material_id` | Material dimension key | 456 |
| `quantity` | Positive ordered units; no unit conversions | 218 |
| `category` | Material grouping: API, Excipient, Packaging, Lab Supplies, Consumables | API |
| `unit_price` | Actual price per unit, illustrative dollars | 52.16 |
| `actual_spend` | quantity × unit_price, dollars | 11370.88 |
| `standard_spend` | quantity × material standard_unit_price, dollars | 11198.66 |
| `price_variance` | actual_spend − standard_spend, dollars | 172.22 |
| `promised_date` | order_date + supplier target_lead_days | 2026-11-19 |
| `delivery_delay_days` | Signed days vs promise; negative is early | 4 |
| `received_date` | promised_date + delivery_delay_days | 2026-11-23 |
| `late_flag` | 1 if received after promise, else 0 | 1 |
| `year` | Calendar year of order (budget year for budgets) | 2026 |
| `month` | YYYY-MM order/budget/snapshot period | 2026-11 |
| `invoice_amount` | Synthetic invoiced amount, dollars | 11370.88 |
| `invoice_variance` | invoice_amount − actual_spend, dollars | 0.0 |
| `invoice_exception` | 1 if absolute invoice variance > $0.01 | 0 |

## budgets

120 rows. Unique grain: **month + category**.

| Field | Definition | Example |
|---|---|---|
| `year` | Calendar year of order (budget year for budgets) | 2025 |
| `month` | YYYY-MM order/budget/snapshot period | 2025-01 |
| `category` | Material grouping: API, Excipient, Packaging, Lab Supplies, Consumables | API |
| `budget_amount` | Monthly category budget, dollars | 4231705.16 |

## inventory_snapshots

12,000 rows. Unique grain: **month + material_id**.

| Field | Definition | Example |
|---|---|---|
| `month` | YYYY-MM order/budget/snapshot period | 2025-01 |
| `material_id` | Material dimension key | 1 |
| `ending_units` | Random monthly end quantity; not derived from a stock movement ledger | 748 |
| `standard_unit_price` | Material reference price, dollars per unit | 42.79 |
| `reorder_point` | Illustrative unit threshold | 1441 |
| `category` | Material grouping: API, Excipient, Packaging, Lab Supplies, Consumables | API |
| `inventory_value` | ending_units × standard_unit_price, dollars | 32006.92 |
| `below_reorder` | 1 when ending_units < reorder_point, otherwise 0 | 1 |

## Derived assets

`dashboard_data.json` contains monthly/category spend, standard, PPV, order/late/exception counts and budgets; year/category summaries; year/supplier summaries; monthly inventory value and below-reorder count; and metadata. `validated_metrics.json` records headline totals. The SQLite supplier view aggregates order counts, spend, late percentage, PPV and invoice exception counts. No missing values are intentionally generated.
