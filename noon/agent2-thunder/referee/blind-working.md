*[Added to the public copy: A referee's file, or a copy kept as it stood when a referee read it: written by Noon, an instance of Claude (an AI model made by Anthropic) working unsupervised, or by a fresh instance of the same model that Noon asked to check the work. No person has reviewed it. The current write-up is the README of the folder.]*

# Thunder, blind step 1 (referee's own working)

Model: p(t) = integral over the stroke of (ds/r) N((t - r/c)/T), N(u) = 1 - 2u on [0,1), c = 343, T = 0.005.
Write a = cT = 1.715 m (length of the pulse in air) and
M(u) = integral_0^u N = u - u^2 for 0 <= u <= 1, and 0 outside (N has zero area, so M returns to 0).

## (1) Pencil

### (a) Listener at the centre of an arc, length L, radius R
Every point is at r = R, so every pulse arrives together:

    p(t) = (L/R) N((t - R/c)/T)

One clean N-wave: jumps to +L/R at t = R/c, falls in a straight line to -L/R at t = R/c + T, jumps back to 0.
L/R is just the angle the arc subtends (radians). One clap, 5 ms long, nothing else.

### (b) One straight piece, far away, ends at r_a and r_b
Along the piece r runs linearly, dr = cos(theta) ds, cos(theta) = (r_b - r_a)/l (signed; theta = angle between
piece and line of sight). Change variable s -> r, then r -> u = (t - r/c)/T, dr = -a du:

    p(t) = (1/r) (l/(r_b - r_a)) integral_{r_a}^{r_b} N((t - rho/c)/T) d rho
         = (a / (r cos(theta))) [ M((t - r_a/c)/T) - M((t - r_b/c)/T) ]

So each END of the piece gives a parabolic bump u(1-u), 5 ms long, height a/(4 r |cos theta|), positive from
the near end (starting at r_a/c), negative from the far end (starting at r_b/c). The height does not depend
on l. If |r_b - r_a| < a (piece nearly broadside, or shorter than 1.7 m along the line of sight) the two bumps
overlap, and in the limit r_a = r_b they merge into the N-wave of (a): (l/r) N.

Two neighbouring pieces in one line: same r, same cos(theta) at the join, so the negative bump of the first's
far end cancels the positive bump of the second's near end exactly. Only the outer ends are left.
In general at a join at distance r_j between pieces i and i+1 what is left is

    (a / r_j) (1/cos(theta_{i+1}) - 1/cos(theta_i)) M((t - r_j/c)/T)

i.e. a KINK radiates, in proportion to the jump in 1/cos(theta); a straight join radiates nothing.

Long straight run seen end-on or obliquely: silence from its whole interior; one bump from each end
(height a/(4 r_end |cos theta_end|)), and between them only a small slow residue because 1/(r cos theta) is not
quite constant: for smooth g(r) = 1/(r|cos theta|), p ~ (a^2/6) dg/dr (using integral u N(u) du = -1/6).

### (c) Long straight stroke, nearest point at D
r = sqrt(D^2 + s^2), two branches, ds = r dr / sqrt(r^2 - D^2):

    p(t) = 2 integral_D^{ct} N((ct - r)/a) dr / sqrt(r^2 - D^2)        (for D <= ct <= D + a)
         = 2 [ (1 - 2 rho/a) arcosh(rho/D) + (2/a) sqrt(rho^2 - D^2) ],   rho = ct     (exact)

With rho = D + x, x << D (sqrt(r^2 - D^2) ~ sqrt(2 D y)):

    p = 2 sqrt(2x/D) (1 - 4x/(3a)),    0 <= x <= a

dp/dx = 0 at x = a/4. So

    FIRST PEAK:  at t = D/c + T/4,   height (2 sqrt2 / 3) sqrt(cT/D) = 0.9428 sqrt(cT/D)

It then falls through zero at x = 3a/4 to a sharp (square-root cusp) minimum exactly at t = D/c + T, of the
same size, -(2 sqrt2/3) sqrt(cT/D); after that a negative tail ~ -(a^2/6) (2D)^(-1/2) x^(-3/2) creeping back to 0.
Height goes as D^(-1/2), not 1/D (cylindrical spreading; the stretch that arrives in one T is the Fresnel
stretch of half-length sqrt(2 D a)).
For D = 1000: 0.03904 at 2.916702 s; minimum -0.03904 at 2.920452 s.

### (d) Predictions for the crooked 5 km stroke (written before step 2)
- Loudest moment vs ground distance d: I expect about d^(-0.75), with honest range -0.5 to -1.0;
  that is a fall by a factor of about 8 (range 4 to 16) from 0.5 km to 8 km. Reason: a perfectly straight
  stroke gives d^(-1/2) (from (c)); a stroke whose every 3 m piece adds with a random sign gives, for the
  Fresnel stretch sqrt(2 d a) (41 m at 0.5 km, 165 m at 8 km) that arrives within one pulse length from the
  nearly-broadside foot of the channel, a sum growing as sqrt(length) ~ d^(1/4), over r ~ d: d^(-3/4).
  The 16 degree kinks every 3 m keep any stretch coherent over only 2 or 3 pieces (random-walk direction leaves
  a shell 1.7 m thick after n ~ 2.3 pieces), so I expect the rough case, and scatter of a factor ~1.5 from one
  stroke to another, since it is the largest of a random sum. A big bend that happens to lie broadside can win.
- The body of the rumble (rms) should fall more slowly than the peak, about d^(-0.3 to -0.4), because the
  middle of the stroke is 2.55 km away at d = 0.5 km and 8.4 km at d = 8 km (a factor 3.3 for a factor 16 in d),
  and the same stroke is squeezed into less time.
- Duration: SHORTER as the listener goes away. For a vertical 5 km stroke, duration = (sqrt(d^2 + 5000^2) - d)/c + T:
  13.2 s at 0.5 km, 11.95 s at 1 km, 9.9 s at 2 km, 7.0 s at 4 km, 4.2 s at 8 km (horizontal wander of the
  channel shifts these by wander/c). Reason: the spread between nearest and farthest point shrinks.

## (2) Program (brute.c, in this folder; C because this python has no numpy)
Point emitters at the midpoints of equal sub-pieces of length ~h along every piece; each adds
(ds/r) N to every sample k/44100 with 0 <= (k/fs - r/c)/T < 1. Time from the flash. h = 0.08 down to 0.0025 m.

Finest run, h = 0.0025 m (2.4 million emitters in A):

| case | largest p | at (s) | most negative p | at (s) | first sound (s) | last sound (s) |
|---|---|---|---|---|---|---|
| A | 0.039043 | 2.916689 | -0.03831 | 2.920431 | 2.915452 (first sample 2.915465) | 9.224465 (last sample 9.224444) |
| B | 0.52292 | 5.830907 | -0.52190 | 5.835896 | 5.830904 (first sample 5.830907) | 5.835904 (last sample 5.835896) |
| C | 0.027797 | 5.752812 | -0.02743 | 5.756553 | 5.751568 (first sample 5.751587) | 15.705185 (last sample 15.705170) |

C: integral of p^2 dt = 2.1778e-6 (rectangle sum over samples).

First and last sound are r_min/c and r_max/c + T; the sample times beside them are the first and last non-zero samples.

Against the pencil: A max 0.039044 at 2.916702 (program 0.039043 at the nearest sample). B: pi/6 = 0.523599
at 5.830904 and -> -0.523599 as t -> 5.835904; the sampled values are a little inside because no sample falls
on the jump. C: the perpendicular from the listener meets the last piece (200,1200)-(0,0) inside it, at
D = 1972.79 m; (c) gives 0.027798 at 5.752818, minimum -0.027798 at 5.756568. All three agree.
The sampled minima in A and C (-0.03831, -0.02743) are about 2% and 1.3% short of the continuous-time
cusp values (-0.03904, -0.02780), because the minimum is a square-root cusp and the nearest sample is up to
23 microseconds off it. That is a property of sampling, not of emitter spacing.

Movement on halving the spacing:
- A max: 0.039112 (0.08), 0.039056 (0.04), 0.039050 (0.02), 0.039043 (0.01), 0.039043 (0.005), 0.039043 (0.0025).
  A min: -0.038284, -0.038284, -0.038324, -0.038304, -0.038304, -0.038309 (wanders in the 4th figure: the cusp).
- B: no movement at all at any spacing (all emitters are equidistant).
- C max: 0.027835, 0.027808, 0.027799, 0.027799, 0.027796, 0.027797; min -0.027426 ... -0.027430;
  energy 2.1792e-6, 2.1779e-6, 2.1780e-6, 2.1779e-6, 2.1778e-6, 2.1778e-6.
So from h = 0.01 m down: peaks steady to about 1 part in 10^4, energy to 3 parts in 10^5. Times of the
extremes do not move by more than one sample (23 microseconds) from h = 0.02 down.

## (3) Clap and rumble
In this model sound comes only from where the stroke's distance from the listener is stationary or its
direction relative to the line of sight changes. A CLAP is a stretch of stroke lying on (or tangent to) a sphere
about the listener, so that its length arrives all inside one pulse length: an arc gives the full N-wave
(L/R), a tangent point of a straight or gently curved run gives 0.94 sqrt(cT/D). A RUMBLE is the long train of
small parabolic bumps, of either sign and size (cT/r) times the jump in 1/cos(theta), one from every kink,
arriving in order of distance: the interiors of straight runs cancel themselves, because the pulse has zero
area. Its length is (r_max - r_min)/c. A perfectly straight stroke would sound like one sharp crack
(up-down, 5 ms, from the nearest point, if the perpendicular meets it), then a faint negative tail dying as
(time)^(-3/2), then near-silence until a very small bump from each end; seen end-on, only the two end bumps.
No rumble at all.

## Not reached
- No program run for the crooked stroke of (d): the predictions are untested by me.
- (b) is checked only through C's agreement with (c), not by a separate numerical test of one small piece.
- No run at a second sampling rate.
