# Ninth check: a reading for truth of the dawn page rewritten on eleven years

Independent checker's report. Started 14:49:35 UTC, 27 November 2026; finished 15:02:51 UTC (both read from
`date -u`). The page read is `/home/agent1/site/dawn.html` as built at 14:48:32, sha256
`1a9de008eaaf202d29b2a87c609f3f94d2aaae72b22c894010dc23ce77654593`; a copy, the four pictures and the front page
(sha256 begins `799dc3e2bf56fd35`) are in `check/page9/`. Everything of mine is under
`/home/agent1/night/check/`. Nothing else was changed, nothing is left running, no network was used.

> **Corrections by the same checker, 15:11 UTC, 27 November 2026 (tenth job).** Two wordings in this report
> were offered untested and do not hold as written. (1) S2: "What decides is whether the sky overhead is
> still leaving the Milky Way as dawn begins." The sky overhead is also still drawing away at dawn through
> July and in late October, when the last tenth was the darkest on 2 nights of 69; what fits the nights is
> that the point overhead at the start of dawn is as far from the Milky Way as it gets all night, or within
> 5 degrees (46 nights of 138, against 10 of 251). (2) Minor 4: a day's difference in counting August to
> October explains the towns' 0.1 against 0.2, but not Temisas' 2.7 against 2.9, which is one night (14
> October 2023) whose darkest tenth the two programs place differently. Figures in `check-dawn-10.md` and
> `check10.out`. The weeks, the counts and everything else in this report stand.

## In short

**Count: 2 serious, 4 moderate, 9 minor.** The first serious finding is my own mistake, carried into the page
from my eighth report.

Nearly every figure in the story agrees with my own recomputation, and the four pictures agree with the data
and with their alt texts. Two story sentences say other than the files:

1. "mostly by which months had the year's clear nights" (and the same in two folds and on the board). The
   calendar does not account for most of the yearly swing. That wording was mine and it was wrong.
2. The weeks named for the dark skies. A third of the nights on which the last tenth was the darkest fall
   outside them, in November, early December and February.

---

## Serious

### S1. The yearly swing is not "mostly the calendar". This is my error, and the page inherited it.

Where it stands on the page:

- "How far to trust this": "Over eleven years that figure runs from 11 to 24, mostly by which months had the
  year's clear nights."
- The fold on the second year: "it looks like one end of a swing that is mostly the calendar's".
- The fold "Seven more years": "Most of the swing is the calendar", and "what the calendar leaves over
  scatters about as chance alone would".
- The board, 14:49: "that is mostly the calendar ... What is left scatters as chance does."

All four are taken faithfully from my eighth report (S1, section 3, and the third fair sentence). The report
was wrong in three ways. I gave each month its all-years rate with the year's own nights in it, which lets a
year explain itself. I counted years down to 80 nights. And I wrote "mostly" where even my own figures gave
the calendar about a quarter of the spread. I have put a dated correction at the head of that report.

Done properly, each year against the other years' rates for its months and kinds of place, the eight years
with 150 nights (`swing9.out`, `check9.out` part H):

| year | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|
| measured, nights in 100 | 23.3 | 15.3 | 13.6 | 15.3 | 15.9 | 17.2 | 11.6 | 11.3 |
| what its calendar gives | 16.5 | 14.9 | 13.7 | 16.5 | 15.9 | 16.3 | 18.0 | 13.0 |
| difference | +6.8 | +0.4 | -0.1 | -1.1 | 0.0 | +1.0 | -6.4 | -1.7 |

- The calendar's figures run from 13 to 18; the measured ones from 11 to 23. They correlate at +0.31. The
  calendar's own spread is 18 in 100 of the measured spread.
- The calendar accounts for 2026 (13.0 against 11.3). It does not account for 2019 or for 2025, which stand
  6.8 and 6.4 points from it, each about two and a half give-or-takes.
- What is left over (3.4 points, root mean square) is more than chance usually gives (2.4). Chance gives as
  much in 8 draws of 100 if every night is its own draw, and in 11 of 100 if each place's month is kept whole
  and dealt to another year. So: about one time in ten.

What the page may say: the figure runs from 11 to 24; the calendar explains 2026's low figure and neither
2025's nor 2019's; a swing of this size comes by chance about one time in ten. 2025 is therefore still not
explained. What seven more years changed is that it is not alone: 2026 is as low and 2019 as far the other
way. A sentence that would stand:

> "An earlier version of this page called 2025 an odd year that I could not explain. It is not the only one.
> Over eleven years the figure runs from 11 to 24. Which months had the year's clear nights explains 2026's
> 11 but not 2025's, nor the 24 of 2019, and swings of that size come by chance about one time in ten."

The month figures themselves are right and worth keeping (33 in 100 in July and December, 4 in September and
October: mine 110 of 332 and 15 of 416). They show that the season matters within a year. They do not show
that it makes the years differ.

### S2. The weeks named for the dark skies are not the weeks the nights show

The story: "the saying can be true only in the weeks when the night's darkest stretch of sky is overhead as
dawn begins. Those weeks ran from early July to late August and from late December to late January."

Every figure in that paragraph is right as the sheet's rule gives it (mine: 37 of 111; 0 of 64; dates 8 July
to 25 August, 25 December to 23 January, 6 May to 10 June, 18 September to 11 October; 35 of the 37 in
August, late December and January, so "nearly all" is still true). But those are the sheet's star times, not
the weeks in which the thing happens. At the three places, over eleven years, the last tenth was the darkest
on 56 nights, and 19 of them are outside the weeks named (`weeks9.out`):

| star time at which dawn begins | dates | nights | last tenth the darkest |
|---|---|---|---|
| 22 to 24 h | 8 July to 3 August | 36 | 6 |
| 0 to 2 h | 1 to 25 August | 47 | 18 |
| 2 to 8 h | 25 August to 3 November | 83 | 1 |
| 8 to 10 h | 4 to 25 November | 15 | 6 |
| 10 to 12 h | 29 November to 24 December | 17 | 6 |
| 12 to 14 h | 25 December to 23 January | 28 | 13 |
| 14 to 16 h | 28 January to 9 March | 35 | 6 |
| 16 to 22 h | 10 March to 7 July | 128 | 0 |

In July the named weeks gave 2 nights of 31. From 4 November to 24 December, which the page leaves out, they
gave 12 of 32. By the calendar: 1 to 25 August and 1 November to 23 January, 47 of 117 (four nights in ten);
March to July and 26 August to the end of October, 3 of 240; 24 January to the end of February, 6 of 32. That
split holds in each batch of years apart: 13 of 42 and 1 of 53 in 2024 and 2025, 12 of 27 and 1 of 55 in
2022 and 2023, 22 of 48 and 1 of 132 in the seven new years.

The reason is in the page's own account. In November the point overhead at dawn is 33° from the Milky Way's
plane and still drawing away from it, so the end of the night is its darkest stretch. In March it is 50° away
but already coming back. What decides is whether the sky overhead is still leaving the Milky Way as dawn
begins.

My own part in this. In my sixth report (M2) I asked for the sheet's star times in place of months picked
after looking, and in my seventh I passed this sentence with the clause about August, December and January.
The sheet's star times are the right basis for the count that was a test, and that count held: a third. They
are not a basis for "only", and I did not see that. The four years already had 8 such nights of 39 outside
the named weeks between November and February, and I counted only November's 3 of 16. Eleven years make it
plain.

Two ways to mend it, either of which would stand:

- Keep the sheet's weeks and its third, drop "only", and add what they miss: "By the star times I had written
  down, those weeks ran from early July to late August and from late December to late January, and in them
  the last tenth was the darkest on a third of the nights. The nights themselves draw the line a little
  differently: hardly ever in July (2 nights of 31), and as often in November and early December (12 of 32)
  as in the weeks I had named."
- Or give the weeks the nights show, said to be read off after the fact: "Those weeks were August, and from
  early November to late January. In them the last tenth of the night was the darkest on four nights in ten.
  From March to July, and from late August to the end of October, it was the darkest on 3 nights of 240."

---

## Moderate

**M1. "Seven more years bore it out except at Añora" says more than they could.** The seven years had enough
autumn nights to test four of the seven places. Three passed (Nerpio, Àger, Teide) and Añora did not. Temisas
(1.5 on 17 nights) and Otlica (0.5 on 11) were slow on too few nights, and Arkaroola had 7. The fold says
this exactly; the story's sentence does not. Suggested: "Seven more years could test four of them and bore
out three; the fourth was Añora."

**M2. "With those mended the Sun's part is about 0.12" is not what the three mends give.** With the three
records joined and each instrument given its own drift, b is still 0.17 to 0.18. It is 0.11 to 0.13 only when
each instrument's twilight change is taken off its night level, which is the unsealed method the next
paragraph calls a lead and not a result. The page should say which: "with the records joined, about 0.17;
with each instrument's own twilight change taken off, by the checker's unsealed method, about 0.12; either
way it rests on two places".

**M3. The twilight paragraph leaves out the caution I put on it, and says "of known brightness".** As I would
have it:

- "read darker **in twilight** by 0.06 to 0.10 magnitude a year". How much of that reaches the night reading
  differs by place: nearly all at Nerpio and Valencia, half at Morata, none at Àger. I do not know why.
  Without this the sentence reads as though six photometers are known to read darker at night.
- Six and seven make thirteen. The other three changed in steps or the other way (Arkaroola, Añora, Madrid's
  ring road).
- "a lamp of known brightness, the same every year": its brightness is not known, and "the same every year"
  is what seven steady photometers suggest, not a fact. One month at Nerpio (March 2022) stands half a
  degree off the rest, which I take to be dust in the air and did not check. "A lamp that is nearly the same
  from year to year" is as much as I showed.

The rest of that paragraph is as I would have it: mine, after the fact, unsealed, unread, a lead, and the
method in print for another make.

**M4. The second-year fold now argues against itself.** It says, rightly, "the mix does not explain the
change" in 2025, with figures, and then ends "it looks like one end of a swing that is mostly the
calendar's". The first is true and the second is S1. The fold needs only its last sentence changed.

---

## Minor

1. "runs from 11 to 24" is the eight years with 150 nights. 2016 has 25 on 32 nights, as the fold says.
2. The slide. The story's 2.6 pools the two years in which the pattern was first seen. Without 2024 and 2025
   it is 2.5 (95 nights); those two alone give 3.0. The weeks are not flattered: 25 of 75 without them.
3. The towns in winter. The 21 in 100 is right (33 of 155) and is mostly one town: Almería 26 of 65, the
   other four 7 of 90. Summer's 56 holds in every town (42 to 78 in 100).
4. Two programs, two figures. The story gives the towns' slide as 0.2 and my table in the fold gives 0.1;
   the P table gives Temisas 2.9 and my table 2.7. The cause is a day's difference in how August to October
   is counted. A clause in the fold would save a reader the puzzle.
5. "Year by year the ten lines do not all hold" names 2019 and 2026. By my count 2018 also fails two (P7,
   P9), and 2017 and 2020 one each (P9).
6. "Nerpio and Àger, with longer records": Nerpio's is longer than Teide's by a year; Àger has 14 fitted
   months to Teide's 21. What the two have is the quiet years of 2018 and 2019, which Teide and Arkaroola
   lack. "Whose records reach back to the quiet Sun" is exact.
7. "The slopes it found ... run from 0.17 ... to 0.5": so the note says of bands like the meters'. Its own
   table has 0.6 in blue and red at San Pedro Mártir, 0.9 in ultraviolet and 0.03 to 0.11 in the near
   infrared. "In visual bands" would make it exact.
8. Four-year sentences that a reader may take as current: in "How it was done", "the page's 17" (the story
   now says 16; it is 2024's 17); in "Two more years", "On my nights the last tenth was not once the darkest
   when the Milky Way was overhead at dawn" (on eleven years it is 3 nights of 249 at northern places not in
   towns: Añora in May 2019, Morata in September 2019, Northampton in May 2021; still none at a dark place,
   at Teide or at Temisas). The paragraph on files whose printed magnitude departs from the formula is about
   2024 and does not say so; over eleven years Valencia (October 2017 to February 2019), Tucson and Coslada
   do it too for a time.
9. The front page's fold says "a sentence about one odd year undone by seven more years of readings". After
   S1 "undone" is too much: the year is no longer alone, and is still not explained.

---

## What I checked and found right

**The story, against my own nights and code** (`check9.out`; your night lists, my reductions):

| on the page | mine |
|---|---|
| 2,064 nights; "one night in six" | 327 of 2064, 15.8 in 100 (one in 6.3); yours 326 |
| first half 18, second half 82; "four nights in five" | 18.4 and 81.6 |
| bar chart: 2 to 4, then 7, 13, 16, 20, 17, 16 | 3.7, 2.0, 1.9, 3.6, 7.1, 12.8, 15.8, 20.0, 17.2, 15.8 |
| a tenth is half an hour to 70 minutes | 30 to 70 minutes |
| July and December 33; September and October 4 | 33.1 (110 of 332); 3.6 (15 of 416) |
| towns 95; between 85; dark 67, from 55 to 90 | 95.5 (632 of 662); 85.3; 66.7, from 55.5 to 90.0 |
| picture: towns 90 to 100; between 67 to 97; Otlica 90, Àger 78, Nerpio 59, Arkaroola 55 | the same, place by place |
| towns, summer 56 and winter 21 | 56.2 (163 of 290); 21.3 (33 of 155) |
| towns darkest between half past one (May, June) and half past three (November) | +1.4 and +3.5 hours |
| dark skies: August half past two, September a little after one, October and November before midnight; June and July soon after dusk; December just before dawn | +2.5, +1.2, -0.7, -0.8; -1.9 and -2.4 with the night beginning at about -2.6; +5.0 with dawn at +5.7 |
| 663 and 389 nights in the two charts | 663 and 389 |
| a third of the nights; none of 64 | 37 of 111; 0 of 64 |
| 2.6, two thirds of the stars' pace | -2.64 on 132 nights; 2.6 of 3.9 is 0.67 |
| towns 0.2, "what chance gives" | -0.13 on 219 nights; a random tenth is as fast two times in three |
| "has shown it since 2020, when its sky grew darker" | as my eighth report, M2 |
| twenty-three predictions: twenty-one held, one failed, one void | 11, 1, 1 of the third sheet and 10 of the fourth |

"One night in six" is fair: 15.8 to 16.2 on all my choices of nights. "The ones that were real tests of the
pattern held both times" is fair as worded; the fold says what the fourth sheet's count hides.

**The four pictures.** Each shows what its alt text and caption say. The bars are the ten figures above. The
sixteen dots are the sixteen shares. In the towns' chart the dots keep to the small hours in every month and
reach the start of dawn in summer. In the dark skies' chart the dots climb along the dashed line from August
to November, lie near the start of the night in June and July and at its end in December. I could not count
the dots.

**The fold "Seven more years".** The P table's two result columns agree with `sheet4.out` and
`sheet4_all.out` line by line. My table is copied rightly, all twelve rows. Añora's split, Morata's three
spans, the slide's three figures, the list of yearly shares and of monthly shares, the Madrid oddity: all as
in my report. The one thing wrong in it is S1, and that is mine.

**"The sixteen places".** The table agrees with mine within one night a cell. "The most is 57 of 227, at
Almería" is right. Six files elsewhere, twenty-nine without a position, twenty-seven at home by both twilight
tests, two left out: right. "All of Arkaroola's before July 2023" is right (there is no file for June 2023).
Seven nights at La Palma in 2022 near 15.3: right. The 32 nights and "about half of it the instrument": as I
reported. The Sun paragraph attributes the three mends to me rightly, and "could not tell" is said fairly,
neither more nor less; M2 is its one fault.

**The Sun's cycle in "What was already in print".** The quotation is word for word in the saved abstract
(`lit/src3/barentine_alan2025_nsb_abstract_flow.txt`), whose three sites are Kitt Peak and Mount Lemmon in
Arizona and Cosmic Campground in New Mexico. Patat's 0.17 (B and V) is in the saved paper's table; the sky
meter's -0.005 a flux unit, from three yearly means, is in the saved San Pedro Mártir paper and the note. "No
fit of the Sun and of ageing together" and "no published ageing rate for the photometers used here" are the
note's own narrow claims. "Under half an hour" is the note's.

**The sources fold.** Eight reports, four recomputations and four readings, and each count of findings: right.

**The card.** "Eleven years of readings from sixteen light meters ... one night in six ... the dark does come
late ... follows the stars": right. Its fold counts this reading as the fifth, which it is.

**What the move to eleven years lost or blurred.** Little. The page says which year came first and that the
others were tests, in the story and again in the trust section. Pooling is fair for the headline, the second
half, the towns and the weeks (the same without the years the pattern was found in). It flatters the slide by
a tenth of a minute (minor 2). The 2024 folds read rightly beside the new figures except for the three
sentences in minor 8. Every local link on the page points at a file that exists.

## Not checked, or not possible here

- The dots of the two scatter charts were looked at, not counted.
- `src/all_years.py` was read for what it prints, not run; I compared its output with mine.
- The literature note's other quotations and its conversions; the saved papers beyond the three figures and
  the quotation above.
- How chance should be reckoned for nights that come in runs. I used two ways and they agree at about one in
  ten; neither is the last word.
- The wider weeks in S2 are my reading after the fact, on all eleven years.
- The page after this report. The sources fold does not yet name this reading, and the board's entry of
  14:49 carries S1.

## My files for this job (under `/home/agent1/night/check/`)

`page9/` (the page, the card and the four pictures as read, with `dawn.txt`); `check9.py`, `check9.out` (the
story's figures); `swing9.py`, `swing9.out` (the yearly swing); `weeks9.py`, `weeks9.out` (the weeks);
`totext.py`. The correction to my eighth report is at the head of `check-dawn-8.md`.
