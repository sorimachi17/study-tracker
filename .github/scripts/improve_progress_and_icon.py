from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Update Apple touch icon to PNG and keep SVG favicon.
s = s.replace('<link rel="apple-touch-icon" href="./app-icon.svg" />', '<link rel="apple-touch-icon" sizes="180x180" href="./app-icon-180.png?v=2" />', 1)

# Replace target controls + summary layout.
old = '''<div class="card progress-card"><div class="challenge-title"><h2>これまでの累計学習時間</h2><div class="target-setting"><div class="target-field"><label for="targetHoursInput">目標</label><div class="target-inline"><input id="targetHoursInput" type="number" min="1" step="1" value="100" /><span>時間</span></div></div><div class="target-field target-start-field"><label for="targetStartDateInput">開始日</label><input id="targetStartDateInput" type="date" /></div><button class="btn" id="saveTargetBtn" type="button">変更</button></div></div><div class="total-row"><div class="total-hours"><span id="totalHours">0h</span> <small id="totalMinutes">0m</small></div><div class="goal-orbit" id="goalOrbit"><div><strong id="goalOrbitPercent">0%</strong><span>進捗</span></div></div></div>'''
new = '''<div class="card progress-card"><div class="challenge-title"><h2>学習目標</h2><div class="target-setting"><div class="target-field"><label for="targetHoursInput">目標</label><div class="target-control target-inline"><input id="targetHoursInput" type="number" min="1" step="1" value="100" /><span>時間</span></div></div><div class="target-field target-start-field"><label for="targetStartDateInput">開始日</label><input class="target-control target-date-control" id="targetStartDateInput" type="date" /></div><button class="btn" id="saveTargetBtn" type="button">変更</button></div></div><div class="total-row total-metrics"><div class="total-metric overall-total"><span class="total-metric-label">全期間の累計学習時間</span><div class="total-hours"><span id="totalHours">0h</span> <small id="totalMinutes">0m</small></div><em>すべての学習記録</em></div><div class="total-metric target-period-total"><div class="target-period-content"><div><span class="total-metric-label">目標開始日からの累計学習時間</span><div class="target-period-hours"><span id="targetPeriodHours">0h</span> <small id="targetPeriodMinutes">0m</small></div></div><div class="goal-orbit" id="goalOrbit"><div><strong id="goalOrbitPercent">0%</strong><span>進捗</span></div></div></div><em id="targetPeriodRange">開始日から現在まで</em></div></div>'''
if old not in s:
    raise SystemExit('progress summary block not found')
s = s.replace(old, new, 1)

# Replace old target-start styling with unified inputs and dual cumulative cards.
old_css = '''/* target-start-date-v1 */
.target-setting{align-items:flex-end}.target-field{display:flex;flex-direction:column;gap:4px}.target-field label{margin:0}.target-inline{display:flex;align-items:center;gap:6px}.target-start-field input{width:142px;min-height:36px;padding:6px 8px}.target-setting .target-inline input{width:78px}.target-start-note{color:var(--muted);font-size:10px;font-weight:750}
@media(max-width:620px){.target-setting{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr) auto;align-items:end;gap:8px}.target-setting .target-inline input,.target-start-field input{width:100%;min-width:0}.target-setting .btn{min-width:58px}}
'''
new_css = '''/* target-start-date-v2 */
.target-setting{align-items:flex-end}.target-field{display:flex;flex-direction:column;gap:5px}.target-field label{margin:0}.target-control{width:150px!important;height:42px!important;min-height:42px!important;box-sizing:border-box}.target-inline{display:flex;align-items:center;gap:4px;border:1px solid var(--line);border-radius:10px;background:var(--surface);overflow:hidden}.target-inline:focus-within{border-color:var(--blue);box-shadow:0 0 0 3px rgba(37,99,235,.12)}.target-setting .target-inline input{flex:1;width:auto!important;min-width:0;height:40px!important;min-height:40px!important;border:0!important;border-radius:0;background:transparent;padding:0 8px;box-shadow:none!important}.target-inline span{padding-right:9px;color:var(--muted);font-size:11px;font-weight:850;white-space:nowrap}.target-start-field input{padding:0 9px!important;line-height:normal}.target-setting .btn{height:42px;min-height:42px}.total-metrics{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:10px;align-items:stretch}.total-metric{min-width:0;padding:16px;border:1px solid var(--line);border-radius:14px;background:var(--surface2)}.total-metric-label{display:block;color:var(--muted);font-size:11px;font-weight:900;margin-bottom:8px}.total-metric .total-hours,.target-period-hours{font-size:clamp(36px,5vw,58px);line-height:1;font-weight:900;letter-spacing:-.05em}.total-metric .total-hours small,.target-period-hours small{font-size:16px;color:var(--muted);font-weight:850;letter-spacing:0}.total-metric>em,.target-period-total>em{display:block;margin-top:8px;color:var(--muted);font-size:10px;font-style:normal;font-weight:750}.target-period-total{background:var(--blueSoft)}.target-period-content{display:flex;align-items:center;justify-content:space-between;gap:14px}.target-period-content>div:first-child{min-width:0}.target-period-total .goal-orbit{width:88px}.target-period-total .goal-orbit strong{font-size:20px}.target-period-total .goal-orbit span{font-size:10px}
@media(max-width:620px){.target-setting{display:grid;grid-template-columns:1fr 1fr;align-items:end;gap:8px;width:100%}.target-control{width:100%!important}.target-setting .btn{grid-column:1/-1;width:100%}.total-metrics{grid-template-columns:1fr}.total-metric{padding:14px}.total-metric .total-hours,.target-period-hours{font-size:42px}.target-period-total .goal-orbit{width:82px}}
'''
if old_css not in s:
    raise SystemExit('target start css block not found')
s = s.replace(old_css, new_css, 1)

# Update dashboard renderer so both totals are visible.
pattern = r"function renderDashboard\(\)\{.*?\}\nfunction chartDateLabel"
m = re.search(pattern, s, flags=re.S)
if not m:
    raise SystemExit('renderDashboard block not found')
new_dashboard = '''function renderDashboard(){const totalMin=sumEntries(()=>true),goalMin=targetPeriodTotal(),targetMin=targetHours*60,pct=Math.min(100,goalMin/targetMin*100),remaining=Math.max(0,targetMin-goalMin),best=targetPeriodBestDay(),pace=targetPaceToGoal(remaining),avgDay=targetPeriodDailyAverage(),startKey=effectiveTargetStartDate(),start=parseDate(startKey),today=parseDate(todayKey()),streak=targetPeriodStreakStats(),elapsedDays=start<=today?Math.max(0,Math.floor((today-start)/DAY_MS)):0;$('pageTitle').textContent='英語'+targetHours+'時間チャレンジ';$('targetHoursInput').value=targetHours;$('targetStartDateInput').value=startKey;$('targetRemainingLabel').textContent='目標（'+targetHours+'時間）までの残り学習時間';$('targetPredictionLabel').textContent='到達予測';$('totalHours').textContent=Math.floor(totalMin/60)+'h';$('totalMinutes').textContent=minutesLabel(totalMin%60);$('targetPeriodHours').textContent=Math.floor(goalMin/60)+'h';$('targetPeriodMinutes').textContent=minutesLabel(goalMin%60);$('targetPeriodRange').textContent=formatShortDate(startKey)+'開始 ・ 目標 '+targetHours+'時間';$('goalOrbit').style.setProperty('--pct',pct+'%');$('goalOrbitPercent').textContent=Math.round(pct)+'%';$('remaining100').textContent=studyTimeLabel(remaining);$('remainingDetail').textContent=formatShortDate(startKey)+'開始 ・ '+Math.round(pct)+'% 達成';$('daysTo100').textContent=pace.primary;$('paceDetail').textContent=pace.detail;$('bestDay').textContent=studyTimeLabel(best.minutes);$('bestDayDate').textContent=best.date?formatShortDate(best.date):'-';$('avgDay').textContent=studyTimeLabel(avgDay);$('avgDayDetail').textContent='目標開始日から今日まで';$('elapsedDays').textContent=elapsedDays+'日';$('elapsedDaysDetail').textContent=formatShortDate(startKey)+'から';$('streakDays').textContent=streak.current+'日';$('currentStreakDetail').textContent=streak.current>0?'目標期間で継続':'今日の記録なし';$('longestStreakDays').textContent=streak.longest+'日';$('longestStreakDetail').textContent=streak.longest?(streak.start===streak.end?formatShortDate(streak.start):formatShortDate(streak.start)+'〜'+formatShortDate(streak.end)):'-'}
function chartDateLabel'''
s = s[:m.start()] + new_dashboard + s[m.end():]

p.write_text(s, encoding='utf-8')

# New app icon: clear at small sizes, progress-ring + rising study bars.
Path('app-icon.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="bg" x1="72" y1="48" x2="448" y2="464" gradientUnits="userSpaceOnUse">
      <stop stop-color="#2563EB"/>
      <stop offset="1" stop-color="#4F46E5"/>
    </linearGradient>
    <linearGradient id="accent" x1="174" y1="326" x2="345" y2="184" gradientUnits="userSpaceOnUse">
      <stop stop-color="#A7F3D0"/>
      <stop offset="1" stop-color="#FFFFFF"/>
    </linearGradient>
  </defs>
  <rect width="512" height="512" rx="116" fill="url(#bg)"/>
  <circle cx="256" cy="256" r="154" fill="none" stroke="#FFFFFF" stroke-opacity=".18" stroke-width="26"/>
  <path d="M256 102a154 154 0 0 1 149 116" fill="none" stroke="#FFFFFF" stroke-width="26" stroke-linecap="round"/>
  <path d="M107 286a154 154 0 0 0 77 99" fill="none" stroke="#A7F3D0" stroke-width="26" stroke-linecap="round"/>
  <rect x="160" y="278" width="46" height="72" rx="14" fill="#FFFFFF" fill-opacity=".74"/>
  <rect x="233" y="234" width="46" height="116" rx="14" fill="#FFFFFF" fill-opacity=".88"/>
  <rect x="306" y="184" width="46" height="166" rx="14" fill="url(#accent)"/>
  <path d="M166 218l48 44 91-92" fill="none" stroke="#FFFFFF" stroke-width="24" stroke-linecap="round" stroke-linejoin="round"/>
</svg>\n''', encoding='utf-8')

Path('manifest.webmanifest').write_text('''{
  "name": "Study Tracker",
  "short_name": "Study Tracker",
  "description": "英語学習時間を記録・振り返るためのStudy Tracker",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "background_color": "#0e1524",
  "theme_color": "#2563eb",
  "orientation": "portrait-primary",
  "icons": [
    {"src":"./app-icon-192.png?v=2","sizes":"192x192","type":"image/png","purpose":"any maskable"},
    {"src":"./app-icon-512.png?v=2","sizes":"512x512","type":"image/png","purpose":"any maskable"}
  ]
}
''', encoding='utf-8')

Path('sw.js').write_text("""const CACHE_NAME='study-tracker-pwa-v2';
const APP_SHELL=['./','./index.html','./manifest.webmanifest','./app-icon.svg','./app-icon-180.png','./app-icon-192.png','./app-icon-512.png'];

self.addEventListener('install',event=>{
  event.waitUntil(caches.open(CACHE_NAME).then(cache=>cache.addAll(APP_SHELL)));
  self.skipWaiting();
});

self.addEventListener('activate',event=>{
  event.waitUntil(
    caches.keys().then(keys=>Promise.all(keys.filter(key=>key!==CACHE_NAME).map(key=>caches.delete(key))))
      .then(()=>self.clients.claim())
  );
});

self.addEventListener('fetch',event=>{
  if(event.request.method!=='GET'||new URL(event.request.url).origin!==self.location.origin)return;
  event.respondWith(
    fetch(event.request)
      .then(response=>{
        const copy=response.clone();
        caches.open(CACHE_NAME).then(cache=>cache.put(event.request,copy));
        return response;
      })
      .catch(()=>caches.match(event.request).then(hit=>hit||caches.match('./index.html')))
  );
});
""", encoding='utf-8')
