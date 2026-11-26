"""Second pass.  The reader's own six-move cost (the five moves of bounds_own.py and the balanced lift AS THE PROGRAM algebra3.py
SUPPOSES IT: pattern P of B on Z_K, K = N/r, holding r, ..., r^(j-1), size divisible by r^j  ->  pattern P + {r^j} on Z_N, same size),
set beside U6-M.json and status.json; every multiset of realised3-M.jsonl checked with the reader's pattern test; the table of
section 3 recomputed with U = the six-move cost only where a checked multiset of that size is on file.   usage: six.py"""
import sys, json, glob, math, collections
sys.path.insert(0, '/home/agent3/pq2/rule/reader')
import bounds_own as bo
from pat import parse, pattern
R = '/home/agent3/pq2/rule/'
five_q = bo.from_quotients
def six_q(N, sizes, cap):
    yield from five_q(N, sizes, cap)
    for r in bo.divisors(N):
        if r < 2 or any(r % t == 0 for t in range(2, r)): continue           # r prime
        j = 0
        while N % r ** (j + 1) == 0: j += 1
        if j < 2: continue
        K = N // r; need = frozenset(r ** i for i in range(1, j))
        for P, bits in sizes[K].items():
            if need <= P:
                s = r ** j
                while (1 << s) <= bits:
                    if bits >> s & 1: yield P | {r ** j}, s
                    s += r ** j
def exps(D, p, q):
    out = []
    for d in sorted(D):
        u = v = 0
        while d % p == 0: d //= p; u += 1
        while d % q == 0: d //= q; v += 1
        out.append(f'{u}{v}')
    return ' '.join(sorted(out))
def table(M):
    if M in (36, 100):
        return {tuple(sorted(r['D'])): (r['size'], bool(r['by'])) for r in json.load(open(f'/home/agent3/pq2/note/rows-{M}.json'))}
    T = {}
    for f in sorted(glob.glob(R + 'out225/z225-*.jsonl')):
        for l in open(f):
            if l.startswith('{'):
                r = json.loads(l); T[tuple(sorted(r['D']))] = (r['size'], r['status'] == 'optimal')
    return T
st = json.load(open(R + 'status.json')); OUT = {}; SIZES6 = {}
for M, p, q in ((36, 2, 3), (100, 2, 5), (225, 3, 5)):
    bo.from_quotients = five_q; u5, s5 = bo.five_moves(M, 2)
    bo.from_quotients = six_q; u6, s6 = bo.five_moves(M, 2); SIZES6[M] = s6
    bo.from_quotients = five_q
    u3 = bo.three_moves(M)
    # realised3: every line checked
    on3 = {}; bad = 0
    for l in open(f'{R}realised3-{M}.jsonl'):
        r = json.loads(l); v = parse(r['multiset'], M)
        if not (sum(v) == r['size'] and pattern(v, M) == sorted(r['D'])): bad += 1; print('FAIL realised3', M, r['D'])
        on3[frozenset(r['D'])] = sum(v)
    on2 = {frozenset(json.loads(l)['D']): json.loads(l)['size'] for l in open(f'{R}realised2-{M}.jsonl')}
    U6f = {frozenset(int(t) for t in k.split(',') if t): v for k, v in json.load(open(f'{R}U6-{M}.json')).items()}
    print(f'Z_{M}: realised3-{M}.jsonl: {len(on3)} multisets, failures of size or exact pattern: {bad}')
    print(f'   my six-move cost against U6-{M}.json: differs for {sum(1 for D in u6 if u6[D] != U6f[D])} of 256; my five-move cost against status.json U5: differs for '
          f'{sum(1 for r in st[str(M)]["rows"] if u5[frozenset(r["D"])] != r["U5"])}; my U3 against status.json U3: differs for {sum(1 for r in st[str(M)]["rows"] if u3[frozenset(r["D"])] != r["U3"])}')
    low = [D for D in u6 if u6[D] < u5[D]]
    print(f'   six-move cost below five-move cost for {len(low)} patterns:', [(exps(D, p, q), u5[D], u6[D], 'multiset of that size on file' if on3.get(D) == u6[D] else 'NO MULTISET ON FILE') for D in low])
    missing = [D for D in u6 if D not in on3]
    print(f'   patterns with no line in realised3-{M}.jsonl: {len(missing)}:', [(sorted(D), exps(D, p, q), 'six', u6[D], 'five', u5[D], 'on file with five moves', on2[D]) for D in sorted(missing, key=lambda D: (len(D), sorted(D)))])
    print(f'      of them with six-move cost below five-move cost: {sum(1 for D in missing if u6[D] < u5[D])}')
    # U as the note now defines it: the five-move bound, or the six-move cost where a checked multiset of that size is on file
    U = {D: (u6[D] if u6[D] < u5[D] and on3.get(D) == u6[D] else u5[D]) for D in u5}
    assert all(on2[D] == u5[D] for D in u5)
    dU = [r['S'] for r in st[str(M)]['rows'] if U[frozenset(r['D'])] != r['U']]
    print('   U as defined, against status.json U: differs for', len(dU), dU)
    T = table(M); c = collections.Counter(); c3 = collections.Counter(); notprog = []; viol = []
    for D, (found, proved) in T.items():
        lb, parts = bo.LB(bo.pairs_of(D, p, q), p, q); u = U[frozenset(D)]
        best = u if found is None else min(found, u); known = proved or lb == best; least = found if proved else (lb if known else None)
        if proved and not lb <= found <= u: viol.append((D, lb, found, u))
        c['proved by a programme'] += proved; c['not proved, LB = smallest known'] += (known and not proved); c['open'] += (not known)
        if known and not proved: notprog.append((exps(D, p, q), 'LB', lb, 'found', found, 'U', u))
        if known: c['LB = least = U' if lb == least == u else 'least = LB < U' if least == lb else 'LB < least = U' if least == u else 'LB < least < U'] += 1
        if proved:
            w = u3[frozenset(D)]; c3['LB = least = U3' if lb == found == w else 'least = LB < U3' if found == lb else 'LB < least = U3' if found == w else 'LB < least < U3'] += 1
        OUT[f'{M}|{exps(D, p, q)}'] = dict(D=list(D), LB=lb, U3=u3[frozenset(D)], U5=u5[frozenset(D)], U6=u6[frozenset(D)], U=u, found=found, proved=proved, least=least)
    print('   table:', dict(c)); print('   three moves, programme-decided:', dict(c3))
    print('   LB = U for', sum(1 for D in T if bo.LB(bo.pairs_of(D, p, q), p, q)[0] == U[frozenset(D)]), '; LB = U3 for', sum(1 for D in T if bo.LB(bo.pairs_of(D, p, q), p, q)[0] == u3[frozenset(D)]),
          '; least is LB or U:', c['LB = least = U'] + c['LB < least = U'] + c['least = LB < U'], 'of', 256 - c['open'])
    print('   not proved by a programme, LB = smallest known:', notprog)
    print('   a proved value below LB or above U:', viol)
json.dump(OUT, open(R + 'reader/second/own-table-six.json', 'w'))
# "not a fair sample"
W = {}
for k, r in OUT.items():
    W[k] = 'open' if r['least'] is None else 'between' if r['LB'] < r['least'] < r['U'] else 'other'
b36 = [k.split('|')[1] for k in W if k.startswith('36|') and W[k] == 'between']
print('strictly between on Z_36:', len(b36), '; of them open on Z_225:', sum(1 for S in b36 if W[f'225|{S}'] == 'open'), '; open on Z_100:', sum(1 for S in b36 if W[f'100|{S}'] == 'open'))
for M in (225, 100):
    op = [k for k in W if k.startswith(f'{M}|') and W[k] == 'open']
    print(f'open on Z_{M}: {len(op)}; with a multiset on file smaller than U: {sum(1 for k in op if OUT[k]["found"] is not None and OUT[k]["found"] < OUT[k]["U"])}')
# section 5 (a): sizes the six-move program reaches for {q, p^2 q} on Z_{p^2 q}
for M, p, q in ((36, 2, 3), (36, 3, 2), (100, 2, 5), (100, 5, 2), (225, 3, 5), (225, 5, 3)):
    K = p * p * q; P = frozenset({q, K}); bits = SIZES6[M][K].get(P, 0)
    got = [s for s in range(1, 2 * K + 1) if bits >> s & 1]; want = [q * t for t in range(p + 1, 2 * K // q + 1)]
    print(f'(p, q) = ({p}, {q}): sizes reached for {{q, p^2 q}} on Z_{K}: {got[:6]}... to {got[-1]}; every q t with t >= p + 1 up to the cap {2 * K}: {got == want}; '
          f'least multiple of q^2 among them: {min(s for s in got if s % (q * q) == 0)}; LB of {{q, q^2, p^2 q}}: {OUT[str(M) + "|" + exps([q, q * q, p * p * q], *((p, q) if (p, q) in ((2, 3), (2, 5), (3, 5)) else (q, p)))]["LB"]}')
