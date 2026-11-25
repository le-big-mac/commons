# types.py -- for the 42 packings of the paper's tables (packings.json): the residues modulo 24 up to 10^6, the quadratic
# invariant chi_2 by the paper's Definition 4.3 from the root quadruple, and curvatures of the forms n^4, 4n^4, 9n^4, 36n^4
# that occur (which settle the quartic invariant where the type has one).   python -I types.py [N for the three (6,1,1,-1)]
import json, os, re, subprocess, sys, math
here = os.path.dirname(os.path.abspath(__file__)); P = json.load(open(os.path.join(here, 'packings.json')))
def kron(a, n):                                         # the Kronecker symbol (a / n)
    if n == 0: return 1 if abs(a) == 1 else 0
    s = 1
    if n < 0:
        n = -n
        if a < 0: s = -s
    v = 0
    while n % 2 == 0: n //= 2; v += 1
    if v:
        if a % 2 == 0: return 0
        if v % 2 == 1 and a % 8 in (3, 5): s = -s
    a %= n                                              # now n is odd and positive: the Jacobi symbol
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5): s = -s
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3: s = -s
        a %= n
    return s if n == 1 else 0
def chi2(n, m):                                         # circle of curvature n, tangent to one of coprime curvature m: rho = n + m
    rho = n + m
    if n % 4 in (0, 1): return kron(rho, n)
    if n % 4 == 2: return kron(-rho, n // 2)
    return kron(2 * rho, n)
SETS = {(6, 1): [0, 1, 4, 9, 12, 16], (6, 5): [0, 5, 8, 12, 20, 21], (6, 13): [0, 4, 12, 13, 16, 21], (6, 17): [0, 8, 9, 12, 17, 20], (8, 7): [3, 6, 7, 10, 15, 18, 19, 22], (8, 11): [2, 3, 6, 11, 14, 15, 18, 23]}
QUART = {(6, 1, 1, 1): ([1, 4, 9, 36], []), (6, 1, 1, -1): ([], [1, 4, 9, 36]), (6, 17, 1, 1): ([1, 4], [9, 36]), (6, 17, 1, -1): ([9, 36], [1, 4])}   # may occur, forbidden
os.makedirs(os.path.join(here, 'types'), exist_ok=True); N = 10**6; bigN = int(sys.argv[1]) if len(sys.argv) > 1 else 10**8
ok8 = ok9 = 0; w_ok = 0; w_all = 0; lines = []
for p in P:
    root = p['root']; t = tuple(p['type']); name = '_'.join(str(x).replace('-', 'm') for x in root)
    out = subprocess.run([os.path.join(here, 'enum')] + [str(x) for x in root] + [str(N), os.path.join(here, 'types', name + '.txt')], capture_output=True, text=True).stdout
    adm = [int(x) for x in re.search(r'residues modulo 24 that occur:((?: \d+)+)', out).group(1).split()]
    miss = set(int(x) for x in open(os.path.join(here, 'types', name + '.txt')).read().split())
    signs = sorted(set(chi2(n, m) for i, n in enumerate(root) for j, m in enumerate(root) if i != j and n > 0 and m > 0 and math.gcd(n, m) == 1))
    signs_all = sorted(set(chi2(n, m) for i, n in enumerate(root) for j, m in enumerate(root) if i != j and n > 0 and math.gcd(n, m) == 1 and n + m > 0))
    r_ok = adm == SETS[t[:2]]; c_ok = signs == [t[2]]; ok9 += r_ok; ok8 += c_ok
    line = '%-20s paper %-15s residues %s %s; chi_2 from the positive coprime pairs of the root: %s %s (with a negative partner allowed: %s)' % (tuple(root), t, adm, 'as the type' if r_ok else 'NOT the type', signs, 'as the type' if c_ok else 'NOT the type', signs_all)
    if len(t) == 4:
        may, forb = QUART[t]; found = {}
        for u in (1, 4, 9, 36):
            n = 1
            while u * n ** 4 <= N:
                v = u * n ** 4
                if v % 24 in adm and v not in miss and v > 0: found.setdefault(u, []).append(v)
                n += 1
        got_may = sorted(v for u in may for v in found.get(u, [])); got_forb = sorted(v for u in forb for v in found.get(u, []))
        line += '; fourth-power forms below 10^6: allowed and occurring %s, forbidden and occurring %s' % (got_may[:6], got_forb[:6])
        if may: w_all += 1; w_ok += (len(got_may) > 0 and not got_forb)
        p['quartic_found'] = (got_may, got_forb)
    lines.append(line); print(line, flush=True)
print('\nresidues as the type: %d of 42; chi_2 as the type: %d of 42; of the %d packings whose type allows a fourth-power form, a witness below 10^6 and nothing forbidden: %d' % (ok9, ok8, w_all, w_ok))
# the three of type (6, 1, 1, -1): none of the four forms up to bigN
for p in P:
    if tuple(p['type']) != (6, 1, 1, -1): continue
    root = p['root']; name = '_'.join(str(x).replace('-', 'm') for x in root) + '_big'
    out = subprocess.run([os.path.join(here, 'enum')] + [str(x) for x in root] + [str(bigN), os.path.join(here, 'types', name + '.txt')], capture_output=True, text=True).stdout
    adm = [int(x) for x in re.search(r'residues modulo 24 that occur:((?: \d+)+)', out).group(1).split()]
    miss = set(int(x) for x in open(os.path.join(here, 'types', name + '.txt')).read().split()); occ = []; cand = 0
    for u in (1, 4, 9, 36):
        n = 1
        while u * n ** 4 <= bigN:
            v = u * n ** 4
            if v % 24 in adm:
                cand += 1
                if v not in miss: occ.append(v)
            n += 1
    print('%s up to %d: %s; admissible numbers of the four forms: %d; occurring as curvatures: %d %s' % (tuple(root), bigN, out.split('\n')[0].split(': ', 1)[1], cand, len(occ), occ[:5]), flush=True)
