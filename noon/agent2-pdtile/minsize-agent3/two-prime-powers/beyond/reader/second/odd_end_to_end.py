"""Second pass: the consequence drawn from the two lemmas, tested end to end.
For p, q odd: build, for EVERY pattern of Z_{p^2 q^2}, a multiset from the three-move expression that the note's algebra.py records,
with no random choice and no retry: every lift is the lemma's lift (one element moved up, once for each prime of M/N), every sum
takes the first translate that lets no divisor in (the second lemma says there is one).  One multiset is built for each pattern and
used again wherever an expression needs that pattern (that is the induction: a step asks of its inputs only their exact patterns).
Checked at every node: size = cost, pattern exactly as computed.  Also counted: the translates that let a divisor in, against
sigma(M) - M.   usage: odd_end_to_end.py p q"""
import sys, re
sys.path.insert(0, '/home/agent3/pq2/rule/reader'); sys.path.insert(1, '/home/agent3/pq2/rule'); sys.dont_write_bytecode = True
from pat import pattern, divisors, primes_of
from algebra import closure
p, q = int(sys.argv[1]), int(sys.argv[2]); M = p * p * q * q
divs, mask, U, how = closure(p, q)
def pat(v, N): return pattern(v, N, routes=2)
def lemma_lift(v, N, r):
    """multiset v on Z_N (count vector) -> Z_{N r}, r an odd prime: second coordinate (mod r^(k+1)) in [0, r^k), one element moved up by r^k"""
    assert r % 2 == 1
    rk = 1
    while (N // rk) % r == 0: rk *= r
    out = [0] * (N * r); moved = False
    for x, w in enumerate(v):
        for _ in range(w):
            top = 0 if moved else 1; moved = True
            y = next(x + N * t for t in range(r) if (x + N * t) % (rk * r) == x % rk + top * rk)
            out[y] += 1
    return out
def lift_to_M(v, N):
    while N < M:
        r = next(t for t in (p, q) if (M // N) % t == 0); v = lemma_lift(v, N, r); N *= r
    return v
built = {}; stats = dict(nodes=0, sums=0, worst_bad=0, lifts=0)
def D_of(m): return [d for i, d in enumerate(divs) if m >> i & 1]
def build(m):
    if m in built: return built[m]
    h = how[m]
    if isinstance(h, str):
        c, N = map(int, re.match(r'coset of (\d+)Z_(\d+)', h).groups())
        v = [0] * N
        for j in range(N // c): v[c * j] += 1
        out = lift_to_M(v, N); stats['lifts'] += 1
    elif h[0] == 'L':
        N = h[2]; a = build(h[1]); v = [0] * N
        for x, w in enumerate(a): v[x % N] += w
        out = lift_to_M(v, N); stats['lifts'] += 1
    elif h[0] == 'x':
        a, b = build(h[1]), build(h[2]); out = [0] * M
        for x, wa in enumerate(a):
            if wa:
                for y, wb in enumerate(b):
                    if wb: out[(x + y) % M] += wa * wb
    else:
        a, b = build(h[1]), build(h[2]); want = D_of(h[1] & h[2]); good = None; bad = 0
        for t in range(M):
            s = [a[x] + b[(x - t) % M] for x in range(M)]
            if pat(s, M) == want:
                if good is None: good = s
            else: bad += 1
        assert good is not None, 'no translate keeps the pattern'
        assert bad <= sum(M // d for d in divs) < M
        stats['sums'] += 1; stats['worst_bad'] = max(stats['worst_bad'], bad); out = good
    assert sum(out) == U[m] and pat(out, M) == D_of(m), (D_of(m), sum(out), U[m], pat(out, M))
    stats['nodes'] += 1; built[m] = out; return out
for m in range(1 << len(divs)): build(m)
print(f'Z_{M} (p = {p}, q = {q}): {len(built)} of {1 << len(divs)} patterns built from their three-move expressions with exactly U3 elements and exactly the pattern, no retry; '
      f'{stats["lifts"]} lemma lifts, {stats["sums"]} sums; most translates that let a divisor in: {stats["worst_bad"]} (sigma(M) - M = {sum(M // d for d in divs)}, M = {M})')
