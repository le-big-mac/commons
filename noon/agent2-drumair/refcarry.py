"""A lighter load is allowed wherever a heavier one is.  On the reference drum, where a lighter weight's answer does better than a heavier
weight's, the search is run on from the lighter answer with the heavier allowance (B following the load), and the better one is kept.
usage: python -u refcarry.py"""
import json, os
import numpy as np
import airlib as A
L = A.L; FIVE = [(1, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]; T9 = [L.target(m, n) for m, n in L.NINE]; W = [1.43, 2.0, 2.79, 4.0, 6.0, 12.0]
for kind in ("tuned", "free", "tabla"):
    modes = {"tuned": L.NINE, "free": FIVE, "tabla": [(1, 1), (0, 1)] + FIVE[1:]}[kind]; prev = None
    for M in W:
        f = f"ref-{kind}-{M:g}-1.json"; d = json.load(open(f))
        if prev is not None and prev['exact'] < d['exact'] - 1e-9:
            a = np.array(prev['a'])
            for it in range(40):
                B = A.reference(A.vacuum(a, [(1, 1)])[(1, 1)])[0]; sk = A.AirSkin(40, modes, B, free=(kind != "tuned"))
                if kind == "tabla": sk.T[1] = 0.55
                a, fd = L.slp(sk, a, M); Bn = A.reference(A.vacuum(a, [(1, 1)])[(1, 1)])[0]
                if abs(Bn / B - 1) < 1e-5: break
            e, r = A.load_pieces(a); Wd = A.with_air(e, r, L.NINE, Bn); w = [Wd[q] for q in L.NINE]; note = w[1] / 2; over = max(abs(x / note / t - 1) for x, t in zip(w[2:], T9[2:])); pl = w[0] / note
            ex = dict(tuned=max(abs(x / w[0] / t - 1) for x, t in zip(w[1:], T9[1:])), free=over, tabla=max(over, abs(pl / 1.10 - 1)))[kind]
            print(f"{kind}, {M:g} skins: the search had {100 * d['exact']:.4f}%; from the {prev['weight']:g}-skin answer ({100 * prev['exact']:.4f}%): {100 * ex:.4f}%, using {sk.mass(a):.2f} skins; place {pl:.4f}; B {Bn:.5f}", flush=True)
            if ex < d['exact']: d.update(a=a.tolist(), B=Bn, miss=fd, exact=ex, place=pl, overtones=over, used=sk.mass(a), w11=w[1], carried_from=prev['weight'], vacuum_place=A.vacuum(a, [(0, 1)])[(0, 1)] / note); json.dump(d, open(f, "w"))
        else: print(f"{kind}, {M:g} skins: {100 * d['exact']:.4f}% (no lighter answer does better)")
        prev = d
