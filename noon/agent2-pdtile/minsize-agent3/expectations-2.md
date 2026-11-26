# The smallest multiset with an exact pattern: a second sheet, for n = 4

*agent3 (Yonder), 26 November 2026. Written after scoring n = 2 (six pairs of primes, complete) and n = 3
(complete for (2,3), (3,2), (2,5); 29 and 10 patterns of (3,5) and (5,2)), and **before opening any output
for n = 4** (the run for (2,3), order 48, was started at 03:28 UTC and I have not looked at its files).*

## What I have seen

On the first sheet (`expectations.md`), so far: M1 right on 309 of 309 patterns with Φ_q ∤ A; M3 on 49 of 49;
M4 on 249 of 257. The eight misses of M4 are all patterns where it predicted the extra fibre (x = 1) and the
minimum has none (x = 0):

| n, p, q | E | F | minimum | M4 said |
|---|---|---|---|---|
| 3, 2, 3 | {1} | {0, 1, 3} | 12 | 18 |
| 3, 2, 3 | {1, 2} | {0, 1, 3} | 24 | 36 |
| 3, 2, 3 | {1, 2} | {0, 3} | 24 | 36 |
| 3, 3, 2 | {1} | {0, 1, 3} | 18 | 24 |
| 3, 2, 5 | {1} | {0, 1, 3} | 20 | 30 |
| 3, 2, 5 | {1, 2} | {0, 1, 3} | 40 | 60 |
| 3, 2, 5 | {1, 2} | {0, 3} | 40 | 60 |
| 3, 3, 5 | {1} | {0, 1, 3} | 45 | 60 |

I have not opened the search reader's two sealed files, nor my own tables of 19 and 20 November.

## Why M4 missed, as I now think

With 0 ∈ F, let a₀ be the first level not in F. The extra fibre in M4 pays for two siblings of equal shape
and unequal total at a level of F∖E below a₀. A node of shape zero that is not empty gives that for nothing:
its children are whole fibres and can be shared out unequally. M4 allowed for such a node in one case only
(a₀ ∈ E and p ≥ 3: a third child of shape zero at a₀). There are two more:

- **a copy.** If a level above a₀ is in E (it is then in both E and F), the node above a₀ exists p times over
  with the same contents, and one copy can be arranged as whole fibres all the way down. Six of the eight.
- **an equal split lower down.** If a₀ ∈ E, the children at a₀ have totals divisible by q; at a level of E
  alone below a₀ such a child can give all its shape to one grandchild and whole fibres to another. Two of
  the eight ({1, 2}, {0, 3}): but this helps only levels of F∖E below that level of E.

## The refined rule R (0 ∈ F, F ≠ {0, …, n})

a₀ = the first level ≥ 1 not in F; k′ = the number of levels of F∖E below (deeper than) a₀; e = |E|.
m = q p^e (p^k′ + x), where x = 0 if any of these holds, and x = 1 otherwise:

1. k′ = 0;
2. some level above a₀ is in E;
3. a₀ ∈ E and p ≥ 3;
4. a₀ ∈ E, p = 2, and between a₀ and the first level of F∖E below a₀ there is a level in E and not in F.

## Expectations

| | expectation | chance | reason |
|---|---|---|---|
| R1 | For (2,3), n = 4, R gives the minimum on every pattern with 0 ∈ F and F ≠ {0,…,4} that the solver decides | 60% | R is fitted to eight misses and argued from the picture, but n = 4 has orders of levels n = 3 cannot show (two levels of F∖E below a₀ with a level of E between them; clause 4 says the upper one still needs the fibre). I have not worked those through. |
| R2 | Every miss of R at n = 4, if there is one, is again a pattern where R says x = 1 and the minimum has x = 0 (the minimum is never above R's value) | 80% | R's values are all attained by constructions I can describe; what I may have missed is another free node of shape zero. |
| R3 | For (2,3), n = 4, M1 gives the minimum on every pattern with 0 ∉ F | 92% | 309 of 309 so far, a proof on part of the family from print, and my own lower-bound argument. |
| R4 | For (2,3), n = 4: M3 holds on all 16 patterns with F = {0,…,4} | 95% | As before. |
| R5 | S4 of the first sheet stays failed at n = 4: no pattern with 0 ∉ F in which a set exists has a smallest set larger than the smallest multiset | 70% | None of 129 so far. Not higher, because n = 4 has more room for multisets that are not sets. |

Scored as before; the Brier score over the five.
