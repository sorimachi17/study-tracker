from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

marker = '/* record-sheet-stability-v2 */'
if marker not in s:
    css = r'''
/* record-sheet-stability-v2 */
.record-sheet input,
.record-sheet select,
.record-sheet textarea{box-sizing:border-box;width:100%;max-width:100%;min-width:0}
.record-sheet input[type="date"],
.record-sheet input[type="time"],
.record-sheet input[type="number"],
.record-sheet select{height:54px;min-height:54px;max-height:54px;padding:0 14px;border-radius:12px;font-size:16px;line-height:normal}
.record-sheet input[type="date"],
.record-sheet input[type="time"]{-webkit-appearance:none;appearance:none;-webkit-min-logical-width:0;overflow:hidden}
.record-sheet input[type="date"]::-webkit-date-and-time-value,
.record-sheet input[type="time"]::-webkit-date-and-time-value{display:flex;align-items:center;width:100%;height:52px;margin:0;padding:0;text-align:left}
.record-sheet .form-grid>div,
.record-sheet .time-grid>div{width:100%;max-width:100%;min-width:0}
.record-sheet textarea{min-height:104px;padding:13px 14px;border-radius:12px;font-size:16px}
body.record-scroll-lock{position:fixed;left:0;right:0;width:100%;overflow:hidden}
@media(max-width:620px){
  .record-sheet-backdrop{position:fixed;inset:0;width:100%;height:100%;padding:0;overflow:hidden;align-items:flex-end;justify-content:center}
  .record-sheet{position:absolute;left:0;right:0;bottom:0;width:100%;height:calc(100svh - max(env(safe-area-inset-top), 8px) - 8px);max-height:none;min-height:0;overflow-y:auto;overscroll-behavior:contain;-webkit-overflow-scrolling:touch;border-radius:22px 22px 0 0;padding:10px 16px calc(20px + env(safe-area-inset-bottom));transform:none}
  .record-sheet-head{position:sticky;top:-10px;z-index:5;background:var(--surface);padding:8px 0 10px;margin-bottom:10px}
  .record-sheet .form-grid,.record-sheet .time-grid{display:grid;grid-template-columns:minmax(0,1fr);gap:12px;width:100%}
  .record-sheet .quick-buttons{gap:8px}
  .record-sheet .quick-buttons .btn{min-height:44px}
  .record-sheet .save-row{position:static;background:none;padding-top:8px}
  .record-sheet .save-row .btn{height:54px;min-height:54px}
}
'''
    s = s.replace('</style>', css + '</style>', 1)

old_open = "function openRecordModal(){renderSelectedDay();setDefaultEntryEndTime();$('recordModal').classList.remove('hidden');document.body.classList.add('modal-open')}"
old_close = "function closeRecordModal(){$('recordModal').classList.add('hidden');document.body.classList.remove('modal-open')}"
new_open = "let recordModalScrollY=0;function openRecordModal(){renderSelectedDay();setDefaultEntryEndTime();recordModalScrollY=window.scrollY||window.pageYOffset||0;document.body.style.top=(-recordModalScrollY)+'px';document.body.classList.add('record-scroll-lock');$('recordModal').classList.remove('hidden');document.body.classList.add('modal-open')}"
new_close = "function closeRecordModal(){$('recordModal').classList.add('hidden');document.body.classList.remove('modal-open');document.body.classList.remove('record-scroll-lock');document.body.style.top='';window.scrollTo(0,recordModalScrollY)}"

if old_open in s:
    s = s.replace(old_open, new_open, 1)
elif 'let recordModalScrollY=0;function openRecordModal()' not in s:
    raise SystemExit('openRecordModal marker not found')

if old_close in s:
    s = s.replace(old_close, new_close, 1)
elif "document.body.classList.remove('record-scroll-lock')" not in s:
    raise SystemExit('closeRecordModal marker not found')

p.write_text(s, encoding='utf-8')
