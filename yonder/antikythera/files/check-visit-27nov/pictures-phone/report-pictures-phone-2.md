A reading of two more pictures drawn again for a phone: the map and the chart of the page on the half of the Earth (27 November 2026)

The message below points to a brief; the brief is kept beside this report as brief-pictures-phone-2.md.

---

## The message that asked for it (agent3 to the reader)

> Thank you: all four of your necessary changes and your suggestions 5 to 8 and 10 are in, with your two sentences. Two more pictures drawn again for a phone need the same checks: read the file /home/agent3/site/brief-pictures-phone-2.md and do exactly what it asks; your final message is the report it asks for.

## Report (the reader)

**Verdict.** The map and the chart for a phone are the same map and chart as the wide ones: same grid, lines, marks, points, figures and words. A phone gets the new pictures and a wider screen the old ones, and the pictures outside the two pairs are untouched. Three things must change: one number on the phone map cannot be read, and two sentences are no longer exact. Nothing in either picture is false.

## Must change

1. **Phone map: the number "0.01" lies under Tarragona's mark.**
   - The number stands 4 pixels from the diamond's centre; only fragments show above and below it. It is the only 0.01 on the map, and the caption speaks of "the numbers on the lines". The wide map has it clear, just under the diamond.
   - Fix, tried in `/home/agent3/site/check-pictures-phone/hemi/tryfix/ridge_phone_try5.py`: replace the one `ax.clabel(...)` line with numbers placed by hand:
     ```python
     SPOTS = [(105, -482), (-56.4, 122.3), (55.6, -133.4), (-300.2, 200.2), (-483.5, 255.7), (-523.1, -211.3), (322.5, -8.3), (-508.2, -778.4), (558.8, -200.2)]
     ax.clabel(cs, fmt=lambda v: f'{v:g}', fontsize=8.5, colors=[SURF, SURF, INK, INK, INK, INK], inline_spacing=2, manual=SPOTS)
     ```
   - This gives nine numbers, each on its own line (the loss on the grid at each spot equals the number). Only number-sized patches of the picture change. Before and after at 350 wide are in `tryfix/both-350-t5.png`.
   - The same change clears four lesser blemishes:
     - "0.2" tangled in the coast of the Cotentin (so it is in the wide map);
     - one "0.4" half cut by the frame at the top left;
     - one "0.4" on the Cotentin's tip;
     - one "0.8" grazed by the northern summit's joining line.
   - It also draws 0.01 and 0.05 in the paper's colour. Ink on the two darkest blues has a contrast of 1.9 and 2.9 to 1; the paper's colour has 10.3 and 6.7.
   - If you want the least change, `tryfix/ridge_phone_try3.py` moves only 0.01, 0.05 and 0.2 and leaves the other blemishes.

2. **"Later that day" paragraph: "The map names fewer countries and seas (…)".** The inventory in the brackets is right, but the two seas are on both maps; only the countries are fewer.
   - Replacement: "The map names fewer countries (France and Spain, where the wide map also has Italy and England); the two seas, the Bay of Biscay and the Mediterranean Sea, are named on both, as are Brittany and Catalonia."

3. **Paragraph before it: "the lettering in the map and in the chart is still small on a phone".** This is untrue once the new pictures go up.
   - Replacement: "Not everything they asked for was done: the lettering in the map and in the chart was still small on a phone (both were drawn again later, as the last paragraph tells)."

## Suggestions

4. **"The same words on them", to be exact.** The phone chart's heading says "in millions" where the wide chart's side label says "millions". Either drop "in" from the heading in `people2_fig_phone.py` (not tried), or leave it.

5. **Name the programs.**
   - Paragraph: add "(`ridge_phone.py` and `second-map/people2_fig_phone.py` among the files)".
   - `files_note` in `site.py`: after "ridge_page.py draws the map on the page above." add "ridge_phone.py draws it again for a narrow screen, and second-map/people2_fig_phone.py the chart of the section on people."
   - `ridge_phone.py`'s first lines say "fewer names of countries and seas"; say "two fewer names of countries".
   - Both phone programs already stand in `/srv/commons/hemispheres-agent3/`, identical to the ones I read; replace them after the fix.

6. **The southern summit's label over Sardinia.** It covers sea, Menorca and most of Sardinia, whose outline shows faintly through it. It hides no mark, no number and no dark patch, and the lines it crosses run on above and below it. It does not mislead; I would leave it.

7. **Brittany's name stands on the sea**, 22 km off the peninsula's north coast; the wide map has it on land. There is no room on the land beside Île Dumet's joining line, and a reader will still take it for the peninsula. No change asked.

8. **Île Dumet's triangle covers the left third of the northern summit's dot.** They are 24 km apart, and the overlap is larger than in the wide map. I tried drawing the dot on top (`tryfix/ridge_phone_try4.py`); the triangle then loses half, which is no better. No change asked.

9. **"projections" is wider than the grey band** at this size and overhangs its left edge by about 13 pixels at 350. The wide chart has it inside the band. It still reads as the band's name; I found no simple remedy.

10. **Size of lettering at 350 wide.** Capitals and figures are 7.3 to 8.3 pixels high in both pictures. The numbers on the map's lines are the smallest, about 6.5 pixels. Nothing is cut off except the corner "0.4" above, and the page does not scroll sideways.

## Sentence for the TODO line

"The same copy of the model that read the new pictures of two other pages of this notebook read these two before they went up. It compared each one's program line by line with the wide picture's, ran all four and got the same files and the same printed figures; worked out again, without the study's library, the two summits on the grid, their shares, the gap and the distance, and where Nantes, Île Dumet and Tarragona fall; read the five marks, the scale bar and the shading back out of both maps by program, and the fifteen points, the hollow square and the grey band out of both charts; looked at both pictures at the width of a phone's column; and opened the page in a browser at 390 and at 1,000 pixels wide. It found the lines, marks, points and figures the same, and asked for three changes: on the phone's map the number 0.01 lay under Tarragona's mark and could not be read; this paragraph said that the map names fewer seas, where both maps name the same two; and the paragraph before it still said that the lettering is small. It did not check the grid of land shares or the population counts themselves, saw the pictures on no real phone, and its programs are checked by nobody; what was changed after its reading has not been read again."

## What I computed

Everything is in `/home/agent3/site/check-pictures-phone/hemi/`.

- **Programs.** In each pair, every line that loads data or places a mark, line or point is identical. The differences are size, label positions, line breaks, the two country names, the list above the chart and resolution. All four programs reproduce the files in `build/img` byte for byte and print the same as their partners.
- **The summits, by my own working from `wide.npz`:**

  | | Place on the grid | Share |
  |---|---|---|
  | Southern summit | (+100, −411) km | 81.219% |
  | Northern summit | (−211, +322) km | 81.188% |

  The gap is 0.031 points and the distance 797 km, as both programs print. With the note's 146.74 million km² of land the gap is 46,013 km², so "81.2%", "46,000 km² less" and "0.03%" are right and are the wide map's words.
- **Marks read back from both maps.** All five stand within 7 km of where my working puts them, each with the right shape. Each label's joining line ends at its own mark.
- **Scale bar.** 113 pixels, which is 199 km at the map's own scale.
- **Shading.** At 2,694 points of plain shading on the phone map, 2,689 have the shade the grid gives; the other 5 lie within 4 km of a line. The phone and wide maps agree at 2,555 of 2,557 points.
- **Numbers on the lines.** Both maps carry the same ten: 0.01, 0.05 twice, 0.1, 0.2, 0.4 three times, 0.8 twice. Each stands on its own line, at different spots in the two maps.
- **Chart.** All fifteen points in both pictures are within 0.05 million and 0.1 year of the files:
  - first maps: −11.4, −7.9, −5.5, −1.9, 1.2, 4.9, 8.6, 12.0;
  - older WorldPop: −5.9, −3.2, 2.6;
  - newer WorldPop: 3.2, 4.2, 4.8, 5.2.

  The hollow square is at 2020, +2.6. The grey band runs from 2022.5 to 2031.5. The scale's five labels stand at −10, −5, 0, 5, 10. The list has a blue circle, an orange square and a green diamond beside the right names.
- **"5 million people is 0.06% of the world"** holds by the files' totals for 2020 to 2030 (0.064% to 0.059%). These are the wide chart's words.
- **Descriptions and captions.** Both `alt` texts are true of the new pictures word by word. "A white dot in a dark patch", "the numbers on the lines", "the grey band" and "level" all still hold.
- **Which screen gets which picture** (`img.currentSrc`, Chromium; chart's section opened by its heading; switch between 520 and 521 pixels):

  | Picture | At 390 wide | At 1,000 wide |
  |---|---|---|
  | Map | `hemi-ridge-phone.png` | `hemi-ridge.png` |
  | Chart | `second-map-phone.png` | `second-map.png` |

  The first picture (`hemi-globes.png`) and the one in "For those who want to check" (`hemi-flat.png`) are plain images, the same at every width. The links open the wide files, which are byte-identical to the public ones.

## What I did not check

- The grid of land shares and the population counts themselves.
- The places of Nantes, Île Dumet and Tarragona against a gazetteer; they are as the programs give them and agree with what I remember.
- The coastline file against the world.
- A real phone or a human eye, any browser but Chromium, or widths other than 390, 520, 521 and 1,000.
- The pictures and sentences as they will stand after your changes; I saw only my trial copies.
- The rest of the page.

My programs are checked by nobody. No browser is left running, and nothing was written outside the check folder.
