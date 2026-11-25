# build.py -- page.src.html + rcore.js + data.json -> rhymes.html (one file, nothing fetched).   python -I build.py
import os
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n), encoding='utf-8').read()
src = rd('page.src.html'); assert src.count('/*CORE*/') == 1 and src.count('/*DATA*/[]') == 1
data = rd('data.json').replace('</', '<\\/')                       # a verse must not be able to close the script element
out = src.replace('/*CORE*/', rd('rcore.js')).replace('/*DATA*/[]', data)
open(os.path.join(here, 'rhymes.html'), 'w', encoding='utf-8').write(out); print('rhymes.html', len(out.encode('utf-8')), 'bytes')
