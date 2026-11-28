# Scout report: the twilight of 2019 as two SQM ageing papers print it, and published reports of the 2019–2020 twilight

Read and measured 28 November 2026. Papers read from the copies in `src7/` (arXiv:2012.04042 version 1 and arXiv:2210.09177); figure images cut out of those PDFs into `src10/`; my scripts and their output files are in `scout10_tools/`. Every number in Task 1 has a line in `scout10_tools/out_summary.txt`, `out_full.txt`, `out_inkprofile.txt`, `out_highsupport.txt` or `out_dates.txt`.

## Short answers

1. Four meters have a plotted twilight series that covers both halves of 2019: Vienna, Potsdam and Stockholm (paper A, Figures 3 to 5, ending in the last week of December 2019), and Potsdam again with Bodinggraben (paper B, Figure 1, ending about December 2020 and November 2021). The other 24 meters of paper B have no twilight series in the paper.
2. In all four, the points of August to December 2019 lie lower about the paper's own line than the points of January to June 2019. Lower means the meter read darker than the twilight model. Measured off the figures: darker in the second half by 0.16 (Stockholm), 0.19 (Potsdam, paper A), 0.24 (Vienna), 0.25 (Potsdam, paper B, after its atmosphere model) and 0.35 (Bodinggraben, after its atmosphere model) magnitudes per square arcsecond. Reading errors are 0.02 to 0.05; the scatter of the points adds 0.03 to 0.10 (one standard error).
3. The same difference in every other plotted year of paper A lies between 0.09 brighter and 0.10 darker (18 station-years, mean of the points found; 0.12 brighter to 0.14 darker by the other ways of taking the mean). 2018: Vienna darker by 0.05, Potsdam 0.00, Stockholm brighter by 0.06.
4. Paper A stops at December 2019, so it cannot say whether the drop lasted. Paper B can, for two meters: Potsdam and Bodinggraben are back on the line by March to June 2020. In paper B's Potsdam panel the dip runs from July 2019 to about February 2020 and is the only one of its depth in 2018 to 2020.
5. Weak points, stated here so they are not lost: Vienna has only 13 detected points after 1 August 2019 and was already below its earlier years from March 2019; November and December are low in every year at every station, so the fair comparison is month against the same month; Bodinggraben's second half of 2019 rests on 6 points; paper B's Potsdam panel is too dense to count points (about one in five could be found).
6. Neither paper mentions 2019 or 2020 as a year in which anything happened, nor volcanoes, smoke or the stratosphere. The words "volcan", "stratospher" and "smoke" occur zero times in each.
7. Task 3: nothing found says the sky overhead in twilight grew darker in 2019 or 2020, and no meter, camera or flat-field record of that twilight was found. New beyond what you have: a 2023 poster from the Tbilisi group with twilight brightness curves of autumn 2019 ("both an increase and a decrease in brightness"), a zenith colour-index paper from Kiruna, a lidar paper from Wales with optical depths, and German observers' reports that blame the purple lights of summer 2019 on forest-fire smoke.

## Task 1. What the figures show

### Which figures count

| paper | figure | what it is | counts? |
|---|---|---|---|
| A | Fig. 1, 2 | single evenings, reading against time of night | no (not against date) |
| A | Fig. 3 | Vienna (IFA), twilight model minus meter, against date | yes |
| A | Fig. 4 | Potsdam-Babelsberg (BA1), same | yes |
| A | Fig. 5 | Stockholm (STO), same | yes |
| A | Fig. A1 to A3 | model aerosol and particulate values at the times of the readings | no (not a twilight quantity; not measured) |
| B | Fig. 1 left | Potsdam-Babelsberg (BA1), four panels of the twilight series | yes |
| B | Fig. 1 right | Bodinggraben (BOD), four panels | yes |
| B | Fig. 2 | histogram of ageing slopes of the 26 meters | no (no dates) |
| B | Fig. 3, B1 to B12 | night-time sky brightness against date, already corrected for ageing ("clear-sky night sky brightness … time chunks of 45 minute length") | no (night, not twilight) |

No figure in either paper stops between January and August 2019, so no meter is dropped for that reason. Paper B's Table 1 gives the Vienna record as "Apr. 2012 – Dec. 2021" and Stockholm as "Dec. 2014 – Dec. 2021", but their twilight series for 2020 and 2021 are not plotted anywhere.

### What is plotted, and the sign

- **Paper A, Figures 3 to 5.** Caption of Figure 3: "Time (x-axis) vs. difference of modeled 𝐵-filter radiance minus observed SQM radiance (y-axis). Each point is the 5-minute average value obtained under clear sky and within a narrow interval of sun altitudes [-6◦ ,-7◦ ]." The axis is labelled Δ(mdl−obs) in mag per square arcsecond. A meter that reads darker gives a larger magnitude, so the plotted value goes **down** (more negative). The points are coloured by the inverse variance inside the five minutes. The green band is the paper's weighted straight-line fit with its one-sigma range. Several points can come from one evening; the figure does not say whether dawn is used as well as dusk (the text's examples are all dusk).
- **Paper B, Figure 1.** Caption: "Topmost panels: Patat model minus observed clear-sky SQM twilight data on y-axis versus time on x-axis. … Each point is a 5-minute-mean (BA1) or 10-minute-mean (BOD) brightness. 2nd panels from top: Prediction from empirical atmospheric model plus linear time trend. 3rd panels from top: The residual after subtraction of the top-panel data from the model in the 2nd panel. The red line and area show a polynomial fit and its standard deviation respectively. Bottom panels: Final scatter after subtraction of the atmospheric model and the linear and polynomial trends." Top panel: same sign as paper A, down = meter darker; the grey band is the straight-line fit. Third and fourth panels: the caption's wording would make them model minus data, but the plotted points are **data minus model** (third panel = top panel minus second panel: matched point by point at Bodinggraben, 24 columns, the two agree to 0.004 mag rms; the other sign misses by 0.37). So in every panel, down = meter darker than expected.

Last dates plotted (centre of the last point found; one pixel is 0.7 to 1.3 days in paper A, 5.2 days for Potsdam and 2.8 days for Bodinggraben in paper B):

| panel | first point | last point |
|---|---|---|
| A Fig. 3 Vienna | 2 Apr 2012 | 24 Dec 2019 |
| A Fig. 4 Potsdam | 3 Jan 2011 | 29 Dec 2019 |
| A Fig. 5 Stockholm | 10 Dec 2014 | 28 Dec 2019 |
| B Fig. 1 Potsdam | first point found 9 Feb 2011; points start at the left-hand frame | last point found 4 Dec 2020; points run into the right-hand frame, which sits at about 25 Dec 2020 (Table 1: "Jan. 2011 – Feb. 2021") |
| B Fig. 1 Bodinggraben | first point found 25 Aug 2016; points start at the left-hand frame | last point found 12 Nov 2021; frame edge about 23 Nov 2021 (Table 1: "Jul. 2016 – Dec. 2021") |

### How I measured

The figures are bitmaps inside the PDFs (3818 px wide in paper A, 1000 px in paper B). Axes were fitted to the tick marks (worst tick 0.5 px in x, 0.7 px in y). Scale: 816 px per magnitude in paper A, 210 in paper B.

Each point is a filled disc of fixed radius (17.0 px in A, 8.65 px in B). A script (`discs.py`) finds discs from their visible rims and writes date and value. A disc wholly hidden under others cannot be found by any method. Found: 718 of the 971 the Vienna panel says it holds, 1124 of 1693 (Potsdam, A), 560 of 796 (Stockholm), 100 of 124 (Bodinggraben, bottom panel), but only 176 of 950 (Potsdam, paper B, bottom panel), where the discs are one colour and each is three months wide.

Checks that the reading is sound:
- The paper's own line, read off the green band, has slope −0.0527, −0.0460 and −0.0338 mag per year; the panels print −0.053, −0.046 and −0.034.
- Three ways of taking a half-year mean, coded before any result was seen: the mean of the discs found; the mean of the calendar-month means; the mean height of all inked pixels in the window (which needs no disc finding). A fourth run, added afterwards as a check, used only discs with at least half their rim showing. The spread among these is my reading error.
- Two things were changed after a first look at the output, both in paper B only: discs "found" on the bare grey and red bands were removed by requiring a green disc, and the grey line of the Potsdam top panel was re-read where it lies over discs (the first try gave a slope of the wrong sign; after the change −0.0475 against the printed −0.048).

Windows: first half = 1 January to 30 June; second half = 1 August to 31 December. All values are offsets from the paper's own line (paper A: green band; paper B top panel: grey band; paper B bottom panel: zero, since the line and polynomial are already taken out).

### The table

Units: mag per square arcsecond. Negative = meter reads darker than the line. "Difference" = second half less first half. The main figure is the mean of discs found; the bracket is the range over the other ways of taking the mean. n = discs found in the window.

| paper | figure, panel | station | latitude | Jan–Jun 2019 less line | Aug–Dec 2019 less line | difference 2019 | difference 2018 | difference 2020 | reading error | scatter (1 s.e.) |
|---|---|---|---|---|---|---|---|---|---|---|
| A | Fig. 3 | Vienna (IFA) | 48°13′54″N | −0.07 (n=47) | −0.32 (n=13) | **darker by 0.24** (0.22 to 0.26) | darker by 0.05 (0.03 to 0.06) | not plotted | ±0.03 | 0.04 |
| A | Fig. 4 | Potsdam (BA1) | 52°22′48″N | −0.04 (n=65) | −0.23 (n=47) | **darker by 0.19** (0.15 to 0.19) | 0.00 (0.00 to 0.02 darker) | not plotted | ±0.02 | 0.03 |
| A | Fig. 5 | Stockholm (STO) | 59°21′12″N | 0.00 (n=54) | −0.16 (n=48) | **darker by 0.16** (0.15 to 0.16) | brighter by 0.06 (0.04 to 0.06) | not plotted | ±0.02 | 0.03 |
| B | Fig. 1 left, top panel (model minus meter) | Potsdam (BA1) | 52°22′48″N | −0.06 (n=12) | −0.26 (n=12) | darker by 0.20 (0.17 to 0.24) | darker by 0.16 (0.08 to 0.16) | brighter by 0.11 (0.09 to 0.12) | ±0.05 at best | 0.08 |
| B | Fig. 1 left, bottom panel (after atmosphere model, line, polynomial) | Potsdam (BA1) | same | +0.01 (n=9) | −0.24 (n=10) | **darker by 0.25** (0.21 to 0.29) | darker by 0.10 (0.05 to 0.11) | brighter by 0.08 (0.07 to 0.11) | ±0.05 at best | 0.10 |
| B | Fig. 1 right, top panel | Bodinggraben (BOD) | 47°47′31″N | +0.09 (n=9) | −0.36 (n=5) | darker by 0.45 (0.34 to 0.45) | darker by 0.14 (0.11 to 0.14) | darker by 0.06 (0.05 to 0.07) | ±0.06 | 0.09 |
| B | Fig. 1 right, bottom panel | Bodinggraben (BOD) | same | +0.05 (n=8) | −0.30 (n=6) | **darker by 0.35** (0.32 to 0.37) | darker by 0.05 (0.04 to 0.06) | darker by 0.06 (0.05 to 0.06) | ±0.03 | 0.07 |

Notes to the table.
- The two Potsdam rows of paper B are the same meter and mostly the same evenings as the Potsdam row of paper A. There are four meters here, not five.
- Paper B's third panel (before the polynomial is taken out) differs from the bottom panel by the polynomial's change across 2019: 0.01 at Potsdam, 0.03 at Bodinggraben (so "darker by 0.26" and "0.38" if measured from the third panel's zero).
- Paper B, Potsdam: with one disc in five found, a single half-year mean is not to be trusted beyond about 0.05, and for some earlier years the disc mean and the inked-area mean disagree by 0.1. The inked-area profile below is the better evidence for that panel.
- Bodinggraben has no points from January to March in 2018 and 2019 (mountain winter), so its "first half" is April to June; its second half of 2019 is one point in August, three in September, two in October.

### The yardstick: other years in the same figures

Second half less first half, mean of discs, every plotted year with points in both halves:

| station (figure) | other years | their differences | mean ± s.d. | 2019 |
|---|---|---|---|---|
| Vienna (A Fig. 3) | 2012–14, 2016–18 | +0.04, −0.02, +0.01, −0.05, −0.10, −0.05 | −0.03 ± 0.05 | −0.24 (4.4 s.d. out) |
| Potsdam (A Fig. 4) | 2011–18 | −0.10, −0.02, −0.09, +0.02, −0.06, +0.09, −0.10, 0.00 | −0.03 ± 0.07 | −0.19 (2.3 s.d. out) |
| Stockholm (A Fig. 5) | 2015–18 | −0.02, −0.02, −0.09, +0.06 | −0.02 ± 0.06 | −0.16 (2.3 s.d. out) |
| Potsdam (B, bottom) | 2011–15, 2017–18, 2020 | −0.19 to +0.08 | −0.08 ± 0.11 | −0.25 (1.6 s.d. out) |
| Bodinggraben (B, bottom) | 2017, 2018, 2020, 2021 | 0.00, −0.05, −0.06, −0.18 | −0.07 ± 0.08 | −0.35 (3.5 s.d. out, on four other years) |

In paper A, 2019 is the largest difference of any year at each of the three stations. In Bodinggraben's top panel (no atmosphere model) 2021 is nearly as large as 2019 (darker by 0.25 to 0.36 against 0.34 to 0.45), on five points in each half.

Season matters. November and December lie below the line in every year at every station (Potsdam, A: −0.11 to −0.30 in 2011–2018; −0.28 in 2019). August to October do not. Mean of the monthly means for August to October, about the line:

| station | earlier years | 2019 | 2020 |
|---|---|---|---|
| Vienna (A) | −0.03, −0.01, 0.00, +0.07, −0.02, −0.01 (2012–14, 2016–18) | −0.29 (Aug, Sep only) | not plotted |
| Potsdam (A) | −0.09, −0.03, +0.01, +0.06, +0.04, +0.10, −0.04, +0.04 (2011–18) | −0.20 | not plotted |
| Stockholm (A) | +0.13, +0.13, +0.05, +0.11 (2015–18) | −0.11 | not plotted |
| Potsdam (B, bottom) | −0.19 to +0.09 (2011–18) | −0.22 | +0.12 |
| Bodinggraben (B, bottom) | +0.03, −0.03, −0.05 (2016–18) | −0.31 | 0.00 (2021: −0.12, one month) |

Each month of 2019 against the mean of the same month in 2016–2018 (paper A, discs found; negative = darker than that month usually is):

| month | Vienna | Potsdam | Stockholm |
|---|---|---|---|
| Jan | +0.15 | −0.05 | −0.03 |
| Feb | +0.11 | −0.01 | −0.09 |
| Mar | −0.19 | +0.05 | −0.11 |
| Apr | −0.02 | +0.02 | −0.06 |
| May | −0.19 | −0.05 | too few to compare |
| Jun | −0.13 | −0.10 | no points |
| Jul | −0.14 | −0.24 | no points |
| Aug | −0.33 | −0.19 | −0.24 |
| Sep | −0.28 | −0.21 | −0.19 |
| Oct | no points | −0.29 | −0.18 |
| Nov | −0.23 (1 point) | −0.13 | −0.20 |
| Dec | −0.23 | −0.02 | −0.09 |

### Steps, bumps and excursions seen

- **Second half of 2019, all four meters.** Visible to the eye in each figure once looked for; plainest at Stockholm, where the points of October to December 2019 reach −0.4 to −0.6 while every earlier autumn sits at or above the line.
  - Potsdam (A Fig. 4): the months January to May 2019 are within 0.05 of their usual value; June −0.10; July to October −0.19 to −0.29; November −0.13; December back to usual (−0.02). Single evenings scatter by ±0.15, so the start cannot be put closer than some time between early June and mid-July 2019: the six points of 2–3 June sit on the line (+0.01), there are none from 4 June to 10 July, and the 12 points of 11–31 July average 0.07 below the line where the Julys of 2016–2018 averaged 0.17 above it.
  - Stockholm (A Fig. 5): no points from early May to 12 August 2019 (the summer gap the paper explains). From the first points after the gap the series is about 0.2 below its usual value for the month, to November; December −0.09.
  - Vienna (A Fig. 3): August and September 2019 are 0.3 below their usual value, but March, May, June and July 2019 were already 0.13 to 0.19 below. So at Vienna the figure shows a slide through 2019 that steepens in late July, not a clean change at mid-year. Paper B says of this meter: "Since we recognized at some stations (e.g. IFA) remaining nonlinear trends, we additionally fit polynomials up to 3rd order to the residuals."
  - Potsdam (B Fig. 1, bottom panel), mean height of the inked area in two-month windows (each disc is 45 days in radius, so edges are blurred by that much): 2018, six windows, −0.04 to +0.05; Jan–Feb 2019 −0.07; Mar–Apr +0.02; May–Jun −0.01; **Jul–Aug −0.18; Sep–Oct −0.25; Nov–Dec −0.22**; Jan–Feb 2020 −0.09; Mar–Apr −0.07; May–Jun +0.08; Jul–Aug +0.14; Sep–Oct +0.06; Nov–Dec −0.06. A dip of about 0.2 lasting from July 2019 to about February 2020, then a return and a spell 0.1 above the line in mid-2020. The atmosphere model of paper B (15 quantities, among them four aerosol optical depths and three particulate measures) did not remove it: the dip is 0.20 in the top panel and 0.25 after the model.
  - Bodinggraben (B Fig. 1, bottom panel), same kind of profile: Jul–Aug 2019 −0.08; **Sep–Oct −0.31**; no points in November or December 2019; Jan–Feb 2020 −0.18 (one point); Mar–Apr 2020 +0.02. The same months of other years: Sep–Oct 2018 −0.09, 2020 −0.05, 2021 −0.13. The lowest point of the whole panel, −0.47, is at about 22 October 2019 (±3 days).
- **Other dates.**
  - Vienna, first half of 2015: 21 points averaging 0.13 below the line (monthly means 0.18 below), followed by a gap with no points from 1 May 2015 to 24 February 2016. Smaller than the 2019 level (0.32 below the line in August to December 2019).
  - Potsdam, first four months of 2016: 0.10 to 0.23 below the line, followed by July to October 2016 0.08 to 0.24 above it (the year whose second half stands highest above its first, by 0.09).
  - Every station, every year: November and December below the line, by 0.01 to 0.30 (mostly 0.1 to 0.3). The paper treats the yearly wave as seasonal.
  - Stockholm: a yearly wave, high in August to October, low in winter and spring, of about ±0.15; the paper notes it ("strong seasonal NSB variations, in particular for Stockholm").
  - Nothing else in 2018 or in the first half of 2019 stands out at Potsdam or Stockholm.

### What the figures cannot say

- Paper A's line is fitted to a series that ends with the low points of late 2019, and there is no 2020 in it. From paper A alone a lasting step (the instrument) and a passing dip (the sky) look the same.
- Paper B shows the recovery for two meters only. For Vienna and Stockholm nothing after December 2019 is plotted. Paper B's Table 3 gives their ageing slopes over the longer record as −68 and −43 mmag per year, against −53 and −34 in paper A; Potsdam −48 against −46.
- All of paper A's meters went through one reduction and one twilight model, so the figures alone cannot rule out a cause in the processing that is common to late 2019.
- The means are unweighted; the paper's lines are weighted by the inverse variance inside each five minutes.

## Task 2. What the papers say

Counts of words in the text copies (`arxiv_2012.04042_flow.txt`, `arxiv_2210.09177_flow.txt`):

| word | paper A | paper B |
|---|---|---|
| volcan | 0 | 0 |
| stratospher | 0 | 0 |
| smoke | 0 | 0 |
| erupt, Raikoke, wildfire, "forest fire" | 0 | 0 |
| 2019 | 21 | 15 |
| 2020 | 27 | 20 |
| aerosol | 6 | 17 |
| scatter | 6 | 21 |

Every "2019" and "2020" in either text is a running head, a citation year, a data-source credit, a span of dates ("obtained between 2011 and 2019") or the date of an example evening. Neither paper says anything about the year 2019 or 2020 as such, and neither remarks on the low points of late 2019.

Paper A, the only dated 2019 evenings:
- Caption of Figure 1 (the figures are cited in Section 4, Results): "…in Stockholm on June 30, 2019 (bottom panel)."
- Caption of Figure 2: "Scotographs of SQM measurements (gray curve) obtained during the course of dusk under clear sky in Potsdam on March 2, 2011 (top panel) and March 31, 2019 (bottom panel). The comparison qualitatively shows the darkening effect after 9 years of operation."

Paper A on scatter and on the atmosphere:
- Section 3 (Models and methods): "it is expected that the residuals of Δmdl−obs show discrepancies. However, the average magnitude of these discrepancies should be independent of time, as long as the average atmospheric composition has not changed significantly."
- Section 3: "We may thus formulate the null hypothesis that any temporal trend (slope) in the residual (twilight model minus SQM measurements) is caused by instrumental effects (i.e. the SQM aging effect), as long as the average composition of the atmosphere has not changed significantly (towards lower abundances) within the same period of time."
- Section 5 (Discussion): "Finally, it is seen in Figures 3–5 that individual measurements obtained under clear sky may differ by a large amount, even up to 1 magSQM arcsec−2 (or a factor of 2.5) on timescales of days or weeks. This scatter is mainly caused by complex atmospheric physics (e.g. short-term changes of atmospheric composition)."
- Section 5: "The Stockholm data also show another peculiarity, i.e. gaps in data during summer. The reason is the stringent filtering for clearskies … In Stockholm, for few days around summer solstice, the Sun’s rate of decline per unit time is far from being constant (within the interval of interest). In this case, the polynomials of the Patat et al. (2006) twilight models appear to systematically differ from the observations."
- Section 6 (Summary and conclusion): "we have checked large-scale atmospheric parameters (AOD, particulate matter, ozone) for existing trends that might cause the observed darkening. As shown in Figures A1–A3 no significant trend was found that could possibly lead to the observed slopes. However, we do notice a slight upward trend of particulate matter, apparent at all three sites."

Paper B on the twilight residuals:
- Section 3.2 (Correcting SQM readings for degrading sensitivity with time using the twilight method): "Assuming that the twilight sky brightness is not affected by ALAN and remains constant, one can reveal any underlying temporal sensitivity change of the measurement system. In addition to this procedure, we now also account for atmospheric changes that may impact the twilight observations."
- Section 3.2: "Since we recognized at some stations (e.g. IFA) remaining nonlinear trends, we additionally fit polynomials up to 3rd order to the residuals. If the subtraction of a polynomial further reduces the scatter (by more than 0.5 percent), we proceed and use also the polynomial as a correction function, accounting for non-linear effects."
- Section 3.2: "Note the strong seasonal variation of NSB during twilight and how accurate the atmospheric model is able to predict them for both the urban site and the rural site."
- Section 5 (Discussion): "The scatter of the aging slopes among our stations, however, does not support such a simple picture. Some other factors, probably dust and polls, may play a crucial role."

The aerosol quantities in paper B's model (Table 2) are black carbon, dust, sea salt and organic matter optical depths at 550 nm and three particulate-matter measures, all from the Copernicus atmosphere service. No stratospheric quantity is among them.

## Task 3. Published reports of the twilight sky in the second half of 2019 and in 2020

The search was run by a separate searcher under the same rules; it saved every source under `src10/` with the prefix `t3_`. I then checked each sentence quoted below by exact search in the saved text (all found), and read the one figure myself.

**Plain result.** No source found says the sky overhead in twilight grew darker in 2019 or 2020, as a measurement or in words. No sky-brightness-meter, TESS-W, all-sky-camera or twilight-flat-field record of a twilight change in that period was found. No source gives a number for a change of zenith twilight brightness. What exists is colour, polarisation, layer height and optical depth, and one poster with brightness curves in arbitrary units.

### Measurements

| source | place | months | what was measured | brighter, darker or colour only |
|---|---|---|---|---|
| Mateshvili and 12 others 2023, EGU General Assembly, EGU23-13861 (poster), DOI 10.5194/egusphere-egu23-13861. A third item from the group you know. | Tbilisi, Georgia | 30 Sep, 1 Oct, 2 Oct 2019, set against 17, 18, 21 Aug 2022 (legend labels end in "e", taken as evening) | twilight sky brightness at 780 and 870 nm, solar zenith angle 89° to 95°, CCD spectrograph | **both**, in words; no number in the text |
| Ugolnikov and Maslov, arXiv:2001.06034 (January 2020; taken to be the preprint of the paper you know) | 55.2° N, near Moscow | mornings of 10 and 12 Sep 2019 against autumn 2018 | sky intensity and polarisation, 540 nm band | **brighter**, in words only; the numbers are for polarisation |
| Lauster and others 2022, Atmos. Chem. Phys. 22, 15925, DOI 10.5194/acp-22-15925-2022 | Kiruna, Sweden, 68° N | spring 2020 | zenith-sky spectrometer, colour index at solar zenith angle above 90° | **colour only** |
| Vaughan, Wareing, Ricketts 2021, Atmos. Chem. Phys. 21, 5597, DOI 10.5194/acp-21-5597-2021 | Capel Dewi, Wales, 52.4° N | June 2019 to May 2020 | lidar at 355 nm: aerosol optical depth of the stratospheric layer | not a twilight measurement; mentions sunsets once |
| F. M. Mims, personal website (forrestmims.org); a lead, not a paper | central Texas | July 2019 to February 2020 | zenith twilight photometer in the near infrared | layer heights only |

The sentences.

- Mateshvili 2023 (`t3_mateshvili_egu23-13861_presentation.txt`): "The presence of a strong aerosol layer significantly disturbs the brightness of the twilight sky (Fig,2, left), causing both an increase and a decrease in brightness depending on the range of heights and thickness of the layer, the presence of a second layer above the first, and the level of transparency in the interval between the two layers." And: "one set of curves measured during autumn 2019 when the stratospheric aerosol layer was disturbed after the Raikoke eruption, and another set of curves measured during summer 2022 when the stratospheric layer was not significantly disturbed in the Northern hemisphere."
  - My reading of its Figure 2, left panel, by pixel (±0.02 in the logarithm; `t3_mateshvili_egu23-13861_fig2_left_panel_zoom.png`, script `t3_curves.py`). The axis is "log10(Intensity), intensity in arbitrary units"; the poster does not say that the six curves share one scale, which wavelength the panel shows, or where the instrument pointed; the months differ. With those cautions: at solar zenith angle 88.5° the three 2019 curves read 4.42 to 4.51 and the three 2022 curves 4.57 to 4.63 (2019 lower). The curves cross near 90°. At 93° the 2019 curves read 3.58 to 3.68 and the 2022 curves 3.45 to 3.56 (2019 higher). At 96° (Sun 6° down, where the SQM papers measure) the 2019 curves read 2.10 (30 September), 1.98 and 2.01, and the two 2022 curves that can be read there 1.96 and 1.99 (the third is behind the legend; at 96.2° it is the lowest of the six): in this near-infrared record 2019 is the same or brighter there, not darker.
- Ugolnikov and Maslov (`t3_ugolnikov2020_arxiv2001.06034_postvolcanic.txt`), abstract: "An increase in sky brightness paired with a decrease in polarization was registered, especially noticeable in the dusk segment." The zenith figure it gives is for polarisation: "The total aerosol effect decreases the zenith polarization near the sunrise to about 0.5." The searcher found no figure for a change of zenith brightness anywhere in the text. The arXiv listing shows no later paper by these authors on 2019–2020 twilight brightness (titles only were checked).
- Lauster 2022 (`t3_lauster2022_acp_zenith_doas_colour_index.txt`): "Raikoke eruption on 22 June 2019 (48.3◦ N, 153.4◦ E; purple arrow). For all cases, the OMPS-LP data show high extinction values in the 30 to 60◦ latitude band and a high PSC-like signature is found during springtime the following year." On smoke it says the opposite, of an earlier year: "wildfires (e.g. July–August 2015, number 5 in Fig. 13) exhibit no signatures in the DOAS measurements due to the different particle size distribution compared to volcanic aerosol or PSC particles." (Line-break hyphens of the saved text removed in both.)
- Vaughan 2021 (`t3_vaughan2021_acp_raikoke_lidar_uk.txt`). Sunsets, in passing: the aerosol "created vivid sunsets around the Northern Hemisphere (Fox, 2019)". Optical depth over Wales: "a maximum value (at 355 nm) around 0.05 in mid-August and remaining above 0.02 until early November. Thereafter, optical depths decayed to around 0.01 by the end of 2019 and remained around that level until May 2020." From satellite, quoted there from Kloss and others: "reached 0.045 north of 55◦ N and 0.030 between 40 and 55◦ N in the early months after the eruption".
- Mims (`t3_mims_forrestmims_org_.txt`): "From Jul 2019 to Feb 2020 (and ongoing), I've been measuring the elevation of the volcanic arerosol cloud from the eruption of the Russian volcano Raikoke on 22 Jun 2019." (the site's spelling). No brightness change is given.

### Reports in words

- **Arbeitskreis Meteore, journal METEOROS (Germany).** These put the purple lights of summer 2019 down to forest-fire smoke, not to Raikoke. None speaks of the zenith or of a darker sky.
  - Nr. 8/2019, cover note: "In diesem Sommer gab es mehrfach intensive Purpurlichter durch die Aerosole verschiedener Waldbrände auf der Nordhalbkugel, hauptsächlich von denen in Kanada und Sibirien."
  - Nr. 3/2020, P. Krämer, review of 2019: "Dritthäufigste Erscheinung war im letzten Jahr das Purpurlicht, das insgesamt 64 mal gemeldet wurde." and "Juni bis August: Immer wieder intensives Purpurlicht und ungewöhnliche Dämmerungsfarben".
  - Nr. 2/2020, C. Hinz: "Solche intensiven Purpurlichter gab es zuletzt im August 2019". For the purple lights of late November and early December 2019 the same article rules out fire and volcano ("keine größeren Waldbrände in der Nordhemisphäre und auch keine hochreichenden Ascheausstöße von Vulkanen") and names polar stratospheric clouds.
- **Deutscher Wetterdienst, "Thema des Tages", 28 August 2019** (A. Leyser): "Trotz teilweise wolkenloser Verhältnisse wurde der Himmel lange vor Sonnenauf- bzw. nach Sonnenuntergang in ein purpurfarbenes Licht getaucht." Cause given: aerosol "die vornehmlich auf diese Brände zurückzuführen waren" (the fires in Canada and Siberia). Colour only.
- **Astronomy magazine, S. J. O'Meara, "Fire in the sky", November 2020:** "A year ago, Northern Hemisphere twilights became infused with incendiary glows capped with simmering purple sheens." It names Ambae, Raikoke and Ulawun. On 2020: "many observers have already reported that the visual effects have greatly waned".
- **Atmospheric Optics website (L. Cowley), "Volcanic Twilight":** a photograph sequence from California, 22 August 2019. The one remark on the sky overhead: "At this time the overhead sky remains a deep blue." It describes that evening, not a change from other years. Its "Volcanic Twilight Diary" page, of an observer in the Netherlands: "He has seen more unusual "volcanic" twilights this year than ever before."
- **Universe Today, D. Dickinson, 30 September 2019:** "violet twilight currently seen worldwide". Colour only.

### Leads seen only as search snippets (not verified)

- Sky & Telescope, B. King, "Volcanoes Turn Twilights Purple" (2019): the page refused. Snippets speak of purple light peaking about 15 minutes after sunset in late August 2019.
- Astronomy & Geophysics, "News", August 2019 (DOI 10.1093/astrogeo/atz154): an index hit for Raikoke with "sunsets"; the page refused.
- Weather (Royal Meteorological Society), "Sunsets and sunrises", September 2019 and August 2020 (DOI 10.1002/wea.3601, 10.1002/wea.3816): titles only.
- A 2023 workshop abstract by Mims: "46 profiles of aerosol layers from the 2019 eruption of Raikoke" (listing only).

### Checked and empty

The saved full texts of the main aerosol papers on 2019 were searched for twilight, sunset, purple and sky colour: Kloss 2021, Ohneiser 2021 (Arctic smoke), Ansmann 2021 (Siberian smoke), Vernier 2024, Wrana 2023, Fromm 2025, de Leeuw 2021, Osborne 2022, Gorkavyi 2021, Chouza 2020. Apart from satellite "sunset" occultations and one citation of the Mateshvili abstract, nothing. Vaughan 2021 is the only one that mentions sunsets.

## Could not open, did not find

Could not open:
- skyandtelescope.org and academic.oup.com (bot checks); the BAMS article page (no text returned); the NASA GLOBE Observer note on purple sunsets (empty page); a Finnish sky-watch observation page (no response); METEOROS Nr. 5 and 6 of 2020 (not at the usual address). NASA ADS was not searched (its pages need a browser or a token); Crossref, OpenAlex, arXiv and Semantic Scholar were used instead.
- The published MNRAS versions of the two papers were not opened; everything here is from the arXiv versions (paper A: version 1, 7 December 2020). A figure may differ in the journal.

Did not find:
- Any statement, by anyone, that the zenith sky in twilight was darker in 2019 or 2020. Neither paper remarks on the low points of late 2019 in its own figures.
- Any number for a change of zenith twilight brightness in 2019–2020.
- Any SQM, TESS-W, all-sky-camera or flat-field record of twilight in 2019–2020 other than the two papers measured here.
- A twilight series after December 2019 for Vienna or Stockholm, or any twilight series for the other 24 meters of paper B.
- A journal paper from the Mateshvili group (three conference items only). A report in Weather, the British Astronomical Association's journal, BAMS, Meteorologische Zeitschrift, or in Finnish, Russian or Japanese sources beyond those listed.

Not done:
- The points were not weighted as the papers weight them, and hidden points could not be counted (found: 66 to 74 per cent in paper A, 81 per cent at Bodinggraben, 19 per cent in paper B's Potsdam panel).
- Figures A1 to A3 of paper A (model aerosol values at the reading times) were looked at for Potsdam only and not measured; by eye the total optical depth of 2019 looks like other years.
- Nothing here tests a cause. The figures show when and by how much the meters read darker than the model; they do not show why.

Files: figure images `src10/A_p4-00[024].png`, `src10/B_p5-00[02].png`; Task 3 sources `src10/t3_*`; scripts `scout10_tools/discs.py`, `halfyears.py`, `summary.py`, `inkprofile.py`, `signcheck.py`, `listdiscs.py`, `geom.py`, `geomB.py`, `probe.py`; point lists `scout10_tools/*.csv`; pictures of the points found `scout10_tools/ov_*.png`.
