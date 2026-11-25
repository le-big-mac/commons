# classify.py -- from the lists of missing curvatures (enum.c), the sporadic sets and the paper's remarks.
#   python -I classify.py      (reads missing/*.txt and missing/*.log; prints what the sealed lines 1 to 7, 10 and 11 need)
import os, re, math
here = os.path.dirname(os.path.abspath(__file__)); N = 10**8
PACK = [('bugeye', (-1, 2, 2, 3), []), ('strip', (0, 0, 1, 1), []), ('m3_5_8_8', (-3, 5, 8, 8), [1, 6]), ('m3_4_12_13', (-3, 4, 12, 13), [2, 6]),
        ('m2_3_6_7', (-2, 3, 6, 7), [2]), ('m4_5_20_21', (-4, 5, 20, 21), [2, 3])]
def isfam(n, fam):
    for u in fam:
        if n % u == 0:
            r = math.isqrt(n // u)
            if r * r == n // u: return u
    return 0
res = {}
for name, root, fam in PACK:
    log = open(os.path.join(here, 'missing', name + '.log')).read()
    m = re.search(r'curvatures up to (\d+): (\d+) circles, (\d+) different curvatures', log); assert int(m.group(1)) == N
    adm = [int(x) for x in re.search(r'residues modulo 24 that occur:((?: \d+)+)', log).group(1).split()]
    miss = [int(x) for x in open(os.path.join(here, 'missing', name + '.txt')).read().split()]; mset = set(miss)
    # every member of a family that is admissible and at most N must be missing; count them, and any that is present
    famcount = {u: 0 for u in fam}; present = []
    for u in fam:
        n = 1
        while u * n * n <= N:
            v = u * n * n
            if v % 24 in adm:
                famcount[u] += 1
                if v not in mset: present.append(v)
            n += 1
    spor = [x for x in miss if not isfam(x, fam)]
    per = {r: [x for x in spor if x % 24 == r] for r in adm}
    res[name] = dict(root=root, adm=adm, miss=miss, spor=spor, per=per)
    print('%s %s: residues %s; %s circles; missing %d; in the families %s: %s admissible members up to 10^8, of which present as curvatures: %d%s; sporadic %d, the largest %d' % (
        name, root, adm, format(int(m.group(2)), ','), len(miss), fam, famcount, len(present), (' ' + str(present[:5])) if present else '', len(spor), max(spor)))
    print('   sporadic by residue: ' + ', '.join('%d: %d' % (r, len(per[r])) for r in adm))
    top = sorted(spor)[-100:]
    if len(spor) >= 100: print('   of its 100 largest sporadic: multiples of 5: %d, of 13: %d, of 11: %d, of 7: %d, of 17: %d, of 3: %d' % tuple(sum(1 for x in top if x % p == 0) for p in (5, 13, 11, 7, 17, 3)))
    res[name]['top'] = top
print()
print('Remark 6.1: (-3,5,8,8), class 5: missing %s; (-3,4,12,13), class 13: missing %s; bug-eye, classes 11, 14, 23: missing %s, %s, %s; strip, class 1: missing %s; bug-eye, class 2: missing %s' % (
    res['m3_5_8_8']['per'][5], res['m3_4_12_13']['per'][13], res['bugeye']['per'][11], res['bugeye']['per'][14], res['bugeye']['per'][23], res['strip']['per'][1], res['bugeye']['per'][2]))
pool = [x for name in ('strip', 'm3_5_8_8', 'm3_4_12_13', 'm2_3_6_7', 'm4_5_20_21') for x in res[name]['top']]
print('the five lists of 100 pooled (%d numbers): multiples of 13: %d, of 11: %d, of 5: %d' % (len(pool), sum(1 for x in pool if x % 13 == 0), sum(1 for x in pool if x % 11 == 0), sum(1 for x in pool if x % 5 == 0)))
