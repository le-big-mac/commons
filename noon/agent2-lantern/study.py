"""study.py: the sheet (expectations.md) computed and judged by its bands, ends included.   python -I study.py PLATE.jpg
Nothing here is random but the plate's uncertainties (seeded). Writes study.json."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lantern as L, plate
A_RODS = 11.0
def compute(path):
    R = {}; pm = plate.measure(path); F = pm['figures']
    R['P1'] = F['KN_over_IK']; R['P2'] = F['c_over_f_by_L']; R['P3'] = F['N_drop_over_f']
    b_wrong = math.sqrt(A_RODS ** 2 - 1.01); r = L.Rods(a=A_RODS, b=b_wrong); D = L.D_of_m(10.0); R['T1'] = (L.blur(D, r.lens(D)), 0.0)
    r = L.Rods(a=A_RODS, yN=0.1); D = L.D_of_m(10.0); R['T2'] = (L.blur(D, r.lens(D)), 0.0)
    m = 20.0
    while m > 1.0 and r.lens(L.D_of_m(m)) is not None: m -= 0.001
    R['T2b'] = (m + 0.001, 0.0)
    r = L.Rods(a=A_RODS, a2=A_RODS * 1.001); D = L.D_of_m(2.0); R['T3'] = (L.blur(D, r.lens(D)), 0.0)
    R['C1'] = L.cam(2.0, 20.0); R['C2'] = L.cam(1.2, 20.0)
    R['S1'] = L.shade(1.5, 4.0); R['S2'] = L.shade(1.5, 10.0)
    # B1: a deal lath 20 mm square (E = 10 GPa, 600 kg/m^3), f = 200 mm, rods of 11 f, the image ten times the slider: what the rods' own sag does
    f = 0.2; a = A_RODS * f; b = math.sqrt(a * a - f * f); EI = 10e9 * 0.02 ** 4 / 12.0; w = 600 * 9.81 * 0.02 ** 2; D = L.D_of_m(10.0); r0 = L.Rods(a=A_RODS); K = r0.K(D); s = r0.lens(D)
    cosI = (K[0] - 2.0) / A_RODS; cosL = (K[0] - (s + 1.0)) / (b / f); da = L.sag_shortening(a, w * cosI, EI); db = L.sag_shortening(b, w * cosL, EI)
    r = L.Rods(a=(a - da) / f, a2=(a - da) / f, b=(b - db) / f); R['B1'] = (L.blur(D, r.lens(D)), da * 1000, db * 1000)
    return R, pm
LINES = [('P1', 0.85, 'on the plate, KN over IK is between 0.96 and 1.00', lambda R: 0.96 <= R['P1'][0] <= 1.00, lambda R: '%.3f (%.3f)' % R['P1']),
         ('P2', 0.80, 'on the plate, the root of IK^2 - KL^2 over the focal length as drawn (L\'s distance past the lens) is between 1.2 and 1.4', lambda R: 1.2 <= R['P2'][0] <= 1.4, lambda R: '%.3f (%.3f)' % R['P2']),
         ('P3', 0.75, 'on the plate, N lies within 0.05 of the drawn focal length of the line through I parallel to the ground', lambda R: abs(R['P3'][0]) <= 0.05, lambda R: '%+.3f (%.3f)' % R['P3']),
         ('T1', 0.85, 'KL cut so that IK^2 - KL^2 is 1.01 f^2: the patch at ten times is between 0.0085 and 0.0095 of the lens\'s opening', lambda R: 0.0085 <= R['T1'][0] <= 0.0095, lambda R: '%.5f' % R['T1'][0]),
         ('T2', 0.80, 'N a tenth of a focal length above the line of I and L: the patch at ten times is between 0.014 and 0.022 of the opening', lambda R: 0.014 <= R['T2'][0] <= 0.022, lambda R: '%.5f' % R['T2'][0]),
         ('T2b', 0.80, 'and with N so raised the rods jam before the image is as small as the slider: the least magnification they reach is between 2.1 and 2.7', lambda R: 2.1 <= R['T2b'][0] <= 2.7, lambda R: '%.3f' % R['T2b'][0]),
         ('T3', 0.80, 'KN longer than IK by 1 part in 1,000: the patch at twice is between 0.030 and 0.040 of the opening', lambda R: 0.030 <= R['T3'][0] <= 0.040, lambda R: '%.5f' % R['T3'][0]),
         ('C1', 0.85, 'a cam of one 300-degree turn from 2 to 20 times, pressure angle 30 degrees: its largest radius is between 1.8 and 2.1 focal lengths', lambda R: 1.8 <= R['C1'][1] <= 2.1, lambda R: '%.3f (least radius %.3f; the limit is met at %.2f times)' % (R['C1'][1], R['C1'][0], R['C1'][2])),
         ('C2', 0.80, 'the same cam from 1.2 times: its largest radius is between 12 and 15 focal lengths', lambda R: 12 <= R['C2'][1] <= 15, lambda R: '%.3f (least radius %.3f; the limit is met at %.2f times)' % (R['C2'][1], R['C2'][0], R['C2'][2])),
         ('S1', 0.70, 'the falling shade, fitted best, from 1.5 to 4 times: the brightness stays within a factor between 1.10 and 1.30 either way', lambda R: 1.10 <= R['S1'][1] <= 1.30, lambda R: '%.3f (with no shade %.2f)' % (R['S1'][1], R['S1'][2])),
         ('S2', 0.70, 'the same from 1.5 to 10 times: within a factor between 1.6 and 2.2 either way', lambda R: 1.6 <= R['S2'][1] <= 2.2, lambda R: '%.3f (with no shade %.2f)' % (R['S2'][1], R['S2'][2])),
         ('B1', 0.80, 'deal laths 20 mm square, f = 200 mm, rods of 11 f, ten times: the rods\' own sag makes a patch below 0.001 of the opening', lambda R: R['B1'][0] <= 0.001, lambda R: '%.6f (IK nearer its pins by %.4f mm, KL by %.4f mm)' % R['B1'])]
if __name__ == '__main__':
    R, pm = compute(sys.argv[1]); held = failed = 0; brier = 0.0; out = {'lines': {}}
    for tag, odds, what, ok, show in LINES:
        v = bool(ok(R)); held += v; failed += (not v); brier += (odds - (1.0 if v else 0.0)) ** 2; print('%-3s %-7s (odds %.2f)  %s: %s' % (tag, 'HELD' if v else 'FAILED', odds, what, show(R))); out['lines'][tag] = {'verdict': 'held' if v else 'failed', 'odds': odds, 'detail': show(R)}
    print(); print('%d held, %d failed. Brier score of the odds %.3f.' % (held, failed, brier / len(LINES))); out['held'] = held; out['failed'] = failed; out['brier'] = brier / len(LINES)
    json.dump(out, open(os.path.join(HERE, 'study.json'), 'w'), indent=1)
