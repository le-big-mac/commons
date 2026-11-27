"""Theorem 1 of the paper (minsize.tex), transcribed by the referee from the paper's text: least size for a pattern on Z_{p^n q}."""
def theorem_value(p, q, n, E, F, balanced):
    E, F = set(E), set(F); e = len(E)
    if not balanced:                                             # (a)
        if F <= E: return p ** e
        return p ** e * (p ** len(F - E) + q)
    if F == set(range(1, n + 1)): return q * p ** e              # (b)
    a0 = min(a for a in range(1, n + 1) if a not in F)           # (c)
    G = {a for a in F - E if a > a0}; k1 = len(G)
    c1 = (k1 == 0)
    c2 = any(a < a0 for a in E)
    c3 = (a0 in E and p >= 3)
    c4 = (k1 >= 1 and a0 in E and p == 2 and any(a0 < b < min(G) for b in E - F))
    x = 0 if (c1 or c2 or c3 or c4) else 1
    return q * p ** e * (p ** k1 + x)
def pattern_to_EF(D, p, q, n):
    """a set D of divisors > 1 of p^n q  ->  (E, F, balanced)"""
    E = {a for a in range(1, n + 1) if p ** a in D}; F = {a for a in range(1, n + 1) if p ** a * q in D}
    assert set(D) == {p ** a for a in E} | {p ** a * q for a in F} | ({q} if q in D else set())
    return E, F, (q in D)
if __name__ == '__main__':
    # the eight values for n = 1 that the paper prints after the theorem
    for p, q in ((2, 3), (3, 2), (3, 5), (5, 2)):
        vals = [theorem_value(p, q, 1, E, F, b) for b in (False, True) for (E, F) in ((set(), set()), ({1}, set()), (set(), {1}), ({1}, {1}))]
        assert vals == [1, p, p + q, p, q, p * q, q, p * q], vals
    # Remark 2 of the paper: balanced, n = 3, F = {3}
    for p, q in ((2, 3), (3, 2), (2, 5), (5, 3)):
        assert theorem_value(p, q, 3, set(), {3}, True) == q * (p + 1)
        assert theorem_value(p, q, 3, {1}, {3}, True) == (q * p * p if p >= 3 else 6 * q)
        assert theorem_value(p, q, 3, {2}, {3}, True) == q * p * (p + 1)
        assert theorem_value(p, q, 3, {1, 2}, {3}, True) == q * p ** 3
    # the remark on r = p: Theorem 1 for n + 1 on patterns without the level n + 1 gives the value of Theorem 1 for n
    import itertools
    cnt = 0
    for p, q in ((3, 2), (3, 5), (5, 2), (5, 3), (7, 2), (2, 3), (2, 5)):      # p = 2 included for the formula's sake (r = p = 2 is not covered by the lemma)
        for n in range(0, 5):
            lv = range(1, n + 1)
            for E in itertools.chain.from_iterable(itertools.combinations(lv, k) for k in range(n + 1)):
                for F in itertools.chain.from_iterable(itertools.combinations(lv, k) for k in range(n + 1)):
                    for b in (False, True):
                        assert theorem_value(p, q, n, E, F, b) == theorem_value(p, q, n + 1, E, F, b); cnt += 1
    print('thm.py: n = 1 values, Remark 2, and "Theorem 1 at n + 1 without the level n + 1 = Theorem 1 at n" on', cnt, 'patterns: all as the paper says')
