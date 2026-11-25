"""Ring loads on the reference drum, the air's strength following the load inside the search (airlib.RefSkin).  40 rings.
usage: python -u refsearch2.py tuned|free|tabla WEIGHT VOLUME OUT.json
tuned: all nine modes, the lowest as the note.  free: the seven overtones against half the second mode.
tabla: as the two measured tablas do: the lowest mode aimed at 1.10 of the note and the seven overtones at whole multiples.
Starts: the answers of a first pass (first-pass/, an alternating scheme that was not a true descent) at this and every lighter weight,
the vacuum's answers, three discs, four random loads; then three shakes of the best."""
import sys, json, time, glob, os
import numpy as np
import airlib as A
L = A.L; kind, M, vol = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); FIVE = [(1, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]
modes = {"tuned": L.NINE, "free": FIVE, "tabla": [(1, 1), (0, 1)] + FIVE[1:]}[kind]; rng = np.random.default_rng(int(100 * M) + int(10 * vol) + 5 * len(kind)); T9 = [L.target(m, n) for m, n in L.NINE]
sk = A.RefSkin(40, modes, vol, free=(kind != "tuned"))
if kind == "tabla": sk.T[1] = 0.55
def exact(a):
    e, r = A.load_pieces(a); vac = A.vacuum(a, L.NINE); B = A.reference(vac[(1, 1)], vol)[0]; W = A.with_air(e, r, L.NINE, B, vac=dict(vac)); w = [W[q] for q in L.NINE]; note = w[1] / 2; over = max(abs(x / note / t - 1) for x, t in zip(w[2:], T9[2:])); pl = w[0] / note
    return dict(tuned=max(abs(x / w[0] / t - 1) for x, t in zip(w[1:], T9[1:])), free=over, tabla=max(over, abs(pl / 1.10 - 1)))[kind], pl, over, B, vac[(0, 1)] / note, w[1]
starts = []
for f in sorted(glob.glob(f"first-pass/ref-{kind}-*-{vol:g}.json")) + sorted(glob.glob(f"first-pass/ref-{kind}-*-1.json")):
    d = json.load(open(f))
    if d['weight'] <= M + 1e-9: starts.append((f"the first pass at {d['weight']:g} skins" + ("" if d['volume'] == vol else f", volume x{d['volume']:g}"), np.array(d['a'])))
nine = np.array(json.load(open(f"../drum/rings2-free-{M:g}.json"))['rings']['40']['a']); fr = np.array(json.load(open(f"../drumfree/s-five-{M:g}.json"))['rings']['40']['a'])
starts += [("the vacuum's tuned load", nine), ("the vacuum's free load", fr), ("a disc to 0.4", L.disc(sk, M / 0.16, 0.4)), ("a disc to 0.5", L.disc(sk, M / 0.25, 0.5)), ("a disc to 0.3", L.disc(sk, M / 0.09, 0.3))] + [(f"random {i + 1}", rng.uniform(0, 20, 40) * (sk.E[:-1] < rng.uniform(0.3, 0.9))) for i in range(4)]
t0 = time.time(); ends = []; best = None
for nm, a0 in starts:
    a, f = L.slp(sk, a0, M); ends.append(f)
    if best is None or f < best[0]: best = (f, a, nm)
for i in range(3):
    a, f = L.slp(sk, best[1] * np.exp(0.3 * rng.standard_normal(40)), M); ends.append(f)
    if f < best[0]: best = (f, a, f"the best, shaken {i + 1}")
f, a, nm = best; ex, pl, over, B, vpl, w11 = exact(a)
print(f"{kind}, {M:g} skins, volume x{vol:g}: least {100 * f:.4f}% ({100 * ex:.4f}% exact) from '{nm}'; {sum(e < f + 2e-5 for e in ends)} of {len(ends)} within 0.002 points, worst {100 * max(ends):.2f}%; used {sk.mass(a):.2f}; B = {B:.4f}; the lowest mode's place {pl:.4f} ({vpl:.4f} without the air); overtones within {100 * over:.3f}%; {time.time() - t0:.0f} s", flush=True)
json.dump(dict(kind=kind, weight=M, volume=vol, B=B, miss=f, exact=ex, place=pl, vacuum_place=vpl, overtones=over, used=sk.mass(a), w11=w11, a=a.tolist(), start=nm, ends=ends), open(sys.argv[4], "w"))
