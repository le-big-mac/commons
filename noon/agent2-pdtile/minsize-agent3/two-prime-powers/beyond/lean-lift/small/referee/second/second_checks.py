"""Second look: small checks of sentences added to the note (exact arithmetic; ../reflib.py).
(1) Section 3, the order of contractions.  One pass from level a down to level 1 in each tree: (i) a level is contracted
    in the pass iff it is contractible for B itself; (ii) after the pass no level of any tree is contractible; (iii) the
    group left has order prod p^(r_p), r_p = number of levels of B with a full group.
(2) Z_9, B = {0, 3, 7}: no level has a full group, the digit of index 1 takes all three values on the support
    (so Proposition 4 of the first result does not apply), and every signing with nonzero sum is good.
(3) 'no full group at any level => every signing with nonzero sum is good' (Lemma 2 at every level, down to Z_1):
    all signings of random multisets with that property; how many of them fail the hypothesis of Proposition 4.
usage: second_checks.py SEED COUNT"""
import sys, random
sys.path.insert(0, '/home/agent3/lean/lift-check/small/referee')
from reflib import *
rng = random.Random(int(sys.argv[1])); count = int(sys.argv[2])

def one_pass(el, n):
    deleted = {}
    for p in sorted(factor(n)):
        a = factor(n)[p]
        for t in range(a, 0, -1):
            cur_a = factor(n).get(p, 0)
            # level t of the current tree is still level t: only levels above t have been deleted so far
            if contractible(el, p, cur_a, t):
                el = contract(el, n, p, cur_a, t); n //= p
                deleted.setdefault(p, []).append(t)
    return el, n, deleted

shapes = [81, 243, 729, 135, 405, 675, 2025, 945, 1575, 4725, 625, 3125, 1323, 3465, 10395, 23625]
npass = 0
for _ in range(count):
    n = rng.choice(shapes); f = factor(n); m = rng.randint(2, 14)
    if rng.random() < 0.5:
        el = [rng.randrange(n) for _ in range(m)]
    else:
        el = []
        while len(el) < m:
            q = rng.choice(list(f)); i = rng.randrange(f[q]); c = rng.choice(el) if el and rng.random() < 0.6 else rng.randrange(n)
            if len(el) + q <= m and rng.random() < 0.85: el += [(c + q ** i * (n // q ** f[q]) * j) % n for j in range(q)]
            else: el.append(rng.randrange(n))
    orig = {p: [t for t in range(1, a + 1) if contractible(el, p, a, t)] for p, a in f.items()}
    fl, nf, deleted = one_pass(el, n)
    for p in f:
        assert sorted(deleted.get(p, [])) == orig[p], ('(i) fails', n, el, p, deleted, orig)
    for p, a in factor(nf).items():
        for t in range(1, a + 1):
            assert not contractible(fl, p, a, t), ('(ii) fails', n, el, nf, fl, p, t)
    target = 1
    for p, a in f.items(): target *= p ** (a - len(orig[p]))
    assert nf == target, ('(iii) fails', n, el, nf, target)
    npass += 1
print(f'(1) one pass from the deepest level up, {npass} multisets of 2..14 elements on {shapes}: the levels deleted are exactly the levels '
      f'contractible for B itself; no contractible level is left; the group left is prod p^(r_p): no exception')

el = [0, 3, 7]
g = good_all(9, el); sg = sign_matrix(3)
dig1 = sorted(set((x // 3) % 3 for x in el)); dig0 = sorted(set(x % 3 for x in el))
print(f'(2) Z_9, B = {{0, 3, 7}}: digit of index 0 takes {dig0}, digit of index 1 takes {dig1} on the support; level 1 contractible '
      f'{contractible(el, 3, 2, 1)}, level 2 contractible {contractible(el, 3, 2, 2)}; signings (first +): '
      + ', '.join(f'{"".join("+" if v > 0 else "-" for v in row)} sum {int(row.sum())} good {bool(gv)}' for row, gv in zip(sg, g)))

tot = [0, 0, 0, 0]
tries = 0
while tot[0] < count // 4 and tries < 200 * count:
    tries += 1
    n = rng.choice([27, 81, 45, 135, 225, 675, 105, 315, 945, 75, 375, 189]); f = factor(n); m = rng.randint(2, 8)
    base = rng.randrange(n); el = [base]
    for _ in range(m - 1):
        x = rng.choice(el)
        q = rng.choice(list(f)); i = rng.randrange(f[q])
        el.append((x + q ** i * (n // q ** f[q]) * rng.randrange(q)) % n if rng.random() < 0.7 else rng.randrange(n))
    if any(not contractible(el, p, a, t) for p, a in f.items() for t in range(1, a + 1)):
        continue
    g = good_all(n, el); sg = sign_matrix(len(el)); sums = sg.sum(axis=1)
    assert ((sums != 0) == g).all(), ('no full group, but good is not the same as nonzero sum', n, el)
    prop4 = all(len(set((x % p ** e) // p ** (e - 1) for x in el)) < p for p, a in f.items() for e in range(1, a + 1))
    tot[0] += 1; tot[1] += len(g); tot[2] += int(g.sum()); tot[3] += (not prop4)
print(f'(3) {tot[0]} multisets of 2..8 elements with no full group at any level of any tree, {tot[1]} signings: good exactly when the sum is not 0 '
      f'({tot[2]} good); for {tot[3]} of the multisets the hypothesis of Proposition 4 of the first result fails (some digit takes every value on the support)')
