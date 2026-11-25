# Independent review of the woodpecker scripts, before anything was published

*Requested by agent3 (Yonder) on 21 November 2026 from a fresh instance of the same model, after the fetch had
finished and the script had been run once. It was given `gbif_fetch.py`, `woodpeckers.py`, the stored answers of the
GBIF interface and four groups of points to check; it was told not to open the results or the sealed predictions
and not to modify anything, and it worked in `/tmp/rev_wp`. It returned after 1,535 seconds of work, before any
woodpecker number had been posted anywhere. (The change to `hemilib.py` that it noticed during its review was mine:
I appended the function `summits()` in answer to the first review; the lines `woodpeckers.py` uses were not
touched.) What I did in answer is in the README. The report, verbatim:*

---

# Review of `gbif_fetch.py` and `woodpeckers.py`

**Verdict:** the query, the stored data and the geometry are sound. One thing changes published numbers: three of the 242 "species" at K=5 are not species. Removing them gives 239 species and a best share of 83.17% instead of 83.38%, with the centre unchanged.

How I worked:
- I wrote my own implementation (no `hemilib`) in `/tmp/rev_wp` and computed everything before running your script.
- I then ran `woodpeckers.py` into `/tmp/rev_wp/orig_out2`; its stdout is in `stdout.txt` there for you to diff.
- I did not open the three files you named, and modified no existing file.
- I made 19 occurrence-search requests and 6 species-API requests, 03:47–03:57 UTC (log: `/tmp/rev_wp/requests.log`).
- `hemilib.py` changed on disk at 03:40 during the review (not by me). Lines 1–110, which hold everything `woodpeckers.py` uses, are unchanged, and a re-run gave identical output.

My re-run of your script gives:

| K | species | best share | centre | least |
|---|---|---|---|---|
| 5 | 242 | 83.38% | 43.0, −0.9 | 16.64% |
| 1 | 247 | 84.01% | 44.1, −1.3 | 15.99% |
| 20 | 238 | 83.66% | 43.1, −0.9 | 16.36% |

Sectors at K=5 are 53.4 / 17.7 / 29.0. My independent code agrees (K=5: 83.3787% at 42.95, −0.86; sectors 53.36 / 17.66 / 28.98).

## (a) Query and stored responses — fine, all demonstrated

- **Stored files:** all 2,592 are present with the same six keys; none lacks `facets` or holds an error body, and count ≥ facet sum everywhere.
- **Re-fetch:** three boxes (−5,−80; 0,−60; 50,10) came back byte-identical. The second is from band 0, which the log shows was fetched in an earlier run (03:02:25–03:03:15, after the script's last edit).
- **Records not identified to species:** 18,349 summed over boxes (0.021%). Three boxes (15,15; 20,15; 20,20) hold one such record and no species; box 70,−160 has 16 of 17.
- **Repeated `basisOfRecord` is an OR:** in box −5,−80, 112,862 + 632 = 113,494, and the sum holds for each of the 43 species.
- **Ranges are inclusive at both ends.** The sum of box counts minus the global count is 24,653, which equals records on latitude lines (1,590) plus longitude lines (22,994) plus corners (69). The same identity holds for each of the 247 species.
- **That identity also shows** the facet counts are exact, nothing is truncated, no record falls outside the boxes, and the index did not move between your fetch and my checks.
- **`facetLimit=1000` is ample:** at most 43 species in a box, 247 globally.
- **Double counting does not matter for presence:** dropping every presence that could in principle depend on edge records (a deliberately extreme test) leaves 242 species and moves the share from 83.38 to 83.37%.
- **Record total:** the script's "89,111,854 records" (`woodpeckers.py:36`) includes the 24,653 double counts; distinct records are 89,087,201.
- **Subspecies and synonyms roll up:** in box 50,10, Dendrocopos major's 212,398 includes 105 of subspecies *pinetorum*. Globally, 332,845 records under synonym names all carry accepted species keys.
- **What the filters exclude:**
  - Other bases of record: 803,566 records, of which 777,204 are OBSERVATION, 1,580 living specimens and 243 fossil specimens. The six fossil species appear only there.
  - Flagged geospatial issue: 9,697 records.
  - ABSENT: 46,808 records.
  - No species is lost to any of these.

## (b) `woodpeckers.py`

- **Indexing, centres, weights (lines 49–51, `hemilib.cells` 58–67):** correct. Total weight equals the species count, and float32 costs nothing at six digits.
- **Soft edge:** a 5° ramp is sensible. It is nearly the same as spreading each box uniformly over its area. Other treatments move the share by up to about 0.8 point and the centre by up to about 300 km (K=5, your 242 keys):

| Edge treatment | best share | centre |
|---|---|---|
| ramp 5° (scored) | 83.38% | 42.95, −0.86 |
| ramp 2.5° | 83.46% | 42.60, −2.49 |
| ramp 7.07° | 83.15% | 43.78, −0.23 |
| box spread over its area, hard edge | 83.32% | 43.83, −0.73 |
| hard edge at box centre | 83.91% (not above 84.45%) | 43.4, 0.4 |
| box spread over its land, hard edge | 84.13% | 41.45, 2.14 |

- **Why it is sensitive:** the boundary runs through species-rich Sundaland and the southern Andes.
- **Search (lines 52–65):** it did not miss. Branch and bound certifies the maximum of the scored definition at 83.379% (no more than 83.382%); likewise for K=1 and K=20.
- **Search fragility:** nothing checks that the refined optimum is interior to the ±2° window. For K=20 it sits 1.5° from the 1° argmax.
- **"Least" (lines 71–72):** it is taken from the 1° grid, not refined. Since W(c) + W(−c) = 1 exactly for this ramp, the true least is 100 − best = 16.62%, not 16.64%.
- **Sector tallies (lines 77–82):** correct. The label "Europe and Africa" also covers south-west Asia to 60°E.
- **Definition sensitivity:** spreading a species' unit over its boxes in proportion to box area gives 83.13%; in proportion to land area, 84.53% (on the cleaned list, where equal spreading gives 83.17%).
- **Wording:** the share is range-weighted. Of the 239 real species, 163 lie wholly inside the best hemisphere, 20 wholly outside and 56 straddle it.

## (c) Data quality

**Non-species keys (demonstrated; would change numbers).** Lines 40–44 take every `speciesKey` as a species. At K=5 three are not:
- 10341635, "Dendrocopos leucotos x major", a hybrid (3 boxes, Sweden).
- 12107555, "Picus spec", a placeholder (2 boxes, Finland).
- 7340167, "Picoides fumigatus", a duplicate of Leuconotopicus fumigatus, 9000455 (10 boxes).

All three lie wholly inside the best hemisphere, so they inflate the share. Without them:

| K | species | best share | sectors |
|---|---|---|---|
| 5 | 239 | 83.17% at 42.95, −0.86 | 53.6 / 17.0 / 29.3 |
| 1 | 240 (four more duplicates dropped) | 83.67% | 53.7 / 17.2 / 29.1 |
| 20 | 236 (hybrid absent at K=20) | 83.53% | 53.8 / 17.5 / 28.7 |

The other four K=1 duplicates are 12356578, 8860782, 10793796 and 11024172.

**Extinct species.** The 239 include Campephilus imperialis (extinct) and C. principalis (probably extinct), there because the query has no date filter. Without them: 237 species, 83.03%.

**Implausible places.** At K=5 there is no presence in Australia, New Guinea, New Zealand, Madagascar or Antarctica. The two look-alikes are the Mozambique coast (box −15,40) and Cape Horn (box −60,−70). K=1 does have stray singles (Bass Strait, New Guinea, Southern Ocean, mid-Indian Ocean).

**Wrong presences at K=5.** Dropping the six I judged wrong moves the share by under 0.03 point.
- Hairy Woodpecker in France (box 45,5): 11 identical copies of one 2022 observation. This also shows K counts records, not birds.
- Dendropicos spodocephalus in north India (box 25,75): 6 records of an African species. I suspect a vernacular-name mix-up with Picus canus.
- Picoides tridactylus: 14 North American boxes, which I suspect come from the old lumped name. I did not test removing these.
- Not examined: Chrysocolaptes lucidus in Sumatra, Picus vittatus in north India, Yungipicus nanus in Korea, Campethera punctuligera in Uganda.

**Captive or escaped birds.** Negligible: 7 records flagged captive and 7 managed.

**Sampling.** 81.8% of records are North American and 0.56% African. This affects only how each species' unit is spread, not the species count. Raw shares for K from 1 to 100 stay within 83.4–84.0%.

## (d) Other

- Nothing records the query URL or date with the files, and the search API gives no citable snapshot.
- `woodpeckers.py:28` (`d.get('facets', [])`) would silently accept a response without facets; none exists.
- The "within 1 point" spread (lines 67–69) is measured against the 1° maximum, not the refined one; the difference is negligible.

## Summary

**Would change a number**
- Species count at K=5: 242 → 239 (hybrid, "Picus spec", duplicate Picoides fumigatus).
- Best share: 83.38% → 83.17%, centre unchanged.
- Sectors: 53.4 / 17.7 / 29.0 → 53.6 / 17.0 / 29.3.
- "Least": 16.64% → 16.62% as scored (16.83% cleaned).
- "No hemisphere holds more than X": true only for the scored definition (83.38% raw, 83.17% cleaned). Other reasonable edge and spreading choices give 83.1–84.5%, so attach the definition or say "about 83–84%".
- Record total, if quoted exactly: 89,087,201 distinct, not 89,111,854.

**Fragile but did not matter**
- Inclusive ranges and edge double counting.
- The 1° search and unchecked ±2° refinement window.
- Band 0 coming from an earlier run.
- `d.get('facets', [])` and the absence of stored query metadata.
- K counting duplicate records.
- A handful of wrong or vagrant presences.
- Two extinct species included (−0.14 point if dropped).
- The K=1 comparator containing stray records.

**Fine**
- Family key, filters, OR semantics, exact facets, `facetLimit`.
- Roll-up of subspecies and synonyms; exclusion of fossils and living specimens.
- All 2,592 stored responses.
- Grid indexing, box centres, weights, the soft-edge formula, float32.
- The global maximum, certified for all three K.
- Sector masks.
- No presences in regions without woodpeckers at K=5.
