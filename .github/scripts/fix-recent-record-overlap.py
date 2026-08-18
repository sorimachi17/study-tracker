from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

marker = '/* recent-record-overlap-fix-v11 */'
if marker in s:
    raise SystemExit('fix already applied')

css = r'''

/* recent-record-overlap-fix-v11 */
.recent-month-body{
  padding:10px 12px 12px;
  display:grid;
  gap:10px;
  background:var(--surface);
}
.recent-month-body .record-row{
  display:grid;
  grid-template-columns:minmax(0,1fr) auto;
  align-items:start;
  gap:12px;
  min-height:0;
  margin:0;
  padding:14px;
}
.recent-month-body .record-main{
  min-width:0;
  width:100%;
}
.recent-month-body .record-title{
  min-width:0;
}
.recent-month-body .record-meta,
.recent-month-body .record-note{
  max-width:100%;
  overflow-wrap:anywhere;
  word-break:break-word;
}
.recent-month-body .row-actions{
  align-self:start;
  flex:0 0 auto;
}
@media(max-width:620px){
  .recent-month-body{
    padding:10px 10px 12px;
    gap:9px;
  }
  .recent-month-body .record-row{
    gap:10px;
    padding:13px;
  }
}
'''

if '</style>' not in s:
    raise SystemExit('missing </style>')
s = s.replace('</style>', css + '\n</style>', 1)
p.write_text(s, encoding='utf-8')
