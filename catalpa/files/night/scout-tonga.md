# Scout report: twilight sky brightness after the Hunga Tonga eruption

Written 27 November 2026 (searches and downloads 19:04 to about 19:20 UTC). Saved files are under `/home/agent1/night/lit/src4/` unless a path says `src/` or `src2/` (those were already on the machine).

How to read the quotations. Every block quotation below was checked by machine against the saved file named on the line under it (`/tmp/scout4/qcheck.py`: Unicode NFKC, all white space and all hyphens removed on both sides, then exact containment). So a hyphen lost at a line end in the PDF text ("posteruption", "highaltitude", "MonteCarlo") is written here with its hyphen; nothing else is altered. "Read off the figure" means I looked at a rendered page image and estimated by eye. "From memory, not verified" means what it says. Text outside block quotations is my summary.

Short answer. A changed twilight sky after Hunga is in print (colour and near-infrared twilight flats at Paranal; zenith twilight radiometry at Lauder; a zenith LED twilight photometer in Texas; many visual reports). A brighter broadband zenith sky at a solar depression near 6.5 degrees, measured with SQM or TESS-W photometers, I did not find anywhere. The nearest thing in print is a La Silla SQM twilight series to early 2024 (Fiorentin et al. 2025) whose authors report no apparent trend and do not mention the eruption; yet their own plot, read by eye, shows 2022 and 2023 brighter than 2019 to 2021 by roughly 0.05 to 0.15 magnitude (see 4a, with its two reservations).

---

## 1. Twilight measurements and reports after Hunga (2022 to 2024)

### 1a. De Rosa et al. 2023, Paranal (24.6 S): twilight flat fields in colour and in the near infrared. The best single source.

R. J. De Rosa, A. Otarola, T. Szeifert, J. Smoker and others, "Effects of the Hunga Tonga-Hunga Ha'apai Volcanic Eruption on Observations at Paranal Observatory", The Messenger 190, 58 (2023), DOI 10.18727/0722-6691/5315, arXiv:2305.08620. Fetched: https://arxiv.org/pdf/2305.08620 . Saved: `arxiv_2305.08620.pdf`, `arxiv_2305.08620_flow.txt`.

> A few days after the volcanic eruption, the ratio of the i (770 nm) and both the u (350 nm) and g (480 nm) flatfields increased by a factor of five, indicating a significant reddening of the twilight sky, and these have still not returned to the pre-explosion values one year later.
> — `src4/arxiv_2305.08620_flow.txt`

> Dome flatfields obtained with the same filters do not show any change in the flux ratio, indicating that the observed effect is atmospheric and not instrumental.
> — `src4/arxiv_2305.08620_flow.txt`

> A sudden change in the decay time of the twilight was also observed in near-infrared data from the HAWK-I instrument at the VLT. Figure 3 shows the count rate during twilight with the Ks filter as a function of the elevation of the Sun, before and after the volcanic eruption.
> — `src4/arxiv_2305.08620_flow.txt`

> The change in the decay time of the sky brightness in the HAWK-I twilight flatfields can be explained by a 36-km-high column of dust in the line of site of the telescope, which became the dominant source of reflection rather than the molecular gas in the troposphere before the eruption.
> — `src4/arxiv_2305.08620_flow.txt`

> In observations obtained in November 2022, the flatter twilight flatfield decay time indicates a decreasing density of the dust in the stratosphere and a reduction in the height of the dust layer down to 29 km, indicated by the later onset of the infrared twilight and illustrated in Figure 3.
> — `src4/arxiv_2305.08620_flow.txt`

> These effects were not immediately transitory in nature, and a year later stunning sunsets are still being seen at Paranal.
> — `src4/arxiv_2305.08620_flow.txt`

What it shows. A measured, lasting change of twilight colour (a ratio, i against u and g, times five, still there after one year) and a brighter near-infrared (Ks, 2.1 micron) twilight. Read off their Figure 3 (by eye): at Sun elevations of about -4.8 to -5.5 degrees the Ks count rates after the eruption are several times the "before eruption" curve; by about -6 degrees every curve has fallen to a nearly flat floor, the post-eruption points sitting a little above the pre-eruption ones. It is a colour ratio and a near-infrared curve, not a visual-band zenith brightness; no magnitude of brightening in the visual is given. The time series in the paper ends January 2023, so it does not say when the effect ended. Their 36 km and 29 km are heights from a simple shadow model of the Ks decay, not lidar heights (see 2).

The same paper on extinction (the sentence begins "The increase in extinction" in the previous column):

> that could be attributed to an increase in aerosol content in the stratosphere (at 25–27 km altitude) from the volcano is not significant compared to the seasonal variability in the sky extinction.
> — `src4/arxiv_2305.08620_flow.txt`

### 1b. Mukherjee et al. 2025, Lauder, New Zealand (45 S): zenith twilight radiometry with a spectrometer.

L. Mukherjee, D. L. Wu, N. Abuhassan, T. F. Hanisco, ... F. M. Mims III and others, "Twilight Near-Infrared Radiometry for Stratospheric Aerosol Layer Height". Fetched (NASA NTRS manuscript): https://ntrs.nasa.gov/api/citations/20250006477/downloads/Twilight%20Near-Infrared%20Radiometry.pdf . Saved: `ntrs_20250006477_twilight_nir_radiometry.pdf`, `_flow.txt`. A search result gives the published version as Remote Sensing 17, 2071 (2025); I did not fetch that version, so the journal reference is not verified from a saved page.

> Twilight ResPan data are also used to estimate the aerosol layer height, with results in good agreement with SAGE and lidar measurements, particularly following the Hunga Tonga eruption in Lauder, New Zealand.
> — `src4/ntrs_20250006477_twilight_nir_radiometry_flow.txt`

> November 26, 2022, was chosen because it followed the Hunga Tonga volcanic eruption, allowing for the observation of aerosol injection into the stratosphere.
> — `src4/ntrs_20250006477_twilight_nir_radiometry_flow.txt`

> Without refraction, the detected height is 28 km, which is higher than the 23 km detected when refraction is included. On the same day lidar data were obtained from Lauder (Figure 17) [67], as well as SAGE data (Figure 25). Both indicate an aerosol layer at a height of approximately 18 km.
> — `src4/ntrs_20250006477_twilight_nir_radiometry_flow.txt`

What it shows. Zenith twilight spectra (450 to 1050 nm) at a southern mid-latitude site in November 2022 used to find the height of the Hunga layer. It is a method paper using a few twilights at solar zenith angles near 94 degrees; it gives no time series and no statement of how much brighter the zenith was than in other years.

### 1c. Mims 2023 (popular article), Texas (29.6 N): zenith LED twilight photometer.

F. M. Mims III, "King of the Ring of Fire", Make: magazine, dated on the page 28 July / 1 August 2023. Fetched: https://makezine.com/projects/king-of-the-ring-of-fire . Saved: `makezine_king_of_the_ring_of_fire.html`, `.txt`. Not peer reviewed.

> An LED twilight photometer is an ultra-sensitive light meter that detects the intensity of scattered sunlight directly overhead (the zenith) for around 90 minutes after sunset or before sunrise.
> — `src4/makezine_king_of_the_ring_of_fire.txt`

> Hunga Tonga aerosols began arriving over my Texas site in May 2022, and I soon began measuring aerosols higher than 30km (98,425 feet).
> — `src4/makezine_king_of_the_ring_of_fire.txt`

> Figure G shows an LED twilight photometer sky profile on November 6, 2022, from the surface to 50km (164,042ft). The profile shows that the densest region of the Hunga Tonga plume was at 25.8km.
> — `src4/makezine_king_of_the_ring_of_fire.txt`

What it shows. A zenith twilight photometer in the NORTHERN subtropics is reported to have recorded the Hunga layer from May 2022. This bears on "northern photometers show nothing" (see the cautions).

### 1d. Visual reports (news, agency pages)

NIWA news item, 15 June 2022, "Seen a stunning sunrise or sunset lately? The Tongan volcano may be the cause". Fetched: https://niwa.co.nz/news/seen-stunning-sunrise-or-sunset-lately-tongan-volcano-may-be-cause . Saved: `niwa2022_sunset_news.html`, `.txt`.

> NIWA has been flooded with enquiries about a strange but beautiful phenomenon – stunning, fiery colours in the sky, appearing just after sunset.
> — `src4/niwa2022_sunset_news.txt`

> To understand these sightings, the forecasting team contacted their colleagues at the Lauder Atmospheric Research Station in Central Otago, who confirmed that their ground-based LIDAR (Light Detection and Ranging) instrument has been detecting unusual spikes in aerosols in the stratosphere, at around 20-25 kilometres above New Zealand.
> — `src4/niwa2022_sunset_news.txt`

Radio New Zealand, 15 June 2022 (same NIWA statement). Fetched: https://www.rnz.co.nz/news/national/469158/stunning-skies-may-be-byproduct-of-tonga-volcano-eruption . Saved: `rnz2022_469158.html`, `.txt`.

> "We're expecting we could see vibrant sunsets for even months to come. I think the concentrations are increasing so they're certainly not going away in the short term."
> — `src4/rnz2022_469158.txt`

NASA SAGE blog, "SAGE III Sees Tonga Aerosols, Water Vapor Months After Eruption". Fetched: https://sage.nasa.gov/?p=6810 . Saved: `nasa_sage_p6810.html`, `.txt`.

> In July, purple and pink hues painted the Antarctica and New Zealand skies — likely the result of atmospheric particles called aerosols that belched into the stratosphere in January during the eruption of the Hunga Tonga-Hunga Ha’apai volcano.
> — `src4/nasa_sage_p6810.txt`

S. J. O'Meara, "Volcanic twilights", Astronomy magazine, published 1 August 2022 (Maun, Botswana, 20 S). Fetched: https://www.astronomy.com/observing/volcanic-twilights/ . Saved: `astronomy_com_volcanic_twilights.html`, `.txt`.

> The plume contained 400,000 tons of sulfur dioxide, which drifted west with the stratospheric winds — and soon began to produce remarkable sunsets in the Southern Hemisphere. Stunning images appeared in the news as the cloud swept west over Australia.
> — `src4/astronomy_com_volcanic_twilights.txt`

> Even after the official start of night, volcanic glow and ruffled clouds remained visible to the unaided eye close to the western horizon for several minutes.
> — `src4/astronomy_com_volcanic_twilights.txt`

What these show. Vivid twilights were reported from Australia (January 2022), southern Africa (January and February 2022), New Zealand (from about June 2022, said to be increasing), Antarctica (July 2022), and Paranal (still in early 2023). None gives a brightness measurement. I found no dated published statement of when the vivid twilights stopped.

### 1e. Ugolnikov and Maslov: nothing on Hunga found

I listed the arXiv papers with author Ugolnikov down to October 2026 (saved: `arxiv_api_ugolnikov.xml`, from http://export.arxiv.org/api/query?search_query=au:Ugolnikov ). No title names Hunga or Tonga; since 2020 the titles are on noctilucent clouds and polar stratospheric clouds. Their twilight sounding is done from central Russia (55 N). Their last volcanic twilight paper is on Raikoke 2019 (see 3d). This covers arXiv only; a journal-only paper would not show.

---

## 2. How long, how far, how high

### 2a. APARC 2025, the Hunga report (the review to cite)

APARC, 2025: The Hunga Volcanic Eruption Atmospheric Impacts Report, Y. Zhu, G. Mann, P. A. Newman, W. Randel (Eds.), APARC Report No. 11, WCRP Report No. 10/2025, DOI 10.34734/FZJ-2025-05237. Chapter 3 lead authors S. Khaykin and A. Bourassa. Fetched: https://ntrs.nasa.gov/api/citations/20260001207/downloads/Hunga_APARC_Report_Frontmatter.pdf (front matter with executive summary) and https://aparc-climate.org/wp-content/uploads/2025/12/Hunga_APARC_Report_Chapter_3.pdf . Saved: `aparc_hunga_report_frontmatter_ntrs_20260001207.pdf`, `aparc_hunga_report_chapter_3.pdf`, each with `_flow.txt`; index page `aparc_report_no_11_page.html`.

Arrival at southern mid-latitudes:

> After initially covering the lower-stratospheric tropics in February 2022, both water vapour and aerosol spread into the southern midlatitudes during the austral fall (April-June 2022) as the stratospheric flow reversed from westward to eastward
> — `src4/aparc_hunga_report_frontmatter_ntrs_20260001207_flow.txt`

> the Hunga aerosol largely shifted towards southern mid-latitudes three months after the eruption, in mid-April.
> — `src4/aparc_hunga_report_chapter_3_flow.txt`

> In five months (by June 2022) the bulk of Hunga aerosol had been transported to the southern mid-latitude stratosphere due to efficient winter transport; northward transport was much weaker and more sporadic during that season.
> — `src4/aparc_hunga_report_chapter_3_flow.txt`

> the peak of the SAOD perturbation at Lauder (45° S) was observed during June–July 2022 (Figure 3.7a).
> — `src4/aparc_hunga_report_chapter_3_flow.txt`

Decay:

> In six months (by July 2022) the global stratospheric aerosol optical depth, which was still dominated by the aerosol in the southern hemisphere, reached a maximum value of 0.01 at 1 µm, and then decayed with an e-folding time of 20 months.
> — `src4/aparc_hunga_report_chapter_3_flow.txt`

> It took over two years for the stratospheric aerosol optical depth to decay to pre-eruption levels. Throughout this time, the bulk of the aerosol remained below 30 km.
> — `src4/aparc_hunga_report_chapter_3_flow.txt`

> One year after the eruption, in early 2023, the Hunga aerosol was spread across the entire Southern Hemisphere, and the SAOD decay rate in the Southern Hemisphere slowed and followed the global decay. By March 2024, more than two years post-eruption, the global and hemispheric SAOD time series converged and approached pre-eruption levels by mid-April 2024.
> — `src4/aparc_hunga_report_chapter_3_flow.txt`

> Extrapolation of the stable decay of Hunga southern-hemispheric SAOD during early 2024 leads to an inferred total lifetime of the Hunga-induced stratospheric aerosol load of about 2.5 years, spanning from mid-January 2022 to mid-July 2024.
> — `src4/aparc_hunga_report_chapter_3_flow.txt`

> Observations from this station are representative of the volcanic aerosol that persisted in the southern mid-latitudes until 2024 (see Section 3.1).
> — `src4/aparc_hunga_report_chapter_3_flow.txt`

> After 2024, the Hunga aerosol loading largely disappeared.
> — `src4/aparc_hunga_report_frontmatter_ntrs_20260001207_flow.txt`

Northern hemisphere:

> whereas the larger-scale increase in the northern extratropical SAOD was not observed before early 2023 (Figure 3.1a). However, by far, the bulk of Hunga aerosol remained in the Southern Hemisphere.
> — `src4/aparc_hunga_report_chapter_3_flow.txt`

> At the northern mid-latitudes (Figure 3.7d), the OHP record shows a small increase in SAOD in late 2022, reflecting the gradual transport of Hunga aerosols to the northern extratropics (Section 3.1).
> — `src4/aparc_hunga_report_chapter_3_flow.txt`

> Volcanic aerosol remained mostly in the tropics and SH lower stratosphere through 2024.
> — `src4/aparc_hunga_report_frontmatter_ntrs_20260001207_flow.txt`

> Hunga water vapour had spread to the Northern Hemisphere (NH) midlatitudes about one year after the eruption in January-March 2023.
> — `src4/aparc_hunga_report_frontmatter_ntrs_20260001207_flow.txt`

Altitude:

> The infrared cooling due to Hunga water vapour caused the initial cloud to descend to around 23-27 km altitude by the middle of February 2022, where it resided for the following few months.
> — `src4/aparc_hunga_report_frontmatter_ntrs_20260001207_flow.txt`

> Past August 2022 (Panels G-O) there is a marked altitude separation between the extinction and effective radius peaks, with the extinction peak remaining near 22 km while the effective radius peak continues to drop.
> — `src4/aparc_hunga_report_chapter_3_flow.txt`

(That last sentence is for the tropics, 10 S to 10 N, from SAGE III/ISS.) Particle size:

> The aerosol particles grew to an effective radius of 0.4 µm in the densest part of the volcanic cloud within a couple of weeks, and the size was roughly maintained through the first two years.
> — `src4/aparc_hunga_report_frontmatter_ntrs_20260001207_flow.txt`

Water vapour went up, the aerosol went down:

> The excess water vapour remained at 20-32 km altitude until October 2022. After November 2022, the Hunga water vapour was carried upward by the tropical stratospheric circulation and reached the mesosphere by early 2023
> — `src4/aparc_hunga_report_frontmatter_ntrs_20260001207_flow.txt`

Read off Figure 3.1 of Chapter 3 (page 66; OMPS-LP NASA v2.1, 997 nm; by eye, so rough). Panel (c), southern-hemisphere mean SAOD: about 0.003 before the eruption; peak about 0.017 near July to August 2022; about 0.012 at the start of 2023; about 0.007 at the end of 2023; about 0.004 by April 2024; then rising again (Ruang) to about 0.006 by mid-2024. Northern-hemisphere mean: a peak near 0.006 around April to May 2022, then about 0.004 through 2023. Panel (a): the brightest patch of the whole record sits at about 30 to 45 S from about May to September 2022.

What it shows. At 30 to 40 S: arrival April to June 2022, peak about June to August 2022, slow decay through 2023 (e-folding about 20 months), back near pre-eruption level about April 2024. So by this record 2023 should be noticeably weaker than 2022, and 2024 near normal until Ruang. Layer height: bulk always below 30 km; about 23 to 27 km in early 2022, extinction peak near 22 km in the tropics afterwards, and lower at mid-latitudes (about 18 km over Lauder in November 2022 by lidar, see 1b; 20 to 25 km over New Zealand in June 2022, see 1d).

### 2b. Supporting papers

B. Legras et al. 2022, "The evolution and dynamics of the Hunga Tonga-Hunga Ha'apai sulfate aerosol plume in the stratosphere", Atmos. Chem. Phys. 22, 14957. Fetched: https://acp.copernicus.org/articles/22/14957/2022/acp-22-14957-2022.pdf . Saved: `legras2022_acp-22-14957-2022.pdf`, `_flow.txt`. (Title, authors and pages checked against the saved file.)

> induced a descent of the plume to 24–26 km over the first 3 weeks by radiative cooling.
> — `src4/legras2022_acp-22-14957-2022_flow.txt`

> volcanic sulfates and water still persisted after 6 months, mainly confined between 35◦ S and 20◦ N until June due to the zonal symmetry of the summer stratospheric circulation at 22–26 km.
> — `src4/legras2022_acp-22-14957-2022_flow.txt`

S. Khaykin et al. 2022, "Global perturbation of stratospheric water and aerosol burden by Hunga eruption", Communications Earth and Environment 3, 316. Fetched: https://www.nature.com/articles/s43247-022-00652-x . Saved: `khaykin2022_s43247-022-00652-x.html`, `.txt`. (Title checked against the saved page; volume and article number from memory, not verified.)

> Owing to the extreme injection altitude, the volcanic plume circumnavigated the Earth in only 1 week and dispersed nearly pole-to-pole in three months.
> — `src4/khaykin2022_s43247-022-00652-x.txt`

> Overall, in about 3 months since the eruption, the Hunga sulfates have spread nearly pole-to-pole, although the aerosol layers detected in the Northern extratropics are less intense, with scattering ratios below 1.8 (Fig. S4).
> — `src4/khaykin2022_s43247-022-00652-x.txt`

G. Taha et al. 2022, "Tracking the 2022 Hunga Tonga-Hunga Ha'apai aerosol cloud in the upper and middle stratosphere using space-based observations", Geophys. Res. Lett. Fetched (accepted manuscript on NASA NTRS): https://ntrs.nasa.gov/api/citations/20220016184/downloads/AGU_Manuscript_Hung_Tonga_gtaha.pdf . Saved: `taha2022_ntrs_20220016184.pdf`, `_flow.txt`.

> Within two weeks, the bulk of the injected material circulated the globe between 20 – 30 km altitude, as observed by satellite instruments.
> — `src4/taha2022_ntrs_20220016184_flow.txt`

B. G. Martinsson, J. Friberg, M. K. Sporre 2025, "Stratospheric aerosol formed by intense volcanism-sea interaction during the 2022 Hunga Ha'apai eruption", Atmos. Chem. Phys. 25, 10677. Fetched: https://acp.copernicus.org/articles/25/10677/2025/acp-25-10677-2025.pdf . Saved: `martinsson2025_acp-25-10677-2025.pdf`, `_flow.txt`. Saved but not quoted; it calls the event the strongest stratospheric aerosol event since Pinatubo.

What they show. Thin northern layers existed within three months, but weak. A small part of the early cloud was much higher (OMPS-LP saw material above 36 km for two and a half months, Taha et al., from their abstract), but the bulk was at 20 to 30 km.

---

## 3. Physics: does a stratospheric layer brighten or darken the zenith at 5 to 8 degrees depression?

The literature I could open does not give one answer for your geometry. What it does give:

### 3a. Where the shadow is

F. Patat, O. S. Ugolnikov, O. V. Postylyakov 2006, "UBVRI twilight sky brightness at ESO-Paranal", Astron. Astrophys., arXiv:astro-ph/0604128. Fetched: https://arxiv.org/pdf/astro-ph/0604128 . Saved: `arxiv_astro-ph_0604128.pdf`, `.txt` (layout), `_flow.txt`. Their Table A.1 (read from the layout text) gives the height of the lower boundary of the Earth's geometric shadow at the zenith: 8.8 km at 3 degrees depression, 35.1 km at 6 degrees, 79.5 km at 9 degrees. My own arithmetic with R(1/cos d - 1) gives about 41 km at 6.5 degrees, as you had.

> the atmospheric layers below ∼30 km (see Table A.1), where the ozone and aerosol stratospheric concentration is maximum.
> — `src4/arxiv_astro-ph_0604128_flow.txt`

(The sentence begins, on the previous page, "since for these low Sun depression angles the lower shadow's boundary passes through"; it is about depressions of 0 to 6 degrees.)

> phases of twilight (also known as deep twilight) are dominated by multiple scattering (Rozenberg 1966), the amount of scattered sunlight is strongly dependent on the amount of aerosol in the lower atmospheric layers
> — `src4/arxiv_astro-ph_0604128_flow.txt`

> Nevertheless, during the deep twilight, when the direct Sun radiation illuminates only the upper atmospheric layers and single scattering on air molecules becomes progressively less important, the amount of aerosols and ozone plays a relevant role through multiple scattering.
> — `src4/arxiv_astro-ph_0604128_flow.txt`

O. S. Ugolnikov, I. A. Maslov 2018, "Optical Depth and Vertical Profile of Stratospheric Aerosol based on Multi-Year Polarization Measurements of the Twilight Sky", arXiv:1807.04365. Fetched: https://arxiv.org/pdf/1807.04365 . Saved: `arxiv_1807.04365.pdf`, `_flow.txt`.

> Consider the twilight period corresponding to the solar zenith angles from 96° to 98°. Due to Chappuis absorption bands of stratospheric ozone, the effective shadow of the Earth is 15-20 km higher than its geometric altitude, and effective single scattering during this period takes place above the stratospheric aerosol layer. Assume that the sky background consists of Rayleigh and multiple scattering.
> — `src4/arxiv_1807.04365_flow.txt`

> 2016 showed an excess of brightness and decrease of polarization of the dusk sky segment during the light stage of twilight (solar zenith angle 92-95°) in the red spectral range. These effects were interpreted by Ugolnikov and Maslov (2018ab) as the presence of stratospheric aerosol scattering.
> — `src4/arxiv_1807.04365_flow.txt`

What these show. At your moment (solar zenith angle about 96.5 degrees) a layer at 18 to 26 km straight overhead is inside the Earth's shadow; Ugolnikov and Maslov use exactly 96 to 98 degrees as the stage where single scattering is above the aerosol layer. Direct single scattering by the layer overhead is seen at 92 to 95 degrees, not at 96.5. Any effect of the layer at 96.5 degrees has to come by multiple scattering (sunlit parts of the layer towards the Sun lighting the air overhead) or by extinction of the grazing sunlight on its way in.

### 3b. Brightening by multiple scattering in the layer (after Pinatubo)

N. Mateshvili, D. Fussen, G. Mateshvili, I. Mateshvili, F. Vanhellemont and others 2013, "Nabro volcano aerosol in the stratosphere over Georgia, South Caucasus from ground-based spectrometry of twilight sky brightness", Atmos. Meas. Tech. 6, 2563. Fetched: https://amt.copernicus.org/articles/6/2563/2013/amt-6-2563-2013.pdf . Saved: `mateshvili2013_amt-6-2563-2013.pdf`, `_flow.txt`. (Title and pages checked against the saved file; author list beyond the first from memory, not verified.)

> Reconsideration of measurements acquired soon after the Pinatubo eruption in 1991 allowed to model the phenomenon of the “second purple light”, a twilight sky brightness enhancement at large solar zenith angles (97–102◦ ). Monte-Carlo modelling reveals that the second purple light is caused by multiple scattering in the stratospheric aerosol layer.
> — `src4/mateshvili2013_amt-6-2563-2013_flow.txt`

> As we have seen above, stratospheric aerosol disturbs significantly twilight sky brightness in the SZA range 91–95◦ .
> — `src4/mateshvili2013_amt-6-2563-2013_flow.txt`

> that the first purple light is mainly caused by primary scattering in the SAL near the observational place. The second purple light is caused mainly by double and triple scattering (Fig. 16).
> — `src4/mateshvili2013_amt-6-2563-2013_flow.txt`

> The second purple light is a quite rare phenomenon which is observed only after strong volcanic eruptions.
> — `src4/mateshvili2013_amt-6-2563-2013_flow.txt`

What it shows. A published case of a BRIGHTER twilight sky at solar zenith angles of 97 to 102 degrees after a large eruption, explained by double and triple scattering in the layer. Limits: the Pinatubo curve (8 November 1991, Abastumani, 41.8 N) was taken at 713 nm with a 1 degree field at a viewing zenith angle of 60 degrees, not at the zenith (read from their Table 1; the 2009 to 2011 work is at 780 nm, 40 to 50 degrees from the zenith, azimuth near the Sun's); Pinatubo was a far larger load than Hunga; and the authors call the phenomenon rare.

### 3c. Modelled zenith twilight with a thin layer (optical depth 0.003 to 0.01)

Mukherjee et al. 2025 (source as in 1b):

> For the twilight model, the dependence of scattered intensity on AOD and ALH is investigated using the Monte Carlo RT code from libRadtran [24], and results are shown for SZA = 94◦ in Figure 11. Larger AODs result in higher scattered intensities
> — `src4/ntrs_20250006477_twilight_nir_radiometry_flow.txt`

> Twilight sky brightness is caused by sunlight scattered by molecules, aerosols, and ozone in a thin volume of air above the momentary height of Earth’s shadow during sunset/sunrise, as shown in Figure 1.
> — `src4/ntrs_20250006477_twilight_nir_radiometry_flow.txt`

What it shows. For the zenith at a solar zenith angle of 94 degrees, at 775 nm, more stratospheric aerosol means more light. Nothing is given for 96.5 degrees or for a broad visual band.

G. E. Shaw 1980, "Radiance and color of the sky at twilight: Perturbations caused by stratospheric haze", Pure and Applied Geophysics 119, 231 to 247. Abstract page fetched: https://link.springer.com/article/10.1007/BF00877763 . Saved: `springer_BF00877763.html`, `.txt`. Abstract only.

> Layers of stratospheric aerosol with optical thicknesses as small as 10−4 cause noticeable perturbations in the monochromatic logarithmic brightness gradient
> — `src4/springer_BF00877763.txt`

### 3d. Measured brightening and measured dimming

O. S. Ugolnikov, I. A. Maslov 2020, "Post-Volcanic Aerosol Altitude and Particle Size Measurements Basing on Twilight Sky Polarimetry", arXiv:2001.06034 (Raikoke 2019, seen from 55 N). Fetched: https://arxiv.org/pdf/2001.06034 . Saved: `arxiv_2001.06034.pdf`, `_flow.txt`.

> An increase in sky brightness paired with a decrease in polarization was registered, especially noticeable in the dusk segment.
> — `src4/arxiv_2001.06034_flow.txt`

K. L. Coulson 1983, "Effects of the El Chichon volcanic cloud in the stratosphere on the intensity of light from the sky", Applied Optics 22, 2265. Abstract page fetched: https://opg.optica.org/abstract.cfm?URI=ao-22-15-2265 . Saved: `coulson1983_optica_abstract.html`. Abstract only (the full text was not tried). The page number is taken from the URL.

> Generally the volcanic cloud produces a diminution of zenith intensity during twilight with a considerable enhancement of intensity over the sky throughout the main part of the day.
> — `src4/coulson1983_optica_abstract.html`

What these show. The signs differ. After Raikoke (a modest load) the twilight sky was brighter. After El Chichon (a very heavy load over Mauna Loa) the ZENITH was dimmer in twilight. The abstract does not say at which solar depressions; I could not read the body. So the classical literature does not let you say "a volcanic layer brightens the zenith at 6.5 degrees" as a known fact. A thin layer brightening by scattering and a thick layer dimming by extinction is a reasonable reading, but that sentence is mine, not a quotation.

Not opened, known only from reference lists and search snippets: F. E. Volz and R. M. Goody 1962, J. Atmos. Sci. 19, 385 ("The Intensity of the Twilight and Upper Atmospheric Dust"); F. E. Volz 1969, Appl. Opt. 8, 2505 (Agung); F. E. Volz 1975, Science 189, 48 (Fuego); N. C. Shah 1969, Tellus 21, 636 ("Enhanced twilight glow caused by the volcanic eruption on Bali Island in March and September 1963"; photometric measurements at Ahmedabad, per a search snippet). These are listed in the reference list of the saved Shaw 1980 page (the three Volz papers) or came up in search; they are the place to look for zenith intensity curves after Agung.

---

## 4. Sky-brightness meters: has anyone seen an eruption, and is twilight used as a calibrator?

I found no paper, preprint or report that names the Hunga eruption (or any eruption) in SQM or TESS-W records. Searches run: the eruption name with "Sky Quality Meter", "SQM", "TESS photometer", "TESS-W", "night sky brightness", "light pollution trend", and with the names of southern observatories. That is an absence in my searches, not proof of absence.

### 4a. The nearest prior work: a southern SQM twilight series that runs through 2022 and 2023

P. Fiorentin, S. Cavazzani, A. Bertolo, S. Ortolani, R. Binotto, I. Saviane 2025, "SQM Ageing and Atmospheric Conditions: How Do They Affect the Long-Term Trend of Night Sky Brightness Measurements?", Sensors 25(2), 516, doi 10.3390/s25020516. Already saved: `src2/pmc_PMC11768471_sensors2025.html`, `.txt`. It includes an SQM at La Silla, Chile (about 29 S), with twilight readings from 2018 to early 2024.

> Figure 19 presents the plot of monthly average values of the sky brightness at twilight in the period from 2018 and the beginning of 2024. The straight horizontal blue line shows the result of a linear regression, performed just to try to highlight a long-term trend. The coefficients of the line are presented in Table 15, again, no apparent trend appears.
> — `src2/pmc_PMC11768471_sensors2025.txt`

> An anomaly seems to be present in the year 2022, when a strong variation in AOD appears, even if it does not correspond to a high variation in the SQM measurements.
> — `src2/pmc_PMC11768471_sensors2025.txt`

> while the sky brightness here considered is the average values at sunset and dawn, when the Sun is about at −6° below the horizon, AOD is always evaluated during the daytime
> — `src2/pmc_PMC11768471_sensors2025.txt`

> An increase in AOD, i.e., a less transparent atmosphere, heavily filters the Sun’s light measured by the SQM at twilight and brings to higher SQM magnitude values.
> — `src2/pmc_PMC11768471_sensors2025.txt`

> Unfortunately, the analysis of the long-term trend of the twilight measurements does not separate the effect of instrumental ageing from the influences of atmospheric changes.
> — `src2/pmc_PMC11768471_sensors2025.txt`

What it shows. This is the paper you must cite and reckon with. An SQM at 29 S, twilight at about -6 degrees, monthly means across 2022 and 2023: the authors see a seasonal wave, an AOD anomaly in 2022, and say the SQM twilight did not change much with it. The words "volcan", "Hunga" and "Tonga" do not occur in the saved text (machine count: 0). They relate a hazier atmosphere to a FAINTER twilight reading (larger magnitude), the opposite sign to yours.

Their Figures 18 and 19, which I then fetched and looked at (image addresses taken from the saved page; saved as `fiorentin2025_sensors-25-00516-g018.jpg` and `fiorentin2025_sensors-25-00516-g019.jpg`). Everything in this paragraph is read off the plots by eye, to about 0.02 magnitude, and none of it is said by the authors. The monthly twilight brightness at La Silla has a yearly wave of about 0.2 to 0.25 magnitude: faintest (about 14.05 to 14.11) in the second half of each year, brightest in about March to April. The yearly brightest points are about 13.83 (2019), 13.94 (2020), 13.84 (2021), 13.70 (2022), 13.77 (2023). The yearly faintest points are about 14.06 (2018), 14.07 (2019), 14.08 (2020), 14.11 (2021), 14.04 (2022); in 2023 the usual climb did not happen and the values stay near 13.91 to 13.93 through the middle of the year, reaching about 14.00 only at the very end. So in this published plot the twilight looks brighter in 2022 and 2023 than in 2019 to 2021 by roughly 0.05 to 0.15 magnitude, the same sign and about the same size as your result. Two things against leaning on it: the first months of the record (early 2018: 13.67, 13.73, 13.80) are as bright as early 2022, with no eruption to explain them; and the record stops at the start of 2024, so it cannot show a return. The aerosol optical depth in the same plot (satellite, daytime, total column) has its largest peak, about 0.10 against 0.05 to 0.07 in other years, in about September to October 2022.

### 4b. Twilight as calibrator

J. Puschnig, S. Naslund, A. Schwope, S. Wallner 2021, "Correcting sky-quality-meter measurements for ageing effects using twilight as calibrator", MNRAS, arXiv:2012.04042. Already saved: `src2/arxiv_2012.04042.pdf`, `_flow.txt`. Sites: Potsdam, Vienna, Stockholm (all northern).

> Hence, they are valid only for a limited range of solar zenith distances (z), i.e. 95–105◦ .
> — `src2/arxiv_2012.04042_flow.txt`

> However, the average magnitude of these discrepancies should be independent of time, as long as the average atmospheric composition has not changed significantly.
> — `src2/arxiv_2012.04042_flow.txt`

> Given the strong influence of atmospheric composition on NSB, we have checked large-scale atmospheric parameters (AOD, particulate matter, ozone) for existing trends that might cause the observed darkening.
> — `src2/arxiv_2012.04042_flow.txt`

What it shows. The method rests on the stated condition that the average atmospheric composition does not change. The paper does not mention volcanic or stratospheric aerosol at all (machine count of "volcan" in the saved text: 0; the only aerosol mentions are tropospheric AOD and particulate matter from reanalysis). So "a volcanic twilight would upset the twilight calibration by about the size of the effect" follows from their own condition, but nobody I found has said it in print; if you say it, it is your inference. The related paper Fiorentin et al. 2022 (Remote Sens. 14, 5787, "Long-Time Trends in Night Sky Brightness and Ageing of SQM Radiometers") is saved in `src2/` as `fiorentin2022_remotesensing_unipd.pdf`; I did not re-read it in this session.

### 4c. Eruptions in older night-sky-brightness records (not meters, but precedent)

K. Krisciunas 1997, "Optical Night-Sky Brightness at Mauna Kea over the Course of a Complete Sunspot Cycle", arXiv:astro-ph/9706111. Already saved: `src/krisciunas1997_arxiv_astro-ph9706111.txt`.

> The anomalous point of 1993, however, is probably due to ash from the Philippine volcano Mt. Pinatubo.
> — `src/krisciunas1997_arxiv_astro-ph9706111.txt`

H. Winkler, F. van Wyk, F. Marang 2014, "South African night sky brightness during high aerosol epochs", arXiv:1409.2996. Fetched: https://arxiv.org/pdf/1409.2996 . Saved: `arxiv_1409.2996.pdf`, `_flow.txt`. Moonlit night sky after Pinatubo, not twilight.

> In this paper we chose to investigate the sky characteristics soon after the Mount Pinatubo volcanic eruption in 1991
> — `src4/arxiv_1409.2996_flow.txt`

---

## 5. Other things in the southern stratosphere, 2019 to 2025, that could be mistaken for it or spoil the comparison years

### 5a. 2021 was not a clean year: Australian wildfire smoke was still decaying

K. Ohneiser et al. 2022, "Australian wildfire smoke in the stratosphere: the decay phase in 2020/2021 and impact on ozone depletion", Atmos. Chem. Phys. 22, 7417. Fetched: https://acp.copernicus.org/articles/22/7417/2022/acp-22-7417-2022.pdf . Saved: `ohneiser2022_acp-22-7417-2022.pdf`, `_flow.txt`. Lidars at Punta Arenas (53 S) and Rio Grande (53.8 S).

> These lidar measurements can be regarded as representative for mid to high latitudes in the Southern Hemisphere.
> — `src4/ohneiser2022_acp-22-7417-2022_flow.txt`

> A slow decay of the stratospheric perturbation detected by means of the 532 nm aerosol optical thickness (AOT) yielded an e-folding decay time of 19–20 months.
> — `src4/ohneiser2022_acp-22-7417-2022_flow.txt`

> above the stratospheric aerosol background of 0.005. After 2 months with strongly varying smoke conditions, the 532 nm AOT decreased to 0.03-0.06 from March–December 2020 and to 0.015–0.03 throughout 2021.
> — `src4/ohneiser2022_acp-22-7417-2022_flow.txt`

> The smoke layers extended, on average, from 9 to 24 km in height.
> — `src4/ohneiser2022_acp-22-7417-2022_flow.txt`

What it shows. At 53 S the stratospheric optical thickness through 2021 was still three to six times the background (0.015 to 0.03 against 0.005, at 532 nm). So 2021 is a low year only relative to 2022; it is not an undisturbed baseline. (Whether 30 to 40 S was as smoky as 53 S in 2021 I did not check.)

### 5b. La Soufriere, April 2021: mostly northern

Y. Li et al. 2023, "In situ measurements of perturbations to stratospheric aerosol and modeled ozone and radiative impacts following the 2021 La Soufriere eruption", Atmos. Chem. Phys. 23, 15351. Fetched: https://acp.copernicus.org/articles/23/15351/2023/acp-23-15351-2023.pdf . Saved: `li2023_acp-23-15351-2023.pdf`, `_flow.txt`.

> The resulting volcanic aerosol plumes dispersed predominately over the Northern Hemisphere (NH)
> — `src4/li2023_acp-23-15351-2023_flow.txt`

> The lower plume was also gradually transported toward the Southern Hemisphere (SH) but at a relatively slower pace.
> — `src4/li2023_acp-23-15351-2023_flow.txt`

### 5c. Ruang, April 2024: the southern stratosphere was loaded again from mid-2024

S. Khaykin et al. 2026, "Global transport of stratospheric aerosol produced by Ruang eruption from EarthCARE ATLID, limb-viewing satellites and ground-based lidar observations", Atmos. Chem. Phys. 26, 607. Fetched: https://acp.copernicus.org/articles/26/607/2026/acp-26-607-2026.pdf . Saved: `khaykin2026_acp-26-607-2026.pdf`, `_flow.txt`.

> The eruption timing in austral Fall and its high-altitude reach fostered efficient poleward transport into the southern extratropics during austral Winter 2024.
> — `src4/khaykin2026_acp-26-607-2026_flow.txt`

> By mid-June, the SAOD perturbation extended across the tropical belt and started propagating into the southern extratropics leading to enhanced SAOD throughout the southern hemisphere by October 2024, i.e. by the end of the Antarctic vortex season.
> — `src4/khaykin2026_acp-26-607-2026_flow.txt`

> doubling of the tropical SAOD and a factor of 1.8 increase of the southern extratropical SAOD for several months.
> — `src4/khaykin2026_acp-26-607-2026_flow.txt`

> At the southern midlatitudes, the Ruang aerosol layer has been observed since the beginning of ATLID observations, between 15–22 km altitude with the maximum intensity at ∼ 18.5 km (Fig. 4e).
> — `src4/khaykin2026_acp-26-607-2026_flow.txt`

> The 2024 Ruang eruption occurred during the late decay phase of the Hunga stratospheric aerosol perturbation (Khaykin et al., 2025).
> — `src4/khaykin2026_acp-26-607-2026_flow.txt`

> Since 2017, the significant SAOD perturbations, caused by either volcanic eruptions or wildfire outbreaks in both hemispheres, occurred at least once per year, maintaining the global stratospheric aerosol loading well above the background levels.
> — `src4/khaykin2026_acp-26-607-2026_flow.txt`

And from the APARC executive summary:

> The first significant post-Hunga SAOD perturbation, caused by the Ruang volcanic eruption in April 2024, ended the period of Hunga-driven stratospheric aerosol perturbation.
> — `src4/aparc_hunga_report_frontmatter_ntrs_20260001207_flow.txt`

What it shows. This is the awkward one for your result. From about June 2024 the southern extratropical SAOD was raised again by a factor of about 1.8 (the ATLID record starts mid-August 2024). If your 2024 twilights are as dark as 2021, then either your 2024 data are mostly from before the Ruang aerosol arrived, or the twilight brightening does not simply follow SAOD. The Ruang particles are reported much smaller than the Hunga ones (median radius 0.127 micron in the same paper, citing Dodangodage et al. 2025, against the Hunga effective radius of 0.4 micron) and the layer lower (15 to 22 km), which could matter, but no source says so for twilight; that link would be yours.

### 5d. Raikoke and Ulawun 2019

Named in Khaykin et al. 2026 among the three largest perturbations since 2000 together with Hunga and the Australian fires (sentence spans a figure caption in the saved text, so not block-quoted). Raikoke is northern (48 N); Ulawun is tropical. Both are before your record's comparison years; I did not pursue them.

### 5e. Solar cycle

No source searched. My own arithmetic, not a citation: at 14 magnitudes per square arcsecond the sky is about 1000 to 1600 times brighter than a natural night sky of 21.5 to 22, so airglow changes over the solar cycle (some tenths of a magnitude of the night sky; Krisciunas 1997 and Patat 2003 in `src/` are the usual references) move the reading by less than 0.001 magnitude. Also the solar maximum was later than 2022 to 2023, so airglow would have made 2024 the brightest year, not 2022.

---

## What I could not open or did not read

- Taha et al. 2022 on PubMed Central (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9786872/): a bot check came back; not worked around. The NASA NTRS manuscript of the same paper was used instead.
- Coulson 1983, Applied Optics: abstract page only; the full text was not tried. The solar depressions at which the zenith was dimmer are therefore unknown to me.
- A Nature 1982 note on a near-infrared twilight anomaly after El Chichon (https://www.nature.com/articles/300620a0.pdf): the fetch returned a web page, not the PDF; not read, not used.
- https://par.nsf.gov/servlets/purl/10585907 : "Not Found".
- Volz and Goody 1962; Volz 1969; Volz 1975; Shah 1969; Meinel and Meinel 1983 (book); Lee and Hernandez-Andres 2003 (purple light); Mateshvili et al. 2005 (Pinatubo twilights, J. Geophys. Res.): not fetched. Known only through the papers above that cite them.
- The published Remote Sensing version of Mukherjee et al. 2025: not fetched; the NTRS manuscript was used.
- The APARC report apart from the front matter and Chapter 3: not read.
- Search-result pages on Antarctic "afterglow" news (July 2022) were seen as snippets only and not saved; the NASA SAGE page quoted above covers the same reports.

Saved but not quoted (kept for your reference): `martinsson2025_acp-25-10677-2025.pdf`; `nsf_par_10561487.pdf` (Deshler et al. 2024, Geophys. Res. Lett., in situ aerosol size spectra in the austral polar vortex before and after Hunga); `noaa_csl_zhu_hunga_2026.pdf` (slides summarising the APARC report); `noaa_csl_news_2025_436_1218.html`.

---

## Things to be careful not to claim

1. Not "the first sign of Hunga in twilight". Twilight colour and near-infrared twilight brightness at Paranal (De Rosa et al. 2023), zenith twilight radiometry at Lauder (Mukherjee et al. 2025) and a zenith LED twilight photometer in Texas (Mims 2023) are in print. What I did not find is the eruption in SQM or TESS-W records, or a broadband zenith brightness at about 6.5 degrees depression. Say "I have not found", not "nobody has".
2. Do not pass over Fiorentin et al. 2025. Their La Silla SQM twilight series (Sun at about -6 degrees, 2018 to early 2024) is the closest published record, and they report no apparent trend and no large SQM change in 2022. Your result has to be set beside it. Their Figure 19, by my eye, shows 2022 and 2023 brighter by 0.05 to 0.15 magnitude, which agrees with you; but that is a reading of someone else's plot, the authors did not draw it, early 2018 in the same plot is just as bright, and a fifth southern site that agrees is not independent proof of the cause. If you use it, say "their published figure appears to show", give the reservations, and consider asking the authors.
3. Do not say the photometer sees sunlit aerosol overhead. At 6.5 degrees the geometric shadow overhead is near 41 km (35.1 km at 6 degrees in Patat et al.) and the effective shadow higher still (Ugolnikov and Maslov), while the bulk of the Hunga aerosol was always below 30 km and near 18 to 25 km at southern mid-latitudes. If the layer is the cause, the route is multiple scattering (as Mateshvili et al. model for 97 to 102 degrees after Pinatubo), and that is an explanation offered, not shown.
4. Do not say theory or precedent predicts a brighter zenith. Coulson (1983) reports a dimmer zenith in twilight after El Chichon; Fiorentin et al. (2025) relate more aerosol to a fainter SQM twilight; Mukherjee et al. model a brighter zenith at 94 degrees; Mateshvili et al. model a brighter sky at 97 to 102 degrees. The sign at 96.5 degrees in a broad visual band is not settled in what I read.
5. Do not call 2021 and 2024 undisturbed. 2021 still carried Australian smoke (three to six times background at 53 S) and some La Soufriere aerosol; from about June 2024 the Ruang aerosol raised southern extratropical SAOD by a factor of about 1.8. A dark 2024 despite Ruang needs a sentence.
6. Check 2023 against 2022. By the satellite record the southern loading peaked in mid-2022; the southern-hemisphere mean in 2023 ran at roughly half to two thirds of its mid-2022 peak (my reading of Figure 3.1c by eye, so rough), and the 30 to 45 S band had its strongest patch in May to September 2022. If your 2023 is as bright as or brighter than 2022, the simple story does not fit; the particle size (roughly constant, about 0.4 micron) and the descent of the layer are the only things in the literature that changed slowly.
7. Do not say the northern hemisphere had none. Thin layers reached northern mid-latitudes within three months, a small increase is seen at 44 N in late 2022, the larger-scale northern increase came in early 2023, and Mims reports the layer over 29.6 N from May 2022. "Too small for these photometers to show" is the defensible wording.
8. Do not give the layer height as 36 km or 40 km. Those are either the early upper fragments (above 36 km for two and a half months) or De Rosa's shadow-model heights. Bulk: 20 to 30 km at first, 23 to 27 km by mid-February 2022, extinction peak near 22 km (tropics), about 18 km over Lauder in November 2022.
9. Do not attribute the brightening to the water vapour. None of the sources read does; the water went up into the mesosphere from late 2022 while the aerosol sank. (That no source does it is my reading of the sources above, not a statement found in one.)
10. If you say that volcanic twilights would bias the twilight calibration of SQMs (Puschnig et al. 2021; Fiorentin et al. 2022, 2025), mark it as your inference from their stated assumption of an unchanged atmosphere. Neither saved paper mentions volcanic aerosol.
11. Dates of the visual reports are news dates (Australia January 2022; Botswana January to February 2022; New Zealand June 2022; Antarctica July 2022; Paranal still in early 2023). No source I read gives an end date for the vivid twilights.
