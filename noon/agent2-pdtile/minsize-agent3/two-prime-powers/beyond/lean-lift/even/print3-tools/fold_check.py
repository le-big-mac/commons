# usage: python3 -I fold_check.py B144926.txt
# Checks  a(n) <= 2*F(n)  for even n in the OEIS table of A144926, where
#   a(n) = number of singular n x n (-1,1)-circulants (from the table, untrusted input: parsed as integers only),
#   F(n) = number of sign vectors of length n whose folding modulo n' (n = 2^k n', n' odd) gives a singular circulant
#          of order n'  (computed here, not from the OEIS).
# F(n): exact formula when n' = 1 or n' prime; exhaustive enumeration over folded vectors when (2^k+1)^n' <= LIMIT.
import sys, math
import numpy as np
LIMIT = 20_000_000

def cyclo(d):
    # integer coefficient list (low to high) of the d-th cyclotomic polynomial, by exact division
    def polydiv(a, b):
        a = a[:]; q = [0] * (len(a) - len(b) + 1)
        for i in range(len(a) - len(b), -1, -1):
            q[i] = a[i + len(b) - 1] // b[-1]
            for j, bj in enumerate(b):
                a[i + j] -= q[i] * bj
        assert all(x == 0 for x in a)
        return q
    p = [-1] + [0] * (d - 1) + [1]
    for e in range(1, d):
        if d % e == 0:
            p = polydiv(p, cyclo(e))
    return p

def red_matrix(d, m):
    # rows: coefficients of X^j mod Phi_d, j = 0..m-1 ; shape (m, phi(d))
    phi = cyclo(d); deg = len(phi) - 1
    rows = []
    cur = [0] * deg
    if deg > 0: cur[0] = 1
    for j in range(m):
        if j == 0:
            cur = [1] + [0] * (deg - 1) if deg > 0 else []
        else:
            top = cur[-1]
            cur = [0] + cur[:-1]
            for i in range(deg):
                cur[i] -= top * phi[i]
        rows.append(cur[:])
    return np.array(rows, dtype=np.int64)

def F_formula(n):
    k = 0; m = n
    while m % 2 == 0: m //= 2; k += 1
    q = 2 ** k
    w = [math.comb(q, t) for t in range(q + 1)]          # value s = 2t - q
    if m == 1:
        return math.comb(n, n // 2), "n' = 1: binomial(n, n/2)"
    if all(m % t for t in range(2, m)):
        return math.comb(n, n // 2) + sum(x ** m for x in w) - w[q // 2] ** m, "n' prime: binomial(n,n/2) + sum_s w(s)^n' - w(0)^n'"
    return None, ""

def F_enum(n):
    k = 0; m = n
    while m % 2 == 0: m //= 2; k += 1
    q = 2 ** k
    base = q + 1
    total = base ** m
    if total > LIMIT:
        return None
    w = np.array([math.comb(q, t) for t in range(q + 1)], dtype=np.int64)
    mats = [red_matrix(d, m) for d in range(1, m + 1) if m % d == 0]
    count = 0
    chunk = 1_000_000
    for start in range(0, total, chunk):
        idx = np.arange(start, min(total, start + chunk), dtype=np.int64)
        digs = np.empty((len(idx), m), dtype=np.int64)
        x = idx.copy()
        for j in range(m):
            digs[:, j] = x % base; x //= base
        vals = 2 * digs - q
        wt = np.prod(w[digs], axis=1)
        bad = np.zeros(len(idx), dtype=bool)
        for M in mats:
            bad |= ~np.any(vals @ M, axis=1)
        count += int(wt[bad].sum())
    return count

a = {}
for line in open(sys.argv[1], encoding="ascii", errors="replace"):
    parts = line.split()
    if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
        a[int(parts[0])] = int(parts[1])
print("terms read:", len(a), "n from", min(a), "to", max(a))
print("%3s %3s %18s %18s %20s %6s  %s" % ("n", "n'", "a(n) listed", "F(n) computed", "2*F(n)", "ok", "how F was had"))
for n in sorted(a):
    if n < 2 or n % 2: continue
    m = n
    while m % 2 == 0: m //= 2
    f, how = F_formula(n)
    e = F_enum(n)
    if f is not None and e is not None:
        how += " ; enumeration agrees" if f == e else " ; ENUMERATION DISAGREES (%d)" % e
    if f is None and e is not None:
        f, how = e, "enumeration of folded vectors"
    if f is None:
        print("%3d %3d %18d %18s %20s %6s  %s" % (n, m, a[n], "-", "-", "-", "not computed (too many folded vectors, n' composite)"))
        continue
    print("%3d %3d %18d %18d %20d %6s  %s" % (n, m, a[n], f, 2 * f, "yes" if a[n] <= 2 * f else "NO", how))
