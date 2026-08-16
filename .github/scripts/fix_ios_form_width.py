from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '/* ios-form-width-fix-v1 */'
if marker not in s:
    css = '''\n/* ios-form-width-fix-v1 */\n.form-grid>div,.time-grid>div{min-width:0}\ninput[type="date"],input[type="time"],input[type="number"],select{width:100%;min-width:0;max-width:100%;box-sizing:border-box}\ninput[type="date"],input[type="time"]{-webkit-min-logical-width:0;display:block}\ninput[type="date"]::-webkit-date-and-time-value,input[type="time"]::-webkit-date-and-time-value{text-align:left;margin:0}\n@media(max-width:620px){\n  .form-grid>div,.time-grid>div{width:100%;min-width:0;max-width:100%}\n  input[type="date"],input[type="time"],input[type="number"],select{width:100%;min-width:0;max-width:100%;display:block}\n}\n'''
    s = s.replace('</style>', css + '</style>', 1)
    p.write_text(s, encoding='utf-8')
