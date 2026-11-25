# mutants.py -- can the tests fail?  Make copies of core.js, each with one thing broken, and run test.js on each.
# usage: python -I mutants.py     (writes mutants/*.js and prints a line for each: caught, or NOT caught)
import subprocess, os, re
here = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(here, 'core.js')).read()
END1 = "      y = sub(y, ulp(y));\n    } while (cmp(y, lim) > 0);\n    this.gS.set(r, min); return min;"
muts = [
 ('succ-first-pass-only', "Algorithm 1's loop makes one pass only", END1, END1.replace("while (cmp(y, lim) > 0)", "while (false)")),
 ('succ-stops-at-sixteenth', "Algorithm 1's loop stops at r - 1/16 instead of r - 1/2", END1, END1.replace("cmp(y, lim) > 0", "cmp(y, add(lim, [7n, 4])) > 0")),
 ('succ-stops-at-eighth', "Algorithm 1's loop stops at r - 1/8 instead of r - 1/2", END1, END1.replace("cmp(y, lim) > 0", "cmp(y, add(lim, [3n, 3])) > 0")),
 ('succ-stops-at-quarter', "Algorithm 1's loop stops at r - 1/4 instead of r - 1/2", END1, END1.replace("cmp(y, lim) > 0", "cmp(y, add(lim, [1n, 2])) > 0")),
 ('succ-steps-two', "Algorithm 1 steps y down by 2/Denominator(y) instead of 1/Denominator(y)", END1, END1.replace("y = sub(y, ulp(y));", "y = sub(y, dbl(ulp(y)));")),
 ('weak-first-pass-only', "Algorithm 3's loop makes one pass only", "      y = sub(y, ulp(y));\n    } while (cmp(y, lim) >= 0);", "      y = sub(y, ulp(y));\n    } while (false);"),
 ('weak-loop-strict', "Algorithm 3's loop stops before r - 1/2 instead of at it", "    } while (cmp(y, lim) >= 0);", "    } while (cmp(y, lim) > 0);"),
 ('weak-no-second-return', "Algorithm 3 without its second early return", "y = this.weakSucc(t); if (cmp(y, t) === 0) { ans = r; break; }", "y = this.weakSucc(t);"),
 ('gaps-not-strict', "the memory of gaps answers 'greater than or equal' where 'greater than' is asked", "this.gS = new Gaps(true);", "this.gS = new Gaps(false);"),
 ('gaps-too-generous', "the memory of gaps reaches one unit in the last place too far down", "if (i < this.z.length && cmp(this.lo[i], t) <= 0) return this.z[i]; };", "if (i < this.z.length && cmp(sub(this.lo[i], ulp(this.lo[i])), t) <= 0) return this.z[i]; };"),
 ('tame-wrong-second-call', "Algorithm 4 asks for the successor of 2r - x instead of 2r - x - 1", "y = this.tameSucc(sub(sub(dbl(r), x), UNIT)), z = fuse(x, y);", "y = this.tameSucc(sub(dbl(r), x)), z = fuse(x, y);"),
 ('M-no-halving', "Algorithm 5 forgets to halve", "else { val = half(val); memo.set(key(r), val); stack.pop(); }                      // val is M(r - M(r - 1)): halve it", "else { memo.set(key(r), val); stack.pop(); }"),
 ('meek-floor', "my reading of Algorithm 6 with the power of two rounded down where it should be rounded up", "for (;;) { q = half(p); if (cmp(q, g) < 0) break; p = q; } }\n    var a = sub(add(x, ulp(x)), p)", "for (;;) { q = half(p); if (cmp(q, g) <= 0) break; p = q; } }\n    var a = sub(add(x, ulp(x)), p)"),
 ('meek-as-printed', "Algorithm 6 with its last line as printed (x ~ y)", "z = fuse(printed ? x : a, y);", "z = fuse(x, y);"),
 ('certificate-too-soon', "the small-gap certificate is given three halvings early", "      if (k > p) return { small: k };", "      if (k > p - 3) return { small: p + 1 };"),
 ('column-no-edge', "the picture's columns without the small move that counts a number standing on an edge", "var w = [ONE, p], lo = sub(a, [ONE, p + 20]), t, m, c, below = false;", "var w = [ONE, p], lo = a, t, m, c, below = false;"),
 ('recipe-floor', "the recipe's power of two rounded down", "p = UNIT; if (cmp(g, UNIT) > 0) { while (cmp(p, g) < 0) p = dbl(p); } else { for (;;) { q = half(p); if (cmp(q, g) < 0) break; p = q; } }\n        a = sub(add(s, m), p); y = sub(sub(dbl(z), UNIT), a); }", "p = UNIT; if (cmp(g, UNIT) > 0) { while (cmp(p, g) < 0) p = dbl(p); } else { for (;;) { q = half(p); if (cmp(q, g) <= 0) break; p = q; } }\n        a = sub(add(s, m), p); y = sub(sub(dbl(z), UNIT), a); }"),
 ('isTame-always', "isTame says yes to every number below 1", "      if (cmp(z, UNIT) < 0) { g = sub(UNIT, z); return g[0] === ONE; }\n      m = this.M(sub(z, UNIT), budget); if (m === null) return null;", "      if (cmp(z, UNIT) < 0) { return true; }\n      m = this.M(sub(z, UNIT), budget); if (m === null) return null;"),
 ('fuse-no-one', "x ~ y without the + 1", "function fuse(x, y) { return half(add(add(x, y), UNIT)); }", "function fuse(x, y) { return half(add(x, y)); }"),
]
os.makedirs(os.path.join(here, 'mutants'), exist_ok=True); caught = 0
for name, what, a, b in muts:
    assert src.count(a) == 1, name
    path = os.path.join(here, 'mutants', name + '.js'); open(path, 'w').write(src.replace(a, b))
    try:
        r = subprocess.run(['node', '--stack-size=20000', '--max-old-space-size=8000', os.path.join(here, 'test.js')], env=dict(os.environ, CORE=path), capture_output=True, text=True, timeout=300)
        m = re.search(r'(\d+) pass, (\d+) fail', r.stdout)
        res = ('caught: %s of the tests fail' % m.group(2)) if m and int(m.group(2)) > 0 else ('NOT caught: all %s tests pass' % m.group(1)) if m else 'caught: the program stops with an error'
    except subprocess.TimeoutExpired:
        res = 'caught: the tests do not finish in five minutes'
    if res.startswith('caught'): caught += 1
    print('%-26s %s -- %s' % (name, what, res), flush=True)
print('\n%d of %d broken copies caught' % (caught, len(muts)))
