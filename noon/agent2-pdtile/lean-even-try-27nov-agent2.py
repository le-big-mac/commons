"""A trial, by exhaustion on small groups, of the two statements Yonder fixed for Lean on 27 November 2026 for every n
(even-lean/EvenFinal.lean: exists_signs_all, not_exists_signs_of_exceptionalPair), with the definition they stand on
(ExceptionalPair).  Noon (agent2), 27 November 2026.  Exact, in whole numbers: X^x reduced modulo each cyclotomic polynomial
(the functions of my earlier trial, ~/lean/two-read/try.py, passed as the first argument; its signs(n, M) lists the nonempty
multisets on Z_n with at most M elements that have NO splitting w = u + v with mask(u) - mask(v) divisible by no Phi_d, d | n).

Together the two statements say: for every n >= 1, a nonempty multiset w on Z_n has no good splitting EXACTLY WHEN it is an
exceptional pair, that is, w = {a, b} (two elements, a = b allowed) with the additive order of a - b in Z_n even.
  - the order of x in Z_n is n / gcd(n, x); for a = b it is 1, so a doubled element is never exceptional;
  - Yonder's plain words: "two marks whose hours differ by a number that is not a multiple of the largest power of 2 in the
    number of hours".  Checked here to be the same thing, for every n up to 2,048 and every difference.
Controls that must find differences: three wrong definitions of the exception (a - b odd as a number; a != b; the order of
a - b a multiple of 4).      usage: python -I try-even.py TRY.PY > try-even.out"""
import sys, itertools, importlib.util
from math import gcd

def order(n, x): return n // gcd(n, x % n)
def exceptional(n, w): return len(w) == 2 and order(n, w[0] - w[1]) % 2 == 0
WRONG = [('a - b odd as a number', lambda n, w: len(w) == 2 and (w[0] - w[1]) % 2 == 1),
         ('a and b different', lambda n, w: len(w) == 2 and w[0] != w[1]),
         ('the order of a - b a multiple of 4', lambda n, w: len(w) == 2 and order(n, w[0] - w[1]) % 4 == 0)]

if __name__ == '__main__':
    spec = importlib.util.spec_from_file_location('trial', sys.argv[1]); T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
    print('THE TWO WORDINGS OF THE EXCEPTION: "the order of x in Z_n is even" against "x is not a multiple of the largest power of 2 in n"')
    differ = 0; pairs = 0
    for n in range(1, 2049):
        p2 = n & -n
        for x in range(n):
            pairs += 1
            if (order(n, x) % 2 == 0) != (x % p2 != 0): differ += 1
    print('  n = 1 .. 2048, every x: %d cases, %d where the two differ' % (pairs, differ))
    print('THE STATEMENTS: nonempty multisets on Z_n with at most M elements; those with no good splitting, against the exceptional pairs')
    plan = [(n, 6) for n in range(1, 9)] + [(n, 5) for n in range(9, 17)] + [(n, 4) for n in range(17, 33)] + [(n, 3) for n in (36, 40, 42, 45, 48, 49, 50, 54, 56, 60, 63, 64, 70, 72, 75, 80, 81, 84, 90, 96, 100, 105, 108, 120)] + [(n, 2) for n in (128, 144, 150, 180, 210, 240, 243, 256, 300, 360, 420)]
    total = 0; total_bad = 0; total_exc = 0; mism = 0; wrong = [0, 0, 0]; by_size = {}; odd_groups = 0; odd_bad = 0; odd_tried = 0
    for n, M in plan:
        tried, bad = T.signs(n, M); bad = set(bad); exc = set(); total += tried
        for m in range(1, M + 1):
            if m == 2:
                for w in itertools.combinations_with_replacement(range(n), 2):
                    if exceptional(n, w): exc.add(w)
        # a wrong definition is tried on the pairs only: the other sizes it leaves alone
        for k, (name, f) in enumerate(WRONG):
            wr = set(w for w in itertools.combinations_with_replacement(range(n), 2) if f(n, w)); wrong[k] += len(wr ^ set(b for b in bad if len(b) == 2))
        d = bad ^ exc; mism += len(d); total_bad += len(bad); total_exc += len(exc)
        if n % 2: odd_groups += 1; odd_bad += len(bad); odd_tried += tried
        for b in bad: by_size[len(b)] = by_size.get(len(b), 0) + 1
        print('  n = %4d  M = %d: %8d multisets; %6d with no good splitting; %6d exceptional pairs; %d differences%s' % (n, M, tried, len(bad), len(exc), len(d), ('; first ' + str(sorted(d)[0])) if d else ''), flush=True)
    print('  together %d multisets on %d groups; %d with no good splitting, %d exceptional pairs, %d differences' % (total, len(plan), total_bad, total_exc, mism))
    print('  sizes of the multisets with no good splitting: %s' % ', '.join('%d of size %d' % (v, k) for k, v in sorted(by_size.items())))
    print('  odd n among them: %d groups, %d multisets, %d with no good splitting (counted in the loop above)' % (odd_groups, odd_tried, odd_bad))
    print('CONTROLS, which must find differences (a wrong definition of the exception, against the pairs with no good splitting, over the same groups):')
    for k, (name, f) in enumerate(WRONG): print('  "%s": %d differences' % (name, wrong[k]))
