# steps_check.py -- the counting facts used in the proof of Theorem P.
import itertools, sys
from math import comb
# (1) for p odd, q an odd prime not dividing p (or q = 0 for the rationals):
#     #{sign vectors s : <s, s0> = 0 in F} + 2 <= 2^(p-1)
worst = 0
for p in range(3, 202, 2):
    for q in [0] + [r for r in range(3, 420, 2) if all(r % t for t in range(3, int(r ** 0.5) + 1, 2))]:
        if q and p % q == 0: continue
        tot = sum(comb(p, j) for j in range(p + 1) if ((p - 2 * j) % q == 0 if q else p - 2 * j == 0))
        assert tot + 2 <= 2 ** (p - 1), (p, q, tot)
        worst = max(worst, (tot + 2) / 2 ** (p - 1))
print("(1) #(s orthogonal to a sign vector) + 2 <= 2^(p-1): all odd p <= 201, all odd primes q < 420 not dividing p, and q = 0; largest ratio %.4f" % worst)
# (2) K = line F*kappa, K-perp = hyperplane: number of sign vectors in the union <= 2^(p-1); all kappa, small p, q
for p, q in [(3, 5), (3, 7), (3, 11), (5, 3), (5, 7), (5, 11), (7, 3), (7, 5)]:
    signs = list(itertools.product([1, -1], repeat=p)); mx = 0
    seen = set()
    for kappa in itertools.product(range(q), repeat=p):
        if not any(kappa): continue
        # normalise: first nonzero entry 1
        i0 = next(i for i in range(p) if kappa[i]); inv = pow(kappa[i0], -1, q)
        kn = tuple(k * inv % q for k in kappa)
        if kn in seen: continue
        seen.add(kn)
        on_line = sum(1 for s in signs if any(all((s[i] - lam * kn[i]) % q == 0 for i in range(p)) for lam in (1, q - 1)) or
                      all((s[i] * kn[0] - s[0] * kn[i]) % q == 0 for i in range(p)) and kn[0] != 0)
        # exact: s on the line iff s = lam*kn for some lam
        on_line = sum(1 for s in signs if any(all((s[i] - lam * kn[i]) % q == 0 for i in range(p)) for lam in range(1, q)))
        perp = sum(1 for s in signs if sum(s[i] * kn[i] for i in range(p)) % q == 0)
        both = sum(1 for s in signs if sum(s[i] * kn[i] for i in range(p)) % q == 0 and any(all((s[i] - lam * kn[i]) % q == 0 for i in range(p)) for lam in range(1, q)))
        mx = max(mx, on_line + perp - both)
    assert mx <= 2 ** (p - 1), (p, q, mx)
    print("(2) p = %d over F_%d: all %d lines; most sign vectors in (line) u (its orthogonal hyperplane): %d <= %d" % (p, q, len(seen), mx, 2 ** (p - 1)))
    sys.stdout.flush()
# (3) the case k = 1 by enumeration: every nonzero f in F_q^p has at least 2^(p-1) good sign vectors
for p, q in [(3, 5), (3, 7), (3, 11), (5, 3), (5, 7), (7, 3)]:
    signs = list(itertools.product([1, -1], repeat=p)); least = 2 ** p
    for f in itertools.product(range(q), repeat=p):
        if not any(f): continue
        g = 0
        for s in signs:
            v = [s[i] * f[i] % q for i in range(p)]
            if sum(v) % q != 0 and len(set(v)) > 1: g += 1
        least = min(least, g)
    assert least >= 2 ** (p - 1)
    print("(3) p = %d over F_%d: least number of good sign vectors over all nonzero f: %d >= %d" % (p, q, least, 2 ** (p - 1)))
    sys.stdout.flush()
