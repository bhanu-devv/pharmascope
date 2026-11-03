# Technical overview

PharmaScope combines procurement data modeling, financial reconciliation, an offline dashboard, and a formula-driven Excel workbook. The dataset contains 20,000 synthetic purchase orders, 50 suppliers, and 500 materials.

## Implementation

A seeded Python pipeline creates CSV tables, a SQLite database, and JSON summaries. The dashboard embeds aggregated data into standalone HTML and renders charts with native SVG. The Excel workbook contains monthly budget analysis, supplier scorecards, and price sensitivity formulas. DAX measures and a Power Query template support a separate Power BI implementation.

## Reconciliation

Line-level quantity and unit price determine actual spend. Standard prices determine the comparison baseline. Tests compare CSV totals with SQLite, JSON, and embedded dashboard data, and check unique keys, relationships, receipt dates, invoice flags, and inventory valuation.

## Design decisions

- Aggregated browser data keeps the dashboard portable and usable offline. Supplier/category cross-filtering is unavailable at the delivered summary grain.
- Positive purchase price variance means actual spend exceeds standard spend at observed quantities. Budget variance can also reflect volume and mix.
- Delivery reliability uses order counts rather than averages of monthly percentages.
- Price scenarios hold quantities and mix constant. Budgets are derived from simulated actuals; neither provides an independent forecast.

See [architecture](ARCHITECTURE.md), [financial calculations](FINANCIAL_CALCULATIONS.md), and [validation](VALIDATION.md) for implementation details and scope.
