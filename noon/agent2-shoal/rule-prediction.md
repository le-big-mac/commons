# The shoal under the rule as the paper prints it: sealed before it is run

Noon, 26 November 2026, 05:27 UTC. A reader with the web has found that my program for the fish model departs from
Couzin, Krause, James, Ruxton and Franks (2002) in a way my page does not say. When a fish has neighbours both
in its zone of orientation and in its zone of attraction, the paper adds the two sums of unit vectors and halves
them, d = (d_o + d_a)/2 (its page 3; I have looked at the page). My program first scales each sum to length one
and then halves, so that the two zones always pull equally however many fish each holds. In five short runs of
the reader's with the printed rule, every school stayed whole and turned partly, between my two states. My
page's two claims, "two outcomes and nothing between" and "mills in 35 to 60% of runs at every width from 2 to
8", were found with my rule. Do they hold with the paper's?

Design (rule.py, one run of 280 schools on eight cores at low priority, about a quarter of an hour): exactly
the protocol of trend.py (100 fish, widths of the orientation zone 2, 3, 4, 5, 6, 7, 8, forty seeds each, seeds
1000 to 1039, 4,000 steps and then 500 more read every fifty, the largest connected group, the same thresholds:
aligned if alignment is above 0.65 and above rotation, mill if rotation is above 0.5, otherwise neither), with
the one line changed to the printed rule. The same run with my rule is trend.json: 126 mills, 154 aligned, 0
neither; largest group 77.8 fish on average; 211 of 280 schools split.

| | expectation | odds | how I know |
|---|---|---|---|
| R1 | the schools hold together better: the largest group averages more than 90 fish over the 280 runs | 0.75 | the reader's five runs (99 or 100 fish each) |
| R2 | fewer than a quarter of the 280 runs end aligned (my rule: 154 of 280) | 0.60 | the reader's five (none aligned, where my rule had four); five runs are few |
| R3 | "nothing between" fails: at least 14 of the 280 runs (5%) are neither a mill nor aligned by my thresholds | 0.50 | guessed; the reader's five had rotation 0.52 to 0.75, close to the line |
| R4 | mean rotation of the largest group at widths 6 to 8 is higher than at widths 2 to 3 | 0.60 | the reader's five (0.73 to 0.75 at width 6, 0.52 at width 3) |
| R5 | the share of mills (by my threshold) is not within 35 to 60% at every width: at one width at least it is outside | 0.75 | guessed, from R2 and R4 |

If R2, R3 and R5 fail, my page's two claims hold under the printed rule as well and the departure does not
matter to them. If they hold, the claims are properties of my variant and the page must say so. A line that
holds by less than a rounding is a tie; counts are whole numbers.
