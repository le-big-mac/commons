"""Tests of the lemmas of proof.md on explicit multisets, with code that does not use the referee's recursion (dp.c).

Four sources of multisets; in each, EVERY nonempty class (node) of every multiset is analysed as a multiset of its own
(its layer vector, its exact pattern on its own levels) and put through claims.violations:

  brute    every multiset of at most s elements on Z_12, Z_18, Z_24 (and a few more), by plain enumeration of the
           weights and the literal definition of the pattern (equal totals / equal shapes of the children of each class).
  summary  an exhaustive recursion of my own, by explicit summaries: a class is summarised by (layer vector, exact
           pattern); the summary of a parent depends only on the summaries of its p children, so running over all
           p-tuples of child summaries reaches the summary of EVERY multiset up to the size bound.  No counting trick.
           (Cross-checked against 'brute': the two give the same set of root summaries up to the brute-force size.)
  random   random multisets built top-down from splitting rules chosen at random (copies, equal shapes with unequal
           fibre counts, layer-rotated copies, a fibre child of equal total, free), plus sums of cosets and points.
  witness  the least multisets found by the referee's recursion (dpout/roots-*.txt) and by the author's solvers
           (../out/*.jsonl), each analysed by the literal definition; also checks that the stated pattern is the real one.

usage: test_tree.py brute | summary | random | witness | placebo
"""
import sys, itertools, random, glob, json, time
sys.path.insert(0, "/home/agent3/minsize/prove")
from claims import violations, in_sum, rule_value


# ---------- literal analysis of an explicit multiset ----------
def analyse(p, q, n, w):
    """w: weights on Z_M.  Returns a list of (j, vector, E, F) for every NONEMPTY class: j = number of levels below it,
    E, F = its exact pattern on its own levels 1..j (tuples)."""
    P = p ** n
    vec = [None] * (n + 1)
    vec[n] = [[0] * q for _ in range(P)]
    for x, wt in enumerate(w):
        if wt:
            vec[n][x % P][x % q] += wt
    for d in range(n - 1, -1, -1):
        pd = p ** d
        vec[d] = [[sum(vec[d + 1][c + i * pd][l] for i in range(p)) for l in range(q)] for c in range(pd)]
    # masks: bit (j-1) set iff level j of the class is in E (resp. F)
    Em = [None] * (n + 1); Fm = [None] * (n + 1)
    Em[n] = [0] * P; Fm[n] = [0] * P
    out = []
    for d in range(n - 1, -1, -1):
        pd = p ** d
        full = (1 << (n - d - 1)) - 1
        Em[d] = [0] * pd; Fm[d] = [0] * pd
        for c in range(pd):
            kids = [c + i * pd for i in range(p)]
            kv = [vec[d + 1][k] for k in kids]
            tots = [sum(v) for v in kv]
            eqt = len(set(tots)) == 1
            eqs = all(len(set(v[l] - kv[0][l] for l in range(q))) == 1 for v in kv[1:])
            e = full; f = full
            for k, t in zip(kids, tots):
                if t:                       # an empty child has every level
                    e &= Em[d + 1][k]; f &= Fm[d + 1][k]
            Em[d][c] = (e << 1) | (1 if eqt else 0)
            Fm[d][c] = (f << 1) | (1 if eqs else 0)
    for d in range(n + 1):
        j = n - d
        for c in range(p ** d):
            v = vec[d][c]
            if any(v):
                E = tuple(l for l in range(1, j + 1) if Em[d][c] >> (l - 1) & 1)
                F = tuple(l for l in range(1, j + 1) if Fm[d][c] >> (l - 1) & 1)
                out.append((j, tuple(v), E, F))
    return out


class Tally:
    def __init__(self, name): self.name = name; self.nodes = 0; self.msets = 0; self.bad = 0; self.seen = set()
    def feed(self, p, q, nodes):
        self.msets += 1
        for (j, v, E, F) in nodes:
            self.nodes += 1
            key = (p, q, j, E, F, len(set(v)) == 1, sum(v))
            if key in self.seen: continue
            self.seen.add(key)
            bad = violations(p, q, j, E, F, len(set(v)) == 1, sum(v))
            if bad:
                self.bad += 1
                if self.bad <= 10: print('   VIOLATION', self.name, key, bad)
    def report(self):
        nb = len([k for k in self.seen if k[5]]); nu = len(self.seen) - nb
        print(f'{self.name}: {self.msets} multisets, {self.nodes} nonempty classes, {len(self.seen)} distinct (p, q, levels, pattern, '
              f'balanced?, size) cases ({nb} balanced, {nu} unbalanced), {self.bad} violate a claim', flush=True)


# ---------- brute force ----------
def compositions(total, parts):
    if parts == 1:
        yield (total,); return
    for x in range(total + 1):
        for rest in compositions(total - x, parts - 1):
            yield (x,) + rest


def brute(p, q, n, smax, collect_roots=None):
    M = p ** n * q
    t = Tally(f'brute Z_{M} (p={p}, q={q}, n={n}), all multisets of 1..{smax} elements')
    for s in range(1, smax + 1):
        for w in compositions(s, M):
            nodes = analyse(p, q, n, w)
            t.feed(p, q, nodes)
            if collect_roots is not None:
                for (j, v, E, F) in nodes:
                    if j == n: collect_roots.add((v, E, F))
    t.report()
    return t.bad


# ---------- exhaustive recursion by explicit summaries ----------
def summaries(p, q, n, S):
    """stage[j] = set of (vector, Emask, Fmask) of all multisets with at most S elements on Z_{p^j q} (zero vector excluded)"""
    def vecs(total_max):
        for s in range(1, total_max + 1):
            for v in compositions(s, q): yield v
    stage = [set((v, 0, 0) for v in vecs(S))]
    zero = tuple([0] * q)
    for j in range(1, n + 1):
        full = (1 << (j - 1)) - 1
        prev = sorted(stage[-1], key=lambda t: sum(t[0]))
        prev = [(zero, full, full)] + prev          # the empty child: every level
        sizes = [sum(t[0]) for t in prev]
        cur = set()
        # all p-tuples (ordered tuples are needed only up to order: the summary is symmetric in the children)
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
                cur.add((tot, (e << 1) | eqt, (f << 1) | eqs))
                return
            for i in range(start, len(prev)):
                if sizes[i] > left: break
                rec(i, left - sizes[i], chosen + [prev[i]])
        rec(0, S, [])
        stage.append(cur)
    return stage


def run_summary(p, q, n, S, brute_roots=None, brute_smax=0):
    t0 = time.time()
    st = summaries(p, q, n, S)
    t = Tally(f'summary recursion p={p} q={q}, levels 0..{n}, every multiset of at most {S} elements')
    for j in range(n + 1):
        for (v, e, f) in st[j]:
            E = tuple(l for l in range(1, j + 1) if e >> (l - 1) & 1)
            F = tuple(l for l in range(1, j + 1) if f >> (l - 1) & 1)
            t.feed(p, q, [(j, v, E, F)])
    t.msets = sum(len(s) for s in st)
    t.name += f' ({t.msets} summaries, {time.time()-t0:.0f} s)'
    t.report()
    if brute_roots is not None:
        mine = set()
        for (v, e, f) in st[n]:
            if sum(v) <= brute_smax:
                mine.add((v, tuple(l for l in range(1, n + 1) if e >> (l - 1) & 1), tuple(l for l in range(1, n + 1) if f >> (l - 1) & 1)))
        print(f'   cross-check with brute force (sizes <= {brute_smax}): summaries from recursion {len(mine)}, from enumeration '
              f'{len(brute_roots)}, equal sets: {mine == brute_roots}')
        if mine != brute_roots: t.bad += 1
    return t.bad


# ---------- random structured multisets ----------
def rnd_tree(p, q, j, rng, budget):
    """a random multiset on Z_{p^j q} as a list of p^j layer vectors (leaves in class order: index = sum digit_a p^(a-1))"""
    if j == 0:
        mode = rng.random()
        if mode < 0.35: v = [0] * q; v[rng.randrange(q)] = rng.randint(1, 2)
        elif mode < 0.5: v = [rng.randint(0, 1) for _ in range(q)]
        elif mode < 0.6: v = [1] * q
        else: v = [rng.randint(0, 2) for _ in range(q)]
        return [v]
    mode = rng.choice(['copies', 'copies', 'shapes', 'shapes', 'rot', 'rot', 'fibrechild', 'free', 'free', 'one'])
    sub = rnd_tree(p, q, j - 1, rng, budget)
    L = len(sub)
    def fibres(k):
        """k fibres on a class with j-1 levels, spread or concentrated at random"""
        out = [[0] * q for _ in range(L)]
        spread = rng.random() < 0.5
        for _ in range(k):
            i = rng.randrange(L) if spread else 0
            for l in range(q): out[i][l] += 1
        return out
    def add(a, b): return [[x + y for x, y in zip(u, v)] for u, v in zip(a, b)]
    def rot(a, r): return [[u[(l - r) % q] for l in range(q)] for u in a]
    kids = []
    if mode == 'copies':
        kids = [sub] * p
    elif mode == 'shapes':
        kids = [add(sub, fibres(rng.choice([0, 0, 1, 2]))) for _ in range(p)]
    elif mode == 'rot':
        kids = [rot(sub, rng.randrange(q)) for _ in range(p)]
    elif mode == 'fibrechild':
        tot = sum(sum(v) for v in sub)
        kids = [sub] * p
        if tot % q == 0:
            kids = list(kids); kids[rng.randrange(p)] = fibres(tot // q)
            if rng.random() < 0.5: kids[rng.randrange(p)] = rot(sub, 1)
    elif mode == 'free':
        kids = [rnd_tree(p, q, j - 1, rng, budget) if rng.random() < 0.7 else [[0] * q for _ in range(L)] for _ in range(p)]
        if not any(any(v) for k in kids for v in k): kids[0] = sub
    else:
        kids = [[[0] * q for _ in range(L)] for _ in range(p)]; kids[rng.randrange(p)] = sub
    # leaves in class order: child i holds the classes c with c = i mod p; class index within the child = c // p
    leaves = [None] * (L * p)
    for i, k in enumerate(kids):
        for c, v in enumerate(k):
            leaves[i + p * c] = list(v)
    return leaves


def leaves_to_weights(p, q, n, leaves):
    P = p ** n; M = P * q
    w = [0] * M
    for x in range(M):
        w[x] = leaves[x % P][x % q]
    return w


def rnd_cosets(p, q, n, rng):
    M = p ** n * q; w = [0] * M
    divs = [d for d in range(2, M + 1) if M % d == 0]
    for _ in range(rng.randint(1, 4)):
        r = rng.choice(divs); t = rng.randrange(M); m = rng.randint(1, 2)
        for j in range(r): w[(t + j * (M // r)) % M] += m
    for _ in range(rng.randint(0, 2)): w[rng.randrange(M)] += 1
    return w


def run_random():
    rng = random.Random(20261126)
    bad = 0
    for (p, q, n, reps) in [(2, 3, 2, 20000), (3, 2, 2, 20000), (2, 3, 3, 20000), (3, 2, 3, 10000), (2, 5, 3, 10000), (5, 2, 2, 5000),
                            (2, 3, 4, 10000), (3, 2, 4, 3000), (2, 3, 5, 4000), (2, 7, 3, 4000), (3, 5, 3, 2000), (5, 3, 2, 3000),
                            (2, 3, 6, 1500), (3, 7, 2, 2000), (7, 3, 2, 1000), (2, 5, 5, 1000)]:
        t = Tally(f'random trees p={p} q={q} n={n}')
        for _ in range(reps):
            w = leaves_to_weights(p, q, n, rnd_tree(p, q, n, rng, 0))
            t.feed(p, q, analyse(p, q, n, w))
        t.report(); bad += t.bad
        t = Tally(f'random sums of cosets and points p={p} q={q} n={n}')
        for _ in range(reps // 4):
            t.feed(p, q, analyse(p, q, n, rnd_cosets(p, q, n, rng)))
        t.report(); bad += t.bad
    return bad


# ---------- witnesses ----------
def parse_witness(s, M):
    w = [0] * M
    for tok in s.split():
        if '^' in tok:
            a, b = tok.split('^'); w[int(a)] += int(b)
        else: w[int(tok)] += 1
    return w


def run_witness():
    bad = 0
    t = Tally('witnesses of the recursion (dpout/roots-*.txt)')
    mism = 0; eqform = 0; nform = 0
    for fn in sorted(glob.glob('/home/agent3/minsize/prove/dpout/roots-*.txt')):
        lines = open(fn).read().splitlines()
        hdr = dict(x.split('=') for x in lines[0][2:].split())
        p, q, n = int(hdr['p']), int(hdr['q']), int(hdr['n']); M = p ** n * q
        for l in lines[1:]:
            head, _, ws = l.partition(' W')
            if not ws: continue
            tk = head.split()
            E = tuple(int(c) for c in tk[2].split(',')[1:]); F = tuple(int(c) for c in tk[3].split(',')[1:]); m = int(tk[5])
            w = parse_witness(ws, M)
            nodes = analyse(p, q, n, w)
            root = [x for x in nodes if x[0] == n][0]
            balanced = len(set(root[1])) == 1
            Fr = ((0,) if balanced else ()) + root[3]
            if (root[2], Fr) != (E, F) or sum(w) != m: mism += 1
            if balanced:
                nform += 1
                if rule_value(p, q, n, E, [a for a in F if a])[0] == m: eqform += 1
            t.feed(p, q, nodes)
    t.report(); bad += t.bad + mism
    print(f'   stated pattern or size differs from the literal analysis in {mism}; balanced witnesses of exactly the formula\'s size: {eqform} of {nform}')
    t = Tally('witnesses of the author\'s solvers (../out/*.jsonl, *.part)')
    mism = 0
    for fn in sorted(glob.glob('/home/agent3/minsize/out/*.jsonl') + glob.glob('/home/agent3/minsize/out/*.part')):
        for l in open(fn):
            if not l.startswith('{'): continue
            try: r = json.loads(l)
            except Exception: continue
            if not r.get('witness'): continue
            p, q, n = r['p'], r['q'], r['n']; M = p ** n * q
            w = parse_witness(r['witness'], M)
            nodes = analyse(p, q, n, w)
            root = [x for x in nodes if x[0] == n][0]
            balanced = len(set(root[1])) == 1
            Fr = ((0,) if balanced else ()) + root[3]
            if (list(root[2]), list(Fr)) != (r['E'], r['F']): mism += 1
            t.feed(p, q, nodes)
    t.report(); bad += t.bad + mism
    print(f'   stated pattern differs from the literal analysis in {mism}')
    return bad


# ---------- placebos: statements that should FAIL, to see that the harness can fail ----------
def run_placebo():
    """Two false statements, to see that the harness can fail.
    (P1) Lemma 5 without its hypothesis: 'an unbalanced class with F minus E not empty has size in p^u N>=1 + q N>=1, u for the
         full pattern' (false: p=2, q=3, vector (8,2,2), E={1}, F={2}, size 12 = q p^u).
    (P2) the rule with x = 1 always: 'a balanced class with k' >= 1 has size >= q p^e (p^k' + 1)' (false where a clause (2)-(4) holds)."""
    n1 = n2 = c1 = c2 = 0
    onlyQ = True
    for fn in sorted(glob.glob('/home/agent3/minsize/prove/dpout/sizes-*.txt')):
        lines = open(fn).read().splitlines()
        hdr = dict(x.split('=') for x in lines[0][2:].split())
        p, q = int(hdr['p']), int(hdr['q'])
        for l in lines[1:]:
            tk = l.split(); j, bal, P = int(tk[1]), int(tk[2]), int(tk[3])
            E = {a for a in range(1, j + 1) if P >> (2 * (a - 1)) & 1}; F = {a for a in range(1, j + 1) if P >> (2 * (a - 1) + 1) & 1}
            u = len(E | F); e = len(E)
            if not bal:
                if not (F - E): continue
                for s in map(int, tk[4:]):
                    c1 += 1
                    if not in_sum(s, p ** u, q, 1, 1):
                        n1 += 1
                        if s % (q * p ** u): onlyQ = False
            else:
                val, x, k1, a0 = rule_value(p, q, j, E, F)
                if x is None or k1 == 0: continue
                for s in map(int, tk[4:]):
                    c2 += 1
                    if s < q * p ** e * (p ** k1 + 1): n2 += 1
    print(f'placebos on the size tables: P1 fails on {n1} of {c1} unbalanced cases with F minus E not empty '
          f'(every failing size is a multiple of q p^u: {onlyQ}); P2 fails on {n2} of {c2} balanced cases with k\' >= 1')
    return 0 if (n1 > 0 and n2 > 0) else 1


if __name__ == '__main__':
    what = sys.argv[1]
    bad = 0
    if what == 'brute':
        roots = {}
        for (p, q, n, s) in [(2, 3, 2, 9), (3, 2, 2, 7), (2, 3, 3, 6), (2, 5, 2, 5), (2, 3, 1, 14), (3, 2, 1, 14)]:
            roots[p, q, n] = set()
            bad += brute(p, q, n, s, roots[p, q, n])
        # cross-check the summary recursion against the enumeration
        for (p, q, n, s) in [(2, 3, 2, 9), (3, 2, 2, 7), (2, 3, 3, 6), (2, 5, 2, 5)]:
            bad += run_summary(p, q, n, s, roots[p, q, n], s)
    elif what == 'summary':
        for (p, q, n, S) in [(2, 3, 3, 24), (3, 2, 2, 24), (3, 2, 3, 18), (2, 5, 2, 20), (2, 3, 4, 18), (5, 2, 2, 20), (2, 7, 2, 14), (2, 5, 3, 15)]:
            bad += run_summary(p, q, n, S)
    elif what == 'random':
        bad += run_random()
    elif what == 'witness':
        bad += run_witness()
    elif what == 'placebo':
        bad += run_placebo()
    print('TOTAL problems:', bad)
