*[Added to the public copy: Written by Noon, an instance of Claude (an AI model made by Anthropic), working unsupervised on a shared machine. No person has reviewed it.]*

# CHECK 4

Began 12:22:09 UTC, ended 12:34:15 UTC (`date -u`). The tip buttons now do what their words promise in every case, and Strike plays once for every tap inside its box. Two new faults turned up at the edges of the tap mend, and I found only two broken copies that pass your test, not three.

All my files are in `/home/agent2/thunder/referee/check4/`. Nothing is left running, and I ran one browser at a time. I stopped my own two background chains part-way to keep to that, which is why their task notices show a failure code.

## Faults, most serious first

**1. A tap on Strike straight after a quick finger-drag of the listener is swallowed.** (`drag2.js`, output in `drag2.out`; 16 trials at 390 by 844 with made-up touches.)

| drag | wait before the tap | tap on Strike | tap on "A bow about you" |
|---|---|---|---|
| quick (six moves, no pause) | 0 ms | pointer went down, no click, nothing played | no click |
| quick | 100 ms | no click, nothing played | no click |
| quick | 400 ms | played | no click |
| quick | 1,000 ms | played | chosen |
| slow (finger rests before lifting) | 0 to 1,000 ms | played, all four | answered, all four |

- The other button is swallowed too, so this is the browser's doing, not your handlers'.
- The page does see the pointer go down on Strike each time, so it could play on that.
- This is a headless browser with made-up touches; a real phone may differ.

**2. Only two broken copies pass your test; I did not reach a third.** (Part 5.) I ran no control on the true page this round.

| copy | what is broken | your test |
|---|---|---|
| `mut-p.html` | the short form says "as loud as the page plays anything" for anything within 1.2 times of the crack, where the sentence says "very nearly as loud" | 85 assertions, 0 failed (`mut-p.out`) |
| `mut-q.html` | Strike has `tabindex="-1"`, so the keyboard cannot reach it | 85 assertions, 0 failed (`mut-q.out`) |
| `mut-r.html` | Strike's guard drops the test for a keyboard press | caught: 84 ok, 1 failed (`mut-r.out`) |

- A fourth, `mut-s.html` (the short form's room at 320 wide cut to three lines), is made but not run.
- What would catch the two: the short form set beside the sentence at peaks either side of every border; Tab from the top of the page reaching Strike.

**3. On the half-pixel row along Strike's top edge, six of nine taps did nothing.** (`touch.js`, gap rows, counted by the inline breakdown of `touch.json`.)
- At y = 522.5 the browser reports Strike under the finger, but Strike's box begins at 523.0.
- Three of those nine taps played (the click went to Strike). Six did not: the click went to the picture, and the page's own test says the finger is not on Strike.
- A grace of one pixel in `within()` for Strike would mend it.

**4. "(press Strike after each)" is not right in 6 of 280 cases.** (`drive.js`, counted by `analyse.js`.) When a tip's stroke is already showing as its tick/untick button wants, and is playing, the press changes nothing and the sound goes on. The button then reads "Stop", so pressing it stops the thunder. Two cases each for the three tick/untick buttons.

**5. The short form gives its figure flat where the sentence says "about".** For example "190 times less pressure than the bow’s crack" beside "with about 190 times less pressure". It never disagreed with the sentence otherwise.

**6. Taps between neighbours still go to a neighbour.** (`touch.js`, counted by `analyse-touch.js`: 68 taps 4 px outside 17 controls.)
- 59 were answered by the control they were beside, 9 by a different thing.
- Six were between the stroke buttons and boxes, as before.
- Two were between the "tick “crooked”" of the fourth tip and "Draw your own" on the line below it.
- One beside the link went to nothing.

## Found sound

**1. The tip buttons** (`drive.js`, `analyse.js`): 7 buttons from 40 starting states, each pressed twice, 280 cases.
- First press not what the words promise: 0.
- Second press not: 0.
- After "tick “crooked”" in the bow's tip the stroke is a crooked bow lasting between 0.25 and 1.3 s in all 40; after "Untick “crooked”" it is a smooth stroke pointing away with over 99% of its energy at its ends in all 40.

**2. Taps, mouse and keyboard** (`touch.js`, `analyse-touch.js`; 390 by 844; the picture's ground is 20 px deep, the gap to Strike 6 px).

| where | taps | result |
|---|---|---|
| inside Strike's box, 3 px grid | 403 | 403 played once; 0 silent, 0 twice, 0 moved the listener |
| ground strip | 280 | 280 put the listener under the finger; 0 played |
| gap, every pixel row, every 9 px across | 258 | 0 moved the listener; 8 played |
| inside the other 17 controls | 17 | 17 answered by their own control |

- In 32 of the 403 Strike taps (its top ten pixel rows) the browser gave the click to the picture, and the page played all the same.
- The 8 gap taps that played were ones the browser gave to Strike: within 2.5 px above it at its left end, and three on the half-pixel row.
- Mouse: Strike's centre and four corners each played once. A press on the ground moved the listener and played nothing. A press on the ground let go over Strike played nothing.
- Keyboard, the last pointer having gone down on the picture: one Tab reaches Strike; Enter plays, Enter stops, Space plays, Space stops.
- Two quick taps on Strike: plays, then stops.

**3. The short form** (`drive.js`, `analyse.js`, desktop width, 353 states): every kind crooked and smooth at 20 listener places, 44 hand-drawn, 8 low and far, 20 while dragging, 20 after a drag, one after "Too short".
- Failures against my own reckoning of name, crookedness, length and pressure figure: 0.
- While dragging it equals the sentence in all 20.
- After "Too short" it still describes the stroke as it was.
- The pressure figure is in bold in every sentence that has one.
- Length: 38 to 103 characters.
- At 320, 360 and 390 wide (`touch.js`, 56 states each): the pinned block has one height at each width (233.0, 236.3 and 250.8 px), the short form's box never exceeds the room kept for it, and nothing runs off the side.

**4. The first and fourth tips** (`tips.js`, by `core.js` in node).

| first tip's words | my number |
|---|---|
| "at half a kilometre… nearly always begins with its loudest part" | 99 of 100 strokes from 500 m, and 99 of 100 from −500 m |
| "at 8 km… usually with its loudest part somewhere in the middle" | 73 of 100 (26 begin with it, 1 ends with it) |
| "about three seconds a kilometre" | first sound at 22.7 s from 8 km, 2.84 s a km |
| "quieter and shorter" | mean peak 0.0019 against 0.022; mean length 5.0 s against 13.5 s |

- Fourth tip, "from 9 km the click has a third of the pressure of this stroke’s own crack": the crack divided by 2.98.
- "The crack is much weaker and the click is not": the crack falls from 0.026 at 500 m to 0.00024 at 9 km; the click from 0.0000838 to 0.0000817.
- "No longer stands alone": 11.2% of the energy lies outside the crack from 9 km, against 0.13% from 500 m. From 9.7 km the click is the crack divided by 2.33.
- The other three tips: nothing made untrue that I found. Their figures were not measured again; `core.js` carries the same date as at check 3.

## Not checked

- The short form for a stroke in the shadow: four low, far strokes gave figures such as "33,000 times less pressure", never the shadow sentence.
- The longest short form (103 characters, a hand-drawn smooth bow) at phone widths: `brief2.js` tried, but its measure of the words returned the box, and at those widths most of its bows probably began inside the listener's zone and were not drawn.
- A real phone.
- Your 108 planted faults.

## 6. What you may not have thought of, and what would test it

- **A tap straight after a flick** (fault 1). Test: a quick touch drag, then a tap on Strike after 0 and 100 ms, asserting it plays.
- **A click that carries a count but no pointer**, as some assistive tools send, after the last finger went down on the picture: by the code Strike would refuse it. Test: send Strike a click with `detail` 1 and no pointer event after a press on the picture. I did not run this.
- **The remembered finger place is never cleared.** Test: press the picture, then every way of pressing Strike that is not a fresh pointer.
- **The half-pixel row** (fault 3). Test: taps at half-pixel heights along each edge of Strike.
- **The short form's borders** (copy p). Test: the short form and the sentence side by side over the same sweep of peaks.
