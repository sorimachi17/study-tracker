from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

replacements = [
    (
        '.record-layout{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(300px,.65fr);gap:14px;align-items:start}',
        '.record-layout{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(300px,.65fr);gap:14px;align-items:stretch}.record-layout>.card{height:100%}'
    ),
    (
        '<div><label for="sentenceInput">覚えた英文</label><textarea id="sentenceInput" placeholder="例: I have no firm answer regarding this matter yet."></textarea></div>',
        ''
    ),
    (
        '<p>日付・記録・英文・カテゴリを確認</p>',
        '<p>日付・記録・カテゴリを確認</p>'
    ),
    (
        '<button class="btn tab" type="button" data-panel="sentencePanel">英文</button>',
        ''
    ),
    (
        '<div id="sentencePanel" class="hidden"><div class="section-head"><h3>覚えた英文</h3><span id="sentenceCount"></span></div><div class="list" id="sentenceList"></div></div>',
        ''
    ),
    (
        '<div><label for="editSentenceInput">覚えた英文</label><textarea id="editSentenceInput"></textarea></div>',
        ''
    ),
    (
        'renderCalendar();renderRecent();renderSentences();renderSelectedDay();renderCategories();',
        'renderCalendar();renderRecent();renderSelectedDay();renderCategories();'
    ),
    (
        "const date=$('dateInput').value||todayKey(),category=$('categoryInput').value,minutes=Number($('minutesInput').value),startTime=$('startTimeInput').value,endTime=$('endTimeInput').value,sentence=$('sentenceInput').value.trim(),note=$('noteInput').value.trim();",
        "const date=$('dateInput').value||todayKey(),category=$('categoryInput').value,minutes=Number($('minutesInput').value),startTime=$('startTimeInput').value,endTime=$('endTimeInput').value,note=$('noteInput').value.trim();"
    ),
    (
        "entries.push({id:String(Date.now())+'-'+Math.random().toString(16).slice(2),date,category,minutes,startTime,endTime,sentence,note,createdAt:Date.now()});",
        "entries.push({id:String(Date.now())+'-'+Math.random().toString(16).slice(2),date,category,minutes,startTime,endTime,sentence:'',note,createdAt:Date.now()});"
    ),
    (
        "$('sentenceInput').value='';",
        ''
    ),
    (
        "$('editSentenceInput').value=e.sentence||'';",
        ''
    ),
    (
        "e.sentence=$('editSentenceInput').value.trim();",
        ''
    ),
    (
        "['recentPanel','sentencePanel','categoryPanel'].forEach(id=>$(id).classList.toggle('hidden',id!==tab.dataset.panel))",
        "['recentPanel','categoryPanel'].forEach(id=>$(id).classList.toggle('hidden',id!==tab.dataset.panel))"
    ),
]

for old, new in replacements:
    if old not in s:
        raise SystemExit(f'target not found: {old[:120]}')
    s = s.replace(old, new, 1)

old_record = "function recordTemplate(e){const range=timeRangeLabel(e),note=cleanRecordNote(e),meta=e.date+' ・ '+(range?'時間帯 '+range:'時間帯 未入力'),sentence=String(e.sentence||'').trim();return'<div class=\"record-row\"><div class=\"record-main\"><div class=\"record-title\"><span class=\"pill\">'+escapeHtml(e.category)+'</span><span class=\"duration-label\">学習時間 '+minutesLabel(e.minutes)+'</span></div><div class=\"record-meta\">'+escapeHtml(meta)+'</div>'+(sentence?'<div class=\"sentence-box\">'+escapeHtml(sentence)+'</div>':'')+(note?'<div class=\"record-note\">'+escapeHtml(note)+'</div>':'')+'</div><div class=\"row-actions\"><button class=\"btn icon-btn\" data-edit=\"'+escapeHtml(e.id)+'\">編集</button></div></div>'}"
new_record = "function recordTemplate(e){const range=timeRangeLabel(e),note=cleanRecordNote(e),meta=e.date+' ・ '+(range?'時間帯 '+range:'時間帯 未入力');return'<div class=\"record-row\"><div class=\"record-main\"><div class=\"record-title\"><span class=\"pill\">'+escapeHtml(e.category)+'</span><span class=\"duration-label\">学習時間 '+minutesLabel(e.minutes)+'</span></div><div class=\"record-meta\">'+escapeHtml(meta)+'</div>'+(note?'<div class=\"record-note\">'+escapeHtml(note)+'</div>':'')+'</div><div class=\"row-actions\"><button class=\"btn icon-btn\" data-edit=\"'+escapeHtml(e.id)+'\">編集</button></div></div>'}"
if old_record not in s:
    raise SystemExit('recordTemplate target not found')
s = s.replace(old_record, new_record, 1)

p.write_text(s, encoding='utf-8')
