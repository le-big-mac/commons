"""Referee's own helpers (written from the words of proof-as-sent.md, sections 1 and 5; nothing imported from the
author's scripts).

Conventions: an element of Z_{p^n} x Z_q is (u, w); u = sum_{a=1..n} u_a p^(a-1); a class of depth d is a residue
class of u mod p^d.  A multiset is an integer array W of shape (p^n, q) (or (K, p^n, q) for K multisets at once).
Level sets are bitmasks: level l <-> bit (l-1).  For the pattern of A the level 0 is kept separately ("balanced").
"""
import numpy as np


def popcount(x):
    return bin(int(x)).count("1")


def set_tables(p, q, umax, B):
    """inS[u][x], inSp[u][x], inQ[u][x] for 0 <= u <= umax, 0 <= x <= B, from the definitions of section 1:
    S_u = {p^u t + q m : t >= 1, m >= 0}, S_u+ = {.. t >= 1, m >= 1}, Q_u = {q p^u t : t >= 1}."""
    inS = np.zeros((umax + 1, B + 1), dtype=bool)
    inSp = np.zeros((umax + 1, B + 1), dtype=bool)
    inQ = np.zeros((umax + 1, B + 1), dtype=bool)
    for u in range(umax + 1):
        P = p ** u
        t = 1
        while P * t <= B:
            m = 0
            while P * t + q * m <= B:
                inS[u, P * t + q * m] = True
                if m >= 1:
                    inSp[u, P * t + q * m] = True
                m += 1
            t += 1
        t = 1
        while q * P * t <= B:
            inQ[u, q * P * t] = True
            t += 1
    return inS, inSp, inQ


def rule(p, q, n, Eset, Fset):
    """The claimed least size for a balanced pattern (E, F), 0 in F; Eset, Fset python sets of levels (F with 0).
    Returns (value, x, a0, kprime) with x None when F is everything (Theorem A)."""
    assert 0 in Fset
    e = len(Eset)
    if all(a in Fset for a in range(0, n + 1)):
        return q * p ** e, None, None, None
    a0 = min(a for a in range(1, n + 1) if a not in Fset)
    Gp = sorted(a for a in range(a0 + 1, n + 1) if a in Fset and a not in Eset)
    kp = len(Gp)
    c1 = (kp == 0)
    c2 = any(a in Eset for a in range(1, a0))
    c3 = (a0 in Eset and p >= 3)
    c4 = False
    if kp >= 1:
        g1 = Gp[0]
        c4 = (a0 in Eset and p == 2 and any((b in Eset and b not in Fset) for b in range(a0 + 1, g1)))
    x = 0 if (c1 or c2 or c3 or c4) else 1
    return q * p ** e * (p ** kp + x), x, a0, kp


def literal_classes(p, q, n, W):
    """W: integer array (K, p^n, q).  Returns per depth d = 0..n:
       G[d]  (K, p^d, q)  vectors of the classes of depth d (class index c = u mod p^d),
       and per depth delta = 0..n-1:
       eqT[delta] (K, p^delta): the p children of the class have equal totals,
       eqS[delta] (K, p^delta): the p children of the class have equal shapes (vectors differ by a multiple of 1).
    """
    K = W.shape[0]
    G = []
    for d in range(n + 1):
        G.append(W.reshape(K, p ** (n - d), p ** d, q).sum(axis=1))
    eqT, eqS = [], []
    for dl in range(n):
        ch = G[dl + 1].reshape(K, p, p ** dl, q)       # child j of class c is class c + j p^dl of depth dl+1
        tot = ch.sum(axis=3)
        eqT.append((tot == tot[:, :1, :]).all(axis=1))
        diff = ch - ch[:, :1, :, :]
        eqS.append((diff == diff[:, :, :, :1]).all(axis=(1, 3)))
    return G, eqT, eqS


def literal_patterns(p, q, n, W):
    """For every class N of every depth d: total, balanced, E(N), F(N) as bitmasks over its own levels 1..n-d,
    straight from the definition: l in E(N) iff every class of depth d+l-1 contained in N has p children of
    equal totals; same with shapes for F(N).  Returns list over d of dict(tot, bal, E, F) with arrays (K, p^d)."""
    K = W.shape[0]
    G, eqT, eqS = literal_classes(p, q, n, W)
    out = []
    for d in range(n + 1):
        tot = G[d].sum(axis=2)
        bal = (G[d] == G[d][:, :, :1]).all(axis=2)
        Eb = np.zeros((K, p ** d), dtype=np.int64)
        Fb = np.zeros((K, p ** d), dtype=np.int64)
        for l in range(1, n - d + 1):
            dep = d + l - 1
            # classes of depth dep inside class c of depth d: indices c' with c' = c mod p^d
            e_all = eqT[dep].reshape(K, p ** (l - 1), p ** d).all(axis=1)
            f_all = eqS[dep].reshape(K, p ** (l - 1), p ** d).all(axis=1)
            Eb |= e_all.astype(np.int64) << (l - 1)
            Fb |= f_all.astype(np.int64) << (l - 1)
        out.append(dict(tot=tot, bal=bal, E=Eb, F=Fb, G=G[d]))
    return out


def bits_to_set(b):
    return {l + 1 for l in range(64) if (int(b) >> l) & 1}
