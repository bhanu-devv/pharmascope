-- SQLite compatible. Run against data/pharma_procurement.sqlite.
-- PURCHASE PRICE VARIANCE: actual purchase value minus standard purchase value.
SELECT category, ROUND(SUM(actual_spend),2) AS actual_spend,
       ROUND(SUM(price_variance),2) AS purchase_price_variance,
       COUNT(*) AS purchase_order_count
FROM purchase_orders GROUP BY category ORDER BY actual_spend DESC;

-- Budget-to-actual by month/category.
SELECT p.month,p.category,ROUND(SUM(p.actual_spend),2) AS actual_spend,
       b.budget_amount,ROUND(SUM(p.actual_spend)-b.budget_amount,2) AS budget_variance
FROM purchase_orders p JOIN budgets b ON b.month=p.month AND b.category=p.category
GROUP BY p.month,p.category,b.budget_amount ORDER BY p.month,p.category;

-- Supplier scorecard; highest late-delivery proportion among suppliers with >=100 orders.
SELECT supplier_name,order_count,total_spend,late_pct,price_variance,invoice_exceptions
FROM v_supplier_scorecard WHERE order_count>=100 ORDER BY late_pct DESC LIMIT 10;

-- Three-way-check analogue: recorded invoice totals versus PO line values (no actual SAP integration).
SELECT po_id,supplier_id,order_date,actual_spend,invoice_amount,invoice_variance
FROM purchase_orders WHERE invoice_exception=1 ORDER BY ABS(invoice_variance) DESC LIMIT 50;

-- Synthetic inventory reorder alerts (month-end snapshots).
SELECT i.month, m.category, COUNT(*) AS materials_below_reorder
FROM inventory_snapshots i JOIN materials m ON i.material_id=m.material_id
WHERE i.below_reorder=1 GROUP BY i.month,m.category ORDER BY i.month,m.category;
