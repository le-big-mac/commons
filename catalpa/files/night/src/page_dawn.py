# Assembles ~/site/dawn.html from page/dawn.src.html and the station table written by src/dawn_recheck.py.
p = '/home/agent1/night/page/dawn.src.html'; s = open(p, encoding='utf-8').read()
s = s.replace('<!--T_STATIONS-->', open('/home/agent1/night/t_stations.html', encoding='utf-8').read().strip())
for tag in ('<!--READERS-->',): s = s.replace(tag, '')
assert '<!--' not in s
open('/home/agent1/site/dawn.html', 'w', encoding='utf-8').write(s); print('dawn.html', len(s), 'bytes')
import shutil
for f in ('dawn-tenths.png', 'dawn-places.png'): shutil.copy('/home/agent1/night/img/' + f, '/home/agent1/site/img/' + f)
print('pictures copied to the site folder')
