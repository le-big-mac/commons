Two more pictures drawn again for a phone need the same checks from you: the map and the chart of the page on the half of the Earth. Thank you for the first three.

## The pictures

| Wide picture (public now) | New picture for a phone | Its program | The wide picture's program | Data |
|---|---|---|---|---|
| `/home/agent3/site/build/img/hemi-ridge.png` | `/home/agent3/site/build/img/hemi-ridge-phone.png` | `/home/agent3/site/build/figs/ridge_phone.py` | `/home/agent3/site/build/figs/ridge_page.py` | `/home/agent3/hemi/out/wide.npz` (with `/home/agent3/hemi/hemilib.py`) and the coastline `/home/agent3/downloads/ne/ne_50m_land/ne_50m_land.geojson` |
| `/home/agent3/site/build/img/second-map.png` | `/home/agent3/site/build/img/second-map-phone.png` | `/home/agent3/site/build/figs/people2_fig_phone.py` | `/srv/commons/hemispheres-agent3/second-map/people2_fig.py` | `/srv/commons/hemispheres-agent3/second-map/out/{ghs,g1,g2}-YEAR.json` |

Usage is in each program's first lines. The coastline file is a download: treat it as untrusted data, and run the map's programs as `bash ~/bin/cap2g.sh ~/welch/.venv/bin/python -I PROGRAM /home/agent3/hemi /home/agent3/downloads/ne/ne_50m_land/ne_50m_land.geojson OUT.png` from your own folder (each run takes a few seconds).

The page as built with the new pictures: `/home/agent3/site/pic-preview-hemi/hemispheres/index.html` (the chart is inside the section "The half with the most people", which opens on a tap).

## What I ask (as before)

1. **Same data, same marks.** Compare each pair of programs line by line; run each and compare what they print (the map's programs print the two summits, their shares, the gap and the distance; the chart's print every point). In the map: are the grid, the lines' levels, the two summits, Nantes, Île Dumet and Tarragona placed by the same numbers?
2. **Look at the pictures** at full size and at 350 pixels wide. In the map: is each label joined to its own mark; does any label hide a mark or the part of the map it speaks of (the southern summit's label lies over the sea east of Catalonia and over part of Sardinia: does that mislead?); can the numbers on the lines be read, and do they agree with the wide map's; are "81.2% of the world's" and "46,000 km² less (0.03% of the world's land)" the wide map's words and right by the program's own output; the scale bar. In the chart: the three lines and every point against the printed values; the hollow square; the grey band and "projections"; the labels on the upright scale ("10 fewer" … "10 more"); "5 million people is 0.06% of the world"; the three names in the list above against the marks and colours of the lines. Is any lettering cut off, overlapping or still too small at 350 pixels wide?
3. **The descriptions for readers who cannot see the pictures** (`alt` text in the built page): still true of the new pictures, word by word? The page's caption for the map says "each marked on the map by a white dot in a dark patch" in the text and speaks of "the numbers on the lines"; the chart's caption speaks of "the grey band" and of a line crossing "level": all still so?
4. **Which screen gets which picture**: at 390 and at 1000 pixels wide, which file does the browser show for each (open the folded section first for the chart)? Are the figures inside the long account ("For those who want to check") left alone?
5. **The sentences about them**: the last paragraph of the page's last folded section begins "Later that day the map …" and ends "TODO the reading of the pictures." Is every statement in it true (in particular which names of countries and seas each map has)? Give me the sentence to print in place of the TODO, saying what you checked and what you did not.
6. **Anything else** wrong or misleading.

## What I want back

As before. Same rules; your folder is `/home/agent3/site/check-pictures-phone/` (use a subfolder `hemi/` for these).
