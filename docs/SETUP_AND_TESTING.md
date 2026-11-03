# Setup and testing

## Open without installing

Extract the repository; double-click `deliverables/PharmaScope_Dashboard.html`. JavaScript must be enabled. The page requires no CDN and makes no network requests. Open the XLSX separately in a compatible spreadsheet application. The ZIP must be extracted before opening local assets.

## Rebuild

Follow the root README with Python 3.11/3.12 and pinned requirements. `build_project.py` replaces five CSVs, SQLite tables, dashboard data and metric JSON. Then run `build_dashboard.py`. Do not use Python's `-O` flag when running assertion-based tests. The original workbook builder uses a specialized runtime not installed by requirements; the supplied XLSX remains usable independently.

## Validation coverage

`test_integrity.py` reconciles primary counts, spend, budget, price calculations, delivery flags, SQLite spend, embedded HTML and workbook formula presence. `test_extended.py` checks foreign keys, natural keys, invoices, standard costs, inventory valuation, all SQLite/CSV row counts, dashboard summary totals, embedded JSON parity and SQL query execution. Tests use only the Python standard library. A failed assertion exits nonzero. GitHub Actions also rebuilds data/dashboard before testing.

Neither formula presence nor cached values prove full spreadsheet application recalculation. Native Excel and Power BI Desktop were not available for end-to-end application verification. Power BI assets require manual assembly. Browser interaction coverage is described in VALIDATION.md.

## Troubleshooting

- `ModuleNotFoundError: numpy`: activate the virtual environment and install requirements.
- Package version unavailable: check Python version; use 3.11/3.12 rather than system Python 3.9.
- Dashboard unchanged after generation: run `build_dashboard.py` and reload the browser.
- Supplier table hidden: choose All categories; the bundled summary has no supplier/category grain.
- `artifact_tool` import error: this affects only the original optional workbook builder; use the delivered workbook.
- Incorrect Power BI budget: check shared month/category dimensions and avoid direct fact-to-fact joins.
- Workbook differs from regenerated data: the workbook is a snapshot; data/dashboard build does not refresh it.
