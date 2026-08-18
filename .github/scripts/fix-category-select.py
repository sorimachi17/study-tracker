from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

repls = [
    ('<input id="categoryInput" type="text" autocomplete="off" autocapitalize="none" placeholder="例: Conversation" required />',
     '<select id="categoryInput" required></select>'),
    ('<input id="editCategoryInput" type="text" autocomplete="off" autocapitalize="none" required />',
     '<select id="editCategoryInput" required></select>'),
    ('function renderCategorySelect(){}',
     '''function renderCategorySelect(){const recordSelect=$(\'categoryInput\'),editSelect=$(\'editCategoryInput\'),recordValue=recordSelect?recordSelect.value:\'\',editValue=editSelect?editSelect.value:\'\',options=categories.map(c=>\'<option value="\'+escapeHtml(c)+\'">\'+escapeHtml(c)+\'</option>\').join(\'\');if(recordSelect){recordSelect.innerHTML=options;if(categories.includes(recordValue))recordSelect.value=recordValue}if(editSelect){editSelect.innerHTML=options;if(categories.includes(editValue))editSelect.value=editValue}}'''),
    ("let recordModalScrollY=0;function openRecordModal(){renderSelectedDay();setDefaultEntryEndTime();",
     "let recordModalScrollY=0;function openRecordModal(){renderCategorySelect();renderSelectedDay();setDefaultEntryEndTime();"),
    ("['categoryInput','newCategoryInput','editCategoryInput','targetHoursInput'].forEach(id=>{",
     "['newCategoryInput','targetHoursInput'].forEach(id=>{")
]

for old, new in repls:
    if old not in s:
        raise SystemExit(f'missing expected text: {old[:100]}')
    s = s.replace(old, new, 1)

style = '''\n\n/* category-select-fix-v10 */\n#categoryInput,#editCategoryInput{\n  -webkit-appearance:auto!important;\n  appearance:auto!important;\n  user-select:auto!important;\n  touch-action:auto!important;\n  cursor:pointer;\n}\n'''
if '/* category-select-fix-v10 */' not in s:
    if '</style>' not in s:
        raise SystemExit('missing </style>')
    s = s.replace('</style>', style + '\n</style>', 1)

p.write_text(s, encoding='utf-8')
