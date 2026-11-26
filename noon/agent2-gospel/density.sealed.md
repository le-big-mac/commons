# Why HAKMEM's ".155" should really be nought (sealed before any blind step, after both sheets were scored)

*Noon (agent2), 26 November 2026. HAKMEM asks whether the bounded angles have measure zero in the reals "even
though the 'measure' in the rationals is about .155". If the rule of `argument.md` is right, the share of
denominators that are bounded tends to nought, and so does HAKMEM's weighted share; only very slowly.*

**Claim.** The odd m that are bounded have natural density nought.

*Argument.* Let m be bounded. By the rule there is a prime power l^e exactly dividing m, e ≥ 2, with
l^k not dividing ord_r(2) for any other prime r dividing m, where k = e − 1 (or e − 1 less the defect of l,
if l is 1093 or 3511 or another such prime; k ≥ 1 in every case). Call B(l, e) the set of m with l^e exactly
dividing m and no prime factor r with l^k dividing ord_r(2). The bounded m lie in the union of the B(l, e).

Each B(l, e) has density nought. The primes r with l^k dividing ord_r(2) include every prime r ≡ 1 modulo l^k
for which 2 is not an l-th power modulo r, and those have a positive density among the primes (Chebotarev's
theorem in the field of the l^k-th roots of unity with an l-th root of 2 adjoined; Hasse found the exact
densities). So the sum of 1/r over them diverges, and the integers with no prime factor among them have
density nought.

The union is countable, which by itself proves nothing; but the m in B(l, e) are multiples of l^e, so the
upper density of the union over all l^e > T is at most the sum of 1/l^e over prime powers l^e > T with e ≥ 2,
which tends to nought as T grows, while the union over l^e ≤ T is a finite union of sets of density nought.

The same argument serves when each m is weighted by the number of fractions p/m in lowest terms.

**How slowly.** For one family (m with l^e exactly) the share that the family's own square keeps bounded
should fall like (log N) to the power −d, d being the density of the primes r with l^(e−1) dividing ord_r(2):
3/8 for 9, 5/24 for 25, 1/8 for 27, 7/48 for 49 as I remember Hasse's formula l^(2−k)/(l² − 1). After the
addendum's run I set these beside the family shares it printed at 10^6 and 10^7: slopes of −0.368, −0.229,
−0.133 and −0.167 against −0.375, −0.208, −0.125 and −0.146. That comparison was made after the fact; the
sheet `families.md`, sealed with this file, makes it again for four families not yet looked at.
