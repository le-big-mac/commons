"""Is U2 (algebra2.py) honest?  Build, for every pattern of Z_36, Z_100 and Z_225, a multiset from the derivation of cost U2, with random
lifts and translates, and check its pattern by exact division.  Up to TRIES attempts.  Writes realised2-M.jsonl.   usage: realise2.py [tries] [seed]"""
import sys, json, random, math
sys.path.insert(0, '/home/agent3/pq2/rule')
from algebra2 import Calc, divisors
from sympy import Poly, cyclotomic_poly, symbols, ZZ
X = symbols('X')
TRIES = int(sys.argv[1]) if len(sys.argv) > 1 else 60; random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
def lift(els, N1, N): return [(x % N1 + N1 * random.randrange(N // N1)) % N for x in els]
def build(C, N, P, s, how=None):
    h = how if how is not None else (C.how[P] if N == C.M else C.S[N][P][s])
    k = h[0]
    if k == 'atom':
        N1, c = h[1], h[2]; x0 = random.randrange(N1); return lift([(x0 + c * j) % N1 for j in range(N1 // c)], N1, N)
    if k == 'lift': return lift(build(C, h[1], h[2], h[3]), h[1], N)
    if k == 'L': return lift(build(C, N, h[2], h[3]), h[1], N)
    if k in ('+', 'x'):
        A, B = build(C, N, h[1], h[2]), build(C, N, h[3], h[4])
        if k == 'x': return [(a + b) % N for a in A for b in B]
        t = random.randrange(N); return A + [(b + t) % N for b in B]
    if k == 'dil':
        c, K, T, w = h[1:]; t = random.randrange(N); return [(c * b + t) % N for b in build(C, K, T, w)]
    if k == 'stack':
        c, K, membs, w = h[1:]; out = []
        order = list(membs) + [random.choice(membs) for _ in range(c - len(membs))]; random.shuffle(order)
        for r, T in enumerate(order):
            t = random.randrange(K); out += [(r + c * ((b + t) % K)) % N for b in build(C, K, T, w)]
        return out
    raise ValueError(h)
for M, p, q in ((36, 2, 3), (100, 2, 5), (225, 3, 5)):
    C = Calc(p, q); divs = [d for d in divisors(M) if d > 1]
    PHI = {d: Poly(cyclotomic_poly(d, X), X, domain=ZZ) for d in divs}
    def pattern(els):
        v = [0] * M
        for x in els: v[x] += 1
        A = Poly(sum(w * X**i for i, w in enumerate(v) if w), X, domain=ZZ)
        return frozenset(d for d in divs if A.rem(PHI[d]).is_zero)
    ok = 0; fails = []; first = 0; mx = 0
    with open(f'realised2-{M}.jsonl', 'w') as f:
        for P in sorted(C.U, key=lambda P: (len(P), sorted(P))):
            for t in range(1, TRIES + 1):
                els = build(C, M, P, C.U[P]); assert len(els) == C.U[P]
                if pattern(els) == P:
                    ok += 1; first += (t == 1); mx = max(mx, t)
                    v = [0] * M
                    for x in els: v[x] += 1
                    f.write(json.dumps(dict(M=M, D=sorted(P), size=C.U[P], attempts=t, last_move=C.how[P][0], multiset=' '.join(f'{i}^{w}' if w > 1 else str(i) for i, w in enumerate(v) if w))) + '\n'); break
            else: fails.append((sorted(P), C.U[P], C.how[P][0]))
    print(f'Z_{M}: {ok} of {len(C.U)} patterns realised with exactly U2 elements; attempts needed: at most {mx}, first attempt in {first}; not realised in {TRIES} attempts: {fails}', flush=True)
