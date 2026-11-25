"""Is the corrected shuffle uniform?  Every sequence of tosses for orders 1 to 5, with its probability 2^-(number of tosses), summed per tiling.
usage: python uniform.py > uniform.out"""
import sys, os, itertools
from fractions import Fraction
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import aztec as A
def rec(x, order, target, tosses, prob, counts):
    if order == target: prob[x.tobytes()] += Fraction(1, 2 ** tosses); counts.append(tosses); return
    y = A.shuffle(x) if order else np.zeros((2, 2), bool); w = A.holes(y); k = int(w.sum())
    for toss in itertools.product((False, True), repeat=k):
        z = y.copy(); A.fill(z, w, np.array(toss, bool)); rec(z, order + 1, target, tosses + k, prob, counts)
for n in range(1, 6):
    prob = defaultdict(Fraction); counts = []; rec(None, 0, n, 0, prob, counts)
    vals = set(prob.values())
    print(f"order {n}: {len(counts)} sequences, {len(prob)} tilings; total probability {sum(prob.values())}; each tiling's probability: {sorted(vals)[0]}" + (" for every one" if len(vals) == 1 else f" to {sorted(vals)[-1]}")
          + f"; 1/2^(n(n+1)/2) = {Fraction(1, 2 ** (n * (n + 1) // 2))}; tosses in a sequence: from {min(counts)} to {max(counts)}")
