"""Excel financial workbook built with artifact_tool."""
from pathlib import Path
import csv
from artifact_tool import Workbook,SpreadsheetFile
P=Path(__file__).resolve().parents[1]
def load(name):
 with (P/'data'/name).open(newline='') as f:return list(csv.DictReader(f))
w=Workbook.create();dash=w.worksheets.add('Executive Summary');monthly=w.worksheets.add('Budget vs Actual');scenario=w.worksheets.add('Price Scenarios');score=w.worksheets.add('Supplier Scorecard');guide=w.worksheets.add('Read Me')
navy='#133353';teal='#087E74';light='#E7F4F0';gray='#E8EFF5'
def header(s,r):
 s.get_range(r).format={'fill':navy,'font':{'bold':True,'color':'#FFFFFF'},'row_height':28}
def title(s,text):
 s.get_range('A1:H1').merge();s.get_range('A1').values=[[text]];s.get_range('A1:H1').format={'fill':navy,'font':{'bold':True,'color':'#FFFFFF','size':16},'row_height':38}
for s,t in [(dash,'PHARMASCOPE | FINANCIAL OVERVIEW'),(monthly,'BUDGET VS ACTUAL | MONTHLY MODEL'),(scenario,'COST INFLATION | SCENARIO MODEL'),(score,'SUPPLIER PERFORMANCE SCORECARD'),(guide,'PROJECT GUIDE | SYNTHETIC CASE STUDY')]:title(s,t)
orders=load('purchase_orders.csv'); budgets=load('budgets.csv'); suppliers=load('suppliers.csv')
# monthly sheet, source monthly aggregates keyed to budget; visible metrics use Excel formulas.
by={}
for r in orders:
 k=(r['month'],r['category']);d=by.setdefault(k,dict(spend=0,standard=0,orders=0,late=0,exceptions=0));d['spend']+=float(r['actual_spend']);d['standard']+=float(r['standard_spend']);d['orders']+=1;d['late']+=int(r['late_flag']);d['exceptions']+=int(r['invoice_exception'])
bs={(r['month'],r['category']):float(r['budget_amount']) for r in budgets}
monthly.get_range('A3:J3').values=[['Month','Category','Actual Spend','Budget','Variance $','Variance %','Std. Spend','Price Variance','PO Count','Late POs']];header(monthly,'A3:J3')
rows=[]
for (m,c),v in sorted(by.items()):rows.append([m,c,round(v['spend'],2),round(bs[(m,c)],2),None,None,round(v['standard'],2),None,v['orders'],v['late']])
n=len(rows);monthly.get_range_by_indexes(3,0,n,10).values=rows
monthly.get_range('E4').formulas=[['=C4-D4']];monthly.get_range(f'E4:E{n+3}').fill_down();monthly.get_range('F4').formulas=[['=IFERROR(E4/D4,0)']];monthly.get_range(f'F4:F{n+3}').fill_down();monthly.get_range('H4').formulas=[['=C4-G4']];monthly.get_range(f'H4:H{n+3}').fill_down()
monthly.get_range(f'C4:E{n+3}').set_number_format('$#,##0.00');monthly.get_range(f'F4:F{n+3}').set_number_format('0.0%');monthly.get_range(f'G4:H{n+3}').set_number_format('$#,##0.00')
monthly.freeze_panes.freeze_rows(3)
for col,width in [('A',16),('B',19),('C',18),('D',18),('E',17),('F',16),('G',18),('H',19),('I',14),('J',14)]:monthly.get_range(f'{col}:{col}').format.column_width=width
# executive model dashboard directly calculated off source rows
labels=[['Total Actual Spend',f"=SUM('Budget vs Actual'!C4:C{n+3})"],['Total Budget',f"=SUM('Budget vs Actual'!D4:D{n+3})"],['Budget Variance', '=B4-B5'],['Budget Variance %','=IFERROR(B6/B5,0)'],['Total Purchase Orders',f"=SUM('Budget vs Actual'!I4:I{n+3})"],['On-time Delivery Rate',f"=IFERROR(1-SUM('Budget vs Actual'!J4:J{n+3})/B8,0)"],['Purchase Price Variance',f"=SUM('Budget vs Actual'!H4:H{n+3})"]]
dash.get_range('A3:B3').values=[['Performance metric','Value']];header(dash,'A3:B3')
for i,(k,f) in enumerate(labels,4):dash.get_range(f'A{i}').values=[[k]];dash.get_range(f'B{i}').formulas=[[f]]
dash.get_range('A12:H12').merge();dash.get_range('A12').values=[['Positive variance indicates actual spending above the budget or standard price.']]
dash.get_range('A14:H14').merge();dash.get_range('A14').values=[['All data is fictional. This workbook uses actual Excel formulas, not fixed KPI text.']]
dash.get_range('B4:B6').set_number_format('$#,##0.00');dash.get_range('B7').set_number_format('0.0%');dash.get_range('B9').set_number_format('0.0%');dash.get_range('B10').set_number_format('$#,##0.00')
dash.get_range('A:A').format.column_width=31;dash.get_range('B:B').format.column_width=23
scenario.get_range('A3:D3').values=[['Price Shock','Baseline Spend','Incremental Cost','Scenario Spend']];header(scenario,'A3:D3');scenario.get_range('A4:A8').values=[[x] for x in [0,.05,.10,.15,.20]]
for i in range(4,9):
 scenario.get_range(f'B{i}').formulas=[["='Executive Summary'!B4"]];scenario.get_range(f'C{i}').formulas=[[f'=A{i}*B{i}']];scenario.get_range(f'D{i}').formulas=[[f'=B{i}+C{i}']]
scenario.get_range('A4:A8').set_number_format('0%');scenario.get_range('B4:D8').set_number_format('$#,##0.00')
scenario.get_range('A:A').format.column_width=18
for c in ['B','C','D']:scenario.get_range(f'{c}:{c}').format.column_width=23
scenario.get_range('A11:F11').merge();scenario.get_range('A11').values=[['Assumption: order quantities and purchasing mix remain unchanged; prices increase uniformly.']]
score.get_range('A3:F3').values=[['Supplier','Region','PO Count','Actual Spend','Late Deliveries','Late Rate']];header(score,'A3:F3')
agg={i:{'count':0,'spend':0,'late':0} for i in range(1,51)}
for r in orders:
 a=agg[int(r['supplier_id'])];a['count']+=1;a['spend']+=float(r['actual_spend']);a['late']+=int(r['late_flag'])
for i,r in enumerate(suppliers,4):
 a=agg[int(r['supplier_id'])];score.get_range(f'A{i}:E{i}').values=[[r['supplier_name'],r['region'],a['count'],round(a['spend'],2),a['late']]];score.get_range(f'F{i}').formulas=[[f'=IFERROR(E{i}/C{i},0)']]
score.get_range('D4:D53').set_number_format('$#,##0.00');score.get_range('F4:F53').set_number_format('0.0%')
for c,wd in [('A',36),('B',22),('C',15),('D',21),('E',20),('F',17)]:score.get_range(f'{c}:{c}').format.column_width=wd
notes=[('DATA','20,000 synthetic purchase orders; 50 synthetic suppliers; 500 materials.'),('EXCEL','Formulas drive budget variance, price variance, on-time delivery, and scenarios.'),('POWER BI','Use the included CSVs, DAX measures and Power Query templates in the powerbi folder.'),('SAP','Transactions are fictional SAP-style business concepts; there is NO SAP ECC integration.'),('METRICS','Delivery rate = on-time purchase orders / total purchase orders.'),('IMPORTANT','Professional experience and software proficiency cannot be claimed solely from this portfolio case study.'),('LICENSE','Generated synthetic data; no external proprietary datasets.')]
for i,(a,b) in enumerate(notes,3):guide.get_range(f'A{i}').values=[[a]];guide.get_range(f'B{i}').values=[[b]]
guide.get_range('A:A').format.column_width=18;guide.get_range('B:B').format.column_width=110
out=P/'deliverables/PharmaScope_Financial_Model.xlsx';SpreadsheetFile.export_xlsx(w).save(str(out));print('saved',out,out.stat().st_size)
