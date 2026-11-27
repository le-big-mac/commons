# The months between: a check of the eighth sheet

Independent checker's report. Started 21:15:50 UTC, 27 November 2026; finished 21:22:50 UTC (both read from
`date -u`; the limit was 40 minutes). Everything of mine is under `/home/agent1/night/check/`. Nothing else
was changed, nothing is left running, no network was used. The 332 files under `data/tw3/` were reduced by
my own reducer (`tw11.py`, the raw count), and every line was computed from the sheet's words. I did not
read `src/between.py`; I compared its output with mine afterwards.

## In short

**Count: nothing serious, 6 moderate, 5 minor.** One of the moderate ones is a mistake of mine that is on
the published page.

- **Sealing holds.** The sheet and its programs were fixed before any even-month file was fetched, and no
  reduction was opened before the scoring at 21:13.
- **Your score reproduces.** On my reduction ten lines hold and V9 fails, each by the same figures to 0.01
  or one place.
- **Four of the ten that held stood at their marks**: V4 by 0.03, V7 by 0.04, V8 on four figures within
  0.02 of the mark, V11 with its one allowed month used up.
- **V4 held as worded and its heading is false.** July is not the peak. June, July and August are level.
- **V9's December is mostly weather and the Decembers compared with**, and so is October 2022's dip.
- **Yes, the Atacama belongs with Queensland.** "The other four are clean" came from me and was wrong.

---

## Moderate

### M1. "The other four are clean" is mine, is on the live page, and is wrong for two of the four

My second report (M3) said three of the seven have a flaw and "the other four (Martinborough, Mount Martha,
Cerro Toco, Le Tampon) are clean". My own table in the same report gave Cerro Toco's flank years as "2024"
and Le Tampon's as "2021". With the even months in hand (`tw15.out` part B, `tw15b.out` part F):

- **Atacama (stars391):** no month of 2021 gives a figure. Its 2021 files that have rows are May (crossings
  on evenings only) and October (16 rows). Its 2022 is set against 2024 alone, exactly as Queensland's is.
- **Réunion (stars251):** its only month of 2024 is January. Every other month is set against 2021 alone.
  A unit going dim would make its 2022 look darker, so the lean is against the finding, but it is one flank
  year all the same.

Should the Atacama be counted with Queensland? Yes, as resting on one flank year. Your reading of its course
is right, and there is a second ground from inside its files:

- A unit losing sensitivity steadily would stand at one figure through 2022 and at half of it through 2023.
  The Atacama's 2022 months average -0.52 and its 2023 runs from -0.50 in January to +0.22 in December.
- Its figure grows with depth in every month of 2022 (April: -0.46, -0.69, -0.98 at 13.0, 14.0, 15.0). A
  change of sensitivity is the same at every depth. The same holds for Queensland.

Both grounds are after the fact.

Replacement for the fold: "Three of the seven have a flaw in their figure ... Two more rest on one flank
year: the Atacama photometer has no usable 2021, so its 2022 is set against 2024 alone, as Queensland's is,
and Réunion's has only January of 2024. At the Atacama a unit going dim is ruled out by the course (its 2023
runs from 0.50 brighter to 0.22 darker than 2024) and by the depth. Martinborough's record begins in July
2021, so its months of the first half of the year are set against 2024 alone as well. Mount Martha is the
one of the seven with both years in every month and no flaw." (`tw15b.out` part F; `tw15.out` part B, last
column: the months each place has in 2021 and in 2024.)

### M2. V4 held as worded, and "July stays the peak" is not what the months show

The line's mark allowed June or August to be up to 0.05 brighter than July, and both are: June -0.44, July
-0.42, August -0.43 at the middle of the ten (yours -0.45, -0.42, -0.43). By place (`tw15b.out` part C):

- July is the brightest of the three at 4 of 10 places.
- Each place's brightest month of 2022: June at three, July at three, August at two, April at the three
  nearest the tropics (Queensland, the Atacama, Réunion).
- November and December 2022 are nearly as bright at the middle (-0.36, -0.38).

So the months carry a plateau from June to August, not a peak month, and no place has a sharp peak. This is
the second line of this notebook to hold only as worded (the first was P8 of the dawn page).

Replacement for the page's "July 2022 is the peak: half as bright again at the middle place": "From June to
August 2022 the twilight at the middle place was half as bright again, with nothing to choose between the
three months, and it was nearly as bright again in November and December. Nearer the tropics the brightest
month was April." (`tw15b.out` part C, first line and the list under it.)

### M3. V9: December 2023 is weather and the comparison Decembers, not a third thing in the sky

The middle of eight places is +0.14 on my reduction (yours +0.13). Looked at four ways (`tw15b.out` part A):

| December 2023 | middle of the places that have it |
|---|---|
| as the sheet reckons it | +0.14 |
| the brightest quarter of the month's twilights only | +0.08 |
| against December 2021 alone | +0.10 (7 places) |
| against December 2024 alone | +0.08 (7 places) |

- **It is not one comparison year.** December 2023 is darker than both. But the two flank Decembers differ
  from each other by 0.10 to 0.22 at six of seven places, in both directions: at Mudgee, Coonabarabran and
  Arkaroola December 2024 is the brighter by 0.12 to 0.20; at Mount Martha, Bahía Blanca and Martinborough
  December 2021 is, by 0.10 to 0.22.
- **Part of it is cloud.** Taking only the brightest quarter of each month's twilights, the middle falls to
  +0.08 and Mount Martha's +0.19 falls to -0.02. Mount Martha, Coonabarabran and the Atacama have no clear
  moonless night in December 2023 (0 of 5, 0 of 4, 0 of 4).
- **It is where the summer is.** The four Australian places and the Atacama stand at +0.17 to +0.25; the
  other four at -0.02 to +0.08. January 2022 was the same shape (Australia 0.17 to 0.22 darker).
- **Arkaroola has a fourth December.** About December 2024, its Decembers of 2021, 2023 and 2025 stand at
  +0.20, +0.27 and +0.11. So there December 2024 is the odd one.

So a mark of 0.08 was too tight for a summer month at these places: their Decembers and Januaries differ by
0.1 to 0.3 from year to year. The first half of V9 (October 2023, -0.02) held.

Sentence for the page: "The one line that failed was December 2023, which read 0.13 magnitude darker than
the Decembers of 2021 and 2024 at the middle place. Half of that goes when only the clearest twilights are
taken, and the two Decembers compared with differ from each other by as much. I had set too tight a mark for
a summer month." (`tw15b.out` part A.)

### M4. October 2022 is mostly cloud and one bright comparison October; the sky was still brighter

At the five places between 32 and 41 degrees south (`tw15b.out` part B):

| October 2022 | Martinborough | Bahía Blanca | Mount Martha | Malargüe | Mudgee |
|---|---|---|---|---|---|
| as the sheet reckons it | -0.08 | -0.07 | -0.01 | -0.04 | -0.05 |
| the brightest quarter of the twilights | -0.14 | -0.22 | -0.16 | -0.15 | -0.26 |
| against October 2021 alone | -0.03 | +0.02 | +0.19 | -0.04 | -0.01 |
| against October 2024 alone | -0.13 | -0.16 | -0.20 | none | -0.09 |
| at the level 15.0 | -0.08 | -0.23 | -0.16 | -0.24 | -0.18 |

- **Cloud.** The twilights of October 2022 scatter more than in the flank Octobers at all five, clearly at
  two (Mount Martha 0.47° against 0.22° and 0.34°; Malargüe 0.60° against 0.32°). Mount Martha has no moonless
  night that month and Mudgee has none clear of five. Among the brightest quarter of twilights all five
  stand at -0.14 to -0.26.
- **The Octobers compared with.** October 2021 is brighter than October 2024 by 0.40 at Mount Martha, 0.18
  at Bahía Blanca and 0.11 at Martinborough. Against 2024 alone the dip is half gone.
- **The clean crossings make no difference** (the same figures to 0.01): the twilights are smooth, only
  darker. Sorting by the night beside it could not be done; half these months have no clear moonless night.

So the brightening was still there in October 2022 at these places, at perhaps half the strength of
September and November. A real weakening is not ruled out. A dip to nothing is not what the sky did.

Sentence for the page: "October 2022 looks like a gap at the places between 32 and 41 degrees south. It is
mostly cloud and one bright October of 2021: among the clearest twilights of the month these places are
still 0.14 to 0.26 magnitude brighter." (`tw15b.out` part B.)

### M5. The order of arrival is carried in outline, with two things to say

The first month of 2022 at -0.10 or below, the first of two in a row, and the same at -0.20
(`tw15b.out` part D):

| place | latitude | first at -0.10 | two in a row | first at -0.20 | two in a row | months before with no figure |
|---|---|---|---|---|---|---|
| Réunion | -21.3 | February | February | February | February | none |
| Atacama | -23.0 | April | April | April | April | January to March |
| Queensland | -28.3 | March | March | March | March | January |
| Arkaroola | -30.3 | April | April | May | May | none |
| Coonabarabran | -31.1 | April | April | April | April | none |
| El Leoncito | -31.8 | March | March | April | June | none |
| Mudgee | -32.6 | May | May | May | May | none |
| Malargüe | -35.3 | March | March | May | July | none |
| Mount Martha | -38.3 | May | May | May | May | March, April |
| Bahía Blanca | -38.7 | April | April | June | June | none |
| Martinborough | -41.2 | May | May | May | May | none |

The first of two in a row against latitude: correlation -0.62 at the 0.10 mark and -0.70 at 0.20 (later
towards the pole); about a month and a half for every ten degrees.

So your order stands in outline: February at 21 degrees south, March at 28, April near 31, May and June
from 32 to 41. Two things do not fit it and should be said:

- **Two places only bound the date.** The Atacama has no figure before April, and Mount Martha none for
  March or April. "By April" and "by May" are all they carry.
- **At the page's own mark of 0.10 the three South American places come a month or two before the
  Australian ones at the same latitude**: El Leoncito and Malargüe in March, Bahía Blanca in April, on
  figures of -0.10 to -0.17 that sit on the mark. At 0.20 the difference is gone.

Replacement: "The brightening reached Réunion in February 2022 and southern Queensland in March, the places
near 31 degrees south in March or April, and those from 32 to 41 degrees south by May or June: about a
month and a half later for every ten degrees further south. Two places have no figure for the months that
would fix it, and the three in South America show a faint start a month or two earlier."
(`tw15b.out` part D.)

### M6. What the lines are worth: the sheet is fair about V1 to V3 and V10, and too generous to "ten held"

- **V10 shows steadiness and nothing else.** 81 in 100 on my reduction (77 of 95; yours 75 of 94). The five
  northern photometers, where nothing happened, give 91 in 100 by the same rule (`tw15b.out` part E). So the
  line would hold with or without a southern brightening. What it does show is the size of the month-to-month
  scatter: an even month stands within 0.13 of the mean of its two neighbours two times in three, and up to
  0.39 off. That is a third of the effect, and the page's single months should be read with it in mind.
- **V1 to V3:** as the sheet says, a meter bright in May and July is bright in June.
- **Of the lines that could go either way, three stood at their marks, and so did the control.** (V5 and
  V6 had room: 7 of 9 where 5 to 8 pass, and 0 of 8 where two were allowed.)

| line | figure | mark | margin |
|---|---|---|---|
| V4 | June -0.44, August -0.43 | not brighter than -0.47 | 0.03 |
| V7 | Réunion, February 2022: -0.24 | -0.20 or below | 0.04 |
| V8 | 4 of 9 | 2 to 5 of 9 | the four are at -0.11 to -0.12; two more at -0.07 and -0.09 |
| V11 | one month out (December 2022, -0.10; yours -0.13) | one allowed | none |

- **V7 is the one new fact:** Réunion, at the volcano's latitude, was 0.24 brighter in February 2022, the
  month after the eruption, and 0.67 and 0.98 in March and April.

Other fair choices change verdicts as follows (`tw15.out` part A): clean crossings, none; the level 13.0,
V7 and V8 fail (Réunion -0.11; 1 of 9); evening alone, V8 fails (6 of 9); morning alone, V10 fails (73 in
100). V9 fails under every choice. The level 15.0 fails V2 to V4, but their marks were set for 14.0 and the
effect is larger deeper, so that says nothing.

So "ten held and one failed" is the true count, and of the five lines the sheet calls real tests, three
held narrowly and one of those (V4) held against its own heading.

---

## Minor

1. Two of the 332 files have a header and no rows (stars246 and stars391, August 2021). Seven more southern
   files give no figure for want of five crossings a side.
2. Counts differ from yours by a place-month or two (V10: 77 of 95 against 75 of 94), from my 400-second
   gap rule against your 200.
3. stars47 (Padova) gives me every month and you about half, for the same reason. It is the unfit control
   of my second report; V11 holds with or without it on my reduction.
4. `src/between.py` was last changed half a second before the sheet was written. Its fingerprint in
   `SHA256SUMS` is of the file as it stands.
5. December 2022 is the one month the northern five miss (-0.10). December is a poor month in the north too.

---

## 1. Sealing

File times, taken at 21:15:50 before I read any file under `data/tw3/` (`sealing15.out`):

| what | time (UTC) |
|---|---|
| `src/between_ref.py`; `between_ref.out` | 20:34:21.59; 20:34:22.72 |
| `src/between_fetch.py` | 20:35:31.77 |
| `src/between.py` last changed | 20:36:00.85 |
| `between_dry.out` (the scoring program on nothing) | 20:36:01.22 |
| the sheet born and last changed | 20:36:01.32 |
| `SHA256SUMS` | 20:36:01.34 |
| fetch log born; first file written | 20:36:14.13; 20:36:25 |
| partial reductions first written; last read by anything | 20:36:26.16; 20:36:26.16 (never since) |
| last file written; fetch done | 21:12:52 |
| final reductions written; first read | 21:12:52.76; 21:13:18.66 |
| `between.out` | 21:13:18.47 to 21:13:18.76 |

- All six fingerprints match the files and are on the board under 20:36.
- The partial reductions were never opened, and the first scoring run is the one at 21:13.
- The fifteen photometers are the sheet's. Every file is an even month of 2021 to 2024. The number on disk
  for each photometer equals the number the log says its folder lists: 332 in all.
- No even-month file of any of the fifteen is in the earlier folders (`data/tw/`, `data/tw2/`).

As before, the times cannot show whether anyone looked into a raw file by hand during the fetch, and they
are evidence and not proof.

## 2. The lines, mine beside yours

| line | mine | yours | verdict |
|---|---|---|---|
| V1 | 10 of 10 | 10 of 10 | held |
| V2 | -0.44 | -0.453 | held |
| V3 | -0.43 | -0.433 | held |
| V4 | June -0.44, August -0.43 (July -0.42) | held | held |
| V5 | 7 of 9 | 7 of 9 | held |
| V6 | 0 of 8 | 0 of 8 | held |
| V7 | -0.24 | -0.24 | held |
| V8 | 4 of 9 | 4 of 9 | held |
| V9 | October -0.02, December +0.14 | -0.015 and +0.131 | failed |
| V10 | 77 of 95 (81 in 100) | 75 of 94 (80 in 100) | held |
| V11 | 5 of 6 months within 0.08 | 5 of 6 | held |

Every month of 2022 and 2023 at each place is in `tw15.out` part B. It agrees with the table at the head of
`between.out` to 0.04 or better at nine places. Coonabarabran differs by up to 0.17 (January 2023), and I
have a figure for its November 2022 where you have none; those months rest on five to eight crossings.

## What was verified and what was not

Verified: the sealing; the list and the files; all eleven lines; the questions on V9, October 2022, the
plateau, the Atacama and the order of arrival, each from the files.

Not checked, or not possible here:

- `src/between.py`, `src/between_ref.py` and `between_dry.out` were not read line by line; I compared
  outputs.
- The Brier score.
- The weather itself. "Cloud" here means what the readings show: scattered twilights and no clear moonless
  night. That October 2022 was a wet month in eastern Australia is from my memory and not checked.
- Whether December 2024 at inland Australia is brighter for a reason (the 2024 eruption the literature note
  mentions) or by chance.
- Sorting twilights by the night beside them, which the files are too thin to carry.
- The page itself: the replacement sentences are for a page I have not seen in its next form.

## My files for this job (under `/home/agent1/night/check/`)

`sealing15.out` (times); `tw11_tw3.pkl` (my reductions of `data/tw3/`); `tw15.py`, `tw15.out` (the eleven
lines, other choices, every month at each place); `tw15b.py`, `tw15b.out` (December, October, the plateau,
the order of arrival, V10's worth, the Atacama).

---

# An evidence reading of the page with the months between written in

Added by the same checker. Started 21:26:56 UTC, 27 November 2026; finished 21:29:45 UTC (the limit was 20
minutes). The page read is `/home/agent1/site/tonga.html` as rebuilt at 21:26, sha256 begins
`88595cdfc571f67a`; a copy is in `check/page16/`. I read the 106 sentences that differ from the live page
(`check/page14/`), the new picture, `between_look.out`, and ran two checks of my own (`tw16.py`, `tw16.out`).

**Nothing serious, 1 moderate, 9 minor.** The new fold, the rewritten paragraphs and the picture are carried
by the output lines, and where your figure and mine stand side by side they are fairly set together.

## Moderate

### "It is mostly cloud" is flatter than the readings carry

The story: "October 2022 looks like a gap in the picture. It is mostly cloud: among the clearest twilights
of that month the southern places are still brighter."

The second half is carried (0.14 to 0.27 brighter on both reductions). For the first half I tried the one
sign of cloud the files hold that neither of us had used: the infrared column. I took the share of twilight
rows in which the enclosure is less than half as much warmer than the sky as on that station's clear
twilights (`tw16.out` part A):

| share of twilight rows under cloud, in 100 | October 2021 | October 2022 | October 2024 |
|---|---|---|---|
| Mudgee | 22 | 51 | 27 |
| Malargüe | 6 | 17 | 0 |
| Mount Martha | 32 | 43 | 38 |
| Bahía Blanca | 13 | 23 | 19 |
| Martinborough | 51 | 35 | 37 |

So October 2022 was cloudier than both Octobers compared with at four of the five, plainly so at Mudgee and
Malargüe, a little at Mount Martha and Bahía Blanca, and not at Martinborough. At Mount Martha the larger
part is the bright October of 2021 (against October 2024 alone it is 0.20 brighter). "Mostly cloud" is right
of Mudgee and more than the files carry of the five together.

Replacement: "October 2022 looks like a gap in the picture. Part of it is cloud and part is one bright
October among the months compared with: among the clearest twilights of that month the southern places are
still brighter." (`tw16.out` part A; `tw15b.out` part B; `between_look.out` part H.) The fold can now say
that the files' own infrared column agrees at four places of five, in place of "neither of us has checked
the weather" standing alone.

## Minor

1. **The fold: "the lines which could have gone either way all stood near their marks."** Three of the five
   did (V4, V7, V8), and so did the control (V11). V5 and V6 had room: 7 of 9 where 5 to 8 pass, and 0 of 8
   where two were allowed. "Three of the five lines which could have gone either way stood near their
   marks, and so did the control" (my fourth report, M6).
2. **"Each figure within 0.01 or one place."** V10 differs by two place-months (77 of 95 against 75 of 94).
   "Within 0.01 or a place or two."
3. **The story: "half as bright again (50 on the first picture), with nothing to choose between the three
   months."** The picture and its alt text have 60, 50 and 49. "Half as bright again or a little more (60,
   50 and 49 on the first picture)" (`between_look.out` part A, "the middle, per cent").
4. **The fold: "June, July and August 2022 are level at the middle (-0.45, -0.42, -0.43)."** Those are the
   ten of the sheet. The eleven of the picture give -0.51, -0.44, -0.43. Say which.
5. **"About a month and a half for every ten degrees"** is my figure at the mark of two tenths; the rank
   correlation beside it is at one tenth. A clause would keep them apart.
6. **The alt text: "the middle of twenty northern meters stays within 10 of no change throughout."** March
   2022 is 0.12 magnitude darker, which is 10.5 per cent. "Within 11."
7. **Sources: "every month of fifteen of them."** The sixteen of the dawn page have every month too, and
   fifteen of those are in the new picture. Thirty-one have every month.
8. **"How far to trust this": "eleven predictions ... and ten held."** One of the ten held only in its
   wording, as the fold says. "Ten held, one of them only as worded" would carry it into the story.
9. **The fold: "runs more smoothly and somewhat higher."** "Somewhat brighter" is what the figures say.

## What you asked, in order

1. **The new fold.** The table agrees with `between.out` line by line, and the bracketed odd-month figures
   with `between_ref.out`. The Brier score is 0.159 by my own sum of the eleven odds, and the odds expect
   7.6. The six paragraphs give my findings as I gave them, bar minors 1 and 2. Side by side: V4 by 0.02 on
   yours and 0.03 on mine; October's clearest quarter 0.16 to 0.27 and 0.14 to 0.26; December's "about half"
   (yours 0.13 to 0.075 at the middle of the eight, mine 0.14 to 0.08). All three pairs use one definition
   and are fairly set together.
2. **The story.** The order of arrival is carried (part B of your output is my table, place for place).
   Réunion's April is 0.98 to 1.00 magnitude, which is two and a half times; it rests on April 2021 alone.
   "At the four places that have later years it has stayed there" is carried: 47 months of 2025 and 2026,
   the middle -0.01, 41 within 0.10. For October, see the moderate finding.
3. **The picture.** It shows what the caption and alt text say: near nothing through 2021, 10 below in
   January 2022, 25 in April and May, 60, 50 and 49 in June to August, 8 in October, about 40 in November
   and December, 17 to 34 to July 2023, then nothing, 13 below in December 2023. One pale line reaches about
   165. The line that leaps before the eruption and sinks at the end of 2024 is Malargüe, and it now has two
   faulty months of 2024. See minor 6 for the north.
4. **"How far to trust this."** Fair. Five of seven is the right count: Malargüe failing, Coonabarabran
   oddly mounted, and Queensland, the Atacama and Réunion on one year. "Most of them show only that the
   measure is steady ... the one new fact is Réunion's February" is what I found. See minor 8.
5. **The fold on the eleven places and the readers' fold.** The paragraph on the five weaknesses is my M1 as
   given, with Martinborough's start. The counts month by month agree with your part A and with mine. The
   January paragraph gives my half-month figures rightly. What is said of my fourth report is right.
6. **Made untrue by the even months and not changed.** I found nothing untrue. The paragraph on the Sun's
   depth is still right for July, and June and August say the same (`tw16.out` part B): at the middle of
   the eleven the twilight is 31, 58 and 99 per cent brighter at the three depths in June, 24, 49 and 92
   in July, 27, 48 and 84 in August, and brighter at the deepest level than at the shallowest in all 32
   place-months. If you want it to match the box: "From June to August 2022, at the middle place, the sky
   overhead was a quarter to a third brighter with the Sun six degrees down and nearly twice as bright with
   the Sun at seven and a half." The list "What this page does not show" is right as it stands.

## Not looked at

`src/between_look.py` itself; part C of its output (the twenty northern photometers month by month), which I
did not recompute; sentences that did not change; the visitor's reports; the page at phone size.

---

# A last evidence reading after the cut

Added by the same checker. Started 21:37:59 UTC, 27 November 2026; finished 21:40:12 UTC (the limit was 15
minutes). The page read is `/home/agent1/site/tonga.html` as rebuilt at 21:37, sha256 begins
`6c56ca551fe96b80`, 51,356 bytes; a copy is in `check/page17/`. I read every sentence of the box and the
story, both pictures as redrawn, and ran one check of my own (the last part of `tw16.out`).

**Nothing serious, 1 moderate, 3 minor.** Every other sentence of the box and the story is carried by an
output line.

## Moderate

### "No other northern meter brightens for months, evening and morning alike" has one exception at three months

The cut dropped the third condition (more the deeper the Sun), so the sentence now rests on months alone.
With every month in hand for twenty northern meters, I counted the longest run of months in a row at 0.10
magnitude brighter or more through 2022 and 2023 (`tw16.out`, "RUNS OF BRIGHT MONTHS"):

| | three months or more in a row | five or more | evening and morning each, five or more |
|---|---|---|---|
| the eleven southern | 11 | 11 (runs of 5 to 19) | 9 |
| the twenty northern | 3 | 0 | 0 |

The three northern ones: the ring road from November 2022, which is one of your four; Padova from May 2022,
in the evening only; and Otlica in Slovenia, January to March 2022 (-0.27, -0.23, -0.17, evening and morning
both). Otlica is not among the four the story names. Its winters swing by half a magnitude either way
(+0.48 in December 2022, +0.52 in January 2023, -0.39 in February 2023), so I take the run for winter
weather, and it comes before the south began. But as written the sentence is not quite true.

Replacement: "No other northern meter brightens for more than three months running; every southern one did
for five or more." (`tw16.out`, "RUNS OF BRIGHT MONTHS".) The Toulouse meter is not in this count, having
only every second month; the story already sets it apart.

## Minor

1. **"One meter from each part of the southern map where I had none. That gave seven."** The cut dropped
   "and a meter had the months needed". Fifteen parts were tried and seven had such a meter
   (`tonga_fetch.log`, `tonga_fetch2.log`). "One meter from each part of the southern map where I had none
   and one had the months needed."
2. **"Since the twilight fades at a steady rate."** It fades by a steady factor for each degree the Sun
   sinks (1.2 to 1.4 magnitudes), which is what lets a difference in degrees be turned into per cent. "At a
   steady rate" could be read as so much light a degree. "Since the twilight fades by the same factor for
   every degree the Sun sinks" is exact (the fold "How it was measured").
3. **The second caption: "the lowest orange dot is a meter with one odd month."** Right, and it is the one
   you take it for: the second meter at Coslada, whose September 2022 reads a magnitude darker. Worth naming
   in the fold on the north if it is not there already.

## The sentences you marked, in order

1. **The box.** "50 to 60 per cent brighter at a typical place" from June to August: 60, 50 and 49
   (`between_look.out` part A, "the middle, per cent"). "At most places it lasted into the middle of 2023":
   6 of 10 in June 2023, 7 of 11 in July (the same part, "at -0.10 or below"). "No northern meter shows the
   same thing": none of thirty-six at three levels (`tw13.out` part B), and none of twenty with every month
   has five bright months in a row. "By accident at four places and then tested it at seven more": right.
2. **"What I was looking for."** Six and a half degrees is right (6.1 to 6.9 at the sixteen; 6.7 at the
   middle of the southern eleven). The dim meter and the brighter sky are each the right way round. See
   minor 2.
3. **The first caption.** Right. The failing meter is Malargüe; its line is low at the end of 2024 and, by
   the same comparison, high at the end of 2021. The picture now draws the pale lines only between months
   next to each other, and that line shows as two short pieces.
4. **"Seven more places."** Three Australian states is right (Victoria, New South Wales, Queensland); the
   Atacama is in Chile. "By 17 to 86 per cent, and less so towards the far south": 0.56, 0.43 and 0.27
   magnitude at 21 to 23, 28 to 33 and 35 to 41 degrees south (`tw12b.out` part B). The four northern marks
   and "something local, since its neighbours show little or nothing" are carried. For the last sentence see
   the moderate finding.
5. **"When, and how much."** First on Réunion in February and last in the far south by May or June: carried
   (`tw15b.out` part D). "Partly cloud": carried (`tw16.out` part A). "About a quarter at a typical one"
   through the first half of 2023: 27, 34, 17, 25, 24, 19. "At every one of the eleven places, the deeper
   the Sun had sunk, the larger the brightening": 11 of 11. "And so does the one near Toulouse": its figure
   is 0.33, 0.31 and 0.34 at the three depths.
6. **"How far to trust this."** Both sentences are right. Five of seven: three found by me, two from your
   table and my withdrawn sentence. Two visitor folders are on the machine; I did not read them.
7. **The pictures.** The first has "south" and "north" on the right lines, the eruption marked, and the
   figures of its alt text. The second names Réunion at the dot at 21 degrees south and 74, and New Zealand
   by a leader to the dot at 41 degrees south and 17; the triangle is labelled as the broken meter off the
   scale; the lowest orange dot stands at about 18 below. Both alt texts still fit.

## Not looked at

The folds, beyond the output lines the story's sentences rest on. The visitors' reports. The page at phone
size. Whether the moved paragraph reads rightly in its new place.
