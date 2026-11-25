"""Verdicts for the second author's twelve statements, by the letter of readers/sheet.md.
usage: python -I sunspots.py MONTHLY SMOOTHED YEARLY results.json
Numbers are read as decimals exactly as printed.  Where a statement names one holder of an extreme, every holder of
that value must satisfy it, as the sheet says."""
import sys, json
from decimal import Decimal
MON, SMO, YRL, OUT = sys.argv[1:5]
def rows(path):
    out = []
    for line in open(path, encoding='utf-8', errors='replace'):
        f = [x.strip() for x in line.strip().split(';')]
        if len(f) >= 4 and f[0]:
            out.append(f)
    return out
R = {12 * int(f[0]) + int(f[1]): Decimal(f[3]) for f in rows(MON)}
S = {12 * int(f[0]) + int(f[1]): Decimal(f[3]) for f in rows(SMO)}
Y = {int(Decimal(f[0])): Decimal(f[1]) for f in rows(YRL)}
R = {n: v for n, v in R.items() if v >= 0}; S = {n: v for n, v in S.items() if v >= 0}; Y = {y: v for y, v in Y.items() if v >= 0}
ym = lambda n: f"{(n - 1) // 12}-{(n - 1) % 12 + 1:02d}"
print(f"monthly values {len(R)} ({ym(min(R))} to {ym(max(R))}); smoothed values {len(S)} ({ym(min(S))} to {ym(max(S))}); yearly values {len(Y)} ({min(Y)} to {max(Y)})")
minima = []
for n in sorted(S):
    if all((n + k) in S for k in range(-60, 61)) and all(S[n] < S[n - k] for k in range(1, 61)) and all(S[n] <= S[n + k] for k in range(1, 61)):
        minima.append(n)
cyc = []
for a, b in zip(minima[:-1], minima[1:]):
    inner = [n for n in range(a + 1, b) if n in S]
    top = max(S[n] for n in inner); mx = min(n for n in inner if S[n] == top)
    cyc.append(dict(start=a, end=b, max=mx, peak=top, rise=mx - a, fall=b - mx, length=b - a))
print(f"{len(minima)} cycle minima: " + ", ".join(ym(n) for n in minima))
for k, c in enumerate(cyc, 1):
    print(f"   cycle {k:2d}: {ym(c['start'])} to {ym(c['end'])}, maximum {ym(c['max'])}, peak {c['peak']}, rise {c['rise']}, fall {c['fall']}")
res = {}
def say(tag, text, ok):
    res[tag] = bool(ok)
    print(f"{tag:4s} {text}  ->  {'held' if ok else 'failed'}")
K = len(cyc); P = {k: cyc[k - 1]['peak'] for k in range(1, K + 1)}
meanlen = sum(c['length'] for c in cyc) / Decimal(K) if K else None
say('B1', f"{len(minima)} minima; mean length of the {K} cycles {float(meanlen):.2f} months", len(minima) == 25 and K == 24 and 131 <= meanlen <= 134)
nrf = sum(c['rise'] < c['fall'] for c in cyc)
say('B2', f"rise shorter than fall in {nrf} of {K} cycles (not in cycles {[k for k, c in enumerate(cyc, 1) if not c['rise'] < c['fall']]})", nrf >= 20)
top = max(R.values()); holders = [n for n in R if R[n] == top]
say('B3', f"largest monthly mean {top} in {', '.join(ym(n) for n in holders)}; largest in 1957 or 1958: {max(v for n, v in R.items() if (n - 1) // 12 in (1957, 1958))}", all((n - 1) // 12 in (1957, 1958) for n in holders))
def ranks(v):
    order = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
            j += 1
        for t in range(i, j + 1):
            r[order[t]] = (i + j) / 2 + 1
        i = j + 1
    return r
def pearson(a, b):
    n = len(a); ma, mb = sum(a) / n, sum(b) / n
    sab = sum((x - ma) * (y - mb) for x, y in zip(a, b)); saa = sum((x - ma) ** 2 for x in a); sbb = sum((y - mb) ** 2 for y in b)
    return sab / (saa * sbb) ** 0.5
rho = pearson(ranks([c['rise'] for c in cyc]), ranks([float(c['peak']) for c in cyc]))
say('B4', f"rank correlation of rise with peak across {K} cycles: {rho:+.4f}", rho <= -0.60)
ys = sorted(Y, key=lambda y: -Y[y])
say('B5', "highest yearly means: " + ", ".join(f"{y} {Y[y]}" for y in ys[:5]), ys[:3] == [1957, 1958, 1778] and Y[ys[0]] > Y[ys[1]] > Y[ys[2]] > Y[ys[3]])
yrs = sorted(Y); x = [float(Y[y]) for y in yrs]; xb = sum(x) / len(x); den = sum((v - xb) ** 2 for v in x)
acf = lambda k: sum((x[t] - xb) * (x[t + k] - xb) for t in range(len(x) - k)) / den
say('B6', f"autocorrelation of the yearly series at lag 10: {acf(10):+.4f}; at lag 11: {acf(11):+.4f} (lag 9: {acf(9):+.4f}, lag 12: {acf(12):+.4f})", acf(11) > acf(10))
ok7 = K >= 24 and all(P[24] < P[k] for k in range(15, 24)) and P[14] < P[24]
say('B7', "peaks of cycles 14 to 24: " + (", ".join(f"{k}: {P[k]}" for k in range(14, 25)) if K >= 24 else "not all exist"), ok7)
pairs = [(e, e + 1) for e in range(2, 23, 2)]
odd = sum(P[o] > P[e] for e, o in pairs) if K >= 23 else None
say('B8', f"odd cycle higher in {odd} of the {len(pairs)} pairs (not in {[(e, o) for e, o in pairs if not P[o] > P[e]] if K >= 23 else '-'})", odd == 8)
low = min(P.values()); lows = [k for k in P if P[k] == low]
say('B9', f"lowest peak {low} in cycle {lows}; cycle 5 has {P.get(5)}, cycle 6 has {P.get(6)}", lows == [5])
openc = [n for n in S if n > minima[-1]]; ot = max(S[n] for n in openc); oh = [n for n in openc if S[n] == ot]
say('B10', f"largest smoothed value since the last minimum ({ym(minima[-1])}): {ot} in {', '.join(ym(n) for n in oh)}", 150 <= ot <= 170 and all((n - 1) // 12 == 2024 for n in oh))
m1 = [Y[y] for y in Y if 1900 <= y <= 2025]; m0 = [Y[y] for y in Y if 1749 <= y <= 1899]
a, b = sum(m1) / len(m1), sum(m0) / len(m0)
say('B11', f"mean yearly value 1900-2025: {float(a):.2f} ({len(m1)} years); 1749-1899: {float(b):.2f} ({len(m0)} years); ratio {float(a / b):.4f}", a >= Decimal('1.15') * b)
zeros = [n for n in R if R[n] == 0]
say('B12', f"months with a monthly mean of exactly 0.0: {len(zeros)}; the latest {ym(max(zeros)) if zeros else '-'}; lowest months since 2010: " + ", ".join(f"{ym(n)} {R[n]}" for n in sorted([n for n in R if n > 12 * 2010], key=lambda n: R[n])[:4]),
    bool(zeros) and (max(zeros) - 1) // 12 == 2009)
json.dump(dict(verdicts=res), open(OUT, 'w'), indent=1)
