# mutants.py -- can the tests fail?  Copies of gcore.js, each with one thing broken, run through gtest.js.
#   python -I mutants.py      (prints a line for each as it finishes: caught, or NOT caught)
import subprocess, os, re
from concurrent.futures import ThreadPoolExecutor, as_completed
here = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(here, 'gcore.js')).read()
muts = [
 ('kron-no-rule-for-2', "the Kronecker symbol without the rule for a lower entry divisible by 2", "if (v % 2 === 1) { t = ((a % 8) + 8) % 8; if (t === 3 || t === 5) s = -s; }", "if (v % 2 === 1) { t = ((a % 8) + 8) % 8; }"),
 ('kron-no-reciprocity', "the Kronecker symbol without the sign of quadratic reciprocity", "if (a % 4 === 3 && n % 4 === 3) s = -s;", ""),
 ('kron-two-in-upper', "the Kronecker symbol without the sign for a factor 2 taken out of the upper entry", "while (a % 2 === 0) { a /= 2; t = n % 8; if (t === 3 || t === 5) s = -s; }", "while (a % 2 === 0) { a /= 2; }"),
 ('chi2-three-mod-four', "chi_2 for a curvature 3 modulo 4 without the factor 2", ": kron(2 * rho, n); }", ": kron(rho, n); }"),
 ('chi2-two-mod-four', "chi_2 for a curvature 2 modulo 4 without the minus sign", "kron(-rho, n / 2)", "kron(rho, n / 2)"),
 ('residues-five', "the residues for an odd curvature 5 modulo 8 taken as for 1", "r === 5 ? [0, 4, 5]", "r === 5 ? [0, 1, 4]"),
 ('table-one-row', "one row of the table of families changed", "'6,5,-1': [[1, 6], []]", "'6,5,-1': [[1, 2], []]"),
 ('type-quartic-kinds', "the kinds with a fourth entry taken to be (6, 1) only", "(k === 1 || k === 17) && c === 1", "(k === 1) && c === 1"),
 ('square-off', "isSquare says yes to one more than a square", "function isSquare(n) { var r = Math.round(Math.sqrt(n)); return r * r === n; }", "function isSquare(n) { var r = Math.round(Math.sqrt(n)); return r * r === n || r * r + 1 === n; }"),
 ('enum-bound', "the walk stops at curvatures N and above instead of above N", "if (nw > N) continue; if (last < 0 && strip", "if (nw >= N) continue; if (last < 0 && strip"),
 ('enum-revisit', "the walk may undo its last move", "last = stack[top + 4]; if (i === last) continue;", "last = stack[top + 4];"),
 ('touching-sign', "two circles are said to touch when the wrong sum of curvatures fits", "s = c1[0] + c2[0]; return u * u + v * v === s * s; }", "s = c1[0] - c2[0]; return u * u + v * v === s * s; }"),
 ('view-gap-tight', "the view test takes the gap's circle a tenth too small", "return dx * dx + dy * dy <= R * R * (1 + 1e-9);", "return dx * dx + dy * dy <= R * R * 0.81;"),
 ('view-outside-pruned', "the view test gives up where the gap is the outside of its circle", "if (dc > R) return true;", "if (dc > R) return false;"),
 ('view-size', "the walk for a view stops at circles twice the least size", "if (b > maxB) continue;", "if (b > maxB / 2) continue;"),
 ('view-no-gap-test', "the view test never prunes (every gap is walked)", "var p = contact(c1, c2), q = contact(c1, c3)", "return true; var p = contact(c1, c2), q = contact(c1, c3)"),
 ('view-strip-period', "the strip's period taken as 3", "c[1] + c[0] * 2 * k, c[2]]", "c[1] + c[0] * 3 * k, c[2]]"),
 ('row-formula', "the formula for a row of circles with m squared for m (m + 1)", "+ m * (m + 1) * (f1[t] + f2[t]); return o; }", "+ m * m * (f1[t] + f2[t]); return o; }"),
 ('row-jump-eager', "a row is jumped although its circles may reach the view (the margin of five radii dropped and the reach halved)", "- 5 / pp[0] > reach; }", "> reach / 2; }"),
 ('row-landing', "after a jump the walk is told the wrong one of the two circles is the newest", "q[last] = pm1; q[i] = pm; last = i;", "q[last] = pm1; q[i] = pm;"),
 ('local-rounded', "positions measured from the view's centre in floating numbers instead of exactly", "c[3] = Number(BigInt(c[1]) * B60 - CX * b) / S60; c[4] = Number(BigInt(c[2]) * B60 - CY * b) / S60;", "c[3] = c[1] - c[0] * view.cx; c[4] = c[2] - c[0] * view.cy;"),
 ('unsafe-shown', "circles past exact floating numbers are shown all the same", "if (!Number.isSafeInteger(b) || !Number.isSafeInteger(nw[1]) || !Number.isSafeInteger(nw[2]) || b > 4e15) continue;", ""),
 ('place-skips-a-check', "place() does not ask whether the third and fourth circles touch", "if (touching(c2, c4) && touching(c3, c4)) return", "if (touching(c2, c4)) return"),
]
for name, what, a, b in muts: assert src.count(a) == 1, name                # every change must find its place before anything is run
os.makedirs(os.path.join(here, 'mutants'), exist_ok=True)
def one(mut):
    name, what, a, b = mut; path = os.path.join(here, 'mutants', name + '.js'); open(path, 'w').write(src.replace(a, b))
    try:
        r = subprocess.run(['nice', '-n', '15', 'node', '--stack-size=30000', os.path.join(here, 'gtest.js')], env=dict(os.environ, CORE=path), capture_output=True, text=True, timeout=120)
        m = re.search(r'(\d+) pass, (\d+) fail', r.stdout)
        res = ('caught: %s of the tests fail' % m.group(2)) if m and int(m.group(2)) > 0 else ('NOT caught: all %s tests pass' % m.group(1)) if m else 'caught: the program stops with an error'
    except subprocess.TimeoutExpired: res = 'caught: the tests do not finish in two minutes (they take five seconds)'
    return '%-22s %s -- %s' % (name, what, res)
lines = {}
with ThreadPoolExecutor(max_workers=4) as ex:
    futs = {ex.submit(one, m): m[0] for m in muts}
    for f in as_completed(futs): lines[futs[f]] = f.result()
for m in muts: print(lines[m[0]])
print('\n%d of %d broken copies caught' % (sum(' -- caught' in l for l in lines.values()), len(muts)))
