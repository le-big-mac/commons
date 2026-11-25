"""After the second reader's report (check-2.md): my own recomputation of the new numbers it gives, before using them.
usage: after_check2.py CATDIR [CATDIR ...]   (under -I through runpy)"""
import sys, os, re, glob, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import dial, ij2019
pat = re.compile(r'^\s*(\d{5})\s+(-?\d{4})\s+([A-Z][a-z]{2})\s+(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\s+(-?\d+)\s+(-?\d+)\s+(\d+)\s+(\S+)\s+\S+\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)(?:\s+(-?\d+\.\d+))?')
def read_cat(prefix, add):
    rows = {}
    for f in sorted(f for d in sys.argv[1:] for f in glob.glob(os.path.join(d, prefix + '*.html'))):
        for line in open(f, encoding='utf-8', errors='replace'):
            m = pat.match(re.sub(r'<[^>]*>', '', line))
            if m: rows[int(m.group(9)) + add] = dict(kind=m.group(11)[0], gamma=float(m.group(12)), mag=float(m.group(13)), umag=float(m.group(14)) if m.group(14) else None,
                                                      y=int(m.group(2)), date=f'{int(m.group(2))} {m.group(3)} {m.group(4)}')
    return rows
def year_of(k):
    jd = 1646679.21 + 29.530589 * k
    return 1 - math.floor(-4712 + (jd + 0.5) / 365.25)
bc = lambda y: f'{1 - y} BC' if y <= 0 else f'AD {y}'
LE, SE = read_cat('LE', 27257), read_cat('SE', 27256)
fl, fs = dial.glyph_months(); L, S = sorted(fl), sorted(fs)
K = [k for k in range(-1250, 2700) if 1 <= year_of(k) <= 300]
sc = {}
for k in K:
    sc[k] = (sum(k + n in LE for n in L), sum(k + n in SE for n in S), sum(1 for n in range(1, 224) if k + n in LE and LE[k + n]['kind'] in 'PT' and n not in L),
             sum(1 for n in range(1, 224) if k + n in SE and SE[k + n]['gamma'] > 0 and n not in S))
tot = [sc[k][0] + sc[k][1] for k in K]; n = len(K)
print(f'1. of {n} starts: A + S = 0 in {sum(t == 0 for t in tot)} ({100 * sum(t == 0 for t in tot) / n:.1f}%); 33 or more in {sum(t >= 33 for t in tot)} ({100 * sum(t >= 33 for t in tot) / n:.1f}%); '
      f'60 or more in {sum(t >= 60 for t in tot)} ({100 * sum(t >= 60 for t in tot) / n:.1f}%); 65 or 66 in {sum(t >= 65 for t in tot)}')
g3 = [k for k in K if sc[k][0] >= 37 and sc[k][1] >= 28 and sc[k][2] <= 0]
right = [k for k in g3 if sc[k][3] <= 2]; wrong = [k for k in g3 if sc[k][3] > 2]
print(f'2. the 43: {len(g3)}; right way round {len(right)}; of those with 66 of 66: {sum(sc[k][0] + sc[k][1] == 66 for k in right)}; with 65:', [(year_of(k), sc[k]) for k in right if sc[k][0] + sc[k][1] == 65])
print('   the 16 by year BC:', [year_of(k) for k in right])
loose = [k for k in K if sc[k][0] + sc[k][1] >= 65 and sc[k][2] == 0]
lr = [k for k in loose if sc[k][3] <= 3]
print(f'3. A + S of 65 or more with U of 0: {len(loose)} starts; their N values: {sorted(sc[k][3] for k in loose)}')
print(f'   right way round (N small): {len(lr)}:', [(year_of(k), sc[k]) for k in lr])
# gamma's sign against the model's north or south, solar glyph months
def model_north(m): return dial.model_lat(m, 'new', 0.0) > 0
for name, ks in (('the 16', right), ('the other 27', wrong)):
    agree = []
    for k in ks:
        agree.append((sum((SE[k + m]['gamma'] > 0) == model_north(m) for m in S if k + m in SE), sum(k + m in SE for m in S)))
    print(f'4. {name}: solar glyph months whose eclipse has gamma on the side the model has the Moon: from {min(a for a, b in agree)} to {max(a for a, b in agree)} of {min(b for a, b in agree)}-{max(b for a, b in agree)}')
# the northern eclipses in unmarked months for the 13 with N of 1 or 2
mags = [SE[k + m]['mag'] for k in right if sc[k][3] > 0 for m in range(1, 224) if k + m in SE and SE[k + m]['gamma'] > 0 and m not in S]
kinds = sorted({SE[k + m]['kind'] for k in right if sc[k][3] > 0 for m in range(1, 224) if k + m in SE and SE[k + m]['gamma'] > 0 and m not in S})
gam = [SE[k + m]['gamma'] for k in right if sc[k][3] > 0 for m in range(1, 224) if k + m in SE and SE[k + m]['gamma'] > 0 and m not in S]
print(f'5. the northern solar eclipses in unmarked months among the 16: {len(mags)}, kinds {kinds}, magnitude {min(mags):.2f} to {max(mags):.2f}, gamma {min(gam):+.2f} to {max(gam):+.2f}')
# histories of single months, from 300 BC
def history(m, D, upto=8, back=5):
    out = []
    for j in range(-back, upto):
        e = D.get(223 * j + m)
        out.append(f"{j}:{'-' if e is None else e['kind'] + '(' + bc(e['y']) + (', ' + format(e['mag'], '.2f') if e['kind'] in 'NP' else '') + ')'}")
    return ' '.join(out)
for m, D, lab in ((213, LE, 'lunar'), (125, LE, 'lunar'), (126, LE, 'lunar'), (214, LE, 'lunar'), (196, SE, 'solar'), (207, SE, 'solar'), (2, SE, 'solar'), (78, SE, 'solar'), (13, SE, 'solar')):
    print(f'6. month {m} ({lab}), cycles -5 to 7: {history(m, D)}')
print('   cycle 0: solar month 2:', SE.get(2), '; solar month 78:', SE.get(78))
# the order in which marked months lose their eclipses, and whether any regains one
def lost(Lst, D):
    first = {}
    for m in Lst:
        f = next((j for j in range(0, 123) if 223 * j + m not in D), None); first[m] = f
        if f is not None: assert all(223 * j + m not in D for j in range(f, 123)), (m, 'regains')
    return first
fa, fsol = lost(L, LE), lost(S, SE)
print('7. lunar months in the order they first lack an eclipse (month: cycle):', sorted(fa.items(), key=lambda x: x[1])[:8], '; solar:', sorted(fsol.items(), key=lambda x: x[1])[:6], '; no month regains an eclipse (asserted)')
off = {m: (38 * (m - 1) + 17) % 446 for m in L}
d = {m: min(((off[m] - 66 + 223) % 446) - 223, ((off[m] - 289 + 223) % 446) - 223, key=abs) for m in L}
xs = [d[m] for m in L]; ys = [fa[m] for m in L]
mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
r = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
print(f'   correlation of the cycle a lunar month first lacks an eclipse with its model distance from the node point: {r:+.3f}')
# the end of cycle 122 and Aum rising
print('8. last eclipses of cycle 122: lunar', LE[max(n for n in LE if n <= 223 * 123)]['date'], '; solar', SE[max(n for n in SE if n <= 223 * 123)]['date'], '; month 27429 solar:', SE.get(27429, {}).get('date'))
for j in (0, 1):
    print(f'9. cycle {j}: lunar glyph months, kind of eclipse:', {m: LE[223 * j + m]['kind'] for m in (2, 73, 214)})
