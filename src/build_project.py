"""Deterministic, synthetic procurement case study. No real patient or enterprise data."""
from pathlib import Path
import sqlite3, json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; DEL=ROOT/'deliverables'
DATA.mkdir(exist_ok=True); DEL.mkdir(exist_ok=True)
rng=np.random.default_rng(20261103)
N=20000
supplier_ids=np.arange(1,51); material_ids=np.arange(1,501)
regions=['North America','Europe','Asia-Pacific','Latin America']
categories=['API','Excipient','Packaging','Lab Supplies','Consumables']
suppliers=pd.DataFrame({'supplier_id':supplier_ids,'supplier_name':[f'Supplier {i:02d} — {regions[(i-1)%4]}' for i in supplier_ids],'region':[regions[(i-1)%4] for i in supplier_ids],'target_lead_days':rng.integers(7,24,50),'quality_rating':rng.integers(80,101,50)})
materials=pd.DataFrame({'material_id':material_ids,'material_name':[f'Material {i:03d}' for i in material_ids],'category':[categories[(i-1)%5] for i in material_ids],'standard_unit_price':np.round(rng.uniform(8,160,500),2),'reorder_point':rng.integers(200,1500,500)})
order_dates=pd.to_datetime('2025-01-01')+pd.to_timedelta(rng.integers(0,730,N),unit='D')
orders=pd.DataFrame({'po_id':np.arange(1,N+1),'order_date':order_dates,'supplier_id':rng.choice(supplier_ids,N),'material_id':rng.choice(material_ids,N),'quantity':rng.integers(20,600,N)})
orders=orders.merge(materials[['material_id','standard_unit_price','category']],on='material_id').merge(suppliers[['supplier_id','target_lead_days']],on='supplier_id')
orders['unit_price']=np.round(orders.standard_unit_price *rng.normal(1.035,.11,N).clip(.72,1.55),2)
orders['actual_spend']=np.round(orders.quantity*orders.unit_price,2)
orders['standard_spend']=np.round(orders.quantity*orders.standard_unit_price,2)
orders['price_variance']=np.round(orders.actual_spend-orders.standard_spend,2)
orders['promised_date']=orders.order_date+pd.to_timedelta(orders.target_lead_days,unit='D')
orders['delivery_delay_days']=rng.choice([-3,-1,0,1,4,9,16],N,p=[.10,.12,.43,.15,.09,.07,.04])
orders['received_date']=orders.promised_date+pd.to_timedelta(orders.delivery_delay_days,unit='D')
orders['late_flag']=(orders.received_date>orders.promised_date).astype(int)
orders['year']=orders.order_date.dt.year; orders['month']=orders.order_date.dt.strftime('%Y-%m')
orders['invoice_amount']=np.round(orders.actual_spend*(1+rng.choice([0,.005,.015,-.01],N,p=[.91,.035,.03,.025])),2)
orders['invoice_variance']=np.round(orders.invoice_amount-orders.actual_spend,2)
orders['invoice_exception']=(orders.invoice_variance.abs()>.01).astype(int)
orders=orders.drop(columns=['standard_unit_price','target_lead_days'])
# Budget anchored to stable year/category, intentionally variable for meaningful variance.
actual=orders.groupby(['year','month','category'],as_index=False)['actual_spend'].sum()
budgets=actual.copy(); budgets['budget_amount']=np.round(budgets.actual_spend*rng.uniform(.91,1.09,len(budgets)),2)
budgets=budgets.drop(columns=['actual_spend'])
# Inventory snapshots are synthetic end-of-month quantities for valuation/coverage demonstrations.
months=sorted(orders.month.unique()); inventory=pd.DataFrame([(m,int(mid),int(rng.integers(150,2600))) for m in months for mid in material_ids],columns=['month','material_id','ending_units'])
inventory=inventory.merge(materials[['material_id','standard_unit_price','reorder_point','category']],on='material_id')
inventory['inventory_value']=np.round(inventory.ending_units*inventory.standard_unit_price,2)
inventory['below_reorder']=(inventory.ending_units<inventory.reorder_point).astype(int)
for name,df in [('suppliers',suppliers),('materials',materials),('purchase_orders',orders),('budgets',budgets),('inventory_snapshots',inventory)]:
 o=df.copy()
 for c in o.select_dtypes(include=['datetime64[ns]']).columns: o[c]=o[c].dt.strftime('%Y-%m-%d')
 o.to_csv(DATA/f'{name}.csv',index=False)
with sqlite3.connect(DATA/'pharma_procurement.sqlite') as conn:
 for name,df in [('suppliers',suppliers),('materials',materials),('purchase_orders',orders),('budgets',budgets),('inventory_snapshots',inventory)]:
  df.to_sql(name,conn,if_exists='replace',index=False)
 conn.execute('CREATE INDEX IF NOT EXISTS idx_order_date ON purchase_orders(order_date)')
 conn.execute('CREATE INDEX IF NOT EXISTS idx_order_supplier ON purchase_orders(supplier_id)')
 conn.execute('CREATE INDEX IF NOT EXISTS idx_order_material ON purchase_orders(material_id)')
 conn.execute('CREATE VIEW IF NOT EXISTS v_supplier_scorecard AS SELECT s.supplier_id, s.supplier_name, s.region, COUNT(*) AS order_count, ROUND(SUM(p.actual_spend),2) AS total_spend, ROUND(100.0*SUM(p.late_flag)/COUNT(*),1) AS late_pct, ROUND(SUM(p.price_variance),2) AS price_variance, SUM(p.invoice_exception) AS invoice_exceptions FROM purchase_orders p JOIN suppliers s ON s.supplier_id=p.supplier_id GROUP BY s.supplier_id,s.supplier_name,s.region')
monthly=orders.groupby(['month','year','category'],as_index=False).agg(spend=('actual_spend','sum'),standard=('standard_spend','sum'),price_variance=('price_variance','sum'),orders=('po_id','count'),late=('late_flag','sum'),exceptions=('invoice_exception','sum'))
monthly=monthly.merge(budgets[['month','category','budget_amount']],on=['month','category'])
category=orders.groupby(['year','category'],as_index=False).agg(spend=('actual_spend','sum'),orders=('po_id','count'),late=('late_flag','sum'),price_variance=('price_variance','sum'))
supplier=orders.groupby(['year','supplier_id'],as_index=False).agg(spend=('actual_spend','sum'),orders=('po_id','count'),late=('late_flag','sum'),price_variance=('price_variance','sum'))
supplier=supplier.merge(suppliers[['supplier_id','supplier_name','region']],on='supplier_id')
inv=inventory.groupby('month',as_index=False).agg(value=('inventory_value','sum'),below=('below_reorder','sum'))
payload={'monthly':json.loads(monthly.round(2).to_json(orient='records')),'category':json.loads(category.round(2).to_json(orient='records')),'supplier':json.loads(supplier.round(2).to_json(orient='records')),'inventory':json.loads(inv.round(2).to_json(orient='records')),'metadata':{'orders':len(orders),'suppliers':len(suppliers),'materials':len(materials),'seed':20261103,'fictional':True}}
(DEL/'dashboard_data.json').write_text(json.dumps(payload,separators=(',',':')))
summary={'orders':len(orders),'supplier_count':len(suppliers),'material_count':len(materials),'spend':round(float(orders.actual_spend.sum()),2),'budget':round(float(budgets.budget_amount.sum()),2),'on_time_pct':round(100*(1-float(orders.late_flag.mean())),2),'invoice_exceptions':int(orders.invoice_exception.sum()),'price_variance':round(float(orders.price_variance.sum()),2)}
(DEL/'validated_metrics.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
