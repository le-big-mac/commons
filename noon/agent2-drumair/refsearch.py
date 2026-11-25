"""Ring loads on the reference drum itself: the air's strength follows from the load (B = 0.2208 times the square of its (1,1) frequency,
divided by VOLUME as a multiple of the reference's), so the search is repeated with the B of its own answer until the two agree.
40 rings.   usage: python -u refsearch.py tuned|free|tabla WEIGHT VOLUME OUT.json
tuned: all nine modes, the lowest as the note.  free: the seven overtones against half the second mode.
tabla: as the two measured tablas do: the lowest mode aimed at 1.10 of the note (half the second mode) and the seven overtones at whole multiples."""
import sys, json, time
import numpy as np
import airlib as A
L = A.L; kind, M, vol = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); FIVE = [(1, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]
modes = {"tuned": L.NINE, "free": FIVE, "tabla": [(1, 1), (0, 1)] + FIVE[1:]}[kind]; rng = np.random.default_rng(int(100 * M) + int(10 * vol) + len(kind)); T9 = [L.target(m, n) for m, n in L.NINE]
def skin(B):
    sk = A.AirSkin(40, modes, B, free=(kind != "tuned"))
    if kind == "tabla": sk.T[1] = 0.55
    return sk
def exact(a, B):
    e, r = A.load_pieces(a); W = A.with_air(e, r, L.NINE, B); w = [W[q] for q in L.NINE]; note = w[1] / 2; over = max(abs(x / note / t - 1) for x, t in zip(w[2:], T9[2:])); pl = w[0] / note
    return dict(tuned=max(abs(x / w[0] / t - 1) for x, t in zip(w[1:], T9[1:])), free=over, tabla=max(over, abs(pl / 1.10 - 1)))[kind], pl, w[1], over
nine = np.array(json.load(open(f"../drum/rings2-free-{M:g}.json"))['rings']['40']['a']); fr = np.array(json.load(open(f"../drumfree/s-five-{M:g}.json"))['rings']['40']['a'])
B = A.reference(A.vacuum(nine if kind == "tuned" else fr, [(1, 1)])[(1, 1)], vol)[0]; a = None; hist = []; t0 = time.time()
for it in range(6):
    sk = skin(B); starts = [nine, fr, L.disc(sk, M / 0.16, 0.4), L.disc(sk, M / 0.25, 0.5), L.disc(sk, M / 0.09, 0.3)] + ([a] if a is not None else []) + [(a if a is not None else nine) * np.exp(0.3 * rng.standard_normal(40)) for _ in range(3)] + [rng.uniform(0, 20, 40) * (sk.E[:-1] < rng.uniform(0.3, 0.9)) for _ in range(4 if it == 0 else 1)]
    ends = [L.slp(sk, a0, M) for a0 in starts]; a, f = min(ends, key=lambda z: z[1]); ex, pl, w11, over = exact(a, B); Bn = A.reference(w11, vol)[0]; hist.append(dict(B=B, miss=f, exact=ex, place=pl, Bnext=Bn, agree=sum(e[1] < f + 2e-5 for e in ends), n=len(ends)))
    print(f"{kind}, {M:g} skins, volume x{vol:g}, round {it + 1}: B = {B:.4f}: least {100 * f:.4f}% ({100 * ex:.4f}% exact); the lowest mode's place {pl:.4f}; overtones within {100 * over:.3f}%; the answer's own B is {Bn:.4f}; {hist[-1]['agree']} of {len(ends)} within 0.002 points; {time.time() - t0:.0f} s", flush=True)
    if abs(Bn / B - 1) < 2e-3: break
    B = Bn
json.dump(dict(kind=kind, weight=M, volume=vol, B=B, miss=f, exact=ex, place=pl, overtones=over, used=sk.mass(a), a=a.tolist(), rounds=hist), open(sys.argv[4], "w"))
