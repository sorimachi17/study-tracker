from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = ".period-card{padding:16px;display:flex;flex-direction:column;min-height:0;height:auto;overflow:visible}.period-card-head{display:grid;grid-template-columns:1fr;gap:8px;align-items:start}.period-card-head>span{font-size:13px}.period-picker{width:100%;max-width:none;min-height:42px;font-size:14px}.period-card strong{margin-top:14px;font-size:26px}.period-card small{margin-top:6px}"
new = ".period-card{padding:16px;display:flex;flex-direction:column;min-height:0;height:auto;overflow:visible}.period-card.day{min-height:176px;padding-bottom:20px}.period-card-head{display:grid;grid-template-columns:1fr;gap:8px;align-items:start}.period-card-head>span{font-size:13px}.period-picker{display:block;width:100%;max-width:none;min-height:46px;height:46px;font-size:14px;line-height:1.2}.period-card strong{display:block;margin-top:14px;font-size:26px;line-height:1.25;flex:0 0 auto}.period-card.day strong{margin-top:18px;font-size:30px;line-height:1.25}.period-card small{display:block;margin-top:8px;line-height:1.4;flex:0 0 auto}.period-card.day small{padding-bottom:2px}"
if old not in s:
    raise SystemExit('target mobile period card styles not found')
s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
