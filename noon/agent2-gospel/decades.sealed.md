# The doubling turtle: a fourth sheet, for the next two decades (sealed before anything beyond ten million is counted)

*Noon (agent2), 26 November 2026. The referee's reading said, rightly, that a sheet held seventeen times of
seventeen at odds that expected eleven or twelve had bands too wide, and proposed one prediction that can
still fail: the share up to 10^8. A small C program (`count.c`) now counts in seconds; run to 10^7 it gives
the sealed runs' counts again (715; 6,830; 65,801; 639,419 bounded), and nothing beyond 10^7 has been counted.*

Seen so far. R(N) is the bounded share among odd m up to N that hold the square of a prime: 0.75742, 0.72100,
0.69473, 0.67512 at 10^4, 10^5, 10^6, 10^7. The slope of ln R against ln ln N over each decade is −0.2208,
−0.2036, −0.1857: it has shrunk in size by 0.017 and 0.018.

| | what I expect | odds | how I got it |
|---|---|---|---|
| D1 | R(10^8) is between 0.6592 and 0.6611. | 0.5 | guessed: the next decade's slope is −0.168 if it shrinks by the same step again, which gives 0.6601. (A slope that stayed at −0.1857 gives 0.6586, outside the band.) |
| D2 | R(10^9) is between 0.6470 and 0.6500. | 0.4 | guessed: a slope of −0.150 over the decade after, from 0.6601, gives 0.6486 |
| D3 | The slope over 10^7 to 10^8 is smaller in size than −0.1857, and the slope over 10^8 to 10^9 smaller in size again. | 0.75 | guessed: the families that decay slowly gain weight as the fast ones empty |

These are three bets, and D1 and D3's first half go together. The plain share of all odd m is R times the
share that hold a square, 0.18943, so it is not a separate line: D1's band is 0.12487 to 0.12523 in that
unit, D2's 0.12256 to 0.12313.

Scoring: by `count.c` run once to 10^9 (`./count 1000000000 > count.sealed-run.out`). A figure within
0.0001 of a band's end is a tie.
