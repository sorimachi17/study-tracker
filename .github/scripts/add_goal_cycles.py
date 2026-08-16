from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) Add current-goal metadata under the target controls.
old_head = '''<div class="card progress-card"><div class="challenge-title"><h2>これまでの累計学習時間</h2><div class="target-setting"><label for="targetHoursInput">目標</label><input id="targetHoursInput" type="number" min="1" step="1" value="100" /><span>時間</span><button class="btn" id="saveTargetBtn" type="button">変更</button></div></div><div class="total-row">'''
new_head = '''<div class="card progress-card"><div class="challenge-title"><h2>これまでの累計学習時間</h2><div class="target-setting"><label for="targetHoursInput">現在の目標</label><input id="targetHoursInput" type="number" min="1" step="1" value="100" /><span>時間</span><button class="btn" id="saveTargetBtn" type="button">変更</button></div></div><div class="current-goal-meta"><div><span>現在の目標</span><strong id="currentGoalName">第1目標</strong></div><div><span>開始日</span><strong id="currentGoalStart">-</strong></div><div><span>今回の積み上げ</span><strong id="currentGoalProgress">0分</strong></div></div><div class="total-row">'''
if old_head not in s:
    raise SystemExit('progress header block not found')
s = s.replace(old_head, new_head, 1)

# 2) Add goal history and next-goal controls after the milestone cards.
old_tail = '''<div class="milestone prediction"><span id="targetPredictionLabel">到達予測</span><strong id="daysTo100">-</strong><em id="paceDetail">-</em></div></div></div></section>'''
new_tail = '''<div class="milestone prediction"><span id="targetPredictionLabel">到達予測</span><strong id="daysTo100">-</strong><em id="paceDetail">-</em></div></div><div class="goal-history-panel"><div class="goal-history-head"><h3>目標履歴</h3><span id="goalHistoryCount"></span></div><div class="goal-history-list" id="goalHistoryList"></div><div class="next-goal-box hidden" id="nextGoalBox"><div><span>次の目標</span><strong>新しいチャレンジを開始</strong></div><div class="next-goal-actions"><input id="nextGoalHoursInput" type="number" min="1" step="1" value="100" aria-label="次の目標時間" /><span>時間</span><button class="btn primary" id="startNextGoalBtn" type="button">次の目標を開始</button></div></div></div></div></section>'''
if old_tail not in s:
    raise SystemExit('milestone tail not found')
s = s.replace(old_tail, new_tail, 1)

# 3) Styling.
css_marker = '/* goal-cycles-v1 */'
if css_marker not in s:
    css = r'''
/* goal-cycles-v1 */
.current-goal-meta{display:flex;gap:18px;align-items:center;flex-wrap:wrap;margin:-4px 0 16px;color:var(--muted)}.current-goal-meta>div{display:flex;align-items:baseline;gap:6px}.current-goal-meta span{font-size:10px;font-weight:850}.current-goal-meta strong{color:var(--text);font-size:12px;font-weight:900}.goal-history-panel{margin-top:16px;padding-top:16px;border-top:1px solid var(--line)}.goal-history-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:9px}.goal-history-head h3{margin:0;font-size:14px}.goal-history-head span{color:var(--muted);font-size:10px;font-weight:800}.goal-history-list{display:grid;gap:7px}.goal-history-row{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:4px 12px;padding:10px 12px;border:1px solid var(--line);border-radius:10px;background:var(--surface2)}.goal-history-row strong{font-size:12px}.goal-history-row b{font-size:12px;white-space:nowrap}.goal-history-row small{grid-column:1/-1;color:var(--muted);font-size:10px;font-weight:750}.goal-history-empty{padding:10px 0;color:var(--muted);font-size:11px}.next-goal-box{margin-top:10px;padding:12px;border:1px solid var(--line);border-radius:11px;background:var(--greenSoft);display:flex;align-items:center;justify-content:space-between;gap:12px}.next-goal-box>div:first-child{display:flex;flex-direction:column;gap:2px}.next-goal-box>div:first-child span{color:var(--muted);font-size:10px;font-weight:850}.next-goal-box>div:first-child strong{font-size:12px}.next-goal-actions{display:flex;align-items:center;gap:7px}.next-goal-actions input{width:82px;min-height:38px;padding:6px 8px}.next-goal-actions>span{color:var(--muted);font-size:11px;font-weight:800}.next-goal-actions .btn{min-height:38px;font-size:11px}.target-setting .btn:disabled,.target-setting input:disabled{opacity:.55;cursor:not-allowed}
@media(max-width:620px){.current-goal-meta{display:grid;grid-template-columns:1fr 1fr;gap:6px 12px;margin-bottom:14px}.current-goal-meta>div{display:flex;flex-direction:column;gap:1px}.next-goal-box{align-items:stretch;flex-direction:column}.next-goal-actions{width:100%}.next-goal-actions input{flex:1;width:auto}.next-goal-actions .btn{flex:0 0 auto}.goal-history-row{padding:10px}}
'''
    s = s.replace('</style>', css + '</style>', 1)

# 4) Initialize goal storage after app state is created.
state_anchor = "DAY_MS=86400000;"
state_insert = "DAY_MS=86400000;const GOALS_STORAGE='study-tracker.goals.v1';let goalHistory=load(GOALS_STORAGE,[]);ensureGoalHistory();"
if 'GOALS_STORAGE' not in s:
    if state_anchor not in s:
        raise SystemExit('state anchor not found')
    s = s.replace(state_anchor, state_insert, 1)

# 5) Add goal helpers and override dashboard/chart functions after the existing renderDashboard/renderProgressChart definitions.
js_marker = '/* goal-cycles-js-v1 */'
if js_marker not in s:
    anchor = "function calendarStatsHtml(stats)"
    if anchor not in s:
        raise SystemExit('calendarStatsHtml anchor not found')
    js = r'''/* goal-cycles-js-v1 */
function ensureGoalHistory(){
  if(Array.isArray(goalHistory)&&goalHistory.length)return;
  const first=firstStudyDate(),created=entries.map(e=>Number(e.createdAt||0)).filter(Boolean),startAt=created.length?Math.max(0,Math.min(...created)-1):Date.now();
  goalHistory=[{id:'goal-'+Date.now(),number:1,targetHours:Math.max(1,Number(targetHours||100)),startDate:first?dateKey(first):todayKey(),startAt,baselineMinutes:0,status:'active',completedDate:null,completedAt:null,completedMinutes:null}];
  save(GOALS_STORAGE,goalHistory);
}
function currentGoal(){ensureGoalHistory();return goalHistory.find(g=>g.status==='active')||goalHistory[goalHistory.length-1]}
function activeGoal(){return goalHistory.find(g=>g.status==='active')||null}
function goalEntries(g){const startAt=Number(g?.startAt||0);return entries.filter(e=>Number(e.createdAt||0)>=startAt)}
function goalProgressMinutes(g){return goalEntries(g).reduce((t,e)=>t+Number(e.minutes||0),0)}
function goalDailyTotals(g){const out={};goalEntries(g).forEach(e=>out[e.date]=(out[e.date]||0)+Number(e.minutes||0));return out}
function goalEndDate(g){return g.status==='completed'&&g.completedDate?parseDate(g.completedDate):parseDate(todayKey())}
function goalElapsedDays(g){const start=parseDate(g.startDate||todayKey()),end=goalEndDate(g);return Math.max(0,Math.floor((end-start)/DAY_MS))}
function goalAverageMinutes(g){return goalProgressMinutes(g)/Math.max(1,goalElapsedDays(g)+1)}
function goalBestDay(g){const daily=goalDailyTotals(g),rows=Object.entries(daily);if(!rows.length)return{date:null,minutes:0};rows.sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0]));return{date:rows[0][0],minutes:rows[0][1]}}
function goalStreakStats(g){
  const dates=Object.keys(goalDailyTotals(g)).sort();if(!dates.length)return{current:0,longest:0,longestStart:null,longestEnd:null};
  const set=new Set(dates),today=parseDate(todayKey()),start=parseDate(g.startDate||todayKey());let cursor=new Date(today),current=0;
  if(!set.has(dateKey(cursor))){cursor.setDate(cursor.getDate()-1)}
  while(cursor>=start&&set.has(dateKey(cursor))){current++;cursor.setDate(cursor.getDate()-1)}
  let longest=0,run=0,runStart=null,bestStart=null,bestEnd=null,prev=null;
  dates.forEach(k=>{const d=parseDate(k);if(prev&&Math.round((d-prev)/DAY_MS)===1){run++}else{run=1;runStart=k}if(run>longest){longest=run;bestStart=runStart;bestEnd=k}prev=d});
  return{current,longest,longestStart:bestStart,longestEnd:bestEnd};
}
function goalPrediction(g,remaining){if(remaining<=0)return{primary:'達成',detail:g.completedDate?formatShortDate(g.completedDate)+'に達成':'目標達成'};const avg=goalAverageMinutes(g);if(avg<=0)return{primary:'-',detail:'記録が増えると予測'};const days=Math.ceil(remaining/avg),d=parseDate(todayKey());d.setDate(d.getDate()+days);return{primary:formatShortDate(dateKey(d)),detail:'あと'+days+'日'}}
function goalCompletionDate(g){let total=0;const list=goalEntries(g).slice().sort((a,b)=>Number(a.createdAt||0)-Number(b.createdAt||0));for(const e of list){total+=Number(e.minutes||0);if(total>=Number(g.targetHours||0)*60)return e.date||todayKey()}return todayKey()}
function syncGoalCompletion(){const g=activeGoal();if(!g)return false;const progress=goalProgressMinutes(g);if(progress<Number(g.targetHours||0)*60)return false;g.status='completed';g.completedDate=goalCompletionDate(g);g.completedAt=Date.now();g.completedMinutes=progress;save(GOALS_STORAGE,goalHistory);return true}
function renderGoalHistory(g){
  const completed=goalHistory.filter(x=>x.status==='completed');$('goalHistoryCount').textContent=completed.length+'件達成';
  $('goalHistoryList').innerHTML=completed.length?completed.slice().reverse().map(x=>'<div class="goal-history-row"><strong>第'+escapeHtml(x.number)+'目標 ・ '+escapeHtml(x.targetHours)+'時間</strong><b>達成</b><small>'+escapeHtml(formatShortDate(x.startDate))+'開始 → '+escapeHtml(x.completedDate?formatShortDate(x.completedDate):'-')+'達成</small></div>').join(''):'<div class="goal-history-empty">達成した目標はここに残ります。</div>';
  const finished=g&&g.status==='completed';$('nextGoalBox').classList.toggle('hidden',!finished);if(finished)$('nextGoalHoursInput').value=Number(g.targetHours||100);
}
function renderDashboard(){
  syncGoalCompletion();const g=currentGoal();targetHours=Math.max(1,Number(g.targetHours||100));localStorage.setItem(STORAGE.target,String(targetHours));
  const totalMin=sumEntries(()=>true),progress=goalProgressMinutes(g),targetMin=targetHours*60,pct=Math.min(100,progress/targetMin*100),remaining=Math.max(0,targetMin-progress),best=goalBestDay(g),pace=goalPrediction(g,remaining),avgDay=goalAverageMinutes(g),streak=goalStreakStats(g),elapsed=goalElapsedDays(g);
  $('pageTitle').textContent='英語学習トラッカー';$('targetHoursInput').value=targetHours;$('targetHoursInput').disabled=g.status==='completed';$('saveTargetBtn').disabled=g.status==='completed';$('saveTargetBtn').textContent=g.status==='completed'?'達成済み':'変更';
  $('currentGoalName').textContent='第'+g.number+'目標 ・ '+targetHours+'時間';$('currentGoalStart').textContent=formatShortDate(g.startDate)+'開始';$('currentGoalProgress').textContent=studyTimeLabel(progress)+' / '+targetHours+'時間';
  $('targetRemainingLabel').textContent='第'+g.number+'目標（'+targetHours+'時間）までの残り学習時間';$('targetPredictionLabel').textContent='到達予測';$('totalHours').textContent=Math.floor(totalMin/60)+'h';$('totalMinutes').textContent=minutesLabel(totalMin%60);$('goalOrbit').style.setProperty('--pct',pct+'%');$('goalOrbitPercent').textContent=Math.round(pct)+'%';$('remaining100').textContent=studyTimeLabel(remaining);$('remainingDetail').textContent='今回 '+Math.round(pct)+'% 達成';$('daysTo100').textContent=pace.primary;$('paceDetail').textContent=pace.detail;
  $('bestDay').textContent=studyTimeLabel(best.minutes);$('bestDayDate').textContent=best.date?formatShortDate(best.date):'-';$('avgDay').textContent=studyTimeLabel(avgDay);$('avgDayDetail').textContent='現在の目標開始から';$('elapsedDays').textContent=elapsed+'日';$('elapsedDaysDetail').textContent=formatShortDate(g.startDate)+'から';$('streakDays').textContent=streak.current+'日';$('currentStreakDetail').textContent=streak.current>0?'現在の目標期間で継続':'今日の記録なし';$('longestStreakDays').textContent=streak.longest+'日';$('longestStreakDetail').textContent=streak.longest?(streak.longestStart===streak.longestEnd?formatShortDate(streak.longestStart):formatShortDate(streak.longestStart)+'〜'+formatShortDate(streak.longestEnd)):'-';renderGoalHistory(g)
}
function renderProgressChart(){
  const el=$('cumulativeChart'),label=$('projectionDateLabel'),g=currentGoal(),daily={};entries.forEach(e=>daily[e.date]=(daily[e.date]||0)+Number(e.minutes||0));const dates=Object.keys(daily).sort();
  if(!dates.length){el.innerHTML='<div class="empty">記録すると、ここに累計時間の推移が表示されます。</div>';label.textContent='第'+g.number+'目標の到達予測 -';return}
  const first=parseDate(dates[0]),today=parseDate(todayKey()),points=[];let total=0,d=new Date(first);while(d<=today){const k=dateKey(d);total+=daily[k]||0;points.push({date:new Date(d),minutes:total});d.setDate(d.getDate()+1)}
  const goalTarget=Number(g.baselineMinutes||0)+Number(g.targetHours||0)*60,remaining=Math.max(0,Number(g.targetHours||0)*60-goalProgressMinutes(g)),pred=goalPrediction(g,remaining);label.textContent=g.status==='completed'?'第'+g.number+'目標 達成 '+formatShortDate(g.completedDate):'予測 '+pred.primary;
  const mobile=window.innerWidth<=620,yMax=Math.max(goalTarget,total,60),W=mobile?500:1000,H=mobile?350:340,L=mobile?88:74,R=mobile?30:28,T=mobile?46:22,B=mobile?64:54,pw=W-L-R,ph=H-T-B,x0=first.getTime(),x1=Math.max(today.getTime(),x0+DAY_MS),x=dt=>L+(dt.getTime()-x0)/(x1-x0)*pw,y=m=>T+(1-m/yMax)*ph,actual=points.map(p=>x(p.date).toFixed(1)+','+y(p.minutes).toFixed(1)).join(' '),yTicks=[0,.25,.5,.75,1].map(v=>yMax*v),spanDays=Math.max(1,Math.round((x1-x0)/DAY_MS)),xFractions=spanDays<14?[0,1]:[0,.5,1],xTicks=xFractions.map(v=>new Date(x0+(x1-x0)*v)),gy=yTicks.map(v=>'<line class="chart-grid" x1="'+L+'" y1="'+y(v).toFixed(1)+'" x2="'+(W-R)+'" y2="'+y(v).toFixed(1)+'"></line><text class="chart-axis-text" x="'+(L-(mobile?14:12))+'" y="'+(y(v)+(mobile?8:5)).toFixed(1)+'" text-anchor="end">'+(v/60).toFixed(v%60?1:0)+'h</text>').join(''),gx=xTicks.map((v,i,arr)=>{const isFirst=i===0,isLast=i===arr.length-1,tx=isFirst?L:isLast?(W-R):x(v),anchor=isFirst?'start':isLast?'end':'middle';return '<text class="chart-axis-text" x="'+tx.toFixed(1)+'" y="'+(H-(mobile?20:17))+'" text-anchor="'+anchor+'">'+chartDateLabel(v)+'</text>'}).join(''),goalY=y(goalTarget).toFixed(1);el.innerHTML='<svg class="chart-svg" viewBox="0 0 '+W+' '+H+'" role="img" aria-label="日付ごとの累計学習時間"><line class="chart-goal" x1="'+L+'" y1="'+goalY+'" x2="'+(W-R)+'" y2="'+goalY+'"></line>'+gy+'<text class="chart-axis-title" x="'+(mobile?8:14)+'" y="'+(mobile?22:18)+'">累計時間</text><text class="chart-goal-label" x="'+(W-R)+'" y="'+(Number(goalY)-(mobile?10:7))+'" text-anchor="end">第'+g.number+'目標</text>'+gx+'<polyline class="chart-actual" points="'+actual+'"></polyline></svg>'
}
'''
    s = s.replace(anchor, js + anchor, 1)

# 6) Replace target update handler so it updates the active goal only.
pattern = re.compile(r"\$\('saveTargetBtn'\)\.addEventListener\('click',\(\)=>\{.*?\}\);(?=\$\('entryForm'\))", re.S)
replacement = """$('saveTargetBtn').addEventListener('click',()=>{const g=activeGoal();if(!g){showToast('次の目標を開始してください');return}const v=Math.round(Number($('targetHoursInput').value));if(!Number.isFinite(v)||v<1){showToast('目標時間を入力してください');return}g.targetHours=v;targetHours=v;save(GOALS_STORAGE,goalHistory);localStorage.setItem(STORAGE.target,String(targetHours));renderDashboard();renderProgressChart();showToast('現在の目標を'+targetHours+'時間に変更しました')});"""
s, n = pattern.subn(replacement, s, count=1)
if n != 1:
    raise SystemExit(f'save target handler replacement failed: {n}')

# 7) Start-next-goal handler.
if "$('startNextGoalBtn').addEventListener" not in s:
    insert_before = "$('entryForm').addEventListener('submit'"
    handler = """$('startNextGoalBtn').addEventListener('click',()=>{const last=currentGoal();if(!last||last.status!=='completed')return;const hours=Math.round(Number($('nextGoalHoursInput').value));if(!Number.isFinite(hours)||hours<1){showToast('次の目標時間を入力してください');return}const next={id:'goal-'+Date.now(),number:Number(last.number||goalHistory.length)+1,targetHours:hours,startDate:todayKey(),startAt:Date.now()+1,baselineMinutes:sumEntries(()=>true),status:'active',completedDate:null,completedAt:null,completedMinutes:null};goalHistory.push(next);targetHours=hours;save(GOALS_STORAGE,goalHistory);localStorage.setItem(STORAGE.target,String(hours));renderAll();showToast('第'+next.number+'目標を開始しました')});"""
    if insert_before not in s:
        raise SystemExit('entry form listener anchor not found')
    s = s.replace(insert_before, handler + insert_before, 1)

# 8) Preserve goal history in backups.
s = s.replace("JSON.stringify({entries,categories,weeklyGoalHours,targetHours},null,2)", "JSON.stringify({entries,categories,weeklyGoalHours,targetHours,goals:goalHistory},null,2)", 1)

# 9) Import goal history when present; old backups still create a first goal automatically.
import_old = "targetHours=Math.max(1,Number(data.targetHours||targetHours||DEFAULT_TARGET_HOURS));save(STORAGE.entries,entries);save(STORAGE.categories,categories);localStorage.setItem(STORAGE.goal,String(weeklyGoalHours));localStorage.setItem(STORAGE.target,String(targetHours));renderAll();showToast('読み込みました')"
import_new = "targetHours=Math.max(1,Number(data.targetHours||targetHours||DEFAULT_TARGET_HOURS));goalHistory=Array.isArray(data.goals)?data.goals:[];save(STORAGE.entries,entries);save(STORAGE.categories,categories);save(GOALS_STORAGE,goalHistory);if(!goalHistory.length)ensureGoalHistory();const importedGoal=currentGoal();if(importedGoal)targetHours=Math.max(1,Number(importedGoal.targetHours||targetHours));localStorage.setItem(STORAGE.goal,String(weeklyGoalHours));localStorage.setItem(STORAGE.target,String(targetHours));renderAll();showToast('読み込みました')"
if import_old in s:
    s = s.replace(import_old, import_new, 1)
else:
    raise SystemExit('import block not found')

# 10) Reset goals too when all learning data is deliberately deleted.
delete_old = "entries=[];save(STORAGE.entries,entries);localStorage.removeItem(LEGACY_STORAGE.entries);localStorage.setItem(STORAGE.legacyMigrated,'true');selectedDate=todayKey();"
delete_new = "entries=[];save(STORAGE.entries,entries);localStorage.removeItem(LEGACY_STORAGE.entries);localStorage.setItem(STORAGE.legacyMigrated,'true');goalHistory=[];save(GOALS_STORAGE,goalHistory);ensureGoalHistory();targetHours=currentGoal().targetHours;selectedDate=todayKey();"
if delete_old in s:
    s = s.replace(delete_old, delete_new, 1)
else:
    raise SystemExit('delete-all block not found')

p.write_text(s, encoding='utf-8')
