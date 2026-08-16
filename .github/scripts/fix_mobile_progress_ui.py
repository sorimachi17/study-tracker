from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = '.milestone.prediction{grid-column:1/-1}'
new = '.milestone.prediction{grid-column:auto}'
if old not in s:
    raise SystemExit('prediction mobile span rule not found')
s = s.replace(old, new, 1)

old = '.period-card-grid{grid-template-columns:1fr}.period-card{padding:14px}.period-picker{max-width:64%}'
new = '.period-card-grid{grid-template-columns:1fr;gap:12px}.period-card{padding:16px;display:flex;flex-direction:column;min-height:0;height:auto;overflow:visible}.period-card-head{display:grid;grid-template-columns:1fr;gap:8px;align-items:start}.period-card-head>span{font-size:13px}.period-picker{width:100%;max-width:none;min-height:42px;font-size:14px}.period-card strong{margin-top:14px;font-size:26px}.period-card small{margin-top:6px}.period-meta{margin-top:12px;padding-top:12px}.period-meta span{font-size:11px}.period-meta b{font-size:14px}'
if old not in s:
    raise SystemExit('mobile recent stats css block not found')
s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
