"""Referee's recount of the README's figures by the blind step's rule.py (rule B). Output: recount.out"""
import sys, math
sys.path.insert(0, '/home/agent2/gospel/referee')
import rule, brute2

if __name__ == '__main__':
    N = 10 ** 7
    out = open('/home/agent2/gospel/referee/recount.out', 'w')
    spf = rule.sieve_spf(N)
    rule_B, d, w = rule.make_rule_B(N, spf)
    pr = [r for r in d if r < 10 ** 6]
    for l in (3, 5, 9):
        print('primes 3..10^6 (%d of them): share with %d | ord_r(2): %.5f' % (len(pr), l, sum(1 for r in pr if d[r] % l == 0) / len(pr)), file=out)
    marks = {3000, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7}
    fam = {9: [0, 0], 25: [0, 0], 27: [0, 0], 49: [0, 0], 121: [0, 0], 169: [0, 0], 81: [0, 0], 125: [0, 0]}
    famrec = {}
    tot = cnt = sq = 0; wtot = wcnt = wsq = 0
    powerful = pb = bnp = 0
    for m in range(3, N + 1, 2):
        f = rule.factor(m, spf)
        phi = 1; hs = False; allsq = True
        for p, e in f.items():
            phi *= (p - 1) * p ** (e - 1)
            if e >= 2: hs = True
            else: allsq = False
        b = rule_B(m)
        tot += 1; wtot += phi
        if hs: sq += 1; wsq += phi
        if b: cnt += 1; wcnt += phi
        if allsq:
            powerful += 1; pb += b
        elif b:
            bnp += 1
        for q, (l, e) in ((9, (3, 2)), (25, (5, 2)), (27, (3, 3)), (49, (7, 2)), (121, (11, 2)), (169, (13, 2)), (81, (3, 4)), (125, (5, 3))):
            if f.get(l) == e:
                fam[q][0] += 1; fam[q][1] += b
        if m + 1 in marks or m in marks:
            n = m + 1 if m + 1 in marks else m
            print('to %8d: odd m from 3: %d; square %.5f; bounded %d = %.5f; of those with a square %.5f; weighted square %.6f; weighted bounded %.6f'
                  % (n, tot, sq / tot, cnt, cnt / tot, cnt / sq, wsq / wtot, wcnt / wtot), file=out)
            famrec[n] = {q: (v[0], v[1]) for q, v in fam.items()}
            out.flush()
    print('to 10^7: all primes squared: %d, of them bounded %d; bounded with a prime occurring once: %d' % (powerful, pb, bnp), file=out)
    L = math.log(math.log(1e7) / math.log(1e6))
    for q in (121, 169, 81, 125, 9, 25, 27, 49):
        a, b = famrec[10 ** 6][q], famrec[10 ** 7][q]
        s6, s7 = a[1] / a[0], b[1] / b[0]
        print('family %3d exactly: 10^6 %d of %d = %.4f; 10^7 %d of %d = %.4f; slope %.3f' % (q, a[1], a[0], s6, b[1], b[0], s7, math.log(s7 / s6) / L), file=out)
    # every denominator to a million, weighted
    wt = wb = ws = 0
    for q in range(1, 10 ** 6 + 1):
        m = q
        while m % 2 == 0: m //= 2
        f = rule.factor(q, spf)
        phi = 1
        for p, e in f.items(): phi *= (p - 1) * p ** (e - 1)
        fm = rule.factor(m, spf)
        wt += phi
        if any(e >= 2 for e in fm.values()): ws += phi
        if m > 1 and rule_B(m): wb += phi
    print('every q to 10^6, weighted: square in odd part %.5f; bounded %.5f' % (ws / wt, wb / wt), file=out)
    n, s = brute2.big_cycle_sum(1093 ** 3 * 4373)
    print('q = 1093^3 * 4373: round of %d steps, |sum| %.3f' % (n, s), file=out)
    out.close()
