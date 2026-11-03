# Validation report

Validated locally on 2026-11-03. This records completed checks, not planned work.

- Regenerated all synthetic datasets, SQLite tables, JSON metrics and standalone HTML using Python 3.12.14 with NumPy 2.3.5 and pandas 2.2.3.
- Original reconciliation test passed for 20,000 orders, 50 suppliers, 500 materials and 120 budget rows.
- Extended checks passed for unique keys, foreign keys, invoice flags, delivery dates, 12,000 inventory rows, database integrity, SQL execution, and CSV/JSON/SQLite/embedded-dashboard totals.
- Headless Chrome loaded the dashboard directly from disk, changed year and category, verified the supplier-grain notice and 10% scenario control, and reported zero JavaScript errors.
- Desktop (1440 px) and mobile (390 px) screenshots captured; mobile page has no horizontal overflow. Screenshots visually reviewed. [Desktop](screenshots/dashboard.png), [filtered scenario](screenshots/filtered-scenario.png), [mobile](screenshots/mobile.png).
- Original workbook preserved. ZIP/XML inspection found 432 formula cells and no cached Excel error cells. This is structural inspection, not a native Excel recalculation test.
- Credential-pattern scan of repository content and workbook XML found no matching tokens/private keys. This is a limited pattern scan, not proof that arbitrary sensitive data is absent.
- Largest source asset is the SQLite file at approximately 4.6 MB; no source file approaches GitHub's ordinary 100 MB limit. No LFS is required for current artifacts.

## Explicitly unverified

Native Excel recalculation, the optional specialized workbook rebuild, Power BI Desktop report assembly/DAX execution, live SAP ingestion, and operational pharmaceutical use were not tested. The GitHub Actions run is a separate post-publication check; see the repository Actions tab for its actual result.
