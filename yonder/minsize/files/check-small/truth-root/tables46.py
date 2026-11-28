# The night before's tables against the new bounds, from the first text's own output line
# "(5) ... even m in [3, 46]: m:value ..." (value = min(b, T2)(m) * sqrt(m)) in root/one/evenconst.out.
import re, sys
from math import sqrt
txt = open(sys.argv[1], encoding="utf-8").read()
line = [l for l in txt.split("\n") if l.strip().startswith("even m in [3, 46]:")][0]
pairs = [(int(a), float(b)) for a, b in re.findall(r"(\d+):([0-9.]+)", line.split("]:")[1])]
print("even m, on every clock: good at least, by the night before's tables / by 3.12/sqrt(m)")
for m, v in pairs:
    if m >= 18:
        old = 1 - 2 * v / sqrt(m); new = 1 - 3.12 / sqrt(m)
        print(m, "%.4f" % old, "%.4f" % new, "tables say more" if old > new else "NEW SAYS MORE")
print("largest value in the line:", max(v for m, v in pairs), "at", max(pairs, key=lambda p: p[1])[0])
print("2*0.304530 =", 2 * 0.304530, " 3.12/sqrt(26) =", 3.12 / sqrt(26))
print("limits doubled:", 2 * 1.2699, 2 * 0.8084, " from 50 marks:", 2 * 1.5481, " odd from 17:", 2 * 0.9702, " 2*1.6914 =", 2 * 1.6914)
from math import comb
print("classical bound times sqrt(m):", [(m, round(comb(m, m // 2) / 2 ** m * sqrt(m), 4)) for m in (3, 4, 5, 6, 7, 8, 20, 100, 101, 1000)])
print("classical bound, m = 1..6:", [(m, comb(m, m // 2), 2 ** m) for m in range(1, 7)])
print("c_100 =", comb(100, 50) / 2 ** 100)
