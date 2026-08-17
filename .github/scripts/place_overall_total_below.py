from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '/* overall-total-below-v7 */'
if marker in s:
    raise SystemExit('patch already applied')

old = '''<div class="card progress-card"><div class="total-row total-metrics"><details class="total-metric overall-total overall-total-details" open><summary><span>全期間の累計学習時間</span><span class="overall-total-chevron" aria-hidden="true">⌄</span></summary><div class="overall-total-body"><div class="total-hours"><span id="totalHours">0h</span> <small id="totalMinutes">0m</small></div><em>すべての学習記録</em></div></details><div class="total-metric target-period-total"><div class="target-period-content"><div><span class="total-metric-label">目標開始日からの累計学習時間</span><div class="target-period-hours"><span id="targetPeriodHours">0h</span> <small id="targetPeriodMinutes">0m</small></div></div><div class="goal-orbit" id="goalOrbit"><div><strong id="goalOrbitPercent">0%</strong><span>進捗</span></div></div></div><em id="targetPeriodRange">開始日から現在まで</em></div></div>'''
new = '''<div class="card progress-card"><div class="total-row total-metrics"><div class="total-metric target-period-total"><div class="target-period-content"><div><span class="total-metric-label">目標開始日からの累計学習時間</span><div class="target-period-hours"><span id="targetPeriodHours">0h</span> <small id="targetPeriodMinutes">0m</small></div></div><div class="goal-orbit" id="goalOrbit"><div><strong id="goalOrbitPercent">0%</strong><span>進捗</span></div></div></div><em id="targetPeriodRange">開始日から現在まで</em></div><details class="total-metric overall-total overall-total-details" id="overallTotalDetails"><summary><span>全期間の累計学習時間</span><span class="overall-total-chevron" aria-hidden="true">⌄</span></summary><div class="overall-total-body"><div class="total-hours"><span id="totalHours">0h</span> <small id="totalMinutes">0m</small></div><em>すべての学習記録</em></div></details></div>'''
if old not in s:
    raise SystemExit('progress totals block not found')
s = s.replace(old, new, 1)

old_storage = "targetStart:'study-tracker.targetStartDate.v1',legacyMigrated:'study-tracker.legacyMigrated.v7'"
new_storage = "targetStart:'study-tracker.targetStartDate.v1',overallTotalOpen:'study-tracker.overallTotalOpen.v1',legacyMigrated:'study-tracker.legacyMigrated.v7'"
if old_storage not in s:
    raise SystemExit('storage block not found')
s = s.replace(old_storage, new_storage, 1)

needle = "currentMonth.setDate(1);const $=id=>document.getElementById(id),fmt=new Intl.DateTimeFormat('ja-JP',{year:'numeric',month:'long'}),DAY_MS=86400000;"
insert = "currentMonth.setDate(1);const $=id=>document.getElementById(id),fmt=new Intl.DateTimeFormat('ja-JP',{year:'numeric',month:'long'}),DAY_MS=86400000;const overallTotalDetails=$('overallTotalDetails');if(overallTotalDetails){overallTotalDetails.open=localStorage.getItem(STORAGE.overallTotalOpen)==='true';overallTotalDetails.addEventListener('toggle',()=>localStorage.setItem(STORAGE.overallTotalOpen,String(overallTotalDetails.open)))}"
if needle not in s:
    raise SystemExit('runtime init point not found')
s = s.replace(needle, insert, 1)

css = r'''
/* overall-total-below-v7 */
.total-metrics{grid-template-columns:minmax(0,1fr)!important;gap:10px!important}
.target-period-total{order:1}
.overall-total-details{order:2;width:100%}
'''
if '</style>' not in s:
    raise SystemExit('style closing tag not found')
s = s.replace('</style>', css + '\n</style>', 1)

p.write_text(s, encoding='utf-8')
