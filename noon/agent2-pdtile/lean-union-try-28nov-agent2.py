"""exhaust.py -- the two statements of union-lean tried by exhaustion on small cases, from their Lean text and the library's
definitions (sg, P, BadAt of Pnq/SignDefs.lean; csum, levelBad of Pnq/EvenTwice.lean), in a program of my own (Noon, 28 Nov 2026).
  U: #{eps : exists c, exists j <= K, levelBad pos (val c) eps j}  <=  2 * #{eps : exists c, levelBad pos (val c) eps 0}
  W: #{eps : exists d | 2^k n', Phi_d | P e eps}  <=  2 * #{eps : exists d | n', Phi_d | P e eps}        (n' odd)
Values for U are vectors of small integers (the group Z^2), or residues modulo 2, 3, 4 or 6 (a group with torsion, where
sg(eps) . v = -v may equal v).  Divisibility by Phi_d is exact, in whole numbers.      python -I exhaust.py"""
import itertools, random, sys
def level_bad(pos, val, eps, j, add, zero, neg):
    sgn = lambda k: val[k] if eps[k] else neg(val[k])
    if j == 0:
        t = zero
        for k in range(len(pos)): t = add(t, sgn(k))
        return t == zero
    M = 2 ** j; half = 2 ** (j - 1)
    def csum(r):
        t = zero
        for k in range(len(pos)):
            if pos[k] % M == r: t = add(t, sgn(k))
        return t
    return all(csum(r) == csum(r + half) for r in range(half))
def groups():
    yield 'Z^2', (lambda a, b: (a[0] + b[0], a[1] + b[1])), (0, 0), (lambda a: (-a[0], -a[1])), lambda rnd: (rnd.randint(-2, 2), rnd.randint(-2, 2))
    for q in (2, 3, 4, 6):
        yield 'Z/%d' % q, (lambda a, b, q=q: (a + b) % q), 0, (lambda a, q=q: (-a) % q), (lambda rnd, q=q: rnd.randrange(q))
def try_U(trials, seed):
    rnd = random.Random(seed); n = worst = tight = 0; emptyk = 0
    for t in range(trials):
        name, add, zero, neg, draw = rnd.choice(list(groups())); m = rnd.randint(0, 9); K = rnd.randint(0, 4); nc = rnd.randint(0, 3)
        pos = [rnd.randrange(2 ** rnd.randint(0, 5)) for _ in range(m)]; vals = [[draw(rnd) for _ in range(m)] for _ in range(nc)]
        lhs = rhs = 0
        for eps in itertools.product((False, True), repeat=m):
            b0 = any(level_bad(pos, v, eps, 0, add, zero, neg) for v in vals); rhs += b0
            lhs += b0 or any(level_bad(pos, v, eps, j, add, zero, neg) for v in vals for j in range(1, K + 1))
        n += 1; emptyk += nc == 0
        if lhs > 2 * rhs: print('U FAILS:', name, m, K, pos, vals, lhs, rhs); return False
        if rhs and lhs == 2 * rhs and lhs < 2 ** m: tight += 1
        if rhs: worst = max(worst, lhs / rhs)
    print('U: %d cases (groups Z^2, Z/2, Z/3, Z/4, Z/6; 0 to 9 elements; K 0 to 4; 0 to 3 systems of values, %d of them with none), none against it; the largest ratio met %.3f; equality with fewer than all signings bad in %d' % (n, emptyk, worst, tight)); return True
def cyclo(d, memo={}):
    if d in memo: return memo[d]
    p = [-1] + [0] * (d - 1) + [1]                      # x^d - 1, lowest degree first
    for t in range(1, d):
        if d % t == 0: p = divide(p, cyclo(t))[0]
    memo[d] = p; return p
def divide(p, q):
    p = p[:]; out = [0] * max(1, len(p) - len(q) + 1)
    for i in range(len(p) - len(q), -1, -1):
        c = p[i + len(q) - 1]; assert q[-1] == 1; out[i] = c
        for j, qc in enumerate(q): p[i + j] -= c * qc
    return out, p[:len(q) - 1]
def bad_at(e, eps, d):
    p = [0] * d
    for k, x in enumerate(e): p[x % d] += 1 if eps[k] else -1          # x^d = 1 modulo Phi_d
    q = cyclo(d)
    if len(p) < len(q): return not any(p)
    return not any(divide(p, q)[1])
def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]
def try_W(trials, seed):
    rnd = random.Random(seed); n = tight = 0; worst = 0
    for t in range(trials):
        m = rnd.randint(0, 10); k = rnd.randint(0, 3); n1 = rnd.choice([1, 1, 3, 3, 5, 7, 9, 15]); N = 2 ** k * n1
        e = [rnd.randrange(rnd.choice([N, 2 * N, 40])) for _ in range(m)]; D = divisors(N); D1 = divisors(n1); lhs = rhs = 0
        for eps in itertools.product((False, True), repeat=m):
            b1 = any(bad_at(e, eps, d) for d in D1); rhs += b1; lhs += b1 or any(bad_at(e, eps, d) for d in D)
        n += 1
        if lhs > 2 * rhs: print('W FAILS:', m, k, n1, e, lhs, rhs); return False
        if rhs and lhs == 2 * rhs and lhs < 2 ** m: tight += 1
        if rhs: worst = max(worst, lhs / rhs)
    print('W: %d cases (0 to 10 elements, exponents repeated or not and not reduced; k 0 to 3; n\' in 1, 3, 5, 7, 9, 15), none against it; the largest ratio met %.3f; equality with fewer than all signings bad in %d' % (n, worst, tight)); return True
def self_test():
    """the program's own parts, on cases worked by hand"""
    assert cyclo(1) == [-1, 1] and cyclo(2) == [1, 1] and cyclo(6) == [1, -1, 1] and cyclo(12) == [1, 0, -1, 0, 1] and cyclo(15) == [1, -1, 0, 1, -1, 1, 0, -1, 1]
    assert bad_at([0, 1], (True, False), 1) and not bad_at([0, 1], (True, True), 1) and bad_at([0, 1], (True, True), 2) and bad_at([0, 2, 4], (True, True, True), 3) and not bad_at([0, 2, 4], (True, True, False), 3)
    assert bad_at([0, 3], (True, True), 6) and bad_at([0, 2], (True, True), 4) and not bad_at([0, 1], (True, True), 4) and bad_at([], (), 7)
    add = lambda a, b: a + b; neg = lambda a: -a
    assert level_bad([0, 1], [5, 5], (True, False), 0, add, 0, neg) and not level_bad([0, 1], [5, 5], (True, True), 0, add, 0, neg) and level_bad([0, 1], [5, 5], (True, True), 1, add, 0, neg) and not level_bad([0, 1], [5, 5], (True, False), 1, add, 0, neg)
    assert level_bad([0, 2, 1, 3], [1, 1, 2, 2], (True, True, False, False), 2, add, 0, neg) and not level_bad([0, 2, 1, 3], [1, 1, 2, 2], (True, False, True, True), 2, add, 0, neg) and level_bad([], [], (), 0, add, 0, neg)
    # a statement that is false must be seen to fail: "at most ONCE" in place of twice
    e = [0, 1]; lhs = sum(any(bad_at(e, eps, d) for d in (1, 2)) for eps in itertools.product((False, True), repeat=2)); rhs = sum(bad_at(e, eps, 1) for eps in itertools.product((False, True), repeat=2)); assert lhs == 4 and rhs == 2
    print('self-test: cyclotomic polynomials, divisibility and the levels agree with cases worked by hand; with exponents 0, 1 the count is 4 against 2, so "at most once" would fail and "twice" is met with equality')
if __name__ == '__main__':
    self_test(); ok = try_U(4000, 'noon-U-1') and try_W(1500, 'noon-W-1'); sys.exit(0 if ok else 1)
