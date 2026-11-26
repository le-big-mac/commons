"""Is the conjunction of the Lean hypotheses hk, h2, h34 of Pnq.balanced_plus the same as
"none of the four clauses of the note's rule holds"?  Checked on every pattern (E, F) with 0 in F and some
level of 1..n missing from F, for n = 1..N_MAX and several p (4, 6 and 9 are there because on the tree p need
only be >= 2).

The Lean side is transliterated from the statement as Lean prints it (lean-balanced-26nov-agent3.log):
  E t l is false for l = 0 and for l > n;  F t l (l >= 1) is false for l > n;
  gBeyond t a0 = the levels l of 1..n with F t l, not E t l, a0 < l;
  hk : gBeyond nonempty
  h2 : forall l < a0, not E t l                       (l = 0 included)
  h34: not E t a0  or  (p = 2 and forall b, a0 < b -> (forall g in gBeyond, b < g) -> E t b -> F t b)
The tree statement lets b run over all natural numbers; here b runs to n + 3.
Also checked: the zmod form (1 <= l in h2, b <= n in h34) gives the same truth value.

usage: python -I negation_check.py
"""
import itertools

N_MAX = 8
PS = [2, 3, 4, 5, 6, 7, 9]


def Et(E, n, l):
    return 1 <= l <= n and l in E


def Ft(F, n, l):
    return l == 0 or (1 <= l <= n and l in F)      # 0 in F is the hypothesis F t 0


def lean_tree(p, n, E, F, a0):
    g = [l for l in range(1, n + 1) if Ft(F, n, l) and not Et(E, n, l) and a0 < l]
    hk = bool(g)
    h2 = all(not Et(E, n, l) for l in range(0, a0))
    h34 = (not Et(E, n, a0)) or (p == 2 and all(
        Ft(F, n, b) for b in range(a0 + 1, n + 4) if all(b < x for x in g) and Et(E, n, b)))
    return hk, h2, h34


def lean_zmod(p, n, E, F, a0):
    g = [l for l in range(1, n + 1) if l in F and l not in E and a0 < l]
    hk = bool(g)
    h2 = all(l not in E for l in range(1, a0))
    h34 = (a0 not in E) or (p == 2 and all(
        b in F for b in range(a0 + 1, n + 1) if all(b < x for x in g) and b in E))
    return hk, h2, h34


def note(p, n, E, F, a0):
    """clauses (1) to (4) as section 3 of the note words them"""
    deeper = [l for l in range(a0 + 1, n + 1) if l in F and l not in E]
    c1 = len(deeper) == 0
    c2 = any(l in E for l in range(1, a0))
    c3 = a0 in E and p >= 3
    c4 = bool(deeper) and a0 in E and p == 2 and any(l in E and l not in F for l in range(a0 + 1, deeper[0]))
    return c1, c2, c3, c4


def main():
    total = bad_all = bad_tree_zmod = 0
    bad_each = [0, 0, 0]          # hk vs not (1);  h2 vs not (2);  h34 vs not (3) and not (4), among patterns with k' >= 1
    edge_a0_n = edge_p2 = edge_beyond = 0
    for p in PS:
        for n in range(1, N_MAX + 1):
            levels = range(1, n + 1)
            for Em in range(1 << n):
                E = {l for l in levels if (Em >> (l - 1)) & 1}
                for Fm in range((1 << n) - 1):                      # F = all levels left out
                    F = {l for l in levels if (Fm >> (l - 1)) & 1}
                    a0 = min(l for l in levels if l not in F)
                    hk, h2, h34 = lean_tree(p, n, E, F, a0)
                    c1, c2, c3, c4 = note(p, n, E, F, a0)
                    total += 1
                    if (hk and h2 and h34) != (not (c1 or c2 or c3 or c4)):
                        bad_all += 1
                    if lean_zmod(p, n, E, F, a0) != (hk, h2, h34):
                        bad_tree_zmod += 1
                    bad_each[0] += hk != (not c1)
                    bad_each[1] += h2 != (not c2)
                    if hk:
                        bad_each[2] += h34 != (not c3 and not c4)
                    edge_a0_n += (a0 == n)
                    edge_p2 += (p == 2 and hk)
                    g = [l for l in levels if l in F and l not in E and a0 < l]
                    edge_beyond += bool(g) and any(l in E and l not in F and l > max(g) for l in levels)
    print(f"patterns tried (p in {PS}, n = 1..{N_MAX}, 0 in F, F not all levels): {total}")
    print(f"   [hk and h2 and h34] differs from [none of the four clauses holds] in: {bad_all}")
    print(f"   hk differs from not-(1) in: {bad_each[0]};  h2 differs from not-(2) in: {bad_each[1]};  "
          f"where k' >= 1, h34 differs from not-(3)-and-not-(4) in: {bad_each[2]}")
    print(f"   tree form and zmod form of the three hypotheses differ in: {bad_tree_zmod}")
    print(f"   edge cases among them: a0 = n: {edge_a0_n};  p = 2 with k' >= 1: {edge_p2};  "
          f"a level of E not in F beyond every level of gBeyond: {edge_beyond}")


if __name__ == '__main__':
    main()
