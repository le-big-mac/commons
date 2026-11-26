"""(A1)-(A5) of Section 3.1 by enumeration.  Sets are built from the definitions up to a bound."""
import itertools
from lib import in_S, in_Sp, in_Q

BOUND = 400
res = {}
counts = {}
fails = []


def note(name, ok, info):
    counts[name] = counts.get(name, 0) + 1
    if not ok:
        fails.append((name, info))


used_prime = {"A4_needs_q_div": 0, "A5_needs_q_div": 0, "A4_Q_only": 0, "A4_Sp_only": 0}
for p, q in itertools.permutations([2, 3, 5, 7, 11], 2):
    for u in range(0, 5):
        P = p ** u
        if q * P * 2 > BOUND and u > 1:
            continue
        S = [x for x in range(0, BOUND + 1) if in_S(x, p, q, u)]
        Sp = [x for x in range(0, BOUND + 1) if in_Sp(x, p, q, u)]
        Q = [x for x in range(0, BOUND + 1) if in_Q(x, p, q, u)]
        # independent construction of the same sets, straight from the displayed definitions
        S2 = sorted({P * t + q * m for t in range(1, BOUND // P + 1) for m in range(0, BOUND // q + 1) if P * t + q * m <= BOUND})
        Sp2 = sorted({P * t + q * m for t in range(1, BOUND // P + 1) for m in range(1, BOUND // q + 1) if P * t + q * m <= BOUND})
        Q2 = sorted({q * P * t for t in range(1, BOUND // (q * P) + 1)})
        assert S == S2 and Sp == Sp2 and Q == Q2
        Sset, Spset, Qset = set(S), set(Sp), set(Q)
        qm0 = [q * m for m in range(0, BOUND // q + 1)]
        qm1 = qm0[1:]
        if u >= 1:
            Sm = [x for x in range(0, BOUND + 1) if in_S(x, p, q, u - 1)]
            Spm = [x for x in range(0, BOUND + 1) if in_Sp(x, p, q, u - 1)]
            Qm = [x for x in range(0, BOUND + 1) if in_Q(x, p, q, u - 1)]
            for x in Sm:
                if p * x <= BOUND:
                    note("A1a", p * x in Sset, (p, q, u, x))
            for x in Spm:
                if p * x <= BOUND:
                    note("A1b", p * x in Spset, (p, q, u, x))
            for x in Qm:
                if p * x <= BOUND:
                    note("A1c", p * x in Qset, (p, q, u, x))
        for x in S:
            for y in S:
                if x + y <= BOUND:
                    note("A2a S+S in S", x + y in Sset, (p, q, u, x, y))
            for y in qm0:
                if x + y <= BOUND:
                    note("A2b S+qZ>=0 in S", x + y in Sset, (p, q, u, x, y))
            for y in qm1:
                if x + y <= BOUND:
                    note("A2e S+qZ>=1 in S+", x + y in Spset, (p, q, u, x, y))
        for x in Sp:
            for y in S:
                if x + y <= BOUND:
                    note("A2c S+ + S in S+", x + y in Spset, (p, q, u, x, y))
            for y in qm0:
                if x + y <= BOUND:
                    note("A2d S+ + qZ>=0 in S+", x + y in Spset, (p, q, u, x, y))
        for x in Q:
            for y in S:
                if x + y <= BOUND:
                    note("A3a Q+S in S+", x + y in Spset, (p, q, u, x, y))
            for y in qm1:
                if x + y <= BOUND:
                    note("A3b Q+qZ>=1 in S+", x + y in Spset, (p, q, u, x, y))
        for x in S:
            if x % q == 0:
                note("A4 member", (x in Qset) or (x in Spset), (p, q, u, x))
                note("A4 bound", x >= q * P, (p, q, u, x))
                if x in Qset and x not in Spset:
                    used_prime["A4_Q_only"] += 1
                if x in Spset and x not in Qset:
                    used_prime["A4_Sp_only"] += 1
            else:
                if x < q * P or not ((x in Qset) or (x in Spset)):
                    used_prime["A4_needs_q_div"] += 1
        for x in Sp:
            if x % q == 0:
                note("A5", x >= q * P + q, (p, q, u, x))
            elif x < q * P + q:
                used_prime["A5_needs_q_div"] += 1

print("bound on integers:", BOUND, " pairs (p,q): ordered pairs of distinct primes from 2,3,5,7,11; u = 0..4 while q p^u * 2 <= bound (u<=1 always)")
for k in sorted(counts):
    print(f"{k:28s} instances {counts[k]:9d}")
print("failures:", len(fails), fails[:10])
print("hypothesis exercised:", used_prime)

# (A4)/(A5) with q not coprime to p would fail; show that coprimality is what is used (q composite but coprime to p is fine)
bad = []
for p, q in [(2, 4), (2, 6), (3, 6), (2, 9), (3, 4), (2, 15), (4, 9)]:
    for u in range(0, 4):
        P = p ** u
        for x in range(1, 300):
            if in_S(x, p, q, u) and x % q == 0:
                if not (x >= q * P and (in_Q(x, p, q, u) or in_Sp(x, p, q, u))):
                    bad.append((p, q, u, x))
print("non-coprime or composite (p,q) where (A4) fails (first few):", bad[:8])
print("pairs with a failure:", sorted({(a, b) for a, b, _, _ in bad}))
