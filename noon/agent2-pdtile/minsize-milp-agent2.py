"""A trial, apart from Lean, of the three least-size statements for multisets on Z_{p^n q}
(agent3's `MinGroup.lean`: minsize_unbalanced_zmod, minsize_balanced_all_zmod, minsize_balanced_zmod).

For every pattern (which of the cyclotomic polynomials Phi_d, d > 1 a divisor of p^n q, divide the mask polynomial
sum_a w(a) X^a), the least number of elements of a multiset with exactly that pattern is found here by integer
programming, a method that owes nothing to the trees of the Lean proof or to agent3's two solvers, and is set beside
the value of the rule as I transcribe it from `Rule.lean` (minU, gOf, xOf, minB).  "Exactly" needs "does not divide",
which is not a linear condition: for each Phi_d that must not divide, one coordinate of the remainder is made at
least 1 or at most -1, chosen by the solver through 0/1 variables.

A disagreement would mean that my reading of the statements is wrong, or the statements are.  Agreement says
nothing of the proofs.            Noon (agent2), 26 November 2026.
usage: python -I minsize-milp-agent2.py p q n [p q n ...]        (numpy, scipy 1.9 or later)
       python -I minsize-milp-agent2.py again SECONDS p q n "1,2" "3" 0|1 [...]     one pattern (E, F, whether Phi_q divides) given longer,
                                                                                     as two questions: is there one smaller than the rule's value? is there one of that size?"""
import sys, itertools, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


def polymul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def polydiv(a, b):                       # exact division of integer polynomials (lowest power first); b monic
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for i in range(len(q) - 1, -1, -1):
        q[i] = a[i + len(b) - 1]
        for j, y in enumerate(b):
            a[i + j] -= q[i] * y
    assert not any(a), 'not an exact division'
    return q


def cyclotomic(d, memo={}):
    if d not in memo:
        num = [-1] + [0] * (d - 1) + [1]
        for e in range(1, d):
            if d % e == 0:
                num = polydiv(num, cyclotomic(e))
        memo[d] = num
    return memo[d]


def remainders(M, d):
    """row a: the coefficients of X^a mod Phi_d, for a = 0..M-1"""
    phi = cyclotomic(d); deg = len(phi) - 1; rows = []; cur = [1] + [0] * (deg - 1) if deg > 0 else []
    for a in range(M):
        rows.append(cur[:])
        nxt = [0] + cur                     # multiply by X
        top = nxt[deg]; nxt = nxt[:deg]
        for k in range(deg):
            nxt[k] -= top * phi[k]          # X^deg = -(lower part of Phi_d), Phi_d being monic
        cur = nxt
    return np.array(rows, dtype=float).T     # deg rows, M columns


# ---- the rule, transcribed from Rule.lean
def gOf(Es, Fs, a0): return {l for l in Fs - Es if a0 < l}
def xOf(p, Es, Fs, a0):
    g = gOf(Es, Fs, a0)
    if (not g) or any(l < a0 for l in Es) or (a0 in Es and 3 <= p) or (a0 in Es and p == 2 and any(a0 < b and all(b < x for x in g) for b in Es - Fs)):
        return 0
    return 1
def minU(p, q, Es, Fs): return p ** len(Es) if Fs <= Es else p ** len(Es) * (p ** len(Fs - Es) + q)
def minB(p, q, Es, Fs, a0): return q * p ** len(Es) * (p ** len(gOf(Es, Fs, a0)) + xOf(p, Es, Fs, a0))

# ---- the rule with one clause of xOf struck out, to see whether these groups can tell the difference (the controls)
def xWithout(clause, p, Es, Fs, a0):
    g = gOf(Es, Fs, a0)
    c = [not g, any(l < a0 for l in Es), a0 in Es and 3 <= p, a0 in Es and p == 2 and any(a0 < b and all(b < x for x in g) for b in Es - Fs)]
    return 0 if any(v for i, v in enumerate(c) if i + 1 != clause) else 1


def least(p, q, n, Es, Fs, phiq, cap, limit=120, floor=1):
    """the least size of a multiset on Z_{p^n q}, with exactly this pattern and between `floor` and `cap` elements; None if there is none"""
    M = p ** n * q
    must = [p ** l for l in Es] + [p ** l * q for l in Fs] + ([q] if phiq else [])
    mustnot = [p ** l for l in range(1, n + 1) if l not in Es] + [p ** l * q for l in range(1, n + 1) if l not in Fs] + ([] if phiq else [q])
    R = {d: remainders(M, d) for d in must + mustnot}
    nb = sum(2 * R[d].shape[0] for d in mustnot); N = M + nb
    A, lo, hi = [], [], []
    def row(wpart, extra=()):
        r = np.zeros(N); r[:M] = wpart
        for i, v in extra: r[i] = v
        return r
    for d in must:
        for k in range(R[d].shape[0]): A.append(row(R[d][k])); lo.append(0); hi.append(0)
    at = M
    for d in mustnot:
        deg = R[d].shape[0]; B = float(np.abs(R[d]).max()) * cap + 1
        for k in range(deg):                 # zplus_k = 1 forces coordinate k >= 1; zminus_k = 1 forces it <= -1
            A.append(row(R[d][k], [(at + 2 * k, -B)])); lo.append(1 - B); hi.append(np.inf)
            A.append(row(R[d][k], [(at + 2 * k + 1, B)])); lo.append(-np.inf); hi.append(B - 1)
        A.append(row(np.zeros(M), [(at + j, 1) for j in range(2 * deg)])); lo.append(1); hi.append(np.inf)
        at += 2 * deg
    A.append(row(np.ones(M))); lo.append(floor); hi.append(cap)
    c = np.zeros(N); c[:M] = 1
    ub = np.concatenate([np.full(M, cap), np.ones(nb)])
    res = milp(c, constraints=LinearConstraint(np.array(A), np.array(lo), np.array(hi)), integrality=np.ones(N), bounds=Bounds(np.zeros(N), ub), options={'time_limit': limit})
    if res.status == 2: return None, None
    if res.status != 0: return 'not decided in %d s' % limit, None
    w = np.rint(res.x[:M]).astype(int)
    return int(w.sum()), w


def pattern_of(p, q, n, w):
    """which Phi_d divide, worked out again from the answer itself, in whole numbers"""
    M = p ** n * q; div = lambda d: not np.any(np.rint(remainders(M, d) @ w))
    return ({l for l in range(1, n + 1) if div(p ** l)}, {l for l in range(1, n + 1) if div(p ** l * q)}, div(q))


def again(argv):
    limit = int(argv[0]); rest = argv[1:]
    for i in range(0, len(rest), 6):
        p, q, n = (int(v) for v in rest[i:i + 3]); Es = {int(v) for v in rest[i + 3].split(',') if v}; Fs = {int(v) for v in rest[i + 4].split(',') if v}; phiq = rest[i + 5] == '1'
        levels = set(range(1, n + 1))
        want = minU(p, q, Es, Fs) if not phiq else q * p ** len(Es) if len(Fs) == n else minB(p, q, Es, Fs, min(levels - Fs))
        t0 = time.time(); below, _ = least(p, q, n, Es, Fs, phiq, cap=want - 1, limit=limit); t1 = time.time()
        at, w = least(p, q, n, Es, Fs, phiq, cap=want, limit=limit, floor=want); t2 = time.time()
        fits = w is not None and pattern_of(p, q, n, w) == (Es, Fs, phiq)
        print(f"Z_{p ** n * q} (p={p}, q={q}, n={n}), E = {sorted(Es)}, F = {sorted(Fs)}, Phi_q {'divides' if phiq else 'does not divide'}: the rule gives {want}. "
              f"A multiset with at most {want - 1} elements: {'none' if below is None else below} [{t1 - t0:.0f} s]. One with exactly {want}: "
              f"{'found, and it has exactly the pattern' if fits else at} [{t2 - t1:.0f} s]", flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'again': again(sys.argv[2:]); sys.exit(0)
    args = [int(v) for v in sys.argv[1:]]
    for i in range(0, len(args), 3):
        p, q, n = args[i:i + 3]; M = p ** n * q; levels = list(range(1, n + 1)); t0 = time.time()
        subsets = [set(c) for r in range(n + 1) for c in itertools.combinations(levels, r)]
        tally = dict(U=[0, 0], A=[0, 0], B=[0, 0]); bad = []; x1 = 0; checked = 0; tell = [0, 0, 0, 0]
        for Es in subsets:
            for Fs in subsets:
                for phiq in (False, True):
                    if not phiq: kind, want = 'U', minU(p, q, Es, Fs)
                    elif len(Fs) == n: kind, want = 'A', q * p ** len(Es)
                    else:
                        a0 = min(set(levels) - Fs); kind, want = 'B', minB(p, q, Es, Fs, a0); x1 += xOf(p, Es, Fs, a0)
                    got, w = least(p, q, n, Es, Fs, phiq, cap=2 * want + 4)
                    tally[kind][0] += 1; ok = got == want
                    if ok and w is not None:
                        ok = pattern_of(p, q, n, w) == (Es, Fs, phiq); checked += 1
                    tally[kind][1] += ok
                    if kind == 'B' and isinstance(got, int):
                        for cl in (1, 2, 3, 4): tell[cl - 1] += got != q * p ** len(Es) * (p ** len(gOf(Es, Fs, a0)) + xWithout(cl, p, Es, Fs, a0))
                    if not ok: bad.append((sorted(Es), sorted(Fs), phiq, want, got))
        print(f"Z_{M} (p={p}, q={q}, n={n}): {sum(v[0] for v in tally.values())} patterns; the least size by integer programming is the rule's value, and the solver's own multiset has exactly the pattern, in: "
              f"Phi_q not dividing {tally['U'][1]} of {tally['U'][0]}; Phi_q and every Phi_(p^l q) dividing {tally['A'][1]} of {tally['A'][0]}; Phi_q dividing and some Phi_(p^l q) not {tally['B'][1]} of {tally['B'][0]}"
              f" (the summand x is 1 in {x1} of those)   [{time.time() - t0:.0f} s]", flush=True)
        print(f"   controls: with clause 1, 2, 3 or 4 of the rule for x struck out, the rule would be wrong on {tell[0]}, {tell[1]}, {tell[2]} and {tell[3]} of these patterns", flush=True)
        for b in bad[:12]: print('   ' + ('NOT DECIDED' if isinstance(b[4], str) else 'DIFFERS') + ': E =', b[0], 'F =', b[1], 'Phi_q divides:', b[2], '; the rule gives', b[3], '; found', b[4], flush=True)
