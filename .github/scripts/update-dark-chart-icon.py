from pathlib import Path
import re

svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" fill="#0e1524"/>
  <rect x="8" y="8" width="496" height="496" rx="104" fill="none" stroke="#223049" stroke-width="2"/>
  <rect x="92" y="326" width="58" height="88" rx="15" fill="#8bb8ff"/>
  <rect x="180" y="284" width="58" height="130" rx="15" fill="#73aaf9"/>
  <rect x="268" y="238" width="58" height="176" rx="15" fill="#5f9df5"/>
  <rect x="356" y="174" width="58" height="240" rx="15" fill="#3b82f6"/>
  <path d="M116 278 L204 230 L292 180 L388 104" fill="none" stroke="#60a5fa" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="116" cy="278" r="19" fill="#60a5fa"/>
  <circle cx="204" cy="230" r="19" fill="#60a5fa"/>
  <circle cx="292" cy="180" r="19" fill="#60a5fa"/>
  <circle cx="388" cy="104" r="19" fill="#60a5fa"/>
</svg>
'''
Path('app-icon.svg').write_text(svg, encoding='utf-8')

index = Path('index.html')
text = index.read_text(encoding='utf-8')
text, n = re.subn(r'app-icon-180\.png\?v=\d+', 'app-icon-180.png?v=4', text)
if n != 1:
    raise SystemExit(f'Expected 1 apple icon reference, got {n}')
index.write_text(text, encoding='utf-8')

manifest = Path('manifest.webmanifest')
m = manifest.read_text(encoding='utf-8')
m, n192 = re.subn(r'app-icon-192\.png\?v=\d+', 'app-icon-192.png?v=4', m)
m, n512 = re.subn(r'app-icon-512\.png\?v=\d+', 'app-icon-512.png?v=4', m)
if n192 != 1 or n512 != 1:
    raise SystemExit(f'Unexpected manifest icon refs: 192={n192}, 512={n512}')
manifest.write_text(m, encoding='utf-8')

sw = Path('sw.js')
s = sw.read_text(encoding='utf-8')
s, nsw = re.subn(r"study-tracker-pwa-v\d+", 'study-tracker-pwa-v4', s, count=1)
if nsw != 1:
    raise SystemExit(f'Expected 1 cache version, got {nsw}')
sw.write_text(s, encoding='utf-8')
