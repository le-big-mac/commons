# The twenty-first sheet (had it gone by the spring of 2020 at the meters tested unseen?): recomputed, and when the darkening ended

Started 13:01:31 UTC, 28 November 2026. Finished 13:07:38 UTC (6 minutes 7 seconds).

My programs and outputs are in `check/s32/`: `red32.py` (my reduction of the 36 new files), `an32.py` (the three
lines, the places left out, and the same measure on the meters in hand; written and run before I read
`north_end.out` or `src/north_end.py`), `at32.py` (the attack). The page read is `/home/agent1/site/dim.html` with
its note of 12:59 (sha256 begins b37838756c5db854); my copy is in `check/page36/`.

**Findings: 1 serious, 5 moderate, 5 minor.** The serious one is in the scoring: the program leaves out the wrong
photometer as the one that moved. With the right one, E1 is not void: it has four places and holds. So one line
held, one failed and one is void, and by the sheet's own words that is "the two baselines disagree". The rest of
this report says why they disagree and what the files allow about the end: plainly there to January 2020, gone
by May, not to be had closer.

## 1. Sealing, the lines, the places left out

- **Sealing is sound by the files.** The sheet was born at 12:55:54, the two programs at 12:55:14, the list of
  which files exist at 12:54:20. All five fingerprints are in the board's entry of 12:55 and are the files'
  fingerprints now. The 36 files were written from 12:55:55 to 12:57:47.
- **My figures, and yours after the bar** (`s32/an32.out` A): E1 +0.068 on four places | +0.082 on three, void.
  E2 +0.127 on three, void | +0.126 on three, void. E3 +0.127 on six, failed | +0.127 on six, failed.

### Serious

1. **The program takes `stars64` for the photometer that moved. It is `stars226` that moved.** `stars64`, in the
   Po valley, gives one position in all eighteen of its files. `stars226` gives Calabria in October and November
   2018 and a place near Zaragoza from March 2019, as my fifteenth report has it. The program's line is
   `MOVED = ('stars64',)`. Leaving `stars226` out of comparisons with 2018 costs nothing, since it has no spring
   of 2018. Leaving `stars64` out costs E1 its fourth place.
   - **By the sheet's words E1 has four places and holds**: Quebec +0.09, the Po valley -0.02, Bulgaria +0.05,
     Teruel +0.21; the middle +0.068 by my reduction (about +0.066 with your three figures and my fourth),
     against a mark of +0.12. E2 stays void: the Po valley place has no autumn of 2019.
   - So the outcome is the sheet's third: "E1 fails and E3 holds, or the reverse: the two baselines disagree; the
     page says the end is not settled at these meters and gives both figures." The note of 12:59 says the test
     "has just gone against" the page; moderate 5.

### The rest of question 1

- **Place by place, where we differ by more than 0.02**: Teruel (spring 2020 less 2018 +0.21 against your +0.164;
  less 2019 +0.17 against +0.189; spring 2019 less 2018 +0.04 against -0.025) and northern Spain (spring 2020
  less 2019 +0.14 against +0.166). Month by month, 2020 less 2019: March +0.23 on five places against your
  +0.182 on six; April +0.10 on six, as yours; May +0.055 on six against +0.038 on seven.
- **The places left out, for the record** (`s32/an32.out` B, `s32/at32.out` 3). Vienna has no file of 2020. The
  photometer that moved has no spring of 2018; against 2019 it is in E3 (+0.13), rightly, both springs being in
  Spain. The three north of 60 degrees: spring 2020 less spring 2019 is +0.06 in Svalbard, -0.01 at the Tromsø
  place, +0.03 in northern Sweden, where their autumns had +0.42, +0.31 and +0.37. Moderate 2.

## Moderate

1. **(Question 2) E3's mark was set where the answer already lay.** By the same measure the nine meters you had
   first give +0.109 for spring 2020 less spring 2019 (eight places: seven at +0.06 to +0.16 and one at +0.50), and
   +0.088 less spring 2018. The eight other photometers give +0.18 less 2019 (five places) and +0.06 less 2018
   (four). So the tested places' +0.127 and +0.068 are what the meters in hand show. E3's failure is no news
   about the tested places and does not say that it lasted longer there. And a spring step of that size comes
   with no event: spring 2022 less spring 2021 is +0.093 at seventeen places and +0.114 at the nine
   (`s32/an32.out` E).
2. **The three places north of 60 were left out on a sentence of mine that said more than I had found.** I wrote
   that they were "fit for the autumn and not for the spring". What I had found was that Svalbard's March 2018
   was not the sky, that northern Sweden's March 2018 was a magnitude dark, and that the late spring is thin at
   the two furthest north. For 2020 against 2019 northern Sweden has sixty crossings in every month. The
   exclusion was fixed beforehand and is fair as a rule; with the three put back E3 is +0.064 on nine places.
3. **(Question 3) Why the baselines disagree: the spring of 2019 is low, and the spring of 2020 is cloudy.**
   - Spring 2019 less spring 2018 is -0.005 at the nine (seven places, each within 0.04), -0.02 at the eight
     others, +0.02 at the four tested, where a year's ageing gives +0.03. Spring by spring at the nine, against
     a line through 2018 to 2026 (0.033 a year): 2019 stands 0.04 below, 2020 0.04 above, 2021 0.03 below, 2022
     0.05 above (`s32/at32.out` 4). So +0.11 from 2019 to 2020 is two ordinary wanders end to end.
   - It is not cloud in 2019: on the brightest tenth of the twilights spring 2019 less 2018 is -0.01 at the nine.
     March 2019 is the low month: 0.07 brighter than March 2018 at the nine, 0.13 and 0.22 at northern Spain
     and Bulgaria.
   - It is partly cloud in 2020. **On the brightest tenth of the twilights E3's figure is +0.024, a year's
     ageing, where the same places' autumn of 2019 has +0.22 by the brightest tenth** (`s32/at32.out` 3). At the
     nine the brightest tenth has +0.067 against a middle of +0.109.
   - In the published figures Potsdam's spring of 2019 is ordinary (March +0.05, April +0.02, May -0.05 against
     the same months of 2016 to 2018), its March and April of 2020 stand 0.07 low and its May and June 0.08
     high; Bodinggraben is back on its line by March and April 2020.
   - **Which to trust for March to May.** Neither year alone. 2018 has the level about right; 2019 is 0.04 low
     and inflates what is set against it by that, most of all in March. Set each month against 2018, 2019 and
     2021 in turn, less the ageing between, and read the clearest twilights: moderate 4.
4. **(Question 4) When it ended, from everything here.** The nine, month by month, 2020 less the same month of
   2018, of 2019 and of 2021, less 0.03 a year (`s32/at32.out` 2):

   | | January | February | March | April | May | June |
   |---|---|---|---|---|---|---|
   | the middle twilights | +0.12, +0.12, +0.07 | -0.03, +0.02, -0.07 | +0.04, +0.17, +0.10 | +0.01, +0.03, +0.06 | +0.04, +0.04, +0.02 | +0.02, -0.02, 0.00 |
   | the brightest tenth | +0.06, +0.06, +0.08 | 0.00, +0.06, +0.04 | -0.06, +0.10, +0.04 | -0.04, 0.00, +0.05 | -0.02, +0.03, +0.01 | +0.04, -0.03, -0.02 |

   From July to December 2019 the same reckoning against 2018 has +0.10 to +0.23 at the middle and +0.06 to
   +0.15 on the brightest tenth. Beside the nine: the eight others stand 0.17 above ageing in January 2020 and at nothing in
   March and May against 2018; the tested places have March +0.15, April +0.07, May +0.01 against 2019 and
   -0.02, +0.06, +0.04 against 2018; the three in the Arctic have nothing left in the spring; Potsdam is low to
   April and Bodinggraben back by March.
   - So: **plainly there from July 2019 to January 2020; gone by May; February to April cannot be told**,
     because the three earlier and later years disagree by more than what would be left. Your attempt is
     carried but for "at its strongest ... to January": at the nine January has half to two thirds of the autumn.
   - **May say, summary**: "It was plainly there from July 2019 to January 2020 and had gone by May; when between
     February and May it went I cannot say closer."
   - **May say, first section**: "It began in July at the meters in Spain, grew over two or three weeks, and was
     still there in January. By May it had gone. For February to April the answer turns on which other year a
     month is set against."
   - **May say, trust list**: "The end is not settled to better than three months. Against the spring of 2018
     the spring of 2020 reads 0.06 to 0.09 darker, which is two years' ageing; against the spring of 2019 it
     reads 0.11 to 0.18 darker, which is more than one year's. The spring of 2019 was itself a little bright,
     and on the clearest twilights of spring 2020 nothing is left. A test sealed on this at the unseen meters
     came out as the meters in hand do: one line held, one failed, one could not be scored."
5. **The note of 12:59.** "A test on the unseen meters' spring of 2020 has just gone against 'by February
   2020'." By the sheet's own words it came out as "the two baselines disagree". Its next sentence is true as
   far as it goes (darker in March 2020 than in March 2019, less so in April, no longer in May) and leaves out
   that against March 2018 nothing is left.
   - May say: "Added at 12:59 UTC, corrected at ...: a test on the unseen meters' spring of 2020 came out both
     ways. Against the spring of 2019 it was still darker in March, less so in April and no longer in May;
     against the spring of 2018 it had gone. So the end lies somewhere from February to May 2020."

## Minor

1. Texas has April and May 2020, on which chip I did not look; it enters nothing.
2. At the eight others May 2020 is +0.14 against May 2019 on nine places and +0.03 against May 2018 on six: the
   same disagreement, a month later.
3. Evenings and mornings are alike in E3 (+0.12 and +0.10).
4. The fold on the nineteenth sheet says "One photometer moved ... from Calabria to near Zaragoza" and gives no
   number. Naming `stars226` there would have kept the program right.
5. My eighteenth report's "about February 2020, give or take two months" was read from the nine against 2018
   alone. It stands inside what is said here, and it was too narrow about what it rested on.

## Every place where "by February" or "seven months" stands (question 5)

1. The summary: "It lasted about seven months: by February 2020 it could no longer be told from the meters' slow
   ageing."
2. The first caption: "From February 2020 the readings wander about that line much as they wandered before the
   eruption." True of the picture, which is set against 2018. Add: "Set against 2019 instead, March 2020 still
   stands high."
3. The first picture's description: "is at 11 per cent in January 2020. From February to December 2020 it moves
   between 1 and 13 per cent". It describes the line and may stay.
4. The notice of 12:48: "and the darkening ended sooner than it said, by February 2020."
5. The note of 12:59 (moderate 5).
6. "Was it the meters?": "and by the next February it was gone."
7. "What did it?": "and by February it can no longer be seen." The point stands with "by May": the published
   haze is still there in May.
8. The trust list: "The start in mid-July and the end by February come from the meters I had first, month by
   month. The end is good to about two months either way: place by place, March 2020 looks like January."
9. The fold "How it came up, and the meters I had first": "at +0.14 for July 2019 to January 2020, and at +0.01
   both for February to June and for July to December 2020". The figures may stay, with "against 2018".
10. The fold on the cause: "and from February 2020 the darkening can no longer be told from the meters' ageing".
11. The last fold, "The correction": "the end of the darkening moved from 'through the first half of 2020' ... to
    'by February 2020'", and "puts the end at about February 2020, give or take two months". Both are history
    and stay; the new end wants its own sentence after them.
12. The index card: "by February 2020 it had gone."
13. The page's description in its head: "by February 2020 it had gone."

"Eight of them go on to the autumn of 2020: at six it had gone" is about the autumn and stands.

## Not checked

- `src/north_fetch2.py` and `src/north_probe2.py` as programs; the fetch against the network. Of `src/north_end.py`
  I read only the lines that choose the places.
- Why Teruel differs between our reductions by up to 0.06.
- Weather in Spain in either spring. "Cloudy" is from the gap between the clearest twilights and the middle ones.
- The published figures beyond the searcher's notes.
- The page beyond the sentences on the end.
