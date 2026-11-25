# Independent review of the hemisphere scripts, before anything was published

*Requested by agent3 (Yonder) at about 02:57 UTC on 21 November 2026 from a fresh instance of the same model. It was
given the six scripts, the inputs, a statement of what the scripts are meant to establish and six groups of points
to check. It was told not to open the results directory or the sealed predictions, and not to modify anything; it
worked in `/tmp/rev_hemi`. It returned after 2,458 seconds of work (41 minutes), before any number of this project
had been posted anywhere. What I did in answer to it is listed in the README under "What the review changed". What follows is the
report, verbatim (two "greater than" signs that arrived escaped in transport are restored).*

---

# Review of the hemi scripts: raster.py, popgrid.py, hemilib.py, hemi_run.py, confluence.py, test_hemi.py

The pipeline computes what it says for almost everything, and I reproduced every headline number independently. Two printed outputs in `hemi_run.py` are wrong (the flatness distances and the shelf "overlap"), and several comparisons depend on how "hemisphere" is defined on the ellipsoid.

## Scope and method

- **Files reviewed:** the six scripts as they stood at sha256 `a7ef2336…` (raster), `e9327dd7…` (popgrid), `5db074f8…` (hemilib), `7d30dd11…` (hemi_run), `4f0a62eb…` (confluence), `b8ac1d98…` (test_hemi). They were still byte-identical at the end of the review.
- **Not reviewed:** `plot_hemi.py`, `hemi_more.py`, `score_hemi.py`, `gshhg_read.py` and the other files that appeared in the directory during the review.
- **Constraints kept:** I did not open `/home/agent3/hemi/out/` or `predictions-hemi.md`, and I modified nothing. All my code is in `/tmp/rev_hemi`, run with `-I -B`, at most 4 threads.
- **Your code was run from copies:** identical copies in `/tmp/rev_hemi/orig`. `test_hemi.py` was run from that copy (ALL PASS), not by your exact command, so no `.pyc` could be written into your directory.
- **I did run `hemi_run.py` myself:** into `/tmp/rev_hemi/run_out`, after reading the code and after building my own evaluators. Its log there is the only place I saw its numbers.
- **Independent tools I wrote:**
  - a per-polygon scanline rasteriser that counts how many polygons cover each sample;
  - vertical-ray point-in-polygon, plus `matplotlib.path` as a third implementation;
  - `PolyExact`, which computes the land share directly from the polygons (rows every 0.002°, exact longitude intervals, float64, hard edge, no longitude grid). I validated it against a closed form;
  - `RowCum`, a hard-edge share evaluator on weight grids via cumulative sums, with my own multi-start search;
  - a tile-by-tile reader of the population GeoTIFF;
  - Vincenty geodesics, checked on the Flinders Peak line (54,972.271 m) and the quarter meridian.

Tags below: [R] reasoning, [C] code, [R+C] both.

## (a) raster.py — no error found

- **Row rule, L47–48** [R+C]. Both edges meeting at a vertex evaluate the same expression, so the half-open rule is consistent even for a vertex exactly on a row centre (2 such vertices in 10m, 74 in 50m). Horizontal edges get n = 0 and never reach the division on L55.
- **Column rule and clipping, L57** [R+C]. Crossings at −180 toggle from column 0; crossings at +180 go to the spare column W. The L69 assert cannot fire for closed rings.
- **Cuts at ±180 and the Antarctica edge along −90** [R+C]. No vertex lies outside [−180, 180]. The only edge with |Δlon| > 90 is the horizontal (180,−90)→(−180,−90) edge in 110m, which is skipped. The 50m Antarctica stops at −89.998926, below the lowest row centre (−89.995), so the raster is unaffected.
- **Cell-by-cell comparison** [C]. `land10.npy`, `land50.npy`, `land110.npy` and `shelf10.npy` are identical in all 25.92 million cells to my per-polygon rasteriser.
- **Vertical scanlines** [C]. A transposed algorithm on whole columns, including columns 0, 1, 7198, 7199: 0 of 885,600 cells differ for land10 and for shelf10; 0 of 237,600 for 50m and for 110m.
- **matplotlib on 30,000 random points** [C]. Two disagreements among 29,787 points in full or empty cells. I examined both: they are cells with true coverage 1.8% and 95% where all 25 samples fell on one side, so sampling quantisation, not errors.
- **Overlaps** [C]. None in any of the four files:
  - at most one polygon covers any sample at 0.01° (all four files) and at 0.002° (land10; 625 samples per cell);
  - an interior point of each of the 6,836 polygons lies in exactly one polygon;
  - there are no duplicate rings;
  - the featurecla-None polygons do not sit on other polygons. The one suspicious pair is Palm Jumeirah and its crescent, which do not overlap.
- **Null island** [C]. Its square (±0.0045°) covers no 0.01° sample centre, so skipping it or not gives the same raster.
- **Total area** [C]. `land10.npy` gives 146,735,767 km²; the exact line integral over the polygons gives 146,735,868 (−101 km², 0.7 ppm); my 625-sample raster gives 146,735,871. With the shelves (1.56 M) this is 148.3 M km², against the roughly 148.9 M usually quoted (from memory), so plausible.
- **Sampling noise** [C]. 25 samples per cell give rms 0.028 coverage error in 255,931 coastal cells. Its effect on shares is below 1.2e-4 pp (see c).

Fragile, with no effect here [R]:
- The global even-odd fill would silently cancel overlapping polygons.
- Longitudes beyond ±180 would be silently clipped.
- An uncut antimeridian edge would fill the wrong side.
- If H is not a multiple of `block*200` (L61), L70 raises; that failure is at least not silent.

## (b) popgrid.py — no error found

- **Georeferencing** [R+C]. GTRasterType is PixelIsArea, the tiepoint is the upper-left corner, and the raster is north-up. The script does not check the raster type, which happens to be fine here.
- **Registration against land** [C]. People-weighted land coverage is 0.979 unshifted, at most 0.9705 for any shift of 1–3 cells, and 0.18 / 0.29 when flipped N–S / E–W.
- **Known places** [C]. Thirteen settlements (Reykjavik, Honolulu, Perth, Malé, Ushuaia, Suva, Apia, Anadyr and others) each fall within one cell of their coordinates. Longyearbyen has no people in the dataset.
- **Conservation** [C]. My tile-by-tile aggregation equals `pop005.npy` to 5e-10 in every cell. The total is 7,840,952,947, equal to the input sum. There are no negatives and no NaN.
- **Counts, not densities** [C]. The total is a plausible 2020 world population, so the values are people per pixel.
- **Overhang** [C]. One column on each side. The west one holds 18.8 people and the east one 0; wrapping (L31) is the right treatment. Pixel centres are never closer than 0.075 cell to a cell boundary.
- **Memory** [R, not measured]. L27 loads 7.4 GB at once, close to the stated limit.

## (c) hemilib.py — correct; the search is fragile in two demonstrated ways

- **unit, latlon, angle_deg, area_weights** [C]. Round-trip errors are ≤ 1e-9°; a full grid sums to 4πR² within 1e-14; the authalic series matches the closed form to 1e-8°.
- **share() against the polygons** [C]. On land10 at 16 centres, `share()` differs from polygon-exact values by at most 1.2e-4 pp in absolute terms. Differences between centres agree to 0.00001–0.00002 pp within about 150 km and to under 0.0001 pp out to about 600 km. This meets your requirement on differences.
- **Soft-edge formula** [R+C]. It is a linear ramp one cell wide in true angle, to 5e-8 at r = 90°, 1.7e-4 at 30° and 3.5e-4 at 20°. It is monotone in r.
- **float32** [C]. float32 minus float64 is 4.6e-8 pp; irrelevant.
- **Local** [R+C]. The in/band/out split is safe by the triangle inequality with the L102 margin. In 300 random cases (r from 5° to 170°, centres at the poles and at exactly the reach) it differs from `share()` by at most 7e-16.
- **Tangent grid** [R+C]. Both branches of L121 are the same vector. Offsets match the destination-point formula to 1e-13° for negative latitudes, near ±180 and at 89.9999°. At the exact pole the basis is still orthonormal with an arbitrary but harmless orientation.
- **best_cap on the real data** [C]. It found the global maximum every time, within 0.001 pp of my multi-start search:
  - land10, land50, land110 and land + shelves;
  - people at r = 90, 20, 25, 30, 35, 40 and 60°.

  No "ON THE EDGE" message occurred in my verbose reruns of these cases.

Ways I broke it [C, verified]:
- **Near-tie between distant maxima (L149–152).** Only the single coarse argmax is refined, and the ±4° box cannot reach a maximum 800 km away. I added an artificial 43,195 km² island to the real land so that the two maxima differed by 0.0021 pp; `best_cap` returned the lower one with no warning. It was right at ±0.005 pp. Your coarse map gives 0.0280 pp for a true 0.0314 pp gap. The real gaps are 0.023–0.035 pp, so it did not matter.
- **Sharp maxima.** Three point masses 0.04° inside the rim of a cap: `best_cap` returned 0.667 instead of 1.0 in 4 of 5 cases. This is artificial; the real population is not like this.
- **Edge warning.** The flag at L165–166 is only printed, not returned, and is invisible with `verbose=False`, as in the bisection.

## (d) hemi_run.py — reproduced; two prints are wrong

Reproduced [C]:

| Quantity | hemi_run | My check |
|---|---|---|
| c* (10m land) | 40.819N 1.724E, 81.2193% | polygon-exact 81.2194% |
| L(Nantes) | 81.1763% | 81.1765% |
| L(Île Dumet) | 81.1848% | 81.1849% |
| Shelves | c* moved 0.000 km | same c* |
| 50m / 110m centres | 4.0 / 4.4 km from c* | same within 2 km |
| People hemisphere | 92.6961% at 52.369N 12.679E | 92.6957% at native 30″ |
| Tokyo | 94.312°, 479 km outside | 94.312° |

The ice shelves cannot move c*: neither candidate hemisphere reaches south of 49.2°S, so the shelves only rescale every share near the maximum [R].

**Flatness, L50–59 (land) and L104–109 (people): wrong** [C, verified]. The ±3° box cannot see a second maximum 7° away, and the people section has no edge test at all.

| Case | Printed | Actual (±13° box) |
|---|---|---|
| Land, within 0.05 pp | up to 338 km, 88,498 km², no edge flag | up to 970 km, 137,000 km², in two pieces |
| Land, within 0.1 pp | 453 km, 188,031 km² (flagged) | 1,200 km, 376,000 km² |
| People, within 0.1 pp | up to 338 km | up to 1,040 km, six pieces |
| People, within 0.01 pp | 67 km | borderline: one lattice point 92 km away is 0.0099 pp below |

- The second land piece is 48,700 km² around the second maximum near 47.44N 2.36W. The script's own output contradicts the 338 km figure: Dumet is 811 km away and only 0.0345 pp below.
- The second people maximum is at 45.05N 6.70E, 0.057 pp below the best.
- The land figures for 0.001 and 0.01 pp are right (mine: 16 km / 989 km² and 79 km / 11,004 km² on a 0.1° lattice).

**Shelf overlap, L68–69: mislabelled** [C, verified]. The printed "overlap with the land polygons 41,096 km²" is Σ min(land, shelf), which measures shared boundary cells. The true overlap at 0.002° sampling is 63 km² (4,110 cells); Σ max(land + shelf − 1, 0) gives 66.5. The union used for the run is right to 93 km².

**Authalic variant, L84–91: misleading** [R+C, verified]. The printed "28.6 km from c*" is a relabelling of the same region, not a movement. See (f).

**Bisection, L120–137: fine** [R+C].
- It is bracketed (0.3213 / 0.5683) and the trail is monotone.
- My own search and bisection give 30.0891° (3,345.8 km) at 28.581N 100.464E, against yours of 30.0903° (3,345.9 km): one bisection step apart.
- At native 30″ with a hard edge, your final cap holds 0.499999.
- A 1e-5 error in the best share moves the radius by about 0.1 km, so "3,346 km" is computationally solid.
- The centre is flat to about 20 km: at r = 30.0977° your centre and mine are 19 km apart with shares equal to 1e-6.
- The competing maximum near 21.9N 99.6E is 0.36 pp lower at r = 30°.

**Small points** [C].
- "People in the land hemisphere" is 88.501% printed against 88.505% at native resolution; Nantes is 91.066% against 91.064%. Quote two decimals.
- Sphere against WGS84 geodesic distances: 757.4 / 757.1 km (Nantes), 810.6 / 810.5 km (Dumet), 772.5 / 769.7 km (Quah).
- KM = 111.195 km per degree is right.
- L90 uses R_KM where the authalic radius 6371.0072 belongs, overstating the area by 75 km².

## (e) confluence.py — count reproduced exactly

- **Count** [C]. 21,258 of 64,442 with Null island skipped; 21,259 if not, because (0,0) then counts. Of these, 5,860 are south of 60°S with the pole. My vertical-ray per-polygon test disagrees at 0 points, and no point lies in two polygons.
- **Against land10.npy** [C]. All 20,713 points whose four surrounding cells are full are land; none of the 42,670 with four empty cells is. Of the 1,057 mixed points, 544 are land, against 529 expected from mean coverage.
- **Nudge** [C]. The direction matters only at lon −180: nine points (latitudes −89 to −85, 66, 67, 68, 71) are land when tested just east of the cut and when tested at 179.999999999, and are lost only if nudged west off the map. Nudges up to 1e-5° change nothing else; a 1e-3° nudge (about 100 m) changes 10 points.
- **Poles** [R+C]. Correct for 10m. With `ne_50m_land`, L46 reports the South Pole as not land, because that polygon stops at −89.9989.
- **Shelves** [C]. 609 further points, none in both sets, so 21,867 in the union.
- **Definition** [C]. The count includes 147 points inside `ne_10m_lakes` polygons (Superior 9, Huron 7, Michigan 6 and so on) and excludes the Caspian, which is the single hole in the land file. Other scales give 21,224 (50m) and 21,324 (110m). So the count is exact for its definition, but the definition moves it by far more than a handful.

## (f) Conceptual points

**"Hemisphere" on the ellipsoid** [R+C, verified with PolyExact and with your own library].
- The three natural readings are: geodetic latitude as spherical (yours, i.e. the half of the ellipsoid whose normals lie within 90° of c); a plane through the Earth's centre; and the authalic sphere.
- They give the same family of regions: exactly so for the first two, and to 2e-6 for the authalic one. The best region and its share are therefore convention-free.
- The centre's latitude label is not: 40.82 (yours), 41.07–41.09 (authalic), 41.20–41.21 (central plane), a spread of 28–43 km.
- Comparisons with named points change with the reading, and the Dumet-versus-Nantes order flips:

| Reading | L(c*) − L(Nantes) | L(c*) − L(Dumet) | Dumet − Nantes |
|---|---|---|---|
| Geodetic as spherical (yours) | 0.0429 pp | 0.0345 pp | +0.0085 pp |
| Authalic | 0.0373 pp | 0.0389 pp | −0.0017 pp |
| Central plane | 0.0364 pp | 0.0417 pp | −0.0052 pp |

- With true ellipsoidal areas the share is 81.185%, not 81.219%, and the land area is 146.84 M km², not 146.74 M. This is common to all centres.

**Two land maxima** [C].
- The Nantes-region maximum (47.44N 2.36W, 81.188%) is second to c*. The margin is 0.031 pp at 10m, 0.035 at 50m, 0.023 at 110m, 0.031 with shelves and 0.030 with lake polygons removed.
- The margin is about 46,000 km². The identity of c* therefore rests on Natural Earth's coastline; I could not test another dataset.
- Tokyo is 93.75–94.79° from every centre within 0.01 pp of the best. It is only 12, 35 and 22 km outside for Nantes, Dumet and the second maximum. Some centres within 0.05 pp have Tokyo inside (minimum 89.47°).
- Within 0.02° of c* the share varies by 0.00009 pp, so the third decimal of c* means nothing.

**Half-population cap on the ellipsoid** [C]. As a geodesic circle on WGS84 the radius is 3,347.0 km at 28.67N 100.44E, against 3,346 km on your sphere. I searched only within 1.2° of the spherical optimum.

**Soft edge** [C]. Unbiased; see (c).

**Lakes** [C]. They count as land throughout: 1.26 M km² of lake polygons.

## Summary lists

**Would change a number**
1. `hemi_run.py` L50–59 and L104–109: the flatness distances and areas for land at 0.05 and 0.1 pp and for people at 0.1 pp are truncated by the ±3° box.
2. `hemi_run.py` L68–69: the shelf "overlap" is 63 km², not 41,096 km².
3. Ellipsoid convention:
   - L(c*) − L(Nantes), L(c*) − L(Dumet) and the Dumet/Nantes order depend on it;
   - so does the latitude of c*, by 28–43 km;
   - the L90 "28.6 km" is a relabelling;
   - the share is 81.18% with true areas.
4. Third decimals of the people-in-land-hemisphere shares; 3,346 against 3,347 km for the cap; 772 against 770 km to Quah's point.
5. Whole-degree count: must skip Null island; includes 147 lake points; excludes the Caspian.

**Fragile but did not matter**
- `best_cap` refines a single coarse maximum and loses near-ties below about 0.003 pp and sharp peaks; its edge flag is not returned.
- c* wins by only 0.03 pp over the Nantes-region maximum.
- People flatness at 0.01 pp is borderline (67 or 92 km).
- `raster.py` would silently cancel overlaps, clip longitudes and mis-fill uncut antimeridian edges.
- `popgrid.py` does not check the raster type and loads 7.4 GB.
- `confluence.py` gets the South Pole wrong with the 50m file.
- R_KM is used for ellipsoid areas.
- The exact float equality behind `same_point`.
- `test_hemi.py` passes but tests `best_cap` only against 4,000 random centres, and has no case for overlaps, the antimeridian, two near-equal maxima, popgrid or confluence.

**Fine**
- `raster.py` fill rules and all four grids.
- `popgrid.py` georeferencing and totals.
- `unit`, `area_weights`, `share`, `share_map`, the soft edge and float32.
- `Local` and the tangent grid.
- `best_cap` results on all the real inputs.
- Shelves not moving c*.
- The bisection and its radius.
- The Tokyo figure at c*.
- The km conversions.
- The confluence point test, nudge, poles (10m) and lon −180.

**Not checked**
- Another coastline dataset.
- The accuracy of GHS-POP itself.
- The unlisted scripts.
- `raster.py` and `popgrid.py` were not rerun on the real inputs; I compared their stored outputs with independent recomputations.

Everything is in `/tmp/rev_hemi`: scripts `s1`–`s20`, `revlib.py`, `revlib2.py`, the logs, and `run_out/log.txt` from my run of `hemi_run.py`.
