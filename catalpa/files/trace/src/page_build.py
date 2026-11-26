# Assembles ~/site/trace.html from page/trace.src.html, the four table fragments and the paragraph on readers,
# and copies the three figures to ~/site/img/. Run after page_tables.py and the three plot scripts.
import shutil
P = '/home/agent1/trace/page/'
s = open(P + 'trace.src.html', encoding='utf-8').read()
for tag, fn in (('<!--T_LATE-->', 't_late.html'), ('<!--T_PAIRS-->', 't_pairs.html'), ('<!--T_SAT-->', 't_sat.html'), ('<!--T_WAVE-->', 't_wave.html'), ('<!--READERS-->', 'readers.html')):
    assert s.count(tag) == 1, tag
    s = s.replace(tag, open(P + fn, encoding='utf-8').read().strip())
open('/home/agent1/site/trace.html', 'w', encoding='utf-8').write(s)
for a, b in (('pairs.png', 'trace-pairs.png'), ('hov.png', 'trace-hov.png'), ('wave.png', 'trace-wave.png')):
    shutil.copy('/home/agent1/trace/' + a, '/home/agent1/site/img/' + b)
print(len(s), 'bytes')
