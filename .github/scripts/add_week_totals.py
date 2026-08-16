from pathlib import Path

p = Path('index.html')
s = p.read_text()

# 1) richer month/week summary card styles
old_css = ".month-sum{border:1px solid var(--line);border-radius:10px;background:var(--surface2);padding:10px;display:grid;gap:3px}.month-sum strong{font-size:20px;line-height:1.1}.month-sum span,.month-sum small{color:var(--muted);font-size:11px;font-weight:800}"
new_css = ".month-sum{border:1px solid var(--line);border-radius:10px;background:var(--surface2);padding:11px;display:grid;gap:7px;text-align:left}.month-sum-title{color:var(--text)!important;font-size:13px!important;font-weight:900!important}.month-sum-stats{display:grid;gap:5px}.month-sum-stat{display:flex;align-items:center;justify-content:space-between;gap:8px;padding-top:5px;border-top:1px solid var(--line)}.month-sum-stat span{color:var(--muted);font-size:9px;font-weight:850}.month-sum-stat strong{color:var(--text);font-size:12px;line-height:1.15;font-weight:900;white-space:nowrap}.week-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.week-sum{border:1px solid var(--line);border-radius:11px;background:var(--surface2);padding:12px;display:grid;gap:8px}.week-sum-title{font-size:13px;font-weight:900}.week-sum-stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}.week-sum-stat{padding:8px;border:1px solid var(--line);border-radius:8px;background:var(--surface);min-width:0}.week-sum-stat span{display:block;color:var(--muted);font-size:8px;font-weight:850}.week-sum-stat strong{display:block;margin-top:3px;color:var(--text);font-size:11px;line-height:1.2;font-weight:900;word-break:keep-all}"
if old_css not in s:
    raise SystemExit('month-sum CSS target not found')
s = s.replace(old_css, new_css, 1)

# mobile week cards one column
old_mobile = ".kpi-grid,.year-grid,.month-grid{grid-template-columns:repeat(2,minmax(0,1fr))}"
new_mobile = ".kpi-grid,.year-grid,.month-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.week-grid{grid-template-columns:1fr}"
if old_mobile not in s:
    raise SystemExit('mobile grid target not found')
s = s.replace(old_mobile, new_mobile, 1)

# 2) add weekly totals tab
old_tabs = '<button class="btn" id="monthTotalViewBtn" type="button">月合計</button></div>'
new_tabs = '<button class="btn" id="monthTotalViewBtn" type="button">月合計</button><button class="btn" id="weekTotalViewBtn" type="button">週合計</button></div>'
if old_tabs not in s:
    raise SystemExit('tabs target not found')
s = s.replace(old_tabs, new_tabs, 1)

# 3) renderCalendar should route to weekly totals
old_route = "function renderCalendar(){if(calendarView==='year')return renderYear();if(calendarView==='months')return renderMonths();"
new_route = "function renderCalendar(){if(calendarView==='year')return renderYear();if(calendarView==='months')return renderMonths();if(calendarView==='weeks')return renderWeeks();"
if old_route not in s:
    raise SystemExit('renderCalendar route target not found')
s = s.replace(old_route, new_route, 1)

# 4) replace month totals rendering and add week totals rendering
old_months = "function renderMonths(){const y=currentMonth.getFullYear();$('calendarTitle').textContent=y+'年の月合計';$('calendarMonthTotal').textContent='';$('yearView').className='year-grid month-grid';const totals=Array.from({length:12},(_,m)=>sumEntries(e=>e.date.startsWith(y+'-'+pad(m+1)+'-'))),max=Math.max(1,...totals);$('yearView').innerHTML=totals.map((t,m)=>'<button class=\"month-sum lvl'+level(t,max)+'\" type=\"button\" data-month=\"'+m+'\"><span>'+(m+1)+'月</span><strong>'+minutesLabel(t)+'</strong><small>クリックで日別へ</small></button>').join('')}"
new_months = "function renderMonths(){const y=currentMonth.getFullYear();$('calendarTitle').textContent=y+'年の月合計';$('calendarMonthTotal').textContent='';$('yearView').className='year-grid month-grid';const statsList=Array.from({length:12},(_,m)=>monthSummaryStats(y,m)),max=Math.max(1,...statsList.map(x=>x.total));$('yearView').innerHTML=statsList.map((stats,m)=>'<button class=\"month-sum lvl'+level(stats.total,max)+'\" type=\"button\" data-month=\"'+m+'\"><span class=\"month-sum-title\">'+(m+1)+'月</span><div class=\"month-sum-stats\"><div class=\"month-sum-stat\"><span>合計時間</span><strong>'+studyTimeLabel(stats.total)+'</strong></div><div class=\"month-sum-stat\"><span>勉強日数</span><strong>'+stats.studyDays+'日</strong></div><div class=\"month-sum-stat\"><span>1日平均</span><strong>'+studyTimeLabel(stats.avg)+'</strong></div></div></button>').join('')}function monthWeekRanges(y,m){const first=new Date(y,m,1),last=new Date(y,m+1,0),ranges=[];let start=new Date(first);while(start<=last){let end=new Date(start),day=(start.getDay()+6)%7;end.setDate(end.getDate()+(6-day));if(end>last)end=new Date(last);ranges.push({start:new Date(start),end:new Date(end)});start=new Date(end);start.setDate(start.getDate()+1)}return ranges}function renderWeeks(){const y=currentMonth.getFullYear(),m=currentMonth.getMonth(),ranges=monthWeekRanges(y,m),statsList=ranges.map(r=>({range:r,stats:recentPeriodStats(r.start,r.end)})),max=Math.max(1,...statsList.map(x=>x.stats.total));$('calendarTitle').textContent=y+'年'+(m+1)+'月の週合計';$('calendarMonthTotal').innerHTML=calendarStatsHtml(monthSummaryStats(y,m));$('yearView').className='week-grid';$('yearView').innerHTML=statsList.map((item,i)=>{const r=item.range,stats=item.stats,label=(r.start.getMonth()+1)+'/'+r.start.getDate()+'〜'+(r.end.getMonth()+1)+'/'+r.end.getDate();return'<div class=\"week-sum lvl'+level(stats.total,max)+'\"><div class=\"week-sum-title\">第'+(i+1)+'週　'+label+'</div><div class=\"week-sum-stats\"><div class=\"week-sum-stat\"><span>合計時間</span><strong>'+studyTimeLabel(stats.total)+'</strong></div><div class=\"week-sum-stat\"><span>勉強日数</span><strong>'+stats.studyDays+'日</strong></div><div class=\"week-sum-stat\"><span>1日平均</span><strong>'+studyTimeLabel(stats.avg)+'</strong></div></div></div>'}).join('')}"
if old_months not in s:
    raise SystemExit('renderMonths target not found')
s = s.replace(old_months, new_months, 1)

# 5) clicking a month in 月合計 opens that month's 週合計
old_month_click = "if(b.dataset.month!==undefined){currentMonth.setMonth(Number(b.dataset.month));calendarView='month';setCalendarView();return}"
new_month_click = "if(b.dataset.month!==undefined){currentMonth.setMonth(Number(b.dataset.month));currentMonth.setDate(1);calendarView='weeks';setCalendarView();return}"
if old_month_click not in s:
    raise SystemExit('month click target not found')
s = s.replace(old_month_click, new_month_click, 1)

# 6) support weekly tab state and button
old_set_view = "function setCalendarView(){const m=calendarView==='month',y=calendarView==='year',ms=calendarView==='months';$('monthView').classList.toggle('hidden',!m);$('yearView').classList.toggle('hidden',m);$('monthViewBtn').classList.toggle('active',m);$('yearViewBtn').classList.toggle('active',y);$('monthTotalViewBtn').classList.toggle('active',ms);renderCalendar()}$('monthViewBtn').addEventListener('click',()=>{calendarView='month';setCalendarView()});$('yearViewBtn').addEventListener('click',()=>{calendarView='year';setCalendarView()});$('monthTotalViewBtn').addEventListener('click',()=>{calendarView='months';setCalendarView()});"
new_set_view = "function setCalendarView(){const m=calendarView==='month',y=calendarView==='year',ms=calendarView==='months',w=calendarView==='weeks';$('monthView').classList.toggle('hidden',!m);$('yearView').classList.toggle('hidden',m);$('monthViewBtn').classList.toggle('active',m);$('yearViewBtn').classList.toggle('active',y);$('monthTotalViewBtn').classList.toggle('active',ms);$('weekTotalViewBtn').classList.toggle('active',w);renderCalendar()}$('monthViewBtn').addEventListener('click',()=>{calendarView='month';setCalendarView()});$('yearViewBtn').addEventListener('click',()=>{calendarView='year';setCalendarView()});$('monthTotalViewBtn').addEventListener('click',()=>{calendarView='months';setCalendarView()});$('weekTotalViewBtn').addEventListener('click',()=>{calendarView='weeks';setCalendarView()});"
if old_set_view not in s:
    raise SystemExit('setCalendarView target not found')
s = s.replace(old_set_view, new_set_view, 1)

p.write_text(s)
print('patched index.html')
