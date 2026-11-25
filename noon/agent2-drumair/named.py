"""Named loads on the reference drum: where the lowest mode sits in a vacuum and with air.   usage: python -u named.py OUT.json
Every figure by exact matching.  Volumes: the reference's, twice it and half it.  Tube: the reference's depth."""
import sys, json, math
import numpy as np
import airlib as A
L = A.L; out = []
R3 = [(0, 1), (1, 1), (0, 2), (0, 3)]
def study(name, edges, rho):
    vac = A.with_air(edges, rho, R3, 0.0); w11 = vac[(1, 1)]; note = w11 / 2; row = dict(name=name, w11=w11, vacuum=vac[(0, 1)] / note, vac02=vac[(0, 2)] / note, vac03=vac[(0, 3)] / note)
    for label, vol in (("double", 2.0), ("reference", 1.0), ("half", 0.5)):
        B, X = A.reference(w11, vol); s = A.with_air(edges, rho, R3, B, vac=dict(vac)); row[label] = dict(B=B, place=s[(0, 1)] / note, r02=s[(0, 2)] / vac[(0, 2)] - 1, r03=s[(0, 3)] / vac[(0, 3)] - 1)
    B, X = A.reference(w11)
    t = A.tube_modes(edges, rho, B, X, 1.25 * vac[(0, 3)]); row['tube'] = dict(X=X, place=t[0] / note, all=[w / note for w in t], x=[X * w for w in t], cavity=math.pi / X / note)
    out.append(row); tb = row['tube']
    print(f"{name}\n   (1,1) at {w11:.4f}; B of the reference drum {row['reference']['B']:.3f}; the lowest mode's place: vacuum {row['vacuum']:.4f}; spring, volume doubled {row['double']['place']:.4f}, reference {row['reference']['place']:.4f}, halved {row['half']['place']:.4f}; tube {tb['place']:.4f}")
    print(f"   the reference spring raises (0,2) by {100 * row['reference']['r02']:+.2f}% and (0,3) by {100 * row['reference']['r03']:+.2f}%; in units of the note the vacuum's round modes are at {row['vacuum']:.3f}, {row['vac02']:.3f}, {row['vac03']:.3f}; with the tube the round modes of skin and air are at " + ", ".join(f"{w:.3f}" for w in tb['all']) + f" (the closed tube alone would resound at {tb['cavity']:.3f})", flush=True)
study("the plain skin", [1.0], [1.0])
study("the 1954 disc: 9.77 times over 0.4", *A.disc_pieces(9.77, 0.4))
study("the first study's best disc, lowest mode tuned: 9.938 times over 0.4004", *A.disc_pieces(9.938, 0.4004))
for M in ("1.43", "4", "12"):
    a = np.array(json.load(open(f"../drum/rings2-free-{M}.json"))['rings']['40']['a']); study(f"the first study's 40-ring load of {M} skins, lowest mode tuned", *A.load_pieces(a))
D = json.load(open("../drumfree/disc.json")); study(f"the third study's best disc, lowest mode free: {D['five']['s']:.3f} times over {D['five']['k']:.4f}", *A.disc_pieces(D['five']['s'], D['five']['k']))
G = json.load(open("../drumfree/after-G.json"))['two1.43']; study(f"the third study's two discs: {G['outer']:.3f} times to {G['ko']:.4f}, {G['inner']:.3f} inside {G['ki']:.4f}", [G['ki'], G['ko'], 1.0], [G['inner'], G['outer'], 1.0])
B5 = json.load(open("../drumfree/best.json"))
for M in ("1.43", "4", "12"): study(f"the third study's 40-ring load of {M} skins, lowest mode free", *A.load_pieces(np.array(B5[f"five|{M}|40"]['a'])))
mid = (np.arange(400) + 0.5) / 400; study("the paper's smooth step (sigma 2.57, k 0.492, xi 0.091), on 400 rings", *A.load_pieces((2.57 ** 2 - 1) / 2 * (1 - np.tanh((mid - 0.492) / 0.091))))
for s, k in ((6.25, 0.45), (16.0, 0.45), (10.0, 0.50), (6.25, 0.55), (16.0, 0.55), (10.0, 0.35), (16.0, 0.30), (25.0, 0.30)): study(f"an even disc: {s:g} times over {k:g}", *A.disc_pieces(s, k))
json.dump(out, open(sys.argv[1], "w"))
