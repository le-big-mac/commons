# build.py -- page.src.html + gcore.js + data.json -> gasket.html (one file, nothing fetched).   python -I build.py
import os
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n), encoding='utf-8').read()
src = rd('page.src.html'); assert src.count('/*CORE*/') == 1 and src.count('/*DATA*/[]') == 1
out = src.replace('/*CORE*/', rd('gcore.js')).replace('/*DATA*/[]', rd('data.json'))
open(os.path.join(here, 'gasket.html'), 'w', encoding='utf-8').write(out); print('gasket.html', len(out), 'bytes')
