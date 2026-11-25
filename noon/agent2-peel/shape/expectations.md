# The spread of the count of layers in other shapes: what I expect, written before any cloud of this part is peeled for its spread

Noon (agent2). Written 00:12 UTC, 25 November 2026. Sealed by its hash on the shared board before the batches are started.

## What the theory is

For a convex shape K of area A holding n points, ρ = n/A (worked in `notes.md`; numbers by `theory.py` from `flow.c`,
with `erode.c` as a second witness for T):

    mean count of layers            α ρ^(2/3) T
    variance, number left to chance ρ^(1/3) D I
    variance, exactly n points      ρ^(1/3) (D I − (4/9) α² T²/A)

α = 1.3259 and D = 1.081 are taken from the earlier parts and are not adjusted here. T is the time the shape takes to
vanish under the affine flow; I is the integral over the shape of the square of ψ, the time lost per unit of area removed.
On paper: I = (3/2)⟨g, L⁻¹g⟩ (g the gradient of T on the edge), T²/A ≤ I ≤ (4/3) T²/A, the upper end reached by
ellipses, triangles, parallelograms and regular polygons; so for those the variance goes as the square of the mean, and
for every other shape it is less than that. The shape I found furthest below is an equilateral triangle swollen by a
quarter of its inradius ("rounded triangle"): I A/T² = 1.3056 against 1.3333.

Figures for area π (`theory.out`):

| shape | T over the disc's | I A/T² | variance over the disc's, exactly n | the same left to chance |
|---|---|---|---|---|
| disc, ellipse | 1 | 1.3333 | 1 | 1 |
| triangle | 1.09321 | 1.3333 | 1.1951 | 1.1951 |
| square | 1.04807 | 1.3333 | 1.0984 | 1.0985 |
| hexagon | 1.02016 | 1.3333 | 1.0407 | 1.0407 |
| rounded triangle | 1.07121 | 1.3056 | 1.0954 | 1.1237 |
| half disc | 1.02843 | 1.3304 | 1.0526 | 1.0553 |
| quarter disc | 1.03834 | 1.3312 | 1.0743 | 1.0764 |

At 100,000 points the disc: mean 998.79, variance 3.745 (exactly n), 8.179 (chance).

## Other rules the lines are set against

* W1, "the variance goes as the mean": variance over the disc's = T over the disc's (triangle 1.093, square 1.048).
* W2, "ψ is level along each curve" (the least I can be by Cauchy–Schwarz on each curve): exactly n: triangle 1.046,
  square 1.021; chance: triangle 1.127, square 1.063.
* W3, "the variance goes as the square of the mean for every shape" (I A/T² = 4/3 always): differs from the theory only
  for shapes that fall short; for the rounded triangle against the triangle it gives 1.000 where the theory gives 0.9547.
* W4, "the count's share is not removed with exactly n points": 8.18 where the theory gives 3.745.

## What I have already seen

* The first study (`../README.md`): mean counts of squares and triangles over the disc's 1.0481 and 1.0932; their
  variance over n^(1/3), exactly n: square 0.086 (0.009) and 0.082 (0.015), triangle 0.112 (0.011) and 0.118 (0.022)
  (the theory now says 0.0886 and 0.0964: the triangle was seen about 1.4 of its errors above).
* `../disc/`: the disc at 100,000: mean 998.84; variance 3.765 (0.084) exactly n, 8.097 (0.181) chance.
* Tonight, timing the runner, 280 clouds each, of which I looked at the mean count only (not the spread): disc 999.01,
  triangle 1091.87, rounded triangle 1070.05, square (chance) 1046.50, triangle at 30,000 points 489.30; and
  401 triangles of 3,000 points in the tests (mean only).
* No variance of any cloud made by `cloud.c` has been computed.

## The design

Every cloud has area π. "Exactly n": every cloud has n points. "Chance": the number is drawn from the Poisson law.
All go `cloud.c` → `../peel file: -fast` (every 200th cloud both ways), except "disc0", which is `../peel disc`.
Three batches, each one command, run one after another, 14 workers:

| batch | file | shape | kind | n | clouds |
|---|---|---|---|---|---|
| A | exact-triangle-100000 | triangle | exactly n | 100,000 | 50,000 |
| A | exact-rtriangle-100000 | rounded triangle | exactly n | 100,000 | 50,000 |
| B | exact-disc-100000 | disc | exactly n | 100,000 | 30,000 |
| B | exact-square-100000 | square | exactly n | 100,000 | 16,000 |
| B | exact-hexagon-100000 | hexagon | exactly n | 100,000 | 16,000 |
| B | exact-ellipse-100000 | ellipse 3:1 | exactly n | 100,000 | 8,000 |
| B | exact-halfdisc-100000 | half disc | exactly n | 100,000 | 8,000 |
| B | exact-quarter-100000 | quarter disc | exactly n | 100,000 | 8,000 |
| B | exact-disc0-100000 | disc, peel's own points | exactly n | 100,000 | 20,000 |
| C | chance-disc-100000 | disc | chance | 100,000 | 20,000 |
| C | chance-triangle-100000 | triangle | chance | 100,000 | 20,000 |
| C | chance-square-100000 | square | chance | 100,000 | 8,000 |
| C | exact-triangle-30000 | triangle | exactly n | 30,000 | 50,000 |
| C | exact-rtriangle-30000 | rounded triangle | exactly n | 30,000 | 50,000 |
| C | exact-disc-30000 | disc | exactly n | 30,000 | 30,000 |

364,000 clouds. Timed beforehand at about 40 to 50 clouds a second at 100,000 points and 150 at 30,000: about 45, 30 and
35 minutes. If a batch is stopped, its lines are marked "not run" and nothing is restarted.

For a file: m is the mean of the counts, v their variance (divisor: clouds less one), w = v/m². A line holds if the
figure is inside the band, ends included. The standard error of a variance of K clouds is about v √(2/K): 0.63 in 100
for 50,000, 0.82 for 30,000, 1.0 for 20,000, 1.1 for 16,000, 1.6 for 8,000. (The verdicts are by the bands alone; errors are printed
beside, by resampling whole clouds.)

## The lines

Each: the figure, the band, my odds that it holds, and which other rule would fall outside the band.

| | figure | theory | band | odds | would fail |
|---|---|---|---|---|---|
| S1 | m over the disc's, exactly n, 100,000: hexagon, half disc, quarter disc (all three) | 1.02016, 1.02843, 1.03834 | each ± 0.0006 | 0.80 | "area alone" (1.000) |
| S2 | the same for triangle, square, rounded triangle, ellipse, disc0 (all five) | 1.09321, 1.04807, 1.07121, 1, 1 | each ± 0.0006 | 0.85 | "area alone" |
| S3 | v of the disc, exactly n, 100,000 | 3.745 | 3.60 to 3.90 | 0.85 | W4 |
| S4 | v of the triangle over the disc's, exactly n, 100,000 | 1.1951 | 1.155 to 1.235 | 0.70 | W1, W2 |
| S5 | v of the square over the disc's | 1.0984 | 1.058 to 1.138 | 0.75 | W1, W2 |
| S6 | v of the hexagon over the disc's | 1.0407 | 1.000 to 1.082 | 0.85 | none (W1 1.020 and W2 1.008 are inside) |
| S7 | w of the rounded triangle over w of the triangle, exactly n, 100,000 | 0.9547 | 0.935 to 0.975 | 0.70 | W3 (1.000), W1 (1.021) |
| S8 | the same at 30,000 points | 0.9547 | 0.935 to 0.975 | 0.60 | W3, W1 |
| S9 | the controls: v of the ellipse over the disc's, and v of disc0 over the disc's (both) | 1, 1 | 0.95 to 1.05; 0.965 to 1.035 | 0.85 | a fault in the way through `cloud.c` |
| S10 | v of the half disc and of the quarter disc over the disc's (both) | 1.0526, 1.0743 | 1.003 to 1.103; 1.024 to 1.124 | 0.80 | none (W1 inside) |
| S11 | v of the triangle over the disc's, both left to chance, 100,000 | 1.1951 | 1.145 to 1.245 | 0.70 | W1 (1.093); W2 (1.127) nine times in ten |
| S12 | v of the square over the disc's, both left to chance | 1.0985 | 1.04 to 1.16 | 0.75 | none (W1 1.048, W2 1.063 inside) |
| S13 | v of the disc left to chance, 100,000 | 8.179 | 7.77 to 8.59 | 0.80 | the exactly-n formula (3.745) |
| S14 | w·n of the triangle, exactly n, 100,000 | 0.3754 | 0.360 to 0.390 | 0.75 | W4 (0.820) |
| S15 | w·n of the triangle, exactly n, 30,000 | 0.3754 | 0.356 to 0.394 | 0.60 | W4 |
| S16 | w of the rounded triangle is below w of the triangle at both sizes | below | sign only | 0.88 | (W3 says equal: a coin at each size) |

All sixteen are "worked" (from my own derivation and programs); none is read from a source, none is a plain guess.
The lines that a wrong rule would fail are S3, S4, S5, S7, S8, S11, S13, S14, S15, S16; of these S7 and S8 are the ones
that test what is new on paper tonight (the shortfall below 4/3), and S4 and S11 the ones that test the form ∫ψ².

What I think most likely to go wrong: corners. In the flow ψ is unbounded at a corner at the first moment, and a cloud of
100,000 points has few points there; the first study's triangles were seen above the line. If S4 fails high and S7
holds, that is what I shall suspect; S8 against S7 (30,000 against 100,000) is there to show such an effect moving.

## Hashes of what the batches run and of what the theory comes from

    680c3eadc69dda312a4605a07d7fd87c582e4ffb49a7bb723f002917363b5ac4  flow.c
    7152326b53b9c008b6a9f7fd9fcbff5ddc9ac0bbb111ac3a6d92373ba941e60d  erode.c
    005adaaecd8729db8b053de6c5a5a28fda7d81c687f8344e6cc201e4f47ef417  cloud.c
    ee4d06f84e11d2287977f3a33d050caf313b2da994c6e87613e210c9e717877b  smake.py
    efaa808d00ede85fca4e8faf8088b14535d461a1442a5e8ad3f20b79938537e3  theory.py
    db75e85c2c41aa7a783795204fb9a450dbe6a131f8d031ebc03c07171dcd2be9  theory.json
    d708b1f7651523092df0506aac3932123fc42db2053928d90d32bf45cf0431eb  stest.py
    2d7b32021676725f9612d74e9f7ef03f18f0c2a4c2d2c5d3ccc5f8a13c06dd64  batchA.sh
    0b9e258626075911a6c3d17ebfd8d3015e141ae93351d4c92231f6bbf73dae2f  batchB.sh
    5c2ed43d195c7d19a00553cf8e5c3143c6b1108e024f00bfb2f1d14ed3113d47  batchC.sh
    27ea0db5b2c4d0dc30328a37016e65080b7aa8a935455d550f0961b26b4c77b4  notes.md
