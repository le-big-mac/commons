"""The README's four tables, in Markdown, from the outputs.   usage: python -I tables.py > tables.out"""
import json
C = json.load(open("after-c.json"))['curves']; T3 = json.load(open("after-3.json")); A = json.load(open("after-45678.json")); A2 = json.load(open("after2.json"))
D = json.load(open("after3-CDEF.json"))['least']; GF = json.load(open("after3-C.json"))['needed']        # the least number over even and odd numbers of sales; the Gamma form where double precision gave out
def least(kind, q, a, target, odd):
    hit = [r for r in D if r['kind'] == kind and abs(r['q'] - q) < 1e-9 and abs(r['target'] - target) < 1e-9 and (a is None or r['a'] is None or abs(r['a'] - a) < 1e-9)]
    return hit[0]['least'] if hit else odd
def big(v): 
    if v is None: return "more than 2 × 10^15"
    if v < 1e7: return f"{v:,.0f}"
    e = len(f"{v:.0f}") - 1; return f"{v / 10 ** e:.1f} × 10^{e}"
print("CURVE-ROWS")
for N in (10, 100, 1000, 10000, 100000, 10 ** 6, 10 ** 9, 10 ** 12):
    cells = [f"{C[g][str(N)]:.4f}" if str(N) in C[g] else (f"{T3['big'][str(N)]:.4f}" if g == "1.0" else "") for g in ("0.0", "0.5", "1.0", "1.5")]; print(f"| {N:,} | " + " | ".join(cells) + " |")
print("NEEDED-ROWS")
for q in ("1.05", "1.1", "1.25", "1.5", "2.0"):
    r = T3['sales_needed'][q]; print(f"| {float(q):g} | " + " | ".join(big(least("copying", float(q), 1.0, float(t), r['imitation'][t])) for t in ("0.75", "0.9", "0.99")) + " | " + " | ".join(f"{least('alone', float(q), None, float(t), r['alone'][t]):,}" for t in ("0.75", "0.9", "0.99")) + " |")
print("A-ROWS")
for a in ("0.1", "0.3", "1.0", "3.0", "10.0", "30.0", "100.0"):
    n = A2['needed']['1.1'][a]; cell = f"about 10^{GF[a]:.0f}" if n is None else big(least("copying", 1.1, float(a), 0.9, n))
    print(f"| {float(a):g} | {A['a'][f'{float(a):g}']:.4f} | {A2['P'][a][1]:.4f} | {cell} |")
from scipy.stats import binom
print(f"| no imitation | {C['0.0']['1000']:.4f} | {float(binom.sf(499999, 999999, 1.1 / 2.1)):.4f} | {A2['needed']['1.1']['none']:,} |")
print("EDGE-ROWS")
for N in ("100", "1000", "10000"): print(f"| {int(N):,} | " + " | ".join(f"{A['edge'][N][g]:.3f}" for g in ("0", "0.25", "0.5", "0.75", "1", "1.25", "1.5", "2")) + " |")
