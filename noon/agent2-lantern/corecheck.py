"""corecheck.py: core.js (the page's sums) against lantern.py on a grid of cases, faults and all.   python -I corecheck.py
Writes the cases to a temporary file, has node work them with core.js, and compares to 1 part in 10^12."""
import json, math, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lantern as L
FAULTS = [dict(a=11.0), dict(a=11.0, b=math.sqrt(121 - 1.05)), dict(a=11.0, yN=0.1), dict(a=11.0, a2=11.011), dict(a=11.0, p=2.01), dict(a=11.0, q=0.99), dict(a=11.0, e=0.05), dict(a=11.0, yL=0.02), dict(a=6.0), dict(a=3.73, a2=3.67, b=3.50, p=1.91, e=0.89), dict(a=26.0, yI=0.03)]
MS = [1.0, 1.01, 1.2, 1.5, 2.0, 2.36, 3.0, 5.0, 7.5, 10.0, 15.0, 20.0, 21.9, 30.0, 51.0]
cases = []; want = []
for kw in FAULTS:
    r = L.Rods(**kw)
    for m in MS:
        D = L.D_of_m(m); s = r.lens(D); K = r.K(D); f = L.focus(D); cases.append({'rods': kw, 'm': m}); want.append({'D': D, 's': s, 'K': K, 'focus': f[0], 'blur': None if s is None else (L.blur(D, s) if s > 1 else None), 'reach': r.reach(), 'light': None if s is None else L.light(m, s), 'light_shade': None if s is None else L.light(m, s, 0.833)})
js = """
const C = require(process.argv[2]); const cases = JSON.parse(require('fs').readFileSync(process.argv[3], 'utf8')); const out = [];
for (const c of cases) { const r = C.rods(c.rods), D = C.DofM(c.m), s = r.lens(D), K = r.K(D); const b = s === null ? null : C.blur(D, s);
  out.push({ D: D, s: s, K: K, focus: C.focus(D)[0], blur: (b === null || !isFinite(b)) ? null : b, reach: r.reach(), light: s === null ? null : C.light(c.m, s), light_shade: s === null ? null : C.light(c.m, s, 0.833) }); }
process.stdout.write(JSON.stringify(out));
"""
d = tempfile.mkdtemp(prefix='noon-corecheck-%d-' % os.getpid())
try:
    open(os.path.join(d, 'cases.json'), 'w').write(json.dumps(cases)); open(os.path.join(d, 'run.js'), 'w').write(js)
    got = json.loads(subprocess.run(['node', os.path.join(d, 'run.js'), os.path.join(HERE, 'core.js'), os.path.join(d, 'cases.json')], capture_output=True, text=True, check=True).stdout)
finally:
    import shutil; shutil.rmtree(d, ignore_errors=True)
bad = 0; none_cases = 0
def same(a, b):
    if a is None or b is None: return a is None and b is None
    if isinstance(a, (list, tuple)): return all(same(x, y) for x, y in zip(a, b))
    return abs(a - b) <= 1e-12 * max(1.0, abs(a))
for c, w, g in zip(cases, want, got):
    none_cases += w['s'] is None
    for k in w:
        if not same(w[k], g[k]): bad += 1; print('DIFFERS', c, k, w[k], g[k])
print('%d cases (%d of them with the rods jammed or out of reach), %d figures each: %d differences' % (len(cases), none_cases, len(want[0]), bad)); sys.exit(1 if bad else 0)
