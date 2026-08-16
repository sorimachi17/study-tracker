from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Add start-date control beside target hours.
old='''<div class="target-setting"><label for="targetHoursInput">目標</label><input id="targetHoursInput" type="number" min="1" step="1" value="100" /><span>時間</span><button class="btn" id="saveTargetBtn" type="button">変更</button></div>'''
new='''<div class="target-setting"><div class="target-field"><label for="targetHoursInput">目標</label><div class="target-inline"><input id="targetHoursInput" type="number" min="1" step="1" value="100" /><span>時間</span></div></div><div class="target-field target-start-field"><label for="targetStartDateInput">開始日</label><input id="targetStartDateInput" type="date" /></div><button class="btn" id="saveTargetBtn" type="button">変更</button></div>'''
if old not in s:
    raise SystemExit('target setting block not found')
s=s.replace(old,new,1)

# Target UI styling.
if 'target-start-date-v1' not in s:
    css='''\n/* target-start-date-v1 */\n.target-setting{align-items:flex-end}.target-field{display:flex;flex-direction:column;gap:4px}.target-field label{margin:0}.target-inline{display:flex;align-items:center;gap:6px}.target-start-field input{width:142px;min-height:36px;padding:6px 8px}.target-setting .target-inline input{width:78px}.target-start-note{color:var(--muted);font-size:10px;font-weight:750}\n@media(max-width:620px){.target-setting{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr) auto;align-items:end;gap:8px}.target-setting .target-inline input,.target-start-field input{width:100%;min-width:0}.target-setting .btn{min-width:58px}}\n'''
    s=s.replace('</style>',css+'</style>',1)

# Add target-start storage and runtime variable.
old_state="const STORAGE={entries:'study-tracker.entries.v2',categories:'study-tracker.categories.v2',goal:'study-tracker.weeklyGoalHours.v2',target:'study-tracker.targetHours.v1',legacyMigrated:'study-tracker.legacyMigrated.v7'}"
new_state="const STORAGE={entries:'study-tracker.entries.v2',categories:'study-tracker.categories.v2',goal:'study-tracker.weeklyGoalHours.v2',target:'study-tracker.targetHours.v1',targetStart:'study-tracker.targetStartDate.v1',legacyMigrated:'study-tracker.legacyMigrated.v7'}"
if old_state not in s:
    raise SystemExit('storage block not found')
s=s.replace(old_state,new_state,1)

old_var="targetHours=Math.max(1,Number(localStorage.getItem(STORAGE.target)||DEFAULT_TARGET_HOURS)),currentMonth=new Date()"
new_var="targetHours=Math.max(1,Number(localStorage.getItem(STORAGE.target)||DEFAULT_TARGET_HOURS)),targetStartDate=localStorage.getItem(STORAGE.targetStart)||'',currentMonth=new Date()"
if old_var not in s:
    raise SystemExit('targetHours variable block not found')
s=s.replace(old_var,new_var,1)

# Helpers for target-period calculations.
anchor='function recentPeriodStats(start,end)'
if 'function effectiveTargetStartDate()' not in s:
    helpers='''function effectiveTargetStartDate(){if(targetStartDate)return targetStartDate;const first=firstStudyDate();return first?dateKey(first):todayKey()}function targetPeriodEntries(){const start=effectiveTargetStartDate();return entries.filter(e=>e.date>=start)}function targetPeriodTotal(){return targetPeriodEntries().reduce((t,e)=>t+Number(e.minutes||0),0)}function targetPeriodDailyAverage(){const start=parseDate(effectiveTargetStartDate()),today=parseDate(todayKey());if(start>today)return 0;const days=Math.max(1,Math.floor((today-start)/DAY_MS)+1);return targetPeriodTotal()/days}function targetPeriodBestDay(){const totals={};targetPeriodEntries().forEach(e=>totals[e.date]=(totals[e.date]||0)+Number(e.minutes||0));let b={date:'',minutes:0};Object.entries(totals).forEach(([date,minutes])=>{if(minutes>b.minutes)b={date,minutes}});return b}function targetPeriodStreakStats(){const start=effectiveTargetStartDate(),days=[...new Set(targetPeriodEntries().filter(e=>Number(e.minutes||0)>0&&e.date).map(e=>e.date))].sort();let best=0,run=0,prev=null,runStart='',bestStart='',bestEnd='';days.forEach(k=>{const d=parseDate(k);if(prev&&Math.round((d-prev)/DAY_MS)===1)run++;else{run=1;runStart=k}if(run>best){best=run;bestStart=runStart;bestEnd=k}prev=d});let current=0,d=parseDate(todayKey());while(dateKey(d)>=start&&days.includes(dateKey(d))){current++;d.setDate(d.getDate()-1)}return{current,longest:best,start:bestStart,end:bestEnd}}function targetPaceToGoal(remaining){if(remaining<=0)return{primary:'達成',detail:targetHours+'時間を達成'};const avg=targetPeriodDailyAverage();if(avg<=0)return{primary:'-',detail:'記録が増えると予測'};const days=Math.ceil(remaining/avg),target=parseDate(todayKey());target.setDate(target.getDate()+days);return{primary:formatShortDate(dateKey(target)),detail:'あと'+days+'日'}}\n'''
    if anchor not in s:
        raise SystemExit('helper anchor not found')
    s=s.replace(anchor,helpers+anchor,1)

# Replace dashboard with start-date scoped goal metrics while keeping all-time total.
dash_pattern=r"function renderDashboard\(\)\{.*?\}\nfunction chartDateLabel"
dash_new='''function renderDashboard(){const totalMin=sumEntries(()=>true),goalMin=targetPeriodTotal(),targetMin=targetHours*60,pct=Math.min(100,goalMin/targetMin*100),remaining=Math.max(0,targetMin-goalMin),best=targetPeriodBestDay(),pace=targetPaceToGoal(remaining),avgDay=targetPeriodDailyAverage(),startKey=effectiveTargetStartDate(),start=parseDate(startKey),today=parseDate(todayKey()),streak=targetPeriodStreakStats(),elapsedDays=start<=today?Math.max(0,Math.floor((today-start)/DAY_MS)):0;$('pageTitle').textContent='英語'+targetHours+'時間チャレンジ';$('targetHoursInput').value=targetHours;$('targetStartDateInput').value=startKey;$('targetRemainingLabel').textContent='目標（'+targetHours+'時間）までの残り学習時間';$('targetPredictionLabel').textContent='到達予測';$('totalHours').textContent=Math.floor(totalMin/60)+'h';$('totalMinutes').textContent=minutesLabel(totalMin%60);$('goalOrbit').style.setProperty('--pct',pct+'%');$('goalOrbitPercent').textContent=Math.round(pct)+'%';$('remaining100').textContent=studyTimeLabel(remaining);$('remainingDetail').textContent=formatShortDate(startKey)+'開始 ・ '+Math.round(pct)+'% 達成';$('daysTo100').textContent=pace.primary;$('paceDetail').textContent=pace.detail;$('bestDay').textContent=studyTimeLabel(best.minutes);$('bestDayDate').textContent=best.date?formatShortDate(best.date):'-';$('avgDay').textContent=studyTimeLabel(avgDay);$('avgDayDetail').textContent='目標開始日から今日まで';$('elapsedDays').textContent=elapsedDays+'日';$('elapsedDaysDetail').textContent=formatShortDate(startKey)+'から';$('streakDays').textContent=streak.current+'日';$('currentStreakDetail').textContent=streak.current>0?'目標期間で継続':'今日の記録なし';$('longestStreakDays').textContent=streak.longest+'日';$('longestStreakDetail').textContent=streak.longest?(streak.start===streak.end?formatShortDate(streak.start):formatShortDate(streak.start)+'〜'+formatShortDate(streak.end)):'-'}
function chartDateLabel'''
s,n=re.subn(dash_pattern,dash_new,s,count=1,flags=re.S)
if n!=1:
    raise SystemExit('renderDashboard replacement failed')

# Replace progress chart so the target line/projection use the selected start date.
chart_pattern=r"function renderProgressChart\(\)\{.*?\}function level\("
chart_new='''function renderProgressChart(){const el=$('cumulativeChart'),label=$('projectionDateLabel'),startKey=effectiveTargetStartDate(),start=parseDate(startKey),today=parseDate(todayKey()),daily={};targetPeriodEntries().forEach(e=>daily[e.date]=(daily[e.date]||0)+Number(e.minutes||0));if(start>today){el.innerHTML='<div class="empty">開始日が未来に設定されています。</div>';label.textContent='目標到達予測 -';return}const points=[];let total=0,d=new Date(start);while(d<=today){const k=dateKey(d);total+=daily[k]||0;points.push({date:new Date(d),minutes:total});d.setDate(d.getDate()+1)}const remaining=Math.max(0,targetHours*60-total),avg=targetPeriodDailyAverage();if(remaining<=0){label.textContent=targetHours+'時間達成'}else if(avg>0){const target=new Date(today);target.setDate(target.getDate()+Math.ceil(remaining/avg));label.textContent='予測 '+formatShortDate(dateKey(target))}else label.textContent=targetHours+'時間の到達予測 -';const mobile=window.innerWidth<=620,yMax=Math.max(targetHours*60,total,60),W=mobile?500:1000,H=mobile?350:340,L=mobile?88:74,R=mobile?30:28,T=mobile?46:22,B=mobile?64:54,pw=W-L-R,ph=H-T-B,x0=start.getTime(),x1=Math.max(today.getTime(),x0+DAY_MS),x=dt=>L+(dt.getTime()-x0)/(x1-x0)*pw,y=m=>T+(1-m/yMax)*ph,actual=points.map(p=>x(p.date).toFixed(1)+','+y(p.minutes).toFixed(1)).join(' '),yTicks=[0,.25,.5,.75,1].map(v=>yMax*v),spanDays=Math.max(1,Math.round((x1-x0)/DAY_MS)),xFractions=spanDays<14?[0,1]:[0,.5,1],xTicks=xFractions.map(v=>new Date(x0+(x1-x0)*v)),gy=yTicks.map(v=>'<line class="chart-grid" x1="'+L+'" y1="'+y(v).toFixed(1)+'" x2="'+(W-R)+'" y2="'+y(v).toFixed(1)+'"></line><text class="chart-axis-text" x="'+(L-(mobile?14:12))+'" y="'+(y(v)+(mobile?8:5)).toFixed(1)+'" text-anchor="end">'+(v/60).toFixed(v%60?1:0)+'h</text>').join(''),gx=xTicks.map((v,i,arr)=>{const isFirst=i===0,isLast=i===arr.length-1,tx=isFirst?L:isLast?(W-R):x(v),anchor=isFirst?'start':isLast?'end':'middle';return '<text class="chart-axis-text" x="'+tx.toFixed(1)+'" y="'+(H-(mobile?20:17))+'" text-anchor="'+anchor+'">'+chartDateLabel(v)+'</text>'}).join(''),goalY=y(targetHours*60).toFixed(1);el.innerHTML='<svg class="chart-svg" viewBox="0 0 '+W+' '+H+'" role="img" aria-label="目標開始日からの累計学習時間"><line class="chart-goal" x1="'+L+'" y1="'+goalY+'" x2="'+(W-R)+'" y2="'+goalY+'"></line>'+gy+'<text class="chart-axis-title" x="'+(mobile?8:14)+'" y="'+(mobile?22:18)+'">目標期間</text><text class="chart-goal-label" x="'+(W-R)+'" y="'+(Number(goalY)-(mobile?10:7))+'" text-anchor="end">目標</text>'+gx+'<polyline class="chart-actual" points="'+actual+'"></polyline></svg>'}function level('''
s,n=re.subn(chart_pattern,chart_new,s,count=1,flags=re.S)
if n!=1:
    raise SystemExit('renderProgressChart replacement failed')

# Save target hours and start date together.
save_pattern=r"\$\('saveTargetBtn'\)\.addEventListener\('click',\(\)=>\{.*?showToast\('目標を'\+targetHours\+'時間に変更しました'\)\}\);"
save_new="$('saveTargetBtn').addEventListener('click',()=>{const v=Math.round(Number($('targetHoursInput').value)),start=$('targetStartDateInput').value;if(!Number.isFinite(v)||v<1){showToast('目標時間を入力してください');return}if(!start){showToast('開始日を入力してください');return}targetHours=v;targetStartDate=start;localStorage.setItem(STORAGE.target,String(targetHours));localStorage.setItem(STORAGE.targetStart,targetStartDate);renderDashboard();renderProgressChart();showToast('目標を更新しました')});"
s,n=re.subn(save_pattern,save_new,s,count=1,flags=re.S)
if n!=1:
    raise SystemExit('save target listener replacement failed')

# Include start date in JSON export/import.
old_export="JSON.stringify({entries,categories,weeklyGoalHours,targetHours},null,2)"
new_export="JSON.stringify({entries,categories,weeklyGoalHours,targetHours,targetStartDate:effectiveTargetStartDate()},null,2)"
if old_export in s:
    s=s.replace(old_export,new_export,1)

old_import="targetHours=Math.max(1,Number(data.targetHours||targetHours||DEFAULT_TARGET_HOURS));save(STORAGE.entries,entries)"
new_import="targetHours=Math.max(1,Number(data.targetHours||targetHours||DEFAULT_TARGET_HOURS));targetStartDate=data.targetStartDate||targetStartDate||'';save(STORAGE.entries,entries)"
if old_import in s:
    s=s.replace(old_import,new_import,1)

old_store="localStorage.setItem(STORAGE.target,String(targetHours));renderAll();showToast('読み込みました')"
new_store="localStorage.setItem(STORAGE.target,String(targetHours));if(targetStartDate)localStorage.setItem(STORAGE.targetStart,targetStartDate);renderAll();showToast('読み込みました')"
if old_store in s:
    s=s.replace(old_store,new_store,1)

p.write_text(s,encoding='utf-8')
