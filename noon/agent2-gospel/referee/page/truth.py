"""Truth for the page's sentences, from the blind step's programs (adding up steps; no rule in the adding).
usage: python -I truth.py  ->  truth.json  (list of {P, Q, p, q, tail, round, sum, bounded, ruleA, ruleB, ...})
Also: searches for denominators whose drawn length is exactly 20,000 steps, and counts the grid.
"""
import sys, json, math
sys.path.insert(0, '/home/agent2/gospel/referee')
import brute, rule

CASES = [(1, 9), (1, 45), (1, 63), (1, 189), (2, 63), (5, 36), (1, 18), (1, 2), (1, 4), (3, 8), (1, 1024), (0, 1), (0, 7), (9, 9),
         (3, 9), (10, 9), (-1, 9), (-2, 45), (7, 45), (44, 45), (1, 9837), (1, 1194649), (1, 2000000), (1999999, 2000000), (1, 1999999),
         (1, 531441), (1, 1594323), (1, 513), (1, 1539), (1, 1125), (1, 3375), (1, 99225), (1, 50), (1, 126), (1, 90), (1, 1), (5, 1),
         (1, 3), (1, 7), (1, 441), (1, 171), (1, 2525), (1, 9009), (1, 1143), (1, 657), (1, 275), (1, 6561), (1, 12), (1, 36), (7, 72),
         (1, 1048576), (1, 1310720), (1, 59049), (1, 19683), (1, 1953125), (1, 117649), (1, 3 * 1093), (1, 5 * 1093 * 9), (123456, 1234567)]


def truth(P, Q, spf, rule_B):
    g = math.gcd(P, Q) or 1
    p, q = P // g, Q // g
    p %= q
    s, m = 0, q
    while m % 2 == 0:
        m //= 2
        s += 1
    tail, n, ssum = brute.cycle_sum(p, q)
    return dict(P=P, Q=Q, p=p, q=q, tail=tail, round=n, sum=ssum, bounded=bool(ssum < 1e-7), m=m,
                ruleA=bool(m > 1 and rule.rule_A(m, spf)), ruleB=bool(m > 1 and rule_B(m)), deg=360.0 * p / q,
                factors=sorted(rule.factor(m, spf).items()))


if __name__ == '__main__':
    N = 2000001
    spf = rule.sieve_spf(N)
    rule_B, d, w = rule.make_rule_B(N, spf)
    out = [truth(P, Q, spf, rule_B) for P, Q in CASES]
    for r in out:
        r['orders'] = {str(l): d[l] for l, e in r['factors'] if l in d}
    # the grid: odd m 3..2001
    closes = spoilt = plain = 0
    for m in range(3, 2002, 2):
        f = rule.factor(m, spf)
        if brute.cycle_sum(1, m)[2] < 1e-9:
            closes += 1
        elif any(e >= 2 for e in f.values()):
            spoilt += 1
        else:
            plain += 1
    # denominators that are drawn to exactly 20,000 steps without being cut: bounded with tail + round = 20000,
    # or unbounded with tail + 4 * round = 20000 (round >= 480 gives 4 rounds)
    exact = []
    for a in range(0, 8):
        for n, kind in (((20000 - a), 'bounded'), ((20000 - a) // 4 if (20000 - a) % 4 == 0 else None, 'unbounded')):
            if n is None:
                continue
            # odd m with ord_m(2) = n and 2^a m <= 2e6
            lim = 2000000 >> a
            # m divides 2^n - 1: try all odd m <= lim with pow(2, n, m) == 1 and exact order n
            for m in range(3, lim + 1, 2):
                if pow(2, n, m) == 1 and rule.order2(m, spf) == n:
                    b = rule_B(m)
                    if (kind == 'bounded') == b:
                        exact.append((a, m, n, kind))
                        if len(exact) > 12:
                            break
            if len(exact) > 12:
                break
        if len(exact) > 12:
            break
    json.dump(dict(cases=out, grid=dict(closes=closes, spoilt=spoilt, plain=plain), exact20000=exact),
              open('/home/agent2/gospel/referee/page/truth.json', 'w'), indent=0)
    print('grid', closes, spoilt, plain)
    print('exactly 20000 drawn, not cut:', exact[:13])
    bad = [(r['P'], r['Q']) for r in out if not (r['bounded'] == r['ruleA'] == r['ruleB'])]
    print('cases where sum, rule A, rule B disagree:', bad)
