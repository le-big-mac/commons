# mutants.py -- can the tests of core.js fail?  Copies of core.js with one thing broken, each run through test-core.js.
#   python -I mutants.py > mutants.out      (the list was rewritten after the referee's reading, with the core)
import subprocess, os, re
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n), encoding='utf-8').read()
core = rd('core.js'); test = rd('test-core.js')
M = [
 ('speed-of-sound', "sound travels at 300 m/s", "var C = 343;", "var C = 300;"),
 ('pulse-length', "the pulse is 4 ms long", "var T = 0.005;", "var T = 0.004;"),
 ('inverse-square', "the pulses weaken as one over the distance squared", "var amp = (l / rm) * shade(", "var amp = (l / rm / rm) * shade("),
 ('hump-upside-down', "the humps are upside down", "p[s] += b * (qh - ql);", "p[s] -= b * (qh - ql);"),
 ('hump-shape', "the hump's integral is wrong at its lower end", "ql = lo <= 0 ? 0 : lo >= 1 ? 1 / 6 : lo * lo * (0.5 - lo / 3);", "ql = lo <= 0 ? 0 : lo >= 1 ? 1 / 6 : lo * lo * (0.5 - lo / 4);"),
 ('hump-not-averaged', "a hump is averaged over three samples' time, not one", "var half = 0.5 / (FS * T);", "var half = 1.5 / (FS * T);"),
 ('both-ends-same-sign', "the two ends of a piece are given the same sign", "B[k] += g; B[k + 1] -= g;", "B[k] += g; B[k + 1] += g;"),
 ('no-foot-cut', "a piece is not cut where the listener's perpendicular meets it", "stops = foot > 1e-9 && foot < 1 - 1e-9 ? [0, foot, 1] : [0, 1];", "stops = [0, 1];"),
 ('no-fine-cut', "pieces are not cut finer close in", "var parts = Math.min(64, Math.ceil(seg / Math.sqrt(0.016 * Math.max(1, rn))));", "var parts = 1;"),
 ('first-arrival', "the sound starts when the first corner of the channel arrives, not the nearest", "var t0 = d.nearest / C - LEAD, len = Math.ceil(((d.farthest - d.nearest) / C + T + LEAD) * FS) + 2 + Math.ceil(0.02 * FS);\n    var p = new Float64Array(len), B", "var t0 = d.r[0] / C - LEAD, len = Math.ceil(((d.farthest - d.nearest) / C + T + LEAD) * FS) + 2 + Math.ceil(0.02 * FS);\n    var p = new Float64Array(len), B"),
 ('reported-first', "the first sound is reported a pulse length late", "inear: d.inear, ifar: d.ifar, first: d.nearest / C,", "inear: d.inear, ifar: d.ifar, first: d.nearest / C + T,"),
 ('nearest-is-first-point', "the nearest point is taken to be the first point", "if (r[i] < lo) { lo = r[i]; ilo = i; }", "if (i === 0) { lo = r[i]; ilo = i; }"),
 ('blur-loses', "the blur divides by too much and loses pressure", "dens = v / (2 * h);", "dens = v / (2.2 * h);"),
 ('blur-with-distance', "the blur grows as the distance, not its square root", "sd = air * Math.sqrt(Math.max(0, C * t) / 1000), h = sd * FS;", "sd = air * (Math.max(0, C * t) / 1000), h = sd * FS;"),
 ('blur-two-passes', "two running means, not three", "for (var pass = 0; pass < 3; pass++) {", "for (var pass = 0; pass < 2; pass++) {"),
 ('no-shadow', "the bending of sound hides nothing", "if (!(bend > 0)) return 1;", "return 1;"),
 ('shadow-twice-as-high', "the shadow is twice as high", "var hs = dx * dx / (2 * bend);", "var hs = dx * dx / bend;"),
 ('shadow-black', "the shadow is made black, not eased", "return u * u * (3 - 2 * u);", "return 0;"),
 ('shadow-not-in-sum', "the shadow is worked out but left out of the sum", "var amp = (l / rm) * shade(Math.abs(0.5 * (X[k] + X[k + 1]) - L[0]), 0.5 * (Z[k] + Z[k + 1]) - L[1], bend);", "var amp = (l / rm);"),
 ('hidden-not-told', "the page is not told which points are hidden", "hidden[q] = shade(Math.abs(pts[q][0] - L[0]), pts[q][1] - L[1], bend);", "hidden[q] = 1;"),
 ('bend-eighty', "rays curve on 80 km", "var BEND = 55000;", "var BEND = 80000;"),
 ('kink-thirty', "the made-up strokes turn 30 degrees a piece", "var KINK = 16;", "var KINK = 30;"),
 ('no-memory', "each piece's turn forgets the last", "var keep = 0.85,", "var keep = 0.0,"),
 ('not-pinned', "the crooked stroke is not brought back to its ends", "if (d < 1e-9) return p;\n    var a =", "if (d < 1e-9) return p;\n    return out;\n    var a ="),
 ('cloud-at-four', "the made-up strokes start 4 km up", "var top = opts.top === undefined ? 5000 : opts.top,", "var top = opts.top === undefined ? 4000 : opts.top,"),
 ('resample-step', "pieces of 5 m where 3 are asked for", "need = step;\n      }", "need = step + 2;\n      }"),
 ('arc-chords', "the bow's points are a little inside its circle", "pts.push([cx + radius * Math.cos(a), cz + radius * Math.sin(a)]);", "pts.push([cx + (radius - (i % 2)) * Math.cos(a), cz + (radius - (i % 2)) * Math.sin(a)]);"),
]
for name, what, a, b in M: assert core.count(a) == 1, name
work = os.path.join(here, 'mutants'); os.makedirs(work, exist_ok=True)
def run(text):
    open(os.path.join(work, 'core.js'), 'w', encoding='utf-8').write(text); open(os.path.join(work, 'test-core.js'), 'w', encoding='utf-8').write(test)
    try: r = subprocess.run(['node', 'test-core.js'], cwd=work, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired: return None, 'the test does not finish'
    m = re.search(r'CORE TEST: (\d+) assertions, (\d+) failed', r.stdout)
    first = next((l[5:95] for l in r.stdout.splitlines() if l.startswith('FAIL')), '')
    return m, first if m else (r.stderr.strip().splitlines() or ['no output'])[-1][:90]
if __name__ == '__main__':
    m, _ = run(core); assert m and m.group(2) == '0', 'the true core does not pass by this runner'
    print('control: the true core.js, run in the same way: %s assertions, 0 failed\n' % m.group(1), flush=True)
    caught = 0
    for name, what, a, b in M:
        m, first = run(core.replace(a, b))
        if m and m.group(2) == '0': res = 'NOT caught: all %s assertions pass' % m.group(1)
        elif m: res = 'caught: %s of %s fail; first: %s' % (m.group(2), m.group(1), first)
        else: res = 'caught: the test stops (%s)' % first
        caught += res.startswith('caught'); print('%-24s %s -- %s' % (name, what, res), flush=True)
    for f in ('core.js', 'test-core.js'): os.remove(os.path.join(work, f))
    print('\n%d of %d broken copies caught' % (caught, len(M)))
