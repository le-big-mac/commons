"""A second run of the double description, to test the first: for each up-set D of Z_M the cone is built FROM THE ORTHANT
(not from the cone of a smaller up-set), with the equations of the d in D taken in a random order of d, and with the
equations written as remainders modulo Phi_d (Phi_d from the Moebius product in lib.cyclotomic) instead of cuboid forms.
The extreme rays must again be exactly the corner cosets.     usage: dd_direct.py M seed|desc [maxrays]   (desc: the d in decreasing order instead of a random order)"""
import sys, json, time, random
import numpy as np
from lib import upsets, corners, cyclotomic, divides
from dd import add_equation, TooBig, phi


def remainder_rows(M, d):
    ph = list(cyclotomic(d)); deg = len(ph) - 1
    rows = np.zeros((deg, M), dtype=np.int64); cur = [0] * deg; cur[0] = 1
    for x in range(M):
        rows[:, x] = cur
        top = cur[-1]; cur = [0] + cur[:-1]
        if top:
            for t in range(deg): cur[t] -= top * ph[t]
    return rows


M = int(sys.argv[1]); DESC = (sys.argv[2] == "desc"); random.seed(0 if DESC else int(sys.argv[2])); maxrays = int(sys.argv[3]) if len(sys.argv) > 3 else 30000
ok = bad = skipped = 0; t00 = time.time(); peak_all = 0
for D in upsets(M):
    order = sorted(D, reverse=True) if DESC else random.sample(list(D), len(D))
    R = np.eye(M, dtype=np.int64); stats = dict(peak=M); rank = sum(phi(e) for e in D)
    try:
        for d in order:
            for b in remainder_rows(M, d): R = add_equation(R, b, rank, maxrays, stats)
    except TooBig as e:
        skipped += 1; print(json.dumps(dict(M=M, D=list(D), skipped=str(e)))); continue
    want = {frozenset(range(x, M, c)) for c in corners(M, D) for x in range(c)}
    got = {frozenset(np.nonzero(r)[0].tolist()) for r in R}
    same = got == want and len(R) == len(want) and all(r.max() == 1 for r in R)
    ok += same; bad += (not same); peak_all = max(peak_all, stats['peak'])
    print(json.dumps(dict(M=M, D=list(D), order=order, rays=len(R), rays_are_corner_cosets=bool(same), peak=stats['peak'])), flush=True)
print(f'# Z_{M}, from the orthant, remainder equations, order {"decreasing d" if DESC else "random"}: {ok} up-sets with rays exactly the corner cosets; {bad} not; {skipped} not computed; largest intermediate number of rays {peak_all}; {time.time() - t00:.0f} s')
