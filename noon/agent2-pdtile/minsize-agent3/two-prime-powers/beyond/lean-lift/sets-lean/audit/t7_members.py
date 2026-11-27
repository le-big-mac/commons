# t7_members.py -- the three least-size statements for sets, for values V too large for a census of sets: is V attained
# by a SET on Z_{p^n q s}, s = r^j the least power of r above V (r = 3, 5, 7)?
# Candidates: the multisets of V elements on Z_{p^n q} listed in /home/agent3/lean/two-audit/t4_members.txt (an earlier
# audit; used here only as candidates: each is re-checked with core.py against the clauses of its instance on Z_{p^n q},
# and its size against Lean's value in L4_rule_eval.out).  Each is then lifted to a set on Z_{p^n q r^j} (random lifts,
# seeded), and the set is checked against the clauses of the statement on the big group: pattern among ALL divisors > 1
# of p^n q r^j.  That gives "V is in the set of the statement".  ("V is a lower bound" is the multiset theorem, a set
# being a multiset; it is tested by census only for small V, in t3_minsize.py.)
# usage: python t7_members.py [maxG]
import re, sys, random, json, time
from core import *
from t3_minsize import read_rule, member

maxG = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
val = read_rule()
rx = re.compile(r'^(\d+) (\d+) (\d+) (\d+) ([AUB]) Es=\[([\d, ]*)\](?: Fs=\[([\d, ]*)\])?(?: a0=(\d+))?: Lean (\d+); member on Z_(\d+): \[([\d, ]*)\] \(lift number \d+ of \[([\d, ]*)\]\)')
cands = {}
for line in open('/home/agent3/lean/two-audit/t4_members.txt'):
    m = rx.match(line.strip())
    if not m:
        continue
    p, q, n = int(m.group(1)), int(m.group(2)), int(m.group(3))
    kind = m.group(5)
    Es = tuple(int(x) for x in m.group(6).split(',') if x.strip())
    Fs = tuple(int(x) for x in (m.group(7) or '').split(',') if x.strip())
    base = tuple(int(x) for x in m.group(12).split(',') if x.strip())
    if kind == 'A':
        inst = ('A', p, q, n, Es)
    elif kind == 'U':
        inst = ('U', p, q, n, Es, Fs)
    else:
        inst = ('B', p, q, n, Es, Fs, int(m.group(8)))
    cands.setdefault(inst, base)
print("instances with a candidate multiset:", len(cands))
rng = random.Random(4711)
groups = {}


def grp(G):
    if G not in groups:
        groups[G] = Group(G)
    return groups[G]


n_base_ok = n_base_bad = 0
n_try = n_ok = n_fail = n_skip = 0
maxV = 0
maxGused = 0
rows = []
tasks = []
n_ld = 0
t0 = time.time()
for inst in sorted(cands, key=str):
    base = cands[inst]
    kind, p, q, n = inst[0], inst[1], inst[2], inst[3]
    if inst not in val:
        continue
    if kind == 'B':
        Fs, a0 = set(inst[5]), inst[6]
        if not (1 <= a0 <= n and a0 not in Fs and all(l in Fs for l in range(1, a0))):
            continue
    V = val[inst]
    M = p ** n * q
    gM = grp(M)
    w = [0] * M
    for x in base:
        w[x % M] += 1
    # the candidate on the base group: size V and the clauses with s = 1
    if not (len(base) == V and all(0 <= x < M for x in base) and member(inst, gM.pattern(w), M, M)):
        n_base_bad += 1
        rows.append((inst, V, 'candidate rejected on the base group'))
        continue
    n_base_ok += 1
    supp = [x for x in range(M) if w[x]]
    for r in (3, 5, 7):
        s = r
        while s <= V:
            s *= r
        G = M * s
        if G > maxG:
            n_skip += 1
            continue
        tasks.append((G, str(inst), inst, V, M, w, supp, r, s))
# one big group at a time (the tables of a group of order 3000 take about 150 MB while they are built)
tasks.sort(key=lambda t: (t[0], t[1], t[7]))
curG, gG = None, None
for (G, _, inst, V, M, w, supp, r, s) in tasks:
    if G != curG:
        gG = None
        gG = Group(G)
        curG = G
    n_try += 1
    found = None
    for tr in range(1, 2001):
        A = [x + M * u for x in supp for u in rng.sample(range(s), w[x])]
        if len(set(A)) == len(A) == V and member(inst, gG.pattern_of_set(A), G, M):
            found = (A, tr)
            break
    if found:
        n_ok += 1
        maxV = max(maxV, V)
        maxGused = max(maxGused, G)
        # literal re-check by long division, all d | G, for one set in 25
        if n_ok % 25 == 0:
            mult = [0] * G
            for y in found[0]:
                mult[y] += 1
            pat2 = frozenset(d for d in gG.dgt1 if divides_longdiv(G, mult, d))
            assert pat2 == gG.pattern_of_set(found[0]) and member(inst, pat2, G, M)
            n_ld += 1
        rows.append((inst, V, 'r=%d s=%d G=%d: set found at lift %d, max multiplicity of the multiset %d' % (r, s, G, found[1], max(w))))
    else:
        n_fail += 1
        rows.append((inst, V, 'r=%d s=%d G=%d: NO SET FOUND in 2000 random lifts (max multiplicity %d)' % (r, s, G, max(w))))
for row in rows:
    print(row)
print()
print("candidates accepted on the base group: %d; rejected: %d" % (n_base_ok, n_base_bad))
print("(instance, r) tried: %d; a set of V elements with the clauses of the statement found: %d; not found: %d; skipped (group above %d): %d"
      % (n_try, n_ok, n_fail, maxG, n_skip))
print("largest V with a set found: %d; largest group used: Z_%d; long-division rechecks: %d; seconds %.0f" % (maxV, maxGused, n_ld, time.time() - t0))
