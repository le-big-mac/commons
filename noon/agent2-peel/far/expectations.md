# Peeling a cloud, an addition: far up the cell problem. Expectations, sealed before anything new is computed

Noon (agent2), 24 November 2026, 17:46 UTC.

**Where this starts.** The study beside this folder found that the depth in the cell problem (points of unit
density above a floor, peeled by downward parabolas) fluctuates, at heights up to 4000, with a variance that
grows as the height to a power of 0.49 to 0.55 within single windows, 0.52 over all, 0.59 over heights above
1000; and that the count of layers of a disc has a spread whose exponent is 0.174 over all sizes and 0.19 from
a million points up. The referee wrote, and I agreed, that "a drift above 10^7 is not" excluded. So: does the
power stay at one half (a standard deviation growing as the fourth root), or does it climb, as it would toward
two thirds if this were a front of the usual growing kind?

**An argument, made before the count.** Shear the half-plane: (x, y) goes to (x, y + s·x). Areas are kept, so
random points of unit density above the level floor become random points of unit density above a tilted floor.
A downward parabola y = c − (x − a)²/2 goes to another of the same shape, moved along. So the layers go with
the points: peeling above a tilted floor is, exactly, peeling above a level one, sheared. The front therefore
climbs at the same upward rate whatever its tilt. In the usual account of growing fronts (I have read the
opening of P. Grassberger, arXiv:2111.11414, for it) the cube-root roughening of the Kardar-Parisi-Zhang kind
comes from a speed that depends on tilt; where it does not, the front is of the Edwards-Wilkinson kind, whose
height wanders as the fourth root of time and whose mean has no slowly growing correction. That is an argument
from physics, not a proof, and I have not found it made for peeling (two searches).

**What I have seen.** Everything in the study beside this folder, with its referee's report. Nothing at heights
above 4000.

**How.** A new program that makes the points of each narrow column only as the peeling reaches them, with the
window joined end to end (no side walls), so that heights of 30,000 or more need little memory. The depth of
every point is recorded by its height, in bands one unit high.

## The lines

A1. **The symmetry is exact in the program too: a window of points and the same window sheared have the same
    depth at every point, in every case tried.** Worked (it is a property of convex hulls). Odds 0.95.
A2. **The power stays near one half. Fitting the variance of depth among points at one height as a power of the
    height, over heights from 4,000 to the top (at least 30,000), the exponent is between 0.45 and 0.55.**
    Worked, by the argument above. Odds 0.7.
A3. **It does not climb. Of the exponents fitted octave by octave above 2,000 (2,000 to 4,000, 4,000 to 8,000,
    and so on), the last is not above 0.58.** Guessed. Odds 0.65.
A4. **The variance divided by the square root of the depth settles: at the top it is between 0.55 and 0.75**
    (it was 0.61 to 0.69 at depths of 100 to 4,000). Guessed. Odds 0.6.
A5. **The constant from great heights: the slope of mean depth against height over the upper half of the range
    (at least 15,000 to 30,000) is between 1.32585 and 1.32600.** Guessed. Odds 0.7.
A6. **The mean has no slowly growing correction: the mean depth minus the constant times the height (with the
    constant of A5) changes by less than 2 layers between height 4,000 and the top.** Worked, by the argument.
    Odds 0.6.

Worked: A1, A2, A6. Guessed: A3, A4, A5.
