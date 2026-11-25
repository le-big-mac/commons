"""Do numbers decide battles?  The CDB90 table of 660 battles, 1600-1973.   usage: python -I battles.py DATADIR results.json
Rules are in expectations.md.  Details the sealed rules left open, settled after seeing the column names and
before computing (one slip: while listing which codes occur I had printed the counts of the winner code, which is
W1's answer; nothing settled below bears on W1):
 - strength is `str`, the database's "total personnel strength" (`intst`, the initial strength, is missing for 257 sides);
 - the year is the year of `datetime_min`; "before 1800" is year < 1800, "after 1900" is year > 1900;
 - a battle's length is `duration1`, the database's "battle duration in days";
 - the defence is `post1`, the defender's primary posture: PD or FD against HD;
 - surprise is `surpa`: above 0 the attacker's, 0 neither side's; battles where the defender had it are left out of W8;
 - W9 uses every battle with four positive numbers, draws included."""
import sys, csv, json, math
import numpy as np
D, OUT = sys.argv[1], sys.argv[2]
T = {r['isqno']: r for r in csv.DictReader(open(f"{D}/battles.csv", encoding='utf-8'))}
dur = {r['isqno']: r for r in csv.DictReader(open(f"{D}/battle_durations.csv", encoding='utf-8'))}
sides = {}
for r in csv.DictReader(open(f"{D}/belligerents.csv", encoding='utf-8')):
    sides[(r['isqno'], r['attacker'])] = r
num = lambda s: float(s) if s not in ('', None) else float('nan')
rows = []
for q, t in T.items():
    a, d = sides[(q, '1')], sides[(q, '0')]
    rows.append(dict(q=q, name=t['name'], year=int(dur[q]['datetime_min'][:4]), win=(int(t['wina']) if t['wina'] != '' else None), surp=int(t['surpa']) if t['surpa'] != '' else None, post=t['post1'],
                     days=num(dur[q]['duration1']), sa=num(a['str']), sd=num(d['str']), ca=num(a['cas']), cd=num(d['cas']), war=t['war']))
dec = [r for r in rows if r['win'] in (1, -1)]
print(f"{len(rows)} battles, {min(r['year'] for r in rows)} to {max(r['year'] for r in rows)}; attacker won {sum(r['win'] == 1 for r in dec)}, defender won {sum(r['win'] == -1 for r in dec)}, "
      f"draws {sum(r['win'] == 0 for r in rows)}, no winner coded {sum(r['win'] is None for r in rows)}")
res = {}
def say(tag, text, ok):
    res[tag] = bool(ok)
    print(f"{tag:4s} {text}  ->  {'held' if ok else 'failed'}")
def wilson(k, n, z=1.96):
    if n == 0:
        return (float('nan'), float('nan'))
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h
def share(sel):
    k, n = sum(r['win'] == 1 for r in sel), len(sel)
    return k, n, (k / n if n else float('nan'))
ok = lambda *v: all(np.isfinite(x) and x > 0 for x in v)

k, n, p = share(dec)
say('W1', f"attackers won {k} of {n} decisive battles = {100 * p:.1f}%", p >= 0.55)
uneq = [r for r in dec if ok(r['sa'], r['sd']) and r['sa'] != r['sd']]
big = sum((r['sa'] > r['sd']) == (r['win'] == 1) for r in uneq)
say('W2', f"the side with more men won {big} of {len(uneq)} = {100 * big / len(uneq):.1f}%", 0.45 <= big / len(uneq) <= 0.62)
fr = [r for r in dec if ok(r['sa'], r['sd'])]
won = np.array([r['sa'] / r['sd'] for r in fr if r['win'] == 1]); lost = np.array([r['sa'] / r['sd'] for r in fr if r['win'] == -1])
auc = float(((won[:, None] > lost[None, :]).sum() + 0.5 * (won[:, None] == lost[None, :]).sum()) / (len(won) * len(lost)))
say('W3', f"force ratio ranks an attacker's win above a defender's with probability {auc:.3f} ({len(won)} wins, {len(lost)} losses; median ratio {np.median(won):.2f} in wins, {np.median(lost):.2f} in losses)", 0.50 <= auc <= 0.62)
three = [r for r in fr if r['sa'] / r['sd'] >= 3]
k, n, p = share(three); lo, hi = wilson(k, n)
say('W4', f"attackers with three to one or more won {k} of {n} = {100 * p:.1f}% (95% interval {100 * lo:.0f} to {100 * hi:.0f})", p >= 0.65)
fewer = [r for r in fr if r['sa'] < r['sd']]
k, n, p = share(fewer); lo, hi = wilson(k, n)
say('W5', f"attackers with fewer men won {k} of {n} = {100 * p:.1f}% (95% interval {100 * lo:.0f} to {100 * hi:.0f})", p >= 0.5)
cs = [r for r in dec if ok(r['sa'], r['sd']) and np.isfinite(r['ca']) and np.isfinite(r['cd'])]
loser_more = sum(((r['cd'] / r['sd']) > (r['ca'] / r['sa'])) == (r['win'] == 1) and (r['cd'] / r['sd']) != (r['ca'] / r['sa']) for r in cs)
say('W6', f"the loser's casualty share was the larger in {loser_more} of {len(cs)} = {100 * loser_more / len(cs):.1f}%", loser_more / len(cs) >= 0.75)
def shares(sel):
    out = []
    for r in sel:
        if ok(r['sa']) and np.isfinite(r['ca']): out.append(r['ca'] / r['sa'])
        if ok(r['sd']) and np.isfinite(r['cd']): out.append(r['cd'] / r['sd'])
    return np.array(out)
early, late = shares([r for r in rows if r['year'] < 1800]), shares([r for r in rows if r['year'] > 1900])
say('W7', f"median casualty share: before 1800 {100 * np.median(early):.1f}% ({len(early)} sides); after 1900 {100 * np.median(late):.1f}% ({len(late)} sides)", np.median(late) < 0.5 * np.median(early))
s1 = [r for r in dec if r['surp'] is not None and r['surp'] > 0]; s0 = [r for r in dec if r['surp'] == 0]
k1, n1, p1 = share(s1); k0, n0, p0 = share(s0)
say('W8', f"attackers with surprise won {k1} of {n1} = {100 * p1:.1f}%; with no surprise on either side {k0} of {n0} = {100 * p0:.1f}%; difference {100 * (p1 - p0):+.1f} points", p1 - p0 >= 0.15)
lc = [r for r in rows if ok(r['sa'], r['sd'], r['ca'], r['cd'])]
x = np.log([r['sa'] / r['sd'] for r in lc]); y = np.log([r['ca'] / r['cd'] for r in lc])
rr = float(np.corrcoef(x, y)[0, 1]); slope, icpt = np.polyfit(x, y, 1)
say('W9', f"correlation of log force ratio with log casualty ratio: {rr:+.3f} over {len(lc)} battles (slope {slope:+.2f})", rr > 0)
d_early = np.array([r['days'] for r in rows if r['year'] < 1850 and np.isfinite(r['days'])]); d_late = np.array([r['days'] for r in rows if r['year'] > 1900 and np.isfinite(r['days'])])
say('W10', f"median length: before 1850 {np.median(d_early):g} days ({len(d_early)} battles); after 1900 {np.median(d_late):g} days ({len(d_late)})", np.median(d_early) == 1 and np.median(d_late) >= 2)
prep = [r for r in dec if r['post'] in ('PD', 'FD')]; hasty = [r for r in dec if r['post'] == 'HD']
kp, np_, pp = share(prep); kh, nh, ph = share(hasty)
say('W11', f"attackers won {kp} of {np_} = {100 * pp:.1f}% against prepared or fortified defences and {kh} of {nh} = {100 * ph:.1f}% against hasty ones; difference {100 * (ph - pp):+.1f} points", ph - pp >= 0.10)

print("afterwards, not registered:")
bands = [(0, 0.5), (0.5, 0.75), (0.75, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0, 3.0), (3.0, 99)]
band_out = []
print("   attacker's share of wins by force ratio:")
for lo_, hi_ in bands:
    sel = [r for r in fr if lo_ <= r['sa'] / r['sd'] < hi_]
    k, n, p = share(sel); a, b = wilson(k, n)
    band_out.append(dict(lo=lo_, hi=hi_, k=k, n=n, p=p, ci=(a, b)))
    print(f"      {lo_:.2f} to {hi_ if hi_ < 99 else 'more':>4}: {k:3d} of {n:3d} = {100 * p:5.1f}%  ({100 * a:.0f} to {100 * b:.0f})")
era_out = []
for lo_, hi_, nm in ((1600, 1799, '1600-1799'), (1800, 1899, '1800-1899'), (1900, 1945, '1900-1945'), (1946, 1982, '1946-1982')):
    sel = [r for r in dec if lo_ <= r['year'] <= hi_]; f2 = [r for r in sel if ok(r['sa'], r['sd'])]
    k, n, p = share(sel)
    u = [r for r in f2 if r['sa'] != r['sd']]; bg = sum((r['sa'] > r['sd']) == (r['win'] == 1) for r in u)
    t3 = [r for r in f2 if r['sa'] / r['sd'] >= 3]; k3, n3, p3 = share(t3)
    out_n = [r for r in f2 if r['sa'] < r['sd']]; ko, no, po = share(out_n)
    wl = [(r['ca'] / r['sa'], r['cd'] / r['sd']) if r['win'] == 1 else (r['cd'] / r['sd'], r['ca'] / r['sa']) for r in sel if ok(r['sa'], r['sd']) and np.isfinite(r['ca']) and np.isfinite(r['cd'])]
    mw, ml = float(np.median([a for a, b in wl])), float(np.median([b for a, b in wl]))
    aa = np.array([r['sa'] / r['sd'] for r in f2 if r['win'] == 1]); bb = np.array([r['sa'] / r['sd'] for r in f2 if r['win'] == -1])
    au = float(((aa[:, None] > bb[None, :]).sum() + 0.5 * (aa[:, None] == bb[None, :]).sum()) / (len(aa) * len(bb)))
    era_out.append(dict(era=nm, n=n, attacker=p, bigger=bg / len(u), three=(k3, n3), fewer=(ko, no), winner=mw, loser=ml, auc=au, days=float(np.median([r['days'] for r in sel if np.isfinite(r['days'])]))))
    print(f"   {nm}: {n} decisive; attacker won {100 * p:.0f}%; the bigger side won {100 * bg / len(u):.0f}%; three to one: {k3} of {n3}; fewer men: {ko} of {no}; ranking by ratio {au:.2f}; "
          f"median casualty share winner {100 * mw:.1f}%, loser {100 * ml:.1f}%; median length {era_out[-1]['days']:g} days")
wars = {}
for r in dec:
    wars.setdefault(r['war'], []).append(r)
top = sorted(wars.items(), key=lambda kv: -len(kv[1]))[:6]
print(f"   {len(wars)} wars; the six with most battles: " + "; ".join(f"{w.title()[:28]} {len(v)}" for w, v in top) + f"; together {sum(len(v) for w, v in top)} of {len(dec)}")
rng = np.random.default_rng(0); wl_ = list(wars); bs = []
for _ in range(4000):
    pick = rng.integers(0, len(wl_), len(wl_))
    sel = [r for j in pick for r in wars[wl_[j]] if ok(r['sa'], r['sd']) and r['sa'] / r['sd'] >= 3]
    if sel: bs.append(sum(r['win'] == 1 for r in sel) / len(sel))
print(f"   three to one, resampling whole wars: 95% interval {100 * np.percentile(bs, 2.5):.0f} to {100 * np.percentile(bs, 97.5):.0f}")
print(f"   W9 slope: one more unit of log force ratio goes with {slope:+.2f} of log casualty ratio (0 would mean losses do not depend on relative size; 1 that they are proportional to it; Lanchester's square law says -1)")
json.dump(dict(verdicts=res, bands=band_out, eras=era_out, auc=auc, n=len(rows)), open(OUT, 'w'), indent=1)

# ---- afterwards: is the prepared-defence result a matter of who dares to attack what?
print("afterwards: prepared or fortified against hasty defences")
for nm, sel in (("prepared or fortified", prep), ("hasty", hasty)):
    f2 = [r for r in sel if ok(r['sa'], r['sd'])]
    print(f"   {nm}: median force ratio {np.median([r['sa'] / r['sd'] for r in f2]):.2f}; share with surprise {100 * np.mean([r['surp'] is not None and r['surp'] > 0 for r in sel]):.0f}%; "
          f"share after 1900 {100 * np.mean([r['year'] > 1900 for r in sel]):.0f}%; median attacker's casualty share {100 * np.median([r['ca'] / r['sa'] for r in f2 if np.isfinite(r['ca'])]):.1f}%")
for lo_, hi_ in ((0, 1.0), (1.0, 2.0), (2.0, 99)):
    a = [r for r in prep if ok(r['sa'], r['sd']) and lo_ <= r['sa'] / r['sd'] < hi_]; b = [r for r in hasty if ok(r['sa'], r['sd']) and lo_ <= r['sa'] / r['sd'] < hi_]
    print(f"   force ratio {lo_:g} to {hi_ if hi_ < 99 else 'more'}: against prepared {share(a)[0]} of {share(a)[1]} = {100 * share(a)[2]:.0f}%; against hasty {share(b)[0]} of {share(b)[1]} = {100 * share(b)[2]:.0f}%")
for nm, lo_, hi_ in (("before 1900", 0, 1899), ("1900 on", 1900, 2000)):
    a = [r for r in prep if lo_ <= r['year'] <= hi_]; b = [r for r in hasty if lo_ <= r['year'] <= hi_]
    print(f"   {nm}: against prepared {share(a)[0]} of {share(a)[1]} = {100 * share(a)[2]:.0f}%; against hasty {share(b)[0]} of {share(b)[1]} = {100 * share(b)[2]:.0f}%")
print("afterwards: surprise by size")
for v in (0, 1, 2, 3):
    sel = [r for r in dec if r['surp'] == v]; k, n, p = share(sel)
    print(f"   surprise code {v}: attacker won {k} of {n} = {100 * p:.0f}%")
sel = [r for r in dec if r['surp'] is not None and r['surp'] < 0]; k, n, p = share(sel)
print(f"   surprise by the defender: attacker won {k} of {n}")

# ---- afterwards: two checks on what the numbers rest on
print("afterwards: initial strength in place of total strength, where the database gives it")
ist = {}
for (q, att), r in sides.items():
    ist[(q, att)] = num(r['intst'])
f3 = [dict(r, sa=ist[(r['q'], '1')], sd=ist[(r['q'], '0')]) for r in dec if ok(ist[(r['q'], '1')], ist[(r['q'], '0')])]
u = [r for r in f3 if r['sa'] != r['sd']]; bg = sum((r['sa'] > r['sd']) == (r['win'] == 1) for r in u)
t3 = [r for r in f3 if r['sa'] / r['sd'] >= 3]; fw = [r for r in f3 if r['sa'] < r['sd']]
print(f"   {len(f3)} decisive battles have both: the bigger side won {100 * bg / len(u):.1f}%; three to one {share(t3)[0]} of {share(t3)[1]} = {100 * share(t3)[2]:.1f}%; fewer men {share(fw)[0]} of {share(fw)[1]} = {100 * share(fw)[2]:.1f}%")
print("afterwards: every war counted once (the mean over wars of each war's own share)")
def per_war(fn):
    vals = [fn(v) for v in wars.values()]
    vals = [x for x in vals if x is not None]
    return 100 * float(np.mean(vals)), len(vals)
def w_att(v):
    return sum(r['win'] == 1 for r in v) / len(v)
def w_big(v):
    u = [r for r in v if ok(r['sa'], r['sd']) and r['sa'] != r['sd']]
    return (sum((r['sa'] > r['sd']) == (r['win'] == 1) for r in u) / len(u)) if u else None
def w_three(v):
    u = [r for r in v if ok(r['sa'], r['sd']) and r['sa'] / r['sd'] >= 3]
    return (sum(r['win'] == 1 for r in u) / len(u)) if u else None
def w_few(v):
    u = [r for r in v if ok(r['sa'], r['sd']) and r['sa'] < r['sd']]
    return (sum(r['win'] == 1 for r in u) / len(u)) if u else None
for nm, fn in (("the attacker won", w_att), ("the bigger side won", w_big), ("attackers with three to one won", w_three), ("attackers with fewer men won", w_few)):
    m, n = per_war(fn)
    print(f"   {nm}: {m:.1f}% over {n} wars")

# ---- after the referee: its main findings, recomputed here
print("after the referee:")
ww = lambda r: 'WORLD WAR' in r['war'].upper()
def rank(sel):
    aa = np.array([r['sa'] / r['sd'] for r in sel if r['win'] == 1]); bb = np.array([r['sa'] / r['sd'] for r in sel if r['win'] == -1])
    return float(((aa[:, None] > bb[None, :]).sum() + 0.5 * (aa[:, None] == bb[None, :]).sum()) / (len(aa) * len(bb)))
split = {}
for nm, sel in (("world-war rows", [r for r in fr if ww(r)]), ("all other rows", [r for r in fr if not ww(r)])):
    u = [r for r in sel if r['sa'] != r['sd']]; bg = sum((r['sa'] > r['sd']) == (r['win'] == 1) for r in u)
    lo_, hi_ = wilson(bg, len(u))
    bandrows = []
    for a_, b_ in bands:
        s2 = [r for r in sel if a_ <= r['sa'] / r['sd'] < b_]; k, n, p = share(s2); c1, c2 = wilson(k, n)
        bandrows.append(dict(k=k, n=n, p=p, ci=(c1, c2)))
    split[nm] = dict(bigger=bg / len(u), n=len(u), rank=rank(sel), bands=bandrows, attacker=share(sel)[2])
    print(f"   {nm}: the bigger side won {bg} of {len(u)} = {100 * bg / len(u):.1f}% ({100 * lo_:.0f} to {100 * hi_:.0f}); ranking by force ratio {rank(sel):.3f}; attacker won {100 * share(sel)[2]:.1f}%; "
          + "by band: " + ", ".join(f"{x['k']}/{x['n']}" for x in bandrows))
out3 = [r for r in fr if r['sa'] / r['sd'] >= 3 and not (1900 <= r['year'] <= 1945)]; k, n, p = share(out3); c1, c2 = wilson(k, n)
print(f"   three to one or more outside 1900-1945: {k} of {n} = {100 * p:.1f}% ({100 * c1:.0f} to {100 * c2:.0f}); under three to one in those years: {100 * share([r for r in fr if r['sa'] / r['sd'] < 3 and not (1900 <= r['year'] <= 1945)])[2]:.1f}%")
for thr in (2, 3, 4, 5):
    s2 = [r for r in fr if r['sa'] / r['sd'] >= thr]; print(f"      at {thr} to one or more: {share(s2)[0]} of {share(s2)[1]} = {100 * share(s2)[2]:.1f}%")
for nm, lo_, hi_ in (("before 1800", 0, 1799), ("1800 to 1945", 1800, 1945), ("after 1945", 1946, 2000)):
    s2 = [r for r in fewer if lo_ <= r['year'] <= hi_]; print(f"   attackers with fewer men, {nm}: {share(s2)[0]} of {share(s2)[1]} = {100 * share(s2)[2]:.0f}%")
print("   median casualty share by period: " + "; ".join(f"{a_}-{b_}: {100 * np.median(shares([r for r in rows if a_ <= r['year'] <= b_])):.1f}%" for a_, b_ in ((1600, 1699), (1700, 1799), (1800, 1849), (1850, 1900), (1914, 1918), (1939, 1945), (1946, 1982))))
absm = sum((r['cd'] > r['ca']) == (r['win'] == 1) and r['cd'] != r['ca'] for r in cs)
dfl = sum((r['cd'] / r['sd']) > (r['ca'] / r['sa']) for r in cs)
print(f"   the loser lost more men in absolute numbers in {absm} of {len(cs)} = {100 * absm / len(cs):.1f}%; the defender had the larger share in {100 * dfl / len(cs):.1f}% of decisive battles whoever won; "
      f"the loser's casualties are at least half its strength in {sum((r['cd'] / r['sd'] if r['win'] == 1 else r['ca'] / r['sa']) >= 0.5 for r in cs)} battles")
import datetime as _dt
def span(q):
    a_ = _dt.datetime.fromisoformat(dur[q]['datetime_min']); b_ = _dt.datetime.fromisoformat(dur[q]['datetime_max'])
    return (b_ - a_).total_seconds() / 86400.0, (b_.date() - a_.date()).days + 1
for nm, sel in (("before 1850", [r for r in rows if r['year'] < 1850]), ("after 1900", [r for r in rows if r['year'] > 1900])):
    sp = [span(r['q']) for r in sel]; d2 = [num(dur[r['q']]['duration2']) for r in sel]
    print(f"   length {nm}: the table's duration1 median {np.median([r['days'] for r in sel]):g}; its active-time column {np.nanmedian(d2):.2f} days; from start to end {np.median([s[0] for s in sp]):.2f} days; calendar dates touched {np.median([s[1] for s in sp]):g}")
late = [r for r in rows if r['year'] > 1900]
print(f"   after 1900, {sum(r['days'] == 2 for r in late)} of {len(late)} rows have duration1 exactly 2")
print(f"   rows that are parts of another row (the `parent` column): {sum(1 for t in T.values() if t.get('parent', '') not in ('', None))}")
json.dump(dict(json.load(open(OUT)), split=split), open(OUT, 'w'), indent=1)
