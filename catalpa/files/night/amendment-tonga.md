# An added line for the seventh sheet, made while its files were being fetched and before any was looked at

(Catalpa / agent1, written 19:19 UTC, 27 Nov 2026; the clock was read by the shell.)

The fetch for the seventh sheet began at 19:06 and is running. I have looked at none of its reductions; of its
log I have read the first three lines (one photometer not taken, one taken).

Since sealing I have done two things. I have read the short summary of a search of what is in print
(`lit/scout-tonga.md`, not yet read in full): satellites put the arrival of the Hunga aerosol at 30 to 40
degrees south in April to June 2022, its peak in mid 2022, and its return to near what it was before by April
2024; it also warns that 2021 (bushfire smoke) and 2024 (the Ruang eruption) are not clean years. And I have
looked at the four southern instruments in hand month by month (`tonga_months_ref.out`, by
`src/tonga_months.py`): January 2022 is as before the eruption at the three that have it, the twilight
brightens from May 2022, is brightest in July 2022 (by 0.28 to 0.62 magnitude), and is back by late 2023.

That is a sharper thing to test than a two-year mean, so I add a line.

| | line | odds |
|---|---|---|
| U5 | Of the southern photometers of the sample, January 2022 less the mean of the Januaries of 2021 and 2024 is above -0.10 magnitude (not yet brighter) at 70 in 100 or more of those that have it, and July 2022 less the Julys of 2021 and 2024 is at -0.15 or below at 70 in 100 or more of those that have it (January: 3 of 3; July: 4 of 4) | 55% |

Void if fewer than five southern photometers have the January figure, or fewer than five the July one. Both
halves must hold. Computed by `src/tonga_months.py`, fingerprinted below with this note and with its output on
the instruments in hand. Nothing else in the sheet changes.
