# welch tournament results

_2026-11-18 22:34 — 20 machines, noise 0.05, continuation 0.98, exact expected payoffs (normalised per round: 3 = mutual cooperation, 1 = mutual defection)_

| rank | machine | by | states | round-robin avg | vs self | coop rate | long-run replicator share |
|---|---|---|---|---|---|---|---|
| 1 | ricochet (hill-climbed vs the house) | agent1 | 6 | 2.546 | 2.550 | 0.52 | 0.0% |
| 2 | free-pass wooer (best 4-state Nash) | evolved | 4 | 2.479 | 2.681 | 0.53 | 0.0% |
| 3 | stiffened wooer | evolved | 3 | 2.463 | 2.597 | 0.47 | 0.0% |
| 4 | handshake (D,D, then friends) | evolved | 3 | 2.423 | 2.527 | 0.38 | 0.0% |
| 5 | shifty handshake (milks the meek) | evolved | 3 | 2.413 | 2.561 | 0.38 | 0.0% |
| 6 | lazybones (three strikes, then done with | agent1 | 4 | 2.376 | 2.929 | 0.60 | 0.0% |
| 7 | anteater (climbed for self-play and non- | agent2 | 7 | 2.356 | 2.941 | 0.69 | 0.0% |
| 8 | open hand (near-equalizer: pays everyone | agent2 | 7 | 2.338 | 2.852 | 0.75 | 99.6% |
| 9 | TFT (reciprocal) | house | 2 | 2.333 | 2.383 | 0.58 | 0.0% |
| 10 | 2TFT (stiffened) | house | 3 | 2.308 | 1.490 | 0.35 | 0.0% |
| 11 | TF2T (forgiving) | house | 3 | 2.285 | 2.944 | 0.77 | 0.0% |
| 12 | suspicious TFT (shifty) | house | 2 | 2.282 | 2.078 | 0.52 | 0.0% |
| 13 | GRIM (punisher) | house | 2 | 2.276 | 1.481 | 0.18 | 0.0% |
| 14 | echo-once | evolved | 2 | 2.225 | 1.898 | 0.32 | 0.0% |
| 15 | ALLD (uncaring) | house | 1 | 2.202 | 1.147 | 0.05 | 0.0% |
| 16 | punish-once | house | 2 | 2.092 | 2.662 | 0.69 | 0.4% |
| 17 | WSLS / Pavlov | house | 2 | 2.086 | 2.749 | 0.58 | 0.0% |
| 18 | alternator | house | 2 | 1.909 | 2.057 | 0.50 | 0.0% |
| 19 | ALLC (patsy) | house | 1 | 1.882 | 2.947 | 0.95 | 0.0% |
| 20 | welcher | house | 3 | 1.773 | 2.440 | 0.82 | 0.0% |

'by' = house (textbook classics), evolved (bred by agent3's simulation), or the entrant's name.
'states' is after minimisation. The replicator column is the ecological version: strategies that
feed on patsies fade once the patsies are gone.

