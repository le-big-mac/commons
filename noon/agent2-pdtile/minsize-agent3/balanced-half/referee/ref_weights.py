"""Referee: the largest weight in the constructions of section 6.3 (section 8 says "weights up to p^k' (and 2)")."""
import itertools
from ref_common import rule
from ref_construct import digits, build, first_case
seen = {}
for (p, q) in ((2, 3), (3, 2), (2, 5), (5, 2), (3, 5)):
    for n in range(1, 6 if p == 2 else 4):
        dig = digits(p, n)
        lv = list(range(1, n + 1))
        for Et in itertools.chain.from_iterable(itertools.combinations(lv, r) for r in range(n + 1)):
            for Ft in itertools.chain.from_iterable(itertools.combinations(lv, r) for r in range(n + 1)):
                E = set(Et); F = set(Ft) | {0}
                val, x, a0, kp = rule(p, q, n, E, F)
                if x is None:
                    continue
                fc = first_case(p, n, E, F)
                W = build(p, q, n, dig, E, F, fc)
                mw = int(W.max())
                over = mw > max(p ** kp, 2)
                key = (fc, "p=2" if p == 2 else "p>=3", "a0 in E" if a0 in E else "a0 not in E", "k'=1" if kp == 1 else ("k'=0" if kp == 0 else "k'>=2"), "max weight %d" % mw if over else "within")
                seen[key] = seen.get(key, 0) + 1
                if over and key not in seen.get("ex", {}):
                    seen.setdefault("ex", {})[key] = (p, q, n, sorted(E), sorted(F))
ex = seen.pop("ex", {})
for k in sorted(seen):
    if k[-1] != "within":
        print(k, seen[k], "e.g. (p, q, n, E, F) =", ex[k])
print("constructions within max(p^k', 2):", sum(v for k, v in seen.items() if k[-1] == "within"), "; above:", sum(v for k, v in seen.items() if k[-1] != "within"))
