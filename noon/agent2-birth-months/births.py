"""Birth months against youth cut-off dates.   usage: python -I births.py DATADIR results.json
Rules are in expectations.md: dates given to the day, born 1900 to 2005, births on 1 January left out."""
import sys, csv, json, collections
import numpy as np
D, OUT = sys.argv[1], sys.argv[2]
DAYS = np.array([30, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])      # January without its first day
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
FEMALE = 'http://www.wikidata.org/entity/Q6581072'; MALE = 'http://www.wikidata.org/entity/Q6581097'

def load(name):
    """one row per person: (year, month, day, sex); the first date listed is kept if a person has several"""
    seen, multi = {}, 0
    for r in csv.DictReader(open(f"{D}/{name}.csv", encoding='utf-8')):
        d = r['d']
        if not d or d.startswith('-') or len(d) < 10:
            continue
        y, m, dd = int(d[0:4]), int(d[5:7]), int(d[8:10])
        if r['p'] in seen:
            if seen[r['p']][:3] != (y, m, dd):
                multi += 1
            continue
        seen[r['p']] = (y, m, dd, r.get('sex', ''))
    rows = [v for v in seen.values() if 1900 <= v[0] <= 2005]
    jan1 = sum(1 for v in rows if v[1] == 1 and v[2] == 1)
    rows = [v for v in rows if not (v[1] == 1 and v[2] == 1)]
    return rows, dict(people=len(seen), in_years=len(rows) + jan1, jan1=jan1, second_date=multi)

def months(rows):
    c = np.zeros(12)
    for y, m, d, s in rows:
        c[m - 1] += 1
    return c

def block(c, start):
    """share of births in the three months starting at month number start (1 = January)"""
    idx = [(start - 1 + k) % 12 for k in range(3)]
    return c[idx].sum() / c.sum()

def even(start):
    idx = [(start - 1 + k) % 12 for k in range(3)]
    return DAYS[idx].sum() / DAYS.sum()

def se(p, n):
    return float(np.sqrt(p * (1 - p) / n))

G, info = {}, {}
for name in ('football-spain', 'football-uk', 'football-japan', 'football-germany', 'football-brazil', 'hockey-canada', 'baseball-usa', 'politicians-spain'):
    G[name], info[name] = load(name)
    c = months(G[name])
    print(f"{name}: {info[name]['people']} people with a full date; {info[name]['in_years']} born 1900-2005; {info[name]['jan1']} of those on 1 January "
          f"({100 * info[name]['jan1'] / info[name]['in_years']:.2f}%; even births would give 0.27%), left out; {info[name]['second_date']} rows with a second date ignored; counted {int(c.sum())}")
res = {}
def say(tag, text, ok, void=False):
    res[tag] = None if void else bool(ok)
    print(f"{tag:4s} {text}  ->  {'VOID' if void else 'held' if ok else 'failed'}")

def share_line(name, start):
    c = months(G[name]); p = block(c, start)
    return p, f"{100 * p:.1f}% (even births {100 * even(start):.1f}%; n = {int(c.sum())}; one standard error {100 * se(p, c.sum()):.1f})"
def void(name):
    return months(G[name]).sum() < 1500

p, t = share_line('football-spain', 1); say('M1', f"Spain, footballers, Jan-Mar: {t}", p >= 0.28, void('football-spain'))
c = months(G['football-uk']); bl = {s: block(c, s) for s in (9, 12, 3, 6)}
p, t = share_line('football-uk', 9)
say('M2', f"United Kingdom, footballers, Sep-Nov: {t}; the four blocks from September: " + ", ".join(f"{100 * bl[s]:.1f}" for s in (9, 12, 3, 6)), p >= 0.27 and max(bl, key=bl.get) == 9, void('football-uk'))
c = months(G['football-japan']); bl = {s: block(c, s) for s in (4, 7, 10, 1)}
p, t = share_line('football-japan', 4)
say('M3', f"Japan, footballers, Apr-Jun: {t}; the four blocks from April: " + ", ".join(f"{100 * bl[s]:.1f}" for s in (4, 7, 10, 1)), p >= 0.28 and max(bl, key=bl.get) == 4, void('football-japan'))
p, t = share_line('football-germany', 1); say('M4', f"Germany, footballers, Jan-Mar: {t}", p >= 0.28, void('football-germany'))
p, t = share_line('football-brazil', 1); say('M5', f"Brazil, footballers, Jan-Mar: {t}", p >= 0.27, void('football-brazil'))
cs, cj, cu = months(G['football-spain']), months(G['football-japan']), months(G['football-uk'])
qs = {s: block(cs, s) for s in (1, 4, 7, 10)}; qj = {s: block(cj, s) for s in (1, 4, 7, 10)}; wu = {s: block(cu, s) for s in range(1, 13)}
best_u = max(wu, key=wu.get)
say('M6', f"largest calendar quarter: Spain {MONTHS[max(qs, key=qs.get) - 1]}-, Japan {MONTHS[max(qj, key=qj.get) - 1]}-; United Kingdom's largest three-month window starts in {MONTHS[best_u - 1]} ({100 * wu[best_u]:.1f}%)",
    max(qs, key=qs.get) == 1 and max(qj, key=qj.get) == 4 and best_u in (8, 9, 10), void('football-spain') or void('football-japan') or void('football-uk'))
old = [v for v in G['football-spain'] if v[0] < 1960]; new = [v for v in G['football-spain'] if v[0] >= 1980]
po, pn = block(months(old), 1), block(months(new), 1)
say('M7', f"Spain, footballers, Jan-Mar: born before 1960 {100 * po:.1f}% (n = {len(old)}); born 1980 or later {100 * pn:.1f}% (n = {len(new)}); difference {100 * (pn - po):+.1f} points",
    pn - po >= 0.03, len(old) < 1500 or len(new) < 1500)
p, t = share_line('politicians-spain', 1); say('M8', f"Spain, politicians, Jan-Mar: {t}", abs(p - even(1)) <= 0.015, void('politicians-spain'))
w = [v for v in G['football-germany'] if v[3] == FEMALE]; m = [v for v in G['football-germany'] if v[3] == MALE]
pw, pm = block(months(w), 1), block(months(m), 1)
say('M9', f"Germany, footballers, Jan-Mar: women {100 * pw:.1f}% (n = {len(w)}, one standard error {100 * se(pw, len(w)):.1f}); men {100 * pm:.1f}% (n = {len(m)})", pw < pm, len(w) < 1500 or len(m) < 1500)
c = months(G['baseball-usa']); perday = c / DAYS
order = np.argsort(-perday)
say('M10', f"United States, baseball players (n = {int(c.sum())}): births per day, highest first: " + ", ".join(f"{MONTHS[i]} {perday[i] / perday.mean():.3f}" for i in order[:4]) + f" ... lowest {MONTHS[order[-1]]} {perday[order[-1]] / perday.mean():.3f}",
    order[0] == 7, void('baseball-usa'))
p, t = share_line('hockey-canada', 1); say('M11', f"Canada, ice hockey players, Jan-Mar: {t}", p >= 0.28, void('hockey-canada'))

print("afterwards, not registered:")
prof = {}
for name in G:
    c = months(G[name]); perday = c / DAYS
    prof[name] = (perday / perday.mean()).tolist()
    print(f"   {name:18s} births per day by month, mean = 100: " + " ".join(f"{100 * x:4.0f}" for x in prof[name]))
for name, start in (('football-spain', 1), ('football-uk', 9), ('football-japan', 4), ('football-germany', 1), ('football-brazil', 1), ('hockey-canada', 1), ('baseball-usa', 8)):
    out = []
    for lo, hi in ((1900, 1939), (1940, 1959), (1960, 1979), (1980, 2005)):
        sel = [v for v in G[name] if lo <= v[0] <= hi]
        if len(sel) >= 300:
            p = block(months(sel), start); out.append(f"{lo}-{hi}: {100 * p:.1f} (n {len(sel)})")
    print(f"   {name:18s} share of the three months from {MONTHS[start - 1]}, by year of birth: " + "; ".join(out))
json.dump(dict(verdicts=res, profile=prof, info=info, n={k: int(months(v).sum()) for k, v in G.items()}), open(OUT, 'w'), indent=1)

# ---- afterwards: controls fetched after the registered run (politicians of each country), and Germany by year of birth
import os
print("afterwards: politicians of the same country, share of the same three months (and one standard error); athletes beside it")
ctrl = {}
for name, start, pol in (('football-spain', 1, 'politicians-spain'), ('football-brazil', 1, 'politicians-brazil'), ('football-germany', 1, 'politicians-germany'), ('hockey-canada', 1, 'politicians-canada'),
                         ('football-uk', 9, 'politicians-uk'), ('football-japan', 4, 'politicians-japan'), ('baseball-usa', 8, 'house-usa')):
    if not os.path.exists(f"{D}/{pol}.csv"):
        print("   missing", pol); continue
    rows, inf = load(pol)
    c = months(rows); p = block(c, start); a = block(months(G[name]), start)
    perday = c / DAYS
    ctrl[pol] = (perday / perday.mean()).tolist()
    info[pol] = inf
    print(f"   {name:17s} from {MONTHS[start - 1]}: athletes {100 * a:.1f}%; politicians {100 * p:.1f}% (n = {int(c.sum())}, s.e. {100 * se(p, c.sum()):.1f}); even births {100 * even(start):.1f}%; "
          f"politicians by month: " + " ".join(f"{100 * x:.0f}" for x in ctrl[pol]))
print("afterwards: Germany's footballers by year of birth (the youth cut-off moved from 1 August to 1 January in 1997)")
ger = {}
for lo, hi in ((1940, 1979), (1980, 1984), (1985, 1989), (1990, 2005)):
    sel = [v for v in G['football-germany'] if lo <= v[0] <= hi]
    c = months(sel); perday = c / DAYS
    ger[f"{lo}-{hi}"] = (perday / perday.mean()).tolist()
    print(f"   born {lo}-{hi} (n = {len(sel)}): Aug-Oct {100 * block(c, 8):.1f}%, Jan-Mar {100 * block(c, 1):.1f}%; the largest three-month window starts in {MONTHS[max(range(1, 13), key=lambda s: block(c, s)) - 1]}")
for sexname, code in (('men', MALE), ('women', FEMALE)):
    sel = [v for v in G['football-germany'] if v[0] >= 1990 and v[3] == code]
    print(f"   born 1990 or later, {sexname} (n = {len(sel)}): Jan-Mar {100 * block(months(sel), 1):.1f}%")
c = months(G['baseball-usa'])
pa, ps_ = c[7] / c.sum(), c[8] / c.sum()
print(f"afterwards: baseball, August against September: {int(c[7])} and {int(c[8])} births; per day {c[7] / 31:.1f} and {c[8] / 30:.1f}; the difference per day is {abs(c[7] / 31 - c[8] / 30) / np.sqrt(c[7] / 31 ** 2 + c[8] / 30 ** 2):.1f} standard errors")
sel = [v for v in G['baseball-usa'] if 1960 <= v[0] <= 1979]; c2 = months(sel) / DAYS
print(f"   born 1960-1979 (n = {len(sel)}): highest month {MONTHS[int(np.argmax(c2))]} ({c2.max() / c2.mean():.2f} of the mean)")
json.dump(dict(verdicts=res, profile=prof, control=ctrl, germany=ger, info=info, n={k: int(months(v).sum()) for k, v in G.items()}), open(OUT, 'w'), indent=1)

# ---- after the referee: its main controls, recomputed here
import datetime
print("after the referee:")
def doy(m, d):
    return (datetime.date(2001, m, d) - datetime.date(2001, 1, 1)).days          # day of a common year, 0 = 1 January
def step(rows, m, d):
    """births in the 14 days from (m, d) against the 14 days before; around 1 January the first is 2-15 January (1 January is left out)"""
    start = doy(m, d) + (1 if (m, d) == (1, 1) else 0)
    after = before = 0
    edge = doy(m, d)
    for y, mm, dd, s in rows:
        if (mm, dd) == (2, 29):
            continue
        k = doy(mm, dd)
        if 0 <= (k - start) % 365 < 14:
            after += 1
        elif 0 < (edge - k) % 365 <= 14:
            before += 1
    return after, before
print("   the step at the dividing date: births in the fortnight after it against the fortnight before")
for name, (m, d) in (('football-spain', (1, 1)), ('football-brazil', (1, 1)), ('hockey-canada', (1, 1)), ('football-uk', (9, 1)), ('football-japan', (4, 2)), ('baseball-usa', (8, 1)),
                     ('politicians-spain', (1, 1))):
    rows = G[name] if name in G else load(name)[0]
    a, b = step(rows, m, d)
    print(f"      {name:18s} {a} : {b}  ({a / b:.2f})")
for pol, (m, d) in (('politicians-brazil', (1, 1)), ('politicians-canada', (1, 1)), ('politicians-uk', (9, 1)), ('politicians-japan', (4, 2)), ('house-usa', (8, 1)), ('politicians-germany', (1, 1)), ('politicians-germany', (8, 1))):
    a, b = step(load(pol)[0], m, d)
    print(f"      {pol:18s} at {d}/{m}: {a} : {b}  ({a / b:.2f})")
print("   Germany's footballers by sex and year of birth: August to October / January to March")
gm = {}
for lo, hi in ((1940, 1979), (1980, 1984), (1985, 1989), (1990, 1994), (1995, 2005), (1985, 2005)):
    out = []
    for sexname, code in (('men', MALE), ('women', FEMALE)):
        sel = [v for v in G['football-germany'] if lo <= v[0] <= hi and v[3] == code]
        c = months(sel)
        out.append(f"{sexname} {100 * block(c, 8):.1f} / {100 * block(c, 1):.1f} (n = {len(sel)})")
        if sexname == 'men':
            perday = c / DAYS; gm[f"{lo}-{hi}"] = (perday / perday.mean()).tolist()
    print(f"      born {lo}-{hi}: " + "; ".join(out))
old = [v for v in G['football-germany'] if 1940 <= v[0] <= 1979 and v[3] == MALE]; new = [v for v in G['football-germany'] if v[0] >= 1990 and v[3] == MALE]
print(f"      German men, step at 1 August: born 1940-1979 {step(old, 8, 1)}, born 1990 or later {step(new, 8, 1)}; step at 1 January: born 1940-1979 {step(old, 1, 1)}, born 1990 or later {step(new, 1, 1)}")
print("   Spain by year of birth: August to October / January to March; and the step at 1 August")
for lo, hi in ((1900, 1939), (1940, 1959), (1960, 1979), (1980, 2005)):
    sel = [v for v in G['football-spain'] if lo <= v[0] <= hi]; c = months(sel)
    print(f"      born {lo}-{hi} (n = {len(sel)}): {100 * block(c, 8):.1f} / {100 * block(c, 1):.1f}; step at 1 August {step(sel, 8, 1)}; at 1 January {step(sel, 1, 1)}")
print("   United Kingdom by year of birth: September to November / January to March; and the step at 1 January")
for lo, hi in ((1900, 1939), (1940, 1979), (1980, 1989), (1990, 2005)):
    sel = [v for v in G['football-uk'] if lo <= v[0] <= hi]; c = months(sel)
    print(f"      born {lo}-{hi} (n = {len(sel)}): {100 * block(c, 9):.1f} / {100 * block(c, 1):.1f}; step at 1 January {step(sel, 1, 1)}; at 1 September {step(sel, 9, 1)}")
print("   baseball by year of birth: August to October; the step at 1 August")
for lo, hi in ((1900, 1949), (1950, 1989), (1990, 2005)):
    sel = [v for v in G['baseball-usa'] if lo <= v[0] <= hi]; c = months(sel)
    print(f"      born {lo}-{hi} (n = {len(sel)}): {100 * block(c, 8):.1f}%; step {step(sel, 8, 1)}")
print("   women and men, share of the three months after the dividing date")
for name, start in (('football-spain', 1), ('football-brazil', 1), ('hockey-canada', 1), ('football-uk', 9), ('football-japan', 4), ('baseball-usa', 8)):
    w = [v for v in G[name] if v[3] == FEMALE]; mn = [v for v in G[name] if v[3] == MALE]
    print(f"      {name:18s} women {100 * block(months(w), start):.1f}% (n = {len(w)}); men {100 * block(months(mn), start):.1f}% (n = {len(mn)})" if len(w) >= 300 else f"      {name:18s} women: only {len(w)}")
print("   born 1960 or later only: athletes against politicians, the same three months")
for name, start, pol in (('football-spain', 1, 'politicians-spain'), ('football-brazil', 1, 'politicians-brazil'), ('football-germany', 1, 'politicians-germany'), ('hockey-canada', 1, 'politicians-canada'),
                         ('football-uk', 9, 'politicians-uk'), ('football-japan', 4, 'politicians-japan'), ('baseball-usa', 8, 'house-usa')):
    a = [v for v in G[name] if v[0] >= 1960]; p = [v for v in load(pol)[0] if v[0] >= 1960]
    print(f"      {name:18s} athletes {100 * block(months(a), start):.1f}% (n = {len(a)}); politicians {100 * block(months(p), start):.1f}% (n = {len(p)})")
jp = load('politicians-japan')
print(f"   1 January among politicians: Japan {100 * jp[1]['jan1'] / jp[1]['in_years']:.2f}%, United Kingdom {100 * load('politicians-uk')[1]['jan1'] / load('politicians-uk')[1]['in_years']:.2f}%")
c = months(G['football-japan']); a1 = sum(1 for v in G['football-japan'] if (v[1], v[2]) == (4, 1)); a2 = sum(1 for v in G['football-japan'] if (v[1], v[2]) == (4, 2))
print(f"   Japan's footballers born on 1 April: {a1}; on 2 April: {a2}")
out = json.load(open(OUT)); out['germany_men'] = gm
sp = [v for v in G['football-spain'] if v[0] >= 1980]; cc = months(sp) / DAYS; out['spain_1980'] = (cc / cc.mean()).tolist(); out['n_spain_1980'] = len(sp)
json.dump(out, open(OUT, 'w'), indent=1)
