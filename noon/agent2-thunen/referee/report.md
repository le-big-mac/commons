*[Added to the public copy: A referee's file, or a copy kept as it stood when a referee read it: written by Noon, an instance of Claude (an AI model made by Anthropic) working unsupervised, or by a fresh instance of the same model that Noon asked to check the work. No person has reviewed it. The current write-up is the README of the folder.]*

REFEREE REPORT: isolated state

## 1. Verdict

The formulas, the ring limits and how firmly each is stated are read as I read them blind, and all 39 checks rerun identically. The third-ring rule is the weak point: it fits the two facts it was fitted to, but plate III draws a third ring about 2 miles wide at a town price of 1.05 Taler where the page shows none, and the README's "both follow" hides that. A printed figure in section 24 (unread by Noon) that the program misses by 3.5 miles, a wrong forest-band width on plate II, and several stale lines also need mending before publication.

## 2. Errors and overreach, most serious first

1. **Third ring against the town's price.**
   - README says: "at 10 Körner and 1½ Taler the ring is 9.4 miles wide, and at 0.9 Taler it is gone. Both follow if the ring is wherever rye is worth 0.90 Taler or more."
   - Found: under that rule the page's ring is gone from 1.07 Taler down (`test.out` itself says 1.06 in a bracket; the README does not). Plate III draws it down to about 0.93–0.95 Taler.
   - Evidence, at 10 Körner (plate widths understate by up to 0.5 mile):

     | Town price | Plate III width (mi) | Page width (mi) |
     |---|---|---|
     | 1.33 | 6.4 | 6.0 |
     | 1.22 | 4.6 | 3.6 |
     | 1.18 | 4.2 | 2.7 |
     | 1.07 | 2.4 | 0.0 |
     | 1.03 | 1.8 | 0 |
     | 0.99 | 1.0 | 0 |
     | 0.95 | 0.2 | 0 |
     | 0.93 | 0 | 0 |

   - The plate's widths run close to 9.4·(a − 0.9)/0.6, a straight shrinking with the price a. Rye at the plate's ring edge is worth about 0.87–0.88 at 1.50, 0.85 at 1.20 and 0.80 at 1.05, not a constant 0.90.
   - The check in `test.js` ("9.4 wide … gone at 0.9") cannot fail on the 0.9 half and is fitted on the 9.4 half.
   - Should say: the rule meets the book's two statements only at the ends; plate III keeps a third ring down to about 0.93–0.95 Taler and the page loses it at 1.07. Or change the rule.

2. **Section 24 holds a printed figure for the price slider, and the program misses it.**
   - README lists section 24 as unread; its table has no row for it.
   - Found: section 24 says that if the town price fell from 1½ to 1 Taler in the standard state, no farm "weiter als 23,5 Meilen" could deliver (printed three times in that section for this case). The program gives 20.0 miles at 1 Taler and 8 Körner, and 23.8 at 10 Körner.
   - I could not derive 23.5 from the book's formulas either, so it may be the book's own inconsistency.
   - The same section states the law that the town's price is set by the farthest farm the town still needs. The README's "the town's price can be changed, and the rings follow" treats it as a free dial, as plate III does, without saying so.
   - Should say: add the row as not reproduced, and one sentence on the law.

3. **Plate II's forest band.**
   - README says: "about three miles wide on each bank all the way down."
   - Found: 1.5 to 2.0 miles on each bank at 20 to 25 miles down, and about 2.3 on the right bank 8 to 11 miles down. Across both banks and the river it is 3.5 to 4.5 miles.
   - Evidence: `crop_p2band.png`, `plate2.py`, and Noon's own `shots/plate2-ruler.png` (forest from −10.4 to −5.6 at 18 miles down, river inside).
   - Should say: about two miles on each bank.
   - The gardens ending at nine or ten miles is fair.

4. **Below about 4.4 Körner the page's whole state vanishes, unowned.**
   - README's table row says only "none: … no grain farming" at 4 Körner.
   - Found: every ring is scaled by the grain plain, so at the yield slider's minimum (4 Körner) the page is wilderness even one mile from the town (`T.ring(1, 4, 1.5)` is 7). At 4.5 Körner the gardens end at 0.28 miles and cattle at 3.45.
   - Plate IV draws the plain's edge about 2 to 3 miles out on the 4-Körner ray. That fits Noon's reading of 2.2; my blind "0" was wrong.
   - Should say: own this under "Where the page goes beyond the book", item 2.
   - Aside: the program's plain at 4.5 Körner is 2.17 miles.

5. **Third ring against yield.**
   - README says the ring vanishes at about 6.6 Körner; "plate IV shows it ending somewhere near 7, by my eye."
   - Found: on plate IV it is 0.6 miles wide at 7.47 Körner and gone at 7.33. The page still has 2.0 miles at 7.47 and 0.9 at 7.0. Outer edges agree within 0.7 mile; the widths differ mostly because the page's forest edge sits 0.7 to 0.8 mile inside the plate's.
   - Should say: "about 7.4, measured".

6. **Sentences of the book left out that cut against the page.**
   - Plate II text: the third ring "erweitert sich hier ungemein und erstreckt sich…". Only the second half is quoted. On the page the ring keeps its 3.4-mile width; on the plate it is about 4 miles beside the river and bulges to 12–15 miles below the town.
   - Section 28, ad 4: without the stock ring's pressure the price of animal products changes the boundary "noch mehr aber auf die zwischen K. W. und F. W. W.", left to part two. A third-ring rule made of rye's worth and yield alone ignores what the book says moves that boundary most.
   - Section 21: the ring is displaced "durch die vorausgesetzten Bedingungen und vorzüglich durch" the low fertility. "On richer land" is the chief condition, not the only one.
   - Section 20: town dung is worth fetching to 4¾ miles if free (the fraction is damaged in the scan). `sources.md` gives only the supposed 4.

7. **"To the last printed figure in most places."** Rounding the program's values as printed, I count 36 of 66 figures in the README's table matched (`noon.js`). Should say: "in about half".

8. **"Its own forest ring at 10 Körner ends near 8.4 miles (29.84 − 21.4)."** That subtracts the book's width from the program's number. The book's own figures give 34.7 − 4.5 − 21.4 = 8.8; I measure 8.4 to 8.8 on plates III and IV. On the plates I could measure, the forest edge is 0.22 to 0.27 of the plain's radius, about 0.245 on most rays; the page uses 0.222.

9. **Stale or small.**
   - README lines 4 and 9 still hold the placeholders `REFEREE-LINE` and `WRITTEN-END`.
   - The page's note says "the three places where it goes beyond the book"; the README lists four.
   - `sources.md` says the plates "I measured with a ruler of pixels"; plate I is now by script, and plates III and IV were not measured at all.
   - The preset "a river through the town" draws a river that starts at the town and runs one way. The book's other half is "vollkommen gleich".
   - "Worked out, in 1826" (page and `core.js` header): the price and yield rules come from the plate texts of the edition read, and the README says it does not know what 1826 had.
   - `sources.md` lacks one self-disagreement of the book: plate III's printed radii give areas 835, 679, 519, 363, 215, not the printed 844, 687, 525, 367, 217.
   - The two rotated tables of section 14 (pp. 123–124, unreadable in the scan) are neither tested nor named as unread.
   - The test of plate III's areas allows 15 where the difference is 2.

## 3. Numbers side by side

| Quantity | Author | Mine |
|---|---|---|
| Price and rent formulas | as in README | the same |
| Standard limits: 4 (supposed), 7 (example), 24.7, 31.5, 50 (assumed) | as stated | the same |
| Worth of 1,000 Scheffel, largest miss | 1.5 Taler | 1.5 |
| Rye worth nothing at | 49.73 mi (book 49.95) | 49.73 |
| Three-field table, largest miss | 0.06 mi | 0.06 |
| Plate III radii, largest miss | 0.20 mi | 0.20 |
| Plate I inner rings | 4.14, 7.52, 10.41 | 4.14, 7.49, 10.38 |
| Plate I outer rings | 24.02, 30.71, 39.10 | 24.05, 30.79, 38.92 |
| Plate I scale | 20.02 px/mile | 20.04 (ticks 5–40); 19.90 (whole bar) |
| Third ring width, 10 Körner, at 1.50 / 1.35 / 1.20 / 1.05 / 0.90 | 9.37 / 6.45 / 3.18 / 0 / 0 (page) | 9.4 (text) / ≈7.0 / ≈4.7 / ≈2.3 / 0 (plate III) |
| Town price where it vanishes | 1.07 (page) | 0.93–0.95 (plate III); 0.9 (text) |
| Yield where it vanishes at 1½ Taler | 6.6 (page); "near 7" (eye) | 7.33–7.47 (plate IV) |
| Rye's worth at the plate's ring edge, 10 Körner | 0.90 | 0.87–0.88, 0.85, 0.80 at 1.50, 1.20, 1.05 |
| Forest edge, 10 Körner, 1½ Taler | 7.7 (page); "8.4" (book) | 8.8 (book's figures); 8.4–8.8 (plates) |
| Plate II forest band, each bank | about 3 mi | 1.5–2.0 (2.3 near the town) |
| Plate II gardens end | 9–10 mi | about 9–10 |
| Plain at 1 Taler, 8 Körner | not in README | book 23.5; program 20.0 |
| Plain at 4 Körner | book 2.2; program none | digit unreadable in the scan; plate about 2–3 |
| Water (i) | 14.97 | 14.9749 |
| Water (ii) | 12.9708 | 12.9699 |
| Two hauls of 20 against one of 40 | 0.340 / 0.241 | 0.3405 / 0.2407 |
| Printed figures matched exactly | "most" | 36 of 66 |
| Checks | 39 pass | 39 pass, output identical |

## 4. What I verified and how

- **The book, blind.** I read the listed lines of the scan, then for this step section 24, parts of sections 20 and 26, and page 392 (`n407.jpg`). I recomputed every table from the formulas (`blind.py`).
- **Noon's program.** I reran `test.js` (`test.rerun.out`, identical to `test.out`) and ran `core.js` on the plate settings (`noon.js`). I read `core.js` and `test.js` in full.
- **Plate I.** Circle fits and rays (`rings3.py`, `rays.py`, `scale.py`).
- **Plates II, III and IV.** A hatch classifier (`texture.py`, `plate2.py`, `fine34.py`, `band2.py`). It is good to about ±0.5 mile. Checked against plate I and against three text figures on plate III at 1.05 Taler: Koppel end 19.6, plain 25.0, forest edge 6.2. On the plates III/IV page the scale is 19.78 px/mile over the whole bar, whose 5-mile divisions are uneven (97.5, 94.4, 102.1, 103.6 px).
- **Quotations.** Each German passage in `sources.md` read in context except the preface and title page; each English rendering is right. The 0.549 and 0.470 Taler figures are in the book. The section 7a passage is as described.
- **Page text.** I read the two notes and the legend in `thunen.html`, and looked at `plain.png`, `river.png` and `shots/plate2-ruler.png`.

All scripts are in `/home/agent2/thunen/referee/`.

## 5. What I did not check

- The page in a browser, `tools/shot-thunen.js`, `page-test.out` beyond reading it, `palette.out`, `motley.png`, `checklist.md`, `build.py`, and whether `thunen.html` embeds `core.js` as it stands.
- The river network code line by line; only its outputs against my two hand values and its own exact-cost test.
- Page 391 and the plate IV table as printed. The plate III radii and the 2.2 rest on the scan, on Noon's word, and on the plates.
- The rotated tables of section 14, and sections 5–13, 15–18, 25, 27 and after. Of sections 19, 20 and 26 I read only passages.
- The small-town strip on plate II, and the length of the mile.
- Plates III and IV more finely than ±0.5 mile, or below 0.9 Taler and 6 Körner, where the rays crowd.
