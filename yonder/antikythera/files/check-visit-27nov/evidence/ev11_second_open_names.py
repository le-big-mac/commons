"""Second evidence reading: which scholars and which cautions stand in the open text (folds shut) of the public page
and of the second candidate. usage: python ev11_second_open_names.py PUBLIC CAND2 ; prints, writes nothing."""
import html, re, sys
pub, c2 = (open(p, encoding='utf-8').read() for p in sys.argv[1:3])
def open_only(s):
    i = s.index('<details class="fold" id="for-those-who-want-to-check">') if 'id="for-those-who-want-to-check"' in s else s.index('<details class="fold">')
    top = s[:i]
    a, b = top.index('<h2>Why 205 BC</h2>'), top.index('<h2>What is mine and what is not</h2>')
    top = top[:a] + top[b:]
    top = re.sub(r'<details class="fold small-fold".*?</details>', lambda m: re.search(r'<summary>.*?</summary>', m.group(0)).group(0), top, flags=re.S)
    top = re.sub(r'<img[^>]*>', ' ', top)
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', top)).split())
op, o2 = open_only(pub), open_only(c2)
print('words in the open text with every fold shut: public', len(op.split()), '| second candidate', len(o2.split()))
for w in ('Freeth', 'Carman and Evans', 'Freeth and Jones', 'Iversen and Jones', 'Efstathiou', 'Jones', 'three published studies', 'old knowledge', 'I cannot say why',
          'happen to cancel', 'kind', 'those papers', 'checked by no person', 'reconstruct', 'no finding of mine', 'share my training', 'anywhere on Earth', 'longer account',
          'keeper', 'by the stars', 'same stars', 'counted generously', 'counted strictly'):
    print(f'   {w!r:28s} public {op.count(w)}   second candidate {o2.count(w)}')
i = o2.index('Very little here is new')
print('\nthe second candidate, folds shut, from "Very little here is new":\n  ', o2[i:i + 330], '...')
