# build.py -- page.src.html + ocore.js -> peel.html (one file, nothing fetched).   python -I build.py
import os
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n), encoding='utf-8').read()
src = rd('page.src.html'); assert src.count('/*CORE*/') == 1
out = src.replace('/*CORE*/', rd('ocore.js')); open(os.path.join(here, 'peel.html'), 'w', encoding='utf-8').write(out); print('peel.html', len(out.encode('utf-8')), 'bytes')
