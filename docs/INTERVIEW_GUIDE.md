# Interview walkthrough

## Two-minute explanation

“PharmaScope is a synthetic procurement finance portfolio case study. It models 20,000 orders across 50 fictional suppliers and 500 materials. A seeded Python pipeline exports CSVs, a SQLite database and aggregated metrics. An offline HTML dashboard lets a reviewer compare spend against budget, inspect delivery reliability and model price shocks. The delivered Excel workbook calculates variances and scenarios with formulas. I also prepared DAX and Power Query templates; there is no completed Power BI report or SAP connection.”

## Questions to prepare

- **How did you reconcile results?** Trace quantity × price at line level, then compare CSV totals with SQLite, JSON and dashboard aggregates. Check foreign keys, unique keys and date/exception flags.
- **Why aggregate for the browser?** Small, private, portable offline delivery; the tradeoff is less drill-down, including no supplier/category cross-filter.
- **What does positive variance mean?** Actual spend exceeds budget or standard. PPV compares prices at observed quantities; budget variance can also reflect volume/mix.
- **What action follows a late supplier flag?** Investigate critical materials, promise accuracy, quality and contractual context before escalation. The model does not prove a causal business problem.
- **What is missing for production?** Authenticated ingestion, validation contracts, exact monetary arithmetic, receipts/invoices at true grains, audit trails, access control, observability and domain review.
- **What is the forecasting limitation?** Scenarios hold quantities/mix constant and budgets are derived from simulated actuals. Neither is an independent forecast.
- **What did you build versus receive assistance on?** Explain the parts you reviewed, changed and can demonstrate. Disclose AI assistance honestly when relevant; do not claim independent authorship of work you cannot explain.

## Demonstration sequence

1. Open dashboard offline and select 2025.
2. Select API; explain why supplier detail is unavailable at that grain.
3. Return to All categories and increase the shock to 10%.
4. Trace a PPV formula in the workbook, then the corresponding SQL aggregate.
5. Show validation checks and explain one limitation before suggesting a future improvement.
