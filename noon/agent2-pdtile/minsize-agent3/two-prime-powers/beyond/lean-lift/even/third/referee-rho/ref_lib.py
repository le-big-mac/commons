# Referee's own code for Lemma rho, written from the statement in lemma-rho.md only.
# rho_2(B): share of signings of the multiset B on Z_(2^k) for which no level 0..k is bad.
import itertools
from fractions import Fraction
import numpy as np


def p(r):
    return Fraction(1, 3) + Fraction(2, 3) * Fraction(-1, 2) ** r


def bad_levels(B, k, eps):
    """Literal reading of the statement for one signing.
    B: sequence of residues modulo 2^k, eps: sequence of +1/-1. Returns the set of bad levels."""
    bad = set()
    if sum(eps) % 3 == 0:
        bad.add(0)
    for j in range(1, k + 1):
        halves = {}
        for b, e in zip(B, eps):
            c = b % (1 << (j - 1))          # the class at depth j-1
            h = (b % (1 << j)) // (1 << (j - 1))  # which of its two halves
            halves.setdefault(c, [0, 0])[h] += e
        if all((s[0] - s[1]) % 3 == 0 for s in halves.values()):
            bad.add(j)
    return bad


def rho_slow(B, k):
    m = len(B)
    good = 0
    for eps in itertools.product((1, -1), repeat=m):
        if not bad_levels(B, k, eps):
            good += 1
    return Fraction(good, 2 ** m)


class Fast:
    """All 2^m signings at once (bit i of S set = sign +1 on element i)."""

    def __init__(self, m):
        self.m = m
        self.N = 1 << m
        self.S = np.arange(self.N, dtype=np.int64)
        pop = np.zeros(self.N, dtype=np.int64)
        for i in range(m):
            pop += (self.S >> i) & 1
        self.pop = pop
        self.cache = {}

    def sig(self, h):
        v = self.cache.get(h)
        if v is None:
            v = ((2 * self.pop[self.S & h] - int(self.pop[h])) % 3).astype(np.int8)
            if len(self.cache) * self.N < 64_000_000:
                self.cache[h] = v
        return v

    def good_vector(self, B, k):
        m = self.m
        assert len(B) == m
        ok = self.sig((1 << m) - 1) != 0
        for j in range(1, k + 1):
            halves = {}
            lo = (1 << (j - 1)) - 1
            for i, b in enumerate(B):
                halves.setdefault(b & lo, [0, 0])[(b >> (j - 1)) & 1] |= 1 << i
            allbal = None
            for h0, h1 in halves.values():
                bal = self.sig(h0) == self.sig(h1)
                allbal = bal if allbal is None else (allbal & bal)
            ok = ok & ~allbal
        return ok

    def count_good(self, B, k):
        return int(self.good_vector(B, k).sum())


_fast = {}


def rho(B, k):
    m = len(B)
    if m == 0:
        return Fraction(0)
    f = _fast.get(m)
    if f is None:
        f = _fast[m] = Fast(m)
    return Fraction(f.count_good(B, k), 1 << m)
