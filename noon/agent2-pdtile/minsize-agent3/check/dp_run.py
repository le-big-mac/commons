"""Driver for dp.c (the referee's tree recursion).  Runs it, checks EVERY witness it prints by exact integer polynomial
division (pattern and size), then compares the least sizes with (a) the note's formulas (section 2 theorem, section 3 rule)
and (b) the author's JSON-line tables in ../out (decided patterns only).
usage: dp_run.py p q n S SU kind(multi|set) threads [nowit]
Writes dp-p{p}-q{q}-n{n}-{kind}-S{S}.out"""
import sys, subprocess, os, json, glob, time
sys.path.insert(0, '/home/agent3/minsize/check')
from pat import *

p, q, n, S, SU, kind, threads = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6], sys.argv[7]
wit = '0' if (len(sys.argv) > 8 and sys.argv[8] == 'nowit') else '1'
here = '/home/agent3/minsize/check'; M = p ** n * q
env = dict(os.environ, OMP_NUM_THREADS=threads)
t0 = time.time()
raw = subprocess.run([f'{here}/dp', str(p), str(q), str(n), str(S), str(SU), kind, wit], capture_output=True, text=True, env=env)
assert raw.returncode == 0, raw.stderr
secs = time.time() - t0
res = {}
nw = 0
for line in raw.stdout.splitlines():
    if not line.startswith('R '): continue
    head, _, w = line.partition(' W')
    t = head.split()
    E = tuple(int(c) for c in t[2].split(',')[1:]); F = tuple(int(c) for c in t[3].split(',')[1:]); m = int(t[5])
    res[E, F] = None if m < 0 else m
    if m > 0 and wit == '1':
        ww = parse_witness(w, M)
        assert sum(ww) == m, ('size', E, F)
        if kind == 'set': assert max(ww) <= 1
        got = exact_pattern_division(p, q, n, ww)
        assert got == (E, F), ('witness has another pattern', E, F, got)
        nw += 1
# the author's tables
auth = {}
for solver in ('cpsat', 'highs'):
    for ext in ('', '.part'):
        f = f'/home/agent3/minsize/out/n{n}-p{p}-q{q}-{kind}-{solver}.jsonl{ext}'
        if os.path.exists(f):
            for l in open(f):
                if not l.startswith('{'): continue
                try: r = json.loads(l)
                except Exception: continue      # a line being written
                if r['undecided']: continue
                auth.setdefault((tuple(r['E']), tuple(r['F'])), {})[solver] = r['min']
out = [f'# p={p} q={q} n={n} order {M}, {kind}; every class of size <= {S}, unbalanced root <= {SU}; {secs:.0f} s; '
       f'{nw} witnesses checked by exact division' + ('' if wit == '1' else ' (witnesses not requested)')]
out.append('# E | F | least size by the recursion | note\'s formula | author\'s solvers (decided) | verdict')
c = dict(thm_ok=0, thm_bad=0, thm_beyond=0, rule_ok=0, rule_bad=0, rule_beyond=0, all_ok=0, all_bad=0, all_beyond=0, auth_same=0, auth_diff=0, sets=0, set_same=0, set_bigger=0, set_smaller=0)
bad = []
for (E, F), m in sorted(res.items(), key=lambda t: (0 in t[0][1], t[0])):
    if 0 not in F: form, which, bound = thm_value(p, q, E, F), 'thm', SU
    else:
        form, x = rule_value(p, q, n, E, F); which = 'all' if x is None else 'rule'; bound = S
    a = auth.get((E, F))
    v = []
    if kind == 'multi':
        if m is None:
            if form > bound: c[which + '_beyond'] += 1; v.append(f'none <= {bound}; formula beyond')
            else: c[which + '_bad'] += 1; v.append('NONE FOUND, FORMULA WITHIN BOUND'); bad.append((E, F, m, form))
        elif m == form: c[which + '_ok'] += 1; v.append('as formula')
        else: c[which + '_bad'] += 1; v.append('DIFFERS FROM FORMULA'); bad.append((E, F, m, form))
    else:
        if m is not None:
            c['sets'] += 1
            if m == form: c['set_same'] += 1; v.append('set of formula size')
            elif m > form: c['set_bigger'] += 1; v.append('SMALLEST SET LARGER THAN FORMULA')
            else: c['set_smaller'] += 1; v.append('SET SMALLER THAN FORMULA'); bad.append((E, F, m, form))
        else: v.append('no set' if S >= M else f'no set <= {S}')
    if a:
        for solver, am in a.items():
            if am is None and m is None: c['auth_same'] += 1
            elif am is not None and m is not None and am == m: c['auth_same'] += 1
            elif am is not None and m is None and am > bound: pass
            else: c['auth_diff'] += 1; v.append(f'DIFFERS FROM AUTHOR {solver}={am}'); bad.append((E, F, m, 'author', solver, am))
    out.append(f'{list(E)} | {list(F)} | {m} | {which} {form} | {a if a else "-"} | {"; ".join(v)}')
if kind == 'multi':
    out.append(f"# 0 not in F (theorem): as formula {c['thm_ok']}, differs {c['thm_bad']}, beyond bound {c['thm_beyond']}")
    out.append(f"# F all levels: as formula {c['all_ok']}, differs {c['all_bad']}, beyond bound {c['all_beyond']}")
    out.append(f"# rest of 0 in F (rule): as formula {c['rule_ok']}, differs {c['rule_bad']}, beyond bound {c['rule_beyond']}")
else:
    out.append(f"# sets: patterns with a set {c['sets']}; smallest set = formula {c['set_same']}; larger {c['set_bigger']}; smaller {c['set_smaller']}")
out.append(f"# author's decided minima (each solver counted): same {c['auth_same']}, different {c['auth_diff']}")
for b in bad: out.append(f'# NOT AS EXPECTED: {b}')
open(f'{here}/dp-p{p}-q{q}-n{n}-{kind}-S{S}.out', 'w').write('\n'.join(out) + '\n')
print("\n".join(out[:1] + out[-(4 + len(bad)):]))
