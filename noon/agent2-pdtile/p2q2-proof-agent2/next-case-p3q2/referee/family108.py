"""Referee: Z_108 (p = 3, q = 2).  Sets A with |A| = 18 and the zeros 3, 9, 54: by brute force on the counts modulo 54
(no lemma used), the zeros 2, 6 and 18 are forced.  So no set of 18 elements has an exact zero set that contains 3, 9, 54
and misses one of 2, 6, 18.  (This settles by hand-size enumeration the patterns that CP-SAT left undecided.)"""
import itertools
d = 54; p, q = 3, 2
surv = {}
for r in range(9):
    cls = [c for c in range(d) if c % 9 == r]                     # 6 residues modulo 54; zeros 3 and 9 <=> each class modulo 9 holds 2 elements
    opts = []
    for N in itertools.product(range(3), repeat=6):
        if sum(N) != 2: continue
        cnt = dict(zip(cls, N))
        if all(cnt[c] - cnt[(c + d // p) % d] - cnt[(c + d // q) % d] + cnt[(c + d // p + d // q) % d] == 0 for c in cls): opts.append(cnt)
    surv[r] = opts
print("survivors per class modulo 9 (of 21 count vectors):", [len(surv[r]) for r in range(9)])
ok18 = all(all(sum(v for c, v in cnt.items() if c % 18 == t) == 1 for t in (r, r + 9)) for r in range(9) for cnt in surv[r])
print("in every survivor both classes modulo 18 above r hold exactly one element:", ok18)
print("=> N_18 = 1 identically, so 18, 6 and 2 are zeros (all cuboid sums of a constant vanish; N_6 = 3, N_2 = 9)")

# ---- second family: |A| = 18 with the zeros 3, 9 and 108 (covers the patterns {2,3,9,108} and {3,9,36,108})
M = 108; okQ = True; ns = []
for r in range(9):
    els = [x for x in range(M) if x % 9 == r]                      # 12 elements; zeros 3, 9 <=> exactly 2 of them in A
    s = 0
    for pair in itertools.combinations(els, 2):
        ind = [0] * M
        for x in pair: ind[x] = 1
        # zero at 108: cuboid sums over the class (they involve c, c+36, c+54, c+90, all congruent to c modulo 18, hence to r modulo 9)
        if all(ind[c] - ind[(c + 36) % M] - ind[(c + 54) % M] + ind[(c + 90) % M] == 0 for c in els):
            s += 1; okQ &= ((pair[1] - pair[0]) % M == 54)
    ns.append(s)
print("zeros 3, 9, 108, |A| = 18: survivors per class modulo 9 (of 66 pairs):", ns, "; every survivor is a coset of Q = {0, 54}:", okQ)
print("=> A + Q = A, so 4, 12, 36, 108 are all zeros; the patterns {2,3,9,108} and {3,9,36,108} (which miss 4) have no set")
