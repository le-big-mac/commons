# What I expect dip.py to show, written at 01:09:16 UTC on 22 November, before it was run

The long run left one thing unexplained: with 400 evenly spaced oscillators at K = 1 the registered recipe
(mean of r over times 300 to 600) read 0.074, but the resting level in long runs is 0.090. My guess: after its
early climb r falls along the curve 1/sqrt(t/2), which knows nothing of the resting level and carries r below
it; what holds r up at rest acts more slowly, so r dips and then comes back.

dip.py: N = 400, 200 runs of 2,400 time units, r averaged over runs and over a running window of 50.

D1. From t = 100 on, the lowest value of that running mean falls between t = 250 and t = 700, and is at least
    10% below the mean of r between 1,500 and 2,000.                                                 odds 0.75
D2. The mean of r between 1,500 and 2,000 is within 0.006 of 0.090.                                  odds 0.85
