# What I expect climb.py to show, written at 21:07:31 UTC on 21 November, before it was run

The referee's open point: at K = 1 the equation dr/dt = -r^3/4 only goes down, yet r first climbs from its
starting value (about 1/sqrt(N)) to about 0.1. My rough argument: the random starting phases ring on, and
their contribution to r^2 grows in proportion to t/N until it meets the falling curve r^2 = 2/t. That puts the
top of the climb at a time proportional to sqrt(N) and a height proportional to N^(-1/4).

climb.py: evenly spaced Gaussian tempos, K = 1, N = 1600, 6400, 25600, 102400 with 32, 16, 8, 2 runs; r averaged
over the runs and then over a running window of 20 time units; "height" is the largest value of that, "time" is
when it occurs.

C1. The slope of log(height) against log N over the four sizes is between -0.30 and -0.12.            odds 0.75
C2. It is between -0.30 and -0.20, as the argument says. (Marked down: the window readings already in hand,
    0.139, 0.096, 0.084 and the referee's 0.062 at 1600, 6400, 12800 and 102400, suggest about -0.17 to -0.19.)
                                                                                                    odds 0.35
C3. The slope of log(time) against log N is between 0.25 and 0.75.                                   odds 0.60
