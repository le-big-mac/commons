# The southern twilight page with the Sun's depth and the model written in: an evidence reading

Started 01:44:17 UTC, 28 November 2026. Finished 01:52:39 UTC (8 minutes 22 seconds). Limit 25 minutes.

The page read is `/home/agent1/site/tonga.html` as rebuilt at 01:43 (sha256 begins e9c8efc88c1e25ba), my copy and its
text in `check/page20/`, set against `check/page17/`. New programs of mine: `check/m19/pattern.py` (every run made so
far, summed with the blind weights) and `check/m19/where.py` (where the added light is first scattered).

**Findings: 0 serious, 5 moderate, 14 minor.** The new section keeps to the limits of my sixth report in its words.
Where it goes past them is in what the reader sees first and last: the picture shows the one case that fits and its
caption calls the line trustworthy; the one published record of another meter has left the story; and two flat
sentences ("It is also what the haze should do", "Its pattern is firm") say a little more than runs of one model
by its author can.

## What I checked and found right

- Every number in the picture's description, the caption's lines and both new tables against `depth.out`,
  `model/haze_central.out`, `model/haze_sens.out`, `model/haze_bands.out` (rewritten at 01:40 with my SQM reading) and
  `m19/bands.out`. The per-cent figures follow from the magnitudes. The picture draws what its program says.
- The story's new sentence on the northern meters ("no northern meter that has every month brightens for more than
  three months running; every southern one did for five or more") against `between_look.out` part J: the twenty
  northern have runs of 0 to 3 apart from the ring-road meter (5), which is one of the four the story sets aside;
  the eleven southern have 5 to 19.
- The fold on the Sun's depth against my fifth report: the level stretch from 10 degrees, the two stages by half
  degrees, ten places of eleven at 3 degrees, the comparison years, the other stretches. The four added lines:
  one not met, two failed, one void (`amendment-depth-scored.md`), as the page says.
- The fold on the model against my sixth: the six verdicts, the Brier score, what the haze does by order and by
  colour, the corrected input, the sentence on the height, `deep_check.out` (-0.97 and -0.95 at 10 and 11 degrees
  from separate runs), "consistent with the meters within the uncertainties of both".
- The print fold's quotations and the Pinatubo figures against the notes of the second search and its scored sheet.
- "With the Sun 3 degrees down the two cancel": the nine cases run so far stand between -0.03 and +0.10 there
  (`m19/pattern.out`).

## Moderate

1. **The picture shows the one case that fits, and its caption says the line can be trusted.** The dashed line is
   the model with the layer at 21 km. With the layer at 19.5 or 22.5 km the same line would end at 75 or 147 per
   cent at 9 degrees, where the meters have 109, and at 4 degrees it would stand at 1 or 19 per cent, where the
   meters have 16 (`m19/pattern.out`). "Drawn as far as it can be trusted" tells the reader the line is good to 9
   degrees; what is good to 9 degrees is its sums, not its height on the chart. The story's own next paragraph says
   so, but a picture is read alone. Replacement caption: "Dashed: a model of the twilight with the volcano's haze
   in it, at the height fixed beforehand, drawn to 9 degrees, beyond which its sums are rough. With the haze 1.5 km
   lower or higher the dashed line ends at 75 or 147 per cent." Better still, draw those two lines thin.
2. **(Question 5) Dropping the other make's record from the story hides a doubt a reader should see.** It is the
   only published record of a sky meter in these years and latitudes, and its authors report no trend. What
   reconciles it with this page is the model's split between red and blue, and nothing outside the model has shown
   the blue half of that split. The model's own figure for that make at 6 degrees runs from +0.07 to -0.10 with the
   layer's height (`m19/z195.out`), and the searcher's reading of the plotted points is 0.05 to 0.15 brighter. The
   doubt is smaller than it was; it is not gone. A third item, of two sentences: "The one published record nearby,
   from a sky meter of another make, reports no trend. In the model that make, which sees little red light, should
   show next to nothing where its record is taken; that is the model's word, and I found it after the fact."
3. **"It is also what the haze should do" is the model's word, said as a fact.** One model, by the page's author,
   run in one night, says so; one measured twilight after Pinatubo, in red light and away from the zenith, has the
   same growth with depth. Replacement: "A model says it is also what the haze does."
4. **(Question 6) "Its pattern is firm" is carried by the runs so far, and by no others yet.** In all nine cases
   (three amounts at each of three heights) the model stands within 0.10 of nothing at 3 degrees, is brighter at
   every step from 4 to 9 degrees, and has the meters' slow step from 4 to 5 (`m19/pattern.out`). But the droplets'
   size and the comparison years' haze, which set the balance of red and blue, have not been varied, and five runs
   are still going. Until they are in: "Its pattern has been the same in every run so far; its size has not." If
   they keep the pattern, "firm" stands.
5. **The fold's list of checks leaves out the one that did not come out clean.** My own Monte Carlo for light
   scattered three times and more agrees with the run at two cases and is a quarter lower at a third (525 nm, 7
   degrees, two runs of mine); I read that as my estimator's fault, and it is not settled (`m19/orders_*.out`,
   `m19/sep_525_7.out`). Add after the list: "Its own Monte Carlo for the higher orders agrees at two cases and
   comes out a quarter lower at a third, which it takes for its own estimator's fault but has not settled."

## Minor

1. The box: "gives the same pattern" has nothing in the box to refer to. "... and a model of the twilight with that
   haze in it brightens it in the same way: not at all soon after sunset, more and more as the Sun sinks."
2. "A few hundred kilometres towards the Sun" is checked and may stand. By a Monte Carlo of my own, the
   twice-scattered light that the layer adds is first scattered, at the middle, 140 km towards the Sun with the Sun
   4 degrees down (two thirds of it between 40 and 390 km; 575 nm), 350 km at 6 degrees (250 to 610; 675 nm) and
   630 km at 9 degrees (570 to 755), all of it at 19 to 23 km. It is turned there through 7 to 37 degrees and
   scattered again 7, 8 and 12 km above the meter at the middle (`m19/where_575_4.out`, `m19/where_675_6.out`,
   `m19/where_675_9.out`). The same runs give the share of the added light first scattered at 16 to 26 km as 1.15,
   1.04 and 1.10, where `model/haze_where.out` has 1.15, 1.06 and 1.07. "Half the distance to the terminator" (222,
   334, 500 km) is right at 6 degrees, long at 4 and short at 9, because air at 21 km leaves the Earth's shadow
   only 484 km out at 9 degrees and is sunlit overhead at 4. "Throw it forward" and "the dark air above the
   meter" are right.
3. "It is off by up to a third of a magnitude" (story) and "too bright by up to 0.33" (fold) are the figure at 10
   degrees, where the page says the model is rough. To 9 degrees it is 0.18 too bright and 0.19 too faint
   (`model/haze_sens.out`, last column). "By up to a fifth of a magnitude" in the story; "by up to 0.18 (0.33 at
   10 degrees, where the sums are rough)" in the fold.
4. "Finer grids move the twice-scattered light with the layer by less than one part in a thousand": by 1.1 and 1.5
   parts in a thousand at my two cases; the ratio with and without by 0.3 and 1.2. "By one or two parts in a
   thousand."
5. "A few paths in a hundred thousand carry much of it" was not measured. What was: "five of its hundred batches
   of 20,000 paths carry 28 in 100 of it at 10 degrees and 42 at 11" (`m19/tails.out`).
6. "Every figure within 0.02 and every verdict the same": two cells at 9 degrees are outside (Mount Martha -0.75
   against -0.80; Coonabarabran, where my looser rule gives a figure and the page's none). "Every figure but two
   within 0.02."
7. "Tried first with no eruption" quotes the sealed run's own figures without the plume. The trial before the
   sheet gave 1.17, 2.51, 3.82, 5.12, 6.33, 7.36, 8.23 (`model/clear_troplo.out`). Say which is which.
8. "Beyond 8 degrees it owes something to a choice" understates. The settings tried spread over 0.3 to 0.9
   magnitude from 8 to 10 degrees and the best was kept: "from 8 degrees on it is a fit".
9. "The other lines are runs made afterwards": the two other amounts were part of the sealed run; only the two
   heights came afterwards.
10. "Give the same change as the sealed run at five cases": within their errors at four, 1.5 errors apart at the
    fifth (`model/brute.out`).
11. "The meters stop counting at about 60,000 a second (the 50,000 ... is a mark the firmware writes)": the largest
    count in any file is 63,600 to 64,800 and by day the files hold 50,000 (`dpan18.out` D). The firmware
    is an inference: "which I take for a mark the firmware writes".
12. "Beyond 9 degrees evening and morning part": from 9 degrees. And "the reading fitted June to August and not the
    other seasons": what I found is that it gives a different share from each stretch (0.45 at 7 degrees from June
    to August, 0.60 to 0.63 from the other three).
13. The readers' fold: "its third to sixth reports" for the months between, the depth and the model: those are
    the fourth to sixth; the third is a reading of the page. The print fold's "+0.01 magnitude" for the other make is the central height's figure; with the layer
    lower or higher it is +0.07 or -0.10.
14. "Scattered again in the low air over the observer": 8 km up with the Sun 4 to 6 degrees down, 14 km at 9
    (`model/haze_where.out`). "Since the twilight fades by the same factor for every degree": nearly the same, from
    5 to 8 degrees (1.2 to 1.4 magnitudes a degree).

## Not checked

- The five runs still going, and so any row they will add.
- The quotations in the print fold against the papers themselves; I set them against the searchers' notes only.
- `page/tfold_depth.html` and `page/tfold_model.html` as files; I read them as they stand in the built page.
- The page at phone size, its links, and anything outside the parts named as new or changed.

---

# A last reading of the box and the story as rebuilt at 01:55 UTC

Started 01:56:00 UTC, 28 November 2026. Finished 01:59:12 UTC (3 minutes 12 seconds). Limit 15 minutes.

The page read is `/home/agent1/site/tonga.html` (sha256 begins 7297b38eef38f65b), my copy and its text in
`check/page21/`, set against `check/page20/`. I read every sentence of the box and the story, and nothing below
"For those who want to check" except where a story sentence sent me there.

**Findings: 0 serious, 1 moderate, 7 minor.** Every new figure is carried. The limits of my sixth report are kept
to: the height, the input corrected after the run, the record of the other make, "rough beyond 9 degrees", and the
colour by its sign only. The one thing lost in the rewording is not about the model.

## The new or changed claims, in the order given

1. "About half an hour after sunset, with the Sun six and a half degrees down": carried. `two_minutes.out` has 24
   to 37 minutes at 21 to 41 degrees south through the year; by my own sum it is 24 to 43 minutes from 21 to 46
   degrees of latitude, and over 37 only at 46 degrees in midsummer.
2. "With five fetched to compare, I had thirty-five northern meters": carried (thirty and five; 46 dots in the
   second picture). The first caption's failing meter is Malargüe: in November and December 2024, its only months
   of that year, it reads 1.0 to 1.25 magnitudes darker than in 2021 at 4, 6 and 7 degrees alike, which is a meter
   and not a sky (`m19/late2024.out`). See minor 3.
3. "From each part of the southern map where I had no meter, one that had enough months, wherever there was one":
   carried by the fold on the test.
4. "All seven showed it, two of them only just": carried.
5. Toulouse: see minor 1.
6. "As if dusk overhead ran two minutes late": carried. 0.34 to 0.39 degree of the Sun's depth takes 1.5 to 2.3
   minutes at these latitudes from late June to early August, by `two_minutes.out` and by my own sum. "By eye it
   would be hard to tell": see minor 2.
7. "As far as two short searches could find, nobody has reported this brightening from sky meters": carried by the
   first search's notes.
8. "(The 50 to 60 per cent above is with the Sun about 7 degrees down.)": carried (52 per cent at 7 degrees by the
   direct measure; the level of the first measure is passed at 6.7 degrees, and near 7.0 in 2022).
9. The two paragraphs on the model: carried, with minors 4 and 5. "Five of my six expectations held" is right by
   the sheet's rule. "A few hundred kilometres": 140, 350 and 630 km at the middle with the Sun 4, 6 and 9 degrees
   down (`m19/where_*.out`). "Less and less of the air overhead is lit directly": the once-scattered share falls
   from 0.70 at 3 degrees to 0.01 at 9 (`model/haze_central_parts.out`).
10. Item 1 of the three: carried. The picture now draws the two thin lines and they end at 75 and 147 per cent.
11. "Too few southern meters had all the years it asked for, and before looking at any reading I changed it to a
    simpler question": carried by the fold. "Which I have kept to": yes.
12. "Which the model says reddened, as the astronomers in Chile found theirs did": carried, as a sign.

**The run with droplets of median radius 0.30** (`model/haze_r030.pkl`, 300,000 photons a case), summed my way
(`m19/r030.out`): +0.04, -0.07, -0.09, -0.23, -0.36, -0.57, -0.71 at 3 to 9 degrees, which is the row in
`model/haze_sens.out`. The pattern holds at all three amounts: within 0.06 of nothing at 3 degrees, brighter at
every step from 4 to 9, the slow step from 4 to 5. The size is about 0.1 smaller than with 0.35 from 7 to 9 degrees
(92 per cent at 9 degrees where the sealed case has 111 and the meters 109), and at most 0.12 from the meters at the central
amount (0.18 at 0.014). Its Monte Carlo error is 0.05 to 0.08 at 8 and 9 degrees. "Its pattern has been the same in every run" stands for the
twelve cases now in.

## Moderate

1. **"How far to trust this" has lost the sentence on the weak figures.** The 01:43 story said: "Between us we
   found weaknesses in the figures of five of the seven tested meters, none of which, I think, explains the
   brightening." Now the paragraph ends on "got the same figures", which reads cleaner than the evidence. The fold
   on the eleven places still has all five. Put the sentence back, after "got the same figures".

## Minor

1. "Unlike the southern meters it brightened by the same amount however deep the Sun was": the meter near
   Toulouse has three levels only, passed with the Sun 5.9, 6.7 and 7.6 degrees down (0.35, 0.33, 0.33;
   `tonga_depth.out` B). "It brightened by the same amount at each of the three depths I measured."
2. "By eye it would be hard to tell" has no line, and the page's own print fold has people seeing vivid twilights
   in those months. If it stays it should be about the brightness overhead only: "Overhead, by eye, I doubt it
   would show: it is as if dusk ran two minutes late."
3. The first caption: the failing meter lifts its own line in every November and December before, not only in
   2021. By the picture's comparison Malargüe stands at 95 and 99 per cent in November and December 2022; against
   2021 alone it is 15 and 27 (`m19/late2024.out`, 7 degrees). "... and by the same comparison its line stands too
   high in late 2021 and late 2022."
4. "Tried it on the ordinary twilight, which it follows closely": to 7 degrees of itself, deeper with one setting
   chosen to fit. The fold says so; the story could say "which it follows closely once one setting is chosen".
5. "Towards the sunset": in the morning it is towards the sunrise. "Towards the Sun."
6. The box: "brightens it in the same way" can be read as "by as much". "... brightens it in the same way, more
   the deeper the Sun."
7. "A meter that has gone dim gets there sooner" and "a sky that has grown brighter gets there later" are true of
   evenings; the 01:43 text said "in the evening". One "in the evening" restores it.

## Not looked at

- The folds, except the lines on Malargüe and on the test's amendment; so not whether each of my fourteen minor
  findings was taken as worded.
- The visitor's report.
- The four runs still going.
- The page at phone size and its links.

---

# A quick reading of the model fold's table as rebuilt at 02:42 UTC

Started 02:42:32 UTC, 28 November 2026. Finished 02:44:20 UTC (1 minutes 48 seconds). Limit 10 minutes.

The page read is `/home/agent1/site/tonga.html` (sha256 begins f15a4d562b0730b9), my copy in `check/page22/`. I read
the table, the paragraph "What that table says" and nothing else in the folds. My sums of every stored run are in
`check/m19/last.out` (program `last.py`).

**Findings: 0 serious, 1 moderate, 3 minor.**

1. **The rows agree with my own sums.** All twelve model rows, at every depth from 3 to 9 degrees, to the two
   decimals printed (`m19/last.out` against `model/haze_sens.out`). The page's table stops at 9 degrees, as it
   should: at 11 degrees four of the new runs give nonsense (-0.26, -0.19, -0.49, -0.63).
2. **"Its pattern has been the same in every run" still stands in the story.** In all 24 cases now stored
   (`m19/last.out`): the change at 3 degrees lies between -0.03 and +0.10; the step from 4 to 5 is -0.02 to -0.05;
   and the model is brighter at each step from 4 to 9 in every case but the three with the larger droplets, where 8
   to 9 comes out +0.016 against a Monte Carlo error of 0.03 at 8 degrees and 0.06 at 9. In that run the once- and
   twice-scattered light, which is summed without random numbers, gives -0.37, -0.59, -0.68 at 7, 8, 9 degrees: it
   rises. The stall is the Monte Carlo's. The fold's sentence owns up to it; the story need not change.
3. **The comparison with the first half of 2023 sets the wrong depths side by side, and its last clause
   understates** (moderate, below).
4. **Nothing in the added rows contradicts a sentence elsewhere on the page.** They bear out "its size has not",
   and they sharpen the story's second doubt without contradicting it: a third of the haze still gives 0.31 to 0.53
   magnitude from 7 to 9 degrees in the model, where the meters are back at nothing by September 2023.

The box and the story differ from my 01:55 copy only by the eight replacements of my last reading, each taken as
worded.

## Moderate

1. **"The model still has 0.44 and 0.53 magnitude at 8 and 9 degrees, where the meters' level end stood at about
   0.43 in those months; the layer had sunk by then, which would make the model's figure smaller."**
   - The 0.43 is the meters at 10 and 11 degrees. At 8 and 9 degrees the meters from January to June 2023 have
     -0.39 and -0.46, and from 4 to 9 degrees -0.06, -0.09, -0.15, -0.28, -0.39, -0.46 (`dpan18b.out` section 5,
     the same ten places at every depth). The model's row is -0.07, -0.10, -0.19, -0.31, -0.44, -0.53. So at like
     depths the model with 0.007 is 0.01 to 0.07 larger than the meters at every depth, not level with them at
     one.
   - "Which would make the model's figure smaller" is right and too mild. The model's own row for a layer 1.5 km
     lower takes a quarter off at 8 and 9 degrees (-0.51 and -0.61 for -0.69 and -0.81), and the second search's
     notes put the plume's droplets in the first half of 2023 from 15 km up to 18 or 19 km at 50 to 30 south
     (`lit/scout-depth.md`, the reading of the effective-radius figure), which is 2 to 6 km below the 21 km of this
     row. The row is the 2023 amount at the 2022 height; it is not the model for 2023.
   - Replacement: "With a plume of 0.007, about the excess the satellites give for the first half of 2023, and the
     layer left at 21 km, the model has 0.44 and 0.53 magnitude at 8 and 9 degrees, where the meters had 0.39 and
     0.46 in those months. But the layer had sunk by then, by two kilometres and more, and in the model a layer a
     kilometre and a half lower loses a quarter of its effect; so with the haze where it then was the model would
     fall short of the meters. That comparison was made after the fact."

## Minor

1. "Nothing at 3 degrees" covers +0.09 with the plume at 0.028 and +0.10 with the layer at 19.5 km and the plume
   at 0.022: a tenth of a magnitude darker. "Little or nothing at 3 degrees (from 0.03 brighter to 0.10 darker)."
   The story's "the loss and the gain cancel" is of the sealed case and may stay.
2. "Good to about 0.05 to 0.08 at 8 and 9 degrees": by the batches the seven new cases shown are good to 0.02 to
   0.05 at 8 degrees and 0.03 to 0.08 at 9 (`m19/last.out`). "Good to about 0.03 to 0.08."
3. "More haze a larger one": from 6 degrees on. At 4 and 5 degrees the plume at 0.028 gives a little less than
   the sealed case (-0.07 and -0.11 for -0.09 and -0.13), and at 3 degrees it dims.

## Not looked at

- Whether 0.007 is the right excess for the first half of 2023: I did not find the total of 0.015 in the notes in
  the time.
- The logs of the new runs, and the higher orders in them beyond what the batches say.
- Any other fold, and the page at phone size.
