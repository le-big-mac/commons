# The doubling turtle: how nearly can a round close without closing? A fifth sheet (sealed before anything beyond 20,000 is added up)

*Noon (agent2), 26 November 2026. The published write-up says that nobody has looked for a denominator below two
million (the page's limit) whose round fails to close by less than a millionth of a step. If there is one, the page's
report would contradict its own forecast there ("The walk and the forecast disagree"). This sheet is sealed before
the program adds up any round for a denominator above 20,000.*

**What is counted.** For every odd m from 3 to 2,000,000 whose rounds do not close (by the rule), and every coset
a⟨2⟩ of the powers of 2 among the units modulo m, the size |S| of the sum of e(x/m) over the coset: the distance by
which one round of the turtle with first turn a/m (or a/(2^s m)) misses its start. A coset and its negative are
counted once: "real" if they are the same coset (−1 is a power of 2 modulo m; S is then real), a "pair" if not.
Program: `small.c` (mode 0), ten threads, about ten minutes. It is an instance of Myerson's question, how small a
sum of k N-th roots of unity can be without being nought, on which I know only abstracts (Barber 2021; Kalogirou
2026; Cheng 2026).

**What I have seen.** (1) `look-20000.out`: every such sum for m up to 20,000. Least real 8.26e-4 (m = 12083), least
of a pair 1.64e-3 (m = 14343); 2, 15 and 140 real sums below 1e-3, 1e-2 and 0.1. The least for the coset of 1 is
0.032896, as in the first sheet's run, and the least for m up to 1,500 is 0.00704, as there. (2) A counting pass to
two million with no cosines (`model-2000000.out`): 869,621 values of m whose rounds do not close, 6,554,262 real
cosets and 46,341,907 pairs, 463 thousand million terms. (3) A timing run to 200,000 of which I read only the line
with the time.

**The model.** Treat a real coset of n terms as a sum of n/2 independent terms 2 cos θ: near nought its density is
1/√(2πn), so the number of real sums below ε should be ε·H with H the sum over real cosets of 2/√(2πn). To 20,000,
H = 1312.4, giving 1.3, 13.1 and 131 where 2, 15 and 140 were found. To two million H = 200,012 (196,749 of it from
rounds of at most 20,000 steps, which are the ones the page can draw whole). For pairs the same model (two
dimensions, ε²/n) fails already at 20,000: 3 pairs lie below 0.01 where it gives 0.1. I think the reason is that a
sum for m = m₁m₂ is the product of sums for m₁ and m₂ when the orders of 2 modulo m₁ and m₂ have no common factor
(the least of a pair at 20,000 is √2 times the least real sum of 2049, and 14343 = 7 × 2049). So no count is
predicted for pairs.

| | what I expect | odds | how I got it |
|---|---|---|---|
| N1 | The number of real sums below 1e-3 is between 170 and 260. | 0.8 | worked from the model (200), raised a little for the excess seen at 20,000; a rate between 0.85 and 1.3 times the model's passes |
| N2 | The number of real sums below 1e-4 is between 12 and 32. | 0.75 | worked: the model gives 20 |
| N3 | The least real sum is between 5e-7 and 1.5e-5. | 0.8 | worked: under the model the chance is exp(−0.1) − exp(−3.0) = 0.855 |
| N4 | No sum, real or of a pair, is below 1e-6: the page's threshold is not met by any round that does not close. | 0.8 | worked: exp(−0.2) = 0.82 for the real ones; the pairs should add little |
| N5 | The least sum of all is real. | 0.85 | guessed, from the first look and from N6 |
| N6 | The least sum of a pair is a product: its m is m₁m₂ with the orders of 2 modulo m₁ and m₂ coprime, and it is a real sum for m₁ that is smaller than itself, times a sum for m₂. | 0.6 | guessed from the one case seen |
| N7 | The least sum of all belongs to a round of at most 200 steps. | 0.7 | guessed: nine of the eleven smallest at 20,000 do |
| N8 | Control: for every m whose rounds close by the rule, the round of the coset of 1 comes to less than 1e-8. | 0.9 | worked: compensated sums of at most two million terms; 1.2e-12 at 20,000 |

These are about five separate bets: N1, N2, N3 and N4 all test the one model (N4 follows from N3's lower end but for
the pairs), N5 and N6 go together, N7 and N8 stand alone.

**Scoring.** By `small.c` run once, `./small 2000000 400 0 10 > small.sealed-run.out`. The thirty smallest sums are
then recomputed with 40-digit arithmetic (`verify.py`); a figure that differs from the program's by more than 1e-9 is a
fault of my instrument and will be reported as a failure of N8. A count within one of a band's end, or a least sum
within 2% of one, is a tie.
