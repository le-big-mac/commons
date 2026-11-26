"""Referee: Lemma 10 of proof-as-sent.md tested directly, for EVERY choice of (a0, T1, T2, H, mode):
 (S1) every class of depth < a0 is balanced and |S| = mu q p^(|T1|+|T2|), mu = 1, p, 2 in modes U, Q, W;
 (S5) for Phi = 0 and for random sums Phi of multisets m.Fib(D): S + Phi is balanced and
      F(S + Phi) = {0} u [1, a0-1] u (T2 \\ H).
Also the two numerical examples in the text (after Lemma 5, and at the end of section 7).

usage: ref_lemma10.py p q nmax seed
"""
import sys, itertools, random
import numpy as np
from ref_common import literal_patterns, bits_to_set
from ref_construct import digits, D_set, Fib, shape_part, my_pattern


def subsets(lst):
    return itertools.chain.from_iterable(itertools.combinations(lst, r) for r in range(len(lst) + 1))


def main():
    p, q, nmax, seed = (int(x) for x in sys.argv[1:5])
    rng = random.Random(seed)
    for n in range(1, nmax + 1):
        dig = digits(p, n)
        nset = nbad = nphi = 0
        for a0 in range(1, n + 1):
            for T1 in subsets(range(1, a0)):
                for T2 in subsets(range(a0 + 1, n + 1)):
                    for H in subsets(T2):
                        for mode in "UQW":
                            S = shape_part(p, q, n, dig, a0, set(T1), set(T2), set(H), mode)
                            nset += 1
                            mu = {"U": 1, "Q": p, "W": 2}[mode]
                            ok = S.min() >= 0 and int(S.sum()) == mu * q * p ** (len(T1) + len(T2))
                            pats = literal_patterns(p, q, n, S.reshape(1, p ** n, q))
                            for d in range(0, a0):
                                ok = ok and bool(pats[d]["bal"].all())
                            wantF = {0} | set(range(1, a0)) | (set(T2) - set(H))
                            E, F = my_pattern(p, q, n, S)
                            ok = ok and F == wantF
                            for _ in range(3):
                                A = S.copy()
                                for _ in range(rng.choice((1, 2, 3))):
                                    T = {a for a in range(1, n + 1) if rng.random() < 0.5}
                                    rest = [a for a in range(1, n + 1) if a not in T]
                                    if rest and rng.random() < 0.7:
                                        b = rng.choice(rest)
                                        A = A + Fib(p, q, n, D_set(p, n, dig, T, b, rng.randrange(p)), rng.choice((1, 2, p, p * p)))
                                    else:
                                        A = A + Fib(p, q, n, D_set(p, n, dig, T), rng.choice((1, 2, p)))
                                E2, F2 = my_pattern(p, q, n, A)
                                nphi += 1
                                ok = ok and F2 == wantF
                            if not ok:
                                nbad += 1
                                if nbad <= 3:
                                    print("   FAIL", p, q, n, a0, T1, T2, H, mode, "F found", sorted(F), "wanted", sorted(wantF), "size", int(S.sum()))
        print(f"Lemma 10: p={p} q={q} n={n}: {nset} parameter sets (a0, T1, T2, H, mode), {nphi} sums S + Phi; failures {nbad}", flush=True)


def examples():
    # after Lemma 5: p=2, q=3, class with children (6,0,0) = (3,0,0)+(3,0,0) and (2,2,2) = (2,2,2)+(0,0,0)
    p, q, n = 2, 3, 2
    W = np.zeros((4, 3), dtype=np.int64)        # u = u1 + 2 u2
    W[0] = (3, 0, 0); W[2] = (3, 0, 0)          # u1 = 0: grandchildren u2 = 0, 1
    W[1] = (2, 2, 2); W[3] = (0, 0, 0)          # u1 = 1
    r = literal_patterns(p, q, n, W.reshape(1, 4, 3))[0]
    print("example after Lemma 5: vector", r["G"][0, 0].tolist(), "total", int(r["tot"][0, 0]), "balanced", bool(r["bal"][0, 0]),
          "E", sorted(bits_to_set(r["E"][0, 0])), "F", sorted(bits_to_set(r["F"][0, 0])),
          "| 12 in S_2+ ?", any(4 * t + 3 * m == 12 for t in range(1, 4) for m in range(1, 5)), "| 12 in Q_2 ?", 12 % 12 == 0)
    # end of section 7: p=2, q=3, n=3, classes of depth 2 (prefixes 00, 01, 10, 11 = (u1,u2)):
    # (6,0,0), (2,2,2), (0,6,6), (4,4,4); (6,0,0) and (0,6,6) split in two equal halves, the others in one child
    n = 3
    W = np.zeros((8, 3), dtype=np.int64)        # u = u1 + 2 u2 + 4 u3
    def put(u1, u2, vec, split):
        base = u1 + 2 * u2
        if split:
            W[base] = [v // 2 for v in vec]; W[base + 4] = [v // 2 for v in vec]
        else:
            W[base] = vec
    put(0, 0, (6, 0, 0), True); put(0, 1, (2, 2, 2), False); put(1, 0, (0, 6, 6), True); put(1, 1, (4, 4, 4), False)
    E, F = my_pattern(p, q, n, W)
    print("example at the end of section 7: size", int(W.sum()), "pattern E", sorted(E), "F", sorted(F), "(text: E={2}, F={0,3}, 36 elements)")


if __name__ == "__main__":
    if sys.argv[1] == "examples":
        examples()
    else:
        main()
