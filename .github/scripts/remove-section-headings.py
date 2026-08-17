from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

replacements = [
    (
        '<section class="section-block"><div class="section-intro"><div class="section-intro-left"><span class="section-number">1</span><h2>進捗を見る</h2></div><p>今どこまで積み上がったかを確認</p></div>\n<div class="card progress-card">',
        '<section class="section-block"><div class="card progress-card">'
    ),
    (
        '<section class="section-block"><div class="section-intro"><div class="section-intro-left"><span class="section-number">2</span><h2>履歴を見る</h2></div><p>日付ごとの学習履歴を確認</p></div>\n<section class="card card-pad">',
        '<section class="section-block"><section class="card card-pad">'
    ),
    (
        '<section class="section-block"><div class="section-intro"><div class="section-intro-left"><span class="section-number">3</span><h2>編集</h2></div><p>記録・カテゴリ・目標を編集</p></div><section class="card card-pad"><div class="tabs">',
        '<section class="section-block"><section class="card card-pad"><div class="section-head"><h2>編集</h2><span>記録・カテゴリ・目標</span></div><div class="tabs">'
    ),
]

for old, new in replacements:
    if old not in s:
        raise SystemExit('Expected block not found: ' + old[:120])
    s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
