"""Embed aggregated data into the offline HTML dashboard; no dependencies."""
from pathlib import Path
import json
P = Path(__file__).resolve().parents[1]
template = (P / 'src/dashboard_template.html').read_text(encoding='utf-8')
data = json.loads((P / 'deliverables/dashboard_data.json').read_text())
assert template.count('__DATA__') == 1
(P / 'deliverables/PharmaScope_Dashboard.html').write_text(
    template.replace('__DATA__', json.dumps(data, separators=(',', ':'))), encoding='utf-8')
print('Built offline dashboard')
