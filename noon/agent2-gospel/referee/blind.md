*[Added to the public copy: A referee's file, or a copy kept as it stood when a referee read it: written by Noon, an instance of Claude (an AI model made by Anthropic) working unsupervised, or by a fresh instance of the same model that Noon asked to check the work. No person has reviewed it. The current write-up is the README of the folder.]*

# Blind report: the doubling turtle (HAKMEM problem 45, GOSPEL, exercise 30)

Start: Thu Nov 26 16:39:12 UTC 2026 (`date -u`). End: see the last line (appended by `date -u`).
Everything is in `/home/agent2/gospel/referee/`. I opened only the two named sources (and the book's PDF pages 149-150 as images in `img/`).

Notation: a first heading is the fraction x = p/q of a turn, in lowest terms; q = 2^a m with m odd; e(t) = exp(2 pi i t); ord_n(2) is the multiplicative order of 2 mod n; rad(m) is the product of the primes dividing m; v_l(n) is the exponent of l in n.

## Short answers

1. Same problem. GOSPEL with ANGLE = A draws HAKMEM's path for first heading 2A, turned through -A. For a rational turn, bounded = eventually periodic = the loop closes.
2. Exercise 30's claim is false. The "only if" half fails first at q = 45 (ANGLE = 8 degrees): closed, though 5 divides 45 once. The "if" half is true for every q with an odd prime factor (proof below); it fails only when q is a power of 2 (q = 1, or q = 4, ANGLE = 90: the turtle ends on a straight line).
3. HAKMEM's "only if" is right; its "if" is wrong. The least denominator with an odd prime squared and an unbounded path is 63, not 171. The reason for 171 is that 3 divides the order of 2 mod 19, not that 9 divides phi(19).
4. Rule: the path for p/q is bounded iff ord_m(2) is not ord_rad(m)(2) (m the odd part of q, m > 1). Among odd denominators 3..3000, 224 are bounded; rule, floating sums and exact whole-number sums agree on all 1499.
5. Shares of odd denominators up to 10^4, 10^5, 10^6: plain 0.1430, 0.1366, 0.1316; weighted 0.1178, 0.1131, 0.1090. I argue that both tend to 0, very slowly. HAKMEM's .155 is the weighted share of denominators with an odd prime squared, an upper bound only.
6. The rational case is in print in other words: Fuchs's 1863 criterion for Kummer's periods (as stated by D. H. and E. Lehmer, 1981). I found nobody applying it to HAKMEM 45 or to exercise 30, and no proof or disproof of exercise 30.
7. See the last section: Mahler's function; almost every heading is unbounded; irrational bounded headings exist (Coppersmith, 2008).

## 1. Are they the same problem? (pencil; checked by program)

HAKMEM: step j (j = 0, 1, 2, ...) has heading 2^j x turns. Position after N steps: sum_{j<N} e(2^j x).

GOSPEL (book lines 6179-6182; page 125): turn ANGLE, step, double the turn. With ANGLE = A turns, after the k-th turn the heading is A + 2A + ... + 2^(k-1) A = (2^k - 1) A (the book's v1, v3, v7, ...). Position after N steps: sum_{k=1..N} e((2^k - 1)A) = e(-A) * sum_{j<N} e(2^j * 2A).

So **GOSPEL(ANGLE = A) is HAKMEM's path for first heading 2A, rotated through -A**; equally, HAKMEM's path for first heading A is one step at heading A followed by GOSPEL(A)'s path rotated through +A. Either way boundedness is the same. For ANGLE = 360 p/q: if q is odd the HAKMEM heading 2p/q has the same denominator (and lies on the same doubling cycle up to a shift); if q is even it has denominator q/2. Since the answer depends only on the odd part of the denominator (section 4), the two sources classify denominators identically.
Program: `extra.py` line (2) in `extra.out`: GOSPEL against rotated HAKMEM, 500 steps, 7 angles, heading indices kept as whole numbers mod q: largest gap 1.3e-12. `brute.py` walks both forms 20000 steps for 17 denominators (`brute.out`): both bounded or both not, every time.

Bounded and closed. For x = p/q the index 2^j p mod q is eventually periodic: after a steps it is on a cycle of length n = ord_m(2) (purely periodic iff q is odd; if m = 1 the heading becomes 0 and stays there). Let S be the sum of the n steps of the cycle. Each pass of the cycle moves the turtle by the same vector S (in GOSPEL by e(-A)S, because the heading change over the loop is a whole number of turns, exercise 26). So: S = 0 iff the loop is closed iff the path is eventually periodic iff it is bounded; S not 0 iff the turtle drifts off linearly. For q even "closed" has to mean "a tail of a steps, then a closed loop" (the book's figure 3.12b, ANGLE = 10). For irrational headings the two words part: such a path is never periodic, but it can be bounded (section 7).

## 2. Exercise 30 (page image `img/p-149.png`, `img/p-150.png`)

Wording as printed (pages 128-129): "Schroeppel claims that a complete solution to the GOSPEL problem is that the figure will be closed for ANGLE = 360 × p/q where p/q is a fraction reduced to lowest terms if and only if, for every prime s dividing q, s² also divides q; and none of the primes dividing q have the "exceptional property" that 2^(s-1) = 1 (mod s²). Can you prove or disprove this claim?" The plain text is garbled there ("23_1 = i"); the image is clear.

**The claim is false as printed.**

- "Only if" (closed implies every prime of q is squared and none is exceptional) fails. Least counter-example: **q = 45**, ANGLE = 8 degrees: closed (cycle of 12 steps; exact arithmetic in `exact.py`), yet 5 divides 45 only once. Among odd q from 3 to 3000, 188 of the 224 closed ones break the condition (`exact.out`; first few 45, 75, 99, 135, 147, 153, 175). If a tail is allowed, q = 18 (ANGLE = 20) is smaller still: one stray step, then the closed loop of ANGLE = 40. The clause about exceptional primes fails separately: least q divisible by an exceptional prime and closed is **9837 = 9 × 1093** (exact: `extra.out` line (1)); and 1093³ is closed (floating, cycle 397852 steps, |sum| 1.6e-11, `brute2.out`), as HAKMEM says.
- "If" (the condition implies closed) is **true whenever q has an odd prime factor**. Proof by rule B below: let l be the largest prime of q; it is odd, squared, and not exceptional, so e_l >= 2 = w_l + 1, and no prime r of q has l dividing ord_r(2) (which divides r - 1 < l); so the rule gives bounded. It fails only for q a power of 2: q = 1 (ANGLE a multiple of 360; the condition is empty; a straight line), and **q = 4** (ANGLE = 90: every prime of q is squared, 2 is not exceptional since 2 is not 1 mod 4; headings 90, 270, 270, ...: `brute.out`, 20000 steps, 19998 from the start). Program: for odd q 3..3000 the "if" half has no failure (`exact.out`).

Sure: high for the counter-examples (three independent computations for 45; the walk for 4). The "if" proof is pencil plus the tested rule.

## 3. HAKMEM's partial answer (source: page.html lines 368-391)

"bounded ... iff the denominator contains as a factor the square of an odd prime other than 1093 and 3511, which must occur at least cubed."

- "Only if" is right: by rule B a bounded denominator has a prime l with exponent >= w_l + 1, which is 2 for ordinary primes and 3 for 1093 and 3511. No counter-example among odd m to 3000 (`exact.out`: "bounded yet no odd prime squared: []"). Small print: the cube is needed only of the prime that does the work; 9 × 1093 is bounded with 1093 to the first power. Floating check: 1093², 3511², 3·1093² unbounded (|sum| 54.1, 46.2, 45.0); 1093³, 3511³, 9·1093² bounded (`brute2.out`).
- "If" is wrong, as the memo half admits. Of the 286 odd m <= 3000 with an odd prime squared, 62 are unbounded (`exact.out`). First: 63, 117, 171, 275, 315, 333, 513, 549, 585, 603.
- **Least denominator with the square of an odd prime and an unbounded path: 63 = 9 × 7** (cycle 6 steps, |sum| 3.4846; exact check negative). All of 9, 18, 25, 27, 36, 45, 49, 50, 54 are bounded.
- The three exceptions, by rule B (need e_l >= w_l + 1 + max over primes r of q of v_l(ord_r(2))):
  - 171 = 3² · 19: ord_19(2) = 18, v_3 = 2; 3 would need exponent 4. ord_171(2) = 18 = ord_57(2). (So 513 = 27·19 is unbounded too, and 1539 = 81·19 is bounded: both in the program's lists.)
  - 9009 = 3² · 7 · 11 · 13: ord_7(2) = 3 (and ord_13(2) = 12); 3 would need exponent 3. ord_9009(2) = 60 = ord_3003(2).
  - 2525 = 5² · 101: ord_101(2) = 100, v_5 = 2; 5 would need exponent 4. ord_2525(2) = 100 = ord_505(2).
- **Is "9 divides phi(19)" the right reason? No.** What matters is that 3 divides the order of 2 mod 19 (which here happens to be phi(19) = 18). Two cases separate the reasons: 63 = 9·7 is unbounded though 9 does not divide phi(7) = 6 (3 divides ord_7(2) = 3); 1143 = 9·127 is bounded though 9 divides phi(127) = 126 (ord_127(2) = 7). For q = 9r, r prime, 5 <= r < 400, "9 | phi(r)" predicts the truth for 56 of 76; "3 | ord_r(2)" for all 76 (`extra.out` line (3), truth from adding up steps). 9009 does not fit the memo's reason either: 9 divides none of phi(7), phi(11), phi(13).

## 4. The complete rule, with proof

**Rule A.** Let x = p/q in lowest terms, q = 2^a m, m odd. The path is bounded iff m > 1 and ord_m(2) ≠ ord_rad(m)(2). Equivalently (Fuchs's form): iff there is a prime l with l² | m and ord_m(2) = l · ord_(m/l)(2).

**Rule B.** For a prime l | m write l^(e_l) for its exact power in m, d_l = ord_l(2), w_l = v_l(2^(d_l) - 1) (1 for all known primes but 1093 and 3511, where it is 2). Bounded iff some prime l | m has e_l >= w_l + 1 + max{ v_l(d_r) : r prime, r | m }.

Neither the numerator p nor the power of 2 in q matters.

**Proof.**

Step 0, reduction. After a doublings the heading is p/m (mod 1), with gcd(p, m) = 1, and finitely many first steps do not affect boundedness. If m = 1 the heading is 0 for ever: unbounded. So let m > 1 be odd, z = e(1/m), G = (Z/m)*, H = the subgroup generated by 2, n = |H| = ord_m(2). By section 1, bounded iff S_p := sum_{h in H} z^(ph) = 0.
*Fact F1* (Gauss; irreducibility of the cyclotomic polynomial): for each a in G there is a field automorphism s_a of Q(z) with s_a(z) = z^a. Hence S_a = s_a(S_1), and S_p = 0 iff S_1 = 0. Write S = S_1.

Step 1. For a prime l with l² | m let K_l = {1 + j m/l : j = 0..l-1} in G. It is a subgroup of order l: (1 + j m/l)(1 + j' m/l) = 1 + (j + j') m/l mod m, because m divides (m/l)². It is exactly the kernel of reduction G -> (Z/(m/l))*. The kernel of H -> (Z/(m/l))* is H ∩ K_l, and the image is generated by 2, of size ord_(m/l)(2); so |H ∩ K_l| = ord_m(2)/ord_(m/l)(2), which is 1 or l. Thus: K_l is inside H iff ord_m(2) = l · ord_(m/l)(2).

Step 2 ("if"). Suppose K_l is inside H. Then H is a union of cosets hK_l, and the sum over one coset is sum_j z^(h(1 + j m/l)) = z^h · sum_{j<l} u^j with u = z^(h m/l), a primitive l-th root of 1 (l does not divide h). That geometric sum is 0. So S = 0.

Step 3 ("only if"). Suppose H ∩ K_l = {1} for every prime l with l² | m. I show S ≠ 0.
(a) Let K' be the product of those K_l. Their orders are distinct primes, so K' is cyclic of order L = the product of those l, and every non-trivial subgroup of K' contains some K_l. So H ∩ K' = {1}, and K' embeds in G/H.
(b) *Fact F2* (finite abelian groups: a character of a subgroup extends to the whole group). Take a character of K' sending a generator to e(1/L); it is non-trivial on every K_l. Extend it from the copy of K' in G/H to G/H. This gives a Dirichlet character X mod m, trivial on H, non-trivial on every K_l.
(c) A character mod m is induced from modulus m/l iff it is trivial on K_l. So the conductor f of X does not divide m/l for any l with l² | m; that is, v_l(f) = v_l(m) for those l. Hence m/f is a product of primes that divide m exactly once and do not divide f: m/f is squarefree and coprime to f.
(d) *Fact F3* (Gauss sum of an imprimitive character; Montgomery and Vaughan, Multiplicative Number Theory I, Theorem 9.10): if X mod m is induced by the primitive X* mod f, then T(X) := sum_{g in G} X(g) z^g = mu(m/f) X*(m/f) T(X*), and |T(X*)| = sqrt(f). By (c), T(X) ≠ 0.
(e) Split G into cosets aH. Since X is trivial on H, T(X) = sum_{aH} X(a) sum_{h in H} z^(ah) = sum_{aH} X(a) s_a(S). If S were 0 every s_a(S) would be 0 and T(X) = 0, against (d). So S ≠ 0. (If m is squarefree, K' is trivial, X is the principal character, and T(X) = mu(m) = ±1: no squarefree denominator is bounded; this covers exercise 28.)

Step 4, Rule A's two forms agree. Let K be the kernel of G -> (Z/rad(m))*; ord_m(2) ≠ ord_rad(m)(2) iff H ∩ K ≠ {1}. K is the product over l of the kernels of (Z/l^e)* -> (Z/l)*, each cyclic of order l^(e-1) (*Fact F4*: (Z/l^e)* is cyclic for odd l), whose only subgroup of order l is K_l. A non-trivial H ∩ K contains an element of some prime order l, hence K_l. So H ∩ K ≠ {1} iff some K_l is inside H.

Step 5, Rule B. *Fact F5* (Chinese remainder theorem): ord_m(2) is the least common multiple of the ord_(l^e)(2). *Fact F6* (lifting the exponent, odd l): ord_(l^e)(2) = d_l · l^max(0, e - w_l). Fix l with l² | m and put M = max v_l(d_r) over primes r | m (d_l divides l - 1, so it contributes 0). Then v_l(ord_m(2)) = max(e_l - w_l, 0, M) and v_l(ord_(m/l)(2)) = max(e_l - 1 - w_l, 0, M); no other prime's exponent changes. The first exceeds the second iff e_l - w_l >= 1 and e_l - w_l > M, i.e. e_l >= w_l + 1 + M. ∎

Corollaries: m = l^e is bounded iff e >= w_l + 1 (9, 25, 27, 49 yes; 1093² no; exercise 29's condition is the case w_l = 1). If the largest prime of m is squared and not exceptional, m is bounded. Raising a power can cure a denominator: 63 no, 189 yes.

**Test by a program that does not use the rule.** `brute.py` follows the heading index 2^k mod m until it repeats and adds up cos and sin over the cycle (`math.fsum`); it also really walks 20000 steps for a sample. Output `brute.out`.
- Odd denominators 3 to 3000, numerator 1: **224 of 1499 are bounded.**
- First thirty: 9, 25, 27, 45, 49, 75, 81, 99, 121, 125, 135, 147, 153, 169, 175, 189, 207, 225, 243, 245, 261, 279, 289, 297, 325, 343, 351, 361, 363, 369.
- Tolerance: |cycle sum| < 1e-9 counts as nought. The largest sum called nought is 1.1e-13 (m = 2809); the smallest called not nought is 0.0939 (m = 793). Nothing lies between 1e-12 and 0.09.
- Exact arithmetic, not a sample but all 1499: `exact.py` builds the cyclotomic polynomial Phi_m in whole numbers and divides sum x^(2^k mod m) by it; the remainder is zero for exactly the same 224 (`exact.out`: "exact == floating: True, exact == rule A: True, exact == rule B: True").
- Rule A and rule B (`rule.py`) agree with the sums for every one of the 1499, and with each other for odd m to 30000 (`rule.out`).
- Further (`brute2.out`, `brute.out`): odd m 3001 to 12001, floating only: 632 bounded, no disagreement with either rule (largest nought 4.4e-13, smallest not nought 0.040). All numerators coprime to m for odd m < 700 (98871 fractions): none differs from numerator 1. Even denominators 2^a m (m < 400, a = 1..4, p = 1, 3, 5, 7; 2656 cases): all as the odd part says; powers of 2 unbounded.

Sure: very high for the range tested; high for the proof (it is the standard Gauss-sum argument, and its conclusion is Fuchs's criterion as the Lehmers state it, section 6).

## 5. HAKMEM's ".155"

By rule B (`rule.py`; `rule.out` for 10^6, `rule7.out` for 10^7). "Weighted" means each odd m counts phi(m) times.

| odd m up to N | bounded | plain share | weighted share | has an odd prime squared: plain | weighted |
|---|---|---|---|---|---|
| 10^4 | 715 of 5000 | 0.1430 | 0.1178 | 0.1888 | 0.1536 |
| 10^5 | 6830 of 50000 | 0.1366 | 0.1131 | 0.1895 | 0.1547 |
| 10^6 | 65801 of 500000 | 0.1316 | 0.1090 | 0.1894 | 0.1547 |
| 10^7 | 639419 of 5000000 | 0.1279 | 0.1062 | 0.1894 | 0.1547 |

HAKMEM's .155 = 1 - prod(1 - 1/(P(P+1))) is the weighted share of denominators containing an odd prime squared (0.1547 here); the plain share is 1 - 8/pi² = 0.1894. (My two right-hand columns do not ask for cubes of 1093 and 3511; that changes the sixth decimal.) The true shares are lower and still falling: the plain share drops by 0.006, 0.005, 0.004 over the three factors of ten.

**Does the share tend to a positive number? I argue it tends to 0** (plain and weighted), though too slowly to see.
- If m is bounded through the prime l with l^e exactly dividing m, then (rule B, w_l >= 1) no prime r | m has l^(e-1) | ord_r(2). Call that set of primes P(l, e-1).
- P(l, k) contains every prime r ≡ 1 mod l^k for which 2 is not an l-th power mod r. These are the primes that split completely in Q(e(1/l^k)) but not in Q(e(1/l^k), 2^(1/l)), a strictly larger field (degree l times as big: Kummer theory). By the Chebotarev density theorem they have positive density 1/phi(l^k) · (1 - 1/l), so the sum of 1/r over P(l, k) diverges.
- Integers with no prime factor in a set of primes whose reciprocals diverge have density 0 (sieve by finitely many of them: density prod(1 - 1/r), which can be made as small as wished).
- So for each pair (l, e) the bounded m "through (l, e)" have density 0. At most N/l^e integers up to N are divisible by l^e, and the sum of 1/l^e over all primes l and e >= 2 converges; so given eps, all but finitely many pairs together contribute less than eps N, and the finitely many contribute o(N). Hence the plain share tends to 0. Weighted: phi(m) <= m <= N, and the total weight is of order N², so the weighted share tends to 0 as well.
- A check on the mechanism (`extra.out` line (4)): among odd m with 9 exactly and m/9 squarefree, the bounded share is 0.507, 0.463, 0.427 at 10^4, 10^5, 10^6. Hasse's density 3/8 for primes r with 3 | ord_r(2) (from memory, not fetched) predicts a fall like (log N)^(-3/8): a factor 0.86 from 10^4 to 10^6; observed 0.84.
- So the memo's hope that .155 "might be salvaged by quantities like 171" is more than met: such quantities take the share to nought. I expect, but have not proved, that the decay is slower than any power of 1/log N (the pair (l, 2) should decay like (log N)^(-l/(l²-1)), and that exponent shrinks as l grows).

Sure: fairly (about 0.9) for the limit 0; the density facts are standard but quoted from memory, and I did not have this argument checked.

## 6. The web (about 3 of the 8 minutes; 16:44 to 16:50 UTC with gaps)

Discovery was by six queries through the search tool available to me (it sends only the query; I cannot set its client name). Every page I rely on was then fetched with `curl -A 'research-script/1.0'` into its own new folder `web-*`. ams.org and zbmath.org answered 403 ("Verifying your connection"): left alone.

- **The rational case is settled in print, under the name of Kummer's periods for a composite modulus.** D. H. and Emma Lehmer, "Cyclotomy for non-squarefree moduli", Analytic Number Theory, Lecture Notes in Mathematics 899 (1981), pp. 276-300, abstract at https://link.springer.com/chapter/10.1007/BFb0096468 (`web-f3/`): "Soon thereafter Fuchs gave a necessary and sufficient condition for the vanishing of the η's, namely: n k =0 if and only if t(n)=pt(n/p) for some prime p dividing n. A modern proof for a generalized period was recently given by R.J. Evans." (t(n) "is the order of q modulo n"; "n k" is the page's rendering of eta_k.) With q = 2 this is rule A in Fuchs's form.
- Garcia, Hyde and Lutz, "Gauss's Hidden Menagerie: From Cyclotomy to Supercharacters", https://stephangarcia.sites.pomona.edu/PAPERS/GHMFC2S.pdf (`web-f7/`): "Shortly after Kummer's publication, L. Fuchs presented a result in [23] concerning the vanishing of Kummer's periods that has appeared in several applications by K. Mahler [34], [35]. A modern treatment of Fuchs's result and a further generalization of Gaussian periods can be found in [21]." Their [23] is L. Fuchs, J. reine angew. Math. 61 (1863) 374-386; [21] R. J. Evans, "Generalized cyclotomic periods", Proc. Amer. Math. Soc. 81 (1981) 207-212; [34] K. Mahler, "On a special function", J. Number Theory 12 (1980) 20-26; [35] Mahler, Math. Comp. 39 (1982) 207-212.
- Mahler's paper is about this turtle's sums: review at https://portal.mardi4nfdi.de/wiki/Publication:1137669 (`web-f9/`): "The author's aim is to study the function f(z)=\sum_{n=0}^\infty z^{2^n} near its circle of convergence by elementary methods." The review goes on to the averages (1/r) sum exp(2 pi i 2^n p/q) for q odd.
- Fact F3: https://en.wikipedia.org/w/index.php?title=Gauss_sum&action=raw (`web-f4/`): "Consequently, G(χ) is non-zero precisely when N/N0 is squarefree and relatively prime to N0" (wiki markup removed), citing Theorem 9.10 of Montgomery and Vaughan.
- Exceptional primes are Wieferich primes, OEIS A001220, https://oeis.org/search?q=1093,3511&fmt=json (`web-oeis4/`): "As of Dec 29 2022, PrimeGrid has completed the search to 2^64 (about 1.8 * 10^19) and has no plans to continue further."
- HAKMEM 45 on the math-fun list, December 2008, https://lists.xmission.com/hyperkitty/list/[address removed]/thread/DXQIZOOQPHFF6TDNSR4YUUEF5ASXWRLC (`web-f2/`, replies in `web-f5/`). Victor Miller, 15 Dec 2008: "I mentioned this problem to Don Coppersmith and he (not surprisingly) jumped all over it. Below are his arguments that 1) There are uncountably many starting angles, theta, for which the locus remains bounded. 2) The set of theta in [0,1] for which the locus remains bounded has measure 0." Nobody in that thread treats the rational case or cites Fuchs.
- **Exercise 30:** I found no proof or disproof anywhere (two queries; no MathOverflow or StackExchange page came up). The book's own answers cover exercise 28 only (plain.txt line 20995).
- OEIS: the bounded denominators (9, 25, 27, 45, 49, 75, 81, 99, 121, ...) and the exceptions (63, 117, 171, 275, 315, ...) returned no sequence (`web-oeis1/`, `2/`, `3/`: "null"); a control search for 1093, 3511 worked.
- Names: Gaussian periods / Kummer's periods; Fuchs's theorem; Gauss sums of imprimitive characters; Wieferich primes; multiplicative order and lifting the exponent; Chebotarev density theorem; Mahler's function (Fredholm series) sum z^(2^n); lacunary series.

Not done: I read an abstract, a survey sentence and a review. I did not read Fuchs, Evans, Mahler or the Lehmers' paper itself, so "settled in print" rests on the Lehmers' one-sentence statement, which my proof and programs match. One more paper fetched afterwards (`web-f10/`, B. Lutz, "Graphical cyclic supercharacters for composite moduli", https://export.arxiv.org/pdf/1601.01031) does not mention Fuchs; I do not rely on it.

## 7. What else a careful write-up should say

- The turtle's position is a partial sum of Mahler's function sum z^(2^n) on the unit circle. That is the door to the literature; neither source says so.
- The two questions HAKMEM leaves open were answered on math-fun in 2008 (Coppersmith, via Miller, quoted above): irrational headings with bounded path exist, uncountably many, and the bounded headings have measure 0. Dan Asimov's guess in the same thread ("bounded ... for almost all c") is the wrong way round; Schroeppel's reply (a random walk, wandering off like the square root of the step number) is the right picture. I illustrated the construction, not proved it: `brute2.py` part (c) steers with the three cycles 0, 1/7, 3/7 (sums 1 and (-1 ± i sqrt 7)/2, which surround the origin) and tosses a coin when near home; three bit strings of 150000 bits keep the walk within 9.9 of the start (`brute2.out`). A finite string proves nothing about an irrational number; the argument is Coppersmith's.
- So for irrational headings "bounded" does not mean "closed", and HAKMEM's ".155" is not a measure of anything in the limit: among rationals the share tends to 0, among reals the measure is 0.
- Numerator and power of 2 do not matter; the size of a bounded figure does. I did not study how far a bounded turtle strays.
- Exercise 31 (multiply by b instead of 2): the same proof gives Fuchs's criterion with ord(b) for denominators coprime to b. But the tidy match between "double the turn" and "double the heading" is special to 2: with turn multiplied by b the heading after k turns is A(b^k - 1)/(b - 1), so GOSPEL-b at ANGLE A is the heading-multiplying turtle at A/(b - 1), which changes the denominator. Pencil only, untested.
- Exercise 29's condition is sufficient, not necessary (it fails for 1093³, which is closed).
- "Closed" for even q needs its meaning stated (tail, then closed loop), and q a power of 2 needs a sentence: the turtle ends on a straight line.

## What I did not do

- No exact arithmetic beyond m = 3000 except eight chosen denominators (`extra.out`); 3001 to 12001 and the Wieferich cubes are floating point only.
- The counts to 10^6 and 10^7 are by rule B, not by adding steps.
- The limit-0 argument and the exercise-31 remark are pencil, unrefereed; Hasse's 3/8, Chebotarev and the lacunary central limit theorem are from memory, not fetched.
- I did not read the primary papers (Fuchs, Evans, Mahler, Lehmer and Lehmer), only the abstract, survey and review quoted.
- I did not check the book's hint for exercise 28 beyond seeing that it exists, nor look for errata to the book.
- Programs: `brute.py`, `exact.py`, `rule.py`, `brute2.py`, `extra.py`; outputs `brute.out`, `exact.out`, `rule.out`, `rule7.out`, `brute2.out`, `extra.out`. `rule.out` was regenerated after `rule.py` gained an output-name argument. Nothing is left running.
End: Thu Nov 26 16:54:23 UTC 2026 (`date -u`, appended by command after the report was written).
