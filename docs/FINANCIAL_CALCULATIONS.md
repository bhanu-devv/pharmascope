# Financial calculations

| Metric | Definition | Interpretation |
|---|---|---|
| Actual spend | Σ(quantity × actual unit price) | Procurement commitment proxy, not cash paid or COGS |
| Standard spend | Σ(quantity × material standard price) | Reference purchasing baseline |
| Purchase price variance | Actual − standard spend | Positive is above standard; not volume variance |
| Budget variance | Actual − budget | Positive is overspend |
| Budget variance % | (actual − budget) / budget | Undefined if budget is zero; workbook uses IFERROR(...,0), DAX DIVIDE defaults to blank |
| On-time delivery | (orders − late orders) / orders | Receipt on promised date counts as on time; count weighted |
| Invoice exception | abs(invoice − actual spend) > 0.01 | Modeled mismatch flag; not a full three-way match |
| Inventory value | ending units × standard unit price | Monthly snapshot valuation, not fair value |
| Below reorder | ending units < reorder point | Indicator, not a validated shortage prediction |
| Scenario incremental cost | filtered spend × shock rate | Uniform price sensitivity, not forecast or realized savings |
| Scenario total spend | spend × (1 + shock rate) | Holds volume, mix and supplier allocation constant |

Example: 100 units at $12 vs a $10 standard gives actual $1,200, standard $1,000 and +$200 PPV. Against a $1,100 budget that is +$100 / 9.09%. A 5% shock adds $60 to actual spend.

Amounts are rounded to cents at line level before aggregation. Reconciliation uses a small tolerance to account for floating representation. Python uses binary floating point, appropriate for this demonstration; a production ledger should use decimal or integer cents with explicit rounding rules.

Budgets are monthly/category actuals multiplied by a seeded uniform 0.91–1.09 factor. Invoice multipliers are 1, 1.005, 1.015, or 0.99. Supplier quality scores and inventory balances are random illustrative inputs, not observed performance. There is no independent demand forecast, consumption model, COGS, FX, tax, payment terms, contract optimization, expiry or clinical validation.
