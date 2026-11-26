"""At the very first step, how long are the two pulls on each fish? A look at why the combining rule matters.
usage: python -I firststep.py > firststep.out      (numpy; couzin.py beside it)   Added 26 November 2026.
For the first ten seeds of the forty-seed runs, at widths 2 and 8: the length of the lining-up sum d_o and of the
attraction sum d_a (plain sums of unit vectors, as in the paper), and for how many fish the second is the longer."""
import os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from couzin import School

if __name__ == '__main__':
    for dro in (2, 8):
        lo = []; la = []; longer = []; no = []; na = []; nrep = []; nboth = []; angp = []; angv = []
        for seed in range(10):
            s = School(ro=1 + dro, seed=1000 + seed)
            d = s.x[None] - s.x[:, None]; dist = np.linalg.norm(d, axis=2); np.fill_diagonal(dist, np.inf)
            u = d / np.where(np.isfinite(dist), dist, 1)[..., None]
            vis = (u * s.v[:, None]).sum(2) > np.cos(np.pi - s.blind / 2)
            zo = (dist >= s.rr) & (dist < s.ro) & vis; za = (dist >= s.ro) & (dist < s.ra) & vis
            d_o = np.linalg.norm((s.v[None] * zo[..., None]).sum(1), axis=1); d_a = np.linalg.norm((u * za[..., None]).sum(1), axis=1)
            # added after a reader's third pass: repulsion comes first under either rule, so count who is left
            rep = (dist < s.rr).any(1); both = ~rep & zo.any(1) & za.any(1)
            vo = (s.v[None] * zo[..., None]).sum(1); va = (u * za[..., None]).sum(1)
            unit = lambda w: w / np.maximum(np.linalg.norm(w, axis=1, keepdims=True), 1e-12)
            ang = lambda w: np.degrees(np.arccos(np.clip((unit(w) * unit(va)).sum(1), -1, 1)))
            nrep.append(int(rep.sum())); nboth.append(int(both.sum()))
            angp.append(np.median(ang(.5 * (vo + va))[both])); angv.append(np.median(ang(.5 * (unit(vo) + unit(va)))[both]))
            lo.append(d_o.mean()); la.append(d_a.mean()); longer.append(int((d_a > d_o).sum())); no.append(zo.sum(1).mean()); na.append(za.sum(1).mean())
        print(f"width {dro}: neighbours in the lining-up zone {np.mean(no):.1f} and in the attraction zone {np.mean(na):.1f} on average;"
              f" length of the lining-up sum {np.mean(lo):.1f}, of the attraction sum {np.mean(la):.1f}; the attraction sum is the longer for {min(longer)} to {max(longer)} of 100 fish over the ten seeds")
        print(f"   fish with a neighbour inside the repulsion radius, which turn away from it under either rule: {min(nrep)} to {max(nrep)} of 100, mean {np.mean(nrep):.0f};"
              f" fish with none, and with neighbours in both other zones: {min(nboth)} to {max(nboth)}. For those, the angle between where the rule points and the attraction sum,"
              f" median over fish and then mean over the ten seeds: the paper's rule {np.mean(angp):.0f} degrees, my variant {np.mean(angv):.0f} degrees")
