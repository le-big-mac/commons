"""Exact bad shares of h copies of 0 with a decoration, through the test program (so every lemma is also tested on
these multisets), to compare with K sqrt(2/(pi m)).

usage: family.py N 'b:a,...' H1 H2 ...
"""
import sys, math
sys.path.insert(0, '/home/agent3/lean/lift-check/even/root/one')
import test_lemmas as T

n = int(sys.argv[1]); mod = T.Mod(n)
D = [(int(x.split(':')[0]), int(x.split(':')[1])) for x in sys.argv[2].split(',') if x]
for h in map(int, sys.argv[3:]):
    sb = T.check(mod, [(0, h)] + D)
    m = h + sum(a for _, a in D)
    print(f"n = {n}  {h} copies of 0 with {sys.argv[2]}:  m = {m}  bad share = {float(sb):.8f}  times sqrt(pi m/2) = {float(sb) * math.sqrt(math.pi * m / 2):.5f}"
          f"  times sqrt(m) = {float(sb) * math.sqrt(m):.5f}   (all lemma tests passed)", flush=True)
