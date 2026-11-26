# How well could a perfect listener tell the Aeneid from Arator by the feet alone?  And the passages for the listening page.
# Reads listen_scans.json (written by listen.py).  Run:  python3 -I listen_ideal.py   -> listen_ideal.out, listen_pool.json, ~/site/listen-data.js
import sys, json, random, math, collections, re; sys.path.insert(0, '/home/agent1/arator')
import scan
D = json.load(open('/home/agent1/arator/listen_scans.json'))
NAME = dict(aen='Aeneid', arator='Arator', juvencus='Juvencus')
def nd(r): return r['pat'][:4].count('D')
def runs(rows):
    """the poem as stretches of consecutive scanned lines that stay inside one book"""
    out = []; cur = []; book = None
    for r in rows:
        b = r.get('book', 0)
        if r['pat'] is None or b != book:
            if cur: out.append(cur)
            cur = []; book = b
            if r['pat'] is None: continue
        cur.append(r)
    if cur: out.append(cur)
    return out
def windows(rows, n):
    return [run[i:i + n] for run in runs(rows) for i in range(0, len(run) - n + 1)]
def best_threshold(lo, hi):
    """lo, hi: lists of counts for the heavier and the lighter poet.  Rule: say 'lighter' when the count is k or more.  Returns the best share right (equal chances of either poet) and k."""
    best = (0, None)
    for k in range(0, max(lo + hi) + 2):
        acc = 0.5 * (sum(1 for c in lo if c < k) / len(lo) + sum(1 for c in hi if c >= k) / len(hi))
        if acc > best[0]: best = (acc, k)
    return best
def freqs(rows):
    c = collections.Counter(r['pat'][:4] for r in rows if r['pat']); n = sum(c.values())
    return {''.join(p): (c[''.join(p)] + 0.5) / (n + 8) for p in __import__('itertools').product('DS', repeat=4)}
def halves(name):
    rows = D[name]
    if name == 'aen': return [r for r in rows if r['book'] % 2 == 1], [r for r in rows if r['book'] % 2 == 0]
    if name == 'arator': return [r for r in rows if r['book'] == 1], [r for r in rows if r['book'] == 2]
    h = len(rows) // 2; return rows[:h], rows[h:]
def likelihood_acc(a, b, n):
    """two-fold: pattern frequencies from one half of each poem, passages from the other half; then the halves change places"""
    accs = []
    for fold in (0, 1):
        fa, fb = freqs(halves(a)[fold]), freqs(halves(b)[fold]); right = []
        for name, sign in ((a, -1), (b, +1)):
            ws = windows(halves(name)[1 - fold], n); r = 0
            for w in ws:
                llr = sum(math.log(fb[x['pat'][:4]] / fa[x['pat'][:4]]) for x in w)
                r += 1 if llr * sign > 0 else 0.5 if llr == 0 else 0
            right.append(r / len(ws))
        accs.append(sum(right) / 2)
    return sum(accs) / 2, accs
def count_acc_cv(a, b, n):
    """the count rule with its threshold chosen on one half of each poem and used on the other"""
    accs = []
    for fold in (0, 1):
        _, k = best_threshold([sum(nd(r) for r in w) for w in windows(halves(a)[fold], n)], [sum(nd(r) for r in w) for w in windows(halves(b)[fold], n)])
        lo = [sum(nd(r) for r in w) for w in windows(halves(a)[1 - fold], n)]; hi = [sum(nd(r) for r in w) for w in windows(halves(b)[1 - fold], n)]
        accs.append(0.5 * (sum(1 for c in lo if c < k) / len(lo) + sum(1 for c in hi if c >= k) / len(hi)))
    return sum(accs) / 2, accs
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s)
for name in D:
    ok = [r for r in D[name] if r['pat']]
    P(f"{NAME[name]}: {len(D[name])} lines, {len(ok)} scanned; dactyls in feet 1-4: {100 * sum(nd(r) for r in ok) / (4 * len(ok)):.2f}%, that is {sum(nd(r) for r in ok) / len(ok):.3f} a line and {8 * sum(nd(r) for r in ok) / len(ok):.2f} in eight lines; spread of the count in one line (sd) {(sum(nd(r) ** 2 for r in ok) / len(ok) - (sum(nd(r) for r in ok) / len(ok)) ** 2) ** 0.5:.3f}")
P('\nA. THE COUNT RULE on passages of n consecutive lines (every passage of the poem that stays inside one book): count the dactyls in feet 1-4, say "the lighter poet" at k or more.')
P('   pair                 n   passages (heavier, lighter)   best k   right, %   [threshold from one half, used on the other: right %, the two folds]   all sixteen patterns known (two-fold) %')
CURVE = {}
for a, b in (('aen', 'arator'), ('juvencus', 'arator')):
    for n in ((1, 2, 4, 8, 16, 24, 32, 40, 48, 56, 64) if a == 'aen' else (1, 2, 4, 8, 16, 32, 64)):
        lo = [sum(nd(r) for r in w) for w in windows(D[a], n)]; hi = [sum(nd(r) for r in w) for w in windows(D[b], n)]
        acc, k = best_threshold(lo, hi); cv, folds = count_acc_cv(a, b, n); lk, lfolds = likelihood_acc(a, b, n)
        CURVE[(a, b, n)] = (acc, k, cv, lk)
        P(f"   {NAME[a]:8s} v {NAME[b]:7s} {n:3d}   {len(lo):6d} {len(hi):6d}             {k:4d}     {100 * acc:5.1f}      [{100 * cv:5.1f}; {100 * folds[0]:.1f}, {100 * folds[1]:.1f}]                                   {100 * lk:5.1f}  ({100 * lfolds[0]:.1f}, {100 * lfolds[1]:.1f})")
P('\nB. The same count rule if the Aeneid is counted by the REFERENCE scansion and not by my program (n = 8):')
refrows = [dict(r, pat=r['ref']) for r in D['aen']]
lo = [sum(nd(r) for r in w) for w in windows(refrows, 8)]; hi = [sum(nd(r) for r in w) for w in windows(D['arator'], 8)]
acc, k = best_threshold(lo, hi); P(f"   {len(lo)} passages of the Aeneid by the reference; best k {k}; right {100 * acc:.1f}%")
P('\nC. EIGHT LINES DRAWN AT RANDOM from anywhere in each poem, not consecutive (20,000 draws of each):')
random.seed(544)
for a, b in (('aen', 'arator'), ('juvencus', 'arator')):
    oa = [nd(r) for r in D[a] if r['pat']]; ob = [nd(r) for r in D[b] if r['pat']]
    lo = [sum(random.sample(oa, 8)) for _ in range(20000)]; hi = [sum(random.sample(ob, 8)) for _ in range(20000)]
    acc, k = best_threshold(lo, hi); P(f"   {NAME[a]} v {NAME[b]}: best k {k}; right {100 * acc:.1f}%   (consecutive lines: {100 * CURVE[(a, b, 8)][0]:.1f}%)")
P('\nD. How the count of dactyls in eight consecutive lines is spread (share of passages, %):')
lo = [sum(nd(r) for r in w) for w in windows(D['aen'], 8)]; hi = [sum(nd(r) for r in w) for w in windows(D['arator'], 8)]
ca, cb = collections.Counter(lo), collections.Counter(hi); HIST = {}
for c in range(0, 33):
    if ca[c] or cb[c]:
        HIST[c] = (100 * ca[c] / len(lo), 100 * cb[c] / len(hi)); P(f"   {c:2d} dactyls: Aeneid {HIST[c][0]:5.2f}   Arator {HIST[c][1]:5.2f}")
sd = lambda v: (sum(x * x for x in v) / len(v) - (sum(v) / len(v)) ** 2) ** 0.5
P(f"   mean and spread (sd): Aeneid {sum(lo) / len(lo):.2f}, {sd(lo):.2f};  Arator {sum(hi) / len(hi):.2f}, {sd(hi):.2f}.   If lines were independent the spread would be {8 ** 0.5 * 0.0 + (8 ** 0.5) * sd([nd(r) for r in D['aen'] if r['pat']]):.2f} and {(8 ** 0.5) * sd([nd(r) for r in D['arator'] if r['pat']]):.2f}.")
k8 = CURVE[('aen', 'arator', 8)][1]
P(f"   with the rule 'Arator at {k8} or more': Aeneid passages called Arator {100 * sum(1 for c in lo if c >= k8) / len(lo):.1f}%; Arator passages called Virgil {100 * sum(1 for c in hi if c < k8) / len(hi):.1f}%")
lo8, hi8 = lo, hi

# are the four feet of a line chosen independently?  The spread of a line's count of dactyls against what independent feet with the same shares would give; and the two extreme lines
P('\nH. One line: the count of dactyls in feet 1-4, as it is and as it would be if each foot were chosen independently with the poem\'s own share for that foot:')
INDEP = {}
for name in ('aen', 'arator', 'juvencus'):
    ok = [r for r in D[name] if r['pat']]; n = len(ok); p = [sum(1 for r in ok if r['pat'][f] == 'D') / n for f in range(4)]
    sdi = sum(x * (1 - x) for x in p) ** 0.5; sdr = sd([nd(r) for r in ok])
    dddd = sum(1 for r in ok if r['pat'][:4] == 'DDDD'); ssss = sum(1 for r in ok if r['pat'][:4] == 'SSSS'); pd = p[0] * p[1] * p[2] * p[3]; ps = (1 - p[0]) * (1 - p[1]) * (1 - p[2]) * (1 - p[3])
    INDEP[name] = dict(p=p, sd=sdr, sd_indep=sdi, dddd=dddd, ssss=ssss, dddd_indep=pd * n, ssss_indep=ps * n, n=n)
    P(f"   {NAME[name]}: shares by foot {[round(100 * x, 1) for x in p]}; sd of the count {sdr:.3f}, independent feet would give {sdi:.3f};  all four dactyls: {dddd} lines of {n} ({100 * dddd / n:.2f}%), independent {pd * n:.0f} ({100 * pd:.2f}%);  all four spondees: {ssss} ({100 * ssss / n:.2f}%), independent {ps * n:.0f} ({100 * ps:.2f}%)")
P('   What my envelope sum would have given with the real spreads of eight consecutive lines: difference of means %.2f, spreads %.2f and %.2f' % (sum(hi8) / len(hi8) - sum(lo8) / len(lo8), sd(lo8), sd(hi8)))

# neighbouring feet: does a dactyl in one foot go with a spondee in the next?  (correlation of the two, -1 to +1)
P('\nI. Neighbouring feet of one line: correlation between "this foot is a dactyl" and "the next one is" (0 if they were chosen separately):')
NEIGH = {}
for name, sel in (('aen', None), ('arator', None), ('arator book 1', 1), ('arator book 2', 2), ('juvencus', None)):
    base = name.split()[0]; ok = [r for r in D[base] if r['pat'] and (sel is None or r['book'] == sel)]; cs = []
    for f in range(3):
        x = [1.0 if r['pat'][f] == 'D' else 0.0 for r in ok]; y = [1.0 if r['pat'][f + 1] == 'D' else 0.0 for r in ok]; mx = sum(x) / len(x); my = sum(y) / len(y)
        cs.append(sum((a - mx) * (b - my) for a, b in zip(x, y)) / len(x) / ((mx * (1 - mx) * my * (1 - my)) ** 0.5))
    c = collections.Counter(r['pat'][:4] for r in ok); rank = sorted(c, key=lambda k: -c[k]).index('SSSS') + 1
    NEIGH[name] = cs
    P(f"   {NAME[base] + name[len(base):]:14s} ({len(ok)} lines): feet 1-2 {cs[0]:+.3f}, feet 2-3 {cs[1]:+.3f}, feet 3-4 {cs[2]:+.3f};  four spondees is the {rank}th commonest of the sixteen patterns ({100 * c['SSSS'] / len(ok):.1f} lines in 100)")
P('   In print (Greenberg 1978, appendix, from Duckworth\'s counts): Aeneid -0.11, -0.07, -0.04;  Arator -0.02, -0.37, -0.22;  Juvencus -0.07, -0.10, -0.03')
# where my guess of 76 went wrong, step by step (count rule on eight lines, Aeneid and Arator, best threshold each time)
P('\nJ. From my guess to the figure, the count rule on eight lines:')
def conv(ps):
    d = [1.0]
    for p in ps:
        d = [(d[i] if i < len(d) else 0) * (1 - p) + (d[i - 1] if i > 0 else 0) * p for i in range(len(d) + 1)]
    return d
def acc_dist(da, db):
    return max(0.5 * (sum(da[:k]) + sum(db[k:])) for k in range(len(da) + 1))
okA = [r for r in D['aen'] if r['pat']]; okB = [r for r in D['arator'] if r['pat']]
shA = [sum(1 for r in okA if r['pat'][f] == 'D') / len(okA) for f in range(4)]; shB = [sum(1 for r in okB if r['pat'][f] == 'D') / len(okB) for f in range(4)]
a1 = acc_dist(conv([sum(shA) / 4] * 32), conv([sum(shB) / 4] * 32)); a2 = acc_dist(conv(shA * 8), conv(shB * 8))
def line_dist(ok):
    c = collections.Counter(nd(r) for r in ok); one = [c[i] / len(ok) for i in range(5)]; d = [1.0]
    for _ in range(8): d = [sum(d[j] * one[i - j] for j in range(len(d)) if 0 <= i - j < 5) for i in range(len(d) + 4)]
    return d
a3 = acc_dist(line_dist(okA), line_dist(okB))
P(f"   32 separate feet, each a dactyl with the poem's overall share: {100 * a1:.1f}   (my sum on paper, with a round spread, gave 76)")
P(f"   32 separate feet, each with the share of its own place in the line: {100 * a2:.1f}")
P(f"   8 lines as the poets wrote them, each drawn separately from the whole poem (exact): {100 * a3:.1f}")
P(f"   8 lines in a row: {100 * CURVE[('aen', 'arator', 8)][0]:.1f}")
# elisions, which the notes leave out: counted for each scanned line as the vowels of its words less the syllables sounded
P('\nK. What the notes do not play: elisions.  Counted for every scanned line as the vowel groups of its words less the syllables the scan sounds (lines scanned with an option may be off by one).')
def nel(r): return sum(sum(1 for u in scan.segment(w) if u[0] == 'V') for w in r['words']) - len(r['q'])
EL = {}
for name in ('aen', 'arator'):
    for r in D[name]:
        if r['pat']: r['el'] = nel(r)
    ok = [r for r in D[name] if r['pat']]; EL[name] = [sum(r['el'] for r in w) for w in windows(D[name], 8)]
    P(f"   {NAME[name]}: {100 * sum(r['el'] for r in ok) / len(ok):.1f} elisions in 100 lines by this count; in eight lines in a row {sum(EL[name]) / len(EL[name]):.2f} on average; passages of eight lines with none: {100 * sum(1 for x in EL[name] if x == 0) / len(EL[name]):.1f}%")
best = max((0.5 * (sum(1 for x in EL['aen'] if x >= k) / len(EL['aen']) + sum(1 for x in EL['arator'] if x < k) / len(EL['arator'])), k) for k in range(0, 12))
P(f"   The rule 'Virgil at {best[1]} elisions or more in eight lines' is right {100 * best[0]:.1f} times in 100 (the count of dactyls: {100 * CURVE[('aen', 'arator', 8)][0]:.1f}).")
ELRULE = best
# ---------- the passages for the page
P('\nE. THE PASSAGES FOR THE PAGE: blocks of eight consecutive lines, cut from the start of each book (lines 1-8, 9-16, ...); a block is used only if the program scanned all eight lines as they stand')
P('   and, for the Aeneid, gave every one of the eight the same five feet as the reference.')
def blocks(name):
    rows = D[name]; byb = collections.OrderedDict()
    for i, r in enumerate(rows): byb.setdefault(r.get('book', 0), []).append((i, r))
    allb = []; good = []
    for b, L in byb.items():
        for j in range(0, len(L) - 7, 8):
            blk = L[j:j + 8]; allb.append(blk)
            if all(r['pat'] and r['how'] == 'plain' and (name != 'aen' or r['pat'] == r['ref']) for _, r in blk): good.append((b, j + 1, blk))
    return allb, good
def show_words(r):
    toks = re.split(r'[\s\-–—]+', r['text']); disp = []
    for t in toks:
        t2 = scan.strip_marks(t).replace('æ', 'ae').replace('œ', 'oe').replace('Æ', 'Ae').replace('Œ', 'Oe').replace('j', 'i').replace('J', 'I')
        if scan.clean_word(t): disp.append(t2)
        elif disp: disp[-1] += ' ' + t2
    assert len(disp) == len(r['words']), (r['text'], disp, r['words'])
    return disp
def pack(r): return dict(t=show_words(r), q=r['q'], w=''.join('0123456789abcdefghijklmnopqrstuvwxyz'[x] for x in r['w']))
POOL = {}; random.seed(544)
for name in ('aen', 'arator'):
    allb, good = blocks(name)
    da = sum(nd(r) for blk in allb for _, r in blk if r['pat']) / sum(1 for blk in allb for _, r in blk if r['pat']); dg = sum(nd(r) for _, _, blk in good for _, r in blk) / (8 * len(good))
    pick = sorted(random.sample(range(len(good)), 120)); chosen = [good[i] for i in pick]; dc = sum(nd(r) for _, _, blk in chosen for _, r in blk) / (8 * len(chosen))
    P(f"   {NAME[name]}: {len(allb)} blocks, {len(good)} usable; dactyls a line in all blocks {da:.3f}, in the usable ones {dg:.3f}, in the 120 drawn (seed 544) {dc:.3f}")
    POOL[name] = [dict(book=b, line=j, d=sum(nd(r) for _, r in blk), lines=[pack(r) for _, r in blk]) for b, j, blk in chosen]
lo = [p['d'] for p in POOL['aen']]; hi = [p['d'] for p in POOL['arator']]
acc, k = best_threshold(lo, hi)
P(f"   On these 240 passages the count rule with its own best k ({k}) is right on {100 * acc:.1f}%; with the k of the whole poems ({k8}) on {100 * 0.5 * (sum(1 for c in lo if c < k8) / 120 + sum(1 for c in hi if c >= k8) / 120):.1f}%.")
allk = {name: [sum(nd(r) for _, r in blk) for _, _, blk in blocks(name)[1]] for name in ('aen', 'arator')}
acc_all = 0.5 * (sum(1 for c in allk['aen'] if c < k8) / len(allk['aen']) + sum(1 for c in allk['arator'] if c >= k8) / len(allk['arator']))
rs = random.Random(1); got = []
for _ in range(20000):
    a_ = rs.sample(allk['aen'], 120); b_ = rs.sample(allk['arator'], 120); got.append(sum(1 for c in a_ if c < k8) + sum(1 for c in b_ if c >= k8))
got.sort(); right240 = sum(1 for c in lo if c < k8) + sum(1 for c in hi if c >= k8)
P(f"   On ALL the usable blocks the rule at {k8} is right on {sum(1 for c in allk['aen'] if c < k8)} of Virgil's {len(allk['aen'])} and {sum(1 for c in allk['arator'] if c >= k8)} of Arator's {len(allk['arator'])}: with the two poets equally likely, {100 * acc_all:.3f}%.  The game's 240: {right240} right ({sum(1 for c in lo if c < k8)} of Virgil's 120, {sum(1 for c in hi if c >= k8)} of Arator's 120).")
P(f"   Of 20,000 other draws of 120 and 120 from the usable blocks, {100 * sum(1 for g in got if g >= right240) / len(got):.1f}% had {right240} or more right; the middle 95% ran from {got[500]} to {got[19499]}.")
POOLSTAT = dict(acc_all=acc_all, right240=right240, share_ge=sum(1 for g in got if g >= right240) / len(got), lo95=got[500], hi95=got[19499], v_right=sum(1 for c in lo if c < k8), a_right=sum(1 for c in hi if c >= k8))
P(f"   Book sizes of the Aeneid in the reference's files: {dict(collections.Counter(r['book'] for r in D['aen']))}")
# the two passages played openly: among the usable blocks of each poem whose count of dactyls is the poem's average to the nearest whole number, the one whose dactyls fall foot by foot most like the poem's (the earliest in the poem if several are equally near)
DEMO = {}
for name in ('aen', 'arator'):
    ok = [r for r in D[name] if r['pat']]; feet = [8 * sum(1 for r in ok if r['pat'][f] == 'D') / len(ok) for f in range(4)]; target = round(sum(feet))
    allb, good = blocks(name); best = None
    for b, j, blk in good:
        if sum(nd(r) for _, r in blk) != target: continue
        dist = sum((sum(1 for _, r in blk if r['pat'][f] == 'D') - feet[f]) ** 2 for f in range(4))
        if best is None or dist < best[0] - 1e-9: best = (dist, b, j, blk)
    dist, b, j, blk = best
    same = [(b2, j2) for b2, j2, blk2 in good if sum(nd(r) for _, r in blk2) == target]; ties = sum(1 for b2, j2, blk2 in good if sum(nd(r) for _, r in blk2) == target and abs(sum((sum(1 for _, r in blk2 if r['pat'][f] == 'D') - feet[f]) ** 2 for f in range(4)) - dist) < 1e-9)
    P(f"   ({len(same)} usable blocks of {NAME[name]} have {target} dactyls, the first of them at {same[0][0]}.{same[0][1]}; {ties} are equally near the poem foot by foot, and the earliest of those is played)")
    DEMO[name] = dict(book=b, line=j, d=target, lines=[pack(r) for _, r in blk])
    P(f"   Played openly for {NAME[name]}: book {b}, lines {j}-{j + 7}: {target} dactyls (the poem's average in eight lines is {sum(feet):.2f}); by foot {[sum(1 for _, r in blk if r['pat'][f] == 'D') for f in range(4)]} against the average {[round(x, 1) for x in feet]}")
    for _, r in blk: P(f"       {r['pat']}  {r['q']}  {' '.join(show_words(r))}")
# single lines from the Aeneid: the lightest and the heaviest kind, and the line the quotation comes from
ONE = {}
for key, name, frag in (('light', 'aen', 'quadripedante putrem'), ('heavy', 'aen', 'inter sese multa vi bracchia'), ('spark', 'aen', 'possunt, quia posse videntur')):
    for r in D[name]:
        if frag in scan.strip_marks(r['text']).lower() and r['pat']:
            ONE[key] = dict(pack(r), book=r.get('book'), line=r.get('line')); P(f"   single line [{key}] {NAME[name]} {r.get('book')}.{r.get('line', '')}: {r['pat']} {r['q']} {' '.join(show_words(r))}   how: {r['how']}" + (f"  reference {r['ref']}" if name == 'aen' else '')); break
# do a poet's neighbouring lines differ more than chance would make them?  The spread of the eight-line count against the same lines in shuffled order (2,000 shuffles inside each book)
P('\nG. The spread (sd) of the count of dactyls in eight consecutive lines, against the same lines shuffled inside their books (2,000 shuffles):')
random.seed(544)
for name in ('aen', 'arator', 'juvencus'):
    rs = runs(D[name]); real = sd([sum(nd(r) for r in w) for w in windows(D[name], 8)]); sh = []
    for _ in range(2000 if name != 'aen' else 500):
        v = []
        for run in rs:
            x = [nd(r) for r in run]; random.shuffle(x); c = [0]
            for y in x: c.append(c[-1] + y)
            v += [c[i + 8] - c[i] for i in range(len(x) - 7)]
        sh.append(sd(v))
    sh.sort(); P(f"   {NAME[name]}: as written {real:.3f}; shuffled {sum(sh) / len(sh):.3f} on average, middle 95% {sh[int(.025 * len(sh))]:.3f} to {sh[int(.975 * len(sh))]:.3f}; shuffles with a spread as small as the real one or smaller: {sum(1 for x in sh if x <= real)} of {len(sh)}")
# a coin's chances, for the page's caution about ten rounds
from math import comb
P('\nF. A coin\'s chances in ten rounds: ' + ', '.join(f"{k} or more right {100 * sum(comb(10, j) for j in range(k, 11)) / 1024:.1f}%" for k in (6, 7, 8, 9, 10)))
pc = CURVE[('aen', 'arator', 8)][0]
P('   A perfect counter\'s chances in ten rounds (each right with chance %.3f): ' % pc + ', '.join(f"{k} or more {100 * sum(comb(10, j) * pc ** j * (1 - pc) ** (10 - j) for j in range(k, 11)):.1f}%" for k in (6, 7, 8, 9, 10)))
json.dump(dict(pool=POOL, demo=DEMO, one=ONE, hist=HIST, k8=k8, indep=INDEP, poolstat=POOLSTAT, elrule=ELRULE, steps=[a1, a2, a3], neigh=NEIGH, npass=[len(lo8), len(hi8)], mean8=[sum(lo8) / len(lo8), sum(hi8) / len(hi8)], curve={f'{a}-{b}-{n}': v for (a, b, n), v in CURVE.items()}), open('/home/agent1/arator/listen_pool.json', 'w'), ensure_ascii=False)
js = 'var LISTEN = ' + json.dumps(dict(pool=POOL, demo=DEMO, one=ONE), ensure_ascii=False, separators=(',', ':')) + ';\n'
open('/home/agent1/site/listen-data.js', 'w').write('// Passages for the listening page: written by listen_ideal.py (files/arator/). Text of Virgil and of Arator; the long and short marks are my program\'s.\n' + js)
P(f"\nwritten: listen_pool.json and ~/site/listen-data.js ({len(js) // 1024} KB)")
open('/home/agent1/arator/listen_ideal.out', 'w').write('\n'.join(out) + '\n')
