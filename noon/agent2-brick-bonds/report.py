"""Markdown tables for the write-up.   usage: report.py census.pkl"""
import pickle, math, sys
from fractions import Fraction
from census import canon, measures, bricks, ASPECT
from bonds import named, word
F = pickle.load(open(sys.argv[1], "rb")); MM = 56.25
mask = lambda J: sum(1 << x for x in J)
def lattice(seq, s): w, J = word(seq); return canon(w, [mask(J)], s)
def stack(w, rows, s):
    cs = []
    for off, seq in rows:
        ww, J = word(seq, off); assert ww == w; cs.append(mask(frozenset(x % w for x in J)))
    return canon(w, cs, s)
def row(name, k):
    m = F[k] if k in F else measures(k)
    run = "endless" if m["run"] == math.inf else str(m["run"])
    if m["ties"] == 0: return f"| {name} | 0 | – | – | {run} | {m['endless']:.0%} |"
    return f"| {name} | {Fraction(m['share']).limit_denominator(60)} | {m['radius'] * MM:.0f} | {m['eff']:.3f} | {run} | {m['endless']:.0%} |"
NAMED = [(canon(b.w, [mask(J) for J in b.cs], b.s), b.name) for b in named()]
print(f"census: {len(F):,} bonds, {sum(1 for m in F.values() if m['ties'] > 0):,} with headers; all named present: {all(k in F for k, _ in NAMED)}\n")
print("| bond | headers, share of face | farthest point from a header's centre, mm | spread | longest internal joint, courses | length under endless internal joints |\n|---|---|---|---|---|---|")
for k, n in NAMED: print(row(n[0].upper() + n[1:], k))
print()
picks = [("Flemish stretcher bond, three stretching courses to one Flemish course, the Flemish courses staggered", stack(12, [(0, "SSS"), (1, "HSHS"), (2, "SSS"), (0, "SSS")], 3)),
         ("One header to four stretchers, each course moved 1¼ bricks", lattice("HSSSS", 5)), ("Sussex course (H S S S), each course moved 1¼ bricks", lattice("HSSS", 5)),
         ("Monk course (H S S), each course moved ¾ brick", lattice("HSS", 3)), ("One header to six stretchers, each course moved 1¾ bricks", lattice("HSSSSSS", 7)),
         ("Flemish stretcher bond, one stretching course to one Flemish course, each pair moved ½ brick", stack(12, [(0, "SSS"), (1, "HSHS")], 2)),
         ("Stretching courses alternating with courses of two headers and a stretcher, each pair moved one brick", stack(8, [(0, "SS"), (1, "HHS")], 4))]
print("| bond | headers, share of face | farthest point from a header's centre, mm | spread | longest internal joint, courses | length under endless internal joints |\n|---|---|---|---|---|---|")
for n, k in picks: print(row(n, k) + ("" if k in F else "  (not in census range)"))
print("\n| longest internal joint allowed, r courses | least share of headers in the census | bound 1/(r+1) | bonds attaining it | of these, with a course mixing headers and stretchers |\n|---|---|---|---|---|")
for r in range(0, 8):
    cand = [(m["share"], k) for k, m in F.items() if m["run"] <= r]; best = min(c[0] for c in cand); opt = [k for s_, k in cand if abs(s_ - best) < 1e-12]
    mixed = sum(1 for k in opt if any(len({L for _, L in bricks(m, k[0])}) == 2 for m in k[3]))
    print(f"| {r} | {Fraction(best).limit_denominator(100)} | {Fraction(1, r + 1)} | {len(opt)} | {mixed} |")
by = {}
for k in F: by[(k[1], k[0])] = by.get((k[1], k[0]), 0) + 1
ws = sorted({w for _, w in by}); hs = sorted({h for h, _ in by})
print("\n| courses in a repeat \\ length of a repeat, quarters | " + " | ".join(str(w) for w in ws) + " |\n|---|" + "---|" * len(ws))
for h in hs: print(f"| {h} | " + " | ".join(str(by.get((h, w), "")) for w in ws) + " |")
# ranks at equal header share, and domination of Flemish
print()
for k, n in NAMED:
    if k not in F or F[k]["ties"] == 0: continue
    m = F[k]; same = sorted((mm["eff"] for kk, mm in F.items() if abs(mm["share"] - m["share"]) < 1e-9), reverse=True)
    better = sum(1 for e in same if e > m["eff"] + 1e-9)
    print(f"{n}: {better} of the {len(same)} bonds with the same share of headers are better spread (best {same[0]:.3f})")
fl = F[lattice("SH", 3)]
dom = [k for k, m in F.items() if m["ties"] and m["share"] <= fl["share"] + 1e-12 and m["radius"] <= fl["radius"] + 1e-9 and k != lattice("SH", 3)]
print("bonds with no more headers than Flemish and no larger covering radius:", len(dom), dom[:3])
top = sorted(((m["eff"], k) for k, m in F.items() if m["ties"] > 0), reverse=True)[:8]
print("best spread overall:")
for e, k in top:
    w, h, s, cs = k; br = " / ".join(f"{bricks(m, w)[0][0]}:" + "".join("S" if L == 4 else "H" for _, L in bricks(m, w)) for m in cs)
    print(f"   {e:.4f} share {F[k]['share']:.3f} run {F[k]['run']} w={w} h={h} s={s}  {br}")
