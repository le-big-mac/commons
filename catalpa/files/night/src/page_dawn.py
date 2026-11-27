# Assembles ~/site/dawn.html from page/dawn.src.html, the two folds kept beside it and the four-year station table
# written by src/four_years.py, and copies the page's four pictures into the site folder.
B = '/home/agent1/night/'
s = open(B + 'page/dawn.src.html', encoding='utf-8').read()
for tag, fn in (('<!--T_STATIONS4-->', 't_stations4.html'), ('<!--FOLD_2025-->', 'page/fold_2025.html'), ('<!--FOLD_STARS-->', 'page/fold_stars.html')):
    assert s.count(tag) == 1, tag; s = s.replace(tag, open(B + fn, encoding='utf-8').read().strip())
for tag in ('<!--READERS-->',): s = s.replace(tag, '')
assert '<!--' not in s, s[s.index('<!--'):s.index('<!--') + 60]
open('/home/agent1/site/dawn.html', 'w', encoding='utf-8').write(s); print('dawn.html', len(s), 'bytes')
import shutil
for f in ('dawn-tenths-4y.png', 'dawn-places-4y.png', 'dawn-towns.png', 'dawn-stars.png'): shutil.copy(B + 'img/' + f, '/home/agent1/site/img/' + f)
print('pictures copied to the site folder')
