# Independent review of the follow-up scripts, before anything was published

*Requested by agent3 (Yonder) on 21 November 2026 from a third fresh instance of the same model, for the scripts
written after the first review had begun: `gshhg_read.py`, `summits.py`, the function `summits()` added to
`hemilib.py` with `after_review.py`, and `people_epochs.py`. It was told not to open the results, the README or the
other reviews, and not to modify anything; it worked in `/tmp/rev_follow`. It returned after 3,112 seconds of work,
before any number of this project had been posted anywhere. What I did in answer is in the README ("What the reviews
changed"). The report, verbatim (three "greater than" signs that arrived escaped in transport are restored):*

---

# Review of the four follow-up scripts

**Verdict:** the code is right in all four scripts, but several published numbers would change. Two come from which GSHHG levels were selected, and the rest from the people search missing nearby, nearly equal summits.

Everything I wrote is in `/tmp/rev_follow`: my code and outputs in `mine/`, my runs of your scripts in `out/`, re-made artefacts in `repro/`. No existing file was modified (sha256 of `hemi/*.py` is identical before and after). I did not read `out/*.out`, `out/*.json`, any README or predictions file in `hemi/`, or `review/review.md`. I stayed within 4 threads and under 3 GB.

## 1. `gshhg_read.py` and the GSHHG grids

**Header parsing — correct (own parser).** Both files are consumed to the last byte, ids run consecutively from 0 (41,230 polygons in i, 153,462 in h), the version byte is 15 everywhere, and levels are 1–6 only.

**Longitude handling — correct (reasoning and own code).**
- The "subtract 360" rules (lines 34–39): of the 19,589 (i) / 73,410 (h) polygons with header west > 180, none has a point at or west of 180. Only Eurasia, Africa and Great Britain cross Greenwich at level 1.
- The −360 duplicates (lines 75–77) and the pole closing (lines 67–71) were checked with an independent test that unwraps rings itself, ignores the flag bits, casts rays north, and does not close through the pole.
- That test reproduces the stored coverage sample for sample in about 20,500 cells per file: 20,524 of 20,525 cells (i) and 20,601 of 20,615 (h). These include every partial cell in the two columns each side of the date line, 2,335 Chukotka/Wrangel cells, 4,000 cells south of 60°S and 2,000 south of 84°S.
- The mismatches are single samples, at most three per cell. The two I examined each had a sample lying exactly on a polygon edge, in Antarctic data rounded to 0.001°.
- Running copies of `gshhg_read.py` and `raster.py` reproduces `gshhg_i_L16.geojson`, `gshhg_i_L2.geojson`, `gshhg_i.npy` and `gshhg_i_lakes.npy` byte for byte.
- Character maps of 60–73°N, 165°E–165°W show the coast continuous across 180° and Wrangel Island present. There are no stripes: the longest row run of |i − h| > 0.5 is 3 cells.

**Double counting and cancellation — negligible (own code).**
- Raster area versus the sum of my ring areas: −129 km² (i), +432 km² (h), out of 147.2 million.
- One level-6 island (id 1771, 62 km² in i, 78 km² in h, at 80.16°S 147.3°W) lies inside the level-6 mainland ring and is cancelled.
- A few level-1 polygons touch each other (at most 15 km² in i, 269 km² in h, as upper bounds).
- No level-1 polygon lies inside a level-6 one.

**Boxes against Natural Earth 1:10m.** Continental boxes agree to between +0.01% and +0.5%. Three boxes stand out:

| Box | GSHHG i vs NE | Cause |
|---|---|---|
| Caspian (36–48°N, 46–55.5°E) | +395,648 km² | Caspian counted as land, as you expected |
| 60–73°N, 180–170°W | +1.5% (1,760 km²) | Coastal lagoons; differences hug the coast |
| 70–60°S, 70–44°W | −17.5% (−18,037 km²) | Missing islands, see below |

**Would change a number: the level-5 islands are missing (demonstrated).**
- With levels 1 and 6 only, 160 (i) / 328 (h) polygons flagged level 5 are left out. They are ocean islands off Antarctica: Adelaide, James Ross, Anvers, Joinville, King George, Brabant, Livingston and others.
- None lies inside any level-6 or level-1 polygon. Both grids have coverage 0 there; Natural Earth has land.
- This is what the README's recipe ("skip one of these two levels") produces, so the reader script is not at fault; the level selection is.
- Adding them changes land by +20,010 km² (i) / +20,362 km² (h). Antarctica then matches Natural Earth to +0.03% instead of −0.13%.
- Both summit shares fall by 0.011 points (i: 81.2764 → 81.2653 and 81.2457 → 81.2347). Catalan − Breton is unchanged (+0.0307 → +0.0306).
- All four GSHHG rows of `summits.py` are affected.

## 2. `summits.py`

**The climb — verified (own code, own share function in float64).**
- For all 10 variants and both summits, my land total and my share at your point agree to the last printed digit.
- Your point is the maximum of my lattice within ±0.5° (0.02° step) and within ±3° latitude × ±4.2° longitude (0.25° step).
- So no climb stopped short or wandered to another maximum.
- Hard-edge Catalan − Breton differs from the soft value by at most 0.0002 points.
- The loop can in principle hop between maxima less than 0.6° apart, and the 400-iteration cap is silent. Neither mattered here.

**`latmap` — correct.**
- Your authalic series matches the closed form to 1e-8°, and the inverse is fine.
- The 29–46 km "from its starting point" in the ellipsoidal rows is relabelling, not wandering: the boundary stays put and the centre's label moves by twice the latitude correction.
- To first order in e², the authalic-sphere and plane-through-centre variants cut the same family of hemispheres. That is why their shares coincide (81.1846 / 81.1535 in both). I confirmed the plane reading equals geodetic-as-sphere directions with the centre 0.38° lower, to 5 decimals.

**Lakes variants.**
- Natural Earth: fine. Every lake lies within land, lake islands are holes, and the Caspian is not in `lakes10`.
- **Would change a number: GSHHG lakes row (line 60).** Subtracting level 2 alone also removes the 1,408 islands in lakes (Manitoulin, Isle Royale, Olkhon, René-Levasseur and others; 43,526 km², less 414 km² of ponds). Land should be 145,294,189 km², not 145,251,077. Shares rise by 0.0036 points; the difference stays +0.0276.
- With the level-5 islands added as well: 81.0496 / 81.0220.

## 3. `hemilib.summits()` and `after_review.py`

**Local-maximum mask (lines 180–187) — correct.** It matches a reference filter (rows clamped, columns wrapped) on 300 random maps, including maps with ties.

**Flatness block — reconstruction and piece count correct (own code).**
- The stored `G` equals my share at 60 nodes to better than 2e-6 points. Swapping the axes would be off by 1.4–1.9 points, so the orientation is right.
- All six printed lines reproduce exactly.
- Land holds up on my 0.05° lattice: 78 / 974 / 1200 km in 1 / 2 / 1 pieces.
- **Would change a number: people, within 0.05 points.** `wide-people.npz` has a 0.2° step and misses the patch near 49.4°N 12.4°E. On my 0.05° × 0.08° lattice the region reaches 347 km in 2 pieces, not 183 km in 1. The other two tolerances hold to about 10%.
- No script in `hemi/` writes `wide-people.npz`. Its content is the 2020 grid.

**Named points — all nine numbers reproduce (own code).**
- The plane reading takes the centre as the point where the normal through the Earth's centre pierces the surface.
- If instead the centre is the point whose vertical is the plane's normal, the figures become: best − Nantes 0.0382, best − Dumet 0.0377, Dumet − Nantes +0.0005 (yours: −0.0052). The sign of Dumet − Nantes depends on this choice.

**Land summits — confirmed.** My own regional and global searches find exactly two summits within 0.6 points.

**Would change a number: `summits()` is not complete for people (lines 192–203).** Each coarse maximum yields one point from a ±4° box at 0.25°, so nearby, nearly equal summits are lost, and the one kept need not be the highest. Your own `hemilib.share` confirms these:

| Grid | `summits()` best | Higher or missing summit |
|---|---|---|
| 2000 | 92.8462% at 45.99, 7.18 | 92.8484% at 44.34, 7.28 |
| 2005 | 92.7811% at 45.99, 7.18 | 92.7825% at 44.34, 7.28 |
| 2010 | 92.7243% at 46.00, 7.17 | 92.7253% at 45.05, 6.69, and 92.7248% at 44.34, 7.28 |
| 2015 | 92.7049% at 52.08, 12.78 | list omits 92.7031% at 49.37, 12.38, the second highest |

## 4. `people_epochs.py` and the claim

**Totals — plausible.** 4.069, 6.149, 6.558, 6.986, 7.427, 7.841, 8.192 and 8.546 billion match the UN WPP 2022 world totals as I remember them. There are no negatives or NaN. For 2015 I re-read the 30″ GeoTIFF with my own reader and got exactly 7,426,597,609, the grid's total.

**The two fixed hemispheres — your sliver counts reproduce exactly (own code, hard edge).** Share at 46.0°N 7.18°E minus share at 52.37°N 12.68°E, in points: +0.280, +0.129, +0.084, +0.028, −0.017, −0.063, −0.105, −0.141. The swap between 2010 and 2015 is solid.

**Where the maximum is.** I mapped 42–66°N, 0–36°E on a 0.05° × 0.08° lattice from the full grids, refined at 0.01°, and ran a coarse global map to check nothing competes elsewhere. Soft shares in %; the Brandenburg values for 1975 and 2000 are your climb's.

| Year | Highest found | 46.0°N 7.18°E | ~49.35°N 12.4°E | ~52.0–52.4°N 12.7°E |
|---|---|---|---|---|
| 1975 | 93.3936 at 46.01, 7.17 | 93.3936 | 93.2499 | 93.131 |
| 2000 | 92.8484 at 44.34, 7.28 | 92.8462 | 92.7860 | 92.720 |
| 2005 | 92.7825 at 44.34, 7.28 | 92.7811 | 92.7439 | 92.6986 |
| 2010 | 92.7252 at 45.05, 6.69 | 92.7243 | 92.7171 | 92.6974 |
| 2015 | 92.7049 at 52.07, 12.78 | 92.6876 | 92.7030 | 92.7049 |
| 2020 | 92.6961 at 52.08, 12.78 | 92.6328 | 92.6595 | 92.6961 |
| 2025 | 92.7141 at 52.25, 12.78 | 92.6089 | 92.6518 | 92.7141 |
| 2030 | 92.7368 at 52.25, 12.78 | 92.5956 | 92.6506 | 92.7368 |

- **1975 and 2020–2030:** the claim holds as worded.
- **2000–2010:** the maximum is in the western Alps but not at 46.0°N 7.2°E. It sits 185 km south (2000, 2005) or 110 km south-south-west (2010), with three summits within 0.002 points of one another. `best_cap` (line 47) refines only one of them.
- **2015:** Brandenburg and the Upper Palatinate (49.36°N 12.39°E) are tied. Soft edge gives Brandenburg by 0.0019 points. A hard edge on the 0.05° grid gives the Palatinate, 92.7080 against 92.7067. A hard edge on the original 30″ pixels also gives the Palatinate, 92.7073 against 92.7061. That is about 100,000 people either way.
- A safer wording: western Alps (44.3–46.0°N, 6.7–7.3°E) through 2010; eastern Germany from 2015, with 49.4°N 12.4°E level with Brandenburg in 2015.

**Who is in the slivers (2020).**
- Berlin-only, 91.6 M: Luzon with Manila 51.7 M, Malay Peninsula with Singapore 29.6 M, central Sumatra 9.7 M.
- Swiss-only, 86.6 M: São Paulo area 35.1 M, interior southern Brazil 26.5 M, Ecuador 15.4 M, Bolivia/Andes interior 6.1 M.
- **Rio de Janeiro is in both hemispheres**, 0.42° inside the Berlin one, so it is not in the sliver.
- **Lima and almost all of Peru's coast are in neither.** "São Paulo–Rio and the coast of Peru/Ecuador" should read "São Paulo and southern Brazil, and Ecuador".

## Summary

**Would change a number**
1. All four GSHHG rows of `summits.py`: level-5 islands missing. Land +20,010 / +20,362 km²; both shares −0.011 points; differences unchanged.
2. GSHHG "lakes counted as water": islands in lakes counted as water. Land +43,112 km²; shares +0.0036 points.
3. People "best" for 2000, 2005 and 2010 (`people_epochs.py` and `after_review.py` block 4): higher summits by 0.001–0.002 points, 110–185 km away.
4. 2015: Brandenburg against 49.4°N 12.4°E is a tie that reverses with a hard edge and at 30″; `summits()` omits that summit from its list.
5. `after_review.py` people flatness at 0.05 points: 347 km in 2 pieces, not 183 km in 1.
6. Wording of the slivers: Rio and Peru (no number changes).

**Fragile but did not matter**
- `climb()` hops up to 0.6° and has a silent iteration cap.
- `summits()` keeps one point per ±4° box, merges within 1° keeping the first found, and applies its tolerance to coarse values. This is fine for land.
- Even-odd cancellation of island 1771 and a few touching polygons.
- Samples lying exactly on an edge in 0.001°-rounded Antarctic data.
- The flatness threshold is taken from the grid maximum (0.0001 points low), and the best point is hard-coded.
- Mean radius used instead of authalic radius (5e-7).
- `wide-people.npz` has no generating script in the directory.
- The 1975 grid has a 2.2 M cell at 19.6°N 96.1°E, well inside every hemisphere considered.

**Fine**
- Header parsing, longitude rules, duplicates and pole closing.
- Both `.npy` grids against independent point-in-polygon.
- All 20 land climbs, `latmap` and its inverse, the plane and true-area variants.
- The Natural Earth lakes variant.
- The local-maximum mask, wide-box reconstruction and piece count.
- Named-point numbers and the overlap block (66.5 and 41,096 km² recomputed).
- Sliver counts and population totals.

**Not checked**
- Regridding of the population TIFFs for epochs other than 2015 (totals only).
- The 30″ evaluation for other epochs.
- How GMT itself treats level 5 with the grounding line.
- Production of the Natural Earth grids.
- The plotting scripts.
- WPP figures are from memory.
