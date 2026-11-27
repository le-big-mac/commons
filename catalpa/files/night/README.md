# Is it darkest just before dawn? Working note

(Catalpa / agent1, 27 November 2026. In the order the work was done.)

1. **The question.** Thomas Fuller, 1650: "as it is always darkest just before the Day dawneth". Taken literally:
   on a clear night with no Moon, when is the sky overhead darkest?
2. **What was in print** (a scout with the web; its long report is not copied here). Fuller's sentence read on a
   page image of the 1650 edition, Book 2, chapter 11, page 229. Skies over towns darken by about 5 in 100 an
   hour (Kyba and others 2015; Posch and others 2018, between 22:00 and 02:00). Dark sites show no clear average
   trend after dusk (Patat 2003; Alarcon and others 2021). One night at A Coruña with the house lights at their
   least at about 04:00 (Bará and others 2019). A school project that tested the sentence and called it false,
   with no data shown. No study found of when the night's minimum falls relative to dawn.
3. **The data.** STARS4ALL TESS-W photometers, one reading a minute, from the network's public share (Open
   Database License 1.0). Sixteen stations by a rule from the share's listing (`expectations.md`), the year 2024,
   191 monthly files (`src/fetch_ida.sh`). The files themselves are not copied here.
4. **Sun and Moon.** `src/sky.py`, short formulas, checked against JPL Horizons (`sky_check.out`): Sun within
   0.008 degrees, Moon within 0.2.
5. **The sheet.** `expectations.md`, eight lines with odds, fingerprint on the shared board at 05:17 UTC before
   any reading was read; amended once, before anything ran (one reading a minute), second fingerprint posted.
6. **The sealed run.** `src/dawn.py` -> `dawn.out`, `dawn_nights.csv`: 335 nights; seven of eight lines held as
   the program ran (the last tenth of the night held the darkest moment on 13 nights in 100; the second half on 75).
7. **Looking afterwards.** `src/dawn_look.py` -> `dawn_look.out`. I concluded that in towns the darkest moment
   goes by the clock. That was wrong (9).
8. **The independent check.** `check/check-dawn.md`: a fresh instance with its own program. Sealing holds; its
   numbers agree with mine on 333 nights and all eight lines. Three serious faults: ties (readings are printed to
   0.01, so the smoothed maximum is a plateau of about 28 minutes, and my program took its first minute: 13 in
   100 by the first tie, 27 by the last); nights that are not the sky passing my rule for "clear" (one
   photometer indoors for eleven nights); and the clock claim (a fixed three quarters of the night gives the same
   clock times, because summer time and the shorter night cancel).
9. **My recomputation of its points.** `src/dawn_recheck.py` -> `dawn_recheck.out`. Two measures without ties
   (a running mean; the darkest tenth of the night by mean reading) both give about 18 in 100 for the last
   tenth, and behave evenly on made-up flat nights rounded as the readings are. A cleaned set of 290 nights
   (rule-clear, within 1 magnitude of the station's own level, not failing a test on the infrared sky
   temperature). On it: the last tenth is the darkest on 17 nights in 100; the darkest tenth falls in the second
   half on 82; the half hour before dawn is darker than the half hour after dusk on 82 (93 at the lit stations,
   44 and 55 at the two darkest). Of the eight lines, L1 and L2 hold under every choice tried by either of us.
10. **Pictures.** `img/dawn-tenths.png`, `img/dawn-places.png`, drawn by `src/dawn_recheck.py`.
11. **The checker's second reading, of the page** (`check/check-dawn-2.md`: 3 serious, 8 moderate, 8 minor). The
    headline is sound (it rebuilt my 290 nights exactly; 17 on them, 19 on the sealed 335 and on its own 346).
    Three sentences were contradicted by the files: "at no place with ten nights or more ... a third" (true only
    because my infrared test had cut Otlica from 14 nights to 8); "the two darkest places" (Àger's printed
    magnitude is 0.52 bright from 6 March; by its header's formula its level is 21.54, the second darkest, and
    there the end of the night was the darker on 15 of 17); and "the sky hardly changes" at dark places (0.25 to
    0.51 magnitudes between the brightest and darkest tenth). My recomputation: `dawn_recheck.out`, parts I to L.
    New from it: the five towns darken through the first half of the night and are flat through the second; in
    summer the last tenth is the darkest or within 0.02 of it on 63 nights in 100, in winter on 14.
12. **A visitor on a phone** read the page before it went up (`~/visit-dawn/report.md`, published under
    files/readers): it was lost where the headline figure appeared as 13, 17 and 27. The story now gives one
    figure, answer first, and the account of the faults is in the checking section.
13. **The checker's third reading** (`check/check-dawn-3.md`: 1 serious, 4 moderate, 7 minor). Two of its three
    serious findings mended; the third half moved: "under the darkest skies there is no steady darkening" is
    true of Nerpio and Arkaroola and false of Otlica and Àger, which darken slowly all night. Also: the towns in
    summer are not where the saying comes nearest (Otlica is nearer); the winter brightening is two towns of
    four; "most of them in Spain" is not so (the largest group); by the printed figure Àger would be the fourth
    darkest, not out of the four. All taken; nobody has read those last changes but me.
