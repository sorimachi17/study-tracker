from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) Make calendar summary plain text and position-friendly.
old_css = '.calendar-total{margin-top:9px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px;width:min(430px,100%)}.calendar-stat{padding:8px 10px;border:1px solid var(--line);border-radius:9px;background:var(--surface2);text-align:left;line-height:1.25}.calendar-stat span{display:block;color:var(--muted);font-size:9px;font-weight:850}.calendar-stat strong{display:block;margin-top:3px;color:var(--text);font-size:13px;font-weight:900}'
new_css = '.calendar-total{margin:0 0 10px;display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap;width:100%}.calendar-stat{display:flex;align-items:baseline;gap:5px;padding:0;border:0;background:none;line-height:1.25}.calendar-stat span{display:inline;color:var(--muted);font-size:10px;font-weight:850}.calendar-stat strong{display:inline;color:var(--text);font-size:13px;font-weight:900}'
if old_css not in s:
    raise SystemExit('calendar summary css not found')
s = s.replace(old_css, new_css, 1)

# Mobile summary: remove box-specific padding and keep simple text row.
s = s.replace('.calendar-heading{width:100%;max-width:430px}.calendar-total{width:100%;gap:5px}.calendar-stat{padding:7px 8px}.calendar-stat strong{font-size:12px}',
              '.calendar-heading{width:100%;max-width:430px}.calendar-total{width:100%;gap:12px;margin-bottom:10px}.calendar-stat strong{font-size:12px}', 1)

# 2) Replace section 2 so it contains only calendar; move recent/category to a new section 3.
start = s.find('<section class="section-block"><div class="section-intro"><div class="section-intro-left"><span class="section-number">2</span><h2>履歴を見る</h2>')
end = s.find('<div class="toast" id="toast"></div>', start)
if start < 0 or end < 0:
    raise SystemExit('history section not found')

new_history = '''<section class="section-block"><div class="section-intro"><div class="section-intro-left"><span class="section-number">2</span><h2>履歴を見る</h2></div><p>日付ごとの学習履歴を確認</p></div>
<section class="card card-pad"><div class="calendar-toolbar"><button class="btn" id="prevMonthBtn" type="button">←</button><div class="calendar-heading"><div class="calendar-title" id="calendarTitle"></div></div><button class="btn" id="nextMonthBtn" type="button">→</button></div><div class="tabs"><button class="btn active" id="monthViewBtn" type="button">月</button><button class="btn" id="yearViewBtn" type="button">年</button></div><div class="calendar-total" id="calendarMonthTotal"></div><div id="monthView"><div class="dow"><span>月</span><span>火</span><span>水</span><span>木</span><span>金</span><span>土</span><span>日</span></div><div class="calendar-grid" id="calendarGrid"></div></div><div id="yearView" class="year-grid hidden"></div></section></section>
<section class="section-block"><div class="section-intro"><div class="section-intro-left"><span class="section-number">3</span><h2>編集</h2></div><p>記録・カテゴリを編集</p></div><section class="card card-pad"><div class="tabs"><button class="btn tab active" type="button" data-panel="recentPanel">最近</button><button class="btn tab" type="button" data-panel="categoryPanel">カテゴリ</button></div><div id="recentPanel"><div class="section-head"><h3>最近の記録</h3><span id="recentCount"></span></div><div class="list" id="recentList"></div></div><div id="categoryPanel" class="hidden"><div class="section-head"><h3>カテゴリ管理</h3><span>追加・並べ替え・削除</span></div><div class="entry-form"><div><label for="newCategoryInput">カテゴリ名</label><input id="newCategoryInput" type="text" placeholder="例: Conversation" /></div><button class="btn primary" id="addCategoryBtn" type="button">追加</button></div><div class="list" id="categoryList" style="margin-top:12px"></div></div></section></section></div>
'''
s = s[:start] + new_history + s[end:]

# 3) Only month/year remain as calendar modes.
s = s.replace("function renderCalendar(){if(calendarView==='year')return renderYear();if(calendarView==='months')return renderMonths();if(calendarView==='weeks')return renderWeeks();",
              "function renderCalendar(){if(calendarView==='year')return renderYear();", 1)

# Previous/next changes by month or year only.
old_nav = "$('prevMonthBtn').addEventListener('click',()=>{if(calendarView==='year'||calendarView==='months')currentMonth.setFullYear(currentMonth.getFullYear()-1);else currentMonth.setMonth(currentMonth.getMonth()-1);renderCalendar()});$('nextMonthBtn').addEventListener('click',()=>{if(calendarView==='year'||calendarView==='months')currentMonth.setFullYear(currentMonth.getFullYear()+1);else currentMonth.setMonth(currentMonth.getMonth()+1);renderCalendar()});"
new_nav = "$('prevMonthBtn').addEventListener('click',()=>{if(calendarView==='year')currentMonth.setFullYear(currentMonth.getFullYear()-1);else currentMonth.setMonth(currentMonth.getMonth()-1);renderCalendar()});$('nextMonthBtn').addEventListener('click',()=>{if(calendarView==='year')currentMonth.setFullYear(currentMonth.getFullYear()+1);else currentMonth.setMonth(currentMonth.getMonth()+1);renderCalendar()});"
if old_nav not in s:
    raise SystemExit('calendar nav handlers not found')
s = s.replace(old_nav, new_nav, 1)

# Year dots go directly back to month; no month-total/weekly modes.
old_year_click = "$('yearView').addEventListener('click',e=>{const b=e.target.closest('[data-date],[data-month]');if(!b)return;if(b.dataset.month!==undefined){currentMonth.setMonth(Number(b.dataset.month));currentMonth.setDate(1);calendarView='weeks';setCalendarView();return}selectedDate=b.dataset.date;currentMonth=parseDate(selectedDate);currentMonth.setDate(1);calendarView='month';setCalendarView();renderSelectedDay()});"
new_year_click = "$('yearView').addEventListener('click',e=>{const b=e.target.closest('[data-date]');if(!b)return;selectedDate=b.dataset.date;currentMonth=parseDate(selectedDate);currentMonth.setDate(1);calendarView='month';setCalendarView();renderSelectedDay()});"
if old_year_click not in s:
    raise SystemExit('year click handler not found')
s = s.replace(old_year_click, new_year_click, 1)

old_set_view = "function setCalendarView(){const m=calendarView==='month',y=calendarView==='year',ms=calendarView==='months',w=calendarView==='weeks';$('monthView').classList.toggle('hidden',!m);$('yearView').classList.toggle('hidden',m);$('monthViewBtn').classList.toggle('active',m);$('yearViewBtn').classList.toggle('active',y);$('monthTotalViewBtn').classList.toggle('active',ms);$('weekTotalViewBtn').classList.toggle('active',w);renderCalendar()}$('monthViewBtn').addEventListener('click',()=>{calendarView='month';setCalendarView()});$('yearViewBtn').addEventListener('click',()=>{calendarView='year';setCalendarView()});$('monthTotalViewBtn').addEventListener('click',()=>{calendarView='months';setCalendarView()});$('weekTotalViewBtn').addEventListener('click',()=>{calendarView='weeks';setCalendarView()});"
new_set_view = "function setCalendarView(){const m=calendarView==='month',y=calendarView==='year';$('monthView').classList.toggle('hidden',!m);$('yearView').classList.toggle('hidden',m);$('monthViewBtn').classList.toggle('active',m);$('yearViewBtn').classList.toggle('active',y);renderCalendar()}$('monthViewBtn').addEventListener('click',()=>{calendarView='month';setCalendarView()});$('yearViewBtn').addEventListener('click',()=>{calendarView='year';setCalendarView()});"
if old_set_view not in s:
    raise SystemExit('calendar view handlers not found')
s = s.replace(old_set_view, new_set_view, 1)

p.write_text(s, encoding='utf-8')
