from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old_entry = '''      <div class="form-grid"><div><label for="dateInput">日付</label><input id="dateInput" type="date" required /></div><div><label for="categoryInput">カテゴリ</label><select id="categoryInput" required></select></div></div>
      <div class="time-grid"><div><label for="startTimeInput">開始時刻</label><input id="startTimeInput" type="time" /></div><div><label for="endTimeInput">終了時刻</label><input id="endTimeInput" type="time" /></div><div><label for="minutesInput">学習時間（分）</label><input id="minutesInput" type="number" min="1" step="1" placeholder="45" required /></div></div>
      <div class="quick-buttons">'''

new_entry = '''      <div class="form-grid"><div><label for="dateInput">日付</label><input id="dateInput" type="date" required /></div><div><label for="categoryInput">カテゴリ</label><select id="categoryInput" required></select></div></div>
      <div><label for="minutesInput">学習時間（分）</label><input id="minutesInput" type="number" min="1" step="1" placeholder="45" required /></div>
      <div class="quick-buttons">'''

if old_entry not in s:
    raise SystemExit('entry form field block not found')
s = s.replace(old_entry, new_entry, 1)

quick_end = '''<button class="btn" type="button" data-min="90">90分</button></div>
      <div><label for="noteInput">'''
quick_new = '''<button class="btn" type="button" data-min="90">90分</button></div>
      <div class="form-grid"><div><label for="startTimeInput">開始時刻</label><input id="startTimeInput" type="time" /></div><div><label for="endTimeInput">終了時刻</label><input id="endTimeInput" type="time" /></div></div>
      <div><label for="noteInput">'''
if quick_end not in s:
    raise SystemExit('quick buttons insertion point not found')
s = s.replace(quick_end, quick_new, 1)

old_edit = '''<div class="form-grid"><div><label for="editDateInput">日付</label><input id="editDateInput" type="date" required /></div><div><label for="editCategoryInput">カテゴリ</label><select id="editCategoryInput" required></select></div></div><div class="time-grid"><div><label for="editStartTimeInput">開始時刻</label><input id="editStartTimeInput" type="time" /></div><div><label for="editEndTimeInput">終了時刻</label><input id="editEndTimeInput" type="time" /></div><div><label for="editMinutesInput">学習時間</label><input id="editMinutesInput" type="number" min="1" step="1" required /></div></div>'''
new_edit = '''<div class="form-grid"><div><label for="editDateInput">日付</label><input id="editDateInput" type="date" required /></div><div><label for="editCategoryInput">カテゴリ</label><select id="editCategoryInput" required></select></div></div><div><label for="editMinutesInput">学習時間（分）</label><input id="editMinutesInput" type="number" min="1" step="1" required /></div><div class="form-grid"><div><label for="editStartTimeInput">開始時刻</label><input id="editStartTimeInput" type="time" /></div><div><label for="editEndTimeInput">終了時刻</label><input id="editEndTimeInput" type="time" /></div></div>'''
if old_edit in s:
    s = s.replace(old_edit, new_edit, 1)

p.write_text(s, encoding='utf-8')
