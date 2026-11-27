"""A trial, by exhaustion on small groups, of the four statements Yonder fixed for Lean on 27 November 2026 that matter outside
(SignFinal.lean: exists_signs_odd, exists_lift_two_all, sizes_eq_two_all; SignMul.lean: sizes_eq_mul_all).
Noon (agent2), 27 November 2026.  Exact, in whole numbers: X^x reduced modulo each cyclotomic polynomial (the functions of my
earlier trial, ~/lean/two-read/try.py, passed as the first argument).

  signs(n, M):  every nonempty multiset w on Z_n, n ODD, with at most M elements can be split w = u + v so that no Phi_d, d | n
                (d = 1 included), divides mask(u) - mask(v).
  lift2(N, M):  every nonempty multiset w on Z_N, ANY N, with at most M elements has a w' on Z_2N that reduces to w, with no Phi_d,
                d | 2N, d not dividing N, dividing mask(w').
  sizes(N, s, T): for every set P of divisors of N, the sizes up to T of the nonempty multisets on Z_(N s) whose mask is divisible
                by Phi_d, d | N s, d > 1, exactly for d in P are the sizes up to T of those on Z_N with exactly the pattern P
                (d | N, d > 1).  (The theorem is of all sizes; a census sees those up to T.)
Controls that must find failures: signs on even n; lift2 asked for no cyclotomic divisor at all; sizes with P not a set of divisors
of N.   usage: python -I try-signs-all.py TRY.PY > try-signs-all.out"""
import sys, itertools, importlib.util

def census(T, n, top):
    ds = [d for d in T.divisors(n) if d > 1]; R = {d: T.residues(n, d) for d in ds}; out = {}; count = 0
    for m in range(1, top + 1):
        for w in itertools.combinations_with_replacement(range(n), m):
            count += 1
            pat = frozenset(d for d in ds if not any(sum(R[d][x][j] for x in w) for j in range(len(R[d][0]))))
            out.setdefault(pat, set()).add(m)
    return out, count

def sizes(T, N, s, top):
    big, c1 = census(T, N * s, top); small, c2 = census(T, N, top); dN = set(d for d in T.divisors(N) if d > 1); differ = []; inside = 0
    for P in set(big) | set(small):
        if P <= dN:
            inside += 1
            if big.get(P, set()) != small.get(P, set()): differ.append((sorted(P), sorted(big.get(P, set())), sorted(small.get(P, set()))))
    # the control: a pattern on the big group that is not a set of divisors of N; the small group's sizes for its part inside N
    outside = [(sorted(P), sorted(big[P]), sorted(small.get(frozenset(P & dN), set()))) for P in big if not P <= dN]
    return c1 + c2, inside, differ, outside

if __name__ == '__main__':
    spec = importlib.util.spec_from_file_location('trial', sys.argv[1]); T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
    print('SIGNS (exists_signs_odd): nonempty multisets on Z_n, n odd, with at most M elements; those with no good signing')
    total = 0
    for n, M in [(1, 12), (3, 16), (5, 11), (7, 8), (9, 8), (11, 6), (15, 6), (21, 5), (27, 5), (33, 4), (45, 4), (49, 4), (81, 3), (105, 3), (135, 3), (165, 3), (195, 3), (231, 2), (315, 2), (1155, 2)]:
        tried, bad = T.signs(n, M); total += tried
        print('  n = %4d  M = %2d: %8d multisets, %d without a good signing%s' % (n, M, tried, len(bad), ('; first ' + str(bad[0])) if bad else ''), flush=True)
    print('  together %d multisets (n = 105, 165, 195, 231, 315 and 1155 have three or four odd primes; n = 3 goes to 16 elements, past the 14 where the plan needs its sharper count)' % total)
    print('  controls, which must fail (even n, outside the statement):')
    for n, M in [(2, 4), (4, 3), (6, 3), (10, 3), (12, 3)]:
        tried, bad = T.signs(n, M); sizes_bad = sorted(set(len(b) for b in bad))
        print('  n = %4d  M = %2d: %8d multisets, %d without a good signing%s; their sizes %s' % (n, M, tried, len(bad), ('; first ' + str(bad[0])) if bad else '', sizes_bad), flush=True)
    print('LIFT ALONG 2 (exists_lift_two_all): nonempty multisets on Z_N with at most M elements; those with no lift to Z_2N free of new cyclotomic divisors')
    total = 0
    for N, M in [(k, 5 if k <= 8 else 4) for k in range(1, 25)] + [(27, 3), (28, 3), (30, 4), (33, 3), (35, 3), (42, 3), (63, 3), (70, 3), (105, 3), (210, 2)]:
        tried, bad = T.lift2(N, M); total += tried
        print('  N = %3d  M = %d: %8d multisets, %d without such a lift%s' % (N, M, tried, len(bad), ('; first ' + str(bad[0])) if bad else ''), flush=True)
    print('  together %d multisets' % total)
    print('  control, which must fail (asked that no cyclotomic polynomial at all divide the lift):')
    for N, M in [(3, 3), (6, 3), (10, 3)]:
        tried, bad = T.lift2(N, M, too_much=True); print('  N = %3d  M = %d: %8d multisets, %d without such a lift%s' % (N, M, tried, len(bad), ('; first ' + str(bad[0])) if bad else ''), flush=True)
    print('SIZES (sizes_eq_two_all with s = 2, sizes_eq_mul_all): the sizes up to T with each pattern P of divisors of N, on Z_(N s) and on Z_N')
    total = 0; alld = 0
    for N, s, top in [(1, 2, 8), (1, 3, 8), (1, 4, 7), (1, 6, 6), (1, 12, 5), (2, 2, 7), (2, 3, 6), (2, 4, 6), (2, 6, 5), (3, 2, 6), (3, 3, 6), (3, 4, 5), (3, 6, 4), (4, 2, 6), (4, 3, 5), (4, 4, 5), (5, 2, 6), (5, 3, 5), (6, 2, 5), (6, 3, 4), (6, 4, 4), (8, 2, 5), (9, 2, 4), (9, 3, 4), (10, 2, 4), (12, 2, 4), (15, 2, 4)]:
        c, inside, differ, outside = sizes(T, N, s, top); total += c; alld += len(differ)
        ctl = [o for o in outside if o[1] != o[2]]
        print('  N = %2d  s = %2d  T = %d: %7d multisets; %2d patterns of divisors of N seen, %d with different sizes%s | control: %d patterns on Z_%d that are not sets of divisors of N, %d of them with other sizes than their part inside N has on Z_N'
              % (N, s, top, c, inside, len(differ), ('; first ' + str(differ[0])) if differ else '', len(outside), N * s, len(ctl)), flush=True)
    print('  together %d multisets; %d differences' % (total, alld))
