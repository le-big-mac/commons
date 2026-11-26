"""A remark of the referee's (not part of the note; nobody has read it), tested here:
LEMMA. In every class of depth d the q layer counts are congruent to one another modulo p^j, where j is the number of
levels of F deeper than d.  (Induction from the leaves: at a level of F the p children of a class have vectors
v + d_i (1,...,1), so their sum is p v + (sum d_i)(1,...,1); at any other level a sum of vectors with entries congruent
mod p^j has entries congruent mod p^j.)
CONSEQUENCE, for E empty, 0 in F, F not all levels, k' >= 1:  |A| >= q (p^k' + 1), the rule's value in that family.
(Let P be a class of depth a0 - 1 whose children have unequal shapes; P is balanced.  Write each child's vector as
p^k' s_c + m_c (1,...,1) with m_c its least entry.  The s_c are not all zero and add up to a constant vector, so that
constant is >= 1 and |P| >= q (p^k' + sum m_c).  A level g of F minus E deeper than a0 has a class Q with children of equal
shape and unequal totals; a child of Q with more than the least total has every layer occupied.  If Q lies in P, some
m_c >= 1; if not, Q lies in another class of depth a0 - 1, which is balanced and not empty, so has >= q elements.)"""
import sys, random
sys.path.insert(0, '/home/agent3/minsize/check')
from pat import *


def check(p, q, n, w):
    E, F = tree_pattern(p, q, n, w)
    for d in range(0, n + 1):
        j = len([a for a in F if a > d])
        for c, v in class_vectors(p, q, n, w, d).items():
            assert len(set(x % p ** j for x in v)) == 1, (p, q, n, w, E, F, d, c, v)


random.seed(3)
def rnd(p, q, n):
    M = p ** n * q; w = [0] * M
    divs = [d for d in range(2, M + 1) if M % d == 0]
    for _ in range(random.randint(1, 4)):
        r = random.choice(divs); t = random.randrange(M); m = random.randint(1, 2)
        for j in range(r): w[(t + j * (M // r)) % M] += m
    for _ in range(random.randint(0, 2)): w[random.randrange(M)] += 1
    return w
tot = 0
for (p, q, n, reps) in [(2, 3, 2, 5000), (3, 2, 2, 5000), (2, 3, 3, 5000), (3, 2, 3, 3000), (2, 5, 3, 3000), (2, 3, 4, 3000), (3, 2, 4, 1000), (2, 3, 5, 1000), (5, 2, 3, 300), (2, 7, 3, 1000)]:
    for _ in range(reps): check(p, q, n, rnd(p, q, n)); tot += 1
print('the lemma holds on', tot, 'random multisets (sums of cosets and points) in ten groups')
