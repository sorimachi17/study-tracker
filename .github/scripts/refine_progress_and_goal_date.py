from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '/* fold-total-goal-line-date-align-v6 */'
if marker in s:
    raise SystemExit('patch already applied')

old_total = '''<div class="card progress-card"><div class="total-row total-metrics"><div class="total-metric overall-total"><span class="total-metric-label">全期間の累計学習時間</span><div class="total-hours"><span id="totalHours">0h</span> <small id="totalMinutes">0m</small></div><em>すべての学習記録</em></div><div class="total-metric target-period-total">'''
new_total = '''<div class="card progress-card"><div class="total-row total-metrics"><details class="total-metric overall-total overall-total-details" open><summary><span>全期間の累計学習時間</span><span class="overall-total-chevron" aria-hidden="true">⌄</span></summary><div class="overall-total-body"><div class="total-hours"><span id="totalHours">0h</span> <small id="totalMinutes">0m</small></div><em>すべての学習記録</em></div></details><div class="total-metric target-period-total">'''
if old_total not in s:
    raise SystemExit('overall total block not found')
s = s.replace(old_total, new_total, 1)

css = r'''
/* fold-total-goal-line-date-align-v6 */
.overall-total-details{padding:0!important;overflow:hidden}
.overall-total-details>summary{list-style:none;display:flex;align-items:center;justify-content:space-between;gap:10px;padding:15px 16px;cursor:pointer;color:var(--muted);font-size:11px;font-weight:900;user-select:none}
.overall-total-details>summary::-webkit-details-marker{display:none}
.overall-total-details .overall-total-body{padding:0 16px 16px}
.overall-total-details .overall-total-body>em{display:block;margin-top:8px;color:var(--muted);font-size:10px;font-style:normal;font-weight:750}
.overall-total-chevron{font-size:18px;line-height:1;transition:transform .18s ease}
.overall-total-details:not([open]) .overall-total-chevron{transform:rotate(-90deg)}
.chart-goal{stroke:var(--text)!important;stroke-width:3!important;stroke-dasharray:10 6!important;opacity:.92!important}
.chart-goal-label{fill:var(--text)!important;font-weight:950!important}
.goal-settings-field>input[type="date"]{-webkit-appearance:none;appearance:none;display:flex!important;align-items:center!important;height:46px!important;min-height:46px!important;line-height:normal!important;padding-top:0!important;padding-bottom:0!important}
.goal-settings-field>input[type="date"]::-webkit-date-and-time-value{display:flex!important;align-items:center!important;height:100%!important;min-height:0!important;margin:0!important;padding:0!important;line-height:normal!important;text-align:left!important}
@media(max-width:620px){
  .overall-total-details>summary{padding:14px}
  .overall-total-details .overall-total-body{padding:0 14px 14px}
}
'''
if '</style>' not in s:
    raise SystemExit('style tag not found')
s = s.replace('</style>', css + '\n</style>', 1)

p.write_text(s, encoding='utf-8')
