from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

start_marker = '<section class="section-block"><div class="section-intro"><div class="section-intro-left"><span class="section-number">2</span><h2>記録する</h2>'
end_marker = '<section class="section-block"><div class="section-intro"><div class="section-intro-left"><span class="section-number">3</span><h2>履歴を見る</h2>'

if start_marker not in s or end_marker not in s:
    raise SystemExit('record/history section markers not found')

start = s.index(start_marker)
end = s.index(end_marker, start)

replacement = '''<button class="record-fab" id="openRecordModalBtn" type="button" aria-label="学習時間を記録"><span class="record-fab-plus">＋</span><span>記録</span></button>
<div class="record-sheet-backdrop hidden" id="recordModal" role="dialog" aria-modal="true" aria-labelledby="recordModalTitle">
  <div class="record-sheet card">
    <div class="record-sheet-handle" aria-hidden="true"></div>
    <div class="section-head record-sheet-head"><h2 id="recordModalTitle">学習時間を記録</h2><button class="record-sheet-close" id="closeRecordModalBtn" type="button" aria-label="閉じる">×</button></div>
    <form class="entry-form" id="entryForm">
      <div class="form-grid"><div><label for="dateInput">日付</label><input id="dateInput" type="date" required /></div><div><label for="categoryInput">カテゴリ</label><select id="categoryInput" required></select></div></div>
      <div class="time-grid"><div><label for="startTimeInput">開始時刻</label><input id="startTimeInput" type="time" /></div><div><label for="endTimeInput">終了時刻</label><input id="endTimeInput" type="time" /></div><div><label for="minutesInput">学習時間（分）</label><input id="minutesInput" type="number" min="1" step="1" placeholder="45" required /></div></div>
      <div class="quick-buttons"><button class="btn" type="button" data-min="15">15分</button><button class="btn" type="button" data-min="25">25分</button><button class="btn" type="button" data-min="45">45分</button><button class="btn" type="button" data-min="60">60分</button><button class="btn" type="button" data-min="90">90分</button></div>
      <div><label for="noteInput">何を勉強したか・メモ</label><textarea id="noteInput" placeholder="例: オンライン英会話、シャドーイング、IELTS Reading"></textarea></div>
      <div class="save-row"><button class="btn primary" type="submit">この内容で記録</button></div>
    </form>
    <div class="record-day-summary"><div class="section-head"><h3>選択日の記録</h3><span id="dayTotal"></span></div><div class="list" id="dayList"></div></div>
    <span id="selectedDateLabel" class="hidden"></span>
  </div>
</div>
'''

s = s[:start] + replacement + s[end:]
s = s.replace('<span class="section-number">3</span><h2>履歴を見る</h2>', '<span class="section-number">2</span><h2>履歴を見る</h2>', 1)

css_marker = '/* floating-record-sheet-v1 */'
if css_marker not in s:
    css = r'''
/* floating-record-sheet-v1 */
.record-fab{position:fixed;right:18px;bottom:calc(22px + env(safe-area-inset-bottom));z-index:16;min-height:54px;padding:0 18px;border:0;border-radius:999px;background:var(--blue);color:#fff;box-shadow:0 14px 34px rgba(37,99,235,.34);display:flex;align-items:center;gap:7px;font-weight:900;font-size:15px}.record-fab-plus{font-size:25px;line-height:1;font-weight:700}.record-fab:active{transform:translateY(1px)}.record-sheet-backdrop{position:fixed;inset:0;z-index:40;background:rgba(6,12,24,.58);display:flex;align-items:center;justify-content:center;padding:20px}.record-sheet{width:min(620px,100%);max-height:min(88vh,820px);overflow:auto;padding:20px;border-radius:22px}.record-sheet-handle{display:none}.record-sheet-head{margin-bottom:16px}.record-sheet-head h2{font-size:19px}.record-sheet-close{width:38px;height:38px;border:1px solid var(--line);border-radius:999px;background:var(--surface2);color:var(--text);font-size:24px;line-height:1;display:grid;place-items:center}.record-day-summary{margin-top:18px;padding-top:16px;border-top:1px solid var(--line)}body.modal-open{overflow:hidden}
@media(max-width:620px){.record-fab{right:16px;bottom:calc(18px + env(safe-area-inset-bottom));min-height:52px;padding:0 17px}.record-sheet-backdrop{align-items:flex-end;padding:0}.record-sheet{width:100%;max-height:88dvh;border-radius:22px 22px 0 0;padding:10px 16px calc(18px + env(safe-area-inset-bottom));box-shadow:0 -18px 50px rgba(0,0,0,.28)}.record-sheet-handle{display:block;width:42px;height:5px;border-radius:999px;background:var(--line);margin:0 auto 10px}.record-sheet-head{position:sticky;top:-10px;z-index:2;background:var(--surface);padding:8px 0 10px;margin-bottom:10px}.record-sheet .form-grid,.record-sheet .time-grid{grid-template-columns:1fr}.record-sheet .save-row{position:sticky;bottom:0;background:linear-gradient(to bottom,transparent,var(--surface) 28%);padding-top:18px}.record-sheet .save-row .btn{min-height:50px}}
'''
    s = s.replace('</style>', css + '</style>', 1)

js_marker = '/* floating-record-sheet-js-v1 */'
if js_marker not in s:
    js = r'''/* floating-record-sheet-js-v1 */
function openRecordModal(){renderSelectedDay();setDefaultEntryEndTime();$('recordModal').classList.remove('hidden');document.body.classList.add('modal-open')}
function closeRecordModal(){$('recordModal').classList.add('hidden');document.body.classList.remove('modal-open')}
$('openRecordModalBtn').addEventListener('click',openRecordModal);
$('closeRecordModalBtn').addEventListener('click',closeRecordModal);
$('recordModal').addEventListener('click',e=>{if(e.target.id==='recordModal')closeRecordModal()});
$('dateInput').addEventListener('change',()=>{selectedDate=$('dateInput').value||todayKey();renderSelectedDay();renderCalendar()});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!$('recordModal').classList.contains('hidden'))closeRecordModal()});
'''
    anchor = "$('saveTargetBtn').addEventListener('click'"
    if anchor not in s:
        raise SystemExit('JS insertion anchor not found')
    s = s.replace(anchor, js + anchor, 1)

old = "renderAll();showToast('記録しました')"
new = "renderAll();closeRecordModal();showToast('記録しました')"
if old in s:
    s = s.replace(old, new, 1)
elif new not in s:
    raise SystemExit('entry submit completion marker not found')

p.write_text(s, encoding='utf-8')
