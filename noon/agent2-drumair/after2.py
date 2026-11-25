"""The referee's controls, redone in my own code.  None registered.   usage: python -u after2.py SECTION OUT.json
F  the discs that the second-look fits chose, put on the reference drum
C  how many of the nineteen named loads have their lowest mode within 0.03 of 1.10, in a vacuum and with the reference air
K  the tube's factor x cot x at the measured tabla's round modes
A  an even layer of moving air on every mode, not only the lowest
W  the load aimed at 1.10 made to carry more weight, and kept inside half the radius
U  the free load of 4 skins searched again with the tube in place of the spring
N  what tuning the drum up two semitones does to the lowest mode's place
G  the lift against the added weight"""
import sys, json, math, time
import numpy as np
from scipy.optimize import linprog
import airlib as A
L = A.L; SEC = sys.argv[1]; out = {}; T9 = [L.target(m, n) for m, n in L.NINE]; FIVE = [(1, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]
REF = lambda k, M, v=1: json.load(open(f"ref-{k}-{M:g}-{v:g}.json"))
def measure(kind, w):
    note = w[1] / 2; over = max(abs(x / note / t - 1) for x, t in zip(w[2:], T9[2:])); pl = w[0] / note
    return dict(tuned=max(abs(x / w[0] / t - 1) for x, t in zip(w[1:], T9[1:])), free=over, tabla=max(over, abs(pl / 1.10 - 1)))[kind], pl, over
def exact_ref(a, kind, vol=1.0):
    e, r = A.load_pieces(a); vac = A.vacuum(a, L.NINE); B = A.reference(vac[(1, 1)], vol)[0]; W = A.with_air(e, r, L.NINE, B, vac=dict(vac)); return (*measure(kind, [W[q] for q in L.NINE]), B, vac)
if SEC == 'F':
    print("F. The discs the second-look fits chose, on the reference drum (exact)"); out['rows'] = []
    for name, s, k in (("without the label (3,2), on the grid", 4.10, 0.5625), ("the low modes alone", 4.20, 0.4838), ("the root mean square", 9.70, 0.4218), ("all twelve, largest difference", 34.42, 0.2300), ("the third study's best disc", 4.343, 0.5042)):
        e, r = A.disc_pieces(s, k); w11 = A.drum.modes(s, k, [(1, 1)])[0]; B = A.reference(w11)[0]; note = w11 / 2; v = A.round_modes(e, r, 0.0, 1)[0] / note; p = A.round_modes(e, r, B, 1)[0] / note
        out['rows'].append(dict(name=name, s=s, k=k, B=B, vacuum=v, place=p)); print(f"   {name}: {s:g} times over {k:g}: B = {B:.2f}; the lowest mode at {v:.3f} in a vacuum and {p:.3f} with the reference air")
if SEC == 'C':
    N = [r for r in json.load(open("named.json")) if r['name'] != "the plain skin"]; v = [r['vacuum'] for r in N]; a = [r['reference']['place'] for r in N]
    out.update(n=len(N), near_vacuum=sum(abs(x - 1.10) <= 0.03 for x in v), near_air=sum(abs(x - 1.10) <= 0.03 for x in a), vacuum=[min(v), max(v)], air=[min(a), max(a)])
    print(f"C. Of the {len(N)} loaded skins of named.out, the lowest mode is within 0.03 of 1.10 in {out['near_vacuum']} in a vacuum and in {out['near_air']} with the reference air; the places run from {min(v):.3f} to {max(v):.3f} in a vacuum and from {min(a):.3f} to {max(a):.3f} with air")
if SEC == 'K':
    out['rows'] = [dict(hz=f, x=2 * math.pi * f * A.DEPTH / A.C, factor=(2 * math.pi * f * A.DEPTH / A.C) / math.tan(2 * math.pi * f * A.DEPTH / A.C)) for f in (240, 660, 1060, 1100)]
    print("K. The tube's factor x cot x for a cavity 12.5 cm deep: " + "; ".join(f"{r['hz']} Hz: x = {r['x']:.2f}, factor {r['factor']:+.2f}" for r in out['rows']) + f"; the pipe alone resounds at {A.C / (2 * A.DEPTH):.0f} Hz")
if SEC == 'A':
    delta = A.RHO0 * 8 * A.RADIUS / (3 * math.pi) / A.SKIN; out['delta'] = delta; out['rows'] = []
    print(f"A. An even layer of {delta:.3f} of the bare skin's weight per area laid on every mode (a piston's worth of air; a rough sum, not a model)")
    cases = [("the 1954 disc", L.disc(L.Skin(40, L.NINE), 8.77, 0.4), "tuned")] + [(f"the reference drum's 40-ring load of 4 skins, {k}", np.array(REF(k, 4)['a']), k) for k in ("tuned", "free", "tabla")]
    for name, a, kind in cases:
        sk = A.RefSkin(40, L.NINE); sk.solve(a, grad=False); W0 = sk.W.copy(); B0 = sk.B; fx = A.AirSkin(40, L.NINE, B0); fx.solve(a + delta, grad=False); W1 = fx.W.copy(); sk.solve(a + delta, grad=False); W2 = sk.W.copy(); B2 = sk.B
        m0, p0, o0 = measure(kind, list(W0)); m1, p1, o1 = measure(kind, list(W1)); m2, p2, o2 = measure(kind, list(W2))
        out['rows'].append(dict(name=name, fall01=1 - W1[0] / W0[0], fall11=1 - W1[1] / W0[1], place0=p0, place_fixed=p1, place_retuned=p2, miss0=m0, miss_fixed=m1, miss_retuned=m2, B0=B0, B2=B2))
        print(f"   {name}: at the same tension the lowest mode falls by {100 * (1 - W1[0] / W0[0]):.2f}% and (1,1) by {100 * (1 - W1[1] / W0[1]):.2f}%; the place goes from {p0:.4f} to {p1:.4f}; tuned back to 440 Hz (B {B0:.3f} to {B2:.3f}) it is {p2:.4f}; the load's own measure goes from {100 * m0:.3f}% to {100 * m2:.3f}% (not searched again)", flush=True)
if SEC == 'W':
    def slp_min(skin, a0, M, Mmin, ub=None, iters=700):
        """lib12.slp with a least weight as well, and an optional ceiling on each ring (0 to keep a ring bare)"""
        R = skin.R; K = len(skin.modes) - 1; a = skin.fit(a0, M); a = a if ub is None else np.minimum(a, ub)
        if skin.mass(a) < Mmin: a = a * Mmin / skin.mass(a)
        c, J = skin.solve(a); f = float(np.abs(c).max()); S = M / 0.16; delta = 0.3 * S; cost = np.zeros(R + 1); cost[-1] = 1.0; ones = np.ones((K, 1)); ub = np.full(R, np.inf) if ub is None else ub
        for it in range(iters):
            A_ub = np.vstack([np.hstack([J, -ones]), np.hstack([-J, -ones]), np.concatenate([skin.A, [0.0]])[None, :], np.concatenate([-skin.A, [0.0]])[None, :]]); b_ub = np.concatenate([-c, c, [M - skin.mass(a)], [skin.mass(a) - Mmin]])
            res = linprog(cost, A_ub=A_ub, b_ub=b_ub, bounds=[(max(-a[j], -delta), min(delta, ub[j] - a[j])) for j in range(R)] + [(0, None)], method='highs')
            if res.status != 0 or f - res.x[-1] < 1e-13:
                delta *= 0.5
                if delta < 1e-9 * S: break
                continue
            a1 = np.maximum(a + res.x[:R], 0); c1, J1 = skin.solve(a1); f1 = float(np.abs(c1).max())
            if f - f1 >= 0.1 * (f - res.x[-1]) and Mmin - 1e-9 <= skin.mass(a1) <= M + 1e-9: a, c, J, f = a1, c1, J1, f1; delta = min(delta * 1.5, 2 * S)
            else: delta *= 0.5
            if delta < 1e-9 * S: break
        return a, f
    print("W. The load aimed at 1.10 on the reference drum (40 rings, up to 12 skins): made to carry more, and kept inside half the radius"); out['rows'] = []; rng = np.random.default_rng(12)
    sk = A.RefSkin(40, [(1, 1), (0, 1)] + FIVE[1:], 1.0, free=True); sk.T[1] = 0.55; base = np.array(REF("tabla", 6)['a']); inside = np.where(sk.E[1:] <= 0.5 + 1e-9, np.inf, 0.0)
    for name, Mmin, ub in (("at least 6 skins", 6.0, None), ("at least 8 skins", 8.0, None), ("at least 4 skins, all inside half the radius", 4.0, inside), ("at least 6 skins, all inside half the radius", 6.0, inside), ("any weight up to 12, all inside half the radius", 0.0, inside)):
        t0 = time.time(); starts = [base, base * 1.3, base * np.exp(0.2 * rng.standard_normal(40)), base * np.exp(0.2 * rng.standard_normal(40))]; ends = [slp_min(sk, a0, 12.0, Mmin, ub) for a0 in starts]; a, f = min(ends, key=lambda z: z[1]); ex, pl, ov, B, vac = exact_ref(a, "tabla")
        last = int(np.nonzero(a > 0.05)[0][-1]); out['rows'].append(dict(name=name, miss=f, exact=ex, used=sk.mass(a), place=pl, B=B, ends=[z[1] for z in ends], a=a.tolist(), loaded_to=float(sk.E[last + 1]), heaviest=float(a.max())))
        print(f"   {name}: least {100 * f:.4f}% ({100 * ex:.4f}% exact) using {sk.mass(a):.2f} skins; the four ended at " + ", ".join(f"{100 * z[1]:.3f}%" for z in ends) + f"; place {pl:.4f}; B {B:.3f}; loaded out to {sk.E[last + 1]:.3f}; heaviest ring +{a.max():.0f}; {time.time() - t0:.0f} s", flush=True)
if SEC == 'U':
    print("U. The tube in the search (a cavity 12.5 cm deep): the spring's search is repeated with each round mode's target moved by what the tube does to it, until the two agree"); out['rows'] = []
    for kind, M in (("free", 4.0), ("tabla", 4.0), ("tuned", 4.0)) if len(sys.argv) < 4 else ((sys.argv[3], 4.0),):
        modes = {"tuned": L.NINE, "free": FIVE, "tabla": [(1, 1), (0, 1)] + FIVE[1:]}[kind]; a = np.array(REF(kind, M)['a']); hist = []
        for it in range(6):
            e, r = A.load_pieces(a); vac = A.vacuum(a, L.NINE); B, X = A.reference(vac[(1, 1)]); sp = A.with_air(e, r, L.NINE, B, vac=dict(vac)); tb = A.tube_modes(e, r, B, X, 1.3 * vac[(0, 3)]); near = {n: min(tb, key=lambda z: abs(z - sp[(0, n)])) for n in (1, 2, 3)}
            wt = [near[1], vac[(1, 1)]] + [(near[2] if q == (0, 2) else near[3] if q == (0, 3) else vac[q]) for q in L.NINE[2:]]; m, pl, ov = measure(kind, wt); hist.append(dict(miss=m, place=pl, B=B, used=float(a @ (np.arange(1, 41) ** 2 - np.arange(40) ** 2) / 1600)))
            print(f"   {kind}, {M:g} skins, round {it}: with the tube {100 * m:.4f}%; the lowest mode at {pl:.4f}; B {B:.4f}", flush=True)
            if it == 5: break
            sk = A.RefSkin(40, modes, 1.0, free=(kind != "tuned"))
            if kind == "tabla": sk.T[1] = 0.55
            for n in (1, 2, 3):                                       # aim the spring's round mode at target * (spring / tube), so that the tube's lands on the target
                if kind == "tuned" and n == 1: sk.T[1:] *= near[1] / sp[(0, 1)]             # the lowest mode is the reference there: move every other target the other way
                elif (0, n) in sk.modes: i = sk.modes.index((0, n)); sk.T[i] *= sp[(0, n)] / near[n]
            a, f = L.slp(sk, a, M)
        out['rows'].append(dict(kind=kind, weight=M, rounds=hist, a=a.tolist()))
if SEC == 'N':
    print("N. Tuning up: the same load with (1,1) raised from 440 Hz by two semitones (a factor 1.12), so that B falls by 1.12 squared"); out['rows'] = []
    for name, a in (("the 1954 disc", L.disc(L.Skin(40, L.NINE), 8.77, 0.4)), ("40 rings, 4 skins, lowest mode free", np.array(REF("free", 4)['a'])), ("40 rings, 2 skins, lowest mode free", np.array(REF("free", 2)['a']))):
        e, r = A.load_pieces(a); vac = A.vacuum(a, [(0, 1), (1, 1)]); B = A.reference(vac[(1, 1)])[0]; note = vac[(1, 1)] / 2; p0 = A.round_modes(e, r, B, 1)[0] / note; p1 = A.round_modes(e, r, B / 1.12 ** 2, 1)[0] / note
        out['rows'].append(dict(name=name, low=p0, high=p1)); print(f"   {name}: the lowest mode's place {p0:.4f} at 440 Hz and {p1:.4f} two semitones up: lower by {p0 - p1:.4f}")
if SEC == 'G':
    from scipy.stats import spearmanr
    N = [r for r in json.load(open("named.json")) if r['name'] != "the plain skin"]; lift = [r['reference']['place'] / r['vacuum'] - 1 for r in N]; wts = []
    for r in N:
        nm = r['name']
        if "times over" in nm and "two discs" not in nm: s_, k_ = [float(x) for x in __import__('re').findall(r"([\d.]+) times over ([\d.]+)", nm)[0]]; wts.append((s_ - 1) * k_ * k_)
        elif "two discs" in nm: wts.append(1.43)
        elif "smooth step" in nm: mid = (np.arange(400) + 0.5) / 400; wts.append(float(((2.57 ** 2 - 1) / 2 * (1 - np.tanh((mid - 0.492) / 0.091)) * 2 * mid / 400).sum()))
        else: wts.append(float(__import__('re').findall(r"load of ([\d.]+) skins", nm)[0]))
    rho = spearmanr(wts, lift).statistic; out.update(spearman=float(rho), n=len(N), weights=wts); print(f"G. Over the {len(N)} loaded skins the rank correlation of the lift with the added weight is {rho:.3f} (with B it is +0.940)")
json.dump(out, open(sys.argv[2], "w"))
