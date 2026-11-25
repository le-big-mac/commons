"""Referee's ruler for blind.c: a plain brute force, no symmetry, no shortcuts,
written from the definitions (general lag d, general number of guesses T),
for small games.  Compares with blind.c on K(1)<=4 and W(1)<=6.

K: is there a strategy of T guesses (guess t a function of answers 1..t-1-d)
   such that the T answers determine the code?
W: is there a strategy such that every code is itself among its T guesses?

Recursive definition, straight from the rule: a 'state' is the list of guesses
sent so far and the set of codes still possible GIVEN THE ANSWERS THE BREAKER
HAS SEEN.  We handle the lag by carrying the full history of guesses and
splitting the code set only by the answers that have arrived.
usage: small.py P C d T K|W
"""
import sys, itertools
from functools import lru_cache

P, Cc, d, T, mode = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
codes = list(itertools.product(range(Cc), repeat=P))
N = len(codes)


def ans(g, c):
    b = sum(x == y for x, y in zip(g, c))
    s = sum(min(g.count(q), c.count(q)) for q in range(Cc))
    return (b, s - b)


A = [[ans(g, c) for c in codes] for g in codes]


@lru_cache(maxsize=None)
def win(t, S, pending):
    """About to send guess t (1-based).  S = frozenset of codes consistent with
    the answers seen so far (answers to guesses 1..t-1-d).  pending = tuple of
    the guesses already sent whose answers have not arrived (at most d of
    them).  Returns True if the breaker can still win from here."""
    if t > T:
        # all guesses sent; all answers come in.
        if mode == 'K':
            sig = set()
            for c in S:
                k = tuple(A[g][c] for g in pending)
                if k in sig:
                    return False
                sig.add(k)
            return True
        else:
            # every code in S must be among the pending guesses (earlier
            # guesses that equalled the code were removed when their answer
            # (P,0) arrived)
            return all(c in pending for c in S)
    for g in range(N):
        pend = pending + (g,)
        if len(pend) > d:
            # the answer to the oldest pending guess arrives before guess t+1
            g0 = pend[0]
            rest = pend[1:]
            parts = {}
            for c in S:
                parts.setdefault(A[g0][c], []).append(c)
            ok = True
            for a, part in parts.items():
                if mode == 'W' and a == (P, 0):
                    continue  # g0 was the code: sent
                if not win(t + 1, frozenset(part), rest):
                    ok = False
                    break
            if ok:
                return True
        else:
            if win(t + 1, S, pend):
                return True
    return False


print(f"P={P} C={Cc} lag={d} T={T} mode={mode}: {'YES' if win(1, frozenset(range(N)), ()) else 'NO'}")
