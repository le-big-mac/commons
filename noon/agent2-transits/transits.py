"""Known patterns among transiting planets, looked for in the plain catalogue.   usage: python -I transits.py pscomppars.csv results.json
Rules are in expectations.md.  Details the sealed rules left open, settled after seeing the column names (not the
values) and before computing:
 - the table is `pscomppars`, one row per planet; a planet counts if `discoverymethod` is "Transit", flagged controversial or not;
 - size is `pl_rade`, period `pl_orbper`, the star's metallicity `st_met` (whichever ratio the table quotes), temperature `st_teff`;
 - "the only known planet of its star" is `sy_pnum` = 1;
 - "a stated eccentricity" is any value in `pl_orbeccen`, zeros included;
 - neighbours are found among the transit-discovered planets of one `hostname` that have a period, ordered by period;
 - the year is `disc_year`."""
import sys, csv, json, math, collections
import numpy as np
SRC, OUT = sys.argv[1], sys.argv[2]
num = lambda s: float(s) if s not in ('', None) else float('nan')
rows = []
for r in csv.DictReader(open(SRC, encoding='utf-8')):
    rows.append(dict(name=r['pl_name'], host=r['hostname'], method=r['discoverymethod'], year=int(r['disc_year']) if r['disc_year'] else None, fac=r['disc_facility'], npl=int(r['sy_pnum']) if r['sy_pnum'] else None,
                     P=num(r['pl_orbper']), R=num(r['pl_rade']), e=num(r['pl_orbeccen']), teff=num(r['st_teff']), met=num(r['st_met']), srad=num(r['st_rad']), elim=r['pl_orbeccenlim'], Rerr=(num(r['pl_radeerr1']) - num(r['pl_radeerr2'])) / 2))
T = [r for r in rows if r['method'] == 'Transit']
fin = np.isfinite
print(f"{len(rows)} planets in the table; {len(T)} found by transit; of those {sum(fin(r['R']) for r in T)} have a size, {sum(fin(r['P']) for r in T)} a period")
res = {}
def say(tag, text, ok):
    res[tag] = bool(ok)
    print(f"{tag:4s} {text}  ->  {'held' if ok else 'failed'}")
def wilson(k, n, z=1.96):
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h

PR = [r for r in T if fin(r['P']) and fin(r['R'])]
s100 = [r for r in PR if r['P'] < 100]
edges = [1.26, 1.58, 2.00, 2.51]
c = [sum(edges[i] <= r['R'] < edges[i + 1] for r in s100) for i in range(3)]
say('X1', f"planets under 100 days in the three bins 1.26-1.58, 1.58-2.00, 2.00-2.51 Earth radii: {c[0]}, {c[1]}, {c[2]}", c[1] < c[0] and c[1] < c[2])
hj = [r for r in PR if r['R'] >= 8 and r['P'] < 10]; small = [r for r in PR if r['R'] < 4]
mh = np.array([r['met'] for r in hj if fin(r['met'])]); ms = np.array([r['met'] for r in small if fin(r['met'])])
say('X2', f"mean metallicity of the stars: hot Jupiters {mh.mean():+.3f} ({len(mh)} planets); planets under 4 Earth radii {ms.mean():+.3f} ({len(ms)}); difference {mh.mean() - ms.mean():+.3f} dex "
          f"(one standard error {math.sqrt(mh.var(ddof=1) / len(mh) + ms.var(ddof=1) / len(ms)):.3f})", mh.mean() - ms.mean() >= 0.08)
p3 = [r for r in PR if r['P'] < 3]; nep = sum(3 <= r['R'] < 8 for r in p3)
say('X3', f"of {len(p3)} planets with periods under 3 days, {nep} have sizes from 3 to 8 Earth radii = {100 * nep / len(p3):.1f}%", nep / len(p3) < 0.08)
per = np.array([r['P'] for r in T if fin(r['P'])])
say('X4', f"median period of {len(per)} transit planets: {np.median(per):.2f} days", 5 <= np.median(per) <= 15)
sysm = collections.defaultdict(list)
for r in T:
    if fin(r['P']):
        sysm[r['host']].append(r)
pairs = []
for h, v in sysm.items():
    v.sort(key=lambda r: r['P'])
    for a, b in zip(v[:-1], v[1:]):
        pairs.append((a, b))
pr = [(a, b) for a, b in pairs if fin(a['R']) and fin(b['R'])]
x = np.log10([a['R'] for a, b in pr]); y = np.log10([b['R'] for a, b in pr])
rr = float(np.corrcoef(x, y)[0, 1])
say('X5', f"correlation of the logarithms of neighbours' sizes: {rr:+.3f} over {len(pr)} pairs in {len([h for h, v in sysm.items() if len(v) > 1])} systems", rr >= 0.4)
outer = sum(b['R'] > a['R'] for a, b in pr); ties = sum(b['R'] == a['R'] for a, b in pr)
say('X6', f"the outer neighbour is the larger in {outer} of {len(pr)} pairs = {100 * outer / len(pr):.1f}% ({ties} ties)", outer / len(pr) >= 0.55)
ratio = np.array([b['P'] / a['P'] for a, b in pairs])
w32, n32 = int(((ratio >= 1.50) & (ratio < 1.53)).sum()), int(((ratio >= 1.47) & (ratio < 1.50)).sum())
say('X7', f"pairs with a period ratio from 1.50 to 1.53: {w32}; from 1.47 to 1.50: {n32}; ratio {w32 / max(n32, 1):.2f}", w32 > 1.5 * n32)
w21, n21 = int(((ratio >= 2.00) & (ratio < 2.04)).sum()), int(((ratio >= 1.96) & (ratio < 2.00)).sum())
say('X8', f"pairs with a period ratio from 2.00 to 2.04: {w21}; from 1.96 to 2.00: {n21}; ratio {w21 / max(n21, 1):.2f}", w21 > 1.3 * n21)
alone = sum(r['npl'] == 1 for r in hj)
lo, hi = wilson(alone, len(hj))
say('X9', f"{alone} of {len(hj)} hot Jupiters are the only known planet of their star = {100 * alone / len(hj):.1f}% ({100 * lo:.0f} to {100 * hi:.0f})", alone / len(hj) >= 0.90)
g = [r for r in PR if r['R'] >= 8 and fin(r['e'])]
e_in = np.array([r['e'] for r in g if r['P'] < 5]); e_out = np.array([r['e'] for r in g if r['P'] > 20])
say('X10', f"median eccentricity of planets of 8 Earth radii or more: periods under 5 days {np.median(e_in):.3f} ({len(e_in)} planets); over 20 days {np.median(e_out):.3f} ({len(e_out)})", np.median(e_in) < 0.05 and np.median(e_out) > 0.10)
hot = [r for r in T if fin(r['R']) and fin(r['teff']) and r['teff'] >= 5000]; cool = [r for r in T if fin(r['R']) and fin(r['teff']) and r['teff'] < 3900]
gh, gc = sum(r['R'] >= 8 for r in hot) / len(hot), sum(r['R'] >= 8 for r in cool) / len(cool)
say('X11', f"share of planets of 8 Earth radii or more: stars of 5,000 K or hotter {100 * gh:.1f}% of {len(hot)}; stars under 3,900 K {100 * gc:.1f}% of {len(cool)}; ratio {gh / gc:.2f}", gh >= 3 * gc)
new = np.array([r['R'] for r in T if fin(r['R']) and r['year'] is not None and r['year'] >= 2019]); kep = np.array([r['R'] for r in T if fin(r['R']) and r['year'] is not None and 2014 <= r['year'] <= 2016])
say('X12', f"median size: discovered 2019 or later {np.median(new):.2f} Earth radii ({len(new)}); 2014 to 2016 {np.median(kep):.2f} ({len(kep)})", np.median(new) > np.median(kep))

print("afterwards, not registered:")
fac = collections.Counter(r['fac'] for r in T)
print("   found by: " + "; ".join(f"{k} {v}" for k, v in fac.most_common(5)))
kepler = lambda r: r['fac'] in ('Kepler', 'K2')
for nm, sel in (("Kepler and K2", [r for r in s100 if kepler(r)]), ("all others", [r for r in s100 if not kepler(r)])):
    cc = [sum(edges[i] <= r['R'] < edges[i + 1] for r in sel) for i in range(3)]
    print(f"   the three size bins, {nm}: {cc[0]}, {cc[1]}, {cc[2]}")
fine = np.round(np.logspace(np.log10(1.0), np.log10(4.0), 13), 3)
hist = [int(sum(fine[i] <= r['R'] < fine[i + 1] for r in s100)) for i in range(12)]
print("   twelve finer bins from 1 to 4 Earth radii: " + ", ".join(f"{fine[i]:.2f}:{hist[i]}" for i in range(12)))
good = [r for r in s100 if fin(r['Rerr']) and r['Rerr'] / r['R'] < 0.08]
cc = [sum(edges[i] <= r['R'] < edges[i + 1] for r in good) for i in range(3)]
print(f"   the three bins among the {len(good)} planets whose size is known to better than 8%: {cc[0]}, {cc[1]}, {cc[2]}")
print(f"   hot Jupiters with company: " + "; ".join(sorted(set(r['host'] for r in hj if r['npl'] and r['npl'] > 1))[:14]))
ez = [r for r in g if r['e'] > 0]
print(f"   eccentricity, exact zeros left out: under 5 days {np.median([r['e'] for r in ez if r['P'] < 5]):.3f} ({sum(r['P'] < 5 for r in ez)}); over 20 days {np.median([r['e'] for r in ez if r['P'] > 20]):.3f} ({sum(r['P'] > 20 for r in ez)}); "
      f"share of exact zeros under 5 days {100 * np.mean(e_in == 0):.0f}%, over 20 days {100 * np.mean(e_out == 0):.0f}%")
for lo_, hi_ in ((1.3, 1.47), (1.47, 1.50), (1.50, 1.53), (1.53, 1.7), (1.9, 1.96), (1.96, 2.00), (2.00, 2.04), (2.04, 2.1)):
    print(f"   period ratio {lo_:.2f} to {hi_:.2f}: {int(((ratio >= lo_) & (ratio < hi_)).sum())} pairs", end=';')
print()
rng = np.random.default_rng(0)
shuf = []
allR = np.array([r['R'] for r in PR if any(r is q for a, b in pr for q in (a, b))]) if False else np.array([a['R'] for a, b in pr] + [b['R'] for a, b in pr])
for _ in range(2000):
    yy = rng.permutation(y)
    shuf.append(np.corrcoef(x, yy)[0, 1])
print(f"   neighbours' sizes with the outer ones shuffled between systems: correlation {np.mean(shuf):+.3f} (95% of shuffles under {np.percentile(shuf, 95):+.3f})")
samestar = [(a, b) for a, b in pr if kepler(a) and kepler(b)]
print(f"   neighbours both found by Kepler or K2: {len(samestar)} pairs, correlation {np.corrcoef(np.log10([a['R'] for a, b in samestar]), np.log10([b['R'] for a, b in samestar]))[0, 1]:+.3f}")
# ---- afterwards: a simple control for each pattern that held
print("afterwards: controls")
kh = np.array([r['met'] for r in hj if kepler(r) and fin(r['met'])]); ks = np.array([r['met'] for r in small if kepler(r) and fin(r['met'])])
print(f"   metallicity within Kepler and K2 discoveries only: hot Jupiters {kh.mean():+.3f} ({len(kh)}); under 4 Earth radii {ks.mean():+.3f} ({len(ks)}); difference {kh.mean() - ks.mean():+.3f} "
      f"(one standard error {math.sqrt(kh.var(ddof=1) / len(kh) + ks.var(ddof=1) / len(ks)):.3f})")
for lo_, hi_ in ((0, 3), (3, 10), (10, 30), (30, 100)):
    sel = [r for r in PR if lo_ <= r['P'] < hi_]; k = sum(3 <= r['R'] < 8 for r in sel)
    print(f"   share of sizes from 3 to 8 Earth radii at periods {lo_} to {hi_} days: {k} of {len(sel)} = {100 * k / len(sel):.1f}%")
both = [(a, b) for a, b in pr if fin(a['srad']) and fin(b['srad']) and a['srad'] > 0]
allp = [r for r in PR if fin(r['srad']) and r['srad'] > 0 and r['R'] < 6]
sl, ic = np.polyfit(np.log10([r['srad'] for r in allp]), np.log10([r['R'] for r in allp]), 1)
small_pairs = [(a, b) for a, b in both if a['R'] < 6 and b['R'] < 6]
ra = np.array([np.log10(a['R']) - (ic + sl * np.log10(a['srad'])) for a, b in small_pairs]); rb = np.array([np.log10(b['R']) - (ic + sl * np.log10(b['srad'])) for a, b in small_pairs])
raw = np.corrcoef(np.log10([a['R'] for a, b in small_pairs]), np.log10([b['R'] for a, b in small_pairs]))[0, 1]
print(f"   neighbours under 6 Earth radii ({len(small_pairs)} pairs): correlation {raw:+.3f}; after taking out what the star's size predicts (planet size goes as star size to the {sl:.2f}): {np.corrcoef(ra, rb)[0, 1]:+.3f}")
for nm, test in (("found from the ground", lambda r: r['fac'] not in ('Kepler', 'K2', 'Transiting Exoplanet Survey Satellite (TESS)')), ("found by Kepler or K2", kepler), ("found by TESS", lambda r: 'TESS' in r['fac'])):
    sel = [r for r in hj if test(r)]; k = sum(r['npl'] == 1 for r in sel)
    print(f"   hot Jupiters {nm}: {k} of {len(sel)} alone = {100 * k / len(sel):.1f}%")
kp = [(a, b) for a, b in pairs if kepler(a) and kepler(b)]; rk = np.array([b['P'] / a['P'] for a, b in kp])
print(f"   period ratios among Kepler and K2 pairs only: 1.47-1.50 {int(((rk >= 1.47) & (rk < 1.50)).sum())}, 1.50-1.53 {int(((rk >= 1.50) & (rk < 1.53)).sum())}; 1.96-2.00 {int(((rk >= 1.96) & (rk < 2.00)).sum())}, 2.00-2.04 {int(((rk >= 2.00) & (rk < 2.04)).sum())}; all pairs {len(rk)}")
# ---- after the referee: its main points, recomputed here
print("after the referee:")
g5 = [r for r in g if r['P'] < 5]; g20 = [r for r in g if r['P'] > 20]
meas5 = [r['e'] for r in g5 if r['e'] > 0 and r['elim'] in ('0', '0.0', '')]; meas20 = [r['e'] for r in g20 if r['e'] > 0 and r['elim'] in ('0', '0.0', '')]
print(f"   X10: of {len(g5)} giants under 5 days, {sum(r['e'] == 0 for r in g5)} have an eccentricity of exactly zero and {sum(r['elim'] not in ('0', '0.0', '') for r in g5)} an upper limit; "
      f"measured values only: median {np.median(meas5):.3f} ({len(meas5)} planets) under 5 days, {np.median(meas20):.3f} ({len(meas20)}) over 20 days")
print("   X10 held by the sealed letter only because the catalogue's assumed zeros count as stated values; the verdict stays as sealed")
sh = []
ins = np.array([a['R'] for a, b in pr]); outs = np.array([b['R'] for a, b in pr])
for _ in range(2000):
    sh.append(np.mean(rng.permutation(outs) > ins))
print(f"   the outer neighbour is the larger in {100 * outer / len(pr):.1f}% of pairs; with outer planets shuffled between systems {100 * np.mean(sh):.1f}% ({100 * np.percentile(sh, 2.5):.1f} to {100 * np.percentile(sh, 97.5):.1f})")
tess = lambda r: 'TESS' in r['fac']
for nm, test in (("Kepler and K2", kepler), ("TESS", tess), ("all others", lambda r: not kepler(r) and not tess(r))):
    out_ = []
    for lo_, hi_ in ((0, 3), (3, 10), (10, 30)):
        sel = [r for r in PR if test(r) and lo_ <= r['P'] < hi_]; k = sum(3 <= r['R'] < 8 for r in sel)
        out_.append(f"{k} of {len(sel)} = {100 * k / max(len(sel), 1):.1f}%")
    print(f"   sizes 3 to 8 Earth radii, {nm}, periods under 3, 3 to 10, 10 to 30 days: " + "; ".join(out_))
for nm, test in (("Kepler and K2", kepler), ("TESS", tess)):
    sm = [r for r in PR if test(r) and r['R'] < 4 and r['P'] < 10]; gi = [r for r in PR if test(r) and r['R'] >= 8 and r['P'] >= 10]
    print(f"   alone, {nm}: planets under 4 Earth radii and under 10 days {100 * np.mean([r['npl'] == 1 for r in sm]):.0f}% of {len(sm)}; giants beyond 10 days {100 * np.mean([r['npl'] == 1 for r in gi]):.0f}% of {len(gi)}")
far = np.array([r['met'] for r in PR if r['R'] >= 8 and r['P'] >= 10 and fin(r['met'])])
print(f"   metallicity of the stars of giants beyond 10 days: {far.mean():+.3f} ({len(far)}); over small planets' stars {far.mean() - ms.mean():+.3f}")
for lo_, hi_ in ((0, 4500), (4500, 6000), (6000, 6500), (6500, 20000)):
    a_ = np.array([r['met'] for r in hj if fin(r['met']) and fin(r['teff']) and lo_ <= r['teff'] < hi_]); b_ = np.array([r['met'] for r in small if fin(r['met']) and fin(r['teff']) and lo_ <= r['teff'] < hi_])
    print(f"      stars from {lo_} to {hi_} K: hot Jupiters' minus small planets' {a_.mean() - b_.mean():+.2f} ({len(a_)} and {len(b_)})")
print(f"   planets listed at a size of exactly 2.00 Earth radii (the edge of a bin): {sum(r['R'] == 2.0 for r in s100)}; planets outside the first panel's frame: {sum(not (0.3 <= r['P'] <= 1000 and 0.4 <= r['R'] <= 30) for r in PR)}")
json.dump(dict(verdicts=res, n=len(T), hist=dict(edges=[float(v) for v in fine], counts=hist), ratio=[float(v) for v in ratio if 1.2 <= v <= 2.6],
               pairs=[(float(a['R']), float(b['R'])) for a, b in pr], pr=[(float(r['P']), float(r['R'])) for r in PR]), open(OUT, 'w'))
