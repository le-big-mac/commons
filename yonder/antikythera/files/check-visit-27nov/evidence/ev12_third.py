"""Third evidence reading: what the third candidate changes from the second, what it keeps of the public page,
and the few new figures. usage: python ev12_third.py PUBLIC CAND2 CAND3 RECORDS_DIR ; prints, writes nothing."""
import difflib, html, json, os, re, sys
pub, c2, c3 = (open(p, encoding='utf-8').read() for p in sys.argv[1:4])
R = sys.argv[4]
LONG_A = '<p class="small">What follows is the page as it stood until 25 November'
WHY_A, WHY_B = '<h2>Why 205 BC</h2>', '<h2>What is mine and what is not</h2>'
def between(s, a, b):
    i = s.index(a); return s[i:s.index(b, i)]
def text(h):
    h = re.sub(r'<img[^>]*alt="([^"]*)"[^>]*>', lambda m: ' [ALT: ' + m.group(1) + '] ', h)
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', h)).split())
def places(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return [(t, a[i1:i2], b[j1:j2]) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal']

print('=== kept parts, source letter for letter ===')
print('long account, public -> third candidate:', places(between(pub, LONG_A, '</details>'), between(c3, LONG_A, '</details>')))
print('"Why 205 BC", public -> third candidate:', places(between(pub, WHY_A, WHY_B), between(c3, WHY_A, WHY_B)))
print('"Why 205 BC", second -> third candidate identical:', between(c2, WHY_A, WHY_B) == between(c3, WHY_A, WHY_B))
m = re.search(r'The papers are listed at the foot of the page\. (Two more fresh copies of the model read this rewrite: .*?)</p>', pub, re.S)
sec3 = c3[c3.index('<details class="fold" id="how-this-page-was-written-and-read">'):]
print('the old account is in the new fold letter for letter:', m.group(1) in sec3)
print('alt texts identical in all three:', re.findall(r'alt="([^"]*)"', pub) == re.findall(r'alt="([^"]*)"', c3) == re.findall(r'alt="([^"]*)"', c2))

print('\n=== second -> third candidate, the whole page but the new fold, word by word ===')
cut = lambda s: text(s[:s.index('<details class="fold" id="how-this-page-was-written-and-read">')])
a, b = cut(c2).split(), cut(c3).split()
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
n = 0
for t, i1, i2, j1, j2 in sm.get_opcodes():
    if t == 'equal': continue
    n += 1
    print(f'[{n}] {t}: OLD[{" ".join(a[i1:i2])}]\n      NEW[{" ".join(b[j1:j2])}]\n      (after: ...{" ".join(b[max(0, j1 - 6):j1])})')

print('\n=== names and cautions with every fold shut: public, second, third ===')
def open_only(s):
    i = s.index('<details class="fold" id="for-those-who-want-to-check">') if 'id="for-those-who-want-to-check"' in s else s.index('<details class="fold">')
    top = s[:i]
    x, y = top.index(WHY_A), top.index(WHY_B)
    top = top[:x] + top[y:]
    top = re.sub(r'<details class="fold small-fold".*?</details>', lambda mm: re.search(r'<summary>.*?</summary>', mm.group(0)).group(0), top, flags=re.S)
    top = re.sub(r'<img[^>]*>', ' ', top)
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', top)).split())
op, o2, o3 = open_only(pub), open_only(c2), open_only(c3)
print('words:', len(op.split()), len(o2.split()), len(o3.split()))
for w in ('Carman and Evans', 'Freeth and Jones', 'Iversen and Jones', 'Efstathiou', 'three published studies', 'I cannot say why', 'reconstruction', 'reading of the marks', 'anticlockwise', '105°', 'keeper', '14° to 38°', 'twenty minutes'):
    print(f'   {w!r:26s} {op.count(w)}  {o2.count(w)}  {o3.count(w)}')

print('\n=== figures ===')
S = json.load(open(os.path.join(R, 'results-S.json')))
td = S['today']
print('on the day, planet minus pointer in size:', {k: round(abs(td[k]), 2) for k in ('mercury', 'venus', 'mars', 'jupiter', 'saturn')}, '-> the largest', round(max(abs(td[k]) for k in ('mercury', 'venus', 'mars', 'jupiter', 'saturn')), 2), '| the Sun', round(abs(td['sun']), 2))
lost = -S['drift']['moon']
print(f'the clock: lost {lost:.1f} deg = {lost / 30:.2f} hours of a twelve-hour dial; shows {360 - lost:.1f} deg = {(360 - lost) / 30:.2f} hours fast; on the day {td["moon"]:.1f} deg = {td["moon"] / 30:.2f} hours fast, which read back is {(360 - td["moon"]) / 30:.2f} hours lost')
print('the clock of the page: nine hours lost = 270 deg = 0.75 of a turn; three hours fast = 90 deg')
print('Venus then and now (run.out): 1.48 and 10.44; Saturn 4.97 and 9.26; ratios %.2f and %.2f' % (10.437 / 1.4818, 9.260 / 4.9654))
rate = abs(S['drift']['moon'] / S['years'])
print(f'the Moon: slow by {rate:.4f} deg a year; model alone 1.035 deg rms (largest 2.54); the slow running equals that after {1.035 / rate:.1f} years, when the two together are about {1.035 * 2 ** 0.5:.2f} deg rms; '
      f'10 deg after {10 / rate:.0f} years; a quarter turn after {90 / rate:.0f} years')
print('planet pointers when new (rms, run.out): Venus 1.5, Jupiter 3.7, Mercury 4.2, Saturn 5.0, Mars 9.6')
for y in (950, 1058, 914, 1112):
    print(f'   AD {y}: {2026 - y} years ago', end=';')
print()
