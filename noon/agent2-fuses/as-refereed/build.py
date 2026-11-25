# build.py -- page.src.html + core.js + landmarks.json -> fuse.html (one file, nothing fetched).   python -I build.py
import json, os
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n), encoding='utf-8').read()
land = json.loads(rd('landmarks.json'))
SUP = str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻')
notes = {  # what the page says where a figure was not computed here
  '5/2':  {'provedNote': 'not finished'},
  '11/4': {'provedNote': 'not run'},
  '23/8': {'meekNote': 'less than 2<sup>−N</sup> with N = 2↑↑9, a tower of nine twos (Xu’s table; not computed here)', 'provedNote': 'not run'},
  '3':    {'tame': 1541023937, 'tameNote': '(the paper’s figure; not computed here)', 'meekNote': 'smaller still', 'provedNote': 'not run'},
}
p52 = os.path.join(here, 'succ-5-2.out'); proved52 = None
if os.path.exists(p52):
    import re; m = re.search(r'above 5/2 is .*?; the gap is 2\^-(\d+);', rd('succ-5-2.out'))
    if m: proved52 = int(m.group(1))
for r in land:
    r.update(notes.get(r['r'], {}))
    if r['r'] == '5/2':
        if proved52: r['proved'] = proved52; r.pop('provedNote')
        else: r['provedNote'] = 'not finished'
src = rd('page.src.html'); assert src.count('/*CORE*/') == 1 and src.count('/*LANDMARKS*/[]') == 1
out = src.replace('/*CORE*/', rd('core.js')).replace('/*LANDMARKS*/[]', json.dumps(land, ensure_ascii=False))
open(os.path.join(here, 'fuse.html'), 'w', encoding='utf-8').write(out); print('fuse.html', len(out), 'bytes; proved gap at 5/2:', proved52)
