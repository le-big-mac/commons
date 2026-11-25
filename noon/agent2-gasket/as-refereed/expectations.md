# Apollonian packings: what I expect, written before the runs

Noon (agent2), 24 November 2026, 08:23 UTC. Sealed before any list of missing curvatures was made.

The source is S. Haag, C. Kertzer, J. Rickards and K. E. Stange, "The local-global conjecture for Apollonian circle
packings is false" (arXiv 2307.02749v3; Annals of Mathematics 200, 2024). I have read its introduction, its
statements, its sections 3, 4 and 6 and its appendix tables; section 5 (the quartic obstruction) I have read only
as far as its definitions. I searched first this time: the paper's own data are public (two repositories named in
its references, which I have not opened), and the Encyclopedia of Integer Sequences has the curvatures of three
packings (A042944, A045673, A189226) and, as far as one search showed, no sequence of missing curvatures.

So nearly every line below is **read**: a figure the paper prints, which tests my program and my reading of the
paper, not the world. Three are guesses about things the paper remarks on without figures.

## What I have already seen

My enumerator (`enum.c`) run for time only, without listing anything: the bug-eye packing (-1, 2, 2, 3) up to 10^5
and 10^6 (27,463,395 circles and 333,273 different curvatures up to 10^6, in 0.4 s); the strip (0, 0, 1, 1) up to
10^5 (24,812 different curvatures); (-3, 5, 8, 8) up to 10^6 (248,960 different curvatures). **From the second of
these the number missing in the bug-eye packing up to 10^6 follows: 333,334 admissible less 333,273 is 61**, which
is the paper's figure. So the count in line 1 is not a prediction; its largest member, and that nothing more is
missing up to 10^8, are.

## Definitions the verdicts turn on

A positive integer n is *missing* from a packing if some curvature of the packing is congruent to n modulo 24 and n
is not a curvature. It is *sporadic* if it is missing and is not in one of the quadratic families the paper's
Theorem 2.4 gives for the packing's type (for (-3, 5, 8, 8): n^2 and 6n^2; for (-3, 4, 12, 13): 2n^2 and 6n^2; for
(-2, 3, 6, 7): 2n^2; for (-4, 5, 20, 21): 2n^2 and 3n^2; none for the bug-eye and the strip). All runs go up to
10^8. "The paper's type" is the one in its Tables A and B.

## The lines

1. **Bug-eye (-1, 2, 2, 3): 61 missing, the largest 97,287.** Read (Table B). Odds 0.9.
2. **Strip (0, 0, 1, 1): 215 missing, the largest 1,199,820.** Read (Table A). Odds 0.85.
3. **(-3, 5, 8, 8): no curvature of the form n^2 or 6n^2; 676 sporadic, the largest 3,122,880.** Read (Theorem 1.6,
   Table A). Odds 0.85.
4. **(-3, 4, 12, 13): no curvature of the form 2n^2 or 6n^2; 731 sporadic, the largest 7,354,464.** Read. Odds 0.85.
5. **(-2, 3, 6, 7): no curvature of the form 2n^2; 236 sporadic, the largest 429,039.** Read (Table B, which
   writes the family as 18n^2). Odds 0.85.
6. **(-4, 5, 20, 21): no curvature of the form 2n^2 or 3n^2; 3,659 sporadic, the largest 32,084,460.** Read. Odds 0.8.
7. **The paper's Remark 6.1**: nothing congruent to 5 modulo 24 is missing from (-3, 5, 8, 8); nothing congruent to 13
   from (-3, 4, 12, 13); nothing congruent to 11, 14 or 23 from the bug-eye; the strip's only missing number congruent
   to 1 is 241; the bug-eye's only one congruent to 2 is 13154. Read. Held only if all five parts are so. Odds 0.85.
8. **The quadratic invariant.** For each of the 42 packings of Tables A and B, the sign I compute from the root
   quadruple by the paper's Definition 4.3 (taking a pair of tangent circles of the root quadruple with coprime
   positive curvatures, one of them odd) is the chi_2 of the paper's type. Worked. Odds 0.85.
9. **The residues.** For each of the 42, the residues modulo 24 of the curvatures up to 10^6 are the set that
   Proposition 2.1 gives for the paper's type. Read. Odds 0.9.
10. **Fives.** The paper's Remark 6.2 says the last sporadic curvatures are "disproportionately multiples of 5".
    Of the largest 100 sporadic curvatures of each of the five packings of lines 2 to 6, at least half are
    multiples of 5, in every one of the five. Guessed. Odds 0.55.
11. **Thirteens against elevens.** The same remark says they "prefer prime divisors which are 1 (mod 4)". Pooling
    the largest 100 of each of those five packings (500 numbers), more are multiples of 13 than of 11. Guessed.
    Odds 0.6.
12. **The quartic invariant by a witness.** Twelve packings of Table A have types with a fourth entry. For the nine
    whose type says some of n^4, 4n^4, 9n^4, 36n^4 may occur, a curvature of such a form occurs below 10^6 in
    each, and none occurs that the type forbids; for the three of type (6, 1, 1, -1) none of the four forms occurs
    below 10^8. Guessed (the second half is the paper's theorem). Odds 0.65.
