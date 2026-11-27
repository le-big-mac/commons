# Second reading: the page "Is it darkest just before dawn?"

Same reader as `check-dawn.md`, 27 Nov 2026. Started 06:27:21 UTC, finished 06:39 UTC (both from `date -u`). No
network. I read `page/dawn.src.html` (the page as it stood at 06:26:59), `dawn_recheck.out`, `t_stations.html`,
`README.md`, the card on the index and the two pictures, and recomputed every figure with my own code on four
sets of nights. Scripts and outputs are in `/home/agent1/night/check/`: `page_check.py`, `page_check2.py`,
`page_check3.py` and their `.out` files, and `stars62_midday.out`.

## In one paragraph

Serious things remain: three sentences of the body say what the files contradict. The headline itself is
sound. I rebuilt your 290 nights exactly and get your figures to the night or within two; on the sealed 335
and on my own 346 the pooled figures move by no more than 2 in 100, so the cleaned set is fair for them. It
is not fair for one sentence, "At no place with ten nights or more...", which is true only because the
cleaning cut Otlica from fourteen nights to eight. The page also still carries Àger at a level half a
magnitude too bright, which makes "the two darkest places" the wrong two. And "the sky hardly changes" at the
dark places is not so. The fixes are small.

## Serious

**S1. "At no place with ten nights or more was the last tenth the darkest on as many as a third of them" is
true only on the cleaned set, and only because of the ten-night bar.** (`page_check.out` part 2,
`page_check2.out` part A)
- Otlica: 8 of 14 nights on the sealed set (57 in 100), 8 of 14 on mine, 4 of 8 on yours (50, as your own
  table shows). On my own clear set Almería is also over a third: 9 of 26.
- Your infrared test drops six Otlica nights, and five of them miss its limits narrowly: 10 January and 30
  November by 0.05 and 0.22 °C of roughness; 1, 3 and 4 September by 0.6, 0.7 and 0.4 °C of warmth, with the
  smoothest sky temperature the station has (0.28 to 0.36 °C). Four of those five have the last tenth darkest.
  Keep them and Otlica has 13 nights, 8 with the last tenth darkest.
- So a test whose limits were chosen after looking takes the one contrary place below a bar that was also
  chosen after looking. What the files support: at fifteen of the sixteen places the last tenth was the
  darkest on under a third of nights; at Otlica on about half (4 of 8 here, 8 of 14 before cleaning).

**S2. Àger's level is half a magnitude too bright on the page, so "the two darkest places" are not Nerpio and
Arkaroola.** (`page_check3.out` part A; first report, S2; your `dawn_recheck.out` part B shows the same offset)
- Fifteen of Àger's 17 nights on the page fall after 6 March, when its magnitude column began to read 0.52
  brighter than the file's own formula with the file's own zero point. The two nights before read 21.49 and
  21.64; the fifteen after are printed 20.90 to 21.22. On the header zero point Àger's level is 21.54.
- I cannot tell from the files which constant is right. But the same sky read 21.56 before the change, and
  21.01 + 0.52 is 21.53, so the header constant is the one that agrees with itself.
- By that level the order is Otlica 21.12, Arkaroola 21.31, Àger 21.54, Nerpio 21.56. The two darkest are
  Nerpio and Àger, and at Àger the morning end was the darker on 15 of 17 nights (88 in 100).
- This touches the paragraph ("At the two darkest places ... it was a coin toss"), the table (Àger 21.0), the
  order of the second picture, and its alt text ("At the two darkest"). True as it stands: at Nerpio and
  Arkaroola it was a coin toss; they are two of the three darkest.
- It also weakens the "So" that follows. Of the four darkest places two are coin tosses and two are 88 and
  100 in 100. "So the part of the saying that holds is about lamps" does not follow; "is strongest where
  there are lamps" does (towns +0.43 mag, Àger +0.15, Teide +0.16, Nerpio and Arkaroola about nothing).
- La Palma's column is 0.50 bright all year: 20.44, not 19.9. Its class does not change; its place in the
  table does.

**S3. "At the darkest places the sky hardly changes through the night" is not so.** (`page_check.out` part 6)
In the middle night the darkest tenth is darker than the brightest tenth by 0.28 mag at Nerpio and 0.51 at
Arkaroola (29 and 60 in 100 of light), 0.25 at Àger, 0.37 at Otlica. The five towns: 0.49. What is small at
Nerpio and Arkaroola is the steady trend (+0.008 and +0.015 mag an hour). The next sentence, on the Milky
Way, needs the sky to change.

## Moderate

**M1. The cleaned set moves every pooled figure a little toward the page's story; say the sealed figure
beside it.** (`page_check.out` parts 1 and 3, `page_check2.out` part A)

| figure | page | your 290, my code | sealed 335 | my clear 346 | my cleaned 274 |
|---|---|---|---|---|---|
| last tenth the darkest | 17 | 17.2 (50 nights) | 18.5 (62) | 18.8 (65) | 17.9 (49) |
| eighth tenth | 21 | 21.4 (62) | 20.6 (69) | 19.9 (69) | 20.4 (56) |
| last three tenths | 55 | 55.2 | 54.6 | 54.3 | 54.4 |
| first half | 18 | 17.9 | 19.1 | 19.7 | 19.7 |
| second half | four in five | 82.1 | 80.9 | 80.3 | 80.3 |
| five towns, darker before dawn | 93 | 93 (68 nights) | 92 (80) | 91 (85) | 94 (63) |
| towns, evening brighter by | 49 | 49 | 51 | 50 | 49 |
| the nine others bar two | about nine in ten | 88 | 87 | 87 | 89 |
| Arkaroola, Nerpio | 44, 55 | 42, 55 | 53, 55 | 53 together | 49 together |
| towns by the clock, middle tie | 04:00, 04:23, 04:12 | 04:01, 04:23, 04:12 | 03:54, 04:20, 04:12 | | 04:02, 04:20, 04:11 |

- The 45 nights left out had the last tenth darkest on 12 (27 in 100): 2 of the 18 that are not the sky, 10
  of the 27 dropped by the infrared test. Nine of those 27 miss the limits by no more than 0.3 °C of
  roughness or 1 °C of warmth, and 7 of the nine have the last tenth darkest. With them kept: 57 of 299 = 19.1.
- So the headline is 17 to 19 depending on which nights count as clear. "About one night in six" is the low
  end; on the sealed set it is nearer one in five. Nothing else in the table turns on the choice.
- The eighth tenth beats the last by 10 or 12 nights of 290, by 7 of 335. I would not lean on that sentence.

**M2. "The eight places in between" should be nine.** Five towns, eight and two make fifteen. The 88 in 100
is right for the seven of the middle class (140 nights) and for all nine others (165 nights).

**M3. "Three quarters of the way through" and "about one [hour] in summer" do not agree, and the summer is
different.** (`page_check.out` part 5, `page_check2.out` part B, `page_check3.out` parts B and C)
- Three quarters through a summer night of 6.3 hours is 1.6 hours before dawn. The "about one" comes from the
  middle tie, by which the share is 0.76, 0.77 and 0.86 in the three seasons (your part D). By the first tie
  it is 0.73, 0.74, 0.77; by the last 0.78, 0.81, 0.91.
- By the page's own measure the middle night's darkest tenth is the eighth in winter and in spring and
  autumn, and the ninth in summer. In summer the last tenth is the darkest on 11 of 35 town nights and within
  0.02 mag of the darkest on 63 in 100; in winter on 2 of 14 and 14 in 100, with the last tenth 0.16 mag
  brighter than the darkest. In the towns in summer the sky stays at its darkest until dawn begins. That is
  where the saying comes nearest, and the page does not say it.
- The clock and the share still cannot be told apart (scatter 1.09 and 1.13 hours; I get your figures). But
  the body now states the share as the fact and the clock as its consequence, which is no better founded
  than the reverse was.

**M4. A straight line through the towns' night misdescribes it.** (`page_check.out` part 4, `page_check2.out`
part B) "Darkened by 4 to 10": in light the five slopes are 3.8, 4.6, 5.5, 6.5 and 8.9 in 100 an hour, so 4 to
9. More to the point, over the first half of the night the towns darken by 0.130 mag an hour and over the
second by 0.002. In the middle night tenths six to nine are within 0.03 mag of the darkest. The towns' sky
stops darkening about halfway and stays there; "three quarters" is the middle of that flat stretch. Kyba's
and Posch's rates are for the evening and the hours to 2 a.m.

**M5. "The evening was half as bright again" is the pooled figure.** By town: Coslada 26 in 100, the ring road
28, Pamplona 39, Almería 50, Valencia 88.

**M6. The fold is not quite fair about L3, L6 and L8.** (first report, M5 and M6)
- "L3, L6 and L8 held under all of mine by margins the reader showed to be thin." I showed more than thin
  margins. By my reconstruction of the sheet's first version, L3 fails without the amendment (Coslada 0.67).
  With the Moon kept 6 or 12 degrees below the horizon, L6 fails (1 of the 2 lit stations left). With "lit"
  drawn at 20.0, or the Moon at 12 degrees, L8 fails.
- The fold says the amendment came before anything ran, which the file times bear out. It should also say
  that the amendment is what makes L3 hold, by the reader's reconstruction.
- The rest of the table's last column is what I found.

**M7. "The saying leans the right way" is a pooled statement.** The darkest tenth falls in the second half on
54 in 100 nights at Arkaroola and 58 at Nerpio (your table). The box and the body give only four in five.

**M8. A correction to my own first report, which bears on S1.** My infrared test and yours are not the same:
mine fails 66 of the sealed nights, yours 41 by my code (you print 42). And my "warm sky" limit, half the
station's best, is set by dry winter nights and is unfair to late summer: Otlica's three September nights
fail it with the calmest sky of the year. I said the limits were chosen after looking; I should have said
that neither test is fit to decide a single station's row.

## Minor

- "Its numbers matched mine night for night": 333 of your 335 nights are in mine, I have 13 more, and f
  differs by more than 0.02 on 6 (all ties). "On 333 of 335 nights" is exact.
- "Reading the same at midday as at night" was 6 March, the day I quoted. On the other days I have now
  sampled the midday reading is 8.7 to 16.4, where a photometer outdoors prints the daytime 0.0; the case
  stood at 18 to 26 °C day and night (`stars62_midday.out`). "Indoors" is my inference, a strong one.
- "In the last quarter of an hour before dawn" (part F): the figure is the smoothed reading a quarter of an
  hour before dawn, which is the last half hour.
- "When the Milky Way is furthest from overhead": four fifths is far, not furthest.
- "Madrid's ring road has five, the observatory at Otlica eight and Tucson nine": Pamplona has seven.
- "The rest are at villages and observatories": Northampton and Santa Cruz de La Palma are towns.
- Bará and others write "vehicle and residential lights"; the page has "the house lights".
- The second picture shows no night counts; four rows have five to nine nights. On the sealed set Arkaroola
  is 53, the other side of the coin-toss line.

**Count: 3 serious, 8 moderate, 8 minor.**

## The pictures (question 4)

- `dawn-tenths.png`: bars at 2.8, 2.8, 1.4, 3.1, 7.9, 13.8, 13.4, 20.7, 16.9, 17.2, as `dawn_recheck.out`
  prints; mine are 2.8, 2.8, 1.4, 3.1, 7.9, 13.4, 13.4, 21.4, 16.6, 17.2 (one or two nights apart in three
  bars). The axis starts at nothing. Alt text and caption agree with the bars.
- `dawn-places.png`: sixteen dots at the values of part E; I get the same but Arkaroola (42 against 44, one
  night). The axis runs from 35 with the line at 50 marked, which is fair for dots. The order and the alt
  text carry S2.

## What was already in print (question 5)

Checked against the saved pages in `lit/src/`, all word for word: Kyba ("Most of the brightly lit sites
darkened as the night progressed, typically by ~5% per hour."); Posch ("values between 0.0 and 0.14", for 10
PM to 2 AM, with larger gradients at urban stations); Bará ("diminish steadily from the end of the
astronomical evening twilight until about 04:00 h", subject as in the minor note); Patat ("there is no clear
average trend"); Alarcon ("no evidence has been found for systematic darkening during the first hours of the
night", TESS photometers of STARS4ALL); Fuller's sentence in full, page 229, chapter 11, the Wellcome
Library's copy; the forum post.

## Verified without change

The box's other figures; 55 and 18; 93 and 49; nine in ten; the coin toss at Nerpio and Arkaroola; the clock
times and "two and a half hours" in winter; the Milky Way's four fifths (I get 75 to 89 by the middle tie, 76
to 85 at the middle of the darkest tenth); the made-up nights (the tenth measure finds the last tenth 8 to 11
times in 100 on flat rounded nights); every row of the station table; the odds summing to 5.2 and the score
0.13; 2024 as the latest year complete at fifteen stations (2025 is complete at twelve); the account of my
three findings and of the sealing.

## Not verified

Which of Àger's two constants is the true one. Any version of the page later than 06:26:59 (the assembled
`site/dawn.html` of that time is the source plus the table; I compared them). Anything that needs the network.

My first report may go out as it is. If it does, this one should go with it, for M8 and the midday note.
