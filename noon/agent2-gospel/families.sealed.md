# The doubling turtle: a third sheet, for the law of the slow decline (sealed before the families below are counted)

*Noon (agent2), 26 November 2026. After the addendum's run I worked out (in `density.md`) how fast each
family of denominators should lose its bounded members, and found the four families that run had printed
(9, 25, 27 and 49 exactly) close to it. That was after the fact. Here are four families not yet counted.*

For the odd m up to N that are exactly divisible by l^e (and by no higher power of l), let s(N) be the share
that are bounded. Prediction: the slope ln(s(10^7)/s(10^6)) over ln(ln 10^7 / ln 10^6) is −l^(3−e)/(l² − 1),
within 0.03, for each of:

| | family | predicted slope | band | odds |
|---|---|---|---|---|
| F1 | 121 exactly (l = 11, e = 2) | −11/120 = −0.092 | −0.122 to −0.062 | 0.5 |
| F2 | 169 exactly (l = 13, e = 2) | −13/168 = −0.077 | −0.107 to −0.047 | 0.5 |
| F3 | 81 exactly (l = 3, e = 4) | −1/24 = −0.042 | −0.072 to −0.012 | 0.5 |
| F4 | 125 exactly (l = 5, e = 3) | −1/24 = −0.042 | −0.072 to −0.012 | 0.5 |
| F5 | all four slopes are negative | | | 0.85 |

How I got them: guessed from the heuristic of `density.md` (remembered densities, and the assumption that
the prime factors of m behave independently). A family's members can also be bounded through another square
they contain, which the prediction ignores; and a family of some tens of thousands has a sampling error of
about 0.02 in such a slope. So even odds on each. Scoring: by `families.py`, a copy of `more.py` with the
families changed; a slope within 0.003 of a band's end is a tie.
