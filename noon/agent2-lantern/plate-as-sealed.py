"""plate.py: Young's own drawing of the arrangement (Lectures, 1807, Plate XXVIII, Fig. 401; the scan at the Internet Archive,
lecturescourseof01younrich, leaf 847, 2340 x 3086 pixels) measured.   python -I plate.py PLATE.jpg
The places of the pivots, of the lens and of the slider were read by me from enlarged pieces of the scan with a grid laid on them
(plate-crops/, made by this script with the places marked), to about a pixel and a half each way; every figure below carries what
that uncertainty does to it (20,000 draws, each place moved by a normal error of 1.5 pixels each way). The ground line under the
wheels is found by the script: the darkest row in six columns clear of the wheels, and a straight line through them."""
import math, os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
PLACES = {'I': (1022, 981), 'L': (1054, 982), 'K': (1209, 753), 'N': (1376, 990),      # the four pivots
          'F': (975, 916), 'E': (871, 916),                                               # the middle of the lens, the painted slider (edge-on)
          'Gleft': (1306, 916), 'Gright': (1376, 916)}                                    # the two faces of the dark bar that stands for the screen
GROUND_COLUMNS = (630, 780, 1000, 1100, 1200, 1290); BAND = (1085, 1125)
def ground(a):
    pts = [(x, BAND[0] + int(a[BAND[0]:BAND[1], x - 3:x + 4].mean(axis=1).argmin())) for x in GROUND_COLUMNS]; xs = np.array([p[0] for p in pts], float); ys = np.array([p[1] for p in pts], float)
    slope, icpt = np.polyfit(xs, ys, 1); return float(slope), float(icpt), pts, float(np.abs(ys - (slope * xs + icpt)).max())
def figures(P, slope):
    d = lambda a, b: math.hypot(P[a][0] - P[b][0], P[a][1] - P[b][1]); IK, KN, KL = d('I', 'K'), d('K', 'N'), d('K', 'L'); f_L = P['L'][0] - P['F'][0]; f_I = (P['I'][0] - P['E'][0]) / 2.0; s = P['F'][0] - P['E'][0]
    lens = lambda sp: 1 / (1 / s + 1 / sp); c2 = IK ** 2 - KL ** 2
    drop = (P['N'][1] - P['I'][1]) - slope * (P['N'][0] - P['I'][0])      # how far N lies below the line through I parallel to the ground (pixels, + is below)
    return {'KN_over_IK': KN / IK, 'IK': IK, 'KN': KN, 'KL': KL, 'IL': P['L'][0] - P['I'][0], 'LN': P['N'][0] - P['L'][0], 'f_by_L': f_L, 'f_by_I': f_I, 'f_by_lens_left': lens(P['Gleft'][0] - P['F'][0]), 'f_by_lens_right': lens(P['Gright'][0] - P['F'][0]),
            'c': math.sqrt(max(c2, 0)), 'c_over_f_by_L': math.sqrt(max(c2, 0)) / f_L, 'root_IL_LN': math.sqrt(max((P['L'][0] - P['I'][0]) * (P['N'][0] - P['L'][0]), 0)), 'N_drop_over_f': drop / f_L,
            'x_drawn': s - f_L, 'xprime_left': P['Gleft'][0] - P['F'][0] - f_L, 'xprime_right': P['Gright'][0] - P['F'][0] - f_L}
def measure(path, draws=20000, sd=1.5, seed=1807):
    from PIL import Image
    a = np.asarray(Image.open(path).convert('L'), float); slope, icpt, pts, off = ground(a); base = figures(PLACES, slope); rng = np.random.default_rng(seed); acc = {k: [] for k in base}
    for _ in range(draws):
        P = {k: (v[0] + rng.normal(0, sd), v[1] + rng.normal(0, sd)) for k, v in PLACES.items()}; fg = figures(P, slope)
        for k in fg: acc[k].append(fg[k])
    return {'ground_slope': slope, 'ground_points': pts, 'ground_worst_off': off, 'figures': {k: (base[k], float(np.std(acc[k]))) for k in base}}
def crops(path):
    from PIL import Image, ImageDraw
    im = Image.open(path).convert('RGB'); os.makedirs(os.path.join(HERE, 'plate-crops'), exist_ok=True)
    for name, (x0, y0, x1, y1), k in (('IL', (995, 935, 1085, 1025), 6), ('K', (1170, 718, 1250, 798), 6), ('N', (1332, 950, 1412, 1030), 6), ('EF', (850, 850, 1000, 950), 5), ('whole', (590, 720, 1400, 1130), 2)):
        c = im.crop((x0, y0, x1, y1)).resize(((x1 - x0) * k, (y1 - y0) * k), Image.LANCZOS); d = ImageDraw.Draw(c)
        if name != 'whole':
            for t in range(0, x1 - x0 + 1, 10): d.line([(t * k, 0), (t * k, (y1 - y0) * k)], fill=(120, 170, 255), width=1); d.text((t * k + 2, 2), str(x0 + t), fill=(0, 60, 200))
            for t in range(0, y1 - y0 + 1, 10): d.line([(0, t * k), ((x1 - x0) * k, t * k)], fill=(120, 170, 255), width=1); d.text((2, t * k + 2), str(y0 + t), fill=(0, 60, 200))
        for lab, (px, py) in PLACES.items():
            if x0 <= px <= x1 and y0 <= py <= y1: X, Y = (px - x0) * k, (py - y0) * k; d.line([(X - 9, Y), (X + 9, Y)], fill=(235, 104, 52), width=2); d.line([(X, Y - 9), (X, Y + 9)], fill=(235, 104, 52), width=2); d.text((X + 6, Y + 6), lab, fill=(235, 104, 52))
        c.save(os.path.join(HERE, 'plate-crops', name + '.png'))
if __name__ == '__main__':
    path = sys.argv[1]; crops(path); m = measure(path); json.dump(m, open(os.path.join(HERE, 'plate.json'), 'w'), indent=1); F = m['figures']
    print('the ground line: slope %.4f (the darkest rows: %s; the furthest from the line %.1f pixels)' % (m['ground_slope'], ', '.join('%d,%d' % p for p in m['ground_points']), m['ground_worst_off']))
    for k in F: print('   %-18s %9.3f  (%.3f)' % (k, F[k][0], F[k][1]))
