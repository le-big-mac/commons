# Corollary K, directly: multisets of 5, 7, 9 elements on Z_n with 4 | n and 15 | n (the region (II) and around it).
# For each: all signings exactly; share of bad signings <= R (first-order sum of the first result, computed from B mod n');
# R < 1; a good signing exists.
import sys, random
from fractions import Fraction as Fr
sys.path.insert(0, '/home/agent3/lean/lift-check/even/prover2')
from lib2 import *
from propK import R_values
from ranks import factor
rnd = random.Random(41)
for n in [60, 120, 180, 420, 840, 1260, 660, 2100]:
    k, n1 = two_part(n)
    f = factor(n1)
    st = {5: [0, Fr(0), Fr(0)], 7: [0, Fr(0), Fr(0)], 9: [0, Fr(0), Fr(0)]}
    for t in range(240):
        m = (5, 7, 9)[t % 3]
        kind = (t // 3) % 4
        if kind == 0: B = [rnd.randrange(n) for _ in range(m)]
        elif kind == 1:      # a coset of the subgroup of order 5 in one class modulo 3^j, the rest near it in the 3-tree, some doubled
            o = rnd.randrange(n); B = [(o + s * (n // 5)) % n for s in range(5)]
            j = rnd.randint(1, f[3])
            while len(B) < m:
                x = (o + rnd.randrange(1, 3) * (n // 3 ** j) + rnd.choice([0, 0, n // 2, n // 4])) % n
                B += [x, x] if len(B) + 2 <= m and rnd.random() < 0.7 else [x]
        elif kind == 2:      # one element in every class modulo 3 and modulo 5, spread over the classes modulo 4
            B = [rnd.randrange(n // 15) * 15 + c for c in rnd.sample(range(15), m)]
            B = [x % n for x in B]
        else:                # union of a coset of order 3 and a coset of order 5 (7 points), cut or padded
            o = rnd.randrange(n); B = [(o + s * (n // 3)) % n for s in range(3)] + [(o + rnd.randrange(n) * 0 + s * (n // 5) + rnd.choice([0, n // 4])) % n for s in range(1, 5)]
            while len(B) < m: B.append(rnd.randrange(n))
            B = B[:m]
        S = all_signs(m, fix_first=False)
        bad = bad_table(B, n, S)
        anybad = np.zeros(S.shape[0], dtype=bool)
        for d in divisors(n): anybad |= bad[d]
        share = Fr(int(anybad.sum()), S.shape[0])
        R, Rfib, pairs = R_values([x % n1 for x in B], n1)
        assert share <= R, (B, n, share, R)
        assert R < 1 and share < 1, (B, n, share, R)
        if m in (5, 7): assert Rfib == 0, (B, n)
        st[m][0] += 1; st[m][1] = max(st[m][1], share); st[m][2] = max(st[m][2], R)
    print('n', n, ' '.join('| m=%d: %d multisets, largest share of bad signings %s, largest R %s' % (m, v[0], v[1], v[2]) for m, v in st.items()), flush=True)
