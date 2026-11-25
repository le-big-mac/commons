import pickle, math, sys
from fractions import Fraction
from census import rot, bricks, canon
from bonds import named
F = pickle.load(open(sys.argv[1] if len(sys.argv) > 1 else "census.pkl", "rb"))
mask = lambda J: sum(1 << x for x in J)
NAMES = {canon(b.w, [mask(J) for J in b.cs], b.s): b.name for b in named()}
def words(key):
    w, h, s, cs = key; out = []
    for m in cs:
        br = bricks(m, w); out.append(f"{br[0][0]}:" + "".join("S" if L == 4 else "H" for _, L in br))
    return " / ".join(out) + f"  shear {s}"
print(len(F), "bonds;  named ones present:", sum(k in F for k in NAMES), "of", len(NAMES), " missing:", [n for k, n in NAMES.items() if k not in F])
by = {}
for k in F: by[(k[1], k[0])] = by.get((k[1], k[0]), 0) + 1
print("bonds by least periods (h0: {w0: count}):")
for h in sorted({a for a, _ in by}): print("  h0 =", h, {w: c for (hh, w), c in sorted(by.items()) if hh == h})
print("\n--- fewest headers for a given longest collar run r (bound: header share >= 1/(r+1)) ---")
for r in range(0, 8):
    cand = [(m["share"], k) for k, m in F.items() if m["run"] <= r]
    if not cand: print(f"r={r}: none"); continue
    best = min(c[0] for c in cand); opt = [k for s_, k in cand if abs(s_ - best) < 1e-12]
    print(f"r={r}: least header share {Fraction(best).limit_denominator(100)} (bound {Fraction(1, r + 1)}), attained by {len(opt)} bonds; "
          f"with a course that mixes headers and stretchers: {sum(1 for k in opt if any(len({L for _, L in bricks(m, k[0])}) == 2 for m in k[3]))}")
    for k in sorted(opt, key=lambda k: (k[1], k[0]))[:6]: print(f"      {NAMES.get(k, ''):38s} w={k[0]} h={k[1]}  {words(k)}")
print("\n--- spread of the headers (hexagonal ideal / covering radius), best 25 ---")
top = sorted(((m["eff"], k) for k, m in F.items() if m["ties"] > 0 and m["radius"] == m["radius"]), reverse=True)
for e, k in top[:25]:
    m = F[k]; print(f"  {e:.4f}  share {m['share']:.3f}  radius {m['radius']:.3f}  run {m['run']}  endless {m['endless']:.2f}  {NAMES.get(k, ''):30s} w={k[0]} h={k[1]}  {words(k)}")
print("\n--- same, among bonds with no endless internal joint, best 15 ---")
n = 0
for e, k in top:
    m = F[k]
    if m["run"] == math.inf: continue
    print(f"  {e:.4f}  share {m['share']:.3f}  radius {m['radius']:.3f}  run {m['run']}  {NAMES.get(k, ''):30s} w={k[0]} h={k[1]}  {words(k)}"); n += 1
    if n == 15: break
print("\n--- named bonds: rank by spread among bonds with the same header share ---")
for k, name in NAMES.items():
    if k not in F or F[k]["ties"] == 0: continue
    m = F[k]; same = sorted((mm["eff"] for kk, mm in F.items() if abs(mm["share"] - m["share"]) < 1e-9), reverse=True)
    print(f"  {name:40s} share {m['share']:.3f} spread {m['eff']:.4f}  rank {same.index(m['eff']) + 1} of {len(same)} (best {same[0]:.4f})")
