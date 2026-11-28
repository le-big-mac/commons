# Did the Korean units change? Their nights as the judge

Written at 08:13 UTC on 28 November 2026, before any night reading of the second network's Korean stations was fetched. The
seventeenth sheet of the night folder.

## Why

The sixteenth sheet came out between its two outcomes. After it, the checker and I found, and it is not a test,
that five stations of the second make in Korea read the twilight about 0.2 magnitude darker from mid-July 2019,
as some fifteen photometers of the first make do in Spain, Portugal and France (`check/check-twilight-13.md`;
`sqm_north_look.out`, `raikoke_tess.out`, `raikoke_night.out`, `raikoke_night2.out`). For the first make the
units can be shown not to have changed: on moonless nights they read as before (the middle of ten places: +0.03
by the middle night and -0.02 by the darker nights, late 2019 less late 2018, my reduction). For the Korean units
the only such evidence is indirect: where the city's own light makes the reading, with the Sun 9 to 11 degrees
down, Seoul and Daejeon read as before. The fetch of the sixteenth sheet kept twilight readings only. The night
readings of those stations have not been fetched or seen by anyone here.

## The measure

Moonless night: readings with the Sun 18 degrees or more below the horizon and the Moon below it (every tenth
reading). The middle of each night with twenty such readings or more; for a month, the clear-night level, the
reading that three quarters of its nights are brighter than (five nights or more; in a city cloud brightens the
night, so the darker nights are the clear ones). A station's figure is the mean over September, October and
November of 2019 less the same month of 2018 (two months or more). Programs: `src/sqm_fetch5.py` (the archives of
2018 and 2019 again; only night readings of the Korean stations are kept, in `data/sqm4/`) and
`src/sqm_korea_night.py`.

## The line

| | line | odds |
|---|---|---|
| K1 | The clear-night level at the middle of the Korean stations (three or more) is within 0.08 magnitude of nothing | 70% |

If it holds, the Korean units did not lose a fifth of a magnitude in mid-2019, and their darker twilight was the
sky's. If the nights too are 0.15 or more darker, it was the units, or something done to them all, and the second
make is no witness. These meters read 0.02 to 0.09 darker a year as they age, and a city's lights change, so a
figure between 0.08 and 0.15 would say little either way.
