# t2_compare.py -- `set_sizes_iff_mul` against the censuses.
# For G = M * s, M = p^n q (p != q primes, n >= 0), s > 1, with a census of the sets on Z_G (up to T_G elements) and of
# the multisets on Z_M (up to T_M elements):
#   L(t) = { D : some set of t elements on Z_G has Phi_d | mask, among ALL divisors d > 1 of G, exactly for d in D }
#   W(t) = { D : some multiset of t elements on Z_M has Phi_d | mask, among the divisors d > 1 of M, exactly for d in D }
# The statement, for a set P of divisors of M (hP) and a size t >= 1:   P\{1} in L(t)  <=>  P\{1} in W(t),
# and it claims this for t < r^j, r an odd prime with r^j | s.  Q = the largest such r^j: the claim covers 1 <= t < Q.
# Reported for each pair: the number of (t, P) in the claimed range (P over all subsets of the divisors > 1 of M),
# how many have both sides true, and every mismatch; then, outside the claim (t >= Q), where the two sides differ.
# Also: "set but no multiset" must never happen at any size (the reduction modulo M of a set is such a multiset).
import json, glob, os, sys, re
from core import divisors


def load(kind):
    best = {}
    for fn in glob.glob('census/%s_*_T*.json' % kind):
        m = re.fullmatch(r'census/%s_(\d+)_T(\d+)((?:_\d+_\d+)?)\.json' % kind, fn)
        if not m:
            continue
        G, T, tag = int(m.group(1)), int(m.group(2)), m.group(3)
        best.setdefault((G, T), []).append(fn)
    out = {}
    for (G, T), fns in best.items():
        parts = [json.load(open(fn)) for fn in fns]
        whole = [p for p in parts if p['lo'] == 0 and p['hi'] == G]
        if whole:
            parts = whole[:1]
        else:
            # the parts must cover [0, G) exactly
            iv = sorted((p['lo'], p['hi']) for p in parts)
            ok = iv[0][0] == 0 and iv[-1][1] == G and all(iv[i][1] == iv[i + 1][0] for i in range(len(iv) - 1))
            if not ok:
                continue
        pres = {}
        for p in parts:
            for t, dct in p['count'].items():
                s = pres.setdefault(int(t), {})
                for key, c in dct.items():
                    D = frozenset(int(x) for x in key.split(',')) if key else frozenset()
                    s[D] = s.get(D, 0) + c
        if G not in out or out[G][0] < T:
            out[G] = (T, pres)
    return out


def factor(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def is_form(M):
    """M = p^n q with p != q primes, n >= 0"""
    f = factor(M)
    if len(f) == 1:
        return list(f.values())[0] == 1          # M = q, n = 0
    if len(f) == 2:
        return 1 in f.values()
    return False


def largest_odd_pp(s):
    f = factor(s)
    return max([r ** e for r, e in f.items() if r != 2], default=1)


def two_part(s):
    f = factor(s)
    return 2 ** f.get(2, 0)
def compare(sets, multi, control):
    """control = False: the pairs (M, s) of the statement (M = p^n q).  control = True: the other M (1, prime powers
    p^k with k >= 2, three primes), which the statement does not cover."""
    tot_claim = tot_true = tot_false = tot_mis = 0
    npairs = 0
    rows = []
    for G in sorted(sets):
        TG, L = sets[G]
        for M in divisors(G):
            s = G // M
            if s == 1 or is_form(M) == control or M not in multi:
                continue
            TM, W = multi[M]
            T = min(TG, TM)
            Q = largest_odd_pp(s)
            Q2 = two_part(s)
            dM = [d for d in divisors(M) if d > 1]
            setM = frozenset(dM)
            nP = 2 ** len(dM)
            claim = true = mis = 0
            mism = []
            beyond = []
            setnomulti = []
            for t in range(1, T + 1):
                Lt = set(D for D in L.get(t, {}) if D <= setM)
                Wt = set(W.get(t, {}))
                for D in Lt - Wt:
                    setnomulti.append((t, sorted(D)))
                if t < Q:
                    claim += nP
                    true += len(Lt & Wt)
                    for D in Lt ^ Wt:
                        mis += 1
                        mism.append((t, sorted(D), 'set only' if D in Lt else 'multiset only'))
                else:
                    for D in Wt - Lt:
                        beyond.append((t, sorted(D)))
            false = claim - true - mis
            npairs += 1
            tot_claim += claim
            tot_true += true
            tot_false += false
            tot_mis += mis
            first_beyond = min([t for t, _ in beyond], default=None)
            # for even s: the same question for the prime 2 (not claimed by the statement): t < 2-part of s
            two = [(t, D) for t, D in beyond if t < Q2]
            rows.append(dict(G=G, M=M, s=s, Q=Q, Q2=Q2, T=T, claimed=claim, true=true, false=false, mismatches=mism,
                             beyond_sizes=max(0, T - Q + 1), nbeyond=len(beyond), beyond=beyond[:200],
                             first_beyond=first_beyond, ntwo=len(two), two=two[:50], set_no_multiset=setnomulti,
                             control=control))
            print("%d %d %d | Q=%d | T=%d | %d | %d | %d | %s | t=%s..%d: %d (t,P) differ%s%s%s" % (
                G, M, s, Q, T, claim, true, false, mism if mism else 0,
                Q, T, len(beyond), (", first at t=%d: %s" % (first_beyond, [b for b in beyond if b[0] == first_beyond][:3])) if beyond else "",
                ("; for the prime 2 (t < %d, not claimed): %d differ %s" % (Q2, len(two), two[:4])) if Q2 > 1 else "",
                ("; SET BUT NO MULTISET: %s" % setnomulti[:5]) if setnomulti else ""))
    print()
    print("%s pairs (M, s): %d; (t, P) with t < Q: %d; both sides true: %d; both false: %d; MISMATCHES: %d" % (
        "CONTROL" if control else "STATEMENT", npairs, tot_claim, tot_true, tot_false, tot_mis))
    withclaim = [r for r in rows if r['Q'] > 1]
    full = [r for r in withclaim if r['T'] >= r['Q'] - 1]
    print("  pairs with a claim (Q > 1): %d; every claimed size t < Q inside the censuses: %d; only the sizes t <= T: %d %s" % (
        len(withclaim), len(full), len(withclaim) - len(full),
        [(r['G'], r['M'], r['s'], 'Q=%d' % r['Q'], 'T=%d' % r['T']) for r in withclaim if r['T'] < r['Q'] - 1]))
    print("  pairs with a set but no multiset at some size (must be 0): %d" % sum(1 for r in rows if r['set_no_multiset']))
    print("  pairs compared at sizes t >= Q: %d; of these with a difference (multiset but no set): %d" % (
        sum(1 for r in rows if r['beyond_sizes'] > 0), sum(1 for r in rows if r['nbeyond'] > 0)))
    ev = [r for r in rows if r['Q2'] > 1 and r['Q2'] > r['Q']]
    print("  pairs with 2-part of s above Q (sizes Q <= t < 2-part compared, not claimed): %d; with a difference there: %d" % (
        len(ev), sum(1 for r in ev if r['ntwo'] > 0)))
    print()
    return rows


if __name__ == '__main__':
    sets = load('set')
    multi = load('multi')
    print("set censuses: ", {G: sets[G][0] for G in sorted(sets)})
    print("multiset censuses: ", {M: multi[M][0] for M in sorted(multi)})
    print()
    print("G M s | Q (largest odd prime power dividing s) | T compared | (t,P) with t < Q | both true | both false | MISMATCHES |"
          " outside the claim: sizes t >= Q compared, (t,P) with a multiset but no set [first few]")
    rows = compare(sets, multi, False)
    print("---- control: M not of the form p^n q (not covered by the statement) ----")
    rows += compare(sets, multi, True)
    json.dump(rows, open('t2_compare.json', 'w'))
