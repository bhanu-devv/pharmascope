from pathlib import Path
import csv, sqlite3, json, math, zipfile
P=Path(__file__).resolve().parents[1]
def rows(file):
 with (P/'data'/file).open() as f:return list(csv.DictReader(f))
o=rows('purchase_orders.csv');b=rows('budgets.csv');s=rows('suppliers.csv');m=rows('materials.csv')
assert len(o)==20000 and len(s)==50 and len(m)==500 and len(b)==120
assert len({r['po_id'] for r in o})==len(o)
assert all(abs(float(r['actual_spend'])-int(r['quantity'])*float(r['unit_price']))<.011 for r in o)
assert all(abs(float(r['price_variance'])-(float(r['actual_spend'])-float(r['standard_spend'])))<.011 for r in o)
assert all(int(r['late_flag'])==(r['received_date']>r['promised_date']) for r in o)
metrics=json.loads((P/'deliverables/validated_metrics.json').read_text())
assert abs(sum(float(r['actual_spend']) for r in o)-metrics['spend'])<.02
assert abs(sum(float(r['budget_amount']) for r in b)-metrics['budget'])<.02
with sqlite3.connect(P/'data/pharma_procurement.sqlite') as c:
 assert c.execute('SELECT COUNT(*) FROM purchase_orders').fetchone()[0]==20000
 assert math.isclose(c.execute('SELECT SUM(actual_spend) FROM purchase_orders').fetchone()[0],metrics['spend'],abs_tol=.02)
html=(P/'deliverables/PharmaScope_Dashboard.html').read_text(); assert '__DATA__' not in html and '20000' in html
with zipfile.ZipFile(P/'deliverables/PharmaScope_Financial_Model.xlsx') as z:
 assert 'xl/workbook.xml' in z.namelist()
 assert any((b'<f>' in z.read(k) or b'<x:f>' in z.read(k)) for k in z.namelist() if k.startswith('xl/worksheets/sheet') and k.endswith('.xml'))
print('PASS: 20,000-row data reconciliation, invoice/delivery flags, SQLite, offline HTML, Excel formulas')
