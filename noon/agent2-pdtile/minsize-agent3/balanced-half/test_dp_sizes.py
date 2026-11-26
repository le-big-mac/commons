"""Test the lemmas and theorems of proof.md on the size tables written by dp_sizes (the referee's recursion with a dump
added): for a group Z_{p^n q} and a bound S, the table lists, for every stage j <= n, every exact pattern on levels 1..j
and balanced/unbalanced, ALL sizes s <= S that some multiset on Z_{p^j q} attains.  So every claim is tested on every
multiset of at most S elements on Z_{p^j q}, j <= n (as far as the recursion is right).

Also: for balanced patterns whose conjectured minimum is <= S, checks that the least attained size EQUALS it.
usage: test_dp_sizes.py dpout/sizes-*.txt"""
import sys
sys.path.insert(0, "/home/agent3/minsize/prove")
from claims import violations, rule_value, thm_unbalanced


def levels(P, j):
    E = [l for l in range(1, j + 1) if P >> (2 * (l - 1)) & 1]
    F = [l for l in range(1, j + 1) if P >> (2 * (l - 1) + 1) & 1]
    return E, F


grand = 0
for fn in sys.argv[1:]:
    lines = open(fn).read().splitlines()
    hdr = dict(t.split('=') for t in lines[0][2:].split())
    p, q, n, S = int(hdr['p']), int(hdr['q']), int(hdr['n']), int(hdr['S'])
    npairs = 0; nviol = 0; shown = 0
    minima = {}
    for l in lines[1:]:
        t = l.split()
        assert t[0] == 'A'
        j, bal, P = int(t[1]), int(t[2]), int(t[3])
        sizes = [int(s) for s in t[4:]]
        E, F = levels(P, j)
        minima[j, bal, P] = min(sizes)
        for s in sizes:
            npairs += 1
            bad = violations(p, q, j, E, F, bool(bal), s)
            if bad:
                nviol += 1
                if shown < 10:
                    print('  VIOLATION', fn, 'j', j, 'E', E, 'F', F, 'bal', bal, 'size', s, bad); shown += 1
    # equality of minima with the formulas, where the formula is within the bound
    eq = 0; beyond = 0; neq = 0; missing = 0
    eq_u = 0; neq_u = 0; beyond_u = 0
    for j in range(0, n + 1):
        for P in range(4 ** j):
            E, F = levels(P, j)
            val = rule_value(p, q, j, E, F)[0]
            got = minima.get((j, 1, P))
            if val > S:
                beyond += 1
                assert got is None or got >= val
            elif got is None:
                missing += 1; print('  NOTHING ATTAINED though formula', val, '<= S:', fn, j, E, F)
            elif got == val: eq += 1
            else: neq += 1; print('  MINIMUM DIFFERS', fn, j, E, F, 'got', got, 'formula', val)
            valu = thm_unbalanced(p, q, E, F)
            gotu = minima.get((j, 0, P))
            if valu > S: beyond_u += 1
            elif gotu == valu: eq_u += 1
            else: neq_u += 1; print('  UNBALANCED MINIMUM DIFFERS', fn, j, E, F, gotu, valu)
    print(f'{fn}: p={p} q={q} n<={n} S={S}: {npairs} (stage, pattern, balanced?, size) cases, {nviol} violate a claim; '
          f'balanced minima: {eq} equal the formula, {neq} differ, {missing} missing, {beyond} beyond the bound; '
          f'unbalanced minima: {eq_u} equal, {neq_u} differ, {beyond_u} beyond')
    grand += nviol + neq + missing + neq_u
print('TOTAL problems:', grand)
