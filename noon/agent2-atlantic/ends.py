"""The two ends of the South Atlantic fit, tested after a reader said my account of the northern end was wrong.
usage: python -I ends.py ETOPO1_Ice_g_gmt4.grd > ends.out             (numpy, scipy, scikit-image; ten seconds; fit.py beside it)
       python -I ends.py ETOPO1_Ice_g_gmt4.grd addendum > ends2.out   (the like-for-like stretch, sealed separately)
       python -I ends.py ETOPO1_Ice_g_gmt4.grd sweep > ends3.out      (not sealed: other cuts and depths; two minutes)
       python -I ends.py ETOPO1_Ice_g_gmt4.grd depths > ends4.out     (not sealed: all six depths on Bullard's stretch)
       python -I ends.py ETOPO1_Ice_g_gmt4.grd figdata ends.npz > ends5.out   (not sealed: where the refit's misfits are; for figures2.py)
       python -I ends.py ETOPO1_Ice_g_gmt4.grd eqsearch > ends6.out   (not sealed: every end of the equatorial search)
       python -I ends.py ETOPO1_Ice_g_gmt4.grd after > ends7.out      (not sealed: checks after a reader read the corrections; three minutes)

Expectations sealed in ends-prediction.md before this was run (26 November 2026).
Africa's margin is taken to 12 N and 24 E, so that it holds the Guinea plateau; South America's is as in fit.py.
"""
import os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))    # fit.py sits beside this file (python -I leaves the folder off the path)
import numpy as np
from scipy.spatial import cKDTree
import fit as F

WHOLE = (46.74, -31.20, 56.30)            # my whole-ocean rotation at 900 m, from fit.out
BULLARD = (44.0, -30.6, 57.0)             # fit 9 of Bullard, Everett and Smith (1965)
HEINE = (50.4, -34.4, 53.4)               # Heine, Zoethout and Mueller (2013), South America against north-west Africa, as the reader copied it
MOULIN = (52.1, -34.6, 53.0)              # Moulin, Aslanian and Unternehr (2010), Santos block against West Africa, as the reader copied it


def km(v, tree):
    d, i = tree.query(v)
    return F.R * 2 * np.arcsin(np.clip(d / 2, 0, 1)), i


def main(path):
    lats, lons, z = F.load(path)
    depth = 900
    sam, afr = F.margins(lats, lons, z, depth, afr_north=12.0, afr_east=24.0)
    la_s, lo_s = F.latlon(sam); la_a, lo_a = F.latlon(afr)
    print(f"900 m line. South America's margin {len(sam) * 20} km, from {la_s[0]:.1f} N {lo_s[0]:.1f} E to {la_s[-1]:.1f} N {lo_s[-1]:.1f} E;"
          f" Africa's {len(afr) * 20} km, from {la_a[0]:.1f} N {lo_a[0]:.1f} E to {la_a[-1]:.1f} N {lo_a[-1]:.1f} E")
    tree_all = cKDTree(afr)
    gui = la_s > 4.0                                                   # the Guianas' stretch
    south = la_s < -20.0
    eq_s = sam[la_s > -5.0]                                            # the equatorial segment, South America's side
    keep_a = (lo_a < 3.0) & (la_a > 0.0)                               # Africa's side: from the northern end to 3 E
    idx = np.nonzero(keep_a)[0]
    runs = np.split(idx, np.nonzero(np.diff(idx) > 1)[0] + 1)
    eq_a = afr[max(runs, key=len)]
    afr_south = afr[la_a < 0.0]
    la_e, lo_e = F.latlon(eq_a)
    print(f"the Guianas' stretch: {gui.sum() * 20} km. The equatorial segment: {len(eq_s) * 20} km of South America's margin,"
          f" {len(eq_a) * 20} km of Africa's (from {la_e[0]:.1f} N {lo_e[0]:.1f} E to {la_e[-1]:.1f} N {lo_e[-1]:.1f} E)")

    def report(name, rot):
        w = F.w_of(*rot)
        rs = sam @ F.rotmat(w).T
        g, i = km(rs[gui], tree_all)
        la_r, lo_r = F.latlon(rs[gui])
        e = F.misfit(w, eq_s, eq_a)
        s = F.misfit(w, sam[south], afr_south)
        endhit = np.mean((i == 0) | (i == len(afr) - 1))
        print(f"  {name:38s} {rot[2]:5.1f} deg about {rot[0]:5.1f} N {rot[1]:6.1f} E | the Guianas' stretch to Africa's margin: median {np.median(g):4.0f} km,"
              f" least {g.min():4.0f}, most {g.max():4.0f} (nearest point is an end of Africa's margin for {100 * endhit:.0f}%);"
              f" it lands at {la_r.min():.1f} to {la_r.max():.1f} N, {lo_r.min():.1f} to {lo_r.max():.1f} E"
              f" | equatorial segment misfit {e:6.1f} km | south of 20 S misfit {s:7.1f} km")
        return np.median(g), e, s

    print("under four rotations:")
    gW, eW, sW = report('my whole-ocean rotation (fit.py)', WHOLE)
    report('Bullard 1965, fit 9', BULLARD)
    report('Heine et al. 2013, equatorial', HEINE)
    report('Moulin et al. 2010, Santos block', MOULIN)

    res = F.best_rotation(eq_s, eq_a)
    f, w = res[0]
    plat, plon, ang = F.pole_of(w)
    near = sum(1 for g, _ in res if g < f * 1.02)
    second = next((g for g, _ in res if g > f * 1.02), np.nan)
    print(f"best rotation for the equatorial segment alone: {ang:.2f} deg about {plat:.2f} N, {plon:.2f} E; misfit {f:.1f} km;"
          f" starts reaching it: {near} of {len(res)}, next best {second:.0f} km")
    print("  the five best ends of the search: " + "; ".join(f"{g:.1f} km at {F.pole_of(x)[2]:.1f} deg about {F.pole_of(x)[0]:.1f} N {F.pole_of(x)[1]:.1f} E" for g, x in res[:5]))
    gE, eE, sE = report('my equatorial rotation', (plat, plon, ang))
    dH = float(F.gc(F.unit(plat, plon), F.unit(HEINE[0], HEINE[1])) / F.R * 180 / np.pi)
    dW = float(F.gc(F.unit(plat, plon), F.unit(WHOLE[0], WHOLE[1])) / F.R * 180 / np.pi)
    print(f"  its pole is {dH:.1f} deg from Heine's and {dW:.1f} deg from my whole-ocean pole; angle {ang - HEINE[2]:+.1f} from Heine's, {ang - WHOLE[2]:+.1f} from the whole-ocean one")

    # where the southern end goes under the whole-ocean rotation
    w = F.w_of(*WHOLE)
    rs = sam @ F.rotmat(w).T
    tail = la_s < -41.0
    g, i = km(rs[tail], tree_all)
    la_r, lo_r = F.latlon(rs[tail])
    print(f"the southern end under my whole-ocean rotation: South America's margin south of 41 S ({tail.sum() * 20} km) lands at {la_r.min():.1f} to {la_r.max():.1f} N,"
          f" {lo_r.min():.1f} to {lo_r.max():.1f} E; Africa's margin ends at {la_a[-1]:.1f} N {lo_a[-1]:.1f} E and reaches {la_a.min():.1f} N at its most southerly;"
          f" distance to Africa's margin: median {np.median(g):.0f} km, {g.min():.0f} to {g.max():.0f}; nearest point is the end of Africa's margin for {100 * np.mean(i == len(afr) - 1):.0f}%")

    print("the sealed lines:")
    print(f"  E1 (the Guianas' stretch still a median of more than 150 km away under the whole-ocean rotation): {gW:.0f} km -> {'held' if gW > 150 else 'failed'}")
    print(f"  E2 (equatorial pole north of 46.7 N and angle below 56.3): {plat:.2f} N, {ang:.2f} -> {'held' if plat > 46.74 and ang < 56.30 else 'failed'}")
    print(f"  E3 (pole within 6 deg of Heine's, angle within 3): {dH:.1f} deg, {ang - HEINE[2]:+.1f} -> {'held' if dH < 6 and abs(ang - HEINE[2]) < 3 else 'failed'}")
    print(f"  E4 (equatorial misfit less than half the whole-ocean rotation's there): {eE:.1f} against {eW:.1f} km -> {'held' if eE < eW / 2 else 'failed'}")
    print(f"  E5 (the Guianas' stretch a median of less than 100 km away under the equatorial rotation): {gE:.0f} km -> {'held' if gE < 100 else 'failed'}")
    print(f"  E6 (south of 20 S worse than 250 km under the equatorial rotation): {sE:.1f} km -> {'held' if sE > 250 else 'failed'}")


def like_for_like(path):
    """The addendum (ends2-prediction.md, sealed before this was run): a refit on something like Bullard's own stretch."""
    lats, lons, z = F.load(path)
    sam, afr = F.margins(lats, lons, z, 900)                           # Africa's margin as in fit.py: south of 8 N, west of 20 E
    la_s, lo_s = F.latlon(sam)
    sam2 = sam[la_s < 2.0]                                             # South America's margin from about the mouth of the Amazon southward
    FIT9, FIT2 = (44.0, -30.6, 57.0), (42.9, -30.1, 57.1)
    res = F.best_rotation(sam2, afr)
    f, w = res[0]
    plat, plon, ang = F.pole_of(w)
    sep = lambda a: float(F.gc(F.unit(plat, plon), F.unit(a[0], a[1])) / F.R * 180 / np.pi)
    near = sum(1 for g, _ in res if g < f * 1.02)
    second = next((g for g, _ in res if g > f * 1.02), np.nan)
    f9 = F.misfit(F.w_of(*FIT9), sam2, afr); f2 = F.misfit(F.w_of(*FIT2), sam2, afr); fw = F.misfit(F.w_of(*WHOLE), sam2, afr)
    print("the addendum: South America's margin south of 2 N against Africa's margin as in fit.py, 900 m line")
    print(f"  margins {len(sam2) * 20} and {len(afr) * 20} km; best rotation {ang:.2f} deg about {plat:.2f} N, {plon:.2f} E; misfit {f:.1f} km;"
          f" starts reaching it: {near} of {len(res)}, next best {second:.0f} km")
    print(f"  its pole is {sep(FIT9):.2f} deg from Bullard's fit 9 and {sep(FIT2):.2f} from his fit 2 (my whole-ocean pole: 2.77 and 3.92); angle {ang - 57.0:+.2f} from fit 9's")
    print(f"  on this stretch: Bullard's fit 9 gives {f9:.1f} km, his fit 2 {f2:.1f} km, my whole-ocean rotation {fw:.1f} km")
    print("the sealed lines of the addendum:")
    print(f"  F1 (nearer to fit 9 than 2.8 deg): {sep(FIT9):.2f} -> {'held' if sep(FIT9) < 2.77 else 'failed'}")
    ok2 = (sep(FIT9) < 1.5 or sep(FIT2) < 1.5) and abs(ang - 57.0) < 0.7
    print(f"  F2 (within 1.5 deg of fit 9 or fit 2, angle within 0.7 of 57.0): {sep(FIT9):.2f}, {sep(FIT2):.2f}, {ang - 57.0:+.2f} -> {'held' if ok2 else 'failed'}")
    print(f"  F3 (misfit below 100 km): {f:.1f} -> {'held' if f < 100 else 'failed'}")
    print(f"  F4 (fit 9 no more than 15% worse than the refit): {100 * (f9 / f - 1):.1f}% worse -> {'held' if f9 <= 1.15 * f else 'failed'}")


def sweep(path):
    """Not sealed: tried after both sheets were scored, to see how much the addendum's answer owes to the one cut and the one depth."""
    lats, lons, z = F.load(path)
    FIT9 = (44.0, -30.6, 57.0)
    print("not sealed. South America's margin cut to south of a latitude, against Africa's margin as in fit.py:")
    print("  depth   cut     best rotation                    misfit   pole from fit 9   angle from fit 9's   fit 9 on the same stretch")
    for depth in (200, 500, 900, 2000):
        sam, afr = F.margins(lats, lons, z, depth)
        la_s, lo_s = F.latlon(sam)
        for cut in (8.0, 6.0, 4.0, 2.0, 0.0, -2.0):
            sam2 = sam[la_s < cut]
            res = F.best_rotation(sam2, afr)
            f, w = res[0]
            plat, plon, ang = F.pole_of(w)
            sep = float(F.gc(F.unit(plat, plon), F.unit(FIT9[0], FIT9[1])) / F.R * 180 / np.pi)
            f9 = F.misfit(F.w_of(*FIT9), sam2, afr)
            print(f"  {depth:5d} {cut:5.0f} N   {ang:6.2f} deg about {plat:6.2f} N {plon:7.2f} E   {f:6.1f} km   {sep:6.2f} deg        {ang - 57.0:+6.2f} deg           {f9:6.1f} km")
    # how differently do two rotations place the equatorial segment?
    sam, afr = F.margins(lats, lons, z, 900, afr_north=12.0, afr_east=24.0)
    la_s, lo_s = F.latlon(sam)
    eq_s = sam[la_s > -5.0]
    MINE_EQ = (60.17, -38.77, 45.44)
    for name, rot in (('Heine et al. 2013', HEINE), ('Moulin et al. 2010', MOULIN), ('my whole-ocean rotation', WHOLE)):
        a = eq_s @ F.rotmat(F.w_of(*MINE_EQ)).T; b = eq_s @ F.rotmat(F.w_of(*rot)).T
        d = F.gc(a, b)
        print(f"  my equatorial rotation against {name}: the same points of South America's equatorial margin land {d.min():.0f} to {d.max():.0f} km apart (median {np.median(d):.0f})")


def signed_km(rs, afr_tree, lats, lons, z, depth):
    """distance from each rotated point to Africa's margin; positive where the point lies on Africa's side of the line (an overlap)"""
    g, i = km(rs, afr_tree)
    la, lo = F.latlon(rs)
    ii = np.clip(np.interp(la, lats, np.arange(len(lats))), 0, len(lats) - 1.001)
    jj = np.clip(np.interp(lo, lons, np.arange(len(lons))), 0, len(lons) - 1.001)
    i0, j0 = ii.astype(int), jj.astype(int)
    fi, fj = ii - i0, jj - j0
    elev = (1 - fi) * ((1 - fj) * z[i0, j0] + fj * z[i0, j0 + 1]) + fi * ((1 - fj) * z[i0 + 1, j0] + fj * z[i0 + 1, j0 + 1])
    return np.where(elev > -depth, g, -g), la, lo


def figdata(path, out):
    """Not sealed. What the corrected figure needs: the refit on Bullard's stretch at 900 m, and where its misfits are."""
    lats, lons, z = F.load(path)
    sam, afr = F.margins(lats, lons, z, 900)
    sam_x, afr_x = F.margins(lats, lons, z, 900, afr_north=12.0, afr_east=24.0)
    sam0, afr0 = F.margins(lats, lons, z, 0, afr_north=12.0, afr_east=24.0)
    la_s, lo_s = F.latlon(sam)
    res = F.best_rotation(sam[la_s < 2.0], afr)
    f, w = res[0]
    plat, plon, ang = F.pole_of(w)
    print(f"not sealed. The refit on Bullard's stretch at 900 m: {ang:.2f} deg about {plat:.2f} N, {plon:.2f} E, misfit {f:.1f} km. Under it, against Africa's margin taken to 12 N and 24 E:")
    tree = cKDTree(afr_x)
    rs = sam @ F.rotmat(w).T
    sg, la, lo = signed_km(rs, tree, lats, lons, z, 900)
    def part(name, m):
        a = sg[m]
        print(f"  {name:46s} {m.sum() * 20:5d} km of margin: overlaps up to {max(a.max(), 0):4.0f} km, gaps up to {max(-a.min(), 0):4.0f} km; median distance {np.median(np.abs(a)):4.0f} km;"
              f" share overlapping {100 * np.mean(a > 0):3.0f}%; lands at {la[m].min():.1f} to {la[m].max():.1f} N, {lo[m].min():.1f} to {lo[m].max():.1f} E")
    part("the Guianas, north of 4 N", la_s > 4)
    part("4 N to 2 N", (la_s <= 4) & (la_s > 2))
    part("northern Brazil, 2 N to 5 S", (la_s <= 2) & (la_s > -5))
    part("the corner of Brazil to 18 S", (la_s <= -5) & (la_s > -18))
    part("18 S to 22 S (the ridge to Trindade)", (la_s <= -18) & (la_s > -22))
    part("22 S to 38 S", (la_s <= -22) & (la_s > -38))
    part("38 S to 45 S (Argentina)", la_s <= -38)
    k = int(np.nanargmax(sg)); dn = float(F.gc(rs[k], F.unit(*F.NIGER)))
    print(f"  largest overlap {sg[k]:.0f} km at {la[k]:.1f} N, {lo[k]:.1f} E, {dn:.0f} km from the Niger delta (South America's {la_s[k]:.1f} N)")
    wal = (la > -21) & (la < -17) & (lo > 9) & (lo < 14)
    if wal.any():
        print(f"  near the Walvis ridge (landing at 17 to 21 S): overlaps up to {max(sg[wal].max(), 0):.0f} km")
    mid = (la_s < 2.0)
    used = np.abs(sg[mid])
    print(f"  South America's margin south of 2 N, each point to Africa's margin: root mean square {np.sqrt((used ** 2).mean()):.0f} km, median {np.median(used):.0f} km")
    np.savez(out, lats=lats[::2], lons=lons[::2], z=z[::2, ::2], w=w, sam900=sam, afr900=afr_x, sam0=sam0, afr0=afr0, cut=2.0)


def depths(path):
    """Not sealed. All six depths on Bullard's stretch (South America's margin south of 2 N)."""
    lats, lons, z = F.load(path)
    FIT9 = (44.0, -30.6, 57.0)
    print("not sealed. All six depths with South America's margin cut to south of 2 N (Africa's as in fit.py):")
    print("  depth   best rotation                    misfit   pole from fit 9   angle from fit 9's   fit 9 on the same stretch   margins (km)")
    for depth in F.DEPTHS:
        sam, afr = F.margins(lats, lons, z, depth)
        la_s, lo_s = F.latlon(sam)
        sam2 = sam[la_s < 2.0]
        res = F.best_rotation(sam2, afr)
        f, w = res[0]
        plat, plon, ang = F.pole_of(w)
        sep = float(F.gc(F.unit(plat, plon), F.unit(FIT9[0], FIT9[1])) / F.R * 180 / np.pi)
        f9 = F.misfit(F.w_of(*FIT9), sam2, afr)
        near = sum(1 for g, _ in res if g < f * 1.02)
        print(f"  {depth:5d}   {ang:6.2f} deg about {plat:6.2f} N {plon:7.2f} E   {f:6.1f} km   {sep:6.2f} deg        {ang - 57.0:+6.2f} deg           {f9:6.1f} km   {len(sam2)*20} and {len(afr)*20}; starts reaching the best: {near} of {len(res)}")


def eqsearch(path):
    """Not sealed. Every end of the search for the equatorial segment alone, and the misfit on the way from my rotation to Heine's."""
    lats, lons, z = F.load(path)
    sam, afr = F.margins(lats, lons, z, 900, afr_north=12.0, afr_east=24.0)
    la_s, lo_s = F.latlon(sam); la_a, lo_a = F.latlon(afr)
    eq_s = sam[la_s > -5.0]
    idx = np.nonzero((lo_a < 3.0) & (la_a > 0.0))[0]
    eq_a = afr[max(np.split(idx, np.nonzero(np.diff(idx) > 1)[0] + 1), key=len)]
    res = F.best_rotation(eq_s, eq_a)
    print("not sealed. All 27 ends of the search for the equatorial segment alone (900 m); 20000 and 30000 mark rotations refused for sliding the margins past each other:")
    for g, x in res:
        pl, po, an = F.pole_of(x)
        d = float(F.gc(F.unit(pl, po), F.unit(HEINE[0], HEINE[1])) / F.R * 180 / np.pi)
        print(f"  {g:8.1f} km   {an:6.2f} deg about {pl:6.2f} N {po:7.2f} E   pole {d:5.1f} deg from Heine's")
    a = res[0][1]; b = F.w_of(*HEINE)
    print("misfit on the equatorial segment along the straight line of rotation vectors from mine (0) to Heine's (1):")
    print("  " + "  ".join(f"{t:.1f}: {F.misfit(a + t * (b - a), eq_s, eq_a):.0f}" for t in np.linspace(0, 1, 11)))


FIT9, FIT2 = (44.0, -30.6, 57.0), (42.9, -30.1, 57.1)                 # Bullard's Table 1: fit 9 (longer stretch, delta and ridge removed), fit 2 (shorter, left in)
REFIT = (43.63, -30.19, 57.08)                                        # ends2.out
LATER = [("Rabinowitz and LaBrecque 1979", (45.5, -32.2, 57.5)),      # as tabulated by Moulin, Aslanian and Unternehr (2010), Table 1
         ("Vink 1982", (47.0, -33.8, 58.0)),
         ("Nuernberg and Mueller 1991, Argentine block", (46.72, -32.67, 56.583)),
         ("Moulin and others 2010, Guyana block", (54.27, -34.98, 50.43)),
         ("Heine and others 2013, against north-west Africa", (50.44, -34.38, 53.40)),
         ("Perez-Diaz and Eagles 2014, 138 Ma", (56.23, -39.28, 59.58))]  # their table prints the longitude unsigned; the text puts the poles in the North Atlantic


def after(path):
    """Not sealed. Checks made after a reader had read the corrections (26 November)."""
    lats, lons, z = F.load(path)
    sam, afr = F.margins(lats, lons, z, 900)
    sam_x, afr_x = F.margins(lats, lons, z, 900, afr_north=12.0, afr_east=24.0)
    la_s, lo_s = F.latlon(sam)
    tree = cKDTree(afr_x)
    rot = lambda r: sam @ F.rotmat(F.w_of(*r)).T
    print("not sealed: made after a reader had read the corrections.")
    # (1) E4 to more digits
    eq_s = sam_x[F.latlon(sam_x)[0] > -5.0]
    la_a, lo_a = F.latlon(afr_x)
    idx = np.nonzero((lo_a < 3.0) & (la_a > 0.0))[0]
    eq_a = afr_x[max(np.split(idx, np.nonzero(np.diff(idx) > 1)[0] + 1), key=len)]
    res = F.best_rotation(eq_s, eq_a)
    eE = res[0][0]; eW = F.misfit(F.w_of(*WHOLE), eq_s, eq_a)
    print(f"(1) E4 to more digits: the equatorial rotation's misfit {eE:.4f} km; my first rotation's on the same stretch {eW:.4f} km, half of which is {eW / 2:.4f}; inside by {eW / 2 - eE:.4f} km")
    # (2) the south: Argentina south of 41 S and south of 38 S, distance to Africa's line (carried on to 24 E)
    print("(2) Argentina's margin, each point to Africa's line: median (least to most), km")
    for name, r in (("my first rotation", WHOLE), ("the refit", REFIT), ("Bullard's fit 9", FIT9), ("Bullard's fit 2", FIT2)):
        row = []
        for cut in (-41.0, -38.0):
            g, i = km(rot(r)[la_s < cut], tree)
            row.append(f"south of {-cut:.0f} S: {np.median(g):4.0f} ({g.min():3.0f} to {g.max():3.0f})")
        print(f"    {name:20s} " + ";  ".join(row))
    # (3) the Guianas in two parts
    west = (la_s > 4.0) & (lo_s < -54.5); east = (la_s > 4.0) & (lo_s >= -54.5)
    print(f"(3) the Guianas' margin north of 4 N, split at 54.5 W: western part {west.sum() * 20} km, eastern part {east.sum() * 20} km. Median distance to Africa's line (taken to 12 N), km:")
    EQ = F.pole_of(res[0][1])
    for name, r in (("the refit", REFIT), ("my first rotation", WHOLE), ("Heine and others 2013", LATER[4][1]), ("Moulin and others 2010, Guyana block", LATER[3][1]), ("my equatorial rotation", EQ)):
        gw, _ = km(rot(r)[west], tree); ge, _ = km(rot(r)[east], tree)
        sg = F.misfit(F.w_of(*r), eq_s, eq_a); ss = F.misfit(F.w_of(*r), sam[la_s < -20.0], afr_x[la_a < 0.0])
        print(f"    {name:38s} western {np.median(gw):4.0f}   eastern {np.median(ge):4.0f}   | misfit on the equatorial stretch {sg:6.1f} km, south of 20 S {ss:7.1f} km")
    for lim, label in ((1.02, "the next end of the equatorial search"), (1.05, "the next end after that")):
        g2, second = [(g, x) for g, x in res if g > res[0][0] * lim][0]
        print(f"    {label} ({g2:.1f} km; {F.pole_of(second)[2]:.1f} deg about {F.pole_of(second)[0]:.1f} N {F.pole_of(second)[1]:.1f} E): south of 20 S {F.misfit(second, sam[la_s < -20.0], afr_x[la_a < 0.0]):.0f} km")
    # (4) how far apart two rotations put the same points of the fitted stretch
    fit = la_s < 2.0
    def apart(a, b):
        d = F.gc(rot(a)[fit], rot(b)[fit]); return f"{d.min():4.0f} to {d.max():4.0f} km (median {np.median(d):4.0f})"
    print("(4) how far apart two rotations put the same points of South America's margin south of 2 N:")
    print(f"    the refit and Bullard's fit 9:   {apart(REFIT, FIT9)}")
    print(f"    the refit and Bullard's fit 2:   {apart(REFIT, FIT2)}")
    print(f"    his fit 9 and his fit 2:         {apart(FIT9, FIT2)}")
    print(f"    my first rotation and his fit 9: {apart(WHOLE, FIT9)}")
    for name, r in LATER:
        print(f"    the refit and {name}: {apart(REFIT, r)}")
    for name, r in LATER:
        print(f"    my first rotation and {name}: {apart(WHOLE, r)}")
    land = (z > 0) & (np.meshgrid(lons, lats)[0] < -34.0)
    LON, LAT = np.meshgrid(lons, lats)
    v = F.unit(LAT[land][::50], LON[land][::50])
    d = F.gc(v @ F.rotmat(F.w_of(*REFIT)).T, v @ F.rotmat(F.w_of(*FIT9)).T)
    print(f"    the refit and Bullard's fit 9 over all the land west of 34 W in the window (South America): {d.min():.0f} to {d.max():.0f} km")
    k2 = int(np.argmin(np.abs(la_s - 2.0)))
    print(f"    where South America's 900 m line crosses 2 N: {lo_s[k2]:.1f} E")
    # (5) where the overlap of northern Brazil is
    sg, la, lo = signed_km(rot(REFIT), tree, lats, lons, z, 900)
    m = (la_s <= 2) & (la_s > -5); k = np.nonzero(m)[0][np.argmax(sg[m])]
    print(f"(5) the largest overlap between 2 N and 5 S under the refit: {sg[k]:.0f} km at South America's {la_s[k]:.1f} N {lo_s[k]:.1f} E, landing at {la[k]:.1f} N {lo[k]:.1f} E, {float(F.gc(rot(REFIT)[k], F.unit(*F.NIGER))):.0f} km from the Niger delta")
    # (6) one step off the other ends of the stretches
    print("(6) one step off (900 m): best rotation, misfit, pole's distance from fit 9 and from fit 2; then how far it puts the points of South America's margin south of 2 N from where his rotations put them")
    def one(label, sam_cut, afr_cut):
        r = F.best_rotation(sam_cut, afr_cut); f, w = r[0]; pl, po, an = F.pole_of(w)
        d9 = float(F.gc(F.unit(pl, po), F.unit(FIT9[0], FIT9[1])) / F.R * 180 / np.pi); d2 = float(F.gc(F.unit(pl, po), F.unit(FIT2[0], FIT2[1])) / F.R * 180 / np.pi)
        k9 = F.gc(rot((pl, po, an))[fit], rot(FIT9)[fit]); k2_ = F.gc(rot((pl, po, an))[fit], rot(FIT2)[fit])
        print(f"    {label:44s} {an:6.2f} deg about {pl:6.2f} N {po:7.2f} E   {f:6.1f} km   {d9:5.2f} deg   {d2:5.2f} deg   | on the ground, from fit 9: {k9.min():3.0f} to {k9.max():3.0f} km; from fit 2: {k2_.min():3.0f} to {k2_.max():3.0f} km")
        return pl, po, an
    one("as sealed (45 S; Africa 8 N to 20 E)", sam[fit], afr)
    for cutn in (4.0, 0.0, -2.0):
        one(f"South America's northern cut at {cutn:.0f} N", sam[la_s < cutn], afr)
    for cut in (-41.0, -38.0):
        one(f"South America's southern end at {-cut:.0f} S", sam[fit & (la_s > cut)], afr)
    for an_, ae_ in ((6.0, 20.0), (10.0, 20.0), (8.0, 18.0), (8.0, 22.0)):
        s2, a2 = F.margins(lats, lons, z, 900, afr_north=an_, afr_east=ae_)
        one(f"Africa's line from {an_:.0f} N round to {ae_:.0f} E", s2[F.latlon(s2)[0] < 2.0], a2)
    # (7) leave out each 500 km of South America's fitted stretch in turn
    idxf = np.nonzero(fit)[0]; blocks = [idxf[i:i + 25] for i in range(0, len(idxf), 25)]
    poles = []
    print(f"(7) leaving out each 500 km of South America's fitted stretch in turn ({len(blocks)} refits):")
    for b in blocks:
        keep = np.ones(len(sam), bool); keep[b] = False; keep &= fit
        r = F.best_rotation(sam[keep], afr); pl, po, an = F.pole_of(r[0][1]); poles.append((pl, po, an, r[0][0], la_s[b].max(), la_s[b].min()))
    P = np.array(poles)
    d0 = np.array([float(F.gc(F.unit(a, b), F.unit(REFIT[0], REFIT[1])) / F.R * 180 / np.pi) for a, b in P[:, :2]])
    d9 = np.array([float(F.gc(F.unit(a, b), F.unit(FIT9[0], FIT9[1])) / F.R * 180 / np.pi) for a, b in P[:, :2]])
    for row, a, b in zip(P, d0, d9):
        print(f"    without {row[4]:6.1f} to {row[5]:6.1f} N: {row[2]:6.2f} deg about {row[0]:6.2f} N {row[1]:7.2f} E, misfit {row[3]:5.1f} km; pole {a:4.2f} deg from the full refit's, {b:4.2f} from fit 9")
    print(f"    the pole moves by up to {d0.max():.2f} deg (median {np.median(d0):.2f}); the angle runs from {P[:, 2].min():.2f} to {P[:, 2].max():.2f}; distance from fit 9 runs from {d9.min():.2f} to {d9.max():.2f} deg")
    w_ = int(np.argmax(d0)); kk = F.gc(rot(tuple(P[w_, :3]))[fit], rot(REFIT)[fit])
    print(f"    on the ground the refit that moves most (without the southernmost block) puts the margin {kk.min():.0f} to {kk.max():.0f} km from the full refit: latitude and angle move together")
    print(f"    the blocks hold {', '.join(str(len(b) * 20) for b in blocks)} km")
    n = len(P); pm = P[:, :3].mean(0)
    jk = np.sqrt((n - 1) / n * ((P[:, :3] - pm) ** 2).sum(0))
    print(f"    jackknife standard errors: pole latitude {jk[0]:.2f} deg, longitude {jk[1]:.2f} deg, angle {jk[2]:.2f} deg (blocks of margin are not independent draws; a rough size only)")


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[2] == 'after':
        after(sys.argv[1])
    elif len(sys.argv) > 2 and sys.argv[2] == 'depths':
        depths(sys.argv[1])
    elif len(sys.argv) > 2 and sys.argv[2] == 'eqsearch':
        eqsearch(sys.argv[1])
    elif len(sys.argv) > 3 and sys.argv[2] == 'figdata':
        figdata(sys.argv[1], sys.argv[3])
    elif len(sys.argv) > 2 and sys.argv[2] == 'sweep':
        sweep(sys.argv[1])
    elif len(sys.argv) > 2 and sys.argv[2] == 'addendum':
        like_for_like(sys.argv[1])
    else:
        main(sys.argv[1])
