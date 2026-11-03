# Power BI Desktop report construction

**Status:** Supporting files supplied; a native `.pbix` file is **not** included. Power BI Desktop is required to author one. The working offline HTML dashboard in `deliverables` is a separate application, not Power BI.

1. Open Power BI Desktop on Windows and import the five CSVs under `data/` using **Get data > Text/CSV**. In Power Query, set ID columns to whole number, monetary columns to decimal/currency, and order/receipt dates to Date. `PowerQuery_Import_Template.m` demonstrates a typed import for the orders table.
2. In Model view, connect `suppliers[supplier_id]` to `purchase_orders[supplier_id]` and `materials[material_id]` to `purchase_orders[material_id]`, both one-to-many, single-direction. `inventory_snapshots` can relate to `materials` by material_id.
3. To analyze orders versus budget by category and month, create a bridge dimension: distinct union of `purchase_orders[month] & "|" & purchase_orders[category]` and `budgets[month] & "|" & budgets[category]`; create the same key in both facts; link bridge 1:* to each fact with single-direction filters. Avoid direct fact-to-fact joins. If reporting across different date granularities, add a conventional calendar dimension.
4. Create measures from `Measures.dax`. These are measure definitions, not an importable `.pbix` document. Create the disconnected price shock table and scenario measures separately.
5. Create report pages: **Executive Finance** (spend, budget, variance, monthly trend), **Suppliers** (late %, spend, invoice exceptions), **Procurement** (price variance by material category), **Inventory** (stock below reorder point, inventory value), and **Scenario** (price-shock slicer and impact).
6. Validate totals against `deliverables/validated_metrics.json` with all filters cleared. A report screenshot or video can be included in the portfolio, but do not claim an ECC connection.

**Scope note:** The budget models **purchase spend**, not a complete pharmaceutical company profit-and-loss statement. Inventory records are synthetic stock snapshots, not calculated from a full perpetual-inventory ledger. Do not infer inventory turnover without cost-of-goods-sold data.

## Cost and platform limits

Power BI Desktop is a free Windows report authoring application; see [Microsoft download documentation](https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-get-the-desktop) and [supported Windows platforms](https://www.microsoft.com/en-us/download/details.aspx?id=58494). It is not a native macOS application. The HTML dashboard needs neither Windows nor Power BI. Cloud collaboration has separate licensing/capacity requirements; consult [Microsoft sharing requirements](https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-share-dashboards) before assuming free distribution. These links were checked on 2026-11-03.

## Modeling safeguards

Use the bridge's month/category columns as slicers so both facts receive filters. A supplier or material filter can affect orders without affecting category budgets: hide budget comparisons on supplier/material pages, or explicitly define a justified allocation. The provided basic Budget measure alone does not guard against misleading filter contexts. Create measures one at a time; `Measures.dax` is reference text, not a bulk import script. Test 2025, 2026, each category, cleared filters, and zero-denominator behavior. Invoice mismatches are modeled amount comparisons, not a real SAP three-way match.
