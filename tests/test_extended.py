"""Cross-artifact reconciliation using only the standard library."""
from pathlib import Path
from decimal import Decimal as D
from datetime import date
import csv,json,sqlite3,re
P=Path(__file__).resolve().parents[1]
def load(name):
    with (P/'data'/f'{name}.csv').open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
tables={n:load(n) for n in ['suppliers','materials','purchase_orders','budgets','inventory_snapshots']}
s={r['supplier_id']:r for r in tables['suppliers']}
mat={r['material_id']:r for r in tables['materials']}
for table,keys in [('suppliers',['supplier_id']),('materials',['material_id']),('purchase_orders',['po_id']),('budgets',['month','category']),('inventory_snapshots',['month','material_id'])]:
    rows=tables[table]
    assert len({tuple(r[k] for k in keys) for r in rows})==len(rows),table
    assert all(all(v!='' for v in r.values()) for r in rows),table
for r in tables['purchase_orders']:
    assert r['supplier_id'] in s and r['material_id'] in mat
    assert D(r['standard_spend'])==D(r['quantity'])*D(mat[r['material_id']]['standard_unit_price'])
    assert D(r['invoice_variance'])==D(r['invoice_amount'])-D(r['actual_spend'])
    assert int(r['invoice_exception'])==int(abs(D(r['invoice_variance']))>D('.01'))
    assert (date.fromisoformat(r['received_date'])-date.fromisoformat(r['promised_date'])).days==int(r['delivery_delay_days'])
    assert r['order_date'][:7]==r['month'] and r['order_date'][:4]==r['year']
for r in tables['inventory_snapshots']:
    assert r['material_id'] in mat
    assert D(r['inventory_value'])==D(r['ending_units'])*D(r['standard_unit_price'])
    assert int(r['below_reorder'])==int(int(r['ending_units'])<int(r['reorder_point']))
assert len(tables['inventory_snapshots'])==12000
j=json.loads((P/'deliverables/dashboard_data.json').read_text())
m=json.loads((P/'deliverables/validated_metrics.json').read_text())
def close(a,b):assert abs(float(a)-float(b))<.02,(a,b)
for grain in ['monthly','category','supplier']:
    close(sum(r['spend'] for r in j[grain]),m['spend'])
    close(sum(r['price_variance'] for r in j[grain]),m['price_variance'])
    assert sum(r['orders'] for r in j[grain])==m['orders']
    close(100*(1-sum(r['late'] for r in j[grain])/m['orders']),m['on_time_pct'])
close(sum(r['budget_amount'] for r in j['monthly']),m['budget'])
assert sum(r['exceptions'] for r in j['monthly'])==m['invoice_exceptions']
html=(P/'deliverables/PharmaScope_Dashboard.html').read_text()
assert json.loads(re.search(r'const DATA=(.*?);const \$=',html).group(1))==j
assert not re.search(r'<(?:script|link)[^>]+(?:src|href)=["\']https?://',html)
with sqlite3.connect(P/'data/pharma_procurement.sqlite') as con:
    assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    for name,rows in tables.items():assert con.execute(f'SELECT COUNT(*) FROM {name}').fetchone()[0]==len(rows)
    close(con.execute('SELECT SUM(total_spend) FROM v_supplier_scorecard').fetchone()[0],m['spend'])
    con.executescript((P/'sql/analysis_queries.sql').read_text())
print('PASS: keys, relationships, invoices, dates, inventory, JSON/HTML/SQLite and SQL')
