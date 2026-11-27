"""Referee's check of the OEIS draft: sequences A and B by the blind step's rule.py (rule A by orders, rule B by primes). Output: oeis-check.out"""
import sys, re, math
sys.path.insert(0, '/home/agent2/gospel/referee')
import rule, brute
if __name__ == '__main__':
    out = open('/home/agent2/gospel/referee/oeis-check.out', 'w')
    N = 10 ** 6
    spf = rule.sieve_spf(N)
    rule_B, d, w = rule.make_rule_B(N, spf)
    A = []; B = []
    for m in range(3, N + 1, 2):
        f = rule.factor(m, spf)
        if rule_B(m): A.append(m)
        elif any(e >= 2 for e in f.values()): B.append(m)
    # form by orders for m <= 10^5, as the Name says
    bad = sum(1 for m in range(3, 10 ** 5, 2) if (rule.rule_A(m, spf)) != (m in set(A[:7000])))
    print('Name of A (orders) against rule B, odd m < 10^5: disagreements', bad, file=out)
    for k in range(2, 7):
        print('k=%d: A %d, B %d' % (k, sum(1 for x in A if x <= 10 ** k), sum(1 for x in B if x <= 10 ** k)), file=out)
    draft = open('/home/agent2/drafts-for-owner/6-oeis-two-sequences.md', encoding='utf-8').read()
    datas = re.findall(r'\*\*Data\.\*\*([\d,\s]+)', draft)
    for name, mine, dd in (('A', A, datas[0]), ('B', B, datas[1])):
        terms = [int(x) for x in re.findall(r'\d+', dd)]
        print('data %s: %d terms; equal to my first %d: %s' % (name, len(terms), len(terms), terms == mine[:len(terms)]), file=out)
    for name, mine in (('A', A), ('B', B)):
        rows = [l.split() for l in open('/home/agent2/drafts-for-owner/6-oeis/b-%s.txt' % name) if l.strip() and not l.startswith('#')]
        idx = [int(r[0]) for r in rows]; vals = [int(r[1]) for r in rows]
        print('b-%s: %d rows; indices 1..n: %s; first %d last %d; equal to my first %d: %s; my count to 20000: %d, to 100000: %d'
              % (name, len(rows), idx == list(range(1, len(rows) + 1)), vals[0], vals[-1], len(vals), vals == mine[:len(vals)],
                 sum(1 for x in mine if x <= 20000), sum(1 for x in mine if x <= 100000)), file=out)
    # 9r, by sums for r < 2000 and by rule to 10^5
    badsum = sum(1 for r in range(5, 2000, 2) if spf[r] == r and ((brute.cycle_sum(1, 9 * r)[2] >= brute.TOL) != (d[r] % 3 == 0)))
    badrule = sum(1 for r in range(5, N // 9, 2) if spf[r] == r and ((9 * r in set()) or ((not rule_B(9 * r)) != (d[r] % 3 == 0))))
    print('9r in B iff 3 | ord_r(2): failures by sums (r < 2000): %d; by rule (r < %d): %d' % (badsum, N // 9, badrule), file=out)
    # p^e a term unless ord same as mod p
    bad = 0; n = 0
    for p in range(3, 1000, 2):
        if spf[p] != p: continue
        e = 2
        while p ** e <= N:
            n += 1
            same = rule.order2(p ** e, spf) == d[p]
            if rule_B(p ** e) == same: bad += 1
            e += 1
    print('p^e (p < 1000, p^e <= 10^6, %d cases): term unless same order as mod p: failures %d' % (n, bad), file=out)
    # powerful non-Wieferich => term
    bad = sum(1 for m in range(3, N + 1, 2) if all(e >= 2 for e in rule.factor(m, spf).values()) and not rule_B(m))
    print('odd m <= 10^6 with every prime squared (no Wieferich square below 10^6): not a term: %d' % bad, file=out)
    # formula offsets: A002326(n) = order of 2 mod 2n+1; A007947(m) = rad(m)
    print('orders: 45 ->', rule.order2(45, spf), ' 15 ->', rule.order2(15, spf), ' 63 ->', rule.order2(63, spf), ' 21 ->', rule.order2(21, spf), file=out)
    print('171, 9009, 2525 in B:', 171 in B, 9009 in B, 2525 in B, ' first of B:', B[0], file=out)
    out.close()
    print(open('/home/agent2/gospel/referee/oeis-check.out').read())
