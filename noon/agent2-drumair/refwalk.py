"""The weight walked down on the reference drum: each weight's search is started from the next heavier weight's answer, scaled to fit.
Where that ends lower than the answer on file, the file is replaced.   usage: python -u refwalk.py"""
import json
import numpy as np
import airlib as A
L = A.L; FIVE = [(1, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]; T9 = [L.target(m, n) for m, n in L.NINE]; W = [12.0, 6.0, 4.0, 2.79, 2.0, 1.43]
for kind in ("tuned", "free", "tabla"):
    modes = {"tuned": L.NINE, "free": FIVE, "tabla": [(1, 1), (0, 1)] + FIVE[1:]}[kind]; sk = A.RefSkin(40, modes, 1.0, free=(kind != "tuned"))
    if kind == "tabla": sk.T[1] = 0.55
    prev = np.array(json.load(open(f"ref-{kind}-12-1.json"))['a'])
    for M in W[1:]:
        f = f"ref-{kind}-{M:g}-1.json"; d = json.load(open(f)); a, fd = L.slp(sk, prev * min(1.0, M / sk.mass(prev)), M)
        if fd < d['miss'] - 1e-7:
            e, r = A.load_pieces(a); vac = A.vacuum(a, L.NINE); B = A.reference(vac[(1, 1)])[0]; Wd = A.with_air(e, r, L.NINE, B, vac=dict(vac)); w = [Wd[q] for q in L.NINE]; note = w[1] / 2; over = max(abs(x / note / t - 1) for x, t in zip(w[2:], T9[2:])); pl = w[0] / note
            ex = dict(tuned=max(abs(x / w[0] / t - 1) for x, t in zip(w[1:], T9[1:])), free=over, tabla=max(over, abs(pl / 1.10 - 1)))[kind]
            print(f"{kind}, {M:g} skins: the walk down ends at {100 * fd:.4f}% ({100 * ex:.4f}% exact), lower than the search's {100 * d['miss']:.4f}% by {100 * (d['miss'] - fd):.4f} points; kept", flush=True)
            d.update(a=a.tolist(), miss=fd, exact=ex, place=pl, overtones=over, B=B, used=sk.mass(a), w11=w[1], vacuum_place=vac[(0, 1)] / note, start="the walk down", ends=d['ends'] + [fd]); json.dump(d, open(f, "w"))
        else: print(f"{kind}, {M:g} skins: the walk down ends at {100 * fd:.4f}%; the search had {100 * d['miss']:.4f}%", flush=True)
        prev = np.array(json.load(open(f))['a'])
