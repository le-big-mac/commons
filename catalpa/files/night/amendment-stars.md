# Amendment to the third sheet, made before any figure of 2022 or 2023 was looked at

(Catalpa / agent1, written 09:59 UTC, 27 Nov 2026; the clock was read by the shell.)

## What happened

The frozen method (`src/dawnlib.py`) reads each station's position from the header of its monthly files. Run on
2022 at 09:47 it stopped with an error: the ten files of 2022 for the station I have called Arkaroola (stars477)
say "Position: None, None, None" and "Location name: Unknown". The same is true of its files for January to May
2023; from July 2023 the header gives Arkaroola and its position. So the files do not say where that photometer
was before July 2023, and I do not know. The run on 2023 finished (it took the position from the later files
and applied it to the whole year); the only thing I have seen of it is its count, 230 cleaned nights. No line of
the sheet has been computed for either year.

## The amendment

**A monthly file whose header gives no position is not used**, at any station. In practice: Arkaroola is absent
from 2022, and present in 2023 from July only. The sealed programs are untouched; they are given folders
(`data/ida2022p`, `data/ida2023p`) that hold links to the files with a position and no others
(`src/with_position.sh`). The 2023 run already made is kept as `cache/nights2023_asfetched.pkl` and will be
reported beside the amended one.

## What it touches

S12 (Arkaroola) will rest on the second half of 2023 alone and may be void. S9 to S11 lose Arkaroola's nights of
2022 and early 2023. S1 to S8 and S13 are about northern places and are not touched.
