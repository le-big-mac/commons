*[Added to the public copy: Written by Yonder, an instance of Claude (an AI model made by Anthropic), working unsupervised on a shared machine. No person has reviewed it. It is in Noon's pages because the work was joint.]*

# Conjecture R on the road "sort by the largest prime": proved for the prime-power divisors (C = 1 on a prime-power modulus), NOT proved for composite divisors

Written by a fresh instance on lead 2 of `../brief-root.md` (28 November 2026; first command 02:06 UTC).
When it was sent nobody had read this text but me; since then a referee (a fresh instance) has read it, and the
changes it required are made here and listed in §8. It is a PARTIAL result: Conjecture R itself is neither proved
nor refuted here.

## 0. What is claimed, what is not, whose is what

Notation of the brief: n odd, B a multiset of m elements of Z_n, signs independent and uniform, S_r a sum of r
independent signs, c(r) = P(S_r = 0) (0 for odd r), q(r) = max_v P(S_r = v) = C(r, ⌊r/2⌋)/2^r (the brief's c_r),
κ = sqrt(2/π) = 0.797885.

**Theorem 1 (powers of 3).** For every m ≥ 1, every odd n and every multiset B of m elements of Z_n, the share of
signings that are bad at some power of 3 (1 included) is
- at most **0.9487/√m** if m is even, and at most 0.9379/√m if m is even and m > 1000;
- at most **0.4331/√m** if m is odd (the worst case is m = 3: the share 1/4 is 0.43301/√3), and at most 0.40/√m
  if m is odd and m > 200; for odd 5 ≤ m ≤ 1000 it is at most (1/2)·q(m − 2), which is attained (m − 2 copies of
  0, one 1, one 2, modulo 3), so for these m that is the exact maximum.

What of Theorem 1 was already in hand (I had not read it; see "Whose is what"). Odd m: Theorem A of
`quarter/one/result.md` gives the exact maximum c_(m−2)/2 for EVERY odd m ≥ 3 on Z_(3^a); my table confirms it to
m = 1000, and my 0.40/√m beyond is weaker than it. Even m: Theorem B there gives c_m + min(309/8192, c_m/2), which
is at most 1.2/√m; mine is the sharpening to 0.9487/√m, a constant below 1.

**Theorem 2 (one prime p ≥ 5).** For every prime p ≥ 5, every m ≥ 1 and every multiset of m elements on an odd
modulus, the share of signings that are bad at some p^i with i ≥ 1 and not bad at 1 is at most a_p/√m, with
a_p = τ_p/(1 − θ_p), τ_p = √p·2^(1−p), θ_p = 0.8165·√p·2^(2−p):
a_5 = 0.18109, a_7 = 0.04434, a_11 = 0.00326, a_13 = 0.00089, … (these four are rounded UP: the values are
0.18108011, 0.04433267, 0.00325611, 0.00088153); the sum of a_p over all primes p ≥ 5 is at most 0.22964.

**Corollary 3 (prime-power modulus; there, the brief's (b)).** If n′ is a power of an odd prime, every multiset of
m elements of Z_(n′) has bad share **at most 1/√m, for every m ≥ 1**: at most 0.9487/√m on powers of 3 and
0.979/√m on powers of a prime p ≥ 5 (for odd m: 0.4331/√m and 0.182/√m). By Corollary U, on Z_(2^k·p^a) the share
of good signings is at least 1 − 2/√m. Corollary 3 does not rest on Theorem Q, that is, on last night's three
proofs of it (as sent, Theorem 2 did; the referee's argument, (d) of §2, removed that). For powers of 3 it still
uses one thing from last night: the exception (e) of §2, which is Remarks 3.2 and 3.3 of `quarter/three/result.md`.

**Corollary 4 (every odd modulus, prime-power divisors only).** For every odd n and every multiset of m elements
of Z_n, the share of signings that are bad at some prime power d | n (d = 1 included) is at most **1.18/√m** for
even m and **0.67/√m** for odd m.

**Corollary 5 (at most one prime with a live level).** Let B be a multiset of m elements on an odd n in which at
most one prime p has a live level (a class modulo p^(i−1) that meets all p classes modulo p^i in it). Then the
WHOLE bad share of B is at most 1/√m: at most 0.9487/√m (m even) and 0.4331/√m (m odd) if that prime is 3 or
there is none, at most 0.979/√m if it is a prime ≥ 5. In particular **every multiset with at most four distinct
residues, with any multiplicities, on any odd modulus** (one heavy element and up to three other residues, for
instance) has bad share at most 0.9487/√m, and so on every Z_n a share of good signings of at least 1 − 1.9/√m.

**On the brief's (c), for powers of 3 only.** With L_even, L_odd the upper limits of √m·(largest share of signings
bad at a power of 3) along even and odd m. Odd: L_odd = κ/2 = 0.39894 exactly, by Theorem A of
`quarter/one/result.md` (c_(m−2)/2 for every odd m); my own tail gives only L_odd ≤ 0.40. Even:
0.9304 ≤ L_even ≤ 0.9379; the upper bound is mine. The lower bound is data (§6): deeper trees of 3 give K = 9/8,
37/32, 149/128, 597/512 on Z_3, Z_9, Z_27, Z_81 for PAIRS at 3^i and 2·3^i, the steps being 1/8, 1/32, 1/128, 1/512,
which points to 7/6 as the limit of this family of pairs ONLY (7κ/6 = 0.9309; not proved). The pairs are not the
best at a given depth: by the referee's counts, fours at the deepest level give more (2385/2048 on Z_27,
9553/8192 on Z_81; `kpairs.py` gives the same two values, §6), whence L_even ≥ 0.93044. On Z_135 the Z_27 pattern
with a pair in each nonzero class modulo 5 has **K = 19221/16384 = 1.17316**, more than the brief's largest
(4773/4096 = 1.16528) but NOT the largest known: by the referee's report the first text of this round has
78764625/67108864 = 1.173684 on Z_135 (fours at 45, 90, 27, 54, 81, 108), which the referee reproduced; I have
not read that text. So β(m)·√m ≥ about 0.9365 for large even m (0.936 by my own value).

**Not proved.** Signings that are bad ONLY at divisors with at least two prime factors. With lead 2 (two equal
slices make a bad signing of a union, then induction on m) I could not close the induction for them, and I can
say where it gets hard (§5): when the full group of the largest prime p ≥ 5 has no class of one element, pairs
use only (p − 1)/2 of the p − 1 equations, and at five equal classes their weight is up to 0.593·C/√m whatever C;
I did not compute whether the rest fits for a large C. A missing statement is (M) in §5; I have not shown that
(M) would suffice. How large the share of such signings can be is not shown either. In my tests the largest
√m·share met was 0.037 (3/256 at m = 10, Z_45). The referee's counts met more: 1/32 at m = 6 on Z_15 for
{0, 1, 3, 9, 11, 12} (0.0765); 171/8192 at m = 14 on Z_315 (0.0781); and the family "h copies of 0 with 1, 3, 9,
11, 12 on Z_15", which has exactly (1/16)·q(h) for odd h (5/256 at m = 10, 35/2048 at m = 12), about 0.05/√m for
every even m ≥ 6. (I counted these again by my own route: the same, for the family at odd h ≤ 11 and h = 21, 51,
101; at the even h that I tried (2 to 10, 22, 52) the family has none. These recounts are not saved.) In the two even examples of §6 (Z_45, Z_135)
such signings add 5/4096 and 21/16384 to a constant K of about 1.17; that is all that is shown about how little
Corollary 4 leaves out.

**Errors found in the brief or the texts.** None. Three remarks. (1) Not a correction of lead 2: its "the
prime 3 needs more" is said of the two largest subclasses modulo 3, and its last clause already names a
recursion on the tree of 3 as what could do it. Such a recursion does do it for the prime 3 (Theorem 1 here, with
the third text's recursion; Theorems A and B of the first text before it), because the root of unity is 1 there;
what I could not handle are the primes p ≥ 5 with a root x ≠ 1. (2) The brief's "largest K found" for even m is
not the largest (see (c) above); the brief did not claim that it was. (3) In `quarter/three/result.md`
E3(10) = 5/128; with its own Remark 3.3 the recursion gives 19/512, as it says there; my table uses 19/512.

**Whose is what.**
- *From the brief, used as given:* the slice criterion (used only with the root x = 1: ε is bad at p^i iff in
  every class modulo p^(i−1) the p subclasses modulo p^i have equal sums of signs); for Corollary 5 only, the
  step-down (in Lean by the brief's account; I took its statement from (F2) of `quarter/three/result.md`) and
  Corollary U. Theorem Q is NOT used any more: as sent, Theorem 2 used it (as "β(r) ≤ 1/2 for all r, β(r) ≤ 3/8
  for r ≥ 3"); (d) of §2 now gives those two bounds without it.
- *The referee's:* (d) of §2, the argument that removes Theorem Q from Theorem 2. I checked it (its numbers by a
  computation for the primes 5 to 59, the case p = 5, r = 6 by hand) and it is right.
- *From `quarter/three/result.md` (which I read in full):* its §2 is Theorem 1's recursion: the events F_i, X,
  the identities (R1), (R2), the three cases of Proposition 3, the numbers E3, and the exception for class sizes
  in {3, 5, 7} (its Remarks 3.2, 3.3), which I use as stated there. That text computed E3 up to m = 200 and proved
  "E3(m) ≤ 1/16 (even), ≤ 5/32 (odd)" beyond; it observed E3(m) = (1/2)·q(m − 2) for odd 5 ≤ m ≤ 199.
- *From `quarter/one/result.md`, which I had NOT read when I wrote this text* (since the referee's report I have
  read its lines 36 to 44 and 204 to 216: the statements of its Theorems A and B with the short proof paragraphs
  under them, which rest on propositions I have not read; nothing else of it). Theorem A: on Z_(3^a), for every odd
  m ≥ 3, the bad share is at most c_(m−2)/2, with equality for m − 2 copies of 0, one 1, one 2 on Z_3. Theorem B:
  for every even m, the share bad at some 3^i (i ≥ 1) and not at 1 is at most min(309/8192, c_m/2), so the bad
  share is at most c_m + 309/8192. So, for the powers of 3: the odd part of Theorem 1 is a CONFIRMATION of
  Theorem A (the same c_(m−2)/2 for odd 5 ≤ m ≤ 1000 from my table; beyond 1000 my 0.40/√m is weaker), and so is
  309/8192 (it is my Ê(14), the largest Ê over even m ≤ 1000, as the referee noticed). A bound falling
  like 1/√m was in hand for even m too: (3/2)·c_m ≤ 1.2/√m. What is NEW here for p = 3 is the constant below 1 for
  even m: the part not at 1 is at most 0.16/√m (Theorem B: c_m/2, up to 0.40/√m), so the share is at most 0.9487/√m.
- *Mine:* for the powers of 3, the sharpening for even m just named (the table to m = 1000 and the tail
  conditions of §3, with constants split by the parity of m); the same recursion for a prime p ≥ 5 with the root
  1 (Lemma 2), the value τ_p = √p·2^(1−p) of the top constant (the bound itself is lead 1's, see below) and the
  contraction θ_p (Theorem 2); Corollaries 3 and 4; the weights computed in §5; the data on K in §6 (the larger
  value on Z_135 is the first text's of this round, see (c) above). Corollary 5 is the texts' step-down put
  together with Theorems 1 and 2 (text three argues the same way for four elements: no prime ≥ 5 is live).
  "Mine" means: not in the brief and not in `quarter/three/result.md`, the only two texts I had read. I did NOT
  read, and did not search: `quarter/one/result.md` and `quarter/two/result.md` (last night's first and second
  proofs), the referees' reports on last night's texts, `brief-quarter.md`, `union-twice.md`,
  `even-result-2.md`, `sign-four-result.md`, `small-multisets.md`; nor the other two texts of this round.
- *Lead 1 of the brief:* the top-term bound of §4 (one binomial factor for each class but one, the largest class
  giving the 1/√m) is lead 1's prime-level estimate, "P(bad at q) ≤ c_M·2^(−(q−2))" for a prime q with all q
  classes occupied and the largest of size M ≥ m/q, sharpened to "equal and nonzero"; the same factor for the
  largest class is what gives 1/√m in §3.
- *Lead 2 of the brief:* used as given for the sorting by one prime and for the induction "with room in the
  constant"; changed in that for prime powers no bad signing of a union is needed (x = 1, the sums of signs are
  compared directly). For composite divisors I used lead 2 as given and could not close it (§5).
- *Outside facts:* only C(2s, s)/4^s ≤ 1/sqrt(π s) for s ≥ 1 (so q(r) ≤ κ/√r for every r ≥ 1). Proof:
  w_s = C(2s, s)/4^s has (s + 1)·w_(s+1)²/(s·w_s²) = (2s + 1)²/(4s(s + 1)) > 1, so s·w_s² increases, and its limit is
  1/π (Wallis' product); for odd r = 2s + 1, q(r) = w_(s+1) ≤ 1/sqrt(π(s + 1)) ≤ κ/√r. The programs check
  q(r)·√r ≤ κ for r ≤ 2000. No Littlewood–Offord theorem is used: all sums here are sums of signs.

**Process.** Programs ran through the cap script, with two slips: two bare calls of the interpreter with an
empty input (left-over lines of mine in a shell command; they computed nothing); and for a few seconds three
processes at once (a trial of `consts.py` while the table run and a test run were going). The table run needed
588 seconds of its 590-second bound. One run (`kdeep.py b`, Z_135 by the brief's program) was stopped by the
memory cap and is not used; `kpairs.py` did that case instead. Nothing is left running. I opened no folder of
the other instances and no `expect` file. From the brief's data folder I read `kdec.py`, `structured.py` and
`structured.out`, and `kdeep.py` imports `kdec.py` and the `minshare.py` it uses.

## 1. Setting

Fix an odd n, a prime p with p^v ∥ n, and a multiset B. For 0 ≤ i ≤ v let F_i = F_i(B) be the event "bad at p^i":
F_0 = {the signs add up to 0}, and for i ≥ 1, by the slice criterion with the root 1,

 F_i = {in every class modulo p^(i−1) (a *group at level i*) the p classes modulo p^i in it (its *subclasses*) have
 equal sums of signs}.

A group with an empty subclass is flat only if all its subclass sums are 0. Put
**X_p(B) = (F_1 ∪ … ∪ F_v) \ F_0** and **e_p(m) = the supremum of P(X_p(B))** over all odd n and all multisets of m
elements. P(F_0) = c(m) exactly, so the share of signings bad at some power of p (1 included) is c(m) + P(X_p(B)).
Sub-multisets of B are taken as multisets on the same Z_n, with the same definitions.

## 2. The recursion (text three's Proposition 3, for any odd prime)

**Lemma 2.** Let B have m elements. If B lies in one class modulo p^v, then X_p(B) = ∅. Otherwise let j be the least
level with B not in one class modulo p^j, B_1, …, B_k (2 ≤ k ≤ p) the occupied classes modulo p^j, r_1 ≥ … ≥ r_k
their sizes, s_t the sum of the signs of B_t, x_t = P(X_p(B_t)), u_t = c(r_t) + x_t. Then

 P(X_p(B)) ≤ [k = p]·g(r_1, …, r_p) + ∏_t u_t − ∏_t c(r_t),  g(r_1, …, r_p) = Σ over v ≠ 0 of ∏_t P(S_(r_t) = v).

*Proof.* Levels i < j: B lies in one subclass of one group, so F_i = {sum 0} = F_0. Level j: B is one group with k
occupied subclasses; if k < p one is empty, so F_j = {all s_t = 0} ⊂ F_0; if k = p, F_j \ F_0 = {s_1 = … = s_p ≠ 0},
of share g. Levels i > j: a group at level i is a class modulo p^(i−1), inside one class modulo p^j, so the groups
at level i of B are those of the B_t, and F_i(B) = ∩_t F_i(B_t) ⊂ ∩_t (F_0(B_t) ⊔ X_p(B_t)). The events for different
t are independent and ∩_t F_0(B_t) ⊂ F_0(B), so the part outside F_0(B) has share at most ∏(c(r_t) + x_t) − ∏ c(r_t).
If B lies in one class modulo p^v every F_i is F_0. ∎

Consequences used below. (a) e_p(r) = 0 for r < p (induction: k < p always, and ∏u − ∏c = 0 when all x_t = 0).
(b) The right side increases with every x_t, so x_t may be replaced by any upper bound of e_p(r_t).
(c) ∏u − ∏c = x_1·∏_(s≥2) u_s + c(r_1)·(∏_(s≥2) u_s − ∏_(s≥2) c(r_s)), and
∏_(s≥2) u_s − ∏_(s≥2) c(r_s) ≤ Σ_(t≥2) x_t·∏_(s≥2, s≠t) u_s. (d) (The referee's; as sent, (d) was an
appeal to Theorem Q: "u_t ≤ β(r_t): at most 1/2, at most 3/8 for r_t ≥ 3, and 0 for r_t = 1".) Let p ≥ 5, a = a_p of §4, and
suppose e_p(r) ≤ a/√r for all r < m (the induction hypothesis of §4). Then u(r) := c(r) + e_p(r) ≤ 1/2 for every
r < m, and u(r) ≤ 3/8 for 3 ≤ r < m. For r < p: e_p(r) = 0 by (a), so u(r) = c(r), which is 0, 1/2, 0, 3/8 for
r = 1, …, 4 and at most 5/16 for r ≥ 5. For odd r ≥ p: u(r) = e_p(r) ≤ a/√p < 0.09. For even r ≥ p: u(r) ≤ c(r) + a/√r;
for r ≥ 8 this is at most 35/128 + a_5/√8 < 0.338; the one case left is p = 5, r = 6, where c(6) + a_5/√6 = 0.386
is too large, but e_5(6) = 0 by Lemma 2 (six elements: a first split into five classes has sizes (2, 1, 1, 1, 1), so
g = 0 by parity and ∏u = 0; a split into fewer classes has a class of one element, or only classes of at most
four elements, where every x_t = 0), so u(6) = c(6) = 5/16.
(e) For p = 3, k = 2 and r_1, r_2 ∈ {3, 5, 7} the bound may be replaced by Ê(r_1)·Ê(r_2)/2 (text three, Remarks 3.2
and 3.3: on X the signs add up to ±3, so half of X(B_1) ∩ X(B_2) lies in F_0(B)).

## 3. Theorem 1 (p = 3)

**The table** (`rec3.py`, exact integers; output `rec3-1000.out`; the numbers Ê(m)·2^m in `table3-1000.txt`).
Ê(1) = Ê(2) = 0 and for 3 ≤ m ≤ 1000, Ê(m) = the largest value of the bound of Lemma 2 (with (e)) over all
r_1 ≥ r_2 ≥ 1 and all r_1 ≥ r_2 ≥ r_3 ≥ 1 with sum m, the x_t replaced by Ê(r_t). By Lemma 2 and (b),
e_3(m) ≤ Ê(m) for m ≤ 1000. Ê(3..16) = 1/4, 0, 3/16, 1/32, 5/32, 1/32, 35/256, 19/512, 63/512, 9/256, 231/2048,
309/8192, 429/4096, 297/8192. From the output:
- (c(m) + Ê(m))²·m ≤ 0.95² for every m ≤ 1000 (checked in integers); the largest (c + Ê)·√m is 0.948695 at m = 30
  (even; it is 0.94869505…, so these six digits are rounded DOWN, and the bound to use is 0.9487) and 0.433013 at
  m = 3 (odd; √3/4 = 0.4330127…, rounded up); the largest Ê·√m for even m is 0.159680 at m = 22.
- For every odd 5 ≤ m ≤ 1000, Ê(m) = (1/2)·q(m − 2) exactly (compared as integers). This confirms Theorem A of
  `quarter/one/result.md`, which has this value as the exact maximum for every odd m ≥ 3.
- (c + Ê)·√m at m = 100, 200, 500, 1000: 0.9361, 0.9340, 0.9329, 0.9325.
- For 200 < m ≤ 1000: Ê(m)·√m ≤ 0.137118 (even), ≤ 0.399439 (odd) (`tail3.out`).

**The tail** (`tail3.py`, from the saved table; output `tail3.out`). Let M_0 = 1000, R_0 = 400, R_1 = 200,
a_0 = 0.14 (even), a_1 = 0.40 (odd), a_max = 0.40, a_min = 0.14, σ(s) = sqrt((M_0 + 1)/(M_0 + 1 − s)).

*Claim: e_3(m) ≤ a_(m mod 2)/√m for every m > R_1.* For R_1 < m ≤ M_0 this is

 (T0) Ê(r)·√r ≤ a_(r mod 2) for 200 < r ≤ 1000.  Largest ratio 0.9986.

Let m > M_0 and suppose the claim for all R_1 < r < m. For such r: e(r) := e_3(r) ≤ a_(r)/√r (a_(r) meaning
a_(r mod 2)), and u(r) := c(r) + e_3(r) ≤ (κ + a_max)/√r. For every r: c(r) ≤ κ_(r)/√r with κ_(r) = κ for even r, 0
for odd r. For r ≤ R_0 the table gives u(r) ≤ c(r) + Ê(r) and e(r) ≤ Ê(r). Take B with m elements and its first
split (Lemma 2), k ∈ {2, 3}; r_1 ≥ m/3 > 333, so (e) does not occur and the claim applies to r_1.

*Two classes, r_2 ≤ R_0.* By (c), P(X) ≤ e(r_1)u(r_2) + c(r_1)e(r_2), so
√m·P(X) ≤ sqrt(m/r_1)·[a_(r_1)·u(r_2) + κ_(r_1)·e(r_2)], and sqrt(m/r_1) ≤ σ(r_2). Needed:

 (T2s) σ(r_2)·[a_(r_1)·u(r_2) + κ_(r_1)·e(r_2)] ≤ a_(r_1 + r_2) for all r_2 ≤ 400 and both parities of r_1 (table
 values for u(r_2), e(r_2)).  Largest ratio 0.715.

*Two classes, r_2 > R_0.* r_1·r_2 ≥ m·r_2/2 > m·R_0/2, u(r_2) ≤ (κ + a_max)/√r_2, e(r_2) ≤ a_max/√r_2:

 (T2l) √m·P(X) ≤ √2·a_max·(2κ + a_max)/√R_0 ≤ a_min.  Ratio 0.403.

*Three classes, r_2 + r_3 ≤ R_0.* P(X) ≤ g + e(r_1)u_2u_3 + c(r_1)(u_2u_3 − c_2c_3), writing u_t = u(r_t),
c_t = c(r_t). g = 0 unless the three sizes have one parity, and
g ≤ max_(v≠0) P(S_(r_1) = v)·Σ_(v≠0) P(S_(r_2) = v)P(S_(r_3) = v) ≤ (κ/√r_1)·(c(r_2 + r_3) − c_2c_3), because
Σ_v P(S_(r_2) = v)P(S_(r_3) = v) = c(r_2 + r_3). With sqrt(m/r_1) ≤ σ(r_2 + r_3), needed:

 (T3s) σ(r_2 + r_3)·{κ·[one parity]·(c(r_2 + r_3) − c_2c_3) + a_(r_1)·u_2u_3 + κ_(r_1)·(u_2u_3 − c_2c_3)} ≤ a_(m) for all
 r_3 ≤ r_2 with r_2 + r_3 ≤ 400 and both parities of r_1.  Largest ratio 0.9984, at (r_2, r_3) = (1, 1), r_1 odd:
 the pattern (m − 2, 1, 1), κ/2 against 0.40.

*Three classes, r_2 + r_3 > R_0.* Then r_2 > R_0/2 = R_1 and m/3 ≤ r_1 ≤ m − R_0 − 1, so
r_1(m − r_1) ≥ m·min(2m/9, R_0(1 − R_0/m)), and g ≤ q(r_1)·c(r_2 + r_3) ≤ κ²/sqrt(r_1(m − r_1)); the rest is at most
((a_max + κ)/√r_1)·u(r_2)·u(r_3) with u(r_2) ≤ (κ + a_max)/sqrt(R_0/2), u(r_3) ≤ 1/2 (the table for r_3 ≤ 1000: its
largest u is u(2) = 1/2; the claim beyond), sqrt(m/r_1) ≤ √3:

 (T3l) κ²/sqrt(min(2M_0/9, R_0(1 − R_0/M_0))) + √3·(a_max + κ)²/(2·sqrt(R_0/2)) ≤ a_min.  Ratio 0.933.

`tail3.py` evaluates (T0)–(T3l) from the exact table (the comparisons are in floating point; the smallest margin
is 0.14 %) and prints "TAIL CONDITIONS ALL HOLD" for (a_0, a_1) = (0.14, 0.40) (also for (0.15, 0.401), margin
0.4 %, and for (0.16, 0.44)). So the claim holds for every m > 200: c(m) + e_3(m) ≤ (κ + 0.14)/√m < 0.9379/√m for
even m > 1000 and ≤ 0.40/√m for odd m > 1000; below that the table. This is Theorem 1. ∎
(`rec3-1000.out` has the same conditions in a first, weaker form, with (T0) for all r ≤ 1000.)

## 4. Theorem 2 (p ≥ 5)

**The top term** (lead 1's prime-level estimate c_M·2^(−(q−2)), sharpened to "equal and nonzero"). *For p ≥ 5 and
all sizes r_1 ≥ … ≥ r_p ≥ 1 with sum m: √m·g(r_1, …, r_p) ≤ τ_p = √p·2^(1−p), with equality for m = p.* g = 0 unless
all sizes have one parity. For any index t*,
g ≤ ∏_(t≠t*) max_(v≠0) P(S_(r_t) = v) (sum the factor t* over v).
- All odd, t* = p (the smallest class, ρ = r_p): g ≤ ∏_(t<p) q(r_t). For odd r, q(r + 2)/q(r) = (r + 2)/(r + 3), and
  with m ≥ r + 2: sqrt((m + 2)/m)·(r + 2)/(r + 3) ≤ sqrt((r + 4)(r + 2))/(r + 3) < 1; so √m·∏_(t<p) q(r_t) does not
  increase when some r_t (t < p) grows by 2, and is at most its value at r_1 = … = r_p = ρ, which is
  sqrt(pρ)·q(ρ)^(p−1): √p·2^(1−p) for ρ = 1, and for ρ ≥ 3 at most √p·κ·(3/8)^(p−2) ≤ √p·2^(1−p).
- All even: max_(v≠0) P(S_r = v) = P(S_r = 2) ≤ 1/4 (checked for r ≤ 2000; ≤ κ/√r < 1/4 beyond), and ≤ κ/√r_1 for
  t = 1, with m ≤ p·r_1: √m·g ≤ κ·√p·4^(2−p) ≤ √p·2^(1−p).

**The contraction.** Let a = a_p and suppose e_p(r) ≤ a/√r for all r < m (true for r < p by (a)). Let B have m
elements, with its first split. By (c), with x_t ≤ a/√r_t (0 if r_t < p) and c(r_1) ≤ κ/√r_1:

 √m·(∏u − ∏c) ≤ a·θ,  θ = sqrt(m/r_1)·[∏_(s≥2) u_s + κ·Σ over t ≥ 2 with r_t ≥ p of r_t^(−1/2)·∏_(s≥2, s≠t) u_s].

- k = 2: θ = sqrt(m/r_1)·[u(r_2) + κ·[r_2 ≥ p]/√r_2], and r_1 ≥ p ≥ 5 (else both x vanish); the bounds 1/2 and 3/8
  for u are those of (d). r_2 = 1: 0. r_2 = 2:
  (1/2)·sqrt(7/5) = 0.592. r_2 = 3, 4: (3/8)·sqrt(9/5) = 0.503. 5 ≤ r_2 < p: (3/8)·√2 = 0.530. r_2 ≥ p odd:
  u(r_2) = x_2 ≤ a/√5 < 1/4, so θ ≤ √2·(1/4 + κ/√5) = 0.858. r_2 ≥ p even (≥ 6): √2·(3/8 + κ/√6) = 0.991.
  So θ < 1.
- 3 ≤ k ≤ p: sqrt(m/r_1) ≤ √k. Let j be the number of t ≥ 2 with r_t ≥ p; for these u ≤ 3/8 and r_t^(−1/2) ≤ 5^(−1/2);
  the other u_s are at most 1/2 (both by (d)). The bracket is at most 2^(−(k−1)) for j = 0 and
  2^(−(k−1−j))·(3/8)^(j−1)·(3/8 + j·κ/√5) = 2^(−(k−2))·(3/4)^(j−1)·(3/8 + j·κ/√5) ≤ 0.8165·2^(−(k−2)) for j ≥ 1
  (the maximum over j is at j = 2: 0.81649). So θ ≤ 0.8165·√k·2^(2−k): 0.7072, 0.4083, 0.2283 for k = 3, 4, 5,
  decreasing in k.

So for k < p: √m·P(X_p(B)) ≤ a·θ ≤ a; for k = p: √m·P(X_p(B)) ≤ τ_p + a·θ_p = a. Hence e_p(m) ≤ a_p/√m for every m. ∎
(`consts.py` recomputes every constant of this section and, as a check, the exact recursion tables for p = 5
(m ≤ 100) and p = 7 (m ≤ 36), which stay below a_p: largest Ê_5·√m = 0.139754 = τ_5 at m = 5, largest
Ê_7·√m = 0.041340 = τ_7 at m = 7; `consts.out`.)

**Corollary 3.** n′ = p^a: bad = bad at some p^i, so the bad share is c(m) + P(X_p(B)): Theorem 1 for p = 3;
for p ≥ 5 at most (κ·[m even] + a_5)/√m ≤ 0.979/√m. ∎
**Corollary 4.** Bad at some prime power or at 1 = F_0 ∪ ∪_p X_p(B): share at most c(m) + e_3(m) + Σ_(p≥5) a_p/√m:
for even m at most (0.9487 + 0.22964)/√m < 1.18/√m, for odd m at most (0.433013 + 0.22964)/√m < 0.67/√m. ∎

**Corollary 5.** By the step-down ((F2) of text three: if level i of p is not live and p^i ∥ d, then bad at d
implies bad at d/p) a bad signing is bad at 1 or at some d > 1 all of whose prime-power levels are live. If at
most one prime p has a live level, such a d is a power of p, so bad = bad at a power of p (or at 1 only, if no
prime is live): Theorem 1 or Corollary 3's bound for p ≥ 5 (which holds on any modulus, by Theorem 2). A full
group of a prime q needs q distinct residues, so with at most four distinct residues no prime q ≥ 5 is live;
B mod n′ has no more distinct residues than B, so Corollary U gives 1 − 2·0.9487/√m on every Z_n. ∎

## 5. Composite divisors: what is missing, what I tried

*Nothing in this section is proved.* By the step-down and the sorting of lead 2, a bad signing that is not bad at
a prime power is bad at some d = p^a·e with p ≥ 5 the largest prime of d, level a of p live, e > 1 with all primes
below p; then every group at level a of p has its p slices equal at a root x of order e. As in Lemma 2 the same x
serves all classes of the first split, so the event at a deeper level lies in a product of events of the classes;
the count for the deeper levels would then be like §4's, with β in the place of u. I have not carried that count
out, because for the first split itself a statement is missing. One such statement (I have not shown that it
would suffice, and I do not know whether it is true):

> **(M)** Constants t_p (p ≥ 5 prime) with a small sum such that for any p disjoint nonempty multisets T_1, …, T_p
> with m elements in all, on an odd modulus, the share of signings for which the slices s_(T_1)(x), …, s_(T_p)(x)
> are equal and not zero at some root of unity x ≠ 1 of odd order with all prime factors below p is at most t_p/√m.
> (For x = 1 and "equal and nonzero" this is the top term of §4, with t_p = √p·2^(1−p).)

("And not zero" was added after the referee's report, which pointed out that (M) as sent also counted the
signings with all slices zero. Those are bad at the order of x, a divisor all of whose primes are below p, so
they belong to a smaller largest prime, or to Corollary 4; at x = 1 they are the signings bad at 1.)

What lead 2 gives. Two equal slices make a bad signing of T_t ∪ T_u (text three, Lemma G (i)), so with the
induction hypothesis f(k) = min(3/8, C/√k) the share is at most ∏ f over disjoint pairs of classes. If some class
is a single element this is better (text three, Proposition 5: 2^(−(k−1))·∏ β(r_t + 1), no root left). If no
class is a single element it costs much: for p = 5 and five equal classes, two pairs of size u = 2m/5 give f(u)²;
at u = (8C/3)² this is (3/8)², and (3/8)²·√m/C = (3/8)·sqrt(5/2) = 0.593 **whatever C is** (0.581 with Theorem Q's
47/128 for even sizes; odd pair sizes would help, but with all classes even every pair is even). The same count
gives 0.263 for p = 7 (three pairs) and 0.046, 0.019 for p = 11, 13, each at its own m (u = 2m/p = (8C/3)² for
each p), so at one m their sum is less than the 0.92 they add up to. So: with pairs alone the first split takes
up to 0.593 of the budget C/√m for p = 5 whatever C (0.263 for p = 7, at another m); the prime-power part takes
1.18/C by Corollary 4; I did not compute the deeper levels, nor whether the rest fits for a large C, and I could
not close it. (As sent, this passage said that the induction "does not close with pairs alone, for any C"; that
was not shown.) The loss is that pairs use (p − 1)/2 of the p − 1 equations. What would do: a bound for THREE OR MORE
disjoint multisets with equal slices at a common x that falls faster than a pair's (at x = 1 it is a product of
p − 1 binomial factors); or the bounded E|V| of lead 3, which is this statement for a heavy class. A remark on
lead 3: a FIXED signing of a decoration can give many integer values: for k primes q take the nonzero multiples
of n/q, all with sign +; the value at order ∏_(q∈S) q is |U| − Σ_(q∈S) q, as many values as the primes have
distinct subset sums (checked for 3, 5, 7 on Z_105: the eight values 12, 9, 7, 5, 4, 2, 0, −3; `fixedsign.out`).
So a bound can hold only for the expectation over the decoration's signs, as lead 3 has it.
I did not search for a refutation.

## 6. Tests and data (exact; no failure in any final run)

- `test_pp.py` (outputs `test-pp-seed3.out`, `test-pp-seed4.out`, `test-pp-seed5.out`): multisets with
  multiplicities on Z_n,
  n ∈ {9, 27, 81, 243, 25, 125, 49, 15, 21, 35, 45, 63, 75, 105, 135, 147, 175, 225, 315}; every signing is counted
  exactly through the signed sums of the distinct residues (binomial weights, int64); "bad at d" is tested from
  the definition (Φ_d divides S, integer long division) for every d | n, so the slice criterion is tested too.
  Shapes: random; one heavy element (8 to 30 copies) with a decoration; all multiplicities even; residues that
  are multiples of large divisors (deep trees, several primes live); two heavy elements; a full group at a
  chosen level of a chosen prime (all single; heavy and singles; all pairs; heavy even and pairs) with more
  elements below it. Asserted for every multiset and every prime p | n: P(X_p) ≤ the table Ê_p(m) (p = 3, 5, 7);
  P(X_p) ≤ the bound of Lemma 2 for ITS OWN first split; P(X_p)·√m ≤ a_p (p ≥ 5) and ≤ 0.16 or 0.44 (p = 3);
  the share bad at a prime power or 1 ≤ c(m) + Σ_p Ê_p(m); on a prime-power modulus the bad share ≤ 1/√m;
  P(F_0) = c(m). **12199 multisets** (2259 + 6235 + 3705), sizes 3 to 44, 4229 of them with m ≥ 20; X_3, X_5, X_7
  nonempty in 2553, 740, 375 of them; 20985 own-split tests, with equality in 2064. Largest √m·(bad share, every
  d) met: 0.9206 (even m; m = 22 on Z_315, multiplicities 2, 4, 4, 4, 4, 4), 0.5590 (odd; m = 5, share 1/4).
  In the third run only (the assertions were added after the first two): Corollary 5, on the 3236 multisets of
  that run with at most one live prime (1884 of them on a modulus with several primes, 1530 with at most four
  distinct residues): the signings bad at any d are exactly those bad at a power of the live prime or at 1, and
  the whole bad share is at most 0.9487/√m, 0.4331/√m (live prime 3 or none) or 1/√m (a live prime ≥ 5).
  Largest √m·(share of signings bad only at composite d) met in these runs: 0.0371 (the share 3/256, m = 10,
  Z_45). That is true of my tests only; the referee's counts met 0.0765 and 0.0781 (§0, "Not proved").
- `heavy3.py` (outputs `heavy3-seed1.out`, `heavy3-seed2.out`): Theorem 1 beyond the table. h copies of 0 and a
  decoration on Z_3, Z_9, Z_27, exact (Python integers, the events F_i from their definition by class sums);
  asserted: share·√m ≤ 0.9487 (m even), 0.9379 (m even, m > 1000), 0.4331 (m odd), 0.40 (m odd, m > 200), compared
  as rationals. **9488 multisets** (5000 + 4488), 3211 of them with m > 1000 (up to m = 10017). (A first run, with
  the weaker limits 0.958 and 0.44, had 13511 multisets and no failure; its outputs were overwritten.)
  Largest met: 0.928772 at m = 10012 (Z_27, 10000 copies of 0 and pairs at 1, 2, 3, 6, 9, 18).
- Data on K (the brief's K_same; not used in any proof). `kpairs.py` (mine: pair sums and long division;
  `kpairs.out`): 37/32 on Z_9 and 4773/4096 on Z_45 as in the brief; 149/128 on Z_27 (pairs at 1, 2, 3, 6, 9, 18);
  597/512 on Z_81 (… and 27, 54); **19221/16384 = 1.173157 on Z_135** (pairs at 5, 10, 15, 30, 45, 90 and at 27, 54,
  81, 108), that is 0.936044/√m. `kdeep.py` (the brief's own `kdec.py`, used as it is; `kdeep-a.out`) gives the
  same 37/32, 149/128, 597/512. With the argument `pp`, `kpairs.py` counts only d = 1 and the prime powers
  (`kpairs-pp.out`; the option was added after `kpairs.out` was made, and the three cases run again without it
  gave the same numbers): 149/128 of the 4773/4096 on Z_45 and 75/64 of the 19221/16384 on Z_135. So in these two
  examples (both with m even) the composite divisors add only 5/4096 and 21/16384 to K. Nothing more is shown
  about what Corollary 4 leaves out: the referee's counts (§0, "Not proved") have a family where it is about
  0.05/√m. Since the referee's report: the pairs are not the best at a given depth (fours at the deepest level:
  2385/2048 on Z_27 for pairs at 1, 2, 3, 6 and fours at 9, 18; 9553/8192 on Z_81 for pairs at 1, 2, 3, 6, 9, 18
  and fours at 27, 54; these are the referee's counts, and `kpairs.py` gives the same in runs that are not
  saved), and 19221/16384 is not the largest K known (§0, on (c)).
- `consts.py`: the constants of §4; `rec3.py`, `tail3.py`: §3.

## 7. Files (all in this folder)

`result.md`; `rec3.py`, `rec3-1000.out`, `table3-1000.txt`, `tail3.py`, `tail3.out` (Theorem 1); `recp.py` (the
recursion for any p, by partitions; used by `consts.py` and `test_pp.py`); `consts.py`, `consts.out` (Theorem 2);
`test_pp.py`, `test-pp-seed3.out`, `test-pp-seed4.out`, `test-pp-seed5.out`, `heavy3.py`, `heavy3-seed1.out`, `heavy3-seed2.out`
(tests); `kpairs.py`, `kpairs.out`, `kpairs-pp.out`, `kdeep.py`, `kdeep-a.out` (data on K); `fixedsign.py`, `fixedsign.out` (the
remark on lead 3). The empty `*.err` files are the error streams of the background runs.

## 8. Changes after the referee's report

The report is `../report-referee-two.md`; the referee's programs are in `../referee-two/`. In its own words: "I
found no gap in any proof and no failure in any exact count; what needs changing is credits and wording." And
from its part 5 ("Not read or not checked"): "Read: `rec3.py`, `tail3.py`, `recp.py`, `consts.py`, `test_pp.py`,
`tail3.out`, the head of `rec3-1000.out`, four lines of `consts.out`. Not read: `heavy3.py`, `kpairs.py`,
`kdeep.py`, `fixedsign.py` and the test outputs. The author's test counts are not verified." "Proofs of Theorem Q,
(F2) and Corollary U: not read. The latter two are covered only by my counts." "Not checked: Wallis's product
itself; whether (M) is true or sufficient; whether lead 2 can be closed with a large C; the process notes."
The changes below were made after its reading (begun 03:37 UTC) and have been read by nobody.

**Changed** (numbers 1 to 7 are the referee's required changes; "old" is the text as sent).
1. *Credits for the powers of 3.*
   - §0, after Theorem 1: new paragraph "What of Theorem 1 was already in hand …" (Theorems A and B of
     `quarter/one/result.md`), close to the referee's wording.
   - §0, "Whose is what": new item "From `quarter/one/result.md`, which I had NOT read …", with what I have now
     read of it (lines 36 to 44 and 204 to 216), what is a confirmation and what is new for p = 3. In "Mine",
     old: "carrying that recursion to a bound that falls like 1/√m for every m"; new: "for the powers of 3, the
     sharpening for even m just named". Old: "I did not search the four older texts for these; I read only the
     brief and `quarter/three/result.md`."; new: the list of the texts I did not read.
   - §0, on (c). Old: "κ/2 = 0.39894 ≤ L_odd ≤ 0.40"; new: "L_odd = κ/2 = 0.39894 exactly, by Theorem A of
     `quarter/one/result.md` …; my own tail gives only L_odd ≤ 0.40".
   - §3, the item on odd m: new sentence "This confirms Theorem A …".
2. *§5 and "Not proved".*
   - §5. Old: "So the induction of lead 2 does not close with pairs alone, for any C."; new: "So: with pairs
     alone the first split takes up to 0.593 of the budget C/√m for p = 5 whatever C (0.263 for p = 7, at another
     m); the prime-power part takes 1.18/C by Corollary 4; I did not compute the deeper levels, nor whether the
     rest fits for a large C, and I could not close it." Old: "0.046, 0.019 for p = 11, 13: together 0.92 of the
     budget C/√m, before the powers of 3 (about 0.95/C) and the deeper levels"; new: "0.046, 0.019 for p = 11, 13,
     each at its own m …, so at one m their sum is less than the 0.92 they add up to". Old: "this is good
     enough" and "it is not"; new: "this is better" and "it costs much".
   - §0, "Not proved". Old: "does not close for them as it stands, and I can say where"; new: "I could not close
     the induction for them, and I can say where it gets hard". Old: "their weight is 0.593·C/√m whatever C. The
     missing statement is (M) in §5."; new: "their weight is up to 0.593·C/√m whatever C; I did not compute
     whether the rest fits for a large C. A missing statement is (M) in §5; I have not shown that (M) would
     suffice."
   - §5, before (M). Old: "because the first split itself is missing:"; new: "because for the first split
     itself a statement is missing. One such statement (I have not shown that it would suffice, and I do not
     know whether it is true):".
   - (M). Old: "are equal at some root of unity x ≠ 1"; new: "are equal and not zero at some root of unity x ≠ 1",
     with a paragraph under (M) that says why. This takes the referee's remark that (M) also counted signings
     with all slices zero, with one difference from its wording: such signings are bad at the order of x, not
     necessarily at 1.
   - "Whose is what". Old: "and it failed (§5)"; new: "and could not close it (§5)". Old: "the obstruction
     computed in §5"; new: "the weights computed in §5".
3. *Theorem Q removed from Theorem 2.*
   - §2 (d). Old: "(d) u_t ≤ β(r_t): at most 1/2, at most 3/8 for r_t ≥ 3, and 0 for r_t = 1 (Theorem Q; X_p ⊔ F_0
     is a set of bad signings of B_t)."; new: the referee's argument, which gives the same two bounds from Lemma
     2 and the induction hypothesis of §4. I checked it: a_p/√p < 0.09 and c(r) + a_p/√r < 3/8 for even r ≥ p, for
     the primes 5 to 59, by a computation (the one exception is p = 5, r = 6, as the referee says); e_5(6) = 0 by
     hand from Lemma 2. It is right.
   - §4: "the bounds 1/2 and 3/8 for u are those of (d)" and "(both by (d))" added where (d) is used.
   - §0. Corollary 3: new sentences "Corollary 3 does not rest on Theorem Q … For powers of 3 it still uses one
     thing from last night: the exception (e) …". "Whose is what": old: "Theorem Q (only as "β(r) ≤ 1/2 for all r,
     β(r) ≤ 3/8 for r ≥ 3"; used in Theorem 2 only; Theorem 1 does not need it)"; new: "Theorem Q is NOT used any
     more …", and the new item "The referee's".
4. *The data on signings bad only at composite d.*
   - §0, "Not proved". Old: "In my tests such signings were rare (the largest √m·share met was 0.037: 3/256 at
     m = 10), and in the two largest examples known for even m they add 5/4096 and 21/16384 to a constant K of
     about 1.17 (§6)."; new: "How large the share of such signings can be is not shown either. In my tests … The
     referee's counts met more: … that is all that is shown about how little Corollary 4 leaves out."
   - §6. Old: "what Corollary 4 leaves out is small there"; new: "Nothing more is shown about what Corollary 4
     leaves out: …". After "0.0371 (the share 3/256, m = 10, Z_45)": new: "That is true of my tests only; …".
5. *Credits to the leads.* "Whose is what": new item "Lead 1 of the brief" (the top-term bound of §4 is lead 1's
   prime-level estimate, sharpened); old in "Lead 2": "(x = 1, the sums of signs are compared directly; the
   factor 1/√m is one binomial factor for the largest class)"; new: "(x = 1, the sums of signs are compared
   directly)", the factor now being credited to lead 1. Old in "Mine": "the exact top constant τ_p = √p·2^(1−p)";
   new: "the value τ_p = √p·2^(1−p) of the top constant (the bound itself is lead 1's, see below)". §4: the
   heading of the top term names lead 1. Remark (1) under "Errors found". Old: "(1) Lead 2 says "the prime 3
   needs more"; for the prime 3 the recursion of `quarter/three/result.md` §2 is enough (Theorem 1), because the
   root of unity is 1 there; it is the primes p ≥ 5 with a root x ≠ 1 that need more."; new: "(1) Not a
   correction of lead 2: … its last clause already names a recursion on the tree of 3 as what could do it. …".
6. *Rounding.* Proof of Corollary 4. Old: "(0.948695 + 0.22964)/√m"; new: "(0.9487 + 0.22964)/√m". §3: after
   "0.948695 at m = 30": "(even; it is 0.94869505…, so these six digits are rounded DOWN, and the bound to use is
   0.9487)", and "rounded up" for 0.433013. Theorem 2: "(these four are rounded UP: the values are 0.18108011,
   0.04433267, 0.00325611, 0.00088153)"; the first, second and fourth are the referee's digits, the third mine.
7. *The data on K.* §0, on (c). Old: "which points to 7/6 in the limit (7κ/6 = 0.9309; not proved)"; new: "which
   points to 7/6 as the limit of this family of pairs ONLY (…). The pairs are not the best at a given depth: by
   the referee's counts, fours at the deepest level give more (2385/2048 on Z_27, 9553/8192 on Z_81; …), whence
   L_even ≥ 0.93044." Old: "0.9303 ≤ L_even"; new: "0.9304 ≤ L_even". Old: "more than the brief's largest
   (4773/4096 = 1.16528), so β(m)·√m ≥ about 0.936 for large even m."; new: "… but NOT the largest known: by the
   referee's report the first text of this round has 78764625/67108864 = 1.173684 on Z_135 …; I have not read
   that text. So β(m)·√m ≥ about 0.9365 for large even m (0.936 by my own value)." §6, the item on K: new
   sentence "Since the referee's report: …". "Mine": "(the larger value on Z_135 is the first text's of this
   round, see (c) above)".
8. *Not one of the seven:* the second line of the text. Old: "Nobody has read this text but me."; new: "When it
   was sent nobody had read this text but me; since then a referee (a fresh instance) has read it, and the
   changes it required are made here and listed in §8." Made so that the head does not contradict this section.

**Not changed.** The statements and constants of Theorems 1 and 2 and of Corollaries 3, 4, 5; Lemma 2 and its
consequences other than (d); the proofs of §3 and §4 other than the two references to (d); the tests and their
counts; §1, §7; the process note of §0; every program and output.

**Three sentences of the report that I find are not quite so** (the text above says what I find instead).
(i) Its 2.2: signings with all slices zero "are already bad at 1": they are bad at the order of x, and need not
be bad at 1 (three elements filling a group of 3, with equal signs, have slice 0 at a cube root of unity and
sum ±3). (ii) Its 2.4: "5/256, 5/512 and 35/2048 at m = 10, 11, 12" and "for all odd m": by my count the family
has (1/16)·q(h) for odd h only, that is, for even m, and none at m = 11; the 5/512 at m = 11 is, by the referee's
output `bruteD.out`, the largest on Z_15 at m = 11, and belongs to another multiset (five copies of 0 and 1, 2,
3, 7, 9, 11; I counted it again: 5/512). (iii) Its 2.3: "Corollary 3 is then independent of last night's
proofs": of the proofs of Theorem Q, yes; for powers of 3 it still uses Remarks 3.2 and 3.3 of last night's
third text (which the referee, by its report, rederived).

**What I newly rely on, and how far I checked it.** The statements of Theorems A and B of `quarter/one/result.md`:
read, their proofs not. The referee's (d): checked as said under 3. The referee's counts of signings bad only at
composite d (1/32, 171/8192, the family, 5/512): counted again by my own route (the definition, by long
division), the same. Its K values 2385/2048 and 9553/8192: `kpairs.py` gives the same. The first text's
78764625/67108864 on Z_135: taken from the referee's report, not checked by me. Its 0.94869505, its "largest Ê
over even m is 309/8192 at m = 14" and its digits of a_5, a_7, a_13: recomputed from my table and my formulas, the
same (0.9486950543; 0.18108011, 0.04433267, 0.00088153).

**Process in this revision.** The checks ran through the cap script (programs given on standard input, and three
runs of `kpairs.py`), one at a time; their outputs are not saved, and no file but this one was created or
changed. One slip: a bare call of the interpreter (a stray line of mine at the end of a command; it printed one
word and computed nothing). I read the whole of the referee's report, also its part 3, which quotes numbers of
the other two texts of this round; in `../referee-two/` I read the list of files and the lines of its outputs
found by searching for "5/512", "171/8192" and "composite". I did not open the folders `one/`, `three/` of this
round or any `expect` file. Nothing is left running.
