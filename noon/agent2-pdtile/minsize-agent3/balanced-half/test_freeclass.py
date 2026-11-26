"""Proposition 12 of proof.md (the semantic form of the condition on x), tested exhaustively in small groups.

  Let k' >= 1, G' = the levels of F minus E beyond a0, g1 = min G', E+ = E union G'.
  CLAIM: x = 0  iff  some balanced multiset with exact pattern (E+, F) and exactly q p^(e+k') elements contains a
  nonempty class of depth < g1 all of whose subclasses are balanced ("a free fibre class above g1").

Method: my own exhaustive recursion by explicit summaries (as in test_tree.py summary), with one more component in the
summary of a class: m = the least depth, relative to the class, of a nonempty subclass all of whose subclasses are
balanced (m = 0 if the class itself is one; a large number if there is none).  A class is such a "fibre class" iff it is
balanced and every one of its levels is in its F.  m(parent) = 0 if the parent is a fibre class, else 1 + min over children.
Every multiset of at most S elements is covered, so for each pattern with q p^(e+k') <= S the right-hand side of the claim
is decided exactly.

usage: test_freeclass.py
"""
import sys, time
sys.path.insert(0, "/home/agent3/minsize/prove")
from claims import rule_value
from test_tree import compositions

BIG = 99


def summaries_m(p, q, n, S):
    zero = tuple([0] * q)
    stage = [set()]
    for s in range(1, S + 1):
        for v in compositions(s, q):
            stage[0].add((v, 0, 0, 0 if len(set(v)) == 1 else BIG))
    for j in range(1, n + 1):
        full = (1 << (j - 1)) - 1
        prev = [(zero, full, full, BIG)] + sorted(stage[-1], key=lambda t: sum(t[0]))
        sizes = [sum(t[0]) for t in prev]
        cur = set()

        def rec(start, left, chosen):
            if len(chosen) == p:
                vs = [c[0] for c in chosen]
                tot = tuple(sum(v[l] for v in vs) for l in range(q))
                if not any(tot): return
                tots = [sum(v) for v in vs]
                eqt = len(set(tots)) == 1
                eqs = all(len(set(v[l] - vs[0][l] for l in range(q))) == 1 for v in vs[1:])
                e = full; f = full
                for c in chosen: e &= c[1]; f &= c[2]
                E = (e << 1) | eqt; F = (f << 1) | eqs
                if len(set(tot)) == 1 and F == (1 << j) - 1: m = 0
                else: m = min(BIG, 1 + min(c[3] for c in chosen))
                cur.add((tot, E, F, m))
                return
            for i in range(start, len(prev)):
                if sizes[i] > left: break
                rec(i, left - sizes[i], chosen + [prev[i]])
        rec(0, S, [])
        stage.append(cur)
    return stage


def run(p, q, n, S):
    t0 = time.time()
    st = summaries_m(p, q, n, S)[n]
    # best[(Emask, Fmask, size)] = least m among balanced roots
    best = {}
    for (v, e, f, m) in st:
        if len(set(v)) == 1:
            k = (e, f, sum(v))
            if m < best.get(k, BIG + 1): best[k] = m
    tested = agree = skipped = 0; x0 = x1 = 0
    for Em in range(2 ** n):
        E = [a for a in range(1, n + 1) if Em >> (a - 1) & 1]
        for Fm in range(2 ** n - 1):
            F = [a for a in range(1, n + 1) if Fm >> (a - 1) & 1]
            val, x, k1, a0 = rule_value(p, q, n, E, F)
            if not k1: continue
            G = sorted(a for a in F if a > a0 and a not in E)
            g1 = G[0]
            size = q * p ** (len(E) + k1)
            if size > S: skipped += 1; continue
            Eplus = Em
            for a in G: Eplus |= 1 << (a - 1)
            m = best.get((Eplus, Fm, size))
            assert m is not None, 'no multiset of the least size for the pattern (E+, F)?'
            rhs = (m <= g1 - 1)
            tested += 1
            if rhs == (x == 0): agree += 1
            else: print('   DISAGREE', (p, q, n), 'E', E, 'F', [0] + F, 'x', x, 'least depth of a free fibre class', m, 'g1', g1)
            if x == 0: x0 += 1
            else: x1 += 1
    print(f'p={p} q={q} n={n}, every multiset of at most {S} elements: {tested} patterns with k\'>=1 and q p^(e+k\') <= {S} '
          f'({x0} with x=0, {x1} with x=1), claim right on {agree}; {skipped} patterns beyond the bound; {time.time()-t0:.0f} s', flush=True)
    return tested - agree


if __name__ == '__main__':
    bad = 0
    for (p, q, n, S) in [(2, 3, 2, 12), (3, 2, 2, 18), (2, 3, 3, 24), (2, 5, 2, 20), (3, 2, 3, 18), (5, 2, 2, 20), (2, 3, 4, 24), (2, 5, 3, 20)]:
        bad += run(p, q, n, S)
    print('TOTAL disagreements:', bad)
