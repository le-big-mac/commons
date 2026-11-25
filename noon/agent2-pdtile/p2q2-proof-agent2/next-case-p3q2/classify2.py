"""Classification of the zero patterns of Z_{p^a q^b}, as classify.py, with the reductions at the top level added
(Lemma E of towards-paqb-agent2.md).  Exploration in floating point, no claims.   (Noon = agent2, 21 November 2026)
 L2 : neither p nor q is a zero (the set lies in a subgroup)
 a  : (T2) holds and there is no orphan
 b  : D^w < k                                   (impossible: k divides |A| = D^w)
 N  : D^w / k is not an integer                 (impossible for these p, q)
 R  : an optimal step complement vanishes outside pZ or outside qZ          (reduce to M/p or M/q at the bottom)
 T  : M not a zero, and an optimal step complement is 1 on P or on Q        (Lemma E.3: reduce to M/p or M/q at the top)
 U  : M a zero, and an optimal step complement charges P\\0 or Q\\0           (then A is a union of cosets of Q or of P: Lemma E.4)
 H  : none of these
usage: classify2.py a b p,q [p,q ...]"""
import sys
from collections import Counter
from steplp import Step
def run(p, a, q, b):
    S = Step(p, a, q, b); ords = [o for o in S.ords if o != (0, 0)]; M = S.M
    tot = [float(S.C[((0, 0), cl)]) for cl in S.cls]
    ind = lambda c0: [1.0 if cl == c0 else 0.0 for cl in S.cls]
    outp = [tot[k] if cl[0] == 0 else 0.0 for k, cl in enumerate(S.cls)]; outq = [tot[k] if cl[1] == 0 else 0.0 for k, cl in enumerate(S.cls)]
    cnt = Counter(); hard = []; rescued = Counter()
    for mask in range(1 << len(ords)):
        Z = {o for i, o in enumerate(ords) if mask >> i & 1}
        if (1, 0) not in Z and (0, 1) not in Z: cnt['L2'] += 1; continue
        t2 = all((l, m) in Z for l in range(1, a + 1) for m in range(1, b + 1) if (l, 0) in Z and (0, m) in Z)
        orph = any((l, 0) not in Z and (0, m) not in Z for (l, m) in Z if l and m)
        if t2 and not orph: cnt['a'] += 1; continue
        k = p ** sum(1 for l in range(1, a + 1) if (l, 0) in Z) * q ** sum(1 for m in range(1, b + 1) if (0, m) in Z)
        r = S.solve(Z); v = r[0]; D = M / v
        if D < k * (1 - 1e-9): cnt['b'] += 1; continue
        if abs(D / k - round(D / k)) > 1e-6: cnt['N'] += 1; continue
        face = [(tot, v)]
        mp = S.solve(Z, obj=outp, extra_eq=face)[0]; mq = S.solve(Z, obj=outq, extra_eq=face)[0]
        R = mp < 1e-7 * max(1, v) or mq < 1e-7 * max(1, v)
        xmax = S.solve(Z, obj=ind((a - 1, b)), extra_eq=face, maximize=True)[0]; ymax = S.solve(Z, obj=ind((a, b - 1)), extra_eq=face, maximize=True)[0]
        top = (a, b) in Z
        T = (not top) and (xmax > 1 - 1e-7 or ymax > 1 - 1e-7); U = top and (xmax > 1e-7 or ymax > 1e-7)
        if R: cnt['R'] += 1; rescued['R, also top'] += (T or U); continue
        if T: cnt['T'] += 1; continue
        if U: cnt['U'] += 1; continue
        cnt['H'] += 1; hard.append((sorted(Z), round(D / k, 4), round(D), 'M zero' if top else 'M not zero', 'T2' if t2 else 'not T2', 'orphan' if orph else 'no orphan'))
    return cnt, hard, rescued
if __name__ == '__main__':
    a, b = int(sys.argv[1]), int(sys.argv[2])
    for pq in sys.argv[3:]:
        p, q = map(int, pq.split(','))
        cnt, hard, rescued = run(p, a, q, b)
        print(f"p^{a} q^{b} (p, q) = ({p}, {q}), M = {p**a * q**b}: " + ", ".join(f"{k} {cnt[k]}" for k in ('L2', 'a', 'b', 'N', 'R', 'T', 'U', 'H')) + f"   [of R, also reducible at the top: {rescued['R, also top']}]", flush=True)
        for h in hard[:60]: print('     H:', h)
