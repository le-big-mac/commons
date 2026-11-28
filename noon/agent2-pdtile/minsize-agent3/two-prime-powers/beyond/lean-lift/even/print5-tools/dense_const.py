import sys, math
# usage: python3 -I dense_const.py B144926_FILE
# For full support (every residue once, m = n) the bad share is a(n)/2^n, a(n) = OEIS A144926.
# Prints share*sqrt(n) for even n (beside 2*sqrt(2/pi) = 1.5958 and beside 2*C(n,n/2)/2^n*sqrt(n)),
# and share*n for odd n (beside the Corollary-1 asymptotic (1/sqrt p)(2p/(pi n))^((p-1)/2) for smallest prime p).
rows = []
for line in open(sys.argv[1], encoding="ascii", errors="replace"):
    parts = line.split()
    if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
        rows.append((int(parts[0]), int(parts[1])))
def spf(n):
    p = 2
    while p * p <= n:
        if n % p == 0: return p
        p += 1
    return n
print("limit constant for even n: 2*sqrt(2/pi) =", round(2 * math.sqrt(2 / math.pi), 4), " one element repeated: sqrt(2/pi) =", round(math.sqrt(2 / math.pi), 4))
mx_even = (0, 0); mx_all = (0, 0)
for n, a in rows:
    if n < 2: continue
    share = a / 2 ** n
    if n % 2 == 0:
        two = 2 * math.comb(n, n // 2) / 2 ** n
        print(f"n={n:2d} even share={share:.6f} share*sqrt(n)={share*math.sqrt(n):.4f}  2*C(n,n/2)/2^n*sqrt(n)={two*math.sqrt(n):.4f}")
        if share * math.sqrt(n) > mx_even[1]: mx_even = (n, share * math.sqrt(n))
    else:
        p = spf(n)
        asym = (1 / math.sqrt(p)) * (2 * p / (math.pi * n)) ** ((p - 1) / 2) if p < n else float('nan')
        print(f"n={n:2d} odd  share={share:.3e} share*sqrt(n)={share*math.sqrt(n):.4e} share*n={share*n:.4f} p={p} Cor1-asymptotic*n={asym*n:.4f}")
print("largest share*sqrt(n) over even n:", mx_even)
