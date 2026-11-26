#!/usr/bin/env python
"""Exact check of hand-built examples used in the sealed hand derivation (no search: each example is
written down by hand; this only reports which Phi_d, d | M, divide its mask polynomial).

usage: python -I check_hand_example.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_example_v import divisors_pattern  # noqa: E402


def crt(u, w, pn, q):
    M = pn * q
    for x in range(M):
        if x % pn == u % pn and x % q == w % q:
            return x
    raise ValueError


def show(name, pts, p, n, q):
    pn = p ** n
    M = pn * q
    A = [crt(u, w, pn, q) for (u, w) in pts]
    Z = divisors_pattern(A, M)
    E = [a for a in range(1, n + 1) if p ** a in Z]
    F = [a for a in range(0, n + 1) if p ** a * q in Z]
    kind = "set" if len(set(A)) == len(A) else "multiset"
    print("%s: M=%d, %s, |A|=%d, A=%s, divisors=%s, E=%s, F=%s" % (name, M, kind, len(A), sorted(A), Z, E, F))


if __name__ == "__main__":
    # (u, w) with u in Z_{p^n}, w in Z_q
    base12 = [(0, 0), (0, 0), (0, 1), (0, 2), (2, 0), (1, 1), (1, 2), (3, 1), (3, 2)]
    show("hand example H1 in Z_12 (p=2,q=3,n=2)", base12, 2, 2, 3)
    lift24 = [(0, 0), (4, 0), (0, 1), (0, 2), (2, 0), (1, 1), (1, 2), (3, 1), (3, 2)]
    show("its lift to a set in Z_24 (p=2,q=3,n=3)", lift24, 2, 3, 3)


def digits(u, p, n):
    return [(u // p ** i) % p for i in range(n)]      # digit index i <-> level i + 1


def general(p, n, q, E, F):
    """The construction of the sealed note for 0 not in F: A1 (levels E u F free, one layer chosen by a
    twist on the levels of E minus F) plus, when F is not inside E, A2 (levels E free, every layer)."""
    D = sorted(set(E) | set(F))
    tw = sorted(set(E) - set(F))
    pts = []
    for u in range(p ** n):
        d = digits(u, p, n)
        if all(d[l - 1] == 0 for l in range(1, n + 1) if l not in D):
            layer = 1 if (tw and all(d[l - 1] != 0 for l in tw)) else 0
            pts.append((u, layer))
    if not set(F) <= set(E):
        for u in range(p ** n):
            d = digits(u, p, n)
            if all(d[l - 1] == 0 for l in range(1, n + 1) if l not in E):
                pts.extend((u, w) for w in range(q))
    return pts


if __name__ == "__main__":
    for (p, n, q, E, F) in [(2, 3, 3, [2], [1, 3]), (2, 3, 3, [], [1, 2, 3]), (3, 2, 2, [], [1, 2]),
                            (2, 4, 3, [2], [1, 3, 4]), (3, 3, 2, [1, 3], [2]), (2, 3, 5, [1, 2], [1, 3]),
                            (3, 2, 2, [1, 2], [1]), (2, 3, 3, [1, 3], [])]:
        k = len(set(F) - set(E))
        e = len(E)
        pred = p ** e * (p ** k + q) if k else p ** e
        show("construction p=%d n=%d q=%d wanted E=%s F=%s formula=%d" % (p, n, q, E, F, pred),
             general(p, n, q, E, F), p, n, q)
