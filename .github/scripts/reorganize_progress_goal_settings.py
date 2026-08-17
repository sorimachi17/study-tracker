from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) Remove goal controls from progress header.
old = '''<div class="card progress-card"><div class="challenge-title"><h2>学習目標</h2><div class="target-setting"><div class="target-field"><label for="targetHoursInput">目標</label><div class="target-control target-inline"><input id="targetHoursInput" type="number" min="1" step="1" value="100" /><span>時間</span></div></div><div class="target-field target-start-field"><label for="targetStartDateInput">開始日</label><div class="target-control target-date-wrap"><input id="targetStartDateInput" type="date" /></div></div><button class="btn" id="saveTargetBtn" type="button">変更</button></div></div><div class="total-row total-metrics">'''
new = '''<div class="card progress-card"><div class="total-row total-metrics">'''
if old not in s:
    raise SystemExit('progress goal controls block not found')
s = s.replace(old, new, 1)

# 2) Replace remaining/elapsed block with the requested six KPI cards in the requested order.
old = '''<div class="goal-status dual-goal-status"><div class="goal-status-item today-goal-status"><span>今日の勉強時間の合計</span><strong id="todayStudyTotal">0分</strong><em id="todayStudyDetail">今日</em></div><div class="goal-status-item remaining-goal-status"><span id="targetRemainingLabel">目標までの残り学習時間</span><strong id="remaining100">100時間</strong><em id="remainingDetail">0% 達成</em></div></div><div class="milestones"><div class="milestone"><span>経過日数</span><strong id="elapsedDays">0日</strong><em id="elapsedDaysDetail">記録開始から</em></div><div class="milestone"><span>連続学習日数</span><strong id="streakDays">0日</strong><em id="currentStreakDetail">今日までの連続記録</em></div><div class="milestone"><span>最長連続勉強日数</span><strong id="longestStreakDays">0日</strong><em id="longestStreakDetail">これまでの最長</em></div><div class="milestone"><span>1日の平均学習時間</span><strong id="avgDay">0分</strong><em id="avgDayDetail">記録開始から今日まで</em></div><div class="milestone"><span>1日の最高学習時間</span><strong id="bestDay">0分</strong><em id="bestDayDate">-</em></div><div class="milestone prediction"><span id="targetPredictionLabel">到達予測</span><strong id="daysTo100">-</strong><em id="paceDetail">-</em></div></div>'''
new = '''<div class="milestones progress-summary-grid"><div class="milestone"><span>今日の勉強時間</span><strong id="todayStudyTotal">0分</strong><em id="todayStudyDetail">今日</em></div><div class="milestone"><span>1日の平均時間</span><strong id="avgDay">0分</strong><em id="avgDayDetail">目標開始日から今日まで</em></div><div class="milestone"><span>連続学習日数</span><strong id="streakDays">0日</strong><em id="currentStreakDetail">今日までの連続記録</em></div><div class="milestone"><span>最長連続日数</span><strong id="longestStreakDays">0日</strong><em id="longestStreakDetail">これまでの最長</em></div><div class="milestone"><span>1日の最高時間</span><strong id="bestDay">0分</strong><em id="bestDayDate">-</em></div><div class="milestone prediction"><span id="targetPredictionLabel">到達予測</span><strong id="daysTo100">-</strong><em id="paceDetail">-</em></div></div>'''
if old not in s:
    raise SystemExit('old KPI block not found')
s = s.replace(old, new, 1)

# 3) Move goal settings into a dedicated tab in Edit.
old = '''<section class="section-block"><div class="section-intro"><div class="section-intro-left"><span class="section-number">3</span><h2>編集</h2></div><p>記録・カテゴリを編集</p></div><section class="card card-pad"><div class="tabs"><button class="btn tab active" type="button" data-panel="recentPanel">最近</button><button class="btn tab" type="button" data-panel="categoryPanel">カテゴリ</button></div><div id="recentPanel"><div class="section-head"><h3>最近の記録</h3><span id="recentCount"></span></div><div class="list" id="recentList"></div></div><div id="categoryPanel" class="hidden"><div class="section-head"><h3>カテゴリ管理</h3><span>追加・並べ替え・削除</span></div><div class="entry-form"><div><label for="newCategoryInput">カテゴリ名</label><input id="newCategoryInput" type="text" placeholder="例: Conversation" /></div><button class="btn primary" id="addCategoryBtn" type="button">追加</button></div><div class="list" id="categoryList" style="margin-top:12px"></div></div></section></section></div>'''
new = '''<section class="section-block"><div class="section-intro"><div class="section-intro-left"><span class="section-number">3</span><h2>編集</h2></div><p>記録・カテゴリ・目標を編集</p></div><section class="card card-pad"><div class="tabs"><button class="btn tab active" type="button" data-panel="recentPanel">最近</button><button class="btn tab" type="button" data-panel="categoryPanel">カテゴリ</button><button class="btn tab" type="button" data-panel="targetPanel">目標</button></div><div id="recentPanel"><div class="section-head"><h3>最近の記録</h3><span id="recentCount"></span></div><div class="list" id="recentList"></div></div><div id="categoryPanel" class="hidden"><div class="section-head"><h3>カテゴリ管理</h3><span>追加・並べ替え・削除</span></div><div class="entry-form"><div><label for="newCategoryInput">カテゴリ名</label><input id="newCategoryInput" type="text" placeholder="例: Conversation" /></div><button class="btn primary" id="addCategoryBtn" type="button">追加</button></div><div class="list" id="categoryList" style="margin-top:12px"></div></div><div id="targetPanel" class="hidden"><div class="section-head"><h3>学習目標</h3><span>目標時間と開始日</span></div><div class="goal-settings-editor"><div class="goal-settings-field"><label for="targetHoursInput">目標時間</label><div class="goal-hours-control"><input id="targetHoursInput" type="number" min="1" step="1" value="100" /><span>時間</span></div></div><div class="goal-settings-field"><label for="targetStartDateInput">開始日</label><input id="targetStartDateInput" type="date" /></div><button class="btn primary" id="saveTargetBtn" type="button">目標を保存</button></div></div></section></section></div>'''
if old not in s:
    raise SystemExit('edit section not found')
s = s.replace(old, new, 1)

# 4) Add clean styles for the six-card KPI grid and goal editor.
css = r'''
/* progress-kpi-goal-editor-v5 */
.progress-summary-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important}
.goal-settings-editor{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr) auto;gap:12px;align-items:end;max-width:720px}
.goal-settings-field{min-width:0}
.goal-settings-field>label{margin-bottom:6px}
.goal-settings-field>input,.goal-hours-control{width:100%;height:46px;min-height:46px;box-sizing:border-box}
.goal-settings-field>input{display:block;min-width:0;padding:0 12px}
.goal-hours-control{display:flex;align-items:center;border:1px solid var(--line);border-radius:10px;background:var(--surface);overflow:hidden}
.goal-hours-control:focus-within{border-color:var(--blue);box-shadow:0 0 0 3px rgba(37,99,235,.12)}
.goal-hours-control input{flex:1;min-width:0;width:auto;height:44px;min-height:44px;border:0;border-radius:0;background:transparent;padding:0 12px;box-shadow:none!important}
.goal-hours-control span{flex:0 0 auto;padding-right:12px;color:var(--muted);font-size:11px;font-weight:850}
.goal-settings-editor>.btn{height:46px;min-height:46px;white-space:nowrap}
@media(max-width:620px){
  .progress-summary-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important}
  .goal-settings-editor{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
  .goal-settings-editor>.btn{grid-column:1/-1;width:100%}
  .goal-settings-field>input,.goal-hours-control{width:100%;min-width:0;max-width:100%}
}
'''
if '/* progress-kpi-goal-editor-v5 */' not in s:
    s = s.replace('</style>', css + '\n</style>', 1)

# 5) Update dashboard JS so it only writes to elements that remain.
old_start = "function renderDashboard(){"
old_end = "\nfunction chartDateLabel(d)"
start_idx = s.find(old_start)
end_idx = s.find(old_end, start_idx)
if start_idx < 0 or end_idx < 0:
    raise SystemExit('renderDashboard boundaries not found')
new_func = """function renderDashboard(){const totalMin=sumEntries(()=>true),todayMin=sumEntries(e=>e.date===todayKey()),goalMin=targetPeriodTotal(),targetMin=targetHours*60,pct=Math.min(100,goalMin/targetMin*100),remaining=Math.max(0,targetMin-goalMin),best=targetPeriodBestDay(),pace=targetPaceToGoal(remaining),avgDay=targetPeriodDailyAverage(),startKey=effectiveTargetStartDate(),streak=targetPeriodStreakStats();$('pageTitle').textContent='英語'+targetHours+'時間チャレンジ';$('targetHoursInput').value=targetHours;$('targetStartDateInput').value=startKey;$('targetPredictionLabel').textContent='到達予測';$('totalHours').textContent=Math.floor(totalMin/60)+'h';$('totalMinutes').textContent=minutesLabel(totalMin%60);$('targetPeriodHours').textContent=Math.floor(goalMin/60)+'h';$('targetPeriodMinutes').textContent=minutesLabel(goalMin%60);$('targetPeriodRange').textContent=formatShortDate(startKey)+'開始 ・ 目標 '+targetHours+'時間';$('todayStudyTotal').textContent=studyTimeLabel(todayMin);$('todayStudyDetail').textContent=formatShortDate(todayKey());$('goalOrbit').style.setProperty('--pct',pct+'%');$('goalOrbitPercent').textContent=Math.round(pct)+'%';$('daysTo100').textContent=pace.primary;$('paceDetail').textContent=pace.detail;$('bestDay').textContent=studyTimeLabel(best.minutes);$('bestDayDate').textContent=best.date?formatShortDate(best.date):'-';$('avgDay').textContent=studyTimeLabel(avgDay);$('avgDayDetail').textContent='目標開始日から今日まで';$('streakDays').textContent=streak.current+'日';$('currentStreakDetail').textContent=streak.current>0?'目標期間で継続':'今日の記録なし';$('longestStreakDays').textContent=streak.longest+'日';$('longestStreakDetail').textContent=streak.longest?(streak.start===streak.end?formatShortDate(streak.start):formatShortDate(streak.start)+'〜'+formatShortDate(streak.end)):'-'}"""
s = s[:start_idx] + new_func + s[end_idx:]

# 6) Include the goal panel in tab switching.
old = "['recentPanel','categoryPanel'].forEach(id=>$(id).classList.toggle('hidden',id!==tab.dataset.panel))"
new = "['recentPanel','categoryPanel','targetPanel'].forEach(id=>$(id).classList.toggle('hidden',id!==tab.dataset.panel))"
if old not in s:
    raise SystemExit('tab panel list not found')
s = s.replace(old, new, 1)

# Guard against visible/JS references that should be gone.
for forbidden in ["今日の勉強時間の合計", "1日の平均学習時間", "最長連続勉強日数", "1日の最高学習時間", "<span>経過日数</span>", "id=\"targetRemainingLabel\"", "id=\"remaining100\"", "id=\"elapsedDays\""]:
    if forbidden in s:
        raise SystemExit('forbidden old UI remains: ' + forbidden)

p.write_text(s, encoding='utf-8')
