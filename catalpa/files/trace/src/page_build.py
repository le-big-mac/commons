# Assembles ~/site/trace.html and ~/site/rise.html from page/trace.src.html and page/rise.src.html, the table
# fragments written by page_tables.py and the paragraphs on readers, and copies the three figures to ~/site/img/.
import shutil
P = '/home/agent1/trace/page/'
def build(src, out, tags):
    s = open(P + src, encoding='utf-8').read()
    for tag, fn in tags:
        assert s.count(tag) == 1, (src, tag, s.count(tag))
        s = s.replace(tag, open(P + fn, encoding='utf-8').read().strip())
    s = s.replace('<!--CHECK4-->', '').replace('<!--CHECK5-->', '').replace('<!--CHECK6-->', '').replace('<!--CHECK7-->', '').replace('<!--CHECK8-->', '').replace('<!--CHECK10-->', '').replace('<!--CHECK11-->', '').replace('<!--CHECK13-->', '')
    assert '<!--' not in s, (src, s[s.index('<!--'):s.index('<!--') + 40])
    open('/home/agent1/site/' + out, 'w', encoding='utf-8').write(s); print(out, len(s), 'bytes')
build('trace.src.html', 'trace.html', (('<!--T_LATE-->', 't_late.html'), ('<!--T_PAIRS-->', 't_pairs.html'), ('<!--T_SAT-->', 't_sat.html'), ('<!--READERS_A-->', 'readers_a.html')))
build('rise.src.html', 'rise.html', (('<!--T_WAVE-->', 't_wave.html'), ('<!--T_BUOYS-->', 't_buoys.html'), ('<!--T_POLO-->', 't_polo.html'), ('<!--T_PASSAGES-->', 't_passages.html'), ('<!--T_WINDSEA-->', 't_windsea.html'), ('<!--T_RISES-->', 't_rises.html'), ('<!--T_NORTH-->', 't_north.html'), ('<!--LIT2-->', 'lit2.html'), ('<!--READERS_B-->', 'readers_b.html')))
for a, b in (('pairs.png', 'trace-pairs.png'), ('hov.png', 'trace-hov.png'), ('wave.png', 'trace-wave.png')):
    shutil.copy('/home/agent1/trace/' + a, '/home/agent1/site/img/' + b)
