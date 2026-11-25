# What I expect plateau.py to show, written at 19:56:56 UTC on 21 November while it was still running (plateau.out empty)

The puzzle: with evenly spaced Gaussian tempos at K = 1, the mean measured r over times 300 to 600 is 0.064 for
every size from 800 to 12,800.

My explanation, from the amplitude equation at the critical point, dr/dt = -r^3/4 (growth rate (pi/4)(K - 1) r,
stationary r^2 = pi (K - 1)): once r has been pushed up to about 0.1 it can only come down as
r = 1/sqrt(1/r0^2 + t/2), whatever the size. Averaged over 300 to 600 that is 0.063 to 0.068. So the large
populations had not finished relaxing; the plateau is the clock, not the size.

If that is right:
P1. At K = 1, for N = 1600 and 3200, the window 600-1200 reads between 0.040 and 0.055 and the window 1200-2400
    between 0.028 and 0.042 (the bare formula gives 0.047 and 0.034), unless a population has reached its own
    resting level first, which only the smaller one might.                                         odds 0.70
P2. Halving or doubling the time step leaves the 300-600 reading within 0.005 of 0.064.              odds 0.85
P3. For N = 6400 and 12800 the window 600-1200 reads within 0.006 of each other.                     odds 0.75
P4. At K = 1.005 and 1.01 (N = 3200) the 300-600 reading is within 0.02 of the many-oscillator value
    (0.125 and 0.177 by r^2 = pi (K - 1)), and at K = 0.98 it is below 0.04.                         odds 0.75
