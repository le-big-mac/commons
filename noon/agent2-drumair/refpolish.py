"""Makes each reference-drum answer agree with its own air: the search is run on from the answer with the B that the answer itself
implies, until B stops changing (to 1 part in 100,000).   usage: python -u refpolish.py ref-KIND-WEIGHT-VOLUME.json ..."""
import sys, json
import numpy as np
import airlib as A
L = A.L; FIVE = [(1, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]; T9 = [L.target(m, n) for m, n in L.NINE]
for f in sys.argv[1:]:
    d = json.load(open(f)); kind, M, vol = d['kind'], d['weight'], d['volume']; modes = {"tuned": L.NINE, "free": FIVE, "tabla": [(1, 1), (0, 1)] + FIVE[1:]}[kind]; a = np.array(d['a']); first = d.get('first_exact', d['exact'])
    for it in range(40):
        B = A.reference(A.vacuum(a, [(1, 1)])[(1, 1)], vol)[0]; sk = A.AirSkin(40, modes, B, free=(kind != "tuned"))
        if kind == "tabla": sk.T[1] = 0.55
        a, fd = L.slp(sk, a, M); Bn = A.reference(A.vacuum(a, [(1, 1)])[(1, 1)], vol)[0]
        if abs(Bn / B - 1) < 1e-5: break
    e, r = A.load_pieces(a); W = A.with_air(e, r, L.NINE, Bn); w = [W[q] for q in L.NINE]; note = w[1] / 2; over = max(abs(x / note / t - 1) for x, t in zip(w[2:], T9[2:])); pl = w[0] / note
    ex = dict(tuned=max(abs(x / w[0] / t - 1) for x, t in zip(w[1:], T9[1:])), free=over, tabla=max(over, abs(pl / 1.10 - 1)))[kind]
    d.update(a=a.tolist(), B=Bn, miss=fd, exact=ex, place=pl, overtones=over, used=sk.mass(a), w11=w[1], first_exact=first, polish_rounds=it + 1, vacuum_place=A.vacuum(a, [(0, 1)])[(0, 1)] / note); json.dump(d, open(f, "w"))
    print(f"{kind}, {M:g} skins, volume x{vol:g}: B = {Bn:.5f} after {it + 1} rounds; {100 * ex:.4f}% exact (it was {100 * first:.4f}% before this pass); the lowest mode's place {pl:.4f} ({d['vacuum_place']:.4f} without the air); overtones within {100 * over:.3f}%; used {sk.mass(a):.2f}", flush=True)
