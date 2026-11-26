"""A recount, with exact integer arithmetic, of the trial of the two Lean statements for sets
(balanced_base_zmod, balanced_plus_zmod) on every subset of Z_{p^n q}.

Written by the reader of the paragraph, from the Lean statements themselves (Pnq/BalancedGroup.lean), not
from the other trial's code.  Differences from that trial:
  * Phi_d | A(X) is decided exactly: the remainder of A(X) modulo Phi_d(X), in integers, is zero;
  * the hypotheses of balanced_plus_zmod are transliterated quantifier by quantifier from the Lean text;
  * the control is broken down by which clause of the note's rule holds.

usage: python -I recount_exact.py p q n
"""
import sys
import numpy as np


def poly_mul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return r


def poly_divexact(a, b):
    a = a[:]
    out = [0] * (len(a) - len(b) + 1)
    for i in range(len(out) - 1, -1, -1):
        c = a[i + len(b) - 1] // b[-1]
        out[i] = c
        for j, y in enumerate(b):
            a[i + j] -= c * y
    assert all(v == 0 for v in a), "division not exact"
    return out


_cyc = {}


def cyclo(d):
    """coefficients of Phi_d, lowest degree first"""
    if d not in _cyc:
        num = [-1] + [0] * (d - 1) + [1]
        den = [1]
        for k in range(1, d):
            if d % k == 0:
                den = poly_mul(den, cyclo(k))
        _cyc[d] = poly_divexact(num, den)
    return _cyc[d]


def rem_rows(N, d):
    """row k = coefficients of X^k mod Phi_d, k = 0..N-1"""
    phi = cyclo(d)
    deg = len(phi) - 1
    rows = np.zeros((N, deg), dtype=np.int64)
    r = [0] * deg
    r[0] = 1
    for k in range(N):
        rows[k] = r
        top = r[-1]
        r = [0] + r[:-1]
        if top:
            for j in range(deg):
                r[j] -= top * phi[j]      # Phi_d is monic
    return rows


def lean_plus_hyps(p, n, E, F, a0):
    """The hypotheses hk, h2, h34 of Pnq.balanced_plus_zmod, as written in Lean.
    E, F: sets of levels in 1..n (ZeroAt A (p^l), ZeroAt A (p^l * q)).  a0 as in hlow, ha1, han, hna."""
    beyond = {l for l in range(1, n + 1) if l in F and l not in E and a0 < l}      # levelsBeyond A a0
    hk = len(beyond) > 0
    h2 = all(l not in E for l in range(1, a0))                                     # forall l, 1 <= l -> l < a0 -> not ZeroAt A (p^l)
    left = a0 not in E                                                             # not ZeroAt A (p^a0)
    right = (p == 2) and all(
        (b in F) for b in range(a0 + 1, n + 1)                                     # forall b, a0 < b -> b <= n ->
        if all(b < g for g in beyond) and b in E)                                  #   (forall g in levelsBeyond, b < g) -> ZeroAt (p^b) -> ZeroAt (p^b q)
    return hk and h2 and (left or right), beyond


def note_clauses(p, n, E, F, a0):
    """The four clauses of the rule as section 3 of the note words them; returns the set of clauses that hold."""
    deeper = sorted(l for l in range(a0 + 1, n + 1) if l in F and l not in E)
    kp = len(deeper)
    hold = set()
    if kp == 0:
        hold.add(1)
    if any(l in E for l in range(1, a0)):
        hold.add(2)
    if a0 in E and p >= 3:
        hold.add(3)
    if kp and a0 in E and p == 2 and any(l in E and l not in F for l in range(a0 + 1, deeper[0])):
        hold.add(4)
    return hold, kp


def main():
    p, q, n = (int(v) for v in sys.argv[1:4])
    N = p ** n * q
    lo_n = N // 2
    hi_n = N - lo_n
    keys = [('E', l) for l in range(1, n + 1)] + [('F', l) for l in range(0, n + 1)]
    ds = {('E', l): p ** l for l in range(1, n + 1)}
    ds.update({('F', l): p ** l * q for l in range(0, n + 1)})
    lo, hi = {}, {}
    for k in keys:
        rows = rem_rows(N, ds[k])
        tl = np.zeros((1 << lo_n, rows.shape[1]), dtype=np.int32)
        m = np.arange(1 << lo_n)
        for b in range(lo_n):
            tl += (((m >> b) & 1)[:, None] * rows[b][None, :]).astype(np.int32)
        th = np.zeros((1 << hi_n, rows.shape[1]), dtype=np.int32)
        m = np.arange(1 << hi_n)
        for b in range(hi_n):
            th += (((m >> b) & 1)[:, None] * rows[lo_n + b][None, :]).astype(np.int32)
        lo[k], hi[k] = tl, th
    pc_lo = np.array([bin(m).count('1') for m in range(1 << lo_n)], dtype=np.int64)
    ncode = 1 << len(keys)
    counts = np.zeros(ncode * (N + 1), dtype=np.int64)
    for h in range(1 << hi_n):
        code = np.zeros(1 << lo_n, dtype=np.int64)
        for i, k in enumerate(keys):
            z = ((lo[k] + hi[k][h][None, :]) == 0).all(axis=1)
            code |= z.astype(np.int64) << i
        size = pc_lo + bin(h).count('1')
        counts += np.bincount(code * (N + 1) + size, minlength=ncode * (N + 1))
    counts = counts.reshape(ncode, N + 1)
    assert counts.sum() == 1 << N

    st = dict(base=0, base_broken=0, plus=0, plus_broken=0, ctrl=0, ctrl_broken=0, fall=0, fall_broken=0,
              rule_patterns=0, rule_broken=0, rule_met=0, plus_patterns=0, plus_met=0)
    ctrl_by = {}
    mismatch = 0
    for code in range(ncode):
        if counts[code].sum() == 0:
            continue
        E = {k[1] for i, k in enumerate(keys) if k[0] == 'E' and (code >> i) & 1}
        Fall = {k[1] for i, k in enumerate(keys) if k[0] == 'F' and (code >> i) & 1}
        if 0 not in Fall:
            continue                                   # Phi_q does not divide A: the other half
        F = Fall - {0}
        sizes = [(s, int(c)) for s, c in enumerate(counts[code]) if c]
        e = len(E)
        miss = [l for l in range(1, n + 1) if l not in F]
        if not miss:
            for s, c in sizes:
                if s == 0:
                    continue                           # the empty set
                st['fall'] += c
                st['fall_broken'] += c * (s < q * p ** e)
            continue
        a0 = miss[0]
        plus, beyond = lean_plus_hyps(p, n, E, F, a0)
        hold, kp = note_clauses(p, n, E, F, a0)
        assert kp == len(beyond)
        x = 0 if hold else 1
        if (x == 1) != plus:
            mismatch += 1
        base_bound = q * p ** (e + kp)
        plus_bound = q * p ** e * (p ** kp + 1)
        rule_bound = q * p ** e * (p ** kp + x)
        st['rule_patterns'] += 1
        least = min(s for s, c in sizes)
        st['rule_broken'] += least < rule_bound
        st['rule_met'] += least == rule_bound
        if plus:
            st['plus_patterns'] += 1
            st['plus_met'] += least == plus_bound
        for s, c in sizes:
            st['base'] += c
            st['base_broken'] += c * (s < base_bound)
            if plus:
                st['plus'] += c
                st['plus_broken'] += c * (s < plus_bound)
            elif kp >= 1:
                st['ctrl'] += c
                st['ctrl_broken'] += c * (s < plus_bound)
                key = tuple(sorted(hold))
                d = ctrl_by.setdefault(key, [0, 0])
                d[0] += c
                d[1] += c * (s < plus_bound)
    print(f"Z_{N} (p={p}, q={q}, n={n}): {1 << N} subsets, zeros decided exactly")
    print(f"   balanced_base_zmod applies to {st['base']} subsets, broken by {st['base_broken']}")
    print(f"   balanced_plus_zmod applies to {st['plus']} subsets, broken by {st['plus_broken']}")
    print(f"   control (k' >= 1, further hypotheses of plus fail): {st['ctrl']} subsets, plus bound broken by {st['ctrl_broken']}")
    for key in sorted(ctrl_by):
        print(f"      of these, clauses {list(key)} of the note's rule hold: {ctrl_by[key][0]} subsets, plus bound broken by {ctrl_by[key][1]}")
    print(f"   patterns with Phi_q | A and a level missing from F that some subset has: {st['rule_patterns']}; "
          f"least size of a set below the rule's value in {st['rule_broken']}, equal to it in {st['rule_met']}; "
          f"patterns where plus applies: {st['plus_patterns']}, bound met in {st['plus_met']}")
    print(f"   Lean hypotheses of plus against 'none of the four clauses holds', on those patterns: {mismatch} disagreements")
    print(f"   F = all levels, set not empty: {st['fall']} subsets, size below q p^e in {st['fall_broken']}")


if __name__ == '__main__':
    main()
