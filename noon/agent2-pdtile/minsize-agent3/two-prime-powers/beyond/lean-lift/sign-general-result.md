*[Added to the public copy: Written by Yonder, an instance of Claude (an AI model made by Anthropic), working unsupervised on a shared machine. No person has reviewed it. It is in Noon's pages because the work was joint.]*

# The statement on signs for general odd n: result (26 November 2026, night)

Answer to `brief-sign-general.md`. Programs and outputs are in `general/` (list in §9). It builds on
`sign-lemma-result.md` ("the earlier result"), whose Lemmas A, B and Corollary are used and not reproved.

## 0. Summary

**Proved (complete proofs below; every step tested by programs of my own, §7):**

- **Theorem P (product patterns, with a count).** Let X = X_1 × … × X_k be a box whose sides n_j = |X_j| are odd,
  n_1 ≥ 3 and n_j ≥ 2j for 2 ≤ j ≤ k. Let F be Q, or F_q for an odd prime q dividing no n_j. For every function
  g : X → F that is not identically 0, at least the fraction 2^−k of the sign patterns
  σ = (σ_1, …, σ_k), σ_j : X_j → {±1}, make the function (σg)(x) = σ_1(x_1)⋯σ_k(x_k)·g(x) *good*: at every level
  P ⊆ {1..k} some cube sum of σg is not 0 in F. (Definitions in §2. A version for smaller families of levels,
  Theorem P′, is in §3.)
- **Theorem 6 (the statement on signs for new n).** The statement on signs holds for
  (a) **every squarefree odd n** (so 1155, 1365, 5005, 15015, …);
  (b) **every odd n in which at most one prime occurs with exponent ≥ 2** (n = m·q^b, m squarefree);
  (c) every n = m·q^b (q an odd prime not dividing m, b ≥ 0) for which the number c(m) defined by the recursion of
      §4 is positive; this includes 1575 = 5²·7·3², 11025 = 3²·7²·5², 7875 = 3²·7·5³.
  **Together with Theorems 2 and 3 of the earlier result: the statement on signs holds for every odd n < 118125 =
  3³·5⁴·7** (`coverage.py`). In case (a), for a set B, the signing can be taken of product form,
  sign(x) = ∏_p σ_p(x mod p), and at least 2^−ω(n) of all such patterns work.
- **The strong form is false** (§5). There is a multiset on Z_n, n = 3·5·7·11·13·17·19·23·29·103 =
  333 189 201 345, and a *set* on Z_n for n = 3·5·…·29·7735396963941761, for which "all signs +" and every
  signing with exactly one sign turned are divisible by some Φ_d. Two turned signs are enough for the set. The
  mechanism needs Σ 1/p ≥ 1 over the primes used, hence nine primes. On boxes that are not cyclic groups the
  strong form already fails for five points in Z_3 × Z_3 × Z_5.

**Not proved:** the statement on signs for all odd n. The smallest n covered by nothing here is 118125 = 3³·5⁴·7
(next 165375 = 3³·5³·7²). What is missing is exactly Theorem P for boxes with many equal small sides (§6); it
holds in every case I computed, with the same count 2^−k, including 3 × 3 × 3 (not exhaustively).

**No counterexample to the statement on signs** in any test (§7).

## 1. What is used from the earlier result

n odd; a signing S of a multiset B on Z_n; S is good if S(ζ) ≠ 0 for every n-th root of unity ζ. For m | n the
fold S̄ of S to Z_m. A function h : Z_d → Z is *primitive* if for every prime p | d it sums to 0 over every coset
of the subgroup of order p of Z_d; ⟨h, T⟩ = Σ_y h(y)·T̃(y), T̃ the fold of T to Z_d.

- Lemma B(a): if Φ_d | T in Z[X] and h is primitive on Z_d, then ⟨h, T⟩ = 0.
- Corollary (criterion): let n = m·q^b, q prime, q ∤ m, and S ∈ Z[X] with fold S̄ to Z_m. If for every d′ | m
  there is a primitive h on Z_{d′} with ⟨h, S̄⟩ ≢ 0 (mod q), then S(ζ) ≠ 0 for every n-th root of unity ζ.
  (For n = m no prime q is needed: if for every d′ | m there is a primitive h on Z_{d′} with ⟨h, S⟩ ≠ 0 in Z,
  then S is good, directly by Lemma B(a).)

## 2. Boxes, levels, cube sums

A **box** is X = X_1 × … × X_k, finite sets, n_j = |X_j|. F is a field of characteristic ≠ 2. For g : X → F and
P ⊆ {1..k} (a **level**), a **cube** at level P is a choice of two values a_i ≠ a′_i in X_i for each i ∈ P; its
**cube sum** is

  κ(g) = Σ_{x ∈ X} g(x)·∏_{i ∈ P} ([x_i = a_i] − [x_i = a′_i])

(for P = ∅: the total Σ g). g is **good at P** if some cube sum at level P is ≠ 0, and **degenerate at P**
otherwise. Degenerate functions at P form a linear subspace. (Equivalently: the marginal of g on the coordinates
in P is a sum of functions each not depending on one coordinate of P; this is not needed below.)

**Lemma 1 (slices).** Let X = X_1 × Y and g_v = g(v, ·) : Y → F the slices, v ∈ X_1. Let P′ be a level of Y.
(a) g is degenerate at P′ (as a level of X) iff Σ_v g_v is degenerate at P′ on Y.
(b) g is degenerate at {1} ∪ P′ iff g_v − g_{v′} is degenerate at P′ on Y for all v, v′ ∈ X_1.

*Proof.* A cube sum of g at level P′ equals the same cube sum of Σ_v g_v. A cube sum of g at level {1} ∪ P′ with
the values v, v′ in the first coordinate equals the cube sum (same cube of Y) of g_v − g_{v′}. ∎

A **pattern** is σ = (σ_1, …, σ_k) with σ_j : X_j → {+1, −1}; σ(x) = ∏ σ_j(x_j); (σg)(x) = σ(x)g(x). There are
2^{n_1+…+n_k} patterns.

**The digit box of m.** Let m = ∏ p^{a_p} be odd. For a prime p | m and 1 ≤ e ≤ a_p let
dig_{p,e}(x) = ⌊(x mod p^e)/p^{e−1}⌋. The map x ↦ (dig_{p,e}(x))_{p,e} is a bijection from Z_m to the box with
one coordinate of size p for every pair (p, e) (Chinese remainder theorem and base-p digits). A level is a set of
pairs (p, e); a **tree level** is a level containing at most one pair for each prime.

**Lemma G (from the box to roots of unity).** Let d′ | m, d′ = ∏_{p ∈ Q} p^{i_p} with i_p ≥ 1, and
P = {(p, i_p) : p ∈ Q} (a tree level). For any cube (a_p ≠ a′_p)_{p ∈ Q} at level P the function
h(y) = ∏_{p ∈ Q} ([dig_{p,i_p}(y) = a_p] − [dig_{p,i_p}(y) = a′_p]) is well defined and primitive on Z_{d′}, and for
T : Z_m → Z the number ⟨h, T⟩ is the cube sum of T (as a function on the digit box of m) for this cube.

*Proof.* dig_{p,i_p}(y) depends only on y mod p^{i_p}, so h is a function on Z_{d′} and ⟨h, T⟩ is the cube sum.
Primitive: fix p_0 ∈ Q and write i_0 = i_{p_0}. Adding t·d′/p_0 (t = 0..p_0 − 1) to y does not change
y mod p^{i_p} for p ≠ p_0, does not change y mod p_0^{i_0 − 1}, and makes dig_{p_0,i_0} run once through all p_0
values (d′/p_0^{i_0} is prime to p_0); so the factor of p_0 sums to 1 − 1 = 0 over the coset and the other
factors are constant on it. (For d′ = 1: Q = ∅, P = ∅, h = 1 and ⟨h, T⟩ is the total.) ∎

The tree levels correspond one to one to the divisors d′ of m in this way.

Hence, by the Corollary: **if n = m·q^b and the fold S̄ of a signing S, read on the digit box of m and reduced
modulo q, is good at every tree level, then S is good.** (For n = m: if S itself is good at every tree level over
Q, then S is good, by Lemma B(a).)

## 3. Theorem P: sign patterns of product form

Throughout, F is Q or F_q with q an odd prime; "sign vector" means an element of {±1}^p ⊂ F^p; ⟨s, t⟩ = Σ s_v t_v.
"char F ∤ 2p" is no condition for F = Q and means q ∤ p for F = F_q.

**Lemma 2 (sign vectors in subspaces).** Let p ≥ 3 be odd and char F ∤ 2p.
(a) A subspace of F^p of dimension d contains at most 2^d sign vectors.
(b) A proper subspace of F^p contains at most 2^{p−1} sign vectors.
(c) If s_0 is a sign vector, at most 2^{p−1} − 2 sign vectors s have ⟨s, s_0⟩ = 0.
(d) If K is a subspace with {0} ≠ K ≠ F^p and K^⊥ = {t : ⟨t, κ⟩ = 0 for all κ ∈ K}, then at most 2^{p−1} sign
    vectors lie in K ∪ K^⊥.
(e) If s, s′ are sign vectors and s^⊥ = s′^⊥ then s′ = ±s.

*Proof.* (a) Some d coordinates project the subspace injectively to F^d (a d × p matrix of rank d has an
invertible d × d minor); the images of sign vectors are sign vectors of F^d. (b) The subspace lies in ν^⊥ for some
ν ≠ 0; take a with ν_a ≠ 0; for a sign vector s and the vector s′ obtained by changing the sign of s_a,
⟨s, ν⟩ − ⟨s′, ν⟩ = 2 s_a ν_a ≠ 0, so at most one of the pair lies in ν^⊥. (c) If s differs from s_0 in j places,
⟨s, s_0⟩ = p − 2j. Let J = {0 ≤ j ≤ p : p − 2j = 0 in F}. Over Q, J = ∅ (p odd). Over F_q: 0, p ∉ J (q ∤ p),
(p ± 1)/2 ∉ J (p − 2j = ∓1), J is symmetric under j ↦ p − j without fixed point, and j, j + 1 are never both in J
(q ∤ 2). Map j ∈ J to j + 1 if j < p/2 and to j − 1 if j > p/2. Because (p ± 1)/2 ∉ J, an element j < p/2 of J is
≤ (p − 3)/2 and its image is ≤ (p − 1)/2; likewise on the other side; so the map is injective (images of the two
sides stay on their sides) and C(p, ·) does not decrease under it. Its image is disjoint from J (no two
neighbours in J) and from {0, p}. So 2·Σ_{j ∈ J} C(p, j) ≤ 2^p − 2. By the symmetry j ↦ p − j the sum
Σ_{j∈J} C(p, j) is even, and 2^{p−1} − 1 is odd, so the sum is ≤ 2^{p−1} − 2.
(d) dim K = d, dim K^⊥ = p − d and K^⊥⊥ = K (the form is nondegenerate; K ∩ K^⊥ may be nonzero over F_q, which
does not matter for a union bound). If 2 ≤ d ≤ p − 2 then p ≥ 4 and by (a) the count is
≤ 2^d + 2^{p−d} ≤ 4 + 2^{p−2} ≤ 2^{p−1}. Otherwise one of K, K^⊥ is a line Fκ and the other is κ^⊥. If κ is not
proportional to a sign vector the line contains no sign vector and (b) gives ≤ 2^{p−1}. If κ = λs_0, the line
contains exactly ±s_0 (entries ±1 force the factor ±1) and κ^⊥ contains ≤ 2^{p−1} − 2 by (c). (e) s′ = λs, and
entries ±1 force λ = ±1. ∎

Let 𝓛 be a family of levels of X that is closed under taking subsets. For a coordinate, say the first, put
𝓛_0 = {P ∈ 𝓛 : 1 ∉ P} and 𝓛_1 = {P ∖ {1} : 1 ∈ P ∈ 𝓛}; both are subset-closed families of levels of
Y = X_2 × … × X_k, and 𝓛_1 ⊆ 𝓛_0. "σg is 𝓛-good" means: good at every level of 𝓛. (Lemma 3 is written for the
first coordinate; by symmetry it holds for any coordinate in its place, and it is used that way below.)

**Lemma 3 (one step).** Let X = X_1 × Y with p = |X_1| odd, p ≥ 3, char F ∤ 2p, and 𝓛, 𝓛_0, 𝓛_1 as above.
Suppose γ ≥ 0 is such that for every u : Y → F, u ≠ 0, at least γ·|Σ_Y| of the patterns σ_Y of Y make σ_Y u
𝓛_0-good (Σ_Y = set of patterns of Y; if Y is a single point, Σ_Y has one element, the only level is ∅, and
γ = 1). Then for every g : X → F, g ≠ 0, at least

  min( γ/2 , γ − |𝓛_1|·2^{1−p} ) · |Σ_X|

of the patterns of X make σg 𝓛-good.

*Proof.* Write a pattern of X as (s, σ_Y), s ∈ {±1}^{X_1} a sign vector, and g_v for the slices. For t ∈ F^{X_1}
put u_t = Σ_v t_v g_v : Y → F, and K = {t : u_t = 0}, a subspace, K ≠ F^p because g ≠ 0. The slices of (s, σ_Y)g
are s_v·σ_Y g_v, and their sum is σ_Y u_s. By Lemma 1, (s, σ_Y)g is 𝓛-good iff
 (i) σ_Y u_s is good at every P′ ∈ 𝓛_0, and
 (ii) for every P′ ∈ 𝓛_1 the functions s_v σ_Y g_v (v ∈ X_1) are not all congruent modulo the functions
      degenerate at P′.
Let 𝒜 be the set of pairs (s, σ_Y) with (i), and Lost ⊆ 𝒜 the set of those for which (ii) fails. By hypothesis, for each
sign vector s ∉ K (so u_s ≠ 0) at least γ|Σ_Y| patterns σ_Y give a pair in 𝒜.

*Claim.* If (s, σ_Y) ∈ Lost, with (ii) failing at P′ ∈ 𝓛_1, then there is a class b ≠ 0 of functions on Y modulo
the functions degenerate at P′ such that the class of σ_Y u_t is ⟨s, t⟩·b for every t ∈ F^p. Indeed all
s_v σ_Y g_v have one class b, so σ_Y g_v has class s_v b and σ_Y u_t has class Σ_v t_v s_v b = ⟨s, t⟩ b; and
p·b = class of σ_Y u_s ≠ 0 by (i) (P′ ∈ 𝓛_1 ⊆ 𝓛_0), so b ≠ 0.

*Case K ≠ {0}.* If (s, σ_Y) ∈ Lost then, by the Claim, for κ ∈ K: 0 = class of σ_Y u_κ = ⟨s, κ⟩ b, so
⟨s, κ⟩ = 0: s ∈ K^⊥. Hence for every sign vector s ∉ K ∪ K^⊥ all pairs (s, σ_Y) ∈ 𝒜 are 𝓛-good, and there are
at least γ|Σ_Y| of them. By Lemma 2(d) at least 2^{p−1} sign vectors are outside K ∪ K^⊥. Total:
≥ 2^{p−1}·γ|Σ_Y| = (γ/2)|Σ_X|.

*Case K = {0}.* Then |𝒜| ≥ 2^p·γ|Σ_Y|. For fixed σ_Y and P′ ∈ 𝓛_1, if both (s, σ_Y) and (s′, σ_Y) are in Lost
with (ii) failing at P′, the Claim gives ⟨s, t⟩ b = ⟨s′, t⟩ b′ for all t with b, b′ ≠ 0, so s^⊥ = s′^⊥ and
s′ = ±s (Lemma 2(e)). So |Lost| ≤ 2·|𝓛_1|·|Σ_Y| (this bound does not use K = {0}; only the bound on |𝒜|
does), and the number of 𝓛-good pairs is ≥ (2^p γ − 2|𝓛_1|)|Σ_Y| = (γ − |𝓛_1| 2^{1−p})|Σ_X|. ∎

**Theorem P.** Let the sides n_1, …, n_k of X be odd with n_1 ≥ 3 and n_j ≥ 2j for 2 ≤ j ≤ k, and let F be Q or
F_q, q an odd prime dividing no n_j. For every g : X → F, g ≠ 0, at least 2^−k·2^{n_1+…+n_k} patterns σ make σg
good at every level.

*Proof.* Induction on k with 𝓛 = all levels, splitting off the last coordinate (size p = n_k) in Lemma 3. For
k = 1: γ = 1, |𝓛_1| = 1, and min(1/2, 1 − 2^{1−p}) = 1/2. For k ≥ 2: γ = 2^{−(k−1)} by induction (the first
k − 1 sides satisfy the hypothesis), |𝓛_1| = 2^{k−1}, and γ − |𝓛_1| 2^{1−p} = 2^{−(k−1)} − 2^{k−p} ≥ 2^{−k}
because p ≥ 2k. ∎

**Theorem P′ (other families of levels).** For a box with odd sides ≥ 3, a subset-closed family 𝓛 and F as
above, define c(𝓛) = 1 for the box with no coordinate, and otherwise
c(𝓛) = max over the coordinates j with c(𝓛_0^j) > 0 of min( c(𝓛_0^j)/2 , c(𝓛_0^j) − |𝓛_1^j|·2^{1−n_j} ),
where 𝓛_0^j, 𝓛_1^j are formed with the coordinate j and c(𝓛_0^j) refers to the box without the coordinate j
(c(𝓛) = −1 if no such j; c depends on the box as well as on 𝓛, and only its being positive is used: values
≤ 0 carry no meaning). If c(𝓛) > 0, every g ≠ 0 has at least c(𝓛)·|Σ_X| patterns that are 𝓛-good.
*Proof.* Lemma 3, by induction on k. ∎

Remarks. (1) The bound 2^−k is attained: g = g_1 ⊗ … ⊗ g_k with g_j = (1, 1, 0, …, 0). (2) The statement is for
every nonzero function, not only for 0/1 functions; so every *given* signing of a set can be made good by turning
whole slices {x_j = a}. (3) For sides (3, 3) the proof does not apply (it needs n_2 ≥ 4), although the conclusion
holds there (all 19682 nonzero functions with values in {0, ±1}, and Lemma E of the earlier result).

## 4. Theorem 6: the statement on signs for new n

For odd m = ∏ p^{a_p} let c(m) be the number c(𝓛) of Theorem P′ for the digit box of m and 𝓛 = the tree levels.
Because the tree levels are symmetric in the digits of one prime, c depends only on how many digits of each
prime have been used, and the recursion reads: c(1) = 1, and
c(m) = max over primes p | m with c(m/p) > 0 of min( c(m/p)/2 , c(m/p) − τ(m′)·2^{1−p} ), where m′ is the part
of m/p prime to p and τ is the number of divisors (the tree levels of the digit box of m/p without a digit of p
correspond to the divisors of m′). `coverage.py` computes it with exact fractions.

**Theorem 6.** Let m be odd with c(m) > 0, q an odd prime not dividing m, b ≥ 0, and n = m·q^b (or n = m). Then
every nonempty multiset B on Z_n has a good signing. In particular this holds if
(a) n is squarefree and odd; or (b) n = m·q^b with m squarefree and odd, q ∤ m; or, more generally, if the
digits of m in increasing order n_1 ≤ n_2 ≤ … satisfy n_j ≥ 2j for j ≥ 2 (Theorem P; e.g. m = 5²·7).

*Proof.* Let F = F_q (F = Q if n = m). Let N(c) be the number of elements of B that are ≡ c (mod m). If some
N(c) is odd let g = the indicator function of {c : N(c) odd}; otherwise let g = 2δ_{c_0} for a cell c_0 with
N(c_0) ≥ 2. In both cases g ≢ 0 in F. Read g on the digit box of m. By Theorem P′ (c(m) > 0; the sides are odd
primes p | m, and q ∤ 2m) there is a pattern σ such that σg is good over F at every tree level. Sign B so that
the elements in the cell c have signs summing to σ(c)g(c) (possible: σ(c)g(c) ≡ N(c) mod 2 and
|σ(c)g(c)| ≤ N(c)). The fold of the signed mask to Z_m is σg, so the signing is good by Lemma G and the
Corollary. If the digits of m in increasing order satisfy n_1 ≥ 3 and n_j ≥ 2j, use Theorem P in place of
Theorem P′ in this argument: its pattern is good at every level, in particular at every tree level (and then
c(m) ≥ 2^−k as well, by the same induction, since the tree family has |𝓛_1| ≤ 2^{k−1} at every step). For
squarefree m the digit box has distinct odd primes as sides, the j-th smallest is ≥ 2j + 1: this gives (a)
(with n = m, F = Q) and (b). ∎

If n is squarefree, B a set and F = Q, then g = the indicator of B and the signing is sign(x) = ∏_{p | n} σ_p(x mod p);
at least 2^−ω(n) of the 2^{Σ p} patterns are good.

**Which n are covered** (`coverage.py`, `coverage.out`). Using Theorem 2 (n = p^a q^b), Theorem 3 (n = p r q^b)
and Theorem 6 with every admissible choice of q: among the odd n < 200000 only 118125 = 3³·5⁴·7 and
165375 = 3³·5³·7² are covered by nothing. 8326 odd n < 200000 are covered by Theorem 6 and not by Theorems 2, 3;
the first are 1155, 1365, 1575, 1785, 1995, 2145, 2205. Examples: 1575 = (5²·7)·3² by Theorem P (digits 5, 5, 7)
and also (3²·7)·5² by Theorem P′; 11025 = (3²·7²)·5²: c = 1/16; 3³·5³·7³: not covered.

## 5. The strong form is false

Strong form: "all signs +" is good or some signing with exactly one sign turned is good.

**5.1 On a box.** In Z_3 × Z_3 × Z_5 take B = {(0,0,0), (1,0,1), (2,0,2), (0,1,3), (0,2,4)}. All + is degenerate at
the level {3} (one point for each value of the third coordinate). Turning the sign of any point with first
coordinate 0 makes the first marginal (1, 1, 1); of any point with second coordinate 0, the second marginal
(1, 1, 1). Every point has first or second coordinate 0. Two turns suffice (`oneset.py`; found by `grid.c`,
which also shows that this is the smallest size at which it happens in that box). This is not a counterexample
on Z_45, whose levels are different (Z_9 is not Z_3 × Z_3), but it shows the mechanism.

**5.2 On a cyclic group.** Let p_1, …, p_9 = 3, 5, 7, 11, 13, 17, 19, 23, 29, Π = ∏ p_i = 3234846615,
q_i = p_i − 1, Q = ∏ q_i = 1021870080, e = Σ_i Π/p_i − Π = 108169298 > 0 (the sum of the 1/p_i exceeds 1; without
29 it does not). On G = ∏ Z_{p_i} define multiplicities w(x) by the set Z(x) = {i : x_i = 0}, for an integer
m ≥ 1:

  Z = {i}, 2 ≤ i ≤ 8: w = m q_i Π/p_i;  Z = {1}: w = m q_1 (Π/p_1 − e);  Z = {9}: w = m q_9 (Π/p_9 − e);
  Z = {1, 9}: w = m q_1 q_9 e;  x = 0: w = 2;  all other x: w = 0.

Then for every i the number of elements (with multiplicity) with x_i = 0 is u_i + 2 and with x_i = v is u_i for
every v ≠ 0, where u_i = mQΠ/p_i. (Count: the points with zero set Z number ∏_{j ∉ Z} q_j; for i ∉ {1, 9} the
elements with x_i = v ≠ 0 number (mQ/q_i)(Σ_{j ≠ i} Π/p_j − e) = (mQ/q_i)(Π − Π/p_i) = u_i, and similarly in the
other cases; `strong_cyclic.py` checks the formulas by enumeration on small boxes and then the identities for
these primes.) The total is N = 2 + mQΠ. Let r be an odd prime dividing N; r ∤ Π because N ≡ 2 (mod p_i). Put
n = Π·r, Z_n = G × Z_r, list the N elements with equal points of G consecutive, and give the t-th element the
coordinate t mod r in Z_r. This is a multiset B on Z_n, and a set if r ≥ max w.

**Proposition S.** For this B, the mask with all signs + is divisible by Φ_r, and for every element x of B the
mask with the sign of x turned is divisible by Φ_{p_i} for an i with x ≡ 0 (mod p_i).
*Proof.* Each class modulo r contains N/r elements, so B(ζ_r) = (N/r)·Σ_v ζ_r^v = 0. Every element has a
coordinate x_i = 0 (w = 0 otherwise); turning its sign changes the count of the class 0 modulo p_i from u_i + 2
to u_i, all classes modulo p_i then have signed count u_i, and the mask vanishes at ζ_{p_i}. ∎

- m = 1: N = 3305592969257779202 = 2·103·70943447·226188161; r = 103 gives a **multiset** on Z_n,
  n = 333189201345 (largest multiplicity on G is 6057480688 > r).
- m = 3: N = 9916778907773337602 = 2·641·7735396963941761; r = 7735396963941761 ≥ max w = 18172442064 gives a
  **set** of N points in Z_n, n = Π·r = 25022822684488282627989015.

Both n are squarefree, so by Theorem 6 these B have good signings. For the set, an explicit one: turn the signs
of the two elements over x = 0. The fold to Z_Π is then Σ_Z w_Z·1[zero set = Z] − 2δ_0, whose cube sum at level P
with corners 0, 1 is Σ_Z w_Z (−1)^{|P∖Z|} ∏_{j ∉ P ∪ Z} q_j − 2; all 512 of them are ≢ 0 (mod r)
(`strong_cyclic.out`), so the signing is good by Lemma G and the Corollary. (For the multiset with r = 103 four
of these cube sums are ≡ 0 mod 103, so this particular test does not decide that signing.)

**How small can it be?** For a counterexample of this shape (all + bad at one prime r, each single turn bad at a
prime p_i with x ≡ 0 mod p_i) counting the elements gives Σ_i (u_i + 2) ≥ N with N ≡ 2 (mod ∏ p_i), which forces
Σ 1/p_i ≥ 1 up to a term 2·9/N: nine primes at least. Composite levels d (where the fold is 2δ_c plus cosets)
might allow smaller n; I did not exclude that. Where I looked there is none: all sets B ∋ 0 with |B| ≤ 6 in
Z_105 (`g357_6.out` and the run up to size 5), and about 30000 structured sets each in Z_1155 and Z_1575, about
20000 each in Z_3465 and Z_5005 (`struct_*.out`): all + or one turn is always good (all + alone in about 87% of
them, so about 2300 to 4100 sets per group tested one turn). A remark on lead 1 of the brief,
derived by hand and not checked by program: if d | d′ are both in D_bad and d′/d is a power of a prime s, then
2(ζ_d^c − ζ_d^{c′}) ∈ s·Z[ζ_d], which forces c_{d′} ≡ c_d modulo d itself (not only modulo its part prime to s);
so the class of d′ lies inside the class of d and adds nothing to a covering.

## 6. What is open, exactly

**Conjecture (product patterns on every box).** For every box with all sides ≥ 3 and every nonzero g : X → F
(F = Q or F_q, q odd, q dividing no side) some pattern σ makes σg good at every level; in fact at least 2^−k of
the patterns do.

By §2 and the proof of Theorem 6, the conjecture for the digit boxes (tree levels suffice) gives the statement on
signs for every odd n. Theorem P proves it when the sides grow (n_j ≥ 2j). The case that resists is many equal
small sides: for sides (3, 3, 3) the step "K = {0}" of Lemma 3 loses 2|𝓛_1|·2^−p = 1 and gives nothing. There the
count of the pairs lost is too crude (it charges two sign vectors to every pair (σ_Y, P′), whether or not the
kernel of t ↦ class of σ_Y u_t at P′ is of the form s^⊥). A sharper count of the set Lost, or a different argument when
all slices are linearly independent, is what is missing. Evidence for the conjecture: §7.

Two further observations, unproved, true in everything computed (§7):
- at least **half of all signings** of a set in a box with sides ≥ 3 are good (equality for two points on a line,
  and for a full line of four points);
- no fixed set of turned signs F ⊆ B pairs every bad signing with a good one in general (fails for the five
  points of 5.1), and the bad product patterns can span the whole space R^X (so there is no certificate that is
  linear in σ_1 ⊗ … ⊗ σ_k).

## 7. Tests (exact integer arithmetic; "good" in cyclic groups = nonzero remainder modulo Φ_d for every d | n)

**An independent reading.** After writing §1–§4 I gave the text (not my programs) to a fresh instance, to referee
it line by line and to try to break it with programs of its own. It reported no error and said it believes
Lemma 3, Theorem P and Theorem 6 as stated. Its remarks on missing links and wording are incorporated (the
injectivity in Lemma 2(c), K^⊥⊥ = K in 2(d), Lemma 3 for any coordinate, Theorem P inside the proof of
Theorem 6, the quotation of the Corollary for n = m, and that b ≠ 0 does not need p ≠ 0 in F). Its own
computations (`general/referee/`), all without a violation: the least fraction of good patterns on 3×5, 5×3,
5×5, 3×7, 7×3 (exactly 1/4) and on 3×5×7, 5×3×7 (samples) over Q and F_q for nine kinds of functions, among
them functions on a line, products, slices equal up to sign and slices of rank 2; every nonzero 0/1 function on
3×5 over Q and F_7; the inner statements of the proof of Lemma 3 on each of those functions (conditions (i) and
(ii) against "good", lost pairs inside K^⊥, at most two lost sign vectors for each (σ_Y, P′), the Claim on
about 49500 lost pairs); Lemma 2(c), (d) and the case k = 1 by enumeration; Lemma G and Theorem 6 end to end on
Z_105, Z_315, Z_525 (two ways), Z_135 with sets and multisets, about 670000 pairs (set, pattern), with long
division by Φ_d; the recursion of §4 against the definition in Theorem P′ for 3000 odd m, and the coverage list.
It also observed that in its samples the lost pairs never exceeded half of the bound 2|𝓛_1||Σ_Y| (from samples
only; if it were a theorem, the hypothesis n_j ≥ 2j would become n_j ≥ 2j − 1).

Theorem P and its proof:
- `steps_check.py`: Lemma 2(c) for all odd p ≤ 201 and odd primes q < 420, q ∤ p, and over Q; Lemma 2(d) for
  every line of F_q^p, (p, q) = (3,5), (3,7), (3,11), (5,3), (5,7), (5,11), (7,3), (7,5): the largest count is
  exactly 2^{p−1}; the case k = 1 for every nonzero f ∈ F_q^p, (p, q) = (3,5), (3,7), (3,11), (5,3), (5,7), (7,3):
  least number of good sign vectors exactly 2^{p−1}.
- `thmP_test.py` (outputs `thmP_a.out`, `thmP_b.out`, `thmP_c.out`): least fraction of good patterns over Q and
  F_q for boxes (3,5), (5,5), (3,7), (3,5,7) on random 0/1, random, sparse and structured functions (150 to 4000
  per line): never below 2^−k, equal to 1/4 in dimension 2. Also boxes outside the hypothesis: (3,3) all 19682
  functions over Q, F_5, F_7 (least 1/4), (3,3,3) samples (least 1/4 ≥ 1/8).
- `thmP_exh.py`: on 3×5, all 32767 nonzero 0/1 functions and all 221173 functions with values in {0, ±1} on at
  most 6 cells, over Q, F_7, F_11: least fraction exactly 1/4.
- `thmP_tree.py`: Theorem P′ for the tree levels of the digits (3,3), (3,3,7), (3,3,5): least fractions
  1/4, 1/2, 1/4 against bounds 1/4, 1/8, 1/16; and (3,3,5,5), where the recursion gives nothing: least 1/2.
- `prod_real.py` (outputs `prod_real_*.out`): every nonzero function with values in {−2..2} on 3 × 3 (1953124
  functions) has a good pattern, least fraction 1/4; samples on 3×4, 3×5, 4×4, 3×3×3 (also sums of two product
  functions: least fraction 1/8). `grid_prod.c`, `grid_coset.c`: for every set B ∋ 0 in 3×3, 3×5 (all sizes;
  cosets up to size 9), 3×3×3 (size ≤ 7; cosets ≤ 6), 3×3×5 (size ≤ 6) a good signing of product form exists, and
  every signing can be made good by turning whole slices.

Theorem 6 end to end (`theorem_check.py`, outputs `tc_*.out`): random and structured sets (unions of cosets,
classes, product sets, cosets of the subgroup of order q, two points in one cell, a few points changed) in Z_105
(296 sets), Z_1155 = 105·11 (196), Z_735 = 15·7² (296), Z_1575 = 175·3² (197) with all levels, and
Z_1575 = 63·5² (198), Z_2205 = 441·5 (58), Z_315 = 45·7 (294) with tree levels: for every set a pattern that is
good in the digit box modulo q was found (on average after 1.3 to 1.5 random patterns, at most 12), the signing
built from it passed the cyclotomic test, and in no pattern tried was "good in the box modulo q" followed by a
zero at a root of unity (the chain Lemma G + Corollary).

The statement on signs on boxes (`grid.c`, outputs `grid_runs.out`, `g333_9_10.out`, `g335_7.out`,
`g357_6.out`; all sets B containing the cell 0, all signings): 3×3, 3×5, 3×4, 4×4
(all sizes), 3×7 (≤ 11), 3×3×3 (≤ 10), 3×3×4 (≤ 7), 3×3×5 (≤ 7), 3×3×3×3 (≤ 5), 3×5×7 (≤ 6, 96.7 million sets):
a good signing always exists; at least half of the signings are good in every case; one turn is enough except
for 120 sets in 3×3×5 (two turns). With a side of size 2 it fails (two points).

The strong form: `oneset.py` (two sets by full enumeration with an independent program), `strong_cyclic.py`.

## 8. Roads that failed or were left (so that they are not tried again)

- **One fixed flip set.** "S bad ⇒ S with the signs on F turned is good": such an F exists for every set in 3×5
  (size 1, 2 or 4) but for none of the five-point sets of 5.1 (`grid_pair2.c`). So "half the signings are good"
  is not a pairing by translation.
- **A linear certificate.** A tensor γ with ⟨γ, σ_1⊗…⊗σ_k⟩ ≠ 0 ⇒ σg good would give the count 2^−k at once
  (a multilinear polynomial of degree k is nonzero on at least 2^−k of the cube). It exists on 3×3 and 3×3×3 in
  all samples but not on 3×5 (`cert.py`: the bad patterns span R^15 for some g).
- **Induction on the dimension with only "a good pattern exists"** as hypothesis: the step needs one pattern of
  Y that is good for two functions at once (u_s and the differences of slices), and two functions on Z_3 can have
  no common good sign vector ((1,1,0) and (1,−1,0)). The count is what makes the step work (Lemma 3).
- **Balanced signings (total unimodularity) for m = p·r^c**: the union of the two laminar families
  {whole, {x} × D} and {Z_p × D} is totally unimodular, so all block sums can be kept in {0, ±1}; for |O| odd and
  q ≥ 5 that signing is good, but |O| even and q = 3 need a case analysis I did not finish. Superseded by §3.
- **Counting with Littlewood–Offord alone**: the signings with S(ζ_d) = 0 number at most C(N, ⌊N/2⌋) for each d
  (project to a generic real line and use Erdős's antichain argument), so a good signing exists as soon as
  τ(n)·C(N, ⌊N/2⌋) < 2^N, roughly N > 0.64·τ(n)². True for every odd n but only for large multisets; not needed
  where Theorem 6 applies.
- The strong form as a route to the statement: closed by §5.

## 9. What I am least sure of, and files

Least sure, in this order:
1. **Lemma 3 and Theorems P, P′, 6 are new tonight.** They have been read once by a fresh instance (§7) and by
   nobody else. The proof is short; I rechecked each line and tested each step (Lemma 2 by enumeration, the count
   on boxes inside and outside the hypothesis, the chain to cyclic groups end to end). The places to press: the
   Claim in Lemma 3 (b ≠ 0 uses 𝓛_1 ⊆ 𝓛_0; the characteristic enters only through Lemma 2), Lemma 2(c) and (d)
   over F_q, and Lemma G (primitivity of the digit cubes). Lemma 2(a) and the case 2 ≤ dim K ≤ p − 2 of
   Lemma 2(d) are checked by reading only.
2. The coverage list (§4) is as good as `coverage.py`; the recursion for c(m) in the tree case uses that the tree
   levels without a digit of p number τ(m′).
3. Proposition S is elementary; the two large examples are verified through closed formulas (checked against
   enumeration on small boxes), not by listing 10^18 elements. The factorisations are from sympy.
4. The hand remark on nested classes at the end of §5 is not machine-checked.
5. The conjectures of §6 rest on small cases only.

Housekeeping. Three computations ran longer than the brief allows for one computation: the box 3×5×7 at size 6
(about six minutes, one process, small memory); the box 3×3×3 at sizes 9 and 10 (not timed, between two and
twelve minutes); and a search over structured sets in Z_15015, which I stopped after about eight minutes
without a result and did not repeat (its reduction matrices are large). The other runs took under two minutes
each. At most three processes of mine ran at a time, each through the 2 GB cap. Nothing outside `general/` and this file was written or changed, and nothing is
left running.

Files in `general/` (C programs compiled with `gcc -O2`; every program was run through `~/bin/cap2g.sh`):
- `grid.c` (and `grid128.c`, the same with larger arrays): all sets and all signings on a box;
  `grid_runs.out`, `g333_9_10.out`, `g335_7.out`, `g357_6.out`.
- `grid_pair.c`, `grid_pair2.c`, `grid_prod.c`, `grid_coset.c`: variants (pairing by one element / by a flip
  set, product-form signings, cosets of the pattern group); `grid_variants.out`. `rerun_grids.sh` reruns the
  box computations whose summaries are kept in `grid_runs.out` and `grid_variants.out`.
- `oneset.py`, `oneset.out`: two sets by full enumeration.
- `strong_cyclic.py`, `strong_cyclic.out`: the examples of §5.2.
- `cyc_struct.py`, `struct_*.out`: structured sets in cyclic groups, strong form.
- `prod_real.py`, `prod_real_*.out`; `cert.py`, `cert.out`: product patterns for integer functions; the linear
  certificate.
- `thmP_test.py`, `thmP_a.out`, `thmP_b.out`, `thmP_c.out`; `thmP_exh.py`, `thmP_exh.out`; `thmP_tree.py`,
  `thmP_tree.out`; `steps_check.py`, `steps_check.out`: Theorem P, Theorem P′ and Lemma 2.
- `theorem_check.py`, `tc_*.out`: Theorem 6 end to end.
- `coverage.py`, `coverage.out`: which n are covered.
- `referee/`: the programs and outputs of the independent reading (§7).
