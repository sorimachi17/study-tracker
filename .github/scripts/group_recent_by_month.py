from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '/* recent-month-fold-v8 */'
if marker in s:
    raise SystemExit('recent month fold patch already applied')

old_storage = "targetStart:'study-tracker.targetStartDate.v1',overallTotalOpen:'study-tracker.overallTotalOpen.v1',legacyMigrated:"
new_storage = "targetStart:'study-tracker.targetStartDate.v1',overallTotalOpen:'study-tracker.overallTotalOpen.v1',recentMonthsOpen:'study-tracker.recentMonthsOpen.v1',legacyMigrated:"
if old_storage not in s:
    raise SystemExit('storage anchor not found')
s = s.replace(old_storage, new_storage, 1)

old_render = "function renderRecent(){const r=[...entries].sort((a,b)=>b.createdAt-a.createdAt).slice(0,8);$('recentCount').textContent=entries.length+'件';$('recentList').innerHTML=r.length?r.map(recordTemplate).join(''):'<div class=\"empty\">まだ記録がありません。</div>'}"
new_render = r'''function renderRecent(){const sorted=[...entries].sort((a,b)=>String(b.date||'').localeCompare(String(a.date||''))||Number(b.createdAt||0)-Number(a.createdAt||0));$('recentCount').textContent=entries.length+'件';if(!sorted.length){$('recentList').innerHTML='<div class="empty">まだ記録がありません。</div>';return}const groups={};sorted.forEach(e=>{const key=String(e.date||'').slice(0,7)||'日付未設定';(groups[key]||(groups[key]=[])).push(e)});const months=Object.keys(groups).sort().reverse(),saved=load(STORAGE.recentMonthsOpen,null),openMonths=Array.isArray(saved)?new Set(saved):new Set(months.length?[months[0]]:[]);$('recentList').innerHTML=months.map(key=>{const list=groups[key],total=list.reduce((sum,e)=>sum+Number(e.minutes||0),0),parts=key.split('-'),label=parts.length===2?Number(parts[0])+'年'+Number(parts[1])+'月':key,open=openMonths.has(key)?' open':'';return '<details class="recent-month-details" data-recent-month="'+escapeHtml(key)+'"'+open+'><summary><div><strong>'+escapeHtml(label)+'</strong><span>'+list.length+'件 ・ '+studyTimeLabel(total)+'</span></div><span class="recent-month-chevron" aria-hidden="true">⌄</span></summary><div class="recent-month-body">'+list.map(recordTemplate).join('')+'</div></details>'}).join('');$('recentList').querySelectorAll('.recent-month-details').forEach(d=>d.addEventListener('toggle',()=>{const openKeys=[...$('recentList').querySelectorAll('.recent-month-details[open]')].map(x=>x.dataset.recentMonth);save(STORAGE.recentMonthsOpen,openKeys)}))}'''
if old_render not in s:
    raise SystemExit('renderRecent anchor not found')
s = s.replace(old_render, new_render, 1)

css = r'''
/* recent-month-fold-v8 */
#recentList{display:grid;gap:10px}
.recent-month-details{border:1px solid var(--line);border-radius:12px;background:var(--surface2);overflow:hidden}
.recent-month-details>summary{list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 15px;cursor:pointer;user-select:none}
.recent-month-details>summary::-webkit-details-marker{display:none}
.recent-month-details>summary>div{display:flex;align-items:baseline;gap:9px;min-width:0}
.recent-month-details>summary strong{font-size:13px;font-weight:900;color:var(--text);white-space:nowrap}
.recent-month-details>summary span:not(.recent-month-chevron){font-size:10px;font-weight:800;color:var(--muted);white-space:nowrap}
.recent-month-chevron{font-size:18px;line-height:1;color:var(--muted);transition:transform .18s ease}
.recent-month-details:not([open]) .recent-month-chevron{transform:rotate(-90deg)}
.recent-month-body{padding:0 12px 8px;background:var(--surface)}
.recent-month-body .record-row:first-child{border-top:0}
@media(max-width:620px){
  .recent-month-details>summary{padding:13px 14px}
  .recent-month-body{padding:0 10px 7px}
}
'''
if '</style>' not in s:
    raise SystemExit('style closing tag not found')
s = s.replace('</style>', css + '\n</style>', 1)

p.write_text(s, encoding='utf-8')
