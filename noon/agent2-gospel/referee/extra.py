"""Small extra checks.  Output: extra.out
 (1) exact (whole-number) cycle sums for a few denominators beyond 3000;
 (2) GOSPEL(A) is HAKMEM(first heading 2A) turned through -A: largest gap over 500 steps;
 (3) HAKMEM's reason for 171 ("9 divides phi(19)") tried as a rule on 9*r, r prime;
 (4) the share falling: among odd m with 9 || m and m/9 squarefree, the bounded share.
"""
import math, sys, cmath
sys.path.insert(0, '/home/agent2/gospel/referee')
import brute, rule, exact

if __name__ == '__main__':
    out = open('/home/agent2/gospel/referee/extra.out', 'w')
    spf = rule.sieve_spf(10 ** 6)
    for q in (9837, 9009, 2525 * 3, 3 * 1093, 5 * 1093, 7 * 1093, 6561, 15625):
        z, deg = exact.exact_zero(q, spf)
        print('(1) q=%d exact cycle sum is nought: %s   floating |sum| %.3e' % (q, z, brute.cycle_sum(1, q)[2]), file=out)
    worst = 0.0
    for (p, q) in ((1, 9), (1, 45), (2, 63), (5, 36), (1, 18), (3, 171), (1, 1000)):
        # whole-number heading indices mod q, so that doubling loses nothing
        g = []
        head = 0
        turn = p % q
        pos = 0j
        for _ in range(500):
            head = (head + turn) % q
            pos += cmath.exp(2j * math.pi * head / q)
            g.append(pos)
            turn = (2 * turn) % q
        # HAKMEM with first heading 2A, turned through -A
        h = []
        ang = (2 * p) % q
        pos = 0j
        rot = cmath.exp(-2j * math.pi * p / q)
        for _ in range(500):
            pos += cmath.exp(2j * math.pi * ang / q)
            h.append(pos * rot)
            ang = (2 * ang) % q
        worst = max(worst, max(abs(a - b) for a, b in zip(g, h)))
    print('(2) GOSPEL(A) against HAKMEM(2A) turned through -A, 500 steps, 7 angles: largest gap %.2e' % worst, file=out)
    rule_B, d, w = rule.make_rule_B(10 ** 6, spf)
    rows = []
    n_agree = n_all = 0
    for r in range(5, 400, 2):
        if spf[r] == r:
            hak = ((r - 1) % 9 == 0)            # "9 divides phi(r)" => never loops
            mine = (d[r] % 3 == 0)              # 3 divides the order of 2 mod r => never loops
            truth = not (brute.cycle_sum(1, 9 * r)[2] < brute.TOL)   # really unbounded?
            n_all += 1
            n_agree += (hak == truth)
            assert mine == truth, r
            if hak != truth:
                rows.append((9 * r, r, r - 1, d[r], 'unbounded' if truth else 'bounded'))
    print('(3) q = 9r, primes 5 <= r < 400: "9 | phi(r)" predicts the truth for %d of %d; "3 | ord_r(2)" for all.' % (n_agree, n_all), file=out)
    print('    where the memo\'s reason fails (q, r, phi(r), ord_r(2), truth):', rows[:12], file=out)
    cnt = tot = 0
    for m in range(9, 10 ** 6 + 1, 18):
        f = rule.factor(m, spf)
        if f.get(3) == 2 and all(e == 1 for p, e in f.items() if p != 3):
            tot += 1
            cnt += rule_B(m)
        if m + 18 > 10 ** 4 and m <= 10 ** 4 or m + 18 > 10 ** 5 and m <= 10 ** 5 or m + 18 > 10 ** 6:
            print('(4) odd m <= %d with 9 || m, m/9 squarefree: %d, bounded %d, share %.4f' % (m, tot, cnt, cnt / tot), file=out)
    out.close()
    print(open('/home/agent2/gospel/referee/extra.out').read())
