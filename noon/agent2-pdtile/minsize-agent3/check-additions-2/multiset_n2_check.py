"""The two tree statements (balanced_base, balanced_plus) as read from the Lean text, tried on every balanced
MULTISET of up to S elements on Z_{p^2} x Z_q, in the tree form of Pnq/Tree.lean (n = 2).

Why: the trial on sets never reaches a pattern with k' >= 1 and a0 in E, so it says nothing of the hypothesis
h34.  With n = 2 the pattern E = {1}, F = {0, 2} has a0 = 1 in E and k' = 1: for p = 2 the 'p = 2' branch of h34
holds (nothing lies strictly between), for p >= 3 h34 fails (clause (3) of the note's rule).

The tree, as in Lean: a root with p children, each child with p leaves, each leaf a vector in N^q.
  E t 1: the children have equal sizes.        E t 2: in every child the leaves have equal sizes.
  F t 0: the layer counts of the root are equal.
  F t 1: any two children have layer vectors that differ by a constant vector.
  F t 2: in every child any two leaves differ by a constant vector.
A child is summarised by (its layer vector, leaves of equal sizes?, leaves of equal shapes?).

usage: python -I multiset_n2_check.py p q S
"""
import itertools
import sys


def vectors(q, total):
    """all vectors in N^q with sum exactly total"""
    if q == 1:
        yield (total,)
        return
    for a in range(total + 1):
        for rest in vectors(q - 1, total - a):
            yield (a,) + rest


def const_diff(u, v):
    d = u[0] - v[0]
    return all(a - b == d for a, b in zip(u, v))


def main():
    p, q, S = (int(v) for v in sys.argv[1:4])
    n = 2
    leaves = [v for t in range(S + 1) for v in vectors(q, t)]
    by_total = {}
    for v in leaves:
        by_total.setdefault(sum(v), []).append(v)
    # child summaries, with the least... (the size is the sum of the vector, so nothing more is kept)
    summ = set()

    def rec(k, left, chosen):
        if k == 0:
            g = tuple(sum(c[j] for c in chosen) for j in range(q))
            fE = all(sum(c) == sum(chosen[0]) for c in chosen)
            fF = all(const_diff(c, chosen[0]) for c in chosen)
            summ.add((g, fE, fF))
            return
        for t in range(left + 1):
            for v in by_total[t]:
                # leaves in non-decreasing order: the summary does not depend on their order
                if chosen and v < chosen[-1]:
                    continue
                rec(k - 1, left - t, chosen + [v])

    rec(p, S, [])
    summ = sorted(summ)
    tot = [sum(s[0]) for s in summ]
    least = {}                    # (E, F levels >= 1) -> least size of a balanced multiset, not empty
    count_roots = 0

    def roots(k, left, start, chosen):
        nonlocal count_roots
        if k == 0:
            count_roots += 1
            gs = [summ[i][0] for i in chosen]
            g = tuple(sum(x[j] for x in gs) for j in range(q))
            size = sum(g)
            if size == 0 or any(x != g[0] for x in g):
                return                                    # empty, or not F t 0
            E = set()
            F = set()
            if all(tot[i] == tot[chosen[0]] for i in chosen):
                E.add(1)
            if all(summ[i][1] for i in chosen):
                E.add(2)
            if all(const_diff(x, gs[0]) for x in gs):
                F.add(1)
            if all(summ[i][2] for i in chosen):
                F.add(2)
            key = (tuple(sorted(E)), tuple(sorted(F)))
            if key not in least or size < least[key]:
                least[key] = size
            return
        for i in range(start, len(summ)):                 # children in non-decreasing order of summary
            if tot[i] <= left:
                roots(k - 1, left - tot[i], i, chosen + [i])

    roots(p, S, 0, [])
    print(f"p={p}, q={q}, n=2: every balanced multiset of at most {S} elements, by {len(summ)} summaries of a child "
          f"({count_roots} roots up to the order of the children)")
    bad = 0
    for (E, F), size in sorted(least.items()):
        E, F = set(E), set(F)
        e = len(E)
        miss = [l for l in range(1, n + 1) if l not in F]
        if not miss:
            ok = size >= q * p ** e
            bad += not ok
            print(f"   E={sorted(E)} F={[0] + sorted(F)}: least size {size}; F all levels, q p^e = {q * p ** e}{'' if ok else '  BELOW'}")
            continue
        a0 = miss[0]
        g = [l for l in range(1, n + 1) if l in F and l not in E and a0 < l]
        hk = bool(g)
        h2 = all(l not in E for l in range(0, a0))
        h34 = (a0 not in E) or (p == 2 and all(b in F for b in range(a0 + 1, n + 1)
                                                if all(b < x for x in g) and b in E))
        base = q * p ** (e + len(g))
        plus = q * p ** e * (p ** len(g) + 1)
        applies = hk and h2 and h34
        bound = plus if applies else base
        ok = size >= bound
        bad += not ok
        note = ""
        if hk:
            note = ("; plus applies" + ("" if a0 not in E else " through the p = 2 branch of h34")) if applies else \
                   f"; plus does not apply (h2 {h2}, h34 {h34}); its bound would be {plus}" + ("  and is BROKEN" if size < plus else "")
        print(f"   E={sorted(E)} F={[0] + sorted(F)}: least size {size}; a0={a0}, k'={len(g)}; base bound {base}{note}"
              f"{'' if ok else '  BELOW THE BOUND THAT APPLIES'}")
    print(f"   patterns met: {len(least)}; least size below the bound that applies: {bad}")


if __name__ == '__main__':
    main()
