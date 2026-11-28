"""Referee: what the page printed (drive.js -> page.json) beside my own program.  python -I compare.py page.json"""
import json, sys, re, math, subprocess, os
import numpy as np
sys.setrecursionlimit(100000)
HERE = '/home/agent2/referee-gasket-27'
J = json.load(open(sys.argv[1]))
if len(sys.argv) > 2:
    X_ = json.load(open(sys.argv[2])); J['snaps'] += X_['snaps']; J['third'] += X_['third']
ONE = [0, 0]
ncmp = 0; ndiff = 0; notes = []
def cmp(ok, what):
    global ncmp, ndiff
    ncmp += 1
    if not ok:
        ndiff += 1
        if len(notes) < 400: notes.append(what)
    return ok
def grp(n): return format(n, ',')
def num(s): return int(s.replace(',', ''))
def is_sq(n): return n >= 0 and math.isqrt(n) ** 2 == n
def is_q(n): return any(n % u == 0 and round((n // u) ** 0.25) ** 4 == n // u for u in (1, 4, 9, 36))
TESTS = {'none': None, '1': lambda b: is_sq(b), '2': lambda b: b % 2 == 0 and is_sq(b // 2), '3': lambda b: b % 3 == 0 and is_sq(b // 3),
         '6': lambda b: b % 6 == 0 and is_sq(b // 6), 'q': is_q, 'five': lambda b: b % 5 == 0}
WORDS = {'1': 'a square', '2': 'twice a square', '3': 'three times a square', '6': 'six times a square', 'q': 'a fourth power, or 4, 9 or 36 times one', 'five': 'a multiple of 5'}
FAMW = {1: 'a square', 2: 'twice a square', 3: 'three times a square', 6: 'six times a square'}

# ---- my own types (kron and chi2 as in my types.py; the table as I copied it from the paper's source)
def kron(a, n):
    if n == 1: return 1
    res = 1; v = 0
    while n % 2 == 0: n //= 2; v += 1
    if v:
        if a % 2 == 0: return 0
        if v % 2 == 1 and a % 8 in (3, 5): res = -res
    a %= n
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5): res = -res
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3: res = -res
        a %= n
    return res if n == 1 else 0
def chi2c(n, rho): return kron(rho, n) if n % 4 in (0, 1) else kron(-rho, n // 2) if n % 4 == 2 else kron(2 * rho, n)
def not_ruled(res, who):
    can = [u for u in (1, 2, 3, 6) if any((u * n * n) % 24 in res for n in range(1, 25))]
    w = [{2: 'twice', 3: 'three times', 6: 'six times'}[u] for u in can if u != 1]
    tail = (', '.join(w[:-1]) + ' or ' + w[-1] if len(w) > 1 else w[0]) + ' a square'
    return (who + ' does not rule out the squares in it, nor ' + tail + '.') if 1 in can else ('No square leaves any of these remainders, so no square can be here. ' + who + ' does not rule out ' + tail + '.')
def shown(w):
    for u in (1, 4, 9, 36):
        if w % u == 0 and round((w // u) ** 0.25) ** 4 == w // u:
            r = round((w // u) ** 0.25); assert u * r ** 4 == w
            return grp(w) + ' is on a circle, and ' + grp(w) + ' = ' + ('' if u == 1 else '%d × (' % u) + ' × '.join([grp(r)] * 4) + ('' if u == 1 else ')')
def my_reduce(q):
    q = list(q)
    while True:
        s = sum(q); ch = False
        for i in range(4):
            n = 2 * (s - q[i]) - q[i]
            if n < q[i]: q[i] = n; ch = True; break
        if not ch: return tuple(sorted(q))
def my_chi2(root):
    vals = set(); stack = [(tuple(root), 0)]; seen = set()
    while stack:
        Q, d = stack.pop()
        if tuple(sorted(Q)) in seen: continue
        seen.add(tuple(sorted(Q)))
        for i in range(4):
            for j in range(4):
                if i != j and Q[i] > 0 and Q[j] > 0 and math.gcd(Q[i], Q[j]) == 1: vals.add(chi2c(Q[i], Q[i] + Q[j]))
        if d < 4:
            s = sum(Q)
            for i in range(4):
                n = 2 * (s - Q[i]) - Q[i]
                if n > Q[i]: stack.append((Q[:i] + (n,) + Q[i + 1:], d + 1))
    return vals
TABLE = {(6, 1, 1): [], (6, 1, -1): [1, 2, 3, 6], (6, 5, 1): [2, 3], (6, 5, -1): [1, 6], (6, 13, 1): [2, 6], (6, 13, -1): [1, 3], (6, 17, 1): [3, 6], (6, 17, -1): [1, 2],
         (8, 7, 1): [3, 6], (8, 7, -1): [2], (8, 11, 1): [], (8, 11, -1): [2, 3, 6]}
def run_gasket(root, N, tag):
    f = '%s/out/third_%s_%s.bin' % (HERE, '_'.join(map(str, root)), tag)
    if not os.path.exists(f):
        r = subprocess.run(['nice', '-n', '15', HERE + '/gasket'] + [str(x) for x in root] + [str(N), f], capture_output=True, text=True)
        open(f + '.log', 'w').write(r.stdout + r.stderr)
    tot = int(re.search(r'total_circles (\d+)', open(f + '.log').read()).group(1))
    return np.fromfile(f, dtype=np.uint32), tot
def my_type(root, c):
    res = sorted(set((np.nonzero(c)[0] % 24).tolist()) | set(x % 24 for x in root))
    k = [r for r in res if math.gcd(r, 24) == 1][0]
    ch = my_chi2(root); assert len(ch) == 1, (root, ch); ch = ch.pop()
    return res, k, ch, TABLE[(len(res), k, ch)]

# ============================================================ 1. the first picture
def tangent(c1, c2): return (c2[0] * c1[1] - c1[0] * c2[1]) ** 2 + (c2[0] * c1[2] - c1[0] * c2[2]) ** 2 == (c1[0] + c2[0]) ** 2
def gen(place, maxB, strip):
    """every circle with curvature <= maxB, as exact whole triples (b, X, Y); for the strip, one period (the lines, the circle at 0, and what lies between x = 0 and x = 2)"""
    out = list(map(tuple, place)); bad = 0
    stack = [(tuple(map(tuple, place)), -1)]
    while stack:
        q, last = stack.pop()
        for i in range(4):
            if i == last: continue
            if strip and last < 0 and i > 1: continue
            o = q[i]; s = [sum(q[j][t] for j in range(4) if j != i) for t in range(3)]
            n = (2 * s[0] - o[0], 2 * s[1] - o[1], 2 * s[2] - o[2])
            if n[0] > maxB or n[0] < o[0] or (n[0] == o[0] and last >= 0): continue
            for j in range(4):
                if j != i and q[j][0] != 0 and not tangent(n, q[j]): bad += 1
            out.append(n); stack.append((q[:i] + (n,) + q[i + 1:], i))
    return out, bad
cache = {}
def circles_for(place, strip, maxB):
    key = json.dumps(place)
    if key not in cache or cache[key][0] < maxB:
        lst, bad = gen(place, maxB, strip)
        cache[key] = (maxB, lst, np.array([c[0] for c in lst], dtype=float), np.array([c[1] for c in lst], dtype=float), np.array([c[2] for c in lst], dtype=float), bad)
    return cache[key]
BIG = 400000
snap_rows = []
for kroot in sorted(set(json.dumps(s['root']) for s in J['snaps'])):
    group_snaps = [s for s in J['snaps'] if json.dumps(s['root']) == kroot]
    mb = max(min(s['view']['s'] / 0.7, BIG) for s in group_snaps)
    for s in group_snaps:
        if 'deep' in s['kind']: continue
        circles_for(s['place'], s['strip'], mb); break
cfile = {}
for s in J['snaps']:
    root = tuple(s['root']); v = s['view']; W = s['size']['W']; H = s['size']['H']; sc = v['s']; hw = W / 2 / sc; hh = H / 2 / sc; maxB = sc / 0.7
    R0 = min(W, H) / 2 - 15; base = R0 * 150 / 295 if s['strip'] else R0 * abs(root[0]); mag = sc / base
    g_ = s['gsay']; g2_ = re.sub(r'^(\(.*?\): 1 circle drawn), and it is not (.*?)(\. )', r'\1, 0 of them \2\3', g_, count=1)
    if g2_ == g_: g2_ = re.sub(r'^(\(.*?\): 1 circle drawn), and it is (.*?)(\. )', r'\1, 1 of them \2\3', g_, count=1)
    if g2_ != g_: ONE[0] += 1
    if ' 1 of them ' in g_ and '1 circle drawn' in g_: ONE[1] += 1
    s['gsay'] = g2_
    m = re.match(r'^\((.*?)\): ([\d,]+) circles? drawn(?:, ([\d,]+) of them (.*?))?( \(the page stopped[^)]*\))?( \(some circles[^)]*\))?\. (Not magnified\.|Magnified ([\d,.e+]+) times\.|Drawn back ([\d.]+) times\.)(.*)$', s['gsay'])
    if not cmp(m is not None, 'cannot read the count sentence: ' + s['gsay']): continue
    Npage = num(m.group(2)); Lpage = num(m.group(3)) if m.group(3) else None
    pd = [tuple(c) for c in s['drawn']]
    pset = set((c[0], c[1] + 2 * c[3] * c[0], c[2]) for c in pd if c[0] != 0)
    def vis(c, v=v, hw=hw, hh=hh):
        x = abs(c[1] / c[0] - v['cx']); y = abs(c[2] / c[0] - v['cy']); r = 1 / abs(c[0]); near = math.hypot(max(x - hw, 0), max(y - hh, 0))
        return near <= r if c[0] > 0 else (near <= r <= math.hypot(x + hw, y + hh))
    seen_page = [c for c in pset if vis(c)]
    cmp(Npage == len(seen_page), '%s %s %s: sentence says %d circles; of the %d the page holds, %d have something in the picture by my geometry' % (s['mode'], root, s['kind'], Npage, len(pset), len(seen_page)))
    test = TESTS[s['hi']]
    if test:
        cmp(Lpage == sum(1 for c in seen_page if c[0] > 0 and test(c[0])), '%s %s %s %s: lit in sentence %s, by my test on the circles in the picture %d' % (s['mode'], root, s['kind'], s['hi'], Lpage, sum(1 for c in seen_page if c[0] > 0 and test(c[0]))))
        cmp(m.group(4) == WORDS[s['hi']], 'words of the light: ' + str(m.group(4)))
    # magnification words
    if abs(mag - 1) < 0.0005: cmp(m.group(7) == 'Not magnified.', 'magnification words %s for %r' % (m.group(7), mag))
    elif mag > 1: cmp(m.group(8) is not None and abs(float(m.group(8).replace(',', '')) - mag) <= max(0.006 * mag, 0.51 if mag >= 100 else 0), 'magnification words %s for %r' % (m.group(7), mag))
    else: cmp(m.group(9) is not None and abs(float(m.group(9)) - 1 / mag) <= 0.006 / mag, 'drawn-back words %s for %r' % (m.group(7), mag))
    if 'deep' in s['kind'] or maxB > BIG:
        # too deep for me to make every circle: test that what is drawn is a packing (no two discs overlap), admissible remainders, and count lit
        lst = sorted(pset); ov = 0
        for a in range(len(lst)):
            for b2 in range(a + 1, len(lst)):
                c1, c2 = lst[a], lst[b2]
                d2 = (c2[0] * c1[1] - c1[0] * c2[1]) ** 2 + (c2[0] * c1[2] - c1[0] * c2[2]) ** 2
                if c1[0] > 0 and c2[0] > 0 and d2 < (c1[0] + c2[0]) ** 2: ov += 1
        cmp(ov == 0, '%s %s %s: %d pairs of drawn circles overlap' % (s['mode'], root, s['kind'], ov))
        snap_rows.append((s['mode'], root, s['kind'], s['hi'], round(mag, 3), Npage, Lpage, 'deep: %d circles, overlaps %d' % (len(lst), ov)))
        continue
    mbv, lst, B, X, Y, bad = circles_for(s['place'], s['strip'], maxB)
    cmp(bad == 0, '%s: %d tangency failures in my own generation' % (root, bad))
    cmp(sorted(c[0] for c in s['place']) == sorted(root), 'the placed circles are not the four of the name')
    if not s['strip']:
        cmp(all(tangent(s['place'][i], s['place'][j]) for i in range(4) for j in range(i)), 'the placed four are not mutually tangent')
    mine = set(); may = set()
    ks = range(int(math.floor((v['cx'] - hw - 3) / 2)), int(math.ceil((v['cx'] + hw + 3) / 2)) + 1) if s['strip'] else [0]
    for k in ks:
        sel = (B != 0) & (B <= maxB)
        with np.errstate(divide='ignore', invalid='ignore'):
            r = 1 / np.abs(B); x = (X + 2 * k * B) / B - v['cx']; y = Y / B - v['cy']
        inbox = sel & (x + r >= -hw) & (x - r <= hw) & (y + r >= -hh) & (y - r <= hh)
        dx = np.maximum(np.abs(x) - hw, 0); dy = np.maximum(np.abs(y) - hh, 0)
        disc = inbox & ((dx * dx + dy * dy <= r * r) | (B < 0))
        for idx in np.nonzero(inbox)[0]:
            c = lst[idx]
            if s['strip'] and k != 0 and c[0] == 1 and c[1] == 0 and False: continue
            t = (c[0], c[1] + 2 * k * c[0], c[2])
            mine.add(t)
            if not disc[idx]: may.add(t)
    only_page = pset - mine; only_mine = mine - pset; visible_missed = only_mine - may
    cmp(not only_page, '%s %s %s: %d circles drawn by the page that I do not have, e.g. %s' % (s['mode'], root, s['kind'], len(only_page), sorted(only_page)[:3]))
    cmp(not visible_missed, '%s %s %s: %d circles that meet the view are not drawn by the page, e.g. %s' % (s['mode'], root, s['kind'], len(visible_missed), sorted(visible_missed)[:3]))
    vm = [c for c in mine if vis(c)]
    cmp(Npage == len(vm), '%s %s %s: the page says %d; of my own circles %d have something in the picture (and %d more only touch by their square or are the outer circle out of view)' % (s['mode'], root, s['kind'], Npage, len(vm), len(mine) - len(vm)))
    if test: cmp(Lpage == sum(1 for c in vm if c[0] > 0 and test(c[0])), '%s %s %s %s: lit: page %s, my own circles in the picture %d' % (s['mode'], root, s['kind'], s['hi'], Lpage, sum(1 for c in vm if c[0] > 0 and test(c[0]))))
    extra = ''
    if s['kind'] == 'whole' and not s['strip']:
        if root not in cfile: cfile[root] = np.fromfile('%s/out/g_%s_1e6.bin' % (HERE, '_'.join(map(str, root))), dtype=np.uint32).astype(np.int64)
        c = cfile[root]; t = int(math.floor(maxB)); mineC = int(c[:t + 1].sum()) + 1
        litC = sum(int(c[b]) for b in range(1, t + 1) if c[b] and test(b)) if test else None
        cmp(Npage == mineC, '%s %s whole: the page says %d circles, my count file (curvature <= %.1f) says %d' % (s['mode'], root, Npage, maxB, mineC))
        if test: cmp(Lpage == litC, '%s %s whole %s: the page says %s lit, my count file says %s' % (s['mode'], root, s['hi'], Lpage, litC))
        extra = 'count file: %d circles, %s lit (curvature <= %.1f)' % (mineC, litC, maxB)
    snap_rows.append((s['mode'], root, s['kind'], s['hi'], round(mag, 3), Npage, Lpage, 'mine in the picture %d (held but unseen %d); page only %d; mine only %d; %s' % (len(vm), len(mine) - len(vm), len(only_page), len(only_mine), extra)))
print('=== first picture: %d views' % len(snap_rows))
for r in snap_rows:
    if r[2] == 'whole' and r[3] in ('1', 'q', 'five') or 'x4' in r[2] and r[3] == '1' or 'deep' in r[2]: print('  ', r)
c1 = (ncmp, ndiff); print('comparisons so far', ncmp, 'differing', ndiff)

# ---- the sentences about each gasket
seen = {}
for s in J['snaps']:
    if s['kind'] != 'whole' or s['hi'] != '1': continue
    root = tuple(s['root'])
    if root == (0, 0, 1, 1): c = np.fromfile(HERE + '/out/g_0_0_1_1_1e6.bin', dtype=np.uint32)
    else: c = np.fromfile('%s/out/g_%s_1e6.bin' % (HERE, '_'.join(map(str, root))), dtype=np.uint32)
    res, k, ch, fam = my_type(root, c)
    want = 'Every number in this gasket leaves ' + re.sub(r', (\d+)$', r' or \1', ', '.join(map(str, res))) + ' on division by 24 (the test told of below). '
    cmp(s['gkind'].startswith(want), '%s: remainders sentence: %s' % (root, s['gkind'][:120]))
    rest = s['gkind'][len(want):]
    if fam: cmp(rest.startswith('None of them is ' + ' or '.join(FAMW[u] for u in fam) + ': that was proved in 2023.'), '%s families: %s (mine %s)' % (root, rest, fam))
    else: cmp(rest.startswith(not_ruled(res, 'The theorem of 2023')), '%s families: %s (mine none; I expect: %s)' % (root, rest, not_ruled(res, 'The theorem of 2023')))
    seen[(s['mode'], root)] = (res, k, ch, fam, rest, s['menu'])
print('=== the seven gaskets, as the page says and as I have them')
for (mode, root), v in seen.items():
    if mode == 'desk': print('  ', root, 'mine: residues', v[0], 'type (%d,%d,%d)' % (len(v[0]), v[1], v[2]), 'families', v[3], '| page:', v[4], '| menu:', v[5])
c2 = (ncmp, ndiff); print('comparisons so far', ncmp, 'differing', ndiff)

# ============================================================ 2. the second picture
MYFILES = {(-1, 2, 2, 3): ('1e7', np.uint32), (0, 0, 1, 1): ('3e7', np.uint8), (-3, 5, 8, 8): ('1e8', np.uint8), (-3, 4, 12, 13): ('1e7', np.uint32), (-2, 3, 6, 7): ('1e7', np.uint32), (-4, 5, 20, 21): ('1e8', np.uint8)}
DATA = json.load(open('/home/agent2/gasket/data.json'))
print('=== second picture')
mycache = {}
for ch in J['charts']:
    d = DATA[ch['i']]; root = tuple(d['root']); tag, dt = MYFILES[root]
    if root not in mycache:
        c = np.fromfile('%s/out/g_%s_%s.bin' % (HERE, '_'.join(map(str, root)), tag), dtype=dt); lim = len(c) - 1
        res = sorted(set((np.nonzero(c[:1000001])[0] % 24).tolist())); look = np.zeros(24, bool); look[res] = True
        miss = np.nonzero(np.tile(look, lim // 24 + 1)[:lim + 1] & (c == 0))[0]; miss = miss[miss > 0].tolist()
        _, k, chi, fam = my_type(root, c[:1000001])
        infam = lambda vv, fam=fam: any(vv % u == 0 and is_sq(vv // u) for u in fam)
        mycache[root] = (lim, res, fam, [m for m in miss if not infam(m)], set(m for m in miss if infam(m)), c)
    lim, res, fam, spor, famset, c = mycache[root]
    rows = {}
    for x, r, vv in ch['marks']: rows.setdefault(r, []).append((x, vv))
    p0 = [vv for x, vv in rows.get(0, [])]
    n_before = ncmp; d_before = ndiff
    # row 0, number for number up to my limit
    for a, b in zip(p0, spor): cmp(a == b, '%s %s: in no family, page %d mine %d' % (ch['mode'], root, a, b))
    cmp(len([vv for vv in p0 if vv <= lim]) == len(spor), '%s %s: in no family, page has %d up to %d, I have %d' % (ch['mode'], root, len([vv for vv in p0 if vv <= lim]), lim, len(spor)))
    beyond = [vv for vv in p0 if vv > lim]
    cmp(not beyond, '%s %s: %d numbers in no family past my limit %d (not checked by me)' % (ch['mode'], root, len(beyond), lim))
    # family rows: every mark up to my limit is absent in my file and of the form; the sets are equal
    pf = set()
    for r in sorted(rows):
        if r == 0: continue
        u = fam[r - 1] if r - 1 < len(fam) else None
        cmp(u is not None and ch['strip']['rows'][r] == ('squares' if u == 1 else '%d× squares' % u), '%s %s: row %d named %s, my family %s' % (ch['mode'], root, r, ch['strip']['rows'][r], u))
        for x, vv in rows[r]:
            ok = u is not None and vv % u == 0 and is_sq(vv // u) and vv % 24 in res and (vv > lim or c[vv] == 0)
            cmp(ok, '%s %s: family mark %d' % (ch['mode'], root, vv))
            if vv <= lim: pf.add(vv)
    cmp(pf == famset, '%s %s: family numbers up to my limit: page %d, mine %d' % (ch['mode'], root, len(pf), len(famset)))
    # places of the marks along the line
    st = ch['strip']; bad = sum(1 for x, r, vv in ch['marks'] if abs(x - (st['left'] + (st['W'] - st['left'] - st['right']) * math.log10(vv) / 8)) > 0.01)
    cmp(bad == 0, '%s %s: %d marks not at their place on the line' % (ch['mode'], root, bad))
    # the sentence
    nf = sum(len(v) for r, v in rows.items() if r > 0); last = p0[-1]
    m = re.match(r'^\((.*?)\), every circle with a number up to ([\d,]+): ([\d,]+) numbers are missing that are in no family, the last of them ([\d,]+)(?:; and ([\d,]+) that are (.*?), none of which is ever there|; the paper rules out no family in this gasket)\.$', ch['csay'])
    if cmp(m is not None, 'cannot read: ' + ch['csay']):
        cmp(num(m.group(3)) == len(p0) and (lim < 10 ** 8 or len(p0) == len(spor)), 'count in no family')
        cmp(num(m.group(4)) == last and last == spor[-1], 'the last: page %s, mine %d' % (m.group(4), spor[-1]))
        if fam:
            want = sum(1 for u in fam for n in range(1, math.isqrt(10 ** 8 // u) + 1) if (u * n * n) % 24 in res)
            cmp(m.group(5) is not None and num(m.group(5)) == want == nf, 'count in families: page %s, marks %d, mine %d' % (m.group(5), nf, want))
        else: cmp(m.group(5) is None, 'a family where I have none')
    cmp(any(t == 'the last, ' + grp(spor[-1]) for t in ch['texts']), 'label of the last: ' + str(ch['texts']))
    tb = ch.get('table', ''); mt = re.search(r'In no family \(([\d,]+)\): (.*)$', tb)
    if cmp(mt is not None, 'cannot read the list'): cmp([num(x) for x in mt.group(2).split(' · ')] == p0 and num(mt.group(1)) == len(p0), '%s %s: the list shown is not the row of marks' % (ch['mode'], root))
    print('  ', ch['mode'], root, 'my limit', lim, '| in no family: page', len(p0), 'mine', len(spor), '| family marks', nf, '(up to my limit: page', len(pf), 'mine', len(famset), ') | comparisons', ncmp - n_before, 'differing', ndiff - d_before, '|', ch['csay'][:60])
for t in J['taps']:
    d = DATA[t['i']]; root = tuple(d['root']); lim, res, fam, spor, famset, c = mycache[root]
    ch = [x for x in J['charts'] if x['mode'] == t['mode'] and x['i'] == t['i']][0]
    m = re.match(r'^([\d,]+) (is missing, and is in no family|= (.*?), so it is never the number of a circle in this gasket)\. It leaves (\d+) on division by 24\.(?: It is one of ([\d,]+) marks (under your finger|within 12 px of the pointer)\.)?$', t['line'])
    if not cmp(m is not None, 'tap not answered with a number: %s %s row %d aimed %d: %s' % (t['mode'], root, t['row'], t['aimed'], t['line'])): continue
    vv = num(m.group(1)); rowmarks = [(x, n) for x, r, n in ch['marks'] if r == t['row']]
    cmp(vv == t['aimed'] or any(abs(x - t['aimedX']) <= 0.75 and n == vv for x, n in rowmarks), '%s %s row %d: aimed at %d, answered %d' % (t['mode'], root, t['row'], t['aimed'], vv))
    cmp(int(m.group(4)) == vv % 24, 'remainder of %d' % vv)
    cmp(vv > lim or c[vv] == 0, '%d is said missing and is a curvature in my file' % vv)
    if t['row'] == 0: cmp(m.group(3) is None and not any(vv % u == 0 and is_sq(vv // u) for u in fam), '%d said in no family' % vv)
    else:
        u = fam[t['row'] - 1]; n = math.isqrt(vv // u)
        cmp(m.group(3) == ((grp(n) + ' × ' + grp(n)) if u == 1 else '%d × (%s × %s)' % (u, grp(n), grp(n))) and u * n * n == vv, 'the square written for %d: %s' % (vv, m.group(3)))
    px = [x for x, n in rowmarks if n == vv][0]; crowd = sum(1 for x, n in rowmarks if abs(x - t['aimedX']) <= 12)
    cmp((num(m.group(5)) if m.group(5) else None) == (crowd if crowd > 2 else None), '%s %s row %d at %d: page says one of %s marks, I count %d within 12' % (t['mode'], root, t['row'], vv, m.group(5), crowd))
    if m.group(6): cmp(m.group(6) == ('under your finger' if t['mode'] == 'phone' else 'within 12 px of the pointer'), 'words for the crowd')
print('taps:', len(J['taps']), 'e.g.', [t['line'] for t in J['taps'][10:13]])
c3 = (ncmp, ndiff); print('comparisons so far', ncmp, 'differing', ndiff)

# ============================================================ 3. the third panel
print('=== third panel')
for t in J['third']:
    q = [int(x) for x in re.findall(r'-?\d+', t['q'])]; s = sum(q); N = t['N']; n0 = ncmp; d0 = ndiff
    if not (s > 0 and s * s == 2 * sum(x * x for x in q)):
        eqn = s * s == 2 * sum(x * x for x in q)
        if eqn and s < 0: cmp(t['tsay'] == 'Those four satisfy the equation, but with every sign the wrong way round: of four circles that touch, at most one has a minus. Try ' + ', '.join(('−%d' % x) if x > 0 else str(-x) for x in q) + '.', 'refusal of signs turned: ' + t['tsay'])
        else: cmp(t['tsay'].startswith('Those four do not satisfy Descartes’s equation'), 'refusal: ' + t['tsay'])
        print('  ', t['q'], '->', t['tsay'][:200]); continue
    if math.gcd(math.gcd(q[0], q[1]), math.gcd(q[2], q[3])) != 1:
        cmp(t['tsay'] == 'Those four have a common divisor; divide it out first.', 'common divisor: ' + t['tsay']); print('  ', t['q'], '->', t['tsay'][:150]); continue
    root = my_reduce(q); c, tot = run_gasket(root, N, str(N)); res, k, ch, fam = my_type(root, c)
    look = np.zeros(24, bool); look[res] = True
    miss = np.nonzero(np.tile(look, N // 24 + 1)[:N + 1] & (c == 0))[0]; miss = miss[miss > 0].tolist()
    infam = [m for m in miss if any(m % u == 0 and is_sq(m // u) for u in fam)]
    name = '(' + ', '.join(('−%d' % -x) if x < 0 else str(x) for x in root) + ')'
    ts = t['tsay']
    cmp(ts.startswith(name + ' are the four largest circles of their gasket. ' if tuple(sorted(q)) == root else 'These circles belong to the gasket whose four largest circles are ' + name + '. '), 'root of %s: mine %s; page: %s' % (t['q'], root, ts[:90]))
    cmp('Its numbers leave ' + ', '.join(map(str, res)) + ' on division by 24. ' in ts, 'remainders of %s: mine %s' % (root, res))
    if fam: cmp('By the paper’s theorem no number in it is ' + ' or '.join(FAMW[u] for u in fam) + '. ' in ts, 'families of %s: mine %s; page: %s' % (root, fam, ts[:260]))
    else: cmp(not_ruled(res, 'The paper’s theorem') + ' ' in ts, 'families of %s: mine none; page: %s' % (root, ts[:260]))
    quart = None; q4 = []
    if len(res) == 6 and k in (1, 17) and ch == 1:
        present = {u: [u * n ** 4 for n in range(1, 200) if u * n ** 4 <= N and c[u * n ** 4] > 0] for u in (1, 4, 9, 36)}
        a = sorted(present[1] + present[4]); b = sorted(present[9] + present[36]); quart = (a[:3], b[:3])
        if k == 1:
            if a or b: cmp('In this gasket no fourth powers are ruled out. The page finds that by looking: ' + shown((sorted(present[1]) + sorted(present[4]) + sorted(present[9]) + sorted(present[36]))[0]) + '; and in a gasket with these remainders the fourth powers, and 4, 9 and 36 times a fourth power, are either all ruled out or none of them is. ' in ts, 'fourth powers in %s: mine present %s; page: %s' % (root, quart, ts))
            else: cmp('In a gasket with these remainders the fourth powers, and 4, 9 and 36 times a fourth power, are either all ruled out or none of them is. The page finds which by looking for one of them on a circle. Up to ' + grp(N) + ' it finds none, which is what would be seen if they are all ruled out, and does not prove it. ' in ts, 'fourth powers in %s: I find none; page: %s' % (root, ts))
        else:
            q4 = [9, 36] if a else [1, 4] if b else []
            if a: cmp('In this gasket 9 times and 36 times a fourth power are ruled out as well. The page finds that by looking: ' + shown((sorted(present[1]) + sorted(present[4]))[0]) + '; and in a gasket with these remainders either the fourth powers and 4 times a fourth power are ruled out, or 9 and 36 times a fourth power are. ' in ts and not b, 'fourth powers in %s: mine %s; page: %s' % (root, quart, ts))
            elif b: cmp('In this gasket the fourth powers, and 4 times a fourth power, are ruled out as well. The page finds that by looking: ' + shown((sorted(present[9]) + sorted(present[36]))[0]) + '; and in a gasket with these remainders either the fourth powers and 4 times a fourth power are ruled out, or 9 and 36 times a fourth power are. ' in ts, 'fourth powers in %s: mine %s; page: %s' % (root, quart, ts))
            else: cmp('In a gasket with these remainders either the fourth powers and 4 times a fourth power are ruled out, or 9 and 36 times a fourth power are. The page finds which by looking for one of them on a circle, and up to ' + grp(N) + ' it finds none. ' in ts, 'fourth powers in %s: none; page: %s' % (root, ts))
    else: cmp('fourth' not in ts, 'fourth powers spoken of in %s where the type has none' % (root,))
    infam = [m_ for m_ in miss if any(m_ % u == 0 and is_sq(m_ // u) for u in fam) or any(m_ % u == 0 and round((m_ // u) ** 0.25) ** 4 == m_ // u for u in q4)]
    m = re.search(r'Going through its ([\d,]+) circles with a number up to ([\d,]+): ([\d,]+) numbers that pass the test are missing(?:, ([\d,]+) of them in the famil(?:ies|y) ruled out \(marked with an orange square\) and ([\d,]+) not)?\.$', ts)
    if cmp(m is not None, 'cannot read the count: ' + ts[-200:]):
        cmp(num(m.group(1)) == tot, 'circles of %s up to %d: page %s, mine %d' % (root, N, m.group(1), tot))
        cmp(num(m.group(3)) == len(miss), 'missing in %s up to %d: page %s, mine %d' % (root, N, m.group(3), len(miss)))
        if fam or q4: cmp(m.group(4) is not None and num(m.group(4)) == len(infam) and num(m.group(5)) == len(miss) - len(infam), 'split in %s: page %s and %s, mine %d and %d' % (root, m.group(4), m.group(5), len(infam), len(miss) - len(infam)))
        else: cmp(m.group(4) is None, 'a split where I have no family')
    if miss:
        lst = re.sub(r' … \(.*$', '', t['nums'].replace('Missing: ', '')).split(' · ')
        cmp([num(x) for x in lst] == miss[:600], 'the list of missing numbers of %s up to %d (first 600)' % (root, N))
        cmp(sorted(num(x) for x in t['bold']) == [m_ for m_ in miss[:600] if m_ in set(infam)], 'which are marked orange in %s' % (root,))
    qf = [m_ for m_ in miss if is_q(m_)]
    print('  ', t['q'], 'N', N, '-> root', root, 'type (%d,%d,%d)' % (len(res), k, ch), 'families', fam, 'circles', tot, 'missing', len(miss), 'in families', len(infam), '| fourth-power forms present (n^4|4n^4 ; 9n^4|36n^4):', quart, '| missing of those forms:', len(qf), qf[:6], '| comparisons', ncmp - n0, 'differing', ndiff - d0)
print()
print('TOTAL comparisons', ncmp, 'differing', ndiff)
print('first picture', c1, '; gasket sentences', (c2[0] - c1[0], c2[1] - c1[1]), '; second picture and taps', (c3[0] - c2[0], c3[1] - c2[1]), '; third panel', (ncmp - c3[0], ndiff - c3[1]))
print('page errors:', J['errs']); print('one-circle sentences in the new wording:', ONE[0], '; still in the old wording:', ONE[1])
for n in notes[:120]: print('  DIFF:', n[:400])
