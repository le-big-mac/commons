"""The two tree statements (balanced_base, balanced_plus) as read from the Lean text, tried on every balanced
MULTISET of up to S elements on Z_{p^n} x Z_q, in the tree form of Pnq/Tree.lean, for any n.
A second program for what multiset_n2_check.py does for n = 2, written so that n = 3 can be reached:
subtrees are replaced by summaries, and the root is built only from children whose layer vectors add up to a
constant vector.

The tree, as in Lean (Pnq/Tree.lean): a node has p children; a leaf is a vector in N^q.
  E t 1: the children have equal sizes.            E t (l+1): every child has E at l.
  F t 0: the layer counts of t are equal.
  F t 1: any two children have layer vectors that differ by a constant vector.   F t (l+1): every child has F at l.
Summary of a subtree with h levels: (layer vector, (E t 1..h), (F t 1..h)).

For each pattern (E, F) with F t 0 that some multiset of at most S elements has, the least size found is set
against the bound that the Lean statements give for it: q p^e when F is all levels (from the divisibility),
balanced_base, and balanced_plus where its hypotheses hk, h2, h34 hold.  Where k' >= 1 and they fail, the
bound of balanced_plus is shown too, to see whether it would be broken.

usage: python -I multiset_tree_check.py p q n S
"""
import itertools
import sys


def vectors(q, total):
    if q == 1:
        yield (total,)
        return
    for a in range(total + 1):
        for rest in vectors(q - 1, total - a):
            yield (a,) + rest


def const_diff(u, v):
    d = u[0] - v[0]
    return all(a - b == d for a, b in zip(u, v))


def combine(children, q):
    """summary of the node whose children have these summaries"""
    gs = [c[0] for c in children]
    g = tuple(sum(x[j] for x in gs) for j in range(q))
    t0 = sum(gs[0])
    e1 = all(sum(x) == t0 for x in gs)
    f1 = all(const_diff(x, gs[0]) for x in gs)
    h = len(children[0][1])
    E = (e1,) + tuple(all(c[1][l] for c in children) for l in range(h))
    F = (f1,) + tuple(all(c[2][l] for c in children) for l in range(h))
    return (g, E, F)


def level_up(summ, p, q, S):
    """all summaries of nodes with p children from summ and at most S elements"""
    summ = sorted(summ)
    tot = [sum(s[0]) for s in summ]
    out = set()

    def rec(k, left, start, chosen):
        if k == 0:
            out.add(combine(chosen, q))
            return
        for i in range(start, len(summ)):
            if tot[i] <= left:
                rec(k - 1, left - tot[i], i, chosen + [summ[i]])

    rec(p, S, 0, [])
    return out


def balanced_roots(summ, p, q, S):
    """summaries of the balanced roots: p - 1 children chosen freely, the last one fixed up to a constant"""
    summ = sorted(summ)
    tot = [sum(s[0]) for s in summ]
    by_g = {}
    for s in summ:
        by_g.setdefault(s[0], []).append(s)
    least = {}

    def finish(chosen):
        G = tuple(sum(c[0][j] for c in chosen) for j in range(q))
        m = max(G)
        while q * m <= S:
            last = tuple(m - x for x in G)
            for s in by_g.get(last, ()):
                g, E, F = combine(chosen + [s], q)
                size = sum(g)
                if size:
                    key = (E, F)
                    if key not in least or size < least[key]:
                        least[key] = size
            m += 1

    def rec(k, left, start, chosen):
        if k == 0:
            finish(chosen)
            return
        for i in range(start, len(summ)):
            if tot[i] <= left:
                rec(k - 1, left - tot[i], i, chosen + [summ[i]])

    rec(p - 1, S, 0, [])
    return least


def main():
    p, q, n, S = (int(v) for v in sys.argv[1:5])
    summ = {(v, (), ()) for t in range(S + 1) for v in vectors(q, t)}
    sizes = [len(summ)]
    for h in range(1, n):
        summ = level_up(summ, p, q, S)
        sizes.append(len(summ))
    least = balanced_roots(summ, p, q, S)
    print(f"p={p}, q={q}, n={n}: every balanced multiset of at most {S} elements (summaries of subtrees with 0..{n - 1} levels: {sizes})")
    bad = 0
    rows = []
    for (Ef, Ff), size in least.items():
        E = {l + 1 for l in range(n) if Ef[l]}
        F = {l + 1 for l in range(n) if Ff[l]}
        rows.append((sorted(E), sorted(F), size))
    for Es, Fs, size in sorted(rows):
        E, F = set(Es), set(Fs)
        e = len(E)
        miss = [l for l in range(1, n + 1) if l not in F]
        if not miss:
            ok = size >= q * p ** e
            bad += not ok
            print(f"   E={Es} F={[0] + Fs}: least size {size}; F all levels, q p^e = {q * p ** e}{'' if ok else '  BELOW'}")
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
        if hk and applies:
            note = f"; plus applies{'' if a0 not in E else ' through the p = 2 branch of h34'}, bound {plus}"
        elif hk:
            note = f"; plus does not apply (h2 {h2}, h34 {h34}); its bound would be {plus}{' and is BROKEN' if size < plus else ''}"
        print(f"   E={Es} F={[0] + Fs}: least size {size}; a0={a0}, k'={len(g)}; base bound {base}{note}"
              f"{'' if ok else '  BELOW THE BOUND THAT APPLIES'}")
    print(f"   patterns met: {len(least)}; least size below the bound that applies: {bad}")


if __name__ == '__main__':
    main()
