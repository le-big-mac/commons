"""A slow, plain search for tiny boards, written apart from lag.c, to test it against.   usage: python -I slow.py n k d Q mode
Prints yes or no: can the codebreaker always determine the code (K) / always have sent it (W) with Q guesses at lag d?"""
import sys, itertools, functools
n, k, d, Q, mode = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
codes = list(itertools.product(range(k), repeat=n))
def answer(g, s):
    b = sum(x == y for x, y in zip(g, s)); return b, sum(min(g.count(c), s.count(c)) for c in range(k)) - b
A = {(g, s): answer(g, s) for g in codes for s in codes}
@functools.lru_cache(maxsize=None)
def can(known, sent):
    """known: answers that have arrived, as a tuple; sent: all guesses so far. True if the codebreaker can still be sure."""
    t = len(sent); arrived = len(known)
    live = [s for s in codes if all(A[sent[i], s] == known[i] for i in range(arrived))]
    if t == Q:                                             # nothing more to send: the rest of the answers come in
        if mode == "K": return len({tuple(A[g, s] for g in sent) for s in live}) == len(live)
        return all(s in sent for s in live)
    for g in codes:
        sent2 = sent + (g,)
        if len(sent2) - arrived <= d:                      # no answer arrives yet
            if can(known, sent2): return True
            continue
        old = sent2[arrived]; good = True
        for a in {A[old, s] for s in live}:
            if not can(known + (a,), sent2): good = False; break
        if good: return True
    return False
print("yes" if can((), ()) else "no")
