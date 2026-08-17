from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '/* target-field-alignment-v3 */'
if marker in s:
    raise SystemExit('alignment patch already applied')
css = r'''
/* target-field-alignment-v3 */
.target-setting{align-items:end!important}
.target-field{display:grid!important;grid-template-rows:16px 42px!important;gap:6px!important;align-self:end!important;min-width:0!important}
.target-field label{display:block!important;height:16px!important;min-height:16px!important;max-height:16px!important;line-height:16px!important;margin:0!important;padding:0!important}
.target-control{height:42px!important;min-height:42px!important;max-height:42px!important;box-sizing:border-box!important}
.target-inline{display:flex!important;align-items:center!important;overflow:hidden!important;padding:0!important}
.target-setting .target-inline input{height:40px!important;min-height:40px!important;max-height:40px!important;line-height:40px!important;padding:0 10px!important;margin:0!important;box-sizing:border-box!important;-webkit-appearance:none!important;appearance:none!important}
.target-inline span{display:flex!important;align-items:center!important;height:40px!important;min-height:40px!important;max-height:40px!important;line-height:40px!important;padding:0 10px 0 0!important;margin:0!important;box-sizing:border-box!important}
.target-start-field input{display:block!important;height:42px!important;min-height:42px!important;max-height:42px!important;line-height:42px!important;padding:0 10px!important;margin:0!important;box-sizing:border-box!important}
.target-setting .btn{height:42px!important;min-height:42px!important;max-height:42px!important;align-self:end!important}
@media(max-width:620px){
  .target-setting{display:grid!important;grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important;grid-template-rows:auto 42px!important;column-gap:8px!important;row-gap:10px!important;align-items:end!important;width:100%!important}
  .target-field{grid-template-rows:16px 42px!important;width:100%!important;align-self:end!important}
  .target-control,.target-start-field input{width:100%!important}
  .target-setting .btn{grid-column:1/-1!important;grid-row:2!important;width:100%!important;margin:0!important}
}
'''
if '</style>' not in s:
    raise SystemExit('style closing tag not found')
s = s.replace('</style>', css + '\n</style>', 1)
p.write_text(s, encoding='utf-8')
