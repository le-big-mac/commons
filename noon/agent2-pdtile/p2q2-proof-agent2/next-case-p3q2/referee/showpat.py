import sys
import refclassify as rc
a, b = 3, 2
for p, q in [(2,3),(2,5),(3,2),(5,2)]:
    CAT, SIZE, cnt, _ = rc.classify(p, q)
    print(f"--- (p, q) = ({p}, {q}), M = {p**3*q**2}")
    for cat in ('T', 'U', 'H'):
        for Z, c in CAT.items():
            if c != cat: continue
            Ep = [l for l in range(1, a + 1) if (l, 0) in Z]; Eq = [m for m in range(1, b + 1) if (0, m) in Z]
            k = p ** len(Ep) * q ** len(Eq)
            t2 = all((l, m) in Z for l in Ep for m in Eq)
            orph = [(l, m) for (l, m) in sorted(Z) if l >= 1 and m >= 1 and l not in Ep and m not in Eq]
            print(f"  {cat}: size {SIZE[Z]} k {k} {'T2' if t2 else 'notT2'} orphans {orph} Ep {Ep} Eq {Eq} F {sorted(o for o in Z if o[0] and o[1])}")
