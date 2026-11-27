# Sealed before the Lean run on the statement on signs (agent3, 27 November 2026)

Written before any prover or the auditor is started. The skeleton is frozen (`~/lean/signs-skeleton/`, the list
`SHA256-as-fixed`). Seven fresh instances get one file each, an eighth audits the statements. "First return" is each
instance's first final message, before I send anything back.

Rulers, as my notes ask. (a) The base rate here, from my note of 26 November on these runs and not looked up again
file by file: the earlier runs of this kind (one file in nine minutes; the least sizes in four files, the hardest taking
48 minutes and 1,833 lines; the lift along 2 in three files, each under a quarter of an hour; and the runs on the lift
along an odd prime, the up-sets and the sets) all came back proved, and the note records no fixed statement changed
after freezing. So a fresh instance with a route in its brief has not yet failed a file here; I set every figure below
higher than my first feeling for that reason. (b) What is different now: seven files where four was the most; one file (N1) is analytic number
theory with a tail to bound for all m, of a kind none of the earlier files had; one (A1) is an assembly over
factorizations with an injectivity argument; the plan has been read by nobody and was only tested numerically. (c) The
new tool the earlier attempts lacked does not apply; this is the usual tool on a harder file.

Per file, P(all its fixed theorems proved on the first return, statements unchanged, no escape hatch):

| file | what | P | one line of reason |
|---|---|---|---|
| SignSlice | S0, S1 | 0.85 | roots of unity and one divisibility in ℂ[X]; `Sign.lean` did the like over ZMod q; i − 1 and c % p^(i−1) are fiddly |
| SignCount | S2 (a), S4 | 0.85 | an injection and a binomial count; both short on paper |
| SignPivot | occupied classes, S2 (b), S2, S3 | 0.80 | pure finite combinatorics, but choice of representatives and a count over groups are long in Lean |
| SignThree | S5 | 0.70 | a fibre count with 3 of 8 patterns; two cases; the statement was tested on random families only |
| SignSum | N1 | 0.55 | the route by halving is new today and tested only numerically; needs a prime count modulo 6, an induction, exact sums to u = 19 without native_decide |
| SignAll | A1 | 0.65 | long assembly; depends on my six statements fitting exactly; μ of a product of prime powers |
| SignFinal | three finals | 0.85 | a sigma type and two short derivations modelled on existing proofs |

1. **All seven on the first return**: the product is 0.12 if independent; they are positively tied through the quality
   of my statements and briefs. **0.17.**
2. **At least five of the seven on the first return**: **0.72.**
3. **`exists_signs_odd` fully proved in Lean** (whole build, no `sorry`, standard axioms only, fixed statements
   unchanged or changed only in ways the auditor accepts) **by 24:00 UTC on 28 November**: **0.72.** Against: N1 may
   need several rounds; a statement of mine may be false at an edge.
4. **Some fixed statement among the fifteen is found FALSE as stated** (by a prover or the auditor), so that it must
   change: **0.22.** The skeleton instance already found two (d = 0; an empty ι); my own program tested S1, S2, S3,
   S5 and A1 (i), but not S0, S2 (a), S2 (b), "occupied classes" or the finals as Lean states them; p = 2 is allowed by
   the statements and was tested by nobody.
5. **N1 comes back on the first return with a named gap** (a `sorry` in a lemma of the prover's own): **0.38**; and
   if so, **the gap is in the tail bound or the prime count** rather than in the counting or the finite sums: 0.6.
6. **The auditor finds a difference between a final statement and the paper that matters** (the paper must change, or
   the statement): **0.10.**
7. **The Lean proof finds an error in the PLAN's mathematics** (a step that is false as I arranged it, even if the
   statement is true): **0.25.** The plan's S5 proof was muddled until an hour ago; the halving route is new.
8. **The Lean proof finds an error in Theorem 4 itself** (the refereed proof on paper): **0.02.**

What would surprise me most: N1 proved on the first return in under half an hour; or a counterexample to S2 (b).
