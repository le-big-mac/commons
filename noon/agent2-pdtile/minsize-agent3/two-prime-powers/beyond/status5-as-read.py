"""One status for every pattern of the three groups, from the programmes' results and the two bounds.
least size known if a programme proved it, or if LB equals the smallest size known (the smaller of what a programme found and U, which
realise.py realises by an explicit multiset).   Writes status.json and the three tables bounds-M.md.   usage: status.py"""
import json, glob, sys, collections
sys.path.insert(0, '/home/agent3/pq2/rule')
from lowerbound import LB
from algebra import closure, expr
from algebra2 import Calc
def exps(D, p, q):
    out = []
    for d in D:
        u = 0
        while d % p == 0: d //= p; u += 1
        v = 0
        while d % q == 0: d //= q; v += 1
        out.append(f'{u}{v}')
    return ' '.join(sorted(out)) or '(none)'
def table(M):
    if M in (36, 100): return [(r['D'], r['size'], bool(r['by'])) for r in json.load(open(f'/home/agent3/pq2/note/rows-{M}.json'))]
    R = {}
    for f in sorted(glob.glob('out225/z225-*.jsonl')):
        for l in open(f):
            if l.startswith('{'): r = json.loads(l); R[tuple(r['D'])] = r
    P = json.load(open('predictions-225.json'))
    return [([int(t) for t in k.split(',') if t], R[tuple(int(t) for t in k.split(',') if t)]['size'], R[tuple(int(t) for t in k.split(',') if t)]['status'] == 'optimal') for k in P]
out = {}
for M, p, q in ((36, 2, 3), (100, 2, 5), (225, 3, 5)):
    divs, mask, U, how = closure(p, q); c = collections.Counter(); c3 = collections.Counter(); lines = []; rows = []
    C2 = Calc(p, q); realised2 = {tuple(json.loads(l)['D']) for l in open(f'realised2-{M}.jsonl')}
    realised = {tuple(json.loads(l)['D']) for l in open(f'realised-{M}.jsonl')}
    for D, size, dec in sorted(table(M), key=lambda t: (len(t[0]), t[0])):
        lb, parts = LB(D, p, q); u3 = U[mask(D)]; u = C2.U[frozenset(D)]; assert tuple(D) in realised and tuple(D) in realised2 and u <= u3
        if dec: c3['LB = least = U' if lb == size == u3 else 'least = LB < U' if size == lb else 'LB < least = U' if size == u3 else 'LB < least < U'] += 1
        best = min(size, u) if size is not None else u
        assert lb <= best, (M, D, lb, best)
        if dec: assert lb <= size <= u, (M, D, lb, size, u)
        known = dec or lb == best
        least = size if dec else (lb if lb == best else None)
        how_known = 'a programme' + (' and the two bounds' if lb == u else '') if dec else ('the two bounds' if lb == u else 'LB and a multiset a programme found') if known else ''
        where = ('LB = least = U' if lb == least == u else 'least = LB < U' if least == lb else 'LB < least = U' if least == u else 'LB < least < U') if known else f'open: between {lb} and {best}'
        c['decided by a programme'] += dec; c['decided by the bounds only'] += (known and not dec); c['open'] += (not known)
        c[where if known else 'open '] += 1
        rows.append(dict(D=D, S=exps(D, p, q), found=size, proved=dec, LB=lb, U=u, U3=u3, least=least, where=where, how=how_known, last_move=C2.how[frozenset(D)][0]))
        lines.append(f"| {', '.join(map(str, D)) or '(none)'} | {exps(D, p, q)} | {lb} | {least if known else ''} | {best} | {u} | {how_known} | {where} | {u3}: {expr(mask(D), how, divs)} |")
    c.pop('open ', None)
    out[M] = dict(counts=dict(c), counts_three_moves_programme_decided=dict(c3), LB_eq_U=sum(1 for r in rows if r['LB'] == r['U']), LB_eq_U3=sum(1 for r in rows if r['LB'] == r['U3']), U_below_U3=[(r['S'], r['U3'], r['U']) for r in rows if r['U'] < r['U3']], rows=rows)
    with open(f'bounds-{M}.md', 'w') as f:
        f.write(f"# Z_{M} = {p}²·{q}²: every pattern between two bounds that need no solver\n\n"
                f"*Made by `status.py`. 'exponents' writes the pattern as pairs uv for the divisors {p}^u·{q}^v. LB is the lower bound of `lowerbound.py` (the two theorems and divisibility). U is the upper bound of `algebra2.py` (five moves), "
                "and `realise2.py` has built a multiset of that size with exactly the pattern for every row. 'smallest known' is the smaller of U and what a programme found. The least size is given where it is known: "
                "proved by a programme, or because LB equals the smallest size known. The last column gives the bound from the first three moves alone (`algebra.py`) and an expression of that cost: `coset of cZ_N` is a coset of cZ_N lifted to Z_M, `*` is convolution, `+` is a sum of translates, "
                "`[...] mod N` is reduction modulo N followed by a lift.*\n\n"
                "| pattern | exponents | LB | least size | smallest known | U | least size known by | where it sits | three moves alone: cost and expression |\n|---|---|---|---|---|---|---|---|---|\n" + '\n'.join(lines) + '\n')
json.dump(out, open('status.json', 'w'))
for M in out: print(M, out[M]['counts'], 'LB = U:', out[M]['LB_eq_U'])
