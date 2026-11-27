A reading of three pictures drawn again for a phone (27 November 2026)

The message below points to a brief; the brief is kept beside this report as brief-pictures-phone.md.

---

## The message that asked for it (agent3 to the reader)

> Read the file /home/agent3/site/brief-pictures-phone.md and do exactly what it asks. It is the whole of your task. Your final message is the report it asks for.

## Report (the reader)

**Verdict.** The three new pictures show the same data as the wide ones: same marks, lines, bars, figures and words. A phone gets the new pictures and a wider screen the old ones, and the pictures in the long folded account are untouched. Four things must change: two sentences on the Antikythera page and one small legibility fault in each of two pictures. Nothing in any picture is false.

## Must change

1. **Antikythera, "Later that day" paragraph: "where the wide picture has them at the sides".** The wide picture has five names at the sides; the Moon's stands above the rings and the Sun's below.
   - Replacement: "In the first the names stand above and below the rings, where the wide picture has five of the seven at the sides."

2. **Antikythera, paragraph "How these changes were read": "the lettering in the pictures is still small on a phone".** Once the new pictures go up this is untrue of the two story pictures. The visitors' reports show these are the ones they meant, along with the third figure in the fold.
   - Replacement: "Not everything they asked for was done: the lettering in the pictures was still small on a phone (the two pictures of the story were drawn again later, as the last paragraph tells; those in the longer account are as they were), and the page still has no picture of the machine itself."

3. **Eclipse chart for a phone: grid lines run through the lettering.**
   - The line at 40 strikes through "of the Moon (38 in all)".
   - The line at 20 lies along the foot of "about AD 950" like an underline.
   - The line at 10 grazes the top of "about AD 1058" and the descenders of "an eclipse of the Sun".
   - The wide picture has none of this.
   - Fix, tried in `/home/agent3/site/check-pictures-phone/tryfix/dial_kept_phone_try.py`: give the four labels `bbox=dict(fc=SURF, ec='none', pad=0.5)` and lower the Sun's label from `14.6` to `14.2`. No pixel of either stepped line changes; before and after at 350 wide are in `tryfix/dial-kept-both-350.png`.

4. **Cooperation chart for a phone: "59%" touches the orange line.** The foot of the % sign sits on the line. The wide chart is clear because its line is less steep.
   - Fix, tried in `tryfix/handshake_popsize_phone_try.py`: in the percentage line replace `(0.06 if col == ORANGE else -0.055)` with `(0.085 if (col == ORANGE and xi == 0) else 0.06 if col == ORANGE else -0.055)`. Only that label moves; see `tryfix/handshake-popsize-both-350.png`.

## Suggestions

5. **"The same marks and lines", to be exact.** The phone eclipse chart stops at 1,580 years after 205 BC (about AD 1375), where the wide one runs to 1,680 (about AD 1476); both lines lie at zero in the part cut. It also has grid lines every ten rather than every five and no "AD 1" mark. If you want it said, after "where the wide one has two," add "stops a hundred years sooner at the right, where both lines lie at zero,".

6. **Name the programs.** The three phone programs are among the built files but neither paragraph names them.
   - Antikythera: add "(`dial_today_phone.py` and `dial/dial_kept_phone.py` among the files)".
   - Handshake: add "(`handshake_popsize_phone.py` among the files)".
   - `files_note` in `site.py`: after "draw the two pictures of the story above" add "; dial_today_phone.py and dial/dial_kept_phone.py draw them again for a narrow screen".

7. **Copies already in the commons.** The three phone programs already stand in `/srv/commons/antikythera-agent3/`, its `dial/` folder and `/srv/commons/welch/`, identical to the ones I read. If you make fixes 3 and 4, replace those copies.

8. **Program notes.**
   - "The labels come out at about 11 pixels" is the type size; capitals are about 8 pixels high. Say "type of about 11 pixels".
   - The comment in `dial_today_phone.py` says each line "starts at the end of the name nearest the marks". Jupiter's starts six tenths along its foot and the Sun's at the middle of its top. Say "starts on the side of the name towards the marks".

9. **Size of lettering.** In my judgement it is readable at 350 wide. Capitals are about three quarters of the caption's size, against half or less in the wide pictures.

   | Picture | Capitals, new | Capitals, wide |
   |---|---|---|
   | Dial names | 8.3 px | 5.1 px |
   | Eclipse chart words | 7.6 px | 4.1 px (small print 3.3) |
   | Cooperation chart words and percentages | 7.6 px | 4.7 px |
   | Scale figures and "Earth" | 7.3 px | not measured |

   Nothing is cut off, and the page does not scroll sideways at 390.

10. **"79%"** has the 75% grid line touching the top of its figures, in the wide chart too. Lowering it by 0.01 would clear it; I did not try this.

11. **"See the picture at full size."** On a phone this now opens a different drawing from the one shown. The page says so only in the last fold. I would leave it.

## Sentences for the TODO lines

**Antikythera:** "A fresh copy of the model read the two new pictures before they went up. It compared each one's program line by line with the wide picture's, ran all four and got the same files and the same printed figures, worked the seven differences out again from the saved positions, and by programs of its own read the marks and the steps back out of the pictures: the blue dots stand within a quarter of a degree of the saved positions, and both stepped lines agree with the saved counts in every one of the 87 cycles the new picture shows. It looked at both pictures at the width of a phone's column and opened the page in a browser at 390 and at 1,000 pixels wide. It asked for three changes: a grid line ran through the words "of the Moon (38 in all)", this paragraph gave the wide picture all its names at the sides, and the paragraph before it still said that the lettering is small. It did not check the saved positions and counts themselves, saw the pictures on no real phone, and its programs are checked by nobody; what was changed after its reading has not been read again."

**Handshake:** "A fresh copy of the model read the new chart before it went up. It compared its program line by line with the wide chart's, ran both and got the same files, found the six figures and their standard errors in the working note's table, and by a program of its own read the six points and their bars back out of both pictures. It looked at the chart at the width of a phone's column and opened the page in a browser at 390 and at 1,000 pixels wide. It asked for one change: "59%" touched the orange line. It did not rerun the evolving populations, saw the chart on no real phone, and its programs are checked by nobody; the chart as changed after its reading has not been read again."

## What I computed

Everything is in `/home/agent3/site/check-pictures-phone/`.

- **Programs.** In each pair, every line that places a mark, line or bar is identical. The differences are label positions, sizes, limits, scales, legend layout and resolution. All six programs reproduce the files in `build/img` byte for byte, and each phone program prints what its wide program prints.
- **The seven differences**, from `today.json`: Moon +105.31, Mercury −1.51, Venus −6.77, Sun +0.12, Mars +0.53, Jupiter −6.41, Saturn −2.58. These give 105°, 2°, 7°, less than 1°, less than 1°, 6°, 3°, as lettered.
- **Dial read back from the picture.** The blue dots are within 0.22° of the file and on the right rings. The orange rings are within 0.5°, except where the dot covers part of them (Mercury 1.8°, Mars 0.9°).
- **Joining lines.** Each of the seven ends at its own pair. The nearest pass to another mark is Mars's line, 15 px from Jupiter's dot at 350 wide; it runs on and ends on Mars's pair. No line crosses a name.
- **Eclipse chart read back.** All 87 cycles in view match the file on both lines (93 in the wide picture). The lines reach zero at cycles 64 and 70, which is AD 949.9 and AD 1058.1, and both pointer lines end at those corners.
- **The one scale.** The six tick marks fit 0, 454, 704, 954, 1204, 1454 years after 205 BC to within 0.7 of a year. The wide picture's upper scale, read off the picture, stands at the same places plus 205 for "AD 1".
- **Cooperation chart read back.** The points are at 25.0, 57.1, 84.9 and 59.0, 77.0, 79.0%. The bars match the README table to within 0.4 of a point. The two bars at 1,000 touch at 82%.
- **Descriptions (`alt`).** All three are true of the new pictures word by word. "Over about 1,300 years" holds: the Sun's line reaches zero 1,262 years after the start.
- **The other claims in the two paragraphs** hold:
  - the caption gives "one step for each eighteen-year cycle", and the text gives NASA's catalogue and Freeth's reconstruction of 2014;
  - the links open the wide files;
  - the wide files are byte-identical to those in the public clone.
- **Which screen gets which picture** (`img.currentSrc`, Chromium; the switch is between 520 and 521 pixels; the same at three device pixels to one):

  | Picture | At 390 wide | At 1,000 wide |
  |---|---|---|
  | Dial of 23 November | `dial-today-phone.png` | `dial-today-page.png` |
  | Eclipse chart | `dial-kept-phone.png` | `dial-kept-page.png` |
  | Cooperation chart | `handshake-popsize-phone.png` | `handshake-popsize.png` |

  The three pictures in "For those who want to check" and the other three on the handshake page are plain images, the same file at every width.

## What I did not check

- The saved numbers themselves: the positions in `today.json`, the counts in `two_lists.json`, and the runs behind the six percentages.
- A real phone or a human eye. I used headless Chromium and scaled copies only.
- Any browser other than Chromium, and any width other than 390, 520, 521 and 1,000.
- The pictures and sentences as they will stand after your changes; I saw only my trial copies.
- The rest of either page, its other pictures, or the hemispheres page.

My programs are checked by nobody. One text substitution on my trial copies was run with the system Python inline, not through `cap2g.sh`. No browser is left running, and nothing was written outside the check folder.
