from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

if 'pwa-head-v1' not in s:
    s=s.replace('<meta name="viewport" content="width=device-width,initial-scale=1" />','<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />',1)
    head='''\n<!-- pwa-head-v1 -->\n<meta name="theme-color" content="#0e1524" />\n<meta name="mobile-web-app-capable" content="yes" />\n<meta name="apple-mobile-web-app-capable" content="yes" />\n<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />\n<meta name="apple-mobile-web-app-title" content="Study Tracker" />\n<link rel="manifest" href="./manifest.webmanifest" />\n<link rel="icon" href="./app-icon.svg" type="image/svg+xml" />\n<link rel="apple-touch-icon" href="./app-icon.svg" />\n'''
    s=s.replace('<title>Study Tracker</title>','<title>Study Tracker</title>'+head,1)

if 'pwa-standalone-css-v1' not in s:
    css='''\n/* pwa-standalone-css-v1 */\nbody.standalone-app{overscroll-behavior-y:none}\nbody.standalone-app .app-shell{padding-top:calc(28px + env(safe-area-inset-top));padding-bottom:calc(78px + env(safe-area-inset-bottom))}\n@media(max-width:620px){body.standalone-app .app-shell{padding-top:calc(18px + env(safe-area-inset-top));padding-bottom:calc(86px + env(safe-area-inset-bottom))}}\n'''
    s=s.replace('</style>',css+'</style>',1)

if 'pwa-runtime-v1' not in s:
    js='''\n/* pwa-runtime-v1 */\nconst runningStandalone=window.matchMedia('(display-mode: standalone)').matches||window.navigator.standalone===true;\nif(runningStandalone)document.body.classList.add('standalone-app');\nif('serviceWorker' in navigator){window.addEventListener('load',()=>{navigator.serviceWorker.register('./sw.js').catch(()=>{})})}\n'''
    s=s.replace('</script>',js+'</script>',1)

p.write_text(s,encoding='utf-8')
