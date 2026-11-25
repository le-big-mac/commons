# build.py -- page.src.html + pcore.js + best.json -> change.html (one file, nothing fetched).   python -I build.py
import os, json
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n), encoding='utf-8').read()
src = rd('page.src.html'); assert src.count('/*CORE*/') == 1 and src.count('/*BEST*/null') == 1
best = json.loads(rd('best.json'))
out = src.replace('/*CORE*/', rd('pcore.js')).replace('/*BEST*/null', json.dumps(best, separators=(',', ':')))
open(os.path.join(here, 'change.html'), 'w', encoding='utf-8').write(out); print('change.html', len(out.encode('utf-8')), 'bytes')
