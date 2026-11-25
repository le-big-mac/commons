"""after.py: what was looked at after the sheet was scored. Nothing here was sealed.   python -I after.py PLATE.jpg
A  what each fault of the rods costs: the patch (as a fraction of the lens's opening) at 2, 5, 10 and 20 times
B  a showman's remedy: one adjustment made by eye at one size of image; what is left at the others
C  the plate: are its lens, slider and screen in focus as drawn? and a lantern built to the plate's own proportions
D  Brewster's bending: laths and iron rods, under their own weight and under a push on the lens
E  the rods' size: how high the joint K stands, and the least and greatest image, for rods of several lengths
F  the cam and the shade at other ranges
G to L were asked for by the referee's report:
G  one rod wrong in its length, by 1 part in 1,000 and in 10,000
H  how KL stands when it pushes the lens: its angle, its thrust, and the friction that locks it; for rods of several lengths
I  bending again: long rods, and the push taken at the lens
J  the cam in Brewster's own sense (a spring holds the lens out, the cam presses it in)
K  a lantern built to the plate by each of its two readings
L  on the plate, how far L lies from the line of I and N"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lantern as L, plate
MS = (2.0, 5.0, 10.0, 20.0); A = 11.0
def patch(r, m):
    D = L.D_of_m(m, r.f); s = r.lens(D); return None if s is None else L.blur(D, s, r.f)
def row(lab, r): print('   %-58s %s' % (lab, '   '.join('jams   ' if patch(r, m) is None else '%.5f' % patch(r, m) for m in MS)))
def main(path):
    print('A  the patch at 2, 5, 10 and 20 times (rods of 11 f; each fault alone)')
    print('   %-58s %s' % ('', '   '.join('%-7s' % ('%g x' % m) for m in MS)))
    row('all as it should be', L.Rods(a=A))
    for eps in (0.01, -0.01, 0.05): row('IK^2 - KL^2 = %.2f f^2' % (1 + eps), L.Rods(a=A, b=math.sqrt(A * A - (1 + eps))))
    for h in (0.01, -0.01, 0.05, 0.1): row('N %.2f f %s the line of I and L' % (abs(h), 'above' if h > 0 else 'below'), L.Rods(a=A, yN=h))
    for d in (0.001, -0.001): row('KN %s than IK by 1 in 1,000' % ('longer' if d > 0 else 'shorter'), L.Rods(a=A, a2=A * (1 + d)))
    for d in (0.01, -0.01): row('I %.2f f too %s the slider (p = %.2f f)' % (abs(d), 'far from' if d > 0 else 'near', 2 + d), L.Rods(a=A, p=2 + d))
    for d in (0.01, -0.01): row('L %.2f f too %s the lens (q = %.2f f)' % (abs(d), 'far from' if d > 0 else 'near', 1 + d), L.Rods(a=A, q=1 + d))
    for d in (0.01, 0.05): row('N %.2f f beyond the screen' % d, L.Rods(a=A, e=d))
    for d in (0.02, 0.05): row('L %.2f f above the line of I and N' % d, L.Rods(a=A, yL=d))
    print('   the lens set once and left (no rods), sharp at 5 times:    ' + '   '.join('%.5f' % L.blur(L.D_of_m(m), L.focus(L.D_of_m(5.0))[0]) for m in MS))
    print()
    print('B  a showman who does not know f^2 = IK^2 - KL^2 but slides L along its bar until the image is sharp at one size, and leaves it')
    for lab, kw in (('KL too short: IK^2 - KL^2 = 1.10 f^2', dict(b=math.sqrt(A * A - 1.10))), ('KL too long: 0.90 f^2', dict(b=math.sqrt(A * A - 0.90))), ('I at 1.9 f, as on the plate', dict(p=1.9)), ('N 0.02 f too high', dict(yN=0.02))):
        for m_set in (3.0, 10.0):
            D = L.D_of_m(m_set); lo, hi = 0.5, 1.5
            for _ in range(80):
                q = (lo + hi) / 2; r = L.Rods(a=A, q=q, **kw); s = r.lens(D)
                if s is None or s > L.focus(D)[0]: lo = q      # the lens too far out: L must sit further beyond it
                else: hi = q
            r = L.Rods(a=A, q=(lo + hi) / 2, **kw); row('%s; L set sharp at %g times (q = %.4f f)' % (lab, m_set, (lo + hi) / 2), r)
    print()
    pm = plate.measure(path); F = pm['figures']; f = F['f_by_L'][0]; P = plate.PLACES
    s = (P['F'][0] - P['E'][0]); si = f * s / (s - f)
    print('C  the plate: with the focal length that L marks (%.1f pixels), a slider %.0f pixels before the lens is sharp %.1f pixels beyond it, at x = %.1f; the dark bar\'s near face is at %d, its far face at %d' % (f, s, si, P['F'][0] + si, P['Gleft'][0], P['Gright'][0]))
    print('   the focal length three ways: by L %.1f (%.1f); by half of I\'s distance from the slider %.1f (%.1f); by the lens equation with the near face %.1f (%.1f), with the far face %.1f (%.1f)' % (F['f_by_L'] + F['f_by_I'] + F['f_by_lens_left'] + F['f_by_lens_right']))
    print('   x x\' as drawn, to the near face: %.0f x %.0f = %.0f; f^2 = %.0f. IL x LN as drawn: %.0f x %.0f = %.0f; IK^2 - KL^2 = %.0f' % (F['x_drawn'][0], F['xprime_left'][0], F['x_drawn'][0] * F['xprime_left'][0], f * f, F['IL'][0], F['LN'][0], F['IL'][0] * F['LN'][0], F['c'][0] ** 2))
    a = F['IK'][0] / f; b = F['KL'][0] / f; a2 = F['KN'][0] / f; p = (P['I'][0] - P['E'][0]) / f; e_far = (P['Gright'][0] - P['Gleft'][0]) / f
    for lab, r in (('a lantern built to the plate, the bar\'s near face taken for the screen (so N is behind it)', L.Rods(a=a, a2=a2, b=b, p=p, e=e_far)), ('the same with N moved to the near face', L.Rods(a=a, a2=a2, b=b, p=p)), ('the plate\'s rods with KL recut to the third condition and N on the near face', L.Rods(a=a, a2=a, p=2.0))):
        print('   %s (rods %.2f f, %.2f f, %.2f f; reach %.1f f):' % (lab, a, a2, r.b, r.reach()) + '  ' + '; '.join('%g times: %s' % (m, 'jams or out of reach' if patch(r, m) is None else '%.3f' % patch(r, m)) for m in (1.5, 2.0, 3.0, 3.16, 4.0)))
    print('   the plate itself shows the image at %.2f times the slider' % (si / s))
    print()
    print('D  bending. f = 200 mm, rods of 11 f (2.2 m), ten times; the patch as a fraction of the opening')
    fm = 0.2; am = A * fm; bm = math.sqrt(am * am - fm * fm); D = L.D_of_m(10.0); r0 = L.Rods(a=A); K = r0.K(D); s0 = r0.lens(D); cosI = (K[0] - 2.0) / A; cosL = (K[0] - (s0 + 1.0)) / (bm / fm)
    for lab, EI, w in (('deal lath 20 mm square', 10e9 * 0.02 ** 4 / 12, 600 * 9.81 * 0.02 ** 2), ('deal lath 10 mm square', 10e9 * 0.01 ** 4 / 12, 600 * 9.81 * 0.01 ** 2), ('iron rod 6 mm round', 190e9 * math.pi * 0.006 ** 4 / 64, 7850 * 9.81 * math.pi * 0.003 ** 2), ('iron wire 3 mm round', 190e9 * math.pi * 0.003 ** 4 / 64, 7850 * 9.81 * math.pi * 0.0015 ** 2)):
        Pcr = math.pi ** 2 * EI / bm ** 2; out = []
        for push in (0.0, 2.0, 5.0):
            if push >= Pcr: out.append('push %g N: buckles' % push); continue
            da = L.sag_shortening(am, w * cosI, EI); db = L.sag_shortening(bm, w * cosL, EI, P=push); r = L.Rods(a=(am - da) / fm, b=(bm - db) / fm); s = r.lens(D); out.append('push %g N: %s' % (push, 'jams' if s is None else '%.5f' % L.blur(D, s)))
        mid = 5 * w * cosL * bm ** 4 / (384 * EI); print('   %-24s KL sags %.1f mm in the middle, buckles at %.0f N;  %s' % (lab, mid * 1000, Pcr, ';  '.join(out)))
    print()
    print('E  the size of the thing: rods of a focal lengths; the joint K at its highest (image as small as the slider); the greatest image')
    for a_ in (6.0, 11.0, 16.0, 26.0):
        r = L.Rods(a=a_); m = 1.0
        while r.lens(L.D_of_m(m + 0.01)) is not None: m += 0.01
        print('   rods %4.0f f: K stands %.2f f above the pivots at its highest; greatest image %.1f times, the screen then %.1f f from the slider' % (a_, r.K(4.0)[1], m, L.D_of_m(m)))
    print()
    print('F  the cam (one turn of 300 degrees, pressure angle 30 degrees) and the shade at other ranges')
    for lo in (1.2, 1.5, 2.0, 3.0, 5.0): c = L.cam(lo, 20.0); print('   cam from %g to 20 times: least radius %.2f f, largest %.2f f' % (lo, c[0], c[1]))
    for lo, hi in ((1.5, 4.0), (1.5, 10.0), (2.0, 20.0), (1.0, 20.0)): x0, fac, bare = L.shade(lo, hi); print('   shade from %g to %g times: within a factor %.2f either way (x0 = %.3f f); with no shade %.2f' % (lo, hi, fac, x0, bare))
def plate_builds(P, sizes, draws=2000, seed=1806, sd=1.5):
    """a lantern built to the plate, by each reading of the screen's face, with every place moved by the reading error: the patches, draw by draw (2.0 for jammed, out of reach, or worse)"""
    import numpy as np
    rng = np.random.default_rng(seed); acc = {'far': {m: [] for m in sizes}, 'near': {m: [] for m in sizes}}
    for _ in range(draws):
        Q = {k: (v[0] + rng.normal(0, sd), v[1] + rng.normal(0, sd)) for k, v in P.items()}; d = lambda x, y: math.hypot(Q[x][0] - Q[y][0], Q[x][1] - Q[y][1]); f_ = Q['L'][0] - Q['F'][0]
        if f_ <= 0: continue
        for key, v_ in (('far', Q['Gright'][0] - Q['F'][0]), ('near', Q['Gleft'][0] - Q['F'][0])):
            if v_ <= f_: continue
            u_ = 1 / (1 / f_ - 1 / v_); r_ = L.Rods(a=d('I', 'K') / f_, a2=d('K', 'N') / f_, b=d('K', 'L') / f_, p=(Q['I'][0] - (Q['F'][0] - u_)) / f_, e=(Q['N'][0] - Q['F'][0] - v_) / f_)
            for m in sizes: c_ = patch(r_, m); acc[key][m].append(2.0 if c_ is None or c_ > 2.0 else c_)
    return acc
def more(path):
    print()
    print('G  one rod wrong in its length (rods of 11 f; the patch at 2, 5, 10 and 20 times)')
    b0 = math.sqrt(A * A - 1)
    print('   %-58s %s' % ('the lens\'s focal length 1 part in 100 longer than the rods were made for', '   '.join('%.5f' % L.blur(L.D_of_m(m, 1.01), L.Rods(a=A).lens(L.D_of_m(m, 1.01)), 1.01) for m in MS)))
    row('KL alone longer by 1 part in 1,000', L.Rods(a=A, b=b0 * 1.001)); row('KL alone longer by 1 part in 10,000', L.Rods(a=A, b=b0 * 1.0001)); row('IK alone longer by 1 part in 1,000', L.Rods(a=A * 1.001, a2=A, b=b0)); row('IK and KN both longer by 1 part in 1,000, KL right', L.Rods(a=A * 1.001, a2=A * 1.001, b=b0)); row('all three longer by 1 part in 1,000', L.Rods(a=A * 1.001, a2=A * 1.001, b=b0 * 1.001))
    print('   IK^2 - KL^2 one part in 100 out is KL out by %.6f f, 1 part in %.0f of its length (%.2f mm in %.2f m with a lens of 200 mm)' % (0.01 / (2 * b0), b0 / (0.01 / (2 * b0)), 200 * 0.01 / (2 * b0), b0 * 0.2))
    print()
    print('H  KL when it pushes the lens: its angle with the lens\'s bar; the thrust along it for a unit push on the lens; the friction of slider on bar that locks it')
    for a_ in (3.73, 6.0, 11.0, 26.0):
        r = L.Rods(a=a_); out = []
        for m in (2.0, 5.0, 10.0, 20.0):
            t = r.thrust(L.D_of_m(m)); out.append('%g x: out of reach' % m if t is None else '%g x: %.0f deg, %.1f times, %.2f' % ((m,) + t))
        m = 1.01
        while r.thrust(L.D_of_m(m)) is not None and r.thrust(L.D_of_m(m))[0] > 30.0: m += 0.01
        print('   rods %5.2f f:  %s;  KL within 30 degrees of the bar (the cam\'s rule: the angle between the push and the motion) only above %.1f times' % (a_, ';  '.join(out), m))
    print()
    print('I  bending again: deal laths, f = 200 mm; a push of 5 N at the lens is 5 / cos of KL\'s angle along KL')
    fm = 0.2
    for a_, side in ((11.0, 0.02), (11.0, 0.01), (26.0, 0.02), (26.0, 0.03)):
        am = a_ * fm; bm = math.sqrt(am * am - fm * fm); EI = 10e9 * side ** 4 / 12; w = 600 * 9.81 * side ** 2; Pcr = math.pi ** 2 * EI / bm ** 2; r0 = L.Rods(a=a_); out = []
        for m in (5.0, 10.0, 25.0, 50.0):
            D = L.D_of_m(m); s0 = r0.lens(D)
            if s0 is None: out.append('%g x: out of reach' % m); continue
            K = r0.K(D); cosI = (K[0] - 2.0) / a_; cosL = (K[0] - (s0 + 1.0)) / (bm / fm); push = 5.0 / cosL
            if push >= Pcr: out.append('%g x: KL buckles (%.0f N along it)' % (m, push)); continue
            da = L.sag_shortening(am, w * cosI, EI); db = L.sag_shortening(bm, w * cosL, EI, P=push); s = L.Rods(a=(am - da) / fm, b=(bm - db) / fm).lens(D); out.append('%g x: %s (%.0f N along KL; it sags %.0f mm)' % (m, 'jams' if s is None else '%.4f' % L.blur(D, s), push, 1000 * 5 * w * cosL * bm ** 4 / (384 * EI) / (1 - push / Pcr)))
        print('   rods %.1f m of lath %d mm square (lying level it would sag %.0f mm; buckles at %.0f N):  %s' % (am, side * 1000, 1000 * 5 * w * am ** 4 / (384 * EI), Pcr, ';  '.join(out)))
    print()
    print('J  the cam in Brewster\'s sense: least and largest radius, one turn of 300 degrees to 20 times, pressure angle 30 degrees')
    for lo in (1.2, 1.5, 2.0, 3.0, 5.0): c = L.cam(lo, 20.0, press=True); c0 = L.cam(lo, 20.0); print('   from %g times: %.2f f to %.2f f (in the other sense %.2f to %.2f); the box rolls %.2f f, so a wheel turning once with the cam would be %.1f f round' % (lo, c[0], c[1], c0[0], c0[1], L.D_of_m(20.0) - L.D_of_m(lo), (L.D_of_m(20.0) - L.D_of_m(lo)) * 360 / 300.0))
    print('   a cam of n turns of 300 degrees each is 1/n the size')
    print()
    pm = plate.measure(path); F = pm['figures']; f = F['f_by_L'][0]; P = plate.PLACES; vN, vF = P['Gleft'][0] - P['F'][0], P['Gright'][0] - P['F'][0]; uN, uF = 1 / (1 / f - 1 / vN), 1 / (1 / f - 1 / vF); a = F['IK'][0] / f; a2 = F['KN'][0] / f; b = F['KL'][0] / f
    print('K  a lantern built to the plate (rods %.2f f, %.2f f, %.2f f), the patch at several sizes' % (a, a2, b))
    for lab, r in (('the far face the screen (slider %.0f pixels before the lens; I %.2f f before it; N at the screen)' % (uF, (P['I'][0] - (P['F'][0] - uF)) / f), L.Rods(a=a, a2=a2, b=b, p=(P['I'][0] - (P['F'][0] - uF)) / f, e=0.0)),
                   ('the near face the screen (slider %.0f before the lens; I %.2f f before it; N %.2f f behind the screen)' % (uN, (P['I'][0] - (P['F'][0] - uN)) / f, (vF - vN) / f), L.Rods(a=a, a2=a2, b=b, p=(P['I'][0] - (P['F'][0] - uN)) / f, e=(vF - vN) / f))):
        print('   %s:' % lab); print('      ' + ';  '.join('%g x: %s' % (m, 'out of reach' if patch(r, m) is None else '%.3f' % patch(r, m)) for m in (2.0, 3.0, 3.16, 3.5, 4.0, 4.08, 5.0, 6.0)))
    import numpy as np
    sizes = (2.0, 3.0, 3.5, 4.0, 5.0, 6.0); acc = plate_builds(P, sizes)
    print('   the same with the reading error carried (2,000 draws, each place moved 1.5 pixels each way; the middle and the two-thirds range; 2.00 stands for jammed, out of reach, or worse):')
    for key, lab in (('far', 'the far face the screen'), ('near', 'the near face the screen')): print('      %-26s %s' % (lab + ':', ';  '.join('%g x: %.2f (%.2f to %.2f)' % ((m,) + tuple(np.percentile(acc[key][m], [50, 16, 84]))) for m in sizes)))
    print()
    print('L  on the plate L lies %+.2f (%.2f) focal lengths from the line of I and N (+ is below); a fiftieth of a focal length is %.1f pixels' % (F['L_off_line_IN_over_f'] + (0.02 * f,)))
if __name__ == '__main__': main(sys.argv[1]); more(sys.argv[1])
