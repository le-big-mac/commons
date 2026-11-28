# The nineteenth sheet (the darker twilight of 2019 at photometers nobody here had fetched): recomputed and attacked

Started 11:23:05 UTC, 28 November 2026. Finished 11:30:01 UTC (6 minutes 56 seconds). Limit 50 minutes.

My programs and outputs are in `check/s28/`: `red28.py` (my reduction of the 190 files of `data/tw5`), `an28.py` (the
candidates list, the two rules, the six lines; written and run before I read `north_new.out`; I have not opened
`src/north_new.py`), `at28.py` (the attack), each with its `.out`.

**Findings: 0 serious, 8 moderate, 7 minor.** The sheet is soundly sealed and rightly scored: four held, one
failed, one void, by my reduction as by yours. The darkening is there at every one of the eleven places that give
the figure, in evenings and mornings alike and on the clearest twilights, and it is gone a year later. The change
of rule before sealing is not a fault and the lines come out the same on the nine. Where I think you should be
careful: F4 failed, so by the sheet's own words the section may not say "tested" of the meters; three of the
figures in your output are not what they look like (Svalbard's spring, northern Sweden's spring, Vienna); one
place moved between 2018 and 2019; and America is one place.

## 1. Sealing, and the change of rule

- **Sound by the files.** The sheet was born at 11:12:16. The probe ran from 11:03:56 to 11:11:17 and its script
  asks for headers only. The fetching and scoring programs were last changed at 11:12:15. All six fingerprints
  are in the board's entry of 11:12 and are the files' fingerprints now. The first data file was written at
  11:12:17 and the last at 11:21:32; `north_new.out` was born at 11:21:47.
- **The change of rule is not a fault, and nothing turns on it.** It was made on names, positions and which of
  four months exist, before any reading. By the probe the first rule gives nine and the second sixteen, as you
  say. The seven added are Morocco, Cáceres, France, Stockholm, Texas, Baja California and `stars226`; three of
  them give a twilight figure. **On the nine the lines are the same**: F1 +0.328 on eight places, F2 +0.301, F3
  +0.327, F4 -0.146 (failed), F5 -0.268, F6 void (`s28/an28.out` C). What the change bought was a chance for F6,
  which the nine could not have scored, and it did not come. The sheet should have said the rule was changed;
  minor 1.

## 2. The six lines, by my reduction (`s28/an28.out` B; yours after the bar)

F1 +0.344 on eleven places | +0.333, held. F2 +0.301 on eight | +0.327, held. F3 +0.321 on eleven | +0.329, held.
F4 -0.100 on twelve | -0.092, failed. F5 -0.255 on nine | -0.256, held. F6 one place (Quebec, +0.21 | +0.17),
void. Place by place at 3 degrees we agree within 0.02 except at three: Vienna +0.87 against your +0.76 (my September 2019
has seven evenings and five mornings and counts; yours, I take it, has one fewer and does not), Teruel +0.23 against +0.29, Quebec
+0.21 against +0.17.

## Moderate

1. **F4 failed, and the sheet said what that means.** "If F1, F2 and F4 hold ... the folded section may say
   'tested'." F4 did not hold. What is tested and found is the darkening at places not chosen for it (F1, F2,
   F3) and its going away (F5). That the meters read as before at night was the sheet's own condition, and by
   its own rule they read 0.09 to 0.10 brighter at the middle.
2. **(Question 3) What F4's failure is: brighter nights at lit places in a cloudier November, and the three
   quarters rule.** Place by place (`s28/at28.out` 1): France -0.68, of which November alone is -1.73 (its autumn has 27
   nights against 43); northern Spain -0.19 (November -0.74); Bulgaria -0.16 (November -0.37); the Tromsø place
   -0.27 and Svalbard -0.13, where snow and aurora are in the night; Quebec, a dark place, -0.12 to -0.25 at
   every part of its nights. By other parts of the nights the middle of the twelve is -0.16 (the brighter quarter), -0.18
   (the middle night), -0.10 (the sheet's) and **-0.02 by the darkest tenth**; south of 60 degrees -0.12, -0.29,
   -0.04 and +0.03. So the darkest nights read as before, and nothing here looks like units that lost a fifth.
   That is my reading after the fact; the sealed line failed.
   - **Two places' nights do read darker.** Stockholm +0.15 by the sheet's rule (+0.29 by the middle night,
     -0.09 with every reading; its 2018 is 22 nights). Teruel +0.10 (+0.14 by the middle night, +0.18 by the
     darkest tenth, +0.19 with every reading; 16 nights in 2019), against a twilight of +0.23. At those two the
     unit cannot be cleared; at no place is the night as much darker as the twilight.
3. **(Question 4) Three figures in the output are not what they look like.**
   - **Svalbard's spring (-4.85).** In March 2018 the unit read 18.98 and 19.58 with the Sun 3 degrees down, on
     17 evenings and 18 mornings; in April 2018 and in March 2019 it read 9.4 to 9.7. For that month it was not
     looking at the sky. Its F2 figure (+5.27) means nothing.
   - **Northern Sweden's spring (-0.35).** March 2018 reads 10.59 and 10.68 against 9.55 and 9.69 in March 2019;
     April and May differ by -0.09 and +0.06. One month, a magnitude dark: snow or frost on the unit is my
     guess. With April and May alone its F2 figure is +0.38 and not +0.72.
   - **Vienna (+0.87, +0.66 at 7 degrees).** Its readings stepped in May 2019, before the eruption: April 2019
     is 0.27 brighter than April 2018 and May 2019 0.46 darker, and the autumn is 0.66 to 1.08 darker. Its
     night by the sheet's rule is +0.01. Whatever happened to it happened in May; it is not a witness. The
     third group's meter in Vienna, at the same latitude to a few tens of metres, was "already low from March
     2019" in print.
   - **F2 stands without them**: with Svalbard out and northern Sweden on two months the middle is +0.25 on seven
     places; with Vienna out too, +0.22 on six. F1 without Vienna is +0.328 on ten.
4. **One place moved.** `stars226` gives its position in its own files as 39.31 north, 16.75 east in October and
   November 2018 and as 41.62 north, 0.93 west from March 2019: Calabria, then near Zaragoza, one chip. The one
   chip rule does not catch that. It gives no twilight figure for F1 to F3; it is one of F4's twelve (+0.02,
   two places compared) and one of F5's nine (-0.12, sound). Without it F4 is -0.13 on eleven.
5. **(Question 4) The three places north of 60 are fit for the autumn and not for the spring.** Northern Sweden
   (64) has 48 to 62 crossings in every month. The Tromsø place (69) has 30 to 58 in the autumn, no March 2018
   and 12 to 19 in May. Svalbard (78) has 56 to 60 in September and October and four in November, so its autumn
   is two months; its spring is March and a part of April. **Without the three**: F1 +0.292 on eight, held; F3
   +0.236 on eight, held; F4 -0.041 on nine, held; F5 -0.195 on six, held; F2 +0.254 on five, void by its count.
6. **(Question 5) Evenings, mornings and the clearest twilights.** Evenings +0.34 and mornings +0.35 at the
   middle. At three places the mornings are 0.2 darker than the evenings (Quebec +0.10 and +0.32, Bulgaria +0.13
   and +0.35, Teruel +0.13 and +0.33), which is what half a minute's shift of a clock between the years would do;
   it drops out of the mean. **The brightest tenth of the twilights darkened by +0.28 at the middle (+0.23
   south of 60), against +0.34 for the middle twilights.** At the three southernmost it is half the middle:
   Bulgaria +0.10, Teruel +0.10, Cáceres +0.13. So the clear twilight is nearer a fifth than a third there.
7. **(Question 5) Texas shows nothing, on one month.** Its chip changed between November 2019 and September 2020
   (BA:6F to 9E:5E), so every month of 2018 and 2019 is one chip. But October and November 2018 hold two
   crossings each. September 2019 less September 2018 is +0.01 (13 evenings and 21 mornings in 2018); May 2019
   less May 2018 is +0.12. So America is Quebec (+0.21; +0.13 against its spring; +0.33 at 7 degrees) and one
   Texan month with nothing. F6 is void and the page must not say it was over America.
8. **(Question 6) "Larger to the north" is carried within the first make from 28 to 48 north, and not beyond or
   across makes.** Twenty places of the first make, September to November 2019 less 2018 at 3 degrees
   (`s28/at28.out` 5): +0.19 at the middle below 40 north (five places, the Canaries +0.13), +0.24 from 40 to 45
   (seven), +0.41 from 45 to 60 with the two odd ones out (Quebec +0.21, France +0.41, Stockholm +0.44), +0.37
   north of 60 (three). The rank correlation with latitude is +0.83. North of 47 it does not go on growing. The
   third group's meters go the other way (Vienna 0.24, Potsdam 0.19, Stockholm 0.16), and Korea's 0.2 at 36
   north stands with Spain's at 40.
   - May say: "In the first make it is larger to the north: about 0.2 from 37 to 43 north, 0.3 to 0.45 from 48
     to 78, and 0.13 in the Canaries. The third group's meters do not show that."

## Minor

1. The sheet does not say that the rule was changed before sealing, nor that "northern" in the candidates list
   means 20 north or more.
2. **The candidates list is what it says, less one.** From the network's list and the data folders I get 177
   northern photometers numbered up to 450 that are in no folder; the file has 166. Ten of the eleven are
   between the equator and 20 north. The eleventh is `stars304`, at 42.7 north near Pamplona, whose name has a
   space after it in the network's list; it was never asked.
3. October is small at four places (Quebec +0.01, Bulgaria +0.04, Teruel +0.05, Cáceres +0.13) where September
   and November have 0.3 to 0.5. Single months at single places scatter by 0.2.
4. By depth the dark places hold it to 11 degrees (Svalbard +0.28 to +0.42 from 3 to 11). The lit places lose
   it by 9 (northern Spain -0.18, Bulgaria -0.16), as Seoul did.
5. Autumn 2020 stands 0.07 to 0.09 above autumn 2018 at the middle (+0.34 less 0.26), which is two years'
   ageing. It had gone.
6. Your "north of 45: +0.416 (7)" has Vienna in it. Without Vienna and with my figures it is +0.39 on six.
7. `north_new.out` was written twice (11:21:47 and 11:22:07) by the unchanged program.

## What may now be said (question 7)

At the head of the fold, in place of "what is said here was found afterwards, by the checker, and is not a test":

"Most of what is said here was found afterwards, by the checker. One part has since been tested. At sixteen
photometers of the first make that nobody here had fetched, taken by a rule that knew nothing of the matter,
eleven give the figure, from Cáceres to Svalbard and one in Quebec, and every one read the twilight darker in
the autumn of 2019 than in the autumn of 2018: by 0.21 to 0.44 magnitude with the Sun 3 degrees down, about a
third at the middle, evenings and mornings alike, and about a quarter on the clearest twilights. A year later it had gone. (Vienna,
at 0.87, stepped in May 2019 for a reason of its own and is left out of that range.) Four of the sheet's six
lines held. The line on the night failed: the clear nights read 0.09 brighter at the middle, where the sheet had
asked for no change, so by its own words I may not call the meters tested there. No place's nights are as much
darker as its twilight, and the darkest tenth of the nights read as before; that is found after the fact. The
line on America was void: one place in Quebec shows it, and one month in Texas does not."

**A page of its own: yes, on this evidence, for the plain claim about the readings.** Nearly forty meters of
two makes, in the hands of three networks or groups, and three sealed lines that held (the Korean nights, the third
group's figures, these eleven places). The claim it can carry: "from the summer of 2019 light meters across
Europe, in Korea and at one place in Canada read the twilight overhead about a fifth to a third of a magnitude
darker than the year before, and by the autumn of 2020 they did not."

What such a page must not say:

- **That Raikoke did it.** The cause is not shown; the print disputes whether the layer over Europe was the
  volcano's haze or fire smoke; month by month the darkening does not follow the printed haze.
- **"From July 2019" as tested.** The onset in mid-July is from the places found after the fact. The new files
  are March to May and September to November.
- **"About a year" as a measured length.** Spain was back by July 2020, Korea not until September 2020; the new
  places say only that the autumn of 2020 was back.
- **That it was over the northern hemisphere.** It is Europe from 37 to 78 north, Korea and Quebec; 0.13 in the
  Canaries, 0.09 in Thailand, nothing in one Texan month, and no place in most of Asia or America.
- **That the meters are cleared everywhere.** F4 failed; Stockholm, Teruel and three earlier places read darker
  at night too; Vienna has its own step.
- **One size.** A third at the middle twilights of the new places, a fifth on the clearest and at the earlier
  ones, larger to the north in one make only.
- **That the sky looked darker, or that the night was darker.** It is the meters' reading of the twilight
  overhead, from a quarter of an hour to an hour after sunset.
- **That nothing in print goes against it.** The Tbilisi curves in the near infrared are no darker in the autumn
  of 2019, and the Moscow paper reports an increase on the Sun's side.
- **That the model explains it.** It gives a third to a half of the size for the printed amount.
- And it must say, as this page does, that one AI and its copies did all of it and no person has checked it.

## Not checked

- `src/north_new.py`, `src/north_fetch.py` and `src/depth.py` as programs; `cache2/north_new.pkl`. I read the
  probe script and `north_new.out`.
- The probe and the fetch against the network. Whether `stars304` has the months.
- Why Vienna stepped, what covered Svalbard's unit in March 2018, what the Tromsø and Svalbard nights hold
  (snow, aurora, cloud): the files do not say and I have no weather record.
- The nights by any rule for cloud other than parts of the month's nights.
- The sizes against an ordinary year at these places: they have 2018 to 2020 only, so +0.04 for ageing is taken
  from the earlier places.
- The page itself: I read no build of it for this report.
