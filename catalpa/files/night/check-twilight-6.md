# The tenth sheet (a model of the twilight with the Hunga haze): the sealing, the model, the result

Started 01:06:15 UTC, 28 November 2026. Finished 01:38:02 UTC (31 minutes 47 seconds). Limit 60 minutes.

My programs and outputs are in `check/m19/` (`order2`, `bands`, `indep`, `orders`, `grids`, `edge`, `tails`), the blind reading in
`check/fig3_blind.txt` (program `check/fig3read.py`), the file times in `check/sealing19.out`.

**Findings: 1 serious, 7 moderate, 6 minor.** I found no mistake in the model's code. Every test of its once- and
twice-scattered sums agrees with it; my test of the higher orders agrees at two cases and runs a quarter low at a
third. What fails is the sentence about the makers' response: it holds for one height of the layer
only. The coordinator's own runs with the layer 1.5 km lower and higher, finished at 01:19 and 01:33 while I worked,
put the model with that response outside 0.15 at three or four of the seven depths. Beyond that the result is a balance of a dimmed
blue and a brightened red, and two of the six verdicts were decided inside the Monte Carlo's own error.

## Step 1: the blind reading (written 01:07:50, before any file under `model/` was opened)

Read by program from the figure's own bitmap in the PDF (1188 by 733 pixels), by pixel colour, with the scales taken
from the frame and checked on the grid lines. Means over the bins 400-450 ... 700-750 nm, relative to the TESS
curve's highest value (98.2 on the figure's scale, at 675 nm):

| | 425 | 475 | 525 | 575 | 625 | 675 | 725 |
|---|---|---|---|---|---|---|---|
| TESS, mine | 0.575 | 0.670 | 0.768 | 0.847 | 0.924 | 0.985 | 0.768 |
| TESS, `haze_bands.py` | 0.58 | 0.68 | 0.77 | 0.82 | 0.90 | 0.96 | 0.75 |
| SQM, mine | 0.472 | 0.597 | 0.673 | 0.479 | 0.120 | 0.009 | 0.006 |
| SQM, `haze_bands.py` | 0.47 | 0.61 | 0.67 | 0.52 | 0.25 | 0.04 | 0.0 |

The TESS readings agree to 0.03 in every bin. The SQM reading in `haze_bands.py` is too high in the 600-650 nm bin
by a factor of two (the curve is 27 at 600 nm, 10 at 625, 2 at 650; 0.25 is its value at 602 nm, not the bin's mean).
My SQM figures beyond 650 nm are the half-thickness of the drawn line, that is, nothing.

## Step 2: the sealing holds, as far as files can show

- `run_haze.py` was born at 00:32:39.000, the sheet at 00:32:39.008, the sealed run's output 0.045 s later; the run
  ended at 01:02:57, which is the 1,818 s its own log gives. `run_haze.py` did not exist before that second and has not been changed since.
- `twimc.py` and `mie.py` were last changed at 00:29:31.74. The earlier form is kept (`twimc_v1.py`) and differs only
  by the droplet layers. All fourteen fingerprints match `SHA256SUMS`; the sheet, the four programs and two clear
  outputs are in the board's 00:32 entry.
- The four test programs written before the sheet (each written once) use no Hunga layer; their second atmospheres
  differ only in the haze near the ground. The eight clear runs vary ozone, ground and low haze, never the
  stratosphere.
- Limits. No output of the four tests is kept. `test_layers.py` (00:29:32) ran the droplet haze of the comparison
  years (0.008) where the clear runs had another form at 0.004, at 2 and 5 degrees and two colours: the stratosphere's
  haze did differ between runs, though not in a pair and not at depth. The board's entry carries its own time only.

## Step 3: the model

Read for mistakes: none found in the geometry, the weights of the paired method, the phase tables, the droplet code
or the drivers. Tested:

| test | result | output |
|---|---|---|
| Once-scattered light, my own sum, 3 cases with and without the plume | equal to the run to 4 figures | `m19/indep_*.out` |
| Twice-scattered light, my own Monte Carlo integration, 675 nm at 6 degrees | with 1.03, without 1.01 of the run's direct sums (my error 0.06); ratio 2.26 +- 0.08 against 2.248 | `m19/indep_675_6.out` |
| The same, 725 nm at 9 degrees | 1.11 and 1.11 (my error 0.16); ratio 2.97 +- 0.18 against 3.024 | `m19/indep_725_9.out` |
| The same, 475 nm at 8 degrees | 1.25 and 1.19 (my error 0.3); ratio 0.78 +- 0.11 against 0.738 | `m19/indep_475_8.out` |
| The run's own twice-scattered light, direct sums against its paired Monte Carlo, ratio with/without over the band | 1.310 / 1.312 at 3 degrees ... 1.918 / 1.885 +- 0.04 at 8, 1.963 / 2.01 +- 0.07 at 9 | `m19/order2.out` A |
| All orders by a backward Monte Carlo of my own (directions drawn evenly, my own geometry and droplets), 675 nm at 6 degrees, 800,000 photons | once 0.98 and 0.97 of the run, twice 0.98 and 0.97 (ratio 2.256 against 2.248); three times and more 1.16 +- 0.15 and 1.09 +- 0.08, ratio with/without 4.0 +- 0.4 against the run's 3.8 | `m19/orders_675_6.out` |
| The same, 725 nm at 8 degrees | twice 0.99 and 1.02 of the run (ratio 2.83 against 2.90); three times and more 0.89 +- 0.20 and 1.10 +- 0.18, ratio with/without 4.7 +- 0.8 against the run's 5.8 | `m19/orders_725_8.out` |
| The same, 525 nm at 7 degrees, two runs of mine (2,000,000 photons) | twice 0.91 to 0.96 of the run; three times and more 0.61 and 0.74 with the plume, 0.80 and 0.84 without; ratio with/without 1.4 +- 0.1 and 1.6 +- 0.3 against the run's 1.86 +- 0.13. The model's plain Monte Carlo, one atmosphere at a time, gives 0.88 +- 0.21 and 0.96 +- 0.11 of the run, ratio 1.69 | `m19/orders_525_7*.out`, `m19/sep_525_7.out` |
| Paired method, second atmosphere identical | differences exactly 0 | `m19/grids_675_8.out` (a) |
| Finer grids in `second` WITH the plume, 675 nm at 8 degrees | 96x32x140: 9.633e-07; 160x48x200: 9.626e-07; 224x80x260: 9.623e-07; ratio with/without 2.4349, 2.4343, 2.4342 | `m19/grids_675_8.out` (b) |
| The same, 725 nm at 10 degrees | 96x32x140: 2.7612e-07; 160x48x200: 2.7571e-07; ratio with/without 3.0771, 3.0735 | `m19/grids2_725_10.out` (b) |
| Droplets: my own Mie code (Bessel functions, textbook ratios) | Qext and Qsca equal to 5 decimals at five single spheres; for the two hazes g 0.6847 / 0.6846 and 0.7729 / 0.7729, extinction against 550 nm 0.7045 / 0.7042 and 0.8870 / 0.8870, phase tables within 0.23% | `m19/edge.out`, `m19/indep_*.out` |
| Small sphere, large sphere, energy | 6.9355e-07 against the formula's 6.9368e-07; 2.0457 against 2.0446 at x = 300; Qsca = Qext | `m19/edge.out` |
| Phase tables: mean one; sampling gives them back | 1.00000; drawn over expected 0.996 to 1.005 in nine rings | `m19/indep_*.out` |
| Sun table at the shadow's edge | within 0.9% (3% at 475 nm) from 0.3 degrees inside the light; leak into the shadow 0.00015 of sunlight at 675 nm | `m19/edge.out` |

## Step 4: the result

**(a) The six verdicts are right and the Brier score is 0.186** (0.1858; `m19/bands.out` F).

**(c) The claim with the makers' response is carried for the central case and for neither other height run**
(serious 1).
With my blind weights the central model gives
+0.03, -0.09, -0.13, -0.28, -0.48, -0.69, -0.81, -0.86, -0.93 at 3 to 11 degrees: within 0.15 of the meters at 7 of
7 depths, largest difference 0.085 (0.089 with the coordinator's weights). Moving every bin of the reading 0.05 the
worst way leaves 7 of 7 (`m19/bands.out` B, C). The model also has the meters' ramp from 3 to 4 degrees and their
shelf from 4 to 5: steps of -0.13 and -0.04, the meters' -0.12 and -0.06. The plume at 0.014 and 0.022 gives 7 of 7 (largest 0.119). Set
against the meters with 2021 alone or 2024 alone as the comparison (my fifth report) it is still 7 of 7.

**(d), (f)** are under moderate 6 and 7; **(b)** under moderate 4; **(e)** under moderate 5.

## Serious

1. **"Within 0.15 of the meters at all seven depths with the makers' printed response" holds only with the layer
   at 21 km.** The coordinator's two runs with the layer moved (600,000 photons a case), summed with the printed
   response (`m19/z195.out`), at 3 to 11 degrees:
   - layer at 19.5 km: +0.07, -0.01, -0.04, -0.16, -0.32, -0.51, -0.61, -0.71, -0.67. Too faint by 0.11 to 0.19 at
     every depth from 4 to 10; within 0.15 at 4 of 7 with my weights, 3 of 7 with the coordinator's.
   - layer at 22.5 km: -0.02, -0.19, -0.23, -0.40, -0.63, -0.83, -0.98, -1.15, -1.26. Too bright by 0.10 to 0.33
     from 6 to 10 degrees; within 0.15 at 3 of 7.

   The print has the strongest part of the layer at 19 to 21.5 km for 50 to 30 south and at 21.5 to 23.5 km for 30
   to 10 south, so both heights are as allowed as 21 km. The model moves by 0.11 to 0.15 magnitude for each
   kilometre at 8 to 10 degrees. The response and the height trade against each other (depths within 0.15, of seven):

   | | layer at 19.5 km | 21 km (sealed) | 22.5 km |
   |---|---|---|---|
   | response as remembered (sealed) | 7 | 4 | 2 |
   | response as printed | 4 (3 with the coordinator's reading) | 7 | 3 |

   May say: "With the response the makers print and the layer centred at 21 km, the height fixed before the run,
   the model is within 0.09 magnitude of the meters at all seven depths from 4 to 10 degrees. With the layer 1.5 km
   lower it is 0.11 to 0.19 too faint, and 1.5 km higher up to 0.33 too bright; the satellite papers allow both.
   The response was corrected after the sealed run, and the sealed line itself failed."

   A thing this opens, not checked: the print puts the layer higher towards the tropics, and the meters' largest
   figure at depth is Réunion's (21 south) and the smallest Martinborough's (41 south). That is the direction the
   model's height gives. It would need its own sealed line.

## Moderate

1. **Z5 and Z6 were each decided inside the Monte Carlo's own error.** Z6 failed because the model missed the
   0.15 mark by 0.002 at 9 degrees and by 0.010 at 8, where the run's own errors are 0.025 and 0.016; either one
   inside would have made it hold. Z5 held with a step of -0.082 against a mark of 0.10, where the errors at 10 and
   11 degrees are 0.034 and 0.052 (`m19/bands.out` F). May say: "Five lines held and one failed by the rule of the
   sheet; two of the six (Z5, Z6) turned on less than the Monte Carlo's error."
2. **At 10 and 11 degrees the model's figure is not secure.** Light scattered three times and more is 35 and 39 in
   100 of the ordinary twilight there and carries 62 and 75 in 100 of the added light, and it comes from the Monte
   Carlo alone. Without the higher orders the model gives -0.72, -0.71, -0.59 at 9, 10, 11 degrees
   (`m19/bands.out` F, last line). The same Monte Carlo's twice-scattered light is below the direct sums by 9% and
   36% without the plume and by 2% and 8% with it (`m19/order2.out` A); at 475 nm and 11 degrees it is 7 to 15 times
   below. Paths are drawn in the haziest atmosphere, so the atmosphere without the plume gets the wilder weights. If
   the higher orders are low in the same way, the sealed model is about -0.99 and -1.01 at 10 and 11 degrees, not
   -1.01 and -1.09. The higher orders are carried by a few rare paths: without the plume the five largest of the
   hundred batches hold 28 in 100 of that light at 10 degrees and 42 at 11, and the middle batch is 0.62 and 0.37 of
   the mean (`m19/tails.out`); the error printed from the batches understates. May say the model's figures to 9
   degrees; for 10 and 11, "about -0.9 to -1.1, where the Monte Carlo is not to be trusted".
3. **The band figure is a balance of opposite changes, and the weights that set the balance were changed after the
   run.** At 8 degrees the model dims 425 and 475 nm by 0.23 and brightens 675 and 725 nm by 1.10 and 1.30. The
   sealed weights were remembered wrongly (0.32 at 425 nm where the makers print 0.58; 1.00 at 725 where they print
   0.77). The correction is sound: my blind reading gives the same weights. But it was made after the result was
   seen, and it moved the model 0.08 to 0.16 towards the meters from 6 to 11 degrees (and 0.05 away from them at 4
   and 5). The sentence under serious 1 is the one to use; it may add "(a
   checker's blind reading of the figure gives the same response to 0.03 and the same result to 0.01)"
   (`m19/bands.out` A, B).
4. **(b) The ordinary curve: to 7 degrees the agreement is the model's, beyond 8 it is the choice.** From 4 to 7
   degrees every setting tried (low haze 0.03, 0.08, 0.20; ozone 210, 300, 390; ground 0.05 to 0.35) is within 0.09
   of the meters. At 8, 9 and 10 degrees the settings spread over 6.26 to 6.53, 7.36 to 7.74 and 8.11 to 8.97, with
   the meters at 6.34, 7.30, 8.26 inside (`model/clear_*.out`; noisy there). The choice hardly moves
   the result itself: with the low haze at 0.08 in place of 0.03 the once- and twice-scattered light changes with the
   plume by a factor of 2.15 in place of 2.24 at 675 nm and 8 degrees (0.05 magnitude), 2.93 in place of 3.07 at 725 nm and
   10 degrees (0.05) and 0.721 in place of 0.724 at 475 nm and 8 degrees (`m19/lowhaze_*.out`,
   `m19/grids2_725_10.out` c). May say: "With the low haze set to the value that fits best (0.03) the model's
   ordinary twilight follows the meters within 0.08 magnitude from 3 to 10 degrees; from 3 to 7 degrees any value
   from 0.03 to 0.20 does so within 0.09."
5. **(e) What could move the answer by more than its margin (0.09 achieved, 0.15 allowed).**
   - The amount of haze: 0.014 to 0.022 moves 10 degrees from -0.75 to -0.94 (my weights). By that slope a plume of
     0.010 or 0.028, which a two-to-one disagreement allows, gives about -0.65 or -1.08: outside.
   - The droplets' size was never varied. It sets both the forward peak and the split between blue and red.
   - The haze of the comparison years. `model/haze_where.out` has 62 in 100 of the ordinary twice-scattered light at
     675 nm first scattered at 16 to 26 km: the model's ordinary red twilight is mostly this layer, whose height and
     width are assumed. The brightening is measured against it.
   - The layer's height: it does, by 0.11 to 0.15 magnitude a kilometre at 8 to 10 degrees (serious 1).
   - Probably not, by size: the ozone table (it moves weight to colours whose change is near the band's mean), one
     direction, the Sun table, polarization. Bending of rays is small at 21 km but not for the low rays that feed
     the blue. Not known: clouds; a layer that differs towards the Sun (the meters' evenings and mornings differ by
     up to 0.4 at a place at 10 degrees).
   - The meters themselves are known to about 0.1 at depth. An agreement of 0.09 is inside both uncertainties.
   May say: "consistent with the meters within the uncertainties of both"; not "reproduces" and not "with nothing
   adjusted" without the sentence about the response.
6. **(d) The other make of meter: fair to set side by side as "not contradicted", no more.** Fiorentin and others
   2025: one SQM at La Silla (29 south, 2,400 m), the mean of the readings at dusk and dawn "when the Sun is about
   at -6 degrees", monthly means from 2018 to the beginning of 2024. They fit one straight line to six years and
   report no trend; of 2022 they say only that a strong change in aerosol "does not correspond to a high variation".
   They did not set 2022 against other years. The model for an SQM at 6 degrees is +0.01 with my weights (-0.02
   with the coordinator's), and 6 degrees is where it crosses from dimmer (+0.09 at 4) to brighter (-0.09 at 8):
   a record at that one depth cannot tell this model from no effect at all. With the layer at 19.5 or 22.5 km the
   model's SQM figure at 6 degrees is +0.07 or -0.10. But their Figure 19 (the saved image, read by my eye, which the authors do not say) has the
   brightest months of 2022 at about 13.70 where 2019 and 2021 have 13.83 and 13.85, and June to August 2022 about a
   tenth of a magnitude brighter than the same months of 2019 to 2021. If that is right the SQM changed by about a
   third of what the TESS meters did, the model's nothing is short by about 0.1, and "reports no trend" alone would
   be a one-sided use of the paper. May say: "For the other make of meter
   the model gives no change at 6 degrees (+0.01). The one published record of that make, at 6 degrees, is reported
   by its authors as showing no trend over six years; its plotted points for mid-2022 look about a tenth of a
   magnitude brighter, a third of what the meters here show." (`m19/bands.out` B)
7. **(f) The model's zenith figure does not bear on the Paranal factor of five, beyond its sign.** De Rosa and
   others 2023 measured twilight sky flat fields with OmegaCAM on the VLT Survey Telescope through a segmented
   filter: the ratio of i (770 nm) to g (480 nm) and to u (350 nm), each normalised to its value before the
   eruption. The text and caption give neither where the telescope pointed nor how deep the Sun was. The factor of
   five is the first days after the eruption; by my eye their Figure 2 has the ratio at about 1.5 to 3 through
   2022. The model is for the zenith, 425 to 725 nm, the haze of June to August: its 725 over 475 nm rises by 1.6,
   2.2, 3.0, 5.1 at 4, 6, 7, 9 degrees. May say: "The model reddens the twilight, as the flat fields at Paranal
   did; the two cannot be compared in size."

## Minor

1. The SQM reading in `haze_bands.py` (600-650 nm: 0.25, mine 0.120) makes the SQM look more like the TESS than
   it is: at 8 degrees -0.14, with mine -0.09; at 11 degrees +0.07, with mine +0.17.
2. The sheet's "no two atmospheres that differ in the stratosphere's haze" holds for pairs only (step 2, limits).
3. The model's colours stop at 400 and 750 nm; the TESS curve runs from 385 nm and has a tail to 800 (22 at 750
   on the figure's scale). Both ends are small and pull opposite ways.
4. The 700-750 nm bin holds the steep edge and 9 nm hidden by the legend: moving it between 0.70 and 0.84 moves 10
   degrees by 0.02.
5. `brute.out`: at 425 nm and 5 degrees two separate runs give +0.142 +- 0.035 against the sealed +0.193, 1.5
   errors apart; the other four cases are within one.
6. The self-test in `mie.py` scales a single sphere's phase function to a mean of one half: run, it prints means of
   0.5007, 0.5040, 0.5000, 0.5002 and a g from the phase function of half the true one. The model does not use that
   line (the tables it uses average to 1.00000).

## Not checked, and unfinished

- No run of the whole model by me: every band figure here is the stored run summed again.
- The higher orders (three and more) were tested independently only at the three cases in the table, and only to
  about a quarter. At 525 nm and 7 degrees mine come out a quarter below the run's in two runs; my estimator also ran
  4 to 12 in 100 low on the exact twice-scattered sums there, so I read the difference as mine, but it is not
  settled. Nothing of mine tests the higher orders at 9 degrees and deeper, where they matter most.
- Droplet size, the haze of the comparison years and ozone were not varied by anyone; the layer's height only by the
  coordinator's runs at 19.5 and 22.5 km, which I summed again but did not test.
- Polarization, bending and clouds are judged by argument, not by a run.
- Fiorentin's Figure 19 and De Rosa's Figure 2 were read by eye from the saved image and page; the La Silla unit's
  own response was not read.
- `model/haze_where.out` was glanced at, not checked.
