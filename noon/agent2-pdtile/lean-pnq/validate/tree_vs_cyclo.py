"""Do the tree conditions E, F of Pnq/Tree.lean mean what the note means?  (agent3 / Yonder)
The Lean file states Lemmas 3, 4 and the counting theorem for a p-ary tree with level conditions defined by recursion.  Lean checks
the proofs; it cannot check that 'E t l' is 'Phi_{p^l} | A' and 'F t l' is 'Phi_{p^l q} | A' for the tree of a set A in Z_{p^n q}.
Here the SAME recursive definitions, transcribed from the Lean source, are evaluated on the tree of A (children = next base-p digit of
x mod p^n, lowest digit first; leaf = indicator over x mod q) and compared with exact division of the mask polynomial by Phi_d.
Every subset containing 0 for small M; random and coset-built sets for larger M."""
import sys, random, itertools
sys.path.insert(0, "/srv/commons/agent2-pdtile/review-agent3-flatness")
from cyclo_exact import divides
def tree(A, p, n, q):
    """nested lists: depth-n p-ary tree, leaf = list of q counts"""
    def build(elems, depth):                 # elems: list of (u_remaining, w)
        if depth == n:
            leaf = [0] * q
            for _, w in elems: leaf[w] += 1
            return leaf
        return [build([(u // p, w) for u, w in elems if u % p == c], depth + 1) for c in range(p)]
    return build([(x % p ** n, x % q) for x in A], 0)
def lay(t, depth, n, q):
    if depth == n: return t
    L = [lay(c, depth + 1, n, q) for c in t]; return [sum(l[j] for l in L) for j in range(q)]
def size(t, depth, n, q): return sum(lay(t, depth, n, q))
def E(t, depth, n, q, l):                    # transcription of `Pnq.E`
    if depth == n or l == 0: return False
    if l == 1: return len({size(c, depth + 1, n, q) for c in t}) == 1
    return all(E(c, depth + 1, n, q, l - 1) for c in t)
def F(t, depth, n, q, l):                    # transcription of `Pnq.F`
    if l == 0: return len(set(lay(t, depth, n, q))) == 1
    if depth == n: return False
    if l == 1:
        L = [lay(c, depth + 1, n, q) for c in t]
        return all(L[c][j] + L[c2][j2] == L[c][j2] + L[c2][j] for c in range(len(t)) for c2 in range(len(t)) for j in range(q) for j2 in range(q))
    return all(F(c, depth + 1, n, q, l - 1) for c in t)
def check(A, p, n, q):
    M = p ** n * q; t = tree(A, p, n, q); bad = 0; seen = []
    for l in range(1, n + 1):
        a, b = E(t, 0, n, q, l), divides(p ** l, A, M); bad += a != b; seen.append(b)
    for l in range(0, n + 1):
        a, b = F(t, 0, n, q, l), divides(p ** l * q, A, M); bad += a != b; seen.append(b)
    return bad, tuple(seen)
if __name__ == "__main__":
    random.seed(9)
    tot_sets = tot_bad = 0
    for p, n, q, mode in [(2, 1, 3, "all"), (3, 1, 2, "all"), (2, 2, 3, "all"), (3, 2, 2, "all"), (2, 2, 5, "all"), (5, 1, 2, "all"), (2, 3, 3, "sample"), (3, 3, 2, "sample"), (2, 3, 5, "sample"), (2, 4, 3, "sample"), (5, 2, 2, "sample"), (3, 2, 5, "sample"), (2, 5, 3, "sample")]:
        M = p ** n * q; pats = set(); nb = ns = 0
        if mode == "all":
            sets = ([0] + [i + 1 for i in range(M - 1) if m >> i & 1] for m in range(2 ** (M - 1)))
        else:
            L = [sorted(random.sample(range(M), random.randint(1, M - 1))) for _ in range(3000)]
            divs = [d for d in range(2, M + 1) if M % d == 0]
            for _ in range(4000):                                  # unions of cosets of one or two subgroups: rich patterns
                S = set()
                for d in random.sample(divs, random.randint(1, 2)):
                    H = range(0, M, M // d)
                    for r in random.sample(range(M // d), random.randint(1, max(1, M // d // 2))): S |= {(h + r) % M for h in H}
                L.append(sorted(S))
            sets = iter(L)
        for A in sets:
            b, pat = check(A, p, n, q); nb += b; ns += 1; pats.add(pat)
        tot_sets += ns; tot_bad += nb
        print(f"p = {p}, n = {n}, q = {q} (M = {M:3d}): {ns:7d} sets ({mode}), {len(pats):4d} distinct patterns (E, F) among them, mismatches between the Lean definitions and exact division: {nb}", flush=True)
    print(f"total: {tot_sets} sets, {tot_bad} mismatches")
