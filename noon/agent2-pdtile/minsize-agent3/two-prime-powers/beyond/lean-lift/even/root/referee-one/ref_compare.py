# compare the author's printed tables (read as data) with my floating point table float_3000.json
import re, json, math, sys
mine = json.load(open(sys.argv[1]))
one = sys.argv[2]
def cmp(fname, pat, key, what):
    n = 0; worst = 0.0; differ = []
    for line in open(one + "/" + fname):
        mm = re.match(pat, line)
        if not mm:
            continue
        m = int(mm.group(1)); v = float(mm.group(2))
        if str(m) not in mine[key]:
            continue
        n += 1
        d = abs(v - mine[key][str(m)])
        worst = max(worst, d)
        if d > 6e-6:
            differ.append((m, v, round(mine[key][str(m)], 6)))
    print("%s (%s): %d values of sqrt(m)*bound compared, largest difference %.2e, differing by more than rounding: %s" % (fname, what, n, worst, differ[:12]))
cmp("sup_3000.out", r"m =\s*(\d+)\s+B\(m\) = [0-9.]+\s+sqrt\(m\) B\(m\) = ([0-9.]+)", "B", "B(m)")
cmp("even_3000.out", r"m =\s*(\d+)\s+level 0.*sqrt\(m\) B_E\(m\) = ([0-9.]+)", "BE", "B_E(m)")
cmp("mixed_400.out", r"m =\s*(\d+)\s+powers of 3.*sqrt\(m\) B3\(m\) = ([0-9.]+)", "B3", "B3(m), m >= 27")
# the constants "without the first two texts": min with Theorem Q as the brief states it
ev = {}; od = {}
for m in range(3, 3001):
    s = math.sqrt(m)
    if m % 2 == 0:
        q = 3 / 8 if m < 10 else 47 / 128
        ev[m] = min(q * s, mine["BE"][str(m)])
    else:
        q = 3 / 8 if m < 9 else 1 / 4
        od[m] = min(q * s, mine["B"][str(m)])
me = max(ev, key=lambda m: ev[m]); mo = max(od, key=lambda m: od[m])
print("with Theorem Q of the brief only: even m: largest %.4f at m = %d; odd m: largest %.4f at m = %d" % (ev[me], me, od[mo], mo))
print("   sqrt(m)B_E at 26, 28, 30: %.4f %.4f %.4f; sqrt(m)B at 29, 31, 33: %.4f %.4f %.4f" % tuple(
    [mine["BE"][str(m)] for m in (26, 28, 30)] + [mine["B"][str(m)] for m in (29, 31, 33)]))
