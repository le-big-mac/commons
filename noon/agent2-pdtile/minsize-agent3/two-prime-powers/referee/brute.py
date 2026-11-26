"""Theorem S by exhaustion, on a small group and up to a size bound.

For Z_M and a bound B: ALL multisets with at most B elements are written down (every vector of M nonnegative integers with
sum <= B).  For each up-set D: the multisets divisible by every Phi_d, d in D (cuboid test, exact) are collected in one set;
the sums of corner cosets with at most B elements are generated separately in another set (closure of {0} under adding one
coset).  Theorem S, both directions, restricted to sizes <= B, is: the two sets are equal.

usage: brute.py M B
"""
import sys, time, json
import numpy as np
from lib import upsets, corners, cuboid_rows, divides


def all_multisets(M, B):
    V = np.zeros((1, 0), dtype=np.int8); rem = np.array([B], dtype=np.int64)
    for i in range(M):
        reps = rem + 1
        idx = np.repeat(np.arange(len(V)), reps)
        starts = np.cumsum(reps) - reps
        val = np.arange(len(idx)) - np.repeat(starts, reps)
        V = np.hstack([V[idx], val[:, None].astype(np.int8)])
        rem = rem[idx] - val
    return V


def coset_sums(M, C, B):
    cos = []
    for c in C:
        for x in range(c):
            v = [0] * M
            for y in range(x, M, c): v[y] = 1
            cos.append(tuple(v))
    seen = {tuple([0] * M)}; frontier = list(seen)
    while frontier:
        nxt = []
        for a in frontier:
            sa = sum(a)
            for k in cos:
                if sa + sum(k) > B: continue
                b = tuple(x + y for x, y in zip(a, k))
                if b not in seen: seen.add(b); nxt.append(b)
        frontier = nxt
    return seen


def main():
    M, B = int(sys.argv[1]), int(sys.argv[2]); t0 = time.time()
    V = all_multisets(M, B); Vf = V.astype(np.float32)
    print(f'# Z_{M}: all multisets with at most {B} elements: {len(V)}', flush=True)
    forms = {}
    for D in upsets(M):
        for d in D:
            if d not in forms:
                E = np.zeros((d, M), dtype=np.float32)
                for t, r in enumerate(cuboid_rows(M, d)):
                    for x, c in r.items(): E[t, x] = c
                forms[d] = (np.abs(Vf @ E.T) < 0.5).all(1)           # exact: small integers in float32
    allok = True
    for D in upsets(M):
        mask = np.ones(len(V), dtype=bool)
        for d in D: mask &= forms[d]
        sat = set(map(tuple, V[mask].tolist()))
        # second test of a sample of the satisfying ones by lib.divides
        for a in list(sat)[:200]:
            for d in D: assert divides(M, d, list(a))
        C = corners(M, D); gen = coset_sums(M, C, B)
        same = (sat == gen); allok &= same
        print(json.dumps(dict(M=M, B=B, D=list(D), corners=C, divisible=len(sat), coset_sums=len(gen), equal=same,
                              divisible_not_sums=[list(a) for a in list(sat - gen)[:3]], sums_not_divisible=[list(a) for a in list(gen - sat)[:3]])), flush=True)
    print(f'# Z_{M}, sizes <= {B}: for every one of the {len(upsets(M))} up-sets the multisets divisible by all Phi_d (d in D) are exactly the sums of corner cosets: {allok}; {time.time() - t0:.0f} s', flush=True)


if __name__ == '__main__':
    main()
