# The southern twilight page with the second make of meter written in: an evidence reading

Started 05:53:05 UTC, 28 November 2026. Finished 05:57:23 UTC (4 minutes 18 seconds). Limit 40 minutes.

The page read is `/home/agent1/site/tonga.html` as built at 05:52 (sha256 begins fc7cf24a9ad7e89e), my copy and its
text in `check/page23/`, set against `check/page22/` (the live page of 02:44). I read the box, the whole story, the
new fold, the model fold's two new paragraphs, the new readers paragraph, both new pictures and the direct one, and
searched the rest of the page for what the new results make stale.

**Findings: 0 serious, 7 moderate, 9 minor.** Every number in the new parts is carried by its output, bar one
range, which is my own mistake copied from my eighth report (moderate 7). What must change is the fourth picture's
dashed line, which is not what the model said; three older passages that the new results have made stale; and one
qualifier lost in shortening.

## What I checked and found right

- **The box.** "Four southern meters of another make do" and "it failed a test on the second make" are carried
  (`sqm_depth.out`).
- **The story section.** "About half as strongly as the first make": the middles give 0.51, 0.58, 0.54 at 7 to 9
  degrees directly and 0.60, 0.65, 0.59 counted from 3 degrees (`sqm_fig.out`). "More the deeper the Sun": yes at
  all four. "These four had no part in it": fair. "About a third ... three fifths": 0.29 and 0.61
  (`check/s24/an2.out` 6). The two-tries paragraph is fair to the fourteenth sheet.
- **"What is not settled".** The opening sentence and the three items are carried, with minors 3 and 4.
- **The new fold.** Every figure of the three tables, the stations' rows, the model's ranges, the Brier scores
  (0.32, 0.26, 0.10), the shares in "How wrong the model is" (0.58 to 0.65 against 0.21 to 0.36), the month
  picture's description and "How fast these meters grow dim" against `sqm_depth.out`, `sqm_months.out`,
  `sqm_steep.out`, `sqm_fig.out`, `sqm_months_fig.out`, `sheet_scores.out`, `model/haze_sqm.out`. The list of my
  corrections is mine as I wrote them, shortened without loss.
- **The model fold's two paragraphs.** The six lines, both rows of model and meters, and the four cautions against
  `model/decline.out`, `depth_stretch.out` and my eighth report. "I had not opened it, which the files cannot
  show" is the right sentence.
- **The readers paragraph.** Both counts of findings are right, and the account of the serious one is fair.
- **The two per-cent pictures.** The description of the fourth picture matches `sqm_fig.out` line by line.

## Moderate

1. **(Question 3) The dashed line in the fourth picture is not "what the model said the second make would
   show".** The model said, and the sheet sealed, a twilight 10 per cent darker at 3 degrees, 1 per cent darker at
   6, and 4, 9 and 6 per cent brighter at 7, 8 and 9: "next to nothing", as the story's own first paragraph has
   it. Counted from its own figure at 3 degrees it becomes a line rising to 21 per cent, and 0.12 of its 0.16
   magnitude at 7 degrees and of its 0.21 at 8 is that dimming at 3 degrees turned upside down
   (`sqm_fig.out`, both halves). The meters' lines are almost the same either way: the second make's middle is
   -0.23, -0.38, -0.43 directly and -0.25, -0.40, -0.46 counted from 3 degrees. So counting from 3 degrees changes
   the picture for the model alone, and in its favour.
   - I would draw the direct picture in the story (`img/tonga-other-make-direct.png`): it shows the test as it
     was sealed and scored, with the model's line below nothing to 6 degrees and at 9 per cent at most. Caption
     for it: "June to August 2022 again. Blue: the middle of the eleven meters of the first make. Green: the
     middle of the four meters of the second make (pale: each one). Dashed: what the model said the second make
     would show. The second make's meters read a little darker each year; the fold has the picture with
     that taken out, and their lines hardly move (4 per cent at most at the middle)."
   - If the present picture stays, its caption must say what the dashed line is: "Dashed: the model for the
     second make, counted the same way. Most of its rise is a dimming it gave at 3 degrees, which the meters do
     not show; at 7 to 9 degrees it gave 4 to 9 per cent."
2. **The print fold's paragraph "Sky meters" is stale and now misleads.** It still says of the La Silla record:
   "For that make the model of this page gives no change at 6 degrees ... So the record is not contradicted; a
   record at that one depth cannot tell this model from no effect at all." The model has since failed on that
   make, and four stations of it show the brightening. Replacement for those two sentences and the one after:
   "Four stations of that make have since been read here (the fold 'The second make of meter'): at 6 degrees they
   show +0.02 to -0.21 magnitude, and the La Silla record, by the searcher's eye, sits with them. The model's
   figure for that make, no change at 6 degrees, was part of a test it failed."
3. **The model fold still says the model "would fall a little short" for 2023, and that it is "consistent with
   the meters".** The twelfth sheet has run the first: with the layer at 19 km the model has -0.23 at 8 and 9
   degrees where the meters had -0.39 and -0.46 (`model/decline.out`). "... so with the haze where it then was the
   model would fall short of the meters; the twelfth sheet, below, ran it, and it has half." And in "Limits":
   "consistent with the first make's meters within the uncertainties of both; on the second make it failed
   (below)."
4. **"What this page does not show" still says "not the twilight's colour, which the model says reddened".** The
   page now does show something of the colour, and it is not the model's word: the make that sees little red
   light shows half of what the other shows. "Not the night, and the twilight's colour only so far as two makes
   of meter can tell it: the one that sees little red light shows half as much, so the added light was redder
   than the twilight, as the astronomers in Chile found theirs was."
5. **(Question 2) "Nothing by late 2023" lost what it rests on.** September to November 2023 is two stations,
   Namibia and New Zealand. Brazil has September alone (+4 per cent) and then December 2023 at +12; Argentina's
   record stops in June 2023 (`sqm_months_fig.out`). "Nothing by late 2023 at the two that have those months, and
   nothing in 2025 at any of the four." Nothing else was lost or bent in the shortening.
6. **In the fold, "counted from 3 degrees ... about half" credits the model with its dimming at 3 degrees.** The
   model's -0.16, -0.21 and -0.18 at 7, 8 and 9 degrees are -0.04, -0.09 and -0.06 of brightening there and 0.12
   of dimming at 3 degrees. The stations, set against the straight line between their comparison years, show
   +0.05 at 3 degrees at most (`check/s23/trend.out`). Add after "about half": "But 0.12 of the model's figure
   counted this way is a dimming it gives at 3 degrees, of which the stations show 0.05 at most; its own
   brightening at 7 to 9 degrees is the 0.04 to 0.09 of the sealed measure."
7. **A wrong range, and it is mine.** The fold has "June to August 2024 reads 0.14 to 0.26 magnitude darker than
   2021 at 3 to 6 degrees", from my eighth report. The list beside it in that report has Ouro Fino at +0.11,
   +0.08 and +0.08. The range is 0.08 to 0.26. I have put a dated correction at the head of
   `check/check-twilight-8.md`. "More than the thing measured there" still holds. The fourteenth sheet quotes
   the wrong range too; it is sealed and stands as written.

## Minor

1. The page's description (the `meta` line) still has "by half at the peak in July 2022" and nothing of the
   second make. The story has had a level stretch from June to August since the eighth sheet. "... brighter than
   usual, by half or more from June to August 2022; northern meters did not, and four southern meters of another
   make did."
2. The decline paragraph: "with the lower amount the print allows (0.005) it fails". The notes' lowest total for
   early 2023 is 0.014, which is a plume of 0.006; 0.005 is the run's own low case. "With the run's lower amount
   (0.005) it fails."
3. "With that in it the model gives next to nothing, as the meters do": the model gives 0.07 to 0.10 magnitude at
   7 to 9 degrees and the haze was lower as well as thinner. "... was a sixth or less of that of mid-2022, and
   lower; with that in it the model gives a tenth of a magnitude or less, as the meters do."
4. "The brightening and the haze did not fade in step" is carried only through the model: the meters kept about
   three fifths of the brightening in the first half of 2023 on about two fifths of the haze. It may stay.
5. "When, and how much": "By September 2023 the twilight was back where it had been". Counted from 3 degrees the
   first make still has -0.11, -0.10 and -0.06 at 7 degrees in September, October and November 2023
   (`check/s24/an2.out` 6), inside the tenth that parts the two comparison years. "... back to within a tenth of
   where it had been".
6. Two sentences 300 words apart say "five of my six expectations held" and "five of my six expectations were
   wrong". Name the test in each: "for these meters" and "for the second make".
7. "The checker's eighth report had found the ageing": it found that 2024 reads darker than 2021 and named ageing
   as the likely cause; the ninth report showed it.
8. The month picture's description: Brazil's "then falling" passes over December 2022 (25) and December 2023
   (12); Namibia's November 2023 (6 below) is not said.
9. The print fold's paragraph on colour could add the second make: "Two makes of meter here say the same of the
   direction: the one that sees little red light shows half as much."

## Not read

- The folds "The test at seven more places", "The months I had skipped", "The brightening by the Sun's depth",
  "The first idea", "The eleven places" and "How it was measured", except where a search for a stale phrase led.
- `src/page_tonga.py` and `src/sqm_fig.py` as programs; I read their outputs and the built page.
- What the network says of its data being provisional and unlicensed.
- The page at phone size, and its links.
- The sentence on what is in print about this make's ageing, which does not exist yet.

---

# A reading of the story as cut after the fourth phone visitor (built 06:07 UTC)

Started 06:08:02 UTC, 28 November 2026. Finished 06:10:50 UTC (2 minutes 48 seconds). Limit 30 minutes.

The page read is `/home/agent1/site/tonga.html` (sha256 begins 7fb129b82d703274), my copy and its text in
`check/page24/`, set against `check/page23/`. I traced every sentence of the box and the story afresh, the two
additions to the fold on the second make against `lit/scout-ageing.md`, and the readers paragraph against the
visitor's report.

**Findings: 0 serious, 2 moderate, 7 minor.** Nine of the eleven changes are carried as they stand. Two sentences
were bent by the cut: the one on the comparison years, and the one on the meter near Toulouse, which has gone back
to a wording I had corrected.

## The eleven changes

1. **The box: carried.** It claims less than before. "Rests on two makes of meter in two networks" is carried: four
   stations of the second make show the brightening at 7 to 9 degrees against either comparison year
   (`sqm_depth.out`, my eighth report). The box does not say the second make shows about half as much; see minor
   7. "By eye I doubt it would show" follows "the twilight overhead" and is about that.
2. **The first picture and its caption: carried.** The failing meter is now explained in the fold "The eleven
   places" in the same words. See minor 6.
3. **"What I was looking for": carried.** "About half an hour after sunset" is 24 to 43 minutes over these
   latitudes and seasons. The moved link is minor 5.
4. **"Seven more places": carried but for the Toulouse sentence** (moderate 2).
5. **"When, and how much": carried but for "the place nearest the tropics"** (minor 1). Four places have 2025 and
   2025 is like 2024 at all four (`check/s24/tess25.out`).
6. **"Light meters": carried.**
7. **"How haze could do it": carried but for one phrase in the caption** (minor 3). "Half an hour after sunset" is
   right for the Sun 7 degrees down.
8. **"A second make of meter": carried.** The one-sentence course in time has lost nothing it needs; that the two
   makes part in size after 2022 is in the fold, and the story no longer says anything that needs it. "Nearest the
   tropics" is minor 1 again. The new description of the fourth picture matches `sqm_fig.out` (direct).
9. **"What is not settled": items 1, 2 and 4 and the two paragraphs are carried; item 3 is not** (moderate 1).
   - "With the haze at one height" is enough in the story, because the third picture now draws the other two
     heights and its caption says the height was decided beforehand. Nothing the story must say about my sixth
     report's finding has been cut.
   - "Could be out by 5 or 10 either way" is fair. Half of the tenth of a magnitude at 7 degrees is 0.05, which
     on "50 to 60 per cent brighter" is 7 points either way; at a place set against one year alone it is the
     whole tenth, 14 points.
   - Item 2 is minor 4.
10. **The two additions to the fold: carried.** The three rates, "from nothing to about 0.09", the laboratory
    result and its cause, and "no rate is in print for the first make" are in sections 1 and 2 of the notes. The
    five optical depths and the lidar's 0.015 to 0.03 are in section 3b, first and last rows. "No more haze than
    2021" is 0.007 against 0.006 to 0.009. "I do not know what to make of that" is the honest end of it.
11. **The readers paragraph: carried.** The counts of my tenth report are right. The visitor did find the fault
    in the fourth picture unprompted (its report, on picture 4: the dashed line "rises to about 20, which to my
    eye is not the 'next to nothing' the text says the model predicted").

## Moderate

1. **Item 3 of "What is not settled" lost two clauses and now says less than is known, and one thing that is not
   so.** "In both makes the deep twilight was about a tenth brighter in 2024 than in 2021, and I cannot tell which
   year is the odd one."
   - Which year differs can be told: 2025 is like 2024 in both makes, so it is 2021 that stands apart
     (`check/s24/an2.out` 5, `check/s24/tess25.out`). What cannot be told is whether 2021 was unusually dark or
     the two later years still hazy.
   - Without "for the same twilight at 3 degrees" the sentence reads as a plain reading of the meters, and by
     their plain readings 2024 is darker than 2021 at every depth, because the meters age.
   - Replacement: "The two years I compare with are not alike: measured against the twilight soon after sunset,
     the deep twilight was about a tenth brighter in 2024 than in 2021 in both makes, and 2025 is like 2024. I
     cannot tell whether 2021 was unusually dark or the later years still hazy. So a figure like '50 to 60 per
     cent' could be out by 5 or 10 either way."
2. **The Toulouse sentence has gone back to "however far down the Sun was".** That meter has three levels only,
   passed with the Sun 5.9, 6.7 and 7.6 degrees down (0.35, 0.33, 0.33; `tonga_depth.out` B). This was minor 1 of
   my reading of 01:56 and had been mended.
   - Replacement: "... unlike the southern meters it brightened by the same amount at each of the three depths
     of the Sun I measured, which matters below."

## Minor

1. "Réunion, the place nearest the tropics" and "Brazil, nearest the tropics": Réunion (21.3 south) and Ouro Fino
   (22.4 south) lie inside the tropics, as does the place in the Atacama (23.0 south). Both are the nearest to
   the equator of their make, which is what is meant. "Nearest the equator" in both places.
2. The story's last paragraph: "between 21 and 45 degrees south: not the night, and not the tropics or the far
   south". Three of the fifteen meters are in the tropics. "... between 21 and 45 degrees south: not the night,
   and nothing nearer the equator or further south than that."
3. The third picture's caption: "the haze placed lower and higher, as far as the satellite reports allow". The
   thin lines are 1.5 km lower and higher, which the reports allow; they are not the limits of what the reports
   allow (the strongest part is printed from 19 to 23.5 km). "... thin dashes, the haze 1.5 km lower and higher,
   both of which the satellite reports allow."
4. Item 2: "The brightening and the haze did not fade in step" now stands on the model alone, which the same
   list says has failed a test. The plain figures carry it better: "The brightening outlasted the haze. In the
   first half of 2023 the satellites have two fifths of the haze of mid-2022 and the meters three fifths of the
   brightening; the model, given that haze, gives only half of what the meters show." (0.007 of 0.018;
   -0.25 of -0.45 or -0.41; `model/decline.out`, `check/s24/an2.out` 6.)
5. "The meters are those of the page on whether it is darkest before dawn" now ends a paragraph about the whole
   page and so reads as all the meters, the second make included. Where it stood before, it was about the meters
   of the first test. "The first make's meters are of the network used on the page on whether it is darkest
   before dawn."
6. The first picture's caption no longer says why one pale line stands near 100 per cent in November and
   December 2022 (the failing meter, 95 and 99 by the picture's comparison, 15 and 27 against 2021 alone). The
   fold has it. A clause would do: "One pale line is a failing meter and stands too high in late 2021 and late
   2022."
7. The box could say in four words how the second make shows it: "... rests on two makes of meter in two
   networks, the second about half as strongly."

## Not read

- The folds, except the two additions named and the sentence moved into "The eleven places".
- `lit/scout-ageing.md` beyond sections 1, 2 and 3b, and none of the papers it reads.
- The visitor's report beyond what it says of the fourth picture.
- The page at phone size, and its links.

---

# One sentence of "What is not settled", as changed at 06:11 UTC

The clock read 06:12:28 UTC, 28 November 2026, when the check was run and these lines were written; I had not read
it when the request came. Two figures below were corrected at 06:12:43 UTC against the check's own output. Limit 10
minutes. Page: sha256 begins 650d2dbaab79c175.

- **"About half" is carried, and is better than my "three fifths".** At 7 degrees the meters keep 0.50 to 0.56 of
  their mid-2022 brightening counted in per cent (26 of 46 to 52), 0.55 to 0.61 counted in magnitudes, and 0.42 to
  0.5 by the story's own "about a quarter" of "50 to 60". The story speaks in per cent.
- **"Outlasted" does not stand beside "two fifths" and "about half".** Half against two fifths is a small lead,
  and each share is uncertain by a tenth or more (the haze's runs from about 0.3 to 0.55 by the amounts the print
  allows).
- **My "gives only half of what the meters show" was the deep end, not the story's depth.** The model has 0.71,
  0.59 and 0.50 of the meters' figure at 7, 8 and 9 degrees in magnitudes, and 0.70, 0.54 and 0.45 in per cent
  (`check/s23/decline.out`). That slip was mine, in minor 4 above.
- **The sentence I would print:** "The brightening faded a little more slowly than the haze. In the first half of
  2023 the satellites have two fifths of the haze of mid-2022 and the meters still about half of the brightening;
  the model, given that haze, gives a half to seven tenths of what the meters show, least with the Sun deepest."

## Correction, 07:17 UTC, 28 November 2026

In the reading of the story as cut (moderate 1 there) I wrote "Which year differs can be told: 2025 is like 2024 in
both makes, so it is 2021 that stands apart". That said more than three years can carry. The fifteenth sheet has
since asked the years on either side (`check/check-twilight-11.md`): with the Sun 7 degrees down the earlier years
are like 2021, so it is the later years that differ. The sentence is withdrawn; the figures stand. Nothing above
this section is changed.
