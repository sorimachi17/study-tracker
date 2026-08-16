from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# 1) Remove 「ごろ」 from target prediction.
s=s.replace("formatShortDate(dateKey(target))+'ごろ'", "formatShortDate(dateKey(target))")

# 2) Replace dropdown-based recent stats with compact history lists.
pattern=r'<div class="progress-kpis"><div class="section-head"><h3>最近の学習時間</h3><span>期間を選んで確認</span></div><div class="period-card-grid">.*?</div></div></div></section>'
replacement='''<div class="progress-kpis"><div class="section-head"><h3>最近の学習時間</h3><span>直近の推移を一覧</span></div><div class="period-card-grid"><div class="period-card day"><div class="period-list-head"><span>今日の合計</span><small>直近7日</small></div><div class="period-history" id="dayHistoryList"></div></div><div class="period-card week"><div class="period-list-head"><span>週の合計</span><small>直近8週</small></div><div class="period-history" id="weekHistoryList"></div></div><div class="period-card month"><div class="period-list-head"><span>月の合計</span><small>直近12か月</small></div><div class="period-history" id="monthHistoryList"></div></div></div></div></div></section>'''
s2,n=re.subn(pattern,replacement,s,count=1,flags=re.S)
if n!=1:
    raise SystemExit(f'recent stats html replace failed: {n}')
s=s2

# 3) Add list-oriented CSS and neutralize old mobile picker-specific rules.
css_anchor='.period-meta b{color:var(--text);font-size:13px;font-weight:900}'
list_css='''.period-list-head{display:flex;align-items:center;justify-content:space-between;gap:10px}.period-list-head>span{font-size:13px;font-weight:900}.period-list-head>small{color:var(--muted);font-size:10px;font-weight:800}.period-history{display:grid;margin-top:10px}.period-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:3px 10px;align-items:center;padding:10px 0;border-top:1px solid var(--line)}.period-row:first-child{border-top:0}.period-row.current{margin:0 -6px;padding:10px 8px;border-radius:10px;background:var(--surface)}.period-row-label{font-size:12px;font-weight:850;min-width:0}.period-row-total{font-size:16px;font-weight:900;white-space:nowrap}.period-row-meta{grid-column:1/-1;color:var(--muted);font-size:10px;font-weight:750}.period-card.day .period-row-meta{display:none}'''
if css_anchor not in s:
    raise SystemExit('css anchor not found')
s=s.replace(css_anchor,css_anchor+list_css,1)

# Remove old special day-card minimum height and picker layout on mobile; keep generic card layout.
s=s.replace('.period-card.day{min-height:176px;padding-bottom:20px}','')
s=s.replace('.period-card-head{display:grid;grid-template-columns:1fr;gap:8px;align-items:start}.period-card-head>span{font-size:13px}.period-picker{display:block;width:100%;max-width:none;min-height:46px;height:46px;font-size:14px;line-height:1.2}.period-card strong{display:block;margin-top:14px;font-size:26px;line-height:1.25;flex:0 0 auto}.period-card.day strong{margin-top:18px;font-size:30px;line-height:1.25}.period-card small{display:block;margin-top:8px;line-height:1.4;flex:0 0 auto}.period-card.day small{padding-bottom:2px}','.period-list-head>span{font-size:13px}.period-list-head>small{font-size:11px}.period-row{padding:11px 0}.period-row.current{margin:0 -4px;padding:11px 8px}.period-row-total{font-size:17px}.period-row-meta{font-size:11px}')

# 4) Replace renderRecentStats with list rendering.
func_pattern=r"function renderRecentStats\(\)\{.*?\}\nfunction renderAll\(\)\{"
new_func=r'''function recentDayLabel(d,index){if(index===0)return'今日';const w=['日','月','火','水','木','金','土'][d.getDay()];return(d.getMonth()+1)+'/'+d.getDate()+'（'+w+'）'}
function renderRecentStats(){const dayList=$('dayHistoryList'),weekList=$('weekHistoryList'),monthList=$('monthHistoryList');if(!dayList||!weekList||!monthList)return;const today=parseDate(todayKey());
const dayRows=[];for(let i=0;i<7;i++){const d=new Date(today);d.setDate(d.getDate()-i);const k=dateKey(d),total=sumEntries(e=>e.date===k);dayRows.push('<div class="period-row'+(i===0?' current':'')+'"><span class="period-row-label">'+recentDayLabel(d,i)+'</span><strong class="period-row-total">'+studyTimeLabel(total)+'</strong></div>')}dayList.innerHTML=dayRows.join('');
const currentWeek=weekStart(today),weekRows=[];for(let i=0;i<8;i++){const start=new Date(currentWeek);start.setDate(start.getDate()-7*i);const end=new Date(start);end.setDate(end.getDate()+6);const stats=recentPeriodStats(start,end),label=i===0?'今週':(start.getMonth()+1)+'/'+start.getDate()+'〜'+(end.getMonth()+1)+'/'+end.getDate();weekRows.push('<div class="period-row'+(i===0?' current':'')+'"><span class="period-row-label">'+label+'</span><strong class="period-row-total">'+studyTimeLabel(stats.total)+'</strong><small class="period-row-meta">'+stats.studyDays+'日学習 ・ 1日平均 '+studyTimeLabel(stats.avg)+'</small></div>')}weekList.innerHTML=weekRows.join('');
const monthRows=[];for(let i=0;i<12;i++){const start=new Date(today.getFullYear(),today.getMonth()-i,1),end=new Date(start.getFullYear(),start.getMonth()+1,0),stats=recentPeriodStats(start,end),label=i===0?'今月':start.getFullYear()+'年'+(start.getMonth()+1)+'月';monthRows.push('<div class="period-row'+(i===0?' current':'')+'"><span class="period-row-label">'+label+'</span><strong class="period-row-total">'+studyTimeLabel(stats.total)+'</strong><small class="period-row-meta">'+stats.studyDays+'日学習 ・ 1日平均 '+studyTimeLabel(stats.avg)+'</small></div>')}monthList.innerHTML=monthRows.join('')}
function renderAll(){'''
s2,n=re.subn(func_pattern,new_func,s,count=1,flags=re.S)
if n!=1:
    raise SystemExit(f'renderRecentStats replace failed: {n}')
s=s2

# Remove obsolete change listener for removed pickers.
s=s.replace("document.addEventListener('change',e=>{if(e.target&&['dayStatsDate','weekStatsSelect','monthStatsSelect'].includes(e.target.id))renderRecentStats()});",'')

p.write_text(s,encoding='utf-8')
