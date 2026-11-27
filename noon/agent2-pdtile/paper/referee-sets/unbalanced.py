r"""The remark after Corollary 21: 'The least multisets of Section 4 for the unbalanced half have multiplicities at most 2,
so there every s with an odd prime factor will do.'  The construction is typed from Section 4.1 of the paper:
  Z_M = Z_{p^n} x Z_q by x -> (x mod p^n, x mod q);  u = sum_a u_a p^(a-1), u_a the digit of level a;
  D(T) = strings that are 0 outside T;  tau(u) = 1 if E\F is not empty and every digit of u at a level of E\F is nonzero,
  else 0;  A1 = {(u, tau(u)) : u in D(E u F)},  A2 = Fib(D(E)) = {(u, w) : u in D(E), all w};
  A = A1 if F subset of E, A = A1 + A2 otherwise.
Checked for every unbalanced pattern of each group listed: |A| = Theorem 1's number, the pattern is exactly (E, F,
unbalanced) by exact division, the largest multiplicity; then A is lifted along r = 3, 5, 7 by the recipe of
Proposition 20 with j = 1 (prop_test.check) and the lift is checked to be a set with exactly the pattern on Z_{M r}.
usage: unbalanced.py"""
import itertools, random, collections
from cyc import pattern
from thm import theorem_m, D_of
from prop_test import check
rnd = random.Random(3)

def crt(u, w, P, q):
    for x in range(u, P * q, P):
        if x % q == w: return x

def strings(p, n, T):
    lv = sorted(T)
    for digs in itertools.product(range(p), repeat=len(lv)):
        yield {a: d for a, d in zip(lv, digs)}

def construct(p, q, n, E, F):
    E = set(E); F = set(F); P = p ** n; A = collections.Counter()
    EF = E - F
    for dg in strings(p, n, E | F):
        u = sum(d * p ** (a - 1) for a, d in dg.items())
        tau = 1 if EF and all(dg[a] != 0 for a in EF) else 0
        A[crt(u, tau % q, P, q)] += 1
    if not F <= E:
        for dg in strings(p, n, E):
            u = sum(d * p ** (a - 1) for a, d in dg.items())
            for w in range(q): A[crt(u, w, P, q)] += 1
    return dict(A)

tot = ok = 0; maxmult = collections.Counter(); lifts = collections.Counter(); lifts_ok = collections.Counter()
for (p, q, n) in [(2, 3, 1), (3, 2, 1), (2, 3, 2), (3, 2, 2), (2, 5, 2), (3, 5, 2), (5, 2, 2), (5, 3, 2), (2, 3, 3), (3, 2, 3), (2, 5, 3),
                  (2, 3, 4), (2, 7, 2), (7, 2, 2), (3, 7, 2), (5, 2, 3), (2, 3, 5), (3, 2, 4), (2, 11, 2)]:
    M = p ** n * q; g_ok = g = 0; gm = 0
    lv = list(range(1, n + 1))
    for eb in range(2 ** n):
        for fb in range(2 ** n):
            E = [a for a in lv if eb >> (a - 1) & 1]; F = [a for a in lv if fb >> (a - 1) & 1]
            A = construct(p, q, n, E, F)
            m = theorem_m(p, q, n, E, F, False); D = D_of(p, q, n, E, F, False)
            good = (sum(A.values()) == m and pattern(A, M) == D)
            tot += 1; ok += good; g += 1; g_ok += good
            mx = max(A.values()); maxmult[mx] += 1; gm = max(gm, mx)
            assert (mx == 1) == (set(F) <= set(E)) or mx == 1      # a set when F is inside E
            if M <= 200:
                for r in (3, 5, 7):
                    if M * r > 800: continue
                    res, cases, _ = check(A, M, r, 1, rnd)
                    lifts[r] += 1; lifts_ok[r] += res
    print(f'Z_{M} (p={p}, q={q}, n={n}): unbalanced patterns {g}; the construction of Section 4.1 has the theorem\'s size and exactly the pattern: {g_ok}; largest multiplicity: {gm}', flush=True)
print(f'all: {tot} constructions, {ok} right; largest multiplicity by number of constructions: {dict(sorted(maxmult.items()))}')
for r in (3, 5, 7):
    print(f'lifted along {r} (one step of the recipe) to a set on Z_(M {r}) with the same size and exactly the pattern: {lifts_ok[r]} of {lifts[r]}')
