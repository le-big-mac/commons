"""The least found at each weight with air of fixed strength: the search's answer or a walk's, whichever is lower, recomputed by exact
matching.   usage: python -u tables.py B > tables-B.out      (writes best-B.json; keeps exact-cache.json)"""
import sys, json, os, glob, hashlib
import numpy as np
import airlib as A
L = A.L; B = float(sys.argv[1]); W = [1.0, 1.43, 2.0, 2.79, 4.0, 6.0, 12.0]; T = [L.target(m, n) for m, n in L.NINE]
cache = json.load(open("exact-cache.json")) if os.path.exists("exact-cache.json") else {}
def exact(a, free):
    key = hashlib.sha256((np.asarray(a).tobytes() + f"{B}|{free}".encode())).hexdigest()
    if key not in cache:
        e, r = A.load_pieces(a); Wd = A.with_air(e, r, L.NINE, B); w = [Wd[q] for q in L.NINE]; note = w[1] / 2
        cache[key] = [(max(abs(x / note / t - 1) for x, t in zip(w[2:], T[2:])) if free else max(abs(x / w[0] / t - 1) for x, t in zip(w[1:], T[1:]))), w[0] / note, w[1]]
    return cache[key]
best = {}; vac = {}; FIVE = [(1, 1), (2, 1), (0, 2), (3, 1), (1, 2), (4, 1), (2, 2), (0, 3)]
for f in glob.glob("../drum/rings2-free-*.json"): d = json.load(open(f)); vac[("tuned", d['weight'])] = d['rings']
VB = json.load(open("../drumfree/best.json"))
for kind in ("tuned", "free"):
    for R in (40, 80):
        walks = {}
        for way in ("up", "down"):
            f = f"walk-{kind}-{B:g}-{way}-{R}.json"
            if os.path.exists(f):
                for row in json.load(open(f))['walk']: walks[(way, row['weight'])] = row
        carry = None
        for M in W:
            f = f"s-{kind}-{B:g}-{M:g}.json"
            if not os.path.exists(f) or str(R) not in json.load(open(f))['rings']: continue
            s = json.load(open(f))['rings'][str(R)]; cands = [(s['miss'], "the search", s['a'], s['used'])] + [(walks[(way, M)]['miss'], f"the walk {way}", walks[(way, M)]['a'], walks[(way, M)]['used']) for way in ("up", "down") if (way, M) in walks]
            fd, src, a, used = min(cands, key=lambda c: c[0])
            if carry is not None and carry[0] < fd - 1e-9:      # a lighter load is allowed here too: if it does better, search on from it
                sk = A.AirSkin(R, FIVE if kind == "free" else L.NINE, B, free=(kind == "free")); a2, f2 = L.slp(sk, np.array(carry[1]), M)
                if f2 < fd: fd, src, a, used = f2, "a lighter load carried up", a2.tolist(), sk.mass(a2)
            carry = (fd, a); ex, pl, w11 = exact(a, kind == "free")
            best[f"{kind}|{M:g}|{R}"] = dict(fd=fd, exact=ex, place=pl, w11=w11, Bref=A.reference(w11)[0], a=a, src=src, used=used, search=s['miss'], walk_gain=s['miss'] - fd, agree=sum(e < s['miss'] + 2e-5 for e in s['ends']), n=len(s['ends']))
json.dump(cache, open("exact-cache.json", "w")); json.dump(best, open(f"best-{B:g}.json", "w"))
print(f"WEIGHT-ROWS B = {B:g}")
for M in W:
    cells = []
    for kind in ("tuned", "free"):
        v = vac[("tuned", M)]['40']['exact'] if kind == "tuned" else VB[f"five|{M:g}|40"]['exact']; cells.append(f"{100 * v:.3f}%")
        for R in (40, 80):
            b = best.get(f"{kind}|{M:g}|{R}"); cells.append(f"{100 * b['exact']:.3f}%" if b else "")
        b = best.get(f"{kind}|{M:g}|40"); cells.append(f"{b['place']:.3f}" if b else ""); cells.append(f"{b['Bref']:.2f}" if b else "")
    print(f"| {M:g} | " + " | ".join(cells) + " |")
print("NOTES")
for kind in ("tuned", "free"):
    for R in (40, 80):
        ks = [f"{kind}|{M:g}|{R}" for M in W if f"{kind}|{M:g}|{R}" in best]
        print(f"{kind}, {R} rings: the least came from " + "; ".join(f"{k.split('|')[1]}: {best[k]['src']}" for k in ks))
        print(f"{kind}, {R} rings: the walks lower than the search, in points: " + "; ".join(f"{k.split('|')[1]}: {100 * best[k]['walk_gain']:.4f}" for k in ks))
        ex = [best[k]['exact'] for k in ks]; print(f"{kind}, {R} rings: places where more weight gave a larger miss: " + ("; ".join(f"{ks[i].split('|')[1]} to {ks[i + 1].split('|')[1]}" for i in range(len(ks) - 1) if ex[i + 1] > ex[i] + 1e-9) or "none"))
        print(f"{kind}, {R} rings: weight used of the weight allowed: " + "; ".join(f"{k.split('|')[1]}: {best[k]['used']:.2f}" for k in ks))
        print(f"{kind}, {R} rings: searches within 0.002 points of the search's least: " + "; ".join(f"{k.split('|')[1]}: {best[k]['agree']} of {best[k]['n']}" for k in ks))
