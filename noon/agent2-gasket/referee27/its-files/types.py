"""Work out chi_2 for each gasket from the paper's Definition (def:chi), using tangent pairs
with coprime curvatures (rho = a+b), over many pairs, and check it is constant.
Also chi_4 for the circle of curvature 49 in (-23,48,49,52) from the lattice of its quadratic form."""
from math import gcd

def kron(a, n):
    """Kronecker symbol (a/n) for n > 0."""
    assert n > 0
    if n == 1:
        return 1
    res = 1
    v = 0
    while n % 2 == 0:
        n //= 2; v += 1
    if v:
        if a % 2 == 0:
            return 0
        if v % 2 == 1 and a % 8 in (3, 5):
            res = -res
    # Jacobi symbol (a/n), n odd
    a %= n
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                res = -res
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            res = -res
        a %= n
    return res if n == 1 else 0

def chi2_circle(n, rho):
    if n % 4 in (0, 1):
        return kron(rho, n)
    if n % 4 == 2:
        return kron(-rho, n // 2)
    return kron(2 * rho, n)

def pairs(q, depth):
    out = set()
    stack = [(tuple(q), 0)]
    seen = set()
    while stack:
        Q, d = stack.pop()
        key = tuple(sorted(Q))
        if key in seen:
            continue
        seen.add(key)
        for i in range(4):
            for j in range(i + 1, 4):
                out.add((min(Q[i], Q[j]), max(Q[i], Q[j])))
        if d < depth:
            s = sum(Q)
            for i in range(4):
                n = 2 * (s - Q[i]) - Q[i]
                if n > Q[i]:
                    stack.append((Q[:i] + (n,) + Q[i + 1:], d + 1))
    return out

if __name__ == '__main__':
    for q in [(-3, 5, 8, 8), (-4, 5, 20, 21), (-1, 2, 2, 3), (0, 0, 1, 1), (-3, 4, 12, 13), (-2, 3, 6, 7), (-23, 48, 49, 52)]:
        vals = {}
        npairs = 0
        for a, b in pairs(q, 7):
            if a <= 0 or b <= 0 or gcd(a, b) != 1:
                continue
            npairs += 1
            for n in (a, b):
                v = chi2_circle(n, a + b)
                vals[v] = vals.get(v, 0) + 1
        print(q, 'coprime positive tangent pairs used:', npairs, 'chi_2 values seen (value: count):', vals)
    # chi_4 for the circle 49 in (-23,48,49,52): form (a+b)x^2+(a+b+c-d)xy+(a+c)y^2 with a=49,(b,c,d)=(-23,48,52)
    a, b, c, d = 49, -23, 48, 52
    A, B, C = a + b, a + b + c - d, a + c
    print('form', A, B, C, 'disc', B * B - 4 * A * C, '= -4*49^2 =', -4 * 49 * 49)
    # find beta, delta in Z[i] with N(beta)=A, N(delta)=C, 2Re(beta conj(delta))=B
    sols = []
    for x in range(-12, 13):
        for y in range(-12, 13):
            if x * x + y * y == A:
                for u in range(-12, 13):
                    for v in range(-12, 13):
                        if u * u + v * v == C and 2 * (x * u + y * v) == B:
                            sols.append(((x, y), (u, v)))
    print('lattice bases (beta, delta):', len(sols), sols[:4])
    def mulmod(p, q, m):
        return ((p[0] * q[0] - p[1] * q[1]) % m, (p[0] * q[1] + p[1] * q[0]) % m)
    def powmod(p, e, m):
        r = (1, 0)
        for _ in range(e):
            r = mulmod(r, p, m)
        return r
    res = set()
    for (beta, delta) in sols:
        # every element x*beta+y*delta coprime to 49 (norm not divisible by 7), small x,y
        for x in range(-3, 4):
            for y in range(-3, 4):
                e = (x * beta[0] + y * delta[0], x * beta[1] + y * delta[1])
                if (e[0] ** 2 + e[1] ** 2) % 7 == 0:
                    continue
                s = powmod(e, 12, 7)        # [e/7] = e^((49-1)/4) mod 7
                s2 = mulmod(s, s, 7)        # [e/49] = [e/7]^2
                res.add((s, s2))
    print('([e/7], [e/49]) over lattice elements coprime to 7, as residues mod 7 (x,y) = x+yi:', sorted(res),
          ' note (6,0) is -1, (0,1) is i, (0,6) is -i')
