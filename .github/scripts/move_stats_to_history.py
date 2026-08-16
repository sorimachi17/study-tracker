from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Remove the whole recent study-time block from section 1.
pat=r'<div class="progress-kpis"><div class="section-head"><h3>最近の学習時間</h3>.*?</div></div></div></section>'
m=re.search(pat,s,flags=re.S)
if not m:
    raise SystemExit('recent study block not found')
block=m.group(0)
# Preserve the closing progress card + section tags.
replacement='</div></section>'
s=s[:m.start()]+replacement+s[m.end():]

# Remove renderRecentStats call from dashboard because the UI no longer exists.
s=s.replace(";renderRecentStats()}","}",1)

# Upgrade month summary styling.
old_css='.calendar-total{margin-top:4px;color:var(--blue);font-size:12px;font-weight:850}'
new_css='.calendar-total{margin-top:9px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px;width:min(430px,100%)}.calendar-stat{padding:8px 10px;border:1px solid var(--line);border-radius:9px;background:var(--surface2);text-align:left;line-height:1.25}.calendar-stat span{display:block;color:var(--muted);font-size:9px;font-weight:850}.calendar-stat strong{display:block;margin-top:3px;color:var(--text);font-size:13px;font-weight:900}.mini-month-stats{display:grid;gap:3px;margin:5px 0 7px;padding:6px;border-radius:7px;background:var(--surface)}.mini-month-stat{display:flex;align-items:center;justify-content:space-between;gap:5px;color:var(--muted);font-size:8px;font-weight:800}.mini-month-stat b{color:var(--text);font-size:9px;font-weight:900;white-space:nowrap}'
if old_css not in s:
    raise SystemExit('calendar total css not found')
s=s.replace(old_css,new_css,1)

# Slightly improve mobile summary readability.
mobile_marker='@media(max-width:620px){.app-shell{padding:18px 14px 40px}'
if mobile_marker not in s:
    raise SystemExit('mobile marker not found')
s=s.replace(mobile_marker,mobile_marker+'.calendar-heading{width:100%;max-width:430px}.calendar-total{width:100%;gap:5px}.calendar-stat{padding:7px 8px}.calendar-stat strong{font-size:12px}',1)

# Replace calendar rendering functions with month/year summaries.
start=s.find('function renderCalendar(){')
end=s.find('function renderRecent(){',start)
if start<0 or end<0:
    raise SystemExit('calendar functions not found')
new_funcs=r'''function monthSummaryStats(y,m){const start=new Date(y,m,1),end=new Date(y,m+1,0);return recentPeriodStats(start,end)}
function calendarStatsHtml(stats){return '<div class="calendar-stat"><span>月合計</span><strong>'+studyTimeLabel(stats.total)+'</strong></div><div class="calendar-stat"><span>勉強日数</span><strong>'+stats.studyDays+'日</strong></div><div class="calendar-stat"><span>1日平均</span><strong>'+studyTimeLabel(stats.avg)+'</strong></div>'}
function renderCalendar(){if(calendarView==='year')return renderYear();if(calendarView==='months')return renderMonths();const y=currentMonth.getFullYear(),m=currentMonth.getMonth();$('calendarTitle').textContent=fmt.format(currentMonth);const monthStats=monthSummaryStats(y,m);$('calendarMonthTotal').innerHTML=calendarStatsHtml(monthStats);const first=new Date(y,m,1),last=new Date(y,m+1,0),offset=(first.getDay()+6)%7,totals=[];for(let d=1;d<=last.getDate();d++){const k=y+'-'+pad(m+1)+'-'+pad(d);totals.push(sumEntries(e=>e.date===k))}const max=Math.max(...totals,1),cells=[];for(let i=0;i<offset;i++)cells.push('<button class="day blank"></button>');for(let d=1;d<=last.getDate();d++){const k=y+'-'+pad(m+1)+'-'+pad(d),total=totals[d-1],cl=['day','lvl'+level(total,max)];if(k===selectedDate)cl.push('selected');if(k===todayKey())cl.push('today');cells.push('<button class="'+cl.join(' ')+'" type="button" data-date="'+k+'"><span class="num">'+d+'</span><span class="mins">'+(total?minutesLabel(total):'')+'</span></button>')}$('calendarGrid').innerHTML=cells.join('')}
function renderYear(){const y=currentMonth.getFullYear();$('calendarTitle').textContent=y+'年の日別';$('calendarMonthTotal').textContent='';$('yearView').className='year-grid';const totals={};entries.forEach(e=>{if(e.date.startsWith(String(y)+'-'))totals[e.date]=(totals[e.date]||0)+Number(e.minutes||0)});const max=Math.max(1,...Object.values(totals));$('yearView').innerHTML=Array.from({length:12},(_,m)=>{const last=new Date(y,m+1,0).getDate(),offset=(new Date(y,m,1).getDay()+6)%7,stats=monthSummaryStats(y,m);let dots='';for(let i=0;i<offset;i++)dots+='<span></span>';for(let d=1;d<=last;d++){const k=y+'-'+pad(m+1)+'-'+pad(d),lv=level(totals[k]||0,max);dots+='<button class="mini-dot lvl'+lv+'" type="button" data-date="'+k+'"></button>'}return'<div class="mini-month"><div class="mini-month-head"><h4>'+(m+1)+'月</h4></div><div class="mini-month-stats"><div class="mini-month-stat"><span>合計</span><b>'+studyTimeLabel(stats.total)+'</b></div><div class="mini-month-stat"><span>勉強日数</span><b>'+stats.studyDays+'日</b></div><div class="mini-month-stat"><span>1日平均</span><b>'+studyTimeLabel(stats.avg)+'</b></div></div><div class="mini-days">'+dots+'</div></div>'}).join('')}
function renderMonths(){const y=currentMonth.getFullYear();$('calendarTitle').textContent=y+'年の月合計';$('calendarMonthTotal').textContent='';$('yearView').className='year-grid month-grid';const totals=Array.from({length:12},(_,m)=>sumEntries(e=>e.date.startsWith(y+'-'+pad(m+1)+'-'))),max=Math.max(1,...totals);$('yearView').innerHTML=totals.map((t,m)=>'<button class="month-sum lvl'+level(t,max)+'" type="button" data-month="'+m+'"><span>'+(m+1)+'月</span><strong>'+minutesLabel(t)+'</strong><small>クリックで日別へ</small></button>').join('')}
'''
s=s[:start]+new_funcs+s[end:]

p.write_text(s,encoding='utf-8')
