# Scout report: meter ageing, the southern stratosphere 2021 to 2025, and twilight after Hunga

Written 28 November 2026 (searches, downloads and checks 05:40 to 06:06 UTC). Downloads are in `/home/agent1/night/lit/src7/`. Where a file saved by an earlier search on this machine was reused instead of fetched again, the path says `src2/` or `src4/`.

How to read it. Every passage in double quotation marks longer than a few words was checked by machine against the saved text named with it (white space and hyphens ignored, otherwise exact). A hyphen lost at a line end in a PDF ("preeruption") is written back in; degree and minus signs are as extracted. "Measured off the figure" means I took the figure's image out of the PDF and turned pixel positions (or colours) into values using the figure's own grid lines and colour bar. Those are my readings, not numbers the authors print: good to about ±0.5 × 10⁻³ in optical depth, worse where a curve is steep. Scripts and their full output are in `/home/agent1/night/lit/scout7_tools/` (`figure_readings_output.txt`).

## Short answers

1. The paper exists as you recalled it. Three city SQMs read darker by 0.034, 0.046 and 0.053 mag per square arcsecond per year. The cause is not separated. Later work puts the range at zero to about 0.09, and a laboratory test found the twilight method overstates the instrument's share.
2. No ageing or drift rate for the TESS-W found in print. One paper looked and saw none.
3. Yes, there was more than the Hunga remnant. Ruang (April 2024) raised the southern extratropical optical depth by a factor of about 1.8 from mid-2024, and it had not returned to the pre-eruption level by the end of 2025. No paper I opened prints the optical depths as numbers for your dates; the table below is measured off published figures.
4. Beyond Fiorentin 2025: twilight flat fields at Paranal (colour, and near-infrared decay), one twilight spectrometer study at Lauder, and visual reports. Nothing with a sky-brightness meter or an all-sky camera.

## 1. Sky Quality Meters reading darker with age

### 1a. The twilight paper

J. Puschnig, M. Näslund, A. Schwope, S. Wallner 2021, "Correcting sky-quality-meter measurements for ageing effects using twilight as calibrator", Monthly Notices of the Royal Astronomical Society 502 (1), 1095–1103, DOI 10.1093/mnras/staa4019 (volume, pages and DOI from the Crossref record, `crossref_staa4019.json`). Body text read from the preprint, arXiv:2012.04042 version 1 ("Submitted to MNRAS", 7 December 2020; `arxiv_2012.04042_flow.txt`). The published abstract in the Crossref record gives the same three slopes. The journal's own page was not tried.

Method. Zenith readings of three SQM-LE units (Potsdam-Babelsberg from 2011, Vienna from 2012, Stockholm from 2015, to 2019) are cut into five-minute clear, moonless pieces and compared with the empirical twilight model of Patat et al. (2006), built from Paranal sky flats, in the B band. A straight line is fitted to model minus reading against date. The part of twilight used (section 3):

> "In order to avoid any influence ALAN might have, we only consider twilight observations with sun altitudes between -6 and -7◦ , i.e. the bright end of the models with NSBs of approximately 13–14.5 magSQM arcsec−2 ."

Why they take it as constant. It is an assumption, stated as a null hypothesis, with one check (sections 3 and 6):

> "We may thus formulate the null hypothesis that any temporal trend (slope) in the residual (twilight model minus SQM measurements) is caused by instrumental effects (i.e. the SQM aging effect), as long as the average composition of the atmosphere has not changed significantly (towards lower abundances) within the same period of time."

> "we have checked large-scale atmospheric parameters (AOD, particulate matter, ozone) for existing trends that might cause the observed darkening. As shown in Figures A1–A3 no significant trend was found that could possibly lead to the observed slopes."

The text does not mention volcanic or stratospheric aerosol (count of "volcan" and "stratospher" in the saved text: 0).

Rate (abstract; Table 3 prints the same as −0.034 ± 0.004, −0.046 ± 0.002, −0.053 ± 0.002, the sign being model minus reading):

> "Twilight SQM observations, calibrated for changing sun altitudes, reveal a linear degradation of the measurement systems (SQM + housing window) with the following slopes: 34±4, 46±2 and 53±2 milli-magSQM arcsec−2 yr−1 for Stockholm, Potsdam-Babelsberg and Vienna."

So the range between units is 0.034 to 0.053, three units.

Cause. Not separated. The abstract lists the candidates, "degradation of the sensor sensitivity and/or loss of transmissivity of optical components (filter, housing window)", and section 4 puts it down to "instrumental aging of the device due to permanent exposure to solar irradiance." The only evidence offered is that the slope is largest at the lowest latitude.

### 1b. Other rates in print

| Source | Method | Rate, darker, mag per sq. arcsec per year | Cause named |
|---|---|---|---|
| Puschnig, Wallner, Schwope, Näslund, MNRAS 518 (3), 4449–4465, DOI 10.1093/mnras/stac3003 (Crossref: online 20 October 2022; read as arXiv:2210.09177, section 3.2) | twilight method with an added atmosphere model, 26 SQMs | zero to about 0.075; mean 0.031 ± 0.020 | "probably caused by changing transmission of the SQM housing window due to UV light exposure over several years", but section 5 adds that the scatter between stations "does not support such a simple picture" |
| Bará, Marco, Ribas, Garcia Gil, Sánchez de Miguel, Zamorano 2021, Int. J. Sustainable Lighting (2021) 1–6 (arXiv:2011.15044, sections 3 and 4) | five outdoor SQMs against unexposed units, start and end | +0.062 ± 0.004; also +0.036 ± 0.002 per MWh/m² of sunlight | if sunlight drives it, "the plastic components of the unit"; otherwise electronics, dust on the window, chemistry in the optics. The housing window was soda-lime glass |
| Fiorentin, Binotto, Cavazzani, Bertolo, Ortolani, Saviane 2022, Remote Sensing 14, 5787, DOI 10.3390/rs14225787 (abstract, Table 2) | twilight, Sun −7° to −6°, dusk and dawn; Veneto network and La Silla | 0.029 ± 0.005 to 0.086 ± 0.022. La Silla, 4 working years: 0.029 ± 0.005 from daily data, 0.017 ± 0.013 from yearly means | "Up to now it is not clear what could be the decay phenomenon"; instrument and atmosphere not separated |
| Fiorentin, Cavazzani, Bertolo, Ortolani, Binotto, Saviane 2025, Sensors 25, 516, DOI 10.3390/s25020516 (conclusions; `src2/` copy) | two aged SQMs measured in the laboratory against new ones | about 0.010 (Padova) and under 0.040 (Pennar), against 0.053 and 0.086 by twilight at the same two sites. La Silla twilight slope (their Figure 18): −0.004 | the internal infrared-blocking filter, not the housing window (see below) |
| Oregon Skyglow Measurement Network, Technical Report 7, 6 March 2023 (`src2/` copy) | new units run beside old ones | 0.019 | Unihedron, personal communication (see below) |
| Bará, Lima, Zamorano 2019, Sustainability 11, 3070 (`src2/` copy) | Galician network 2015 to 2018, raw trend | +0.09 | left open (ageing, aerosol or real change) |
| Pun, So, Leung, Wong 2014, arXiv:1401.1200 (`src2/` copy) | Hong Kong housing covers | not a rate: loss "leveled at ∼ 0.25 and 0.10 mag arcsec−2" (polycarbonate, glass) after about a year | housing window |

On the cause, the two most specific statements:

> "The windows of the watertight housing showed no significant ageing even after 9 years of exposure and use of the instrument, while the internal infrared blocking filter showed a change in its spectral transmittance at short wavelengths of about 80%."
> — Fiorentin 2025, introduction, reporting Fiorentin et al. 2022, Measurement 191, 110823 (that paper not opened)

> "Unihedron (personal communication, 2022) notes that two issues can be involved: 1) development of a translucent film on the blue glass IR filter, which seems related to moisture and 2) yellowing of the plastic case of the semiconductor sensor over time."
> — Oregon report, Processing Step 2

And the limit on the twilight method itself (Fiorentin 2025, conclusions): the twilight calibration also takes in changes of the atmosphere, "Therefore, it cannot provide unambiguous information on the degradation of SQMs, which must be evaluated separately".

Two smaller points. Shah et al. 2025 (MNRAS, DOI 10.1093/mnras/staf1200, arXiv:2507.11343) measure nothing themselves and restate Puschnig 2021 as "an average darkening effect of 0.0440±0.0003 mag/arcsec2 per year across three SQMs"; that figure and its error are theirs, not in Puschnig 2021. Green, Luginbuhl, Wainscoat and Duriscoe 2022 (Astron. Astrophys. Rev. 30, 1, DOI 10.1007/s00159-021-00138-3), fetched from the publisher's open page, names the Sky Quality Meter once, for its passband, and contains neither "ageing", "aging" nor "Puschnig": no rate there.

## 2. The TESS-W

None found. The one statement in a refereed paper is Alarcon, Serra-Ricart, Lemes-Perera, Mallorquín 2021, Astronomical Journal 162, 25, DOI 10.3847/1538-3881/abfdaa (arXiv:2105.01066), section 5.3:

> "The possibility that the TESS photometers suffer from aging effects is on the table. The only systematic study of this with SQM + window devices is the recent one by Puschnig et al. (2021), which suggests that a darkening of up to 0.053 mSQM arcsec−2 yr−1 can occur at midlatitudes. However, we do not observe evidence of this behavior in the continuous measurements of the TESS photometers or any bias in the distributions of photometers manufactured in different years. Further work should be done on this matter."

They give no number and no test. Their conclusions list it as open: "Future work should address possible aging effects".

Also checked: J. Zamorano, "Monitoring with TESS photometers", version 2.0, April 2026, and the "TESS Photometer Manual", version 4.1, September 2026 (both fetched today from the Madrid group's site): neither contains "aging", "ageing", "drift", "degrad", "stability" or "recalibrat". The arXiv listing of abstracts pairing "sky brightness" with aging, ageing, sensitivity drift or degradation (14 entries) holds only the SQM papers above. Nothing on the window, the dichroic filter or the sensor of the TESS-W.

## 3. The southern stratosphere, mid-2021 to 2025

### 3a. What the texts say

Sources. S. Khaykin and 19 others 2026, "Global transport of stratospheric aerosol produced by Ruang eruption from EarthCARE ATLID, limb-viewing satellites and ground-based lidar observations", Atmos. Chem. Phys. 26, 607–622, DOI 10.5194/acp-26-607-2026 (published 13 January 2026). S. Khaykin, G. Taha, T. Sakai, I. Morino, B. Liley 2025, "Stratospheric aerosols", in State of the Climate in 2024, Bull. Amer. Meteor. Soc. 106 (8), S99–S101, DOI 10.1175/BAMS-D-25-0102.1 (read in the open-archive copy of the whole chapter, `hal_insu-05525230_sotc2024_global_climate.pdf`).

Ruang ended the Hunga period (State of the Climate in 2024):

> "Extrapolation of the stable decay of the Hunga southern hemispheric sAOD during early 2024 leads to an inference of the total lifetime of the Hunga-induced stratospheric aerosol load of 2.5 years, spanning from mid-January 2022 to mid-July 2024."

> "The eruption of Ruang ended the era of Hunga-induced sAOD perturbation. The Ruang aerosols spread throughout the tropics in less than two months and were transported farther into the southern extratropics during the austral winter (Fig. 2.73a)."

How much (Khaykin 2026, section 4):

> "The Ruang eruptions caused a doubling of the tropical SAOD and a factor of 1.8 increase of the southern extratropical SAOD for several months. By the end of 2025, the SAOD has not yet returned to the pre-eruption levels, suggesting the lifetime of Ruang aerosol in the stratosphere of at least 16 months."

Injection: "a total of ∼ 0.4 Tg of SO2 into the stratosphere. The eruptive column reached altitudes of 19–25 km" (same section). Particles: "an average median radius of 0.127 µm (Dodangodage et al., 2025)".

When and where (Khaykin 2026, section 3.2; State of the Climate in 2024):

> "By mid-June, the SAOD perturbation extended across the tropical belt and started propagating into the southern extratropics leading to enhanced SAOD throughout the southern hemisphere by October 2024, i.e. by the end of the Antarctic vortex season. With that, the bulk of aerosol perturbation has remained within the tropics."

> "The massive transport of Ruang sulfates into the southern extratropics is reflected in the SH extratropical sAOD enhancement peaking in October 2024 (Fig. 2.74b)."

Heights. Tropics: "between 19–23 km altitude" in September 2024, risen 1 to 2 km by January 2025. Southern mid-latitudes (Khaykin 2026, section 3.3):

> "At the southern midlatitudes, the Ruang aerosol layer has been observed since the beginning of ATLID observations, between 15–22 km altitude with the maximum intensity at ∼ 18.5 km (Fig. 4e)."

Over Lauder (45° S) a sharp layer "near 20 km altitude" on 16 October 2024 and "a higher-altitude peak at 22 km" on 6 March 2025.

Still there in 2025: "by early May 2025 the northern extratropical SAOD has returned to the pre-eruption levels, whereas the southern extratropics were still polluted by Ruang sulphate aerosols".

A preprint not yet refereed (O. Soares, S. Khaykin and others, EGUsphere egusphere-2026-5639, discussion opened 15 October 2026) gives decay times: e-folding "Ruang (290 ± 19 days) and Hunga (379 ± 20 days)", and time to return to the level of the week before the eruption, "Ruang persisting for 738 ± 21 days", from OMPS-LP. Counted from the April 2024 eruptions that is late April or early May 2026 (my arithmetic). The latitude band used for Ruang is not stated in the passages I read.

The "before" state. 2021 was not clean. At 53° S (Punta Arenas lidar; Ohneiser et al. 2022, Atmos. Chem. Phys. 22, 7417; `src4/` copy) the Australian smoke still gave a 532 nm optical thickness of "0.015–0.03 throughout 2021" against a background of 0.005, counted from the tropopause up ("from 9 to 24 km"). That is a deeper column than the satellite figures below, which start at the 380 K level, so the two are not comparable number for number. Khaykin 2026's Figure 6 also marks La Soufrière (April 2021) just before the mid-2021 rise in the table.

### 3b. Optical depths

All in units of 10⁻³. Only the last row is printed in a paper's text; the rest I measured off published figures.

| Record (source figure) | Wavelength, layer | Latitude | Mid-2021 | Hunga peak | Just before Ruang | Mid to late 2024 | 2025 |
|---|---|---|---|---|---|---|---|
| GloSSAC to 2023, then SAGE III/ISS (Khaykin 2026, Fig. 6) | 525 nm, above 380 K | 60° S–25° S | 6.3–6.4 in Mar–May; 7.4 in Jun; 8.7–9.0 in Aug–Oct | 24.8 in Aug–Sep 2022 | 6.9–7.0 in Mar–Apr 2024 | 8.8 Jun; 11.2 Jul; 12.9–13.1 Aug–Oct; 12.0 Dec | 11.6 Jan; 9.6–9.9 Feb–May; 10.1–10.3 Jun–Jul (curve ends) |
| SAGE III/ISS zonal mean (State of the Climate in 2025, Fig. 2.72b) | 532 nm, 380 K to 33 km | 50° S–40° S | 8.3–8.9 in Jun–Sep | 29.8 in Aug 2022 | 7.6–8.0 in Mar–May 2024 | 12.2 Jul; 13.9 Aug; 15.1 Oct | 12.6 Jan; 10.0–10.1 Mar–Apr; 11.7–12.1 Jul–Aug; 11.2 Oct (last point) |
| Lauder lidar, monthly means (same figure) | 532 nm, 380 K to 33 km | 45° S | 5.9–6.6 in Jun–Sep | 28.0 in Aug 2022 | 7.1–7.9 in Mar–Apr 2024 | 15.7–16.6 Jul–Aug (top of curve about 18); 12.2–12.7 Oct–Dec | 8.9–9.3 Feb–Mar; 11.0–11.5 Apr–May; 16.4 Jul (top about 17); 8.2–9.2 Sep–Dec |
| OMPS-LP on NOAA-21 (Khaykin 2026, Fig. 2a, colour map) | 869 nm | 20° S–45° S | figure starts April 2024 | – | 2.3–2.5 in Apr–May 2024 | 3.3 Jun; 4.8–5.6 Jul–Oct; 4.3 Dec | 3.8 Jan; 3.1–3.3 Feb–Jun; 3.3–3.7 Jul–Oct |
| same, narrower bands | 869 nm | 20–30° S / 30–40° S / 40–50° S | – | – | 2.1 / 2.4–2.7 / 2.7 (Apr–May) | peaks 4.7 (Sep) / 6.0 (Oct) / 6.9 (Oct) | May to Oct: 2.9 falling to 2.6 / 3.1 rising to 4.0 then 3.6 / 3.6 rising to 4.7 |
| Punta Arenas lidar (Ohneiser 2022, text) | 532 nm, tropopause up | 53° S | 15–30 "throughout 2021" | – | – | – | – |

What the table shows. In the first row the step from the March–April 2024 low to August–October 2024 is 6.95 to 13.0, a factor of 1.87, which agrees with the paper's printed "factor of 1.8"; that is my only check of the readings against a printed number. By these records the southern mid-latitudes in 2025 stood above mid-2021: by 7 to 18 per cent in the first row (9.6–10.3 against 8.7–9.0) and by 12 to 52 per cent in the second (10.0–12.6 against 8.3–8.9). Mid-2021 itself stood above early 2021. In the OMPS-LP map the southern enhancement grows with latitude (peaks of 4.7 at 20–30° S, 6.0 at 30–40° S, 6.9 at 40–50° S), and 20–30° S is a low band between the tropical and mid-latitude maxima throughout.

The State of the Climate in 2025 figure (Bull. Amer. Meteor. Soc. 107 (8), page S100, Fig. 2.72) I have only as the first page of a repository copy of the section that follows it (`dlr_Steinbrecht_BAMS_2026.pdf`). The text of that year's aerosol section I could not open (the publisher's site refused), so two things are unexplained here: the July 2025 spike in the Lauder lidar curve (about 16, against 12 in the satellite zonal mean), and a mild rise through mid-2025 that shows in the SAGE III curve for 50–40° S (10.0 to 12.1) and in the OMPS-LP map at 30–50° S, barely in the 60–25° S curve, and not at 20–30° S. Neither Khaykin 2026 nor anything else I opened comments on them.

### 3c. Anything else in 2025

Nothing else in the southern stratosphere is named in what I opened. Khaykin 2026 names one 2025 event, northern: wildfires "in Canada and Siberia" in late May 2025. Lewotobi Laki-laki (Flores, Indonesia) "erupted on July 7, 2025, propelling a column of ash 18 kilometers (11 miles) into the air" (NASA Earth Observatory note); I found no published stratospheric aerosol measurement of it, and Khaykin 2026 does not mention it (word count 0). Hayli Gubbi (Ethiopia, November 2025) is northern and known to me from search snippets only.

## 4. Twilight after Hunga, southern hemisphere

Measurements:

- **Paranal, Chile (24.6° S).** R. J. De Rosa, A. Otarola, T. Szeifert, J. Smoker, F. Selman, A. Mehner, F. Bian, E. Sedaghati, J. V. Seidel, A. Smette, W.-J. de Wit 2023, "Effects of the Hunga Tonga–Hunga Ha‘apai Volcanic Eruption on Observations at Paranal Observatory", The Messenger 190, DOI 10.18727/0722-6691/5315 (arXiv:2305.08620). Twilight flat fields, so colour and decay, not zenith brightness in a visual band:

  > "A few days after the volcanic eruption, the ratio of the i (770 nm) and both the u (350 nm) and g (480 nm) flatfields increased by a factor of five, indicating a significant reddening of the twilight sky, and these have still not returned to the pre-explosion values one year later."

  > "Dome flatfields obtained with the same filters do not show any change in the flux ratio, indicating that the observed effect is atmospheric and not instrumental."

  Near-infrared (2.1 µm) twilight counts against Sun elevation (the plot's axis is labelled from −5° to −8°) changed their decay; the fitted layer height is 36 km for March 2022 and 29 km for November 2022. Visual: "a year later stunning sunsets are still being seen at Paranal."
- **Lauder, New Zealand (45° S).** L. Mukherjee, D. L. Wu, N. Abuhassan, T. F. Hanisco and others 2025, "Twilight Near-Infrared Radiometry for Stratospheric Aerosol Layer Height", Remote Sensing 17 (12), 2071, DOI 10.3390/rs17122071 (reference from Crossref; text read in the NASA manuscript, `src4/` copy). Zenith twilight spectra used to find the layer height; the date it names is "November 26, 2022". No time series and no statement of how much brighter the sky was (the words "brighter" and "time series" do not occur in its text).
- **La Silla (29° S), your known paper.** Its own sentence on 2022: "An anomaly seems to be present in the year 2022, when a strong variation in AOD appears, even if it does not correspond to a high variation in the SQM measurements."

Visual reports, with place and months:

- New Zealand, from late May 2022: NIWA news note, 15 June 2022: "Since late May, NIWA’s forecasting team has been flooded with messages from members of the public across the country, enquiring about a strange but beautiful phenomenon – stunning, fiery colours in the sky, appearing just before or after the sun crosses the horizon." The Lauder lidar saw aerosol "at around 20-25 kilometres above New Zealand."
- Scott Base, Antarctica, July 2022: Antarctica New Zealand news note, 15 July 2022 (same text on NIWA's site), with aerosol "between 15 – 24km above Antarctica". NASA's SAGE note of 20 September 2022: "In July, purple and pink hues painted the Antarctica and New Zealand skies".
- Not journal or agency, so leads only: S. J. O'Meara, Astronomy magazine, 1 August 2022, Maun, Botswana (20° S), January and February 2022 (`src4/` copy). P. Lowenstein, EarthSky community gallery, Mutare, Zimbabwe (19° S): on 23 May 2022 he describes "more prolonged colourful post-sunset and pre-dawn twilights which persist longer after sunset and appear earlier before sunrise", and on 31 January 2023, after 308 photographed evenings, "it is only recently after almost a year that the volcanic sunsets are becoming less frequent and have diminished in intensity."

That gallery entry is the only place I found the words "persist longer" for the twilight. No journal paper or agency note I found reports a brighter or longer twilight as a measurement.

## Searched for and not found

- A published ageing or drift rate for the TESS-W, or any laboratory test of its window, dichroic filter or sensor.
- An SQM, TESS-W or all-sky camera record of twilight after Hunga, other than Fiorentin 2025. Searches named La Silla, Cerro Tololo, Cerro Pachón, Las Campanas, Siding Spring, the South African observatory, El Leoncito, Brazil, Argentina, Australia, Namibia.
- Any journal report of purple or vivid twilights from South America other than Paranal.
- A paper printing southern mid-latitude stratospheric optical depth as numbers for mid-2021, mid-2024 and 2025. Only factors and figures are printed.
- A published stratospheric aerosol measurement of any 2025 eruption in the southern hemisphere.
- An arXiv paper since 2020 pairing twilight or sky brightness with Hunga, Tonga or volcano words (the listing returned four entries, the newest from January 2020; the Paranal paper's abstract does not use those words).

## Could not open, or did not

- PubMed Central (Fiorentin 2025): a bot check came back to the command-line client; left alone, the `src2/` copy from yesterday used. Europe PMC's service reset the connection twice.
- mdpi.com (Fiorentin 2022): 403; the University of Padua repository copy used instead.
- American Meteorological Society pages and the NOAA repository copy of State of the Climate in 2024: refused (405, 403). The 2024 chapter was read from the French open archive. The text of the 2025 aerosol section: not found anywhere open.
- Fiorentin et al. 2022, Measurement 191, 110823 (the window and filter measurements): not tried; known through Fiorentin 2025.
- Dodangodage et al. 2025, J. Quant. Spectrosc. Radiat. Transfer 333, 109333: read only the abstract of the NASA manuscript copy (aerosol "at an altitude of approximately 20 km" ten days after the eruption).
- "Tropopause Height Inferred from Twilight Photometry", Bull. Amer. Meteor. Soc.: snippet only, not opened.
- Fetched, found to hold nothing on these questions, and deleted: two EGUsphere preprints on Hunga (northern transport; ultraviolet retrievals), a paper on another sky sensor, the Antarctic chapter of State of the Climate in 2025 and the ozone section of the 2024 edition. Kept though off the subject: a 2023 conference abstract on twilight spectra over Tbilisi, 2021 to 2022, northern (`egu23-13861_abstract.html`). Saved and not quoted: the State of the Climate in 2023 chapter (`hal_insu-04682457_sotc2023_strat_aerosols.pdf`), whose caption to the same Lauder figure gives the layer as "between 380 K and 1000 K potential temperature".
- The place latitudes in section 4 (Paranal, La Silla, Maun, Mutare) are from general knowledge, not from the sources.
- This was a search of about 25 minutes. Grey literature (network reports, conference posters) is thinly covered, so "not found" is not "does not exist".
