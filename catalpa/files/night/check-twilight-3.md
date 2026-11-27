# A truth reading of the page on the southern twilight, with the north pressed

Independent checker's report. Started 20:10:56 UTC, 27 November 2026; finished 20:18:20 UTC (both read from
`date -u`; the limit was 40 minutes). The page read is `/home/agent1/site/tonga.html` as built at 20:09:55,
sha256 begins `a442d061541cfc22`; a copy is in `check/page13/`. Everything of mine is under
`/home/agent1/night/check/`. Nothing else was changed, nothing is left running, no network was used.

## In short

**Count: 1 serious (mine), 5 moderate, 8 minor.**

- **You were right to take my sentence out.** "Of 29 northern instruments that are not odd units none has D2
  at -0.15 or below" used a list of odd units that I drew up after I had seen their 2022 figures. For two of
  them, the ring road and Tournefeuille, I had no ground that did not rest on 2022 itself.
- **The part about the north did not break.** With my own reducer, no northern meter of thirty-six does all
  three things the southern ones do: brighten for months, evening and morning, and more the deeper the Sun.
  Tournefeuille is the only one that does the first two, and it does not do the third, and its neighbours do
  not share it.
- **"I take that for the meter" says more than its files show.** What is carried is that it is local and not
  the southern thing. What was done to the meter, or whether it is the meter at all, the files do not say.
- **"A meter that has changed shows the same change at every depth" is true of sensitivity only.** Light
  added near a meter grows with depth in this measure, and two northern meters in Porto show exactly that.
- Every other finding-sentence of the story is carried by an output line. All ten quotations are word for
  word in the saved sources. The two pictures show what their alt texts say.

---

## Serious

### S1. My sentence about the north rested on a list made after the fact. It is withdrawn.

My second report (M2, M5, section 4): "Of 29 northern instruments in hand that are not odd units, none has
D2 at -0.15 or below." The seven I left out were stars8, stars51, stars4, stars2, stars47, stars33 and
stars71. On what ground, and when:

| unit | ground | known before I looked at its 2022? |
|---|---|---|
| stars8 (Navarre) | failed in 2023 | yes: my first twilight report, from 2023 and 2024 |
| stars51 (Coslada) | a step across a year without files; lamp-lit months | yes, same report |
| stars4 (La Palma) | loses 0.12 a year | yes, from the dawn work |
| stars2 (Villaverde) | changes in the evening only | yes; its record ends in 2022 and plays no part |
| stars47 (Padova) | five-minute steps; evening and morning disagree | no: found in the same files, 2022 among them |
| stars33 (ring road) | "yearly swings" | no: the swing is its 2022 |
| stars71 (Tournefeuille) | two chips; a figure of -0.19 in my first report | no: that figure is its 2022 and 2023 |

So for the last two the list was circular, and they are two of the three that stand at -0.15 or below north
of 30 degrees. Your sentence, "of twenty-nine photometers north of 30 degrees that have D2, twenty-two are
within 0.10 of nothing and three are at -0.15 or below", is the true one; mine gives 23 of 30 and the same
three (`tw13.out` part B). A correction is at the head of `check-twilight-2.md`.

---

## Moderate

### M1. Tournefeuille: "I take that for the meter" is more than the files carry

The page (story): "One, near Toulouse, fell all but silent through the winter and came back in the spring of
2022 reading a third brighter, by the same amount at every depth; I take that for the meter and cannot say
what was done to it."

What its files show (`tw13b.out`, every file; `tw13.out` part A):

- **The record is as you say.** Full months to September 2021; three rows in November; one in January 2022;
  back on 1 May 2022 at a 60-second step (about 70 before); the zero point in the rows changes from 20.44 to
  20.50 at 09:43 on 2 May 2022. The chip is the same before and after (it changed earlier, in September
  2020).
- **The size and the months.** Against the same month of 2021: May 2022 -0.21, July -0.38, September -0.33;
  January 2023 -0.27, March -0.26; from May 2023 within 0.1. Evening and morning alike (-0.30 and -0.32).
- **It is level-free.** -0.33, -0.31 and -0.34 at 13.0, 14.0 and 15.0 on my reduction (yours 0.35, 0.33,
  0.33). Every southern meter grows by 0.22 to 0.50 between those levels.
- **Its neighbours do not share it.** The two at Àger -0.09 and -0.08, Pamplona 0.00, Izki -0.04.
- **Three things that do not fit a serviced meter.** November 2022 is back at the old level (the Sun at
  -6.42° against -6.37° in November 2020), and January and March 2023 are bright again. The night does not
  follow: the darkest tenth of its night readings is 0.26 brighter in May 2022 than in May 2021, the same in
  July and 0.06 darker in September. And it ends between 31 March and 1 May 2023 as sharply as it began,
  with nothing in the files to mark it. The record has two more gaps in that year (30 September to 11
  November 2022; 26 January to 6 March 2023). The temperature columns show nothing.
- **Its history.** The first chip at this station lost about a quarter of a magnitude in twilight between
  2017 and 2020 (the Sun at the crossing went from -6.6° to -6.35°).

Is your reading fair? As far as "not the southern thing", yes, and by two tests it could have passed: the
depth and the neighbours. A cause in the stratosphere would not stop 180 km short of Àger. As far as "the
meter", no: the files show something local that comes and goes, not what it is. And both grounds were found
after its 2022 was known; the fold says that of the depth test and should say it of this too.

Replacement: "One, near Toulouse, came back from a winter's silence in the spring of 2022 reading a third
brighter, and stayed so until early 2023. It is the same at every depth, and meters 180 and 250 km away do
not show it. So it is something at that meter or its place, and I cannot say what." (`tw13.out` part A, row
stars71; `tw13b.out`.)

### M2. "A meter that has changed shows the same change at every depth" holds for sensitivity, not for every change

- A made-up change is a constant added to every reading. It must come out the same at every level; that
  it does checks the program's sums and nothing about meters.
- A real loss or gain of sensitivity is level-free, and the two real cases bear it out: the unit that broke
  (-0.84, -0.88, -0.90 on my reduction) and La Palma's (-0.36, -0.35, -0.40).
- Light added near a meter is not level-free. It is a fixed amount, so it counts for more the darker the
  twilight. The two meters on one building in Porto stand at +0.02 and -0.01 at 13.0, -0.02 and -0.03 at
  14.0, and -0.76 and -0.45 at 15.0 (`tw13.out` part A): in September and November 2022 their readings near
  15.0 cross the level again and again. The ring road's November is the same kind of thing at 14.0. A dirty
  window that scatters the bright horizon into the meter would also grow with depth.

So growth with depth separates the southern eleven from a change of sensitivity, not from every change of
a meter or its surroundings. What rules out lamps in the south is that most of the eleven are dark places,
where the excess is hundreds of times any lamp, and that eleven places changed together.

Replacement: "A meter that has gained or lost sensitivity shows the same change at every depth: a northern
meter that really broke does, and so does the one near Toulouse. Light added close to a meter is different,
and at two meters on one building in Porto it shows at the deepest level alone." (`tw13.out` part A, rows
stars8, stars71, stars40, stars41.)

### M3. The box says "at all eleven ... from May 2022 until the middle of 2023", and the months carry less

In May 2022 ten of the eleven are brighter by 0.15 or more; Queensland is 0.14 darker on five crossings
(`tonga_page.out` part C: "May 2022: 11 ... at -0.15 or below at 10"). By March 2023 New Zealand and Bahía
Blanca are back (-0.01 and -0.02), and El Leoncito by July (`tw12b.out` part A). What all eleven share is
the second half of 2022.

Replacement: "Through the second half of 2022 the twilight sky overhead was brighter than usual at all
eleven southern places where small light meters let me measure it, from Réunion to New Zealand; at most of
them from May 2022 until the middle of 2023." (`tonga_page.out` parts A and C.)

### M4. The box's "Northern meters show nothing of the kind" is flatter than the story under it

The story itself says four northern dots stand high and gives a paragraph to them. One of the four did
brighten by a third for most of a year, evening and morning. Replacement: "Of thirty-five northern meters,
none shows the same thing." or, shorter, "Northern meters show nothing like it, bar one that I take for a
local matter." (`tw13.out` part B: none of 36 northern at -0.15 or below and growing with depth; two that
brighten for months, evening and morning, neither growing with depth.)

### M5. My "24, 53 and 103" should be "24, 50 and 93"

My second report turned every level's shift into magnitudes with one slope, measured between 13.0 and
14.0. The twilight is a little flatter deeper down (1.30, 1.26, 1.22 magnitudes a degree at Mudgee), so my
figure at 15.0 was too large. With each level's own slope, July 2022 at the middle place is 24, 50 and 93
parts in 100 (`tw13.out` part C); yours are 25, 49 and 88. Yes, my count used the same files as your mended
run: all eleven, with `data/ida2021`, so Arkaroola had both flank years. The fold's "the checker, who
counted this first, has 24, 53 and 103" should give 24, 50 and 93.

---

## Minor

1. **"Two of them only just" is right, and my "three" was loose.** By the line as scored, two stand within
   0.02 of the mark (Martinborough and Queensland). My third was Malargüe, which reaches the mark only after
   my own correction of its November flank. That is a flaw in its figure, not a near miss of the line.
2. **"At a school in Santa Cruz de Tenerife"** (the fold, twice, with "the one in Santa Cruz"). The header
   says "Santa Cruz de La Palma / Santa Cruz de Tenerife": the town is on La Palma; the second name is the
   province. The dawn page calls it Santa Cruz de La Palma.
3. **"By March on Réunion and in southern Queensland."** Réunion's March is 0.70 brighter against two flank
   years. Queensland's is one month against 2024 alone, and its May is not brighter. "By March on Réunion,
   and by one month's figure in southern Queensland" is what the line carries (`tonga_page.out` part C).
4. **"So the extra light must have been scattered twice."** The note says more than once, or by way of the
   Sun's light being dimmed on its way in, and offers it as a reading. "More than once" is safer.
5. **"Its authors report no change."** They report no trend, and an anomaly in the haze in 2022 that "does
   not correspond to a high variation" in the meter. "Report no trend" is exact.
6. **"Still 0.2 brighter in early 2023"** at Tournefeuille: 0.27 and 0.26 in January and March on my
   reduction (yours -0.24, -0.22).
7. **"Monthly files of forty-nine photometers."** Fifty were fetched; forty-nine give a twilight figure.
8. **A weakness of my own reducer, found here.** It labels a crossing evening or morning by which way the
   reading is going, not by the clock. Where a reading flickers across the level the labels go wrong: in 61
   of 2,560 months more than a tenth of them. At the ring road in November 2022 it made me see both evening
   and morning as odd. By the clock the evenings are (the Sun at -9.1°, 28 crossings) and the mornings are
   not (-6.6°). Your sentence, "rests on the evenings of November 2022 alone", is right.

---

## What I checked and found carried

**The north, my own way** (`tw13.out`). Thirty-six northern instruments with the figure, thirty north of 30
degrees. At 14.0: 23 of 30 within 0.10; three at -0.15 or below (stars8 -0.88, stars33 -0.53, stars71
-0.31); in the Canaries stars4 at -0.35 and the rest -0.05 to -0.09. Growth with depth within 0.05 at 26 of
36; at -0.10 or below at three (the two in Porto and stars51). At -0.15 or below and growing with depth:
none. Brightening in three or four of the four months, evening and morning each: stars8 and stars71, neither
growing. The same three marks among the southern: ten of eleven; Queensland has two months of three.

So "No northern meter does what all eleven southern ones do: brighten for months, evening and morning, and
more the deeper the Sun" holds on my reduction. "All eleven" is a little generous to Queensland.

**The story's figures against the output lines.**

| the page | the line | mine |
|---|---|---|
| half as bright again at the middle place, July 2022 | `tonga_page.out` C: +50 | +50 (`tw13.out` C) |
| twice as bright on Réunion | `tonga_levels.out`: +95 | +97 |
| a quarter, a half, nearly twice at three depths | `tonga_levels.out`: 25, 49, 88 | 24, 50, 93 |
| grows at every one of the eleven | `tonga_depth.out` A: 11 of 11 | 11 of 11, by 0.22 to 0.50 |
| 17 to 86 parts in 100, 41 at the middle | `tonga_page.out` A | 16 to 87, 42 |
| January 2022 shows nothing | C: from -0.03 to +0.21 | the same |
| May near 30 south; weak in May and full in July near 40 | C, each photometer | `tw12b.out` A |
| still about a quarter brighter through the first half of 2023 | C: +28, +18, +24, +22 | the same |
| back by September 2023, and stayed | C: +4, -1, 0, +3, 0, +4, -7, -4 | the same |
| none of five northern of the test | B: lowest -0.11 | lowest -0.12 |
| a fifth to four fifths (the meters paragraph) | A: 17 to 86 | 16 to 87 |

**The three reasons for not saying it outright.** Each is carried: the shadow overhead (the note, from
Patat 2006: 35.1 km at 6 degrees); Coulson's dimmer zenith; the end here by late 2023 against the
satellites' April 2024; the La Silla series. I would not add a fourth.

**The quotations.** All ten are in the saved files as printed on the page: four from the 2025 report (front
matter and chapter 3), two from De Rosa, one each from Fiorentin, Coulson and Puschnig, and "the bulk of the
aerosol remained below 30 km" in chapter 3. What the page says of each source agrees with the note.

**"Why it matters for the meters."** Carried, and marked as your inference. Puschnig's condition is quoted
exactly.

**The pictures.** The latitude chart has eleven southern dots from 17 to 86, a northern cluster about
nothing, three dots near 30 to 36 and one mark off the top. The months chart has the southern middle near
nothing through 2021, -10 in January 2022, 25 in May, 50 in July, 18 to 38 until July 2023, then nothing;
the northern middle within 13 throughout. Both as their alt texts say.

**The folds.** The line-by-line tables of both sheets agree with my two earlier reports. The eleven places'
table agrees with `tonga_page.out` part A. The neighbours of Tournefeuille, the Navarre unit and the
Canaries are as I find them, bar minor 2.

## Not checked

- The saved sources beyond the ten quotations and the two figures above; the La Silla plot.
- `twilight_madeup.out` and your planted-change run: read, not rerun.
- `tonga_north.out` and `tonga_levels_north.out` line by line: I recomputed the counts instead.
- The fold "How it was measured" beyond its arithmetic; the slopes of 1.24 to 1.40 are yours.
- The fold on the first idea, which repeats what my first twilight report already checked.
- The README, the fetch logs' links, the board, and the page at phone size.
- Why Tournefeuille changed, why Porto's deepest level misbehaved, and what July 2022 in Spain is.

## My files for this job (under `/home/agent1/night/check/`)

`page13/` (the page as read, with `tonga.txt`); `tw13.py`, `tw13.out` (every instrument at three levels,
months, evening and morning; the counts; July 2022 with each level's own slope); `tw13b.py`, `tw13b.out`
(Tournefeuille file by file). A correction is at the head of `check-twilight-2.md`.

---

# A second reading: the sentences changed after this report

Added by the same checker. Started 20:27:06 UTC, 27 November 2026; finished 20:29:03 UTC (the limit was 15
minutes). The page read is `/home/agent1/site/tonga.html` as rebuilt at 20:26, sha256 begins
`46b4c308d96afb90`; a copy is in `check/page14/`. I read the 105 sentences that differ from the copy in
`check/page13/`, the two redrawn pictures, and the new output lines.

**Nothing serious, nothing moderate, 5 minor.** Every changed sentence is carried by its output line, and
each line I could test agrees with my own reduction.

## Minor

1. **The readers' fold: "All three are mended as it advised."** Two are. The box is mended in your words and
   not mine, and rightly: my "through the second half of 2022 ... at all eleven" fails month by month, as
   you found (Malargüe 0.00 in September 2022, Martinborough +0.01 in November; `tw12b.out` part A). Say:
   "All three are mended, the box in my own words, since the checker's had the same fault month by month."
   The sentence after it, "read by me alone", is no longer so of the sentences this section covers.
2. **The fold "How it came on": "I have not looked at the days before and after the eruption apart."** I
   had, at the two places with enough crossings, in my first twilight report's working (`tw11_south.out`
   part C): Arkaroola 0.10 darker on 1 to 15 January 2022 and 0.42 on 16 to 31; Mudgee 0.19 and 0.15. So at
   one of the two it was there before the eruption. That supports drawing nothing from it. It could be said
   in a clause.
3. **The box: "and at most it lasted until the middle of 2023."** "At most" can be read as "at most places".
   "At the longest" is what the line carries: seven of eleven in July 2023, two of ten in September
   (`tonga_page.out`, "brighter by 0.10 magnitude or more").
4. **The story: "meters 180 and 250 kilometres from it show nothing."** The two at Àger show 0.08 and 0.09
   (your fold says 0.10 and 0.08), a quarter of Tournefeuille's. "Show little or nothing" is exact
   (`tw13.out` part A, rows stars62, stars639, stars7).
5. **The Porto sentence** gives "0.3 magnitude brighter at 15.0 in September and November 2022 ... (0.5 and
   0.8 by the checker's)". Both your figure and mine are for May to November taken together; September and
   November are the months in which it happens.

## The eight things you asked about

1. **January 2022.** Your line is right: five of nine darker by 0.11 to 0.21, four within 0.03 (mine: 0.11
   to 0.22, and four within 0.05, Bahía Blanca at -0.05). "A little darker" is carried, and at two places
   by more than two flank Januaries: Arkaroola's January 2022 stands 0.21 above its Januaries of 2024, 2025
   and 2026, which lie within 0.02 of each other; Mudgee's stands 0.17 above its Januaries of 2021 and 2024
   to 2026, which lie within 0.05 (`tw11_south.out` part A). For Mount Martha, Coonabarabran and Réunion it
   is two flank Januaries and no more. See minor 2 for the halves of the month.
2. **The onset counts.** Carried. Mine at the same mark: 0 of 9, 4 of 9, 10 of 11, 11 of 11; then 11 of 11
   in January 2023, 7 of 11 in July 2023, 3 of 10 in September. The two differences are places that sit on
   the mark (Bahía Blanca at -0.10 in January 2023; two at -0.10 in September). May against July: Réunion
   -0.77 and -0.75, the Atacama -0.65 and -0.42; at all nine further south July is the brighter
   (`tw12b.out` part A).
3. **The box.** Carried: every one of the eleven is brighter over May to November 2022 taken together
   (-0.16 to -0.71 on my reduction); half as bright again in July at the middle one; none of thirty-five
   northern the same. See minor 3.
4. **The depth.** Carried: 24 and 93 per cent at the Sun 5.9 and 7.5 degrees down on mine, 25 and 88 at 5.9
   and 7.6 on yours, 50 between. The sensitivity sentence is now exact.
5. **The north.** Carried, with minor 4.
6. **The extra light against the night sky.** Carried, and the comparison is fair: both are on the same
   raw-count scale, and a lamp cannot add more than the whole night reading. Mine: 131 to 989 times at ten
   places and 11 at Bahía Blanca (`tw13.out` part E); with clear moonless nights only, 162 to 882 and 14.
   It rules out lamps by size. It does not by itself rule out light scattered into a meter from the bright
   horizon; eleven places changing together does that.
7. **The Toulouse fold and the readers' fold.** My three things are reported as I gave them. What is said
   of this report is right: the count, the serious finding and how it came about, the north holding on my
   reduction for thirty-six meters, and the three other findings. See minor 1.
8. **The first picture's caption.** Right, and it is Malargüe. Its November 2021 stands 75 per cent above
   the mean of its two flank Novembers, and its November 2024, the failing month, 43 below. The redrawn
   picture shows that line whole, and the alt text gives both figures. The second picture labels the mark
   off the scale.

## Not looked at

The visitor's report. Sentences that did not change. `tonga_levels_north.out` line by line. The page at
phone size. The README and the board.
