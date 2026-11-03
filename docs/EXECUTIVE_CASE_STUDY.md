# Executive case study — PharmaScope

## Decision context

A fictional manufacturer needs to review purchasing price pressure, delivery reliability and invoice differences. This is an educational dataset, with no actual company or supplier impact.

## Verified synthetic results

| Metric | Full 2025–2026 scenario |
|---|---:|
| Orders | 20,000 |
| Purchase spend | $533,669,433.23 |
| Budget | $531,285,884.15 |
| Above budget | $2,383,549.08 |
| Purchase price variance | +$17,481,695.68 |
| On-time delivery | 65.38% |
| Invoice exceptions | 1,685 |
| 5% uniform price-shock increment | $26,683,471.66 |

These values reconcile to `deliverables/validated_metrics.json`. Budgets are derived from simulated spend; price-shock values are sensitivities, not forecasts. Delivery patterns are randomly generated, so no causal explanation can be inferred.

## Recommendations for the demonstration

1. Review high-spend suppliers alongside delivery rates, material criticality and contract terms; lateness alone does not establish supplier risk.
2. Investigate positive PPV at material level before making a negotiation recommendation; standards may be stale, and mix/volume matter.
3. Route the modeled invoice exceptions for targeted investigation. Exception counts are not proven fraud, losses or recoverable savings.

## Limits

No verified savings, regulated pharmaceutical workflow, SAP ECC connection, consumption/COGS ledger, independent budget or forecast. Real decisions require validated operational data and finance/procurement review.
