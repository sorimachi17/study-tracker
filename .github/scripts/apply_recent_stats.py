from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old_html = '<div class="progress-kpis"><div class="section-head"><h3>最近の学習時間</h3><span>すべて合計時間</span></div><div class="kpi-grid"><div class="kpi blue"><span>今日の合計</span><strong id="todayMinutes">0m</strong></div><div class="kpi green"><span>今週の合計</span><strong id="weekMinutes">0h</strong></div></div></div>'
new_html = '<div class="progress-kpis"><div class="section-head"><h3>最近の学習時間</h3><span>期間を選んで確認</span></div><div class="period-card-grid"><div class="period-card day"><div class="period-card-head"><span id="dayCardTitle">今日の合計</span><input class="period-picker" id="dayStatsDate" type="date" /></div><strong id="daySelectedTotal">0分</strong><small id="daySelectedLabel">-</small></div><div class="period-card week"><div class="period-card-head"><span>週の合計</span><select class="period-picker" id="weekStatsSelect"></select></div><strong id="weekSelectedTotal">0分</strong><div class="period-meta"><span>勉強日数 <b id="weekStudyDays">0日</b></span><span>1日平均 <b id="weekDailyAverage">0分</b></span></div></div><div class="period-card month"><div class="period-card-head"><span>月の合計</span><select class="period-picker" id="monthStatsSelect"></select></div><strong id="monthSelectedTotal">0分</strong><div class="period-meta"><span>勉強日数 <b id="monthStudyDays">0日</b></span><span>1日平均 <b id="monthDailyAverage">0分</b></span></div></div></div></div>'
if old_html not in s:
    raise SystemExit('recent stats html not found')
s = s.replace(old_html, new_html, 1)

old_css = '.progress-kpis{margin-top:16px;padding-top:16px;border-top:1px solid var(--line)}'
new_css = old_css + '.period-card-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.period-card{border:1px solid var(--line);border-radius:13px;padding:15px;min-width:0}.period-card.day{background:var(--blueSoft)}.period-card.week{background:var(--greenSoft)}.period-card.month{background:var(--amberSoft)}.period-card-head{display:flex;align-items:center;justify-content:space-between;gap:10px}.period-card-head>span{font-size:12px;font-weight:900;white-space:nowrap}.period-card strong{display:block;margin-top:13px;font-size:27px;line-height:1.05;letter-spacing:-.035em}.period-card small{display:block;margin-top:7px;color:var(--muted);font-size:11px;font-weight:750}.period-picker{width:auto;max-width:68%;min-height:34px;padding:5px 8px;border-radius:9px;font-size:11px;font-weight:800;background:var(--surface)}.period-meta{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:11px;padding-top:10px;border-top:1px solid var(--line)}.period-meta span{display:flex;flex-direction:column;gap:2px;color:var(--muted);font-size:10px;font-weight:750}.period-meta b{color:var(--text);font-size:13px;font-weight:900}'
if old_css not in s:
    raise SystemExit('progress-kpis css not found')
s = s.replace(old_css, new_css, 1)

mobile_marker = '@media(max-width:620px){.app-shell{padding:18px 14px 40px}'
if mobile_marker not in s:
    raise SystemExit('mobile media marker not found')
s = s.replace(mobile_marker, mobile_marker + '.period-card-grid{grid-template-columns:1fr}.period-card{padding:14px}.period-picker{max-width:64%}', 1)

helper_marker = 'function renderAll(){'
if helper_marker not in s:
    raise SystemExit('renderAll marker not found')
helpers = r'''function recentPeriodStats(start,end){const today=parseDate(todayKey()),effectiveEnd=end>today?today:end;if(effectiveEnd<start)return{total:0,studyDays:0,avg:0};const list=entries.filter(e=>{const d=parseDate(e.date);return d>=start&&d<=effectiveEnd}),total=list.reduce((sum,e)=>sum+Number(e.minutes||0),0),studyDays=new Set(list.filter(e=>Number(e.minutes||0)>0).map(e=>e.date)).size,days=Math.max(1,Math.floor((effectiveEnd-start)/DAY_MS)+1);return{total,studyDays,avg:total/days}}
function monthKeyFromDate(d){return d.getFullYear()+'-'+pad(d.getMonth()+1)}
function monthStartFromKey(k){const[y,m]=k.split('-').map(Number);return new Date(y,m-1,1)}
function renderRecentStats(){const dayInput=$('dayStatsDate'),weekSelect=$('weekStatsSelect'),monthSelect=$('monthStatsSelect');if(!dayInput||!weekSelect||!monthSelect)return;const today=todayKey();if(!dayInput.value)dayInput.value=today;const dayKey=dayInput.value||today,dayTotal=sumEntries(e=>e.date===dayKey);$('dayCardTitle').textContent=dayKey===today?'今日の合計':'選択日の合計';$('daySelectedTotal').textContent=studyTimeLabel(dayTotal);$('daySelectedLabel').textContent=formatShortDate(dayKey);const first=firstStudyDate()||parseDate(today),firstWeek=weekStart(first),currentWeek=weekStart(parseDate(today)),previousWeek=weekSelect.value||dateKey(currentWeek),weekOptions=[];for(let d=new Date(firstWeek);d<=currentWeek;d.setDate(d.getDate()+7)){const start=new Date(d),end=new Date(d);end.setDate(end.getDate()+6);weekOptions.push({value:dateKey(start),label:formatShortDate(dateKey(start))+'〜'+formatShortDate(dateKey(end))})}weekSelect.innerHTML=weekOptions.map(o=>'<option value="'+o.value+'">'+o.label+'</option>').join('');weekSelect.value=weekOptions.some(o=>o.value===previousWeek)?previousWeek:weekOptions[weekOptions.length-1].value;const ws=parseDate(weekSelect.value),we=new Date(ws);we.setDate(we.getDate()+6);const weekStats=recentPeriodStats(ws,we);$('weekSelectedTotal').textContent=studyTimeLabel(weekStats.total);$('weekStudyDays').textContent=weekStats.studyDays+'日';$('weekDailyAverage').textContent=studyTimeLabel(weekStats.avg);const firstMonth=new Date(first.getFullYear(),first.getMonth(),1),todayDate=parseDate(today),currentMonthStart=new Date(todayDate.getFullYear(),todayDate.getMonth(),1),previousMonth=monthSelect.value||monthKeyFromDate(currentMonthStart),monthOptions=[];for(let d=new Date(firstMonth);d<=currentMonthStart;d.setMonth(d.getMonth()+1)){monthOptions.push({value:monthKeyFromDate(d),label:d.getFullYear()+'年'+(d.getMonth()+1)+'月'})}monthSelect.innerHTML=monthOptions.map(o=>'<option value="'+o.value+'">'+o.label+'</option>').join('');monthSelect.value=monthOptions.some(o=>o.value===previousMonth)?previousMonth:monthOptions[monthOptions.length-1].value;const ms=monthStartFromKey(monthSelect.value),me=new Date(ms.getFullYear(),ms.getMonth()+1,0),monthStats=recentPeriodStats(ms,me);$('monthSelectedTotal').textContent=studyTimeLabel(monthStats.total);$('monthStudyDays').textContent=monthStats.studyDays+'日';$('monthDailyAverage').textContent=studyTimeLabel(monthStats.avg)}
'''
s = s.replace(helper_marker, helpers + helper_marker, 1)

old_dashboard = "$('todayMinutes').textContent=minutesLabel(todayMin);$('weekMinutes').textContent=minutesLabel(weekMin)}"
if old_dashboard not in s:
    raise SystemExit('dashboard recent assignments not found')
s = s.replace(old_dashboard, 'renderRecentStats()}', 1)

listener_marker = "$('saveTargetBtn').addEventListener('click'"
if listener_marker not in s:
    raise SystemExit('listener marker not found')
listener = "document.addEventListener('change',e=>{if(e.target&&['dayStatsDate','weekStatsSelect','monthStatsSelect'].includes(e.target.id))renderRecentStats()});"
s = s.replace(listener_marker, listener + listener_marker, 1)

p.write_text(s, encoding='utf-8')
