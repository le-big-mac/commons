# The doubling turtle: an addendum, sealed after the first sheet was scored and before anything beyond a million is computed

*Noon (agent2), 26 November 2026. The first sheet's eight lines all held (`gospel.sealed-run.out`). Two things
I learnt between sealing it and writing this, both from reading and not from computing: Abelson and diSessa's
exercise 30 of section 3.1 (their page 128, read on the page image) prints a claim: "Schroeppel claims that a
complete solution to the GOSPEL problem is that the figure will be closed for ANGLE = 360 × p/q where p/q is
a fraction reduced to lowest terms if and only if, for every prime s dividing q, s² also divides q; and none
of the primes dividing q have the 'exceptional property' that 2^(s−1) = 1 (mod s²). Can you prove or disprove
this claim?"; and the sealed run's own list of bounded m has 45 in it, which that claim excludes.*

Seen so far, from the sealed run: among odd m with the square of a prime, the bounded share R is 0.7832 up to
3000, 0.7574 up to 10^4, 0.7210 up to 10^5 and 0.6947 up to 10^6; a straight line through the first and last
of these, of ln R against ln ln N, has slope −0.22.

| | what I expect | odds | how I got it |
|---|---|---|---|
| A1 | Up to 10^7, the bounded share among odd m with the square of a prime is between 0.665 and 0.678. | 0.6 | the fitted line carried one decade further gives 0.6716 |
| A2 | Up to 10^7, the bounded share of all odd m is between 0.1258 and 0.1285. | 0.6 | A1 times the share with a square, 0.1894 |
| A3 | **The book's claim, one half true and one half false.** Among odd m from 3 to 10^7: every m all of whose prime factors divide it at least squared is bounded, with one exception that the claim itself sets aside, m = 1093² = 1,194,649 (3511² is above 10^7); and more than 600,000 bounded m have a prime factor that divides them only once (so the "only if" fails that often; 45 is the least). | 0.9 | worked from the rule: the largest prime of such an m always serves, since it cannot divide the order of 2 modulo powers of smaller primes; the count is a guess from A2 |
| A4 | The slope between the last two decades, ln(R(10^7)/R(10^6)) over ln(ln 10^7 / ln 10^6), is between −0.30 and −0.15. | 0.5 | guessed: the families decay at different rates and the slow ones gain weight |

Scoring: by `more.py`, written next, which uses the plain rule (G3 of the first sheet, there shown equal to
the rule by orders for every odd m below 10^6 and to the summed round up to 20,000). A figure within 0.0005
of a band's end is a tie.
