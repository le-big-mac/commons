"""Is the upper bound U honest?  For every pattern of Z_M (M = 36, 100, 225) build a multiset from the expression of cost U found by
algebra.py: a coset of cZ_N lifted to Z_M with random lifts; convolution; sum with a random translate; reduction modulo N and a random
lift.  Check its pattern by exact division.  Up to TRIES attempts with fresh random choices.  Writes realised-M.jsonl (one multiset
of size U for each pattern, where found) and prints the count.   usage: realise.py [tries] [seed]"""
import sys, json, random, re
sys.path.insert(0, '/home/agent3/pq2/rule')
from algebra import closure
from sympy import Poly, cyclotomic_poly, symbols, ZZ
X = symbols('X')
TRIES = int(sys.argv[1]) if len(sys.argv) > 1 else 40; random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
def build(m, how, M):
    h = how[m]
    if isinstance(h, str):
        c, N = map(int, re.match(r'coset of (\d+)Z_(\d+)', h).groups()); x0 = random.randrange(N)
        return [((x0 + c * j) % N + N * random.randrange(M // N)) % M for j in range(N // c)]
    if h[0] == 'L':
        N = h[2]; return [(x % N + N * random.randrange(M // N)) % M for x in build(h[1], how, M)]
    A, B = build(h[1], how, M), build(h[2], how, M)
    if h[0] == 'x': return [(a + b) % M for a in A for b in B]
    t = random.randrange(M); return A + [(b + t) % M for b in B]
for M, p, q in ((36, 2, 3), (100, 2, 5), (225, 3, 5)):
    divs, mask, U, how = closure(p, q)
    PHI = {d: Poly(cyclotomic_poly(d, X), X, domain=ZZ) for d in divs}
    def pattern(els):
        v = [0] * M
        for x in els: v[x] += 1
        A = Poly(sum(w * X**i for i, w in enumerate(v) if w), X, domain=ZZ)
        return [d for d in divs if A.rem(PHI[d]).is_zero]
    ok = 0; fails = []; tries_used = []
    with open(f'realised-{M}.jsonl', 'w') as f:
        for m in range(1 << len(divs)):
            D = [d for i, d in enumerate(divs) if m >> i & 1]
            for t in range(1, TRIES + 1):
                els = build(m, how, M)
                assert len(els) == U[m]
                if pattern(els) == D:
                    ok += 1; tries_used.append(t)
                    v = [0] * M
                    for x in els: v[x] += 1
                    f.write(json.dumps(dict(M=M, D=D, size=U[m], attempts=t, multiset=' '.join(f'{i}^{w}' if w > 1 else str(i) for i, w in enumerate(v) if w))) + '\n'); break
            else: fails.append((D, U[m]))
    print(f'Z_{M}: {ok} of {1 << len(divs)} patterns realised with exactly U elements; attempts needed: at most {max(tries_used)}, first attempt in {sum(1 for t in tries_used if t == 1)}; not realised in {TRIES} attempts: {fails}', flush=True)
