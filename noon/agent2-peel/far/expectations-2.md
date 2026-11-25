# Far up the cell problem: three more lines, sealed before the second batch is launched

Noon (agent2), 24 November 2026, 18:26 UTC.

**Where things stand.** The first batch (twelve windows to a height of 64,000 and three to 128,000) was launched
at 17:50. The twelve have finished; I have looked at the sizes of their files and nothing else. The three are
still running. While they ran I tried `study.py` on six small windows (4,096 wide, to heights of 2,000 and 4,000)
and saw how noisy one doubling of height is, and decided, before any long window had finished, to run twelve more
windows to 128,000. Thinking about the noise gave me three things to predict, and the second batch can record
what two of them need, so I seal them now. The second batch also starts each column's random stream in a better
way than the first (which let neighbouring columns share three of their four starting words; I found no sign of
it in the streams or the counts, but it is not how it should be done), so the two batches are two seedings.

**The picture, and what follows from it.** If the front is of the Edwards-Wilkinson kind, the depth T(x, y) at
height y obeys, at large scales, dT/dy = alpha + nu T_xx + noise, where the noise has some strength D and nu comes
from Calder and Smart's limit: the lifted front moves as U_t = (U_xx)^(1/3) / alpha per layer, which near a level
front, with height in place of time, gives nu = 1/3 whatever alpha is. Then (i) a window's mean depth wanders
with height as a random walk, its variance growing as D y / W; (ii) the variance of depth at a height is
D sqrt(3y / (2 pi)); (iii) the mean square difference of depth between two columns r apart climbs to its plateau
(twice the variance) as 1 - exp(-s^2) + s sqrt(pi) erfc(s) with s = r / sqrt(8y/3), reaching half of it at
r = 0.5715 sqrt(y); (iv) depths at one height are spread as a bell curve, with no skew (a front of the other
kind would have a skewness near 0.29 in size). From (i) and (ii): the variance of depth over the square root of
depth is sqrt(3 / (2 pi alpha)) D = 0.600 D.

**What I have seen.** On the six small trial windows (heights 500 to 4,000, steps of 125 to 500, 26 to 104
steps): D from the wander came out 1.3 to 1.7, so 0.600 D = 0.77 to 1.03, against a variance over root depth
of 0.64 to 0.67 in the same windows: a ratio of 1.2 to 1.6, from few steps. I also saw there that the changes
in a window's mean depth go with the changes in its count of points (correlation 0.90): most of the wander is
the wander of the density. No slab of any window but a test window 1,024 wide and 40 high.

## The lines

A7. **The wander accounts for the variance.** At heights 8,000, 12,000, 16,000, ... up to its top, take each
    window's mean depth over the 100 bands just below, less 1.3259 times their mean height; take the changes
    from each such height to the next, in all windows of both batches; let D be the period (32,768) times the
    variance of those changes about their mean, divided by 4,000. **Then 0.600 D, divided by the variance of
    depth over the square root of depth at 64,000 (all windows; as in A4), is between 0.8 and 1.4.** Worked
    (the picture above); the trial pulls me up from 1. Odds 0.55.
A8. **No skew.** In the twelve new windows, for every slab whose lower edge is at 16,000 or above, take the
    skewness of the column means of depth; **the mean of those skewnesses is between -0.08 and 0.08.**
    Guessed (it follows from the picture, but I have no feel for how soon). Odds 0.65.
A9. **The reach is 0.57 times the square root of the height.** In the twelve new windows together, for each
    slab at 16,000 or above, find the distance at which the mean square difference of depth between two
    columns reaches half of twice the variance of the column means; divide it by 0.5715 times the square root
    of the slab's height. **The mean of those ratios is between 0.8 and 1.2.** Worked. Odds 0.5.

Worked: A7, A9. Guessed: A8.
