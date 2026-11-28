# largest quotient of an exact share of a heavy family to the text's bounds (my floating point tables), m >= 47
import sys, json, math
import ref_heavy as rh
tab = json.load(open(sys.argv[1]))
best = {}
for name, (n, deco) in rh.FAM.items():
    r, A = rh.heavy(n, deco)
    for h in range(max(1, 47 - r), 3001 - r):
        m = r + h
        if m % 7 not in (0, 1) and m > 200:
            continue
        v = float(rh.share(r, A, h)) * math.sqrt(m)
        keys = ("B", "B3") if m % 2 else ("B", "BE", "B3")
        for key in keys:
            q = v / tab[key][str(m)]
            kk = (key, m % 2)
            if kk not in best or q > best[kk][0]:
                best[kk] = (q, name, m, v, tab[key][str(m)])
for kk in sorted(best):
    print("bound %s, m %s: largest share/bound = %.4f  (%s, m = %d, sqrt(m)*share = %.4f, sqrt(m)*bound = %.4f)" % (
        kk[0], "odd" if kk[1] else "even", best[kk][0], best[kk][1], best[kk][2], best[kk][3], best[kk][4]))
