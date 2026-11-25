"""Checks made after the sheet was scored; none registered.   usage: python -u after.py SECTION OUT.json
M  the mass of moving air, left out of the model: a piston's worth of outside air on the lowest mode alone, as a first-order estimate
T  the tube in place of the spring, on the reference drum's ring loads
R  80 rings for the reference drum's 40-ring loads of 4 skins (the air following the load)
I  strays: modes not among the nine, below 5.5 times the note, in those loads (with their air)"""
import sys, json, math, time
import numpy as np
import airlib as A
L = A.L; SEC = sys.argv[1]; out = {}; T9 = [L.target(m, n) for m, n in L.NINE]
REF = {k: json.load(open(f"ref-{k}-4-1.json")) for k in ("tuned", "free", "tabla")}
def measure(kind, w):
    note = w[1] / 2; over = max(abs(x / note / t - 1) for x, t in zip(w[2:], T9[2:])); pl = w[0] / note
    return dict(tuned=max(abs(x / w[0] / t - 1) for x, t in zip(w[1:], T9[1:])), free=over, tabla=max(over, abs(pl / 1.10 - 1)))[kind], pl, over
if SEC == 'M':
    delta = A.RHO0 * 8 * A.RADIUS / (3 * math.pi) / A.SKIN
    print(f"M. The mass of moving air. A piston of the skin's size in a wall carries air 8a/(3 pi) deep: {1000 * A.RHO0 * 8 * A.RADIUS / (3 * math.pi):.0f} g/m^2, or {delta:.3f} of the bare skin's weight per area.\n   Laid evenly on the lowest mode alone (first order, the mode's shape with its air unchanged), it lowers that mode by:"); out['delta'] = delta; out['rows'] = []
    cases = [("the 1954 disc", L.disc(L.Skin(40, L.NINE), 8.77, 0.4), None)] + [(f"the reference drum's 40-ring load of 4 skins, {k}", np.array(v['a']), v['B']) for k, v in REF.items()]
    for name, a, B in cases:
        if B is None: B = A.reference(A.vacuum(a, [(1, 1)])[(1, 1)])[0]
        sk = A.AirSkin(40, [(0, 1), (0, 2)], B); c, J = sk.solve(a); rho = 1 + np.repeat(a, sk.per)
        # d ln w / d(load on ring j) is J-like; an even load delta on every ring changes ln w by delta * sum_j g_j, g_j = -0.5 * (sum r u^2 on ring j) / (sum r rho u^2)
        ab = np.zeros((3, sk.N)); ab[0, 1:] = sk.off; ab[2, :-1] = sk.off; lam = sk.W[0] ** 2; ab[1] = sk.diag[0] - lam * sk.r * rho
        from scipy.linalg import solve_banded
        u = solve_banded((1, 1), ab, sk.r); share = float((sk.r * u * u).sum() / (sk.r * rho * u * u).sum()); drop = 0.5 * delta * share
        out['rows'].append(dict(name=name, B=B, share=share, drop=drop)); print(f"   {name} (B = {B:.3f}): {100 * drop:.1f}% (the bare skin's share of the mode's moving mass is {share:.3f})")
    print("   The (1,1) mode carries air too, less of it, and that would lower the note as well; I have not computed it. So the lowest mode's place is lowered by less than these figures.")
if SEC == 'T':
    print("T. The tube (12.5 cm deep, as the reference drum) in place of the spring, on the reference drum's 40-ring loads of 4 skins; exact"); out['rows'] = []
    for k, v in REF.items():
        a = np.array(v['a']); e, r = A.load_pieces(a); vac = A.vacuum(a, L.NINE); w11 = vac[(1, 1)]; B, X = A.reference(w11); sp = A.with_air(e, r, L.NINE, B, vac=dict(vac)); t = A.tube_modes(e, r, B, X, 1.3 * vac[(0, 3)]); note = w11 / 2
        # the tube's round modes nearest the spring's three
        near = [min(t, key=lambda z: abs(z - sp[(0, n)])) for n in (1, 2, 3)]; wt = [near[0], w11] + [(near[1] if q == (0, 2) else near[2] if q == (0, 3) else vac[q]) for q in L.NINE[2:]]
        ms, pls, ovs = measure(k, [sp[q] for q in L.NINE]); mt, plt, ovt = measure(k, wt)
        out['rows'].append(dict(kind=k, spring=ms, tube=mt, place_spring=pls, place_tube=plt, round_tube=[z / note for z in t], round_spring=[sp[(0, n)] / note for n in (1, 2, 3)], cavity=math.pi / X / note))
        print(f"   {k}: with the spring {100 * ms:.3f}% (lowest mode at {pls:.4f}); with the tube {100 * mt:.3f}% (lowest mode at {plt:.4f}); round modes of skin and tube, in notes: " + ", ".join(f"{z / note:.3f}" for z in t) + f" (spring: " + ", ".join(f"{sp[(0, n)] / note:.3f}" for n in (1, 2, 3)) + f"; the tube alone resounds at {math.pi / X / note:.2f})", flush=True)
if SEC == 'R':
    print("R. 80 rings, from the reference drum's 40-ring loads of 4 skins split in two (four searches each, the air following the load)"); rng = np.random.default_rng(80); out['rows'] = []; FIVE = [(1, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]
    for k, v in REF.items():
        modes = {"tuned": L.NINE, "free": FIVE, "tabla": [(1, 1), (0, 1)] + FIVE[1:]}[k]; sk = A.RefSkin(80, modes, 1.0, free=(k != "tuned"))
        if k == "tabla": sk.T[1] = 0.55
        start = np.repeat(np.array(v['a']), 2); f0 = sk.miss(start); t0 = time.time(); ends = [L.slp(sk, start, 4.0)] + [L.slp(sk, start * np.exp(0.2 * rng.standard_normal(80)), 4.0) for _ in range(3)]; a, f = min(ends, key=lambda z: z[1])
        e, r = A.load_pieces(a); vac = A.vacuum(a, L.NINE); Bn = A.reference(vac[(1, 1)])[0]; W = A.with_air(e, r, L.NINE, Bn, vac=dict(vac)); ex, pl, ov = measure(k, [W[q] for q in L.NINE])
        out['rows'].append(dict(kind=k, start=f0, miss=f, exact=ex, place=pl, moved=float(np.abs(a - start).max()), ends=[z[1] for z in ends], B=Bn, used=sk.mass(a), a=a.tolist()))
        print(f"   {k}: 40 rings {100 * v['exact']:.4f}%; split in two {100 * f0:.4f}%; after the search {100 * f:.4f}% ({100 * ex:.4f}% exact); the four ended at " + ", ".join(f"{100 * z[1]:.4f}%" for z in ends) + f"; largest change in a ring's load {np.abs(a - start).max():.1f}; place {pl:.4f}; B {Bn:.4f}; used {sk.mass(a):.2f}; {time.time() - t0:.0f} s", flush=True)
if SEC == 'I':
    print("I. Strays: modes that are not among the nine, below 5.5 times the note (finite differences; m up to 12, n up to 6; round modes with their air)"); out['rows'] = []
    for k, v in REF.items():
        a = np.array(v['a']); modes = [(m, n) for m in range(13) for n in range(1, 7)]; sk = A.AirSkin(40, [(1, 1)] + [q for q in modes if q != (1, 1)], v['B']); sk.solve(a, grad=False); note = sk.W[0] / 2
        st = sorted((float(w / note), q[0], q[1]) for w, q in zip(sk.W[1:], sk.modes[1:]) if q not in L.NINE and w / note < 5.5); out['rows'].append(dict(kind=k, strays=st)); print(f"   {k}: " + ("; ".join(f"({m},{n}) at {x:.2f}" for x, m, n in st) or "none"))
if SEC == 'P':
    print("P. The discs as printed in the README, recomputed on the reference drum (exact)"); out['rows'] = []
    def disc(s_, k_):
        e, r = A.disc_pieces(s_, k_); vac = {q: w for q, w in zip(L.NINE, A.drum.modes(s_, k_, L.NINE))}; B = A.reference(vac[(1, 1)])[0]; rnd = A.round_modes(e, r, B, 3); w = [rnd[0], vac[(1, 1)]] + [(rnd[1] if q == (0, 2) else rnd[2] if q == (0, 3) else vac[q]) for q in L.NINE[2:]]; return w, B
    for label, s_, k_, kind in (("all nine tuned, in full", None, None, "tuned"), ("all nine tuned, as printed", 16.8, 0.322, "tuned"), ("aimed at 1.10, as printed", 7.86, 0.384, "tabla"), ("the 1954 disc", 9.77, 0.4, "tuned")):
        if s_ is None: d = json.load(open("discair-ref.json"))['tuned']; s_, k_ = d['s'], d['k']
        w, B = disc(s_, k_); m, pl, ov = measure(kind, w); out['rows'].append(dict(label=label, s=s_, k=k_, miss=m, place=pl, B=B)); print(f"   {label}: {s_:.4g} times over {k_:.4g}: {100 * m:.2f}% ({'the lowest as the note' if kind == 'tuned' else 'the eight misses with the lowest aimed at 1.10'}); the lowest mode's place {pl:.3f}; B {B:.3f}")
if SEC == 'X':
    print("X. What else the reference drum implies: the skin's tension, from the load and the 440 Hz, and the pull around the rim"); out['rows'] = []
    def row(name, w11):
        cm = 2 * math.pi * A.F11 * A.RADIUS / w11; T = A.SKIN * cm * cm; pull = T * 2 * math.pi * A.RADIUS; out['rows'].append(dict(name=name, w11=w11, tension=T, pull=pull, kgf=pull / 9.81)); print(f"   {name}: (1,1) at {w11:.3f} in the model's units; waves on the bare skin at {cm:.0f} m/s; tension {T / 1000:.2f} kN/m; pull around the rim {pull:.0f} N, the weight of {pull / 9.81:.0f} kg")
    row("the plain skin", 3.8317); row("the 1954 disc", A.drum.modes(9.77, 0.4, [(1, 1)])[0])
    for M in (2.0, 4.0, 6.0): row(f"40 rings, {M:g} skins, lowest mode free", json.load(open(f"ref-free-{M:g}-1.json"))['w11'])
    skin = A.SKIN * math.pi * A.RADIUS ** 2 * 1000; out['skin_g'] = skin; print(f"   the bare skin weighs {skin:.2f} g (0.25 kg/m^2 over a radius of 6.5 cm); a patch of 9 to 15 g is {9 / skin:.1f} to {15 / skin:.1f} skins")
if SEC == 'S':
    from scipy.stats import spearmanr
    N = [r for r in json.load(open("named.json")) if r['name'] != "the plain skin"]; lift = [r['reference']['place'] / r['vacuum'] - 1 for r in N]; Bs = [r['reference']['B'] for r in N]; rho = spearmanr(Bs, lift).statistic; out['spearman'] = float(rho); out['n'] = len(N)
    order = sorted(zip(Bs, lift)); print(f"S. Does the lift follow B?  Over the {len(N)} loaded skins of named.out, the rank correlation of the lift with B is {rho:.3f}. In order of B: " + "; ".join(f"B {b:.2f}: {100 * l:.1f}%" for b, l in order))
json.dump(out, open(sys.argv[2], "w"))
