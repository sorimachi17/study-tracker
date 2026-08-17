from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old_date = '<div class="target-field target-start-field"><label for="targetStartDateInput">開始日</label><input class="target-control target-date-control" id="targetStartDateInput" type="date" /></div>'
new_date = '<div class="target-field target-start-field"><label for="targetStartDateInput">開始日</label><div class="target-control target-date-wrap"><input id="targetStartDateInput" type="date" /></div></div>'
if old_date not in s:
    raise SystemExit('target date field block not found')
s = s.replace(old_date, new_date, 1)

old_status = '<div class="goal-status"><div><span id="targetRemainingLabel">目標までの残り学習時間</span><em id="remainingDetail">0% 達成</em></div><strong id="remaining100">100時間</strong></div>'
new_status = '<div class="goal-status dual-goal-status"><div class="goal-status-item today-goal-status"><span>今日の勉強時間の合計</span><strong id="todayStudyTotal">0分</strong><em id="todayStudyDetail">今日</em></div><div class="goal-status-item remaining-goal-status"><span id="targetRemainingLabel">目標までの残り学習時間</span><strong id="remaining100">100時間</strong><em id="remainingDetail">0% 達成</em></div></div>'
if old_status not in s:
    raise SystemExit('goal status block not found')
s = s.replace(old_status, new_status, 1)

old_render = "function renderDashboard(){const totalMin=sumEntries(()=>true),goalMin=targetPeriodTotal(),targetMin=targetHours*60,pct=Math.min(100,goalMin/targetMin*100),remaining=Math.max(0,targetMin-goalMin),best=targetPeriodBestDay(),pace=targetPaceToGoal(remaining),avgDay=targetPeriodDailyAverage(),startKey=effectiveTargetStartDate(),start=parseDate(startKey),today=parseDate(todayKey()),streak=targetPeriodStreakStats(),elapsedDays=start<=today?Math.max(0,Math.floor((today-start)/DAY_MS)):0;$('pageTitle').textContent='英語'+targetHours+'時間チャレンジ';$('targetHoursInput').value=targetHours;$('targetStartDateInput').value=startKey;$('targetRemainingLabel').textContent='目標（'+targetHours+'時間）までの残り学習時間';$('targetPredictionLabel').textContent='到達予測';$('totalHours').textContent=Math.floor(totalMin/60)+'h';$('totalMinutes').textContent=minutesLabel(totalMin%60);$('targetPeriodHours').textContent=Math.floor(goalMin/60)+'h';$('targetPeriodMinutes').textContent=minutesLabel(goalMin%60);$('targetPeriodRange').textContent=formatShortDate(startKey)+'開始 ・ 目標 '+targetHours+'時間';$('goalOrbit').style.setProperty('--pct',pct+'%');$('goalOrbitPercent').textContent=Math.round(pct)+'%';$('remaining100').textContent=studyTimeLabel(remaining);$('remainingDetail').textContent=formatShortDate(startKey)+'開始 ・ '+Math.round(pct)+'% 達成';$('daysTo100').textContent=pace.primary;$('paceDetail').textContent=pace.detail;$('bestDay').textContent=studyTimeLabel(best.minutes);$('bestDayDate').textContent=best.date?formatShortDate(best.date):'-';$('avgDay').textContent=studyTimeLabel(avgDay);$('avgDayDetail').textContent='目標開始日から今日まで';$('elapsedDays').textContent=elapsedDays+'日';$('elapsedDaysDetail').textContent=formatShortDate(startKey)+'から';$('streakDays').textContent=streak.current+'日';$('currentStreakDetail').textContent=streak.current>0?'目標期間で継続':'今日の記録なし';$('longestStreakDays').textContent=streak.longest+'日';$('longestStreakDetail').textContent=streak.longest?(streak.start===streak.end?formatShortDate(streak.start):formatShortDate(streak.start)+'〜'+formatShortDate(streak.end)):'-'}"
new_render = "function renderDashboard(){const totalMin=sumEntries(()=>true),todayMin=sumEntries(e=>e.date===todayKey()),goalMin=targetPeriodTotal(),targetMin=targetHours*60,pct=Math.min(100,goalMin/targetMin*100),remaining=Math.max(0,targetMin-goalMin),best=targetPeriodBestDay(),pace=targetPaceToGoal(remaining),avgDay=targetPeriodDailyAverage(),startKey=effectiveTargetStartDate(),start=parseDate(startKey),today=parseDate(todayKey()),streak=targetPeriodStreakStats(),elapsedDays=start<=today?Math.max(0,Math.floor((today-start)/DAY_MS)):0;$('pageTitle').textContent='英語'+targetHours+'時間チャレンジ';$('targetHoursInput').value=targetHours;$('targetStartDateInput').value=startKey;$('targetRemainingLabel').textContent='目標までの残り学習時間';$('targetPredictionLabel').textContent='到達予測';$('totalHours').textContent=Math.floor(totalMin/60)+'h';$('totalMinutes').textContent=minutesLabel(totalMin%60);$('targetPeriodHours').textContent=Math.floor(goalMin/60)+'h';$('targetPeriodMinutes').textContent=minutesLabel(goalMin%60);$('targetPeriodRange').textContent=formatShortDate(startKey)+'開始 ・ 目標 '+targetHours+'時間';$('todayStudyTotal').textContent=studyTimeLabel(todayMin);$('todayStudyDetail').textContent=formatShortDate(todayKey());$('goalOrbit').style.setProperty('--pct',pct+'%');$('goalOrbitPercent').textContent=Math.round(pct)+'%';$('remaining100').textContent=studyTimeLabel(remaining);$('remainingDetail').textContent=formatShortDate(startKey)+'開始 ・ '+Math.round(pct)+'% 達成';$('daysTo100').textContent=pace.primary;$('paceDetail').textContent=pace.detail;$('bestDay').textContent=studyTimeLabel(best.minutes);$('bestDayDate').textContent=best.date?formatShortDate(best.date):'-';$('avgDay').textContent=studyTimeLabel(avgDay);$('avgDayDetail').textContent='目標開始日から今日まで';$('elapsedDays').textContent=elapsedDays+'日';$('elapsedDaysDetail').textContent=formatShortDate(startKey)+'から';$('streakDays').textContent=streak.current+'日';$('currentStreakDetail').textContent=streak.current>0?'目標期間で継続':'今日の記録なし';$('longestStreakDays').textContent=streak.longest+'日';$('longestStreakDetail').textContent=streak.longest?(streak.start===streak.end?formatShortDate(streak.start):formatShortDate(streak.start)+'〜'+formatShortDate(streak.end)):'-'}"
if old_render not in s:
    raise SystemExit('renderDashboard block not found')
s = s.replace(old_render, new_render, 1)

marker = '/* target-overflow-goal-status-v4 */'
if marker in s:
    raise SystemExit('v4 CSS already present')
css = r'''
/* target-overflow-goal-status-v4 */
.target-setting,.target-field{min-width:0!important;max-width:100%!important}
.target-start-field{overflow:hidden!important}
.target-date-wrap{display:flex!important;align-items:center!important;width:100%!important;min-width:0!important;max-width:100%!important;height:42px!important;min-height:42px!important;max-height:42px!important;padding:0!important;border:1px solid var(--line)!important;border-radius:10px!important;background:var(--surface)!important;overflow:hidden!important;box-sizing:border-box!important}
.target-date-wrap:focus-within{border-color:var(--blue)!important;box-shadow:0 0 0 3px rgba(37,99,235,.12)!important}
.target-date-wrap input{display:block!important;flex:1 1 auto!important;width:100%!important;min-width:0!important;max-width:100%!important;height:40px!important;min-height:40px!important;max-height:40px!important;margin:0!important;padding:0 10px!important;border:0!important;border-radius:0!important;background:transparent!important;box-shadow:none!important;box-sizing:border-box!important;-webkit-min-logical-width:0!important}
.dual-goal-status{display:grid!important;grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important;align-items:stretch!important;gap:14px!important}
.dual-goal-status .goal-status-item{display:flex!important;flex-direction:column!important;justify-content:center!important;min-width:0!important;gap:4px!important}
.dual-goal-status .goal-status-item strong{order:2!important;margin:0!important;font-size:22px!important;line-height:1.1!important}
.dual-goal-status .goal-status-item em{order:3!important}
.dual-goal-status .remaining-goal-status{align-items:flex-end!important;text-align:right!important}
.dual-goal-status .today-goal-status{align-items:flex-start!important;text-align:left!important}
@media(max-width:620px){
  .target-setting{grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important;overflow:hidden!important}
  .target-field,.target-control,.target-date-wrap{width:100%!important;min-width:0!important;max-width:100%!important}
  .dual-goal-status{grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important;gap:10px!important;padding:13px 14px!important}
  .dual-goal-status .goal-status-item span{font-size:11px!important;line-height:1.35!important}
  .dual-goal-status .goal-status-item strong{font-size:20px!important}
  .dual-goal-status .goal-status-item em{font-size:10px!important;line-height:1.35!important}
}
'''
if '</style>' not in s:
    raise SystemExit('style tag not found')
s = s.replace('</style>', css + '\n</style>', 1)
p.write_text(s, encoding='utf-8')

sw = Path('sw.js')
if sw.exists():
    sws = sw.read_text(encoding='utf-8')
    sws = sws.replace("study-tracker-pwa-v2", "study-tracker-pwa-v3")
    sw.write_text(sws, encoding='utf-8')
