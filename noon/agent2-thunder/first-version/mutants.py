# mutants.py -- can the tests of core.js fail?  Copies of core.js with one thing broken, each run through test-core.js.
#   python -I mutants.py > mutants.out
import subprocess, os, re
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n), encoding='utf-8').read()
core = rd('core.js'); test = rd('test-core.js')
M = [
 ('speed-of-sound', "sound travels at 300 m/s", "var C = 343;", "var C = 300;"),
 ('pulse-length', "the pulse is 4 ms long", "var T = 0.005;", "var T = 0.004;"),
 ('inverse-square', "the pulses weaken as one over the distance squared", "var g = (l / rm) * (T * C / dr);", "var g = (l / rm / rm) * (T * C / dr);"),
 ('hump-upside-down', "the humps are upside down", "p[s] += b * (v - v * v); }", "p[s] -= b * (v - v * v); }"),
 ('hump-shape', "the hump is a triangle, not a parabola", "p[s] += b * (v - v * v); }", "p[s] += b * 0.5 * (v < 0.5 ? v : 1 - v); }"),
 ('both-ends-same-sign', "the two ends of a piece are given the same sign", "B[k] += g; B[k + 1] -= g;", "B[k] += g; B[k + 1] += g;"),
 ('square-on-ignored', "a piece square-on to the listener makes no sound", "square++;\n        var tau", "square++; continue;\n        var tau"),
 ('square-on-height', "a square-on piece is twice too loud", "gs = (l / rm) * T * FS;", "gs = 2 * (l / rm) * T * FS;"),
 ('first-arrival', "the sound starts when the first corner of the channel arrives, not the nearest", "var t0 = d.nearest / C - LEAD, len = Math.ceil(((d.farthest - d.nearest) / C + T + LEAD) * FS) + 2 + Math.ceil(0.02 * FS);\n    var p = new Float64Array(len), B", "var t0 = r[0] / C - LEAD, len = Math.ceil(((d.farthest - d.nearest) / C + T + LEAD) * FS) + 2 + Math.ceil(0.02 * FS);\n    var p = new Float64Array(len), B"),
 ('reported-first', "the first sound is reported a pulse length late", "inear: d.inear, ifar: d.ifar, first: d.nearest / C,", "inear: d.inear, ifar: d.ifar, first: d.nearest / C + T,"),
 ('nearest-is-first-point', "the nearest point is taken to be the first point", "if (r[i] < lo) { lo = r[i]; ilo = i; }", "if (i === 0) { lo = r[i]; ilo = i; }"),
 ('blur-loses', "the blur divides by too much and loses pressure", "dens = v / (2 * h);", "dens = v / (2.2 * h);"),
 ('blur-with-distance', "the blur grows as the distance, not its square root", "sd = air * Math.sqrt(Math.max(0, C * t) / 1000), h = sd * FS;", "sd = air * (Math.max(0, C * t) / 1000), h = sd * FS;"),
 ('blur-two-passes', "two running means, not three", "for (var pass = 0; pass < 3; pass++) {", "for (var pass = 0; pass < 2; pass++) {"),
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
