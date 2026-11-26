"""Reader's recomputation of the table of section 3, the sentence 'with the first three moves alone', the counts of 'In short',
and the examples of sections 5 and 6, from: rows-36.json, rows-100.json (the earlier note's tables), out225/z225-*.jsonl (the run),
the reader's own LB / U3 / U (own-bounds-2.json, made by bounds_own.py) and the sizes of the multisets the reader checked
(realised-sizes.json, made by check_multisets.py).   usage: table_own.py"""
import json, glob, collections
R = '/home/agent3/pq2/rule/'
OB = json.load(open(R + 'reader/own-bounds-2.json')); RS = json.load(open(R + 'reader/realised-sizes.json'))
def key(M, D): return f'{M}|{",".join(map(str, sorted(D)))}'
def exps(D, p, q):
    out = []
    for d in sorted(D):
        u = v = 0
        while d % p == 0: d //= p; u += 1
        while d % q == 0: d //= q; v += 1
        out.append(f'{u}{v}')
    return ' '.join(sorted(out))
def table(M):
    """pattern -> (smallest size a programme found or None, proved least by a programme?)"""
    if M in (36, 100):
        return {tuple(sorted(r['D'])): (r['size'], bool(r['by'])) for r in json.load(open(f'/home/agent3/pq2/note/rows-{M}.json'))}
    T = {}
    for f in sorted(glob.glob(R + 'out225/z225-*.jsonl')):
        for l in open(f):
            if l.startswith('{'):
                r = json.loads(l); T[tuple(sorted(r['D']))] = (r['size'], r['status'] == 'optimal')
    return T
ALL = {}
for M, p, q in ((36, 2, 3), (100, 2, 5), (225, 3, 5)):
    T = table(M); assert len(T) == 256
    c = collections.Counter(); c3 = collections.Counter(); viol = []; bytwo = []; opens = []
    for D, (found, proved) in T.items():
        b = OB[key(M, D)]; lb, u3, u = b['LB'], b['U3'], b['U']
        assert RS[f'realised|{key(M, D)}'] == u3 and RS[f'realised2|{key(M, D)}'] == u, (M, D)   # a checked multiset of each size exists
        if proved and not (lb <= found <= u): viol.append((D, lb, found, u))
        if found is not None and found < lb: viol.append(('found below LB', D, lb, found))
        best = u if found is None else min(found, u)
        known = proved or lb == best
        least = found if proved else (lb if known else None)
        c['proved by a programme'] += proved; c['known by the bounds only'] += (known and not proved); c['open'] += (not known)
        if known and not proved: bytwo.append((exps(D, p, q), lb, found, u, 'LB = U' if lb == u else 'LB = a multiset a programme found, U larger'))
        if not known: opens.append((exps(D, p, q), lb, best))
        if known:
            c['LB = least = U' if lb == least == u else 'least = LB < U' if least == lb else 'LB < least = U' if least == u else 'LB < least < U'] += 1
        if proved:
            c3['LB = least = U3' if lb == found == u3 else 'least = LB < U3' if found == lb else 'LB < least = U3' if found == u3 else 'LB < least < U3'] += 1
        ALL[(M, exps(D, p, q))] = dict(D=D, LB=lb, U3=u3, U=u, found=found, proved=proved, least=least)
    print(f'Z_{M}:', dict(c))
    print('   LB = U for', sum(1 for D in T if OB[key(M, D)]['LB'] == OB[key(M, D)]['U']), '; LB = U3 for', sum(1 for D in T if OB[key(M, D)]['LB'] == OB[key(M, D)]['U3']))
    print('   three moves, programme-decided only:', dict(c3))
    print('   proved value below LB or above U, or a found multiset below LB:', viol)
    print('   known by the bounds only:', bytwo)
    print('   least is LB or U:', c['LB = least = U'] + c['LB < least = U'] + c['least = LB < U'], 'of', 256 - c['open'])
    print('   LB < least < U:', [(S, r['LB'], r['least'], r['U']) for (m, S), r in ALL.items() if m == M and r['least'] is not None and r['LB'] < r['least'] < r['U']])
    print('   least = LB < U:', [(S, r['LB'], r['U']) for (m, S), r in ALL.items() if m == M and r['least'] is not None and r['LB'] == r['least'] < r['U']])
def mirror(S): return ' '.join(sorted(t[1] + t[0] for t in S.split()))
def six(S, k):
    out = []
    for M in (36, 100, 225): out += [ALL[(M, S)][k], ALL[(M, mirror(S))][k]]
    return out
print('\nsix readings (2,3) (3,2) (2,5) (5,2) (3,5) (5,3):')
for S, name in (('01 02 21', '(a) {q, q2, p2q}'), ('01 02 22', '(b) {q, q2, p2q2}'), ('12 21', '{pq2, p2q}'), ('01 10 21', '{p, q, p2q}'), ('02 11 20', '{q2, pq, p2}'), ('01 02 20 22', '{q, q2, p2, p2q2}')):
    print(' ', name, '\n     LB', six(S, 'LB'), '\n     U3', six(S, 'U3'), '\n     U ', six(S, 'U'), '\n     found', six(S, 'found'), '\n     proved', six(S, 'proved'), '\n     least', six(S, 'least'))
json.dump({f'{M}|{S}': r for (M, S), r in ALL.items()}, open(R + 'reader/own-table.json', 'w'))
