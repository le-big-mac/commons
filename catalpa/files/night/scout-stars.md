# Scout report: star time and the darkest part of the night in zenith photometer records

Searched and read 27 Nov 2026, 09:30 to 09:46 UTC. Every file named below is in `/home/agent1/night/lit/src2/`. Where only an arXiv number is given, the address fetched was `https://arxiv.org/pdf/` followed by that number. All 71 block quotations were checked by machine against the named saved file after the report was written (whitespace ignored); statements read from figures and page images were not, and are marked.

How to read this report

- Quotations are exact strings from the saved text files (whitespace and line breaks aside). Text extraction flattens superscripts: `arcsec2` is arcsec², `arcsec−2 yr−1` is "per square arcsecond per year", `40◦` is 40°. `[sic]` marks a word left as the extraction gave it (a hyphen lost at a line break, or the author's own spelling).
- `_flow.txt` files are PDF text in reading order; plain `.txt` beside a PDF is the same text with the page layout kept (used for tables).
- Sign convention trap: these papers measure in magnitudes, where a larger number is a darker sky. Authors differ on whether "NSB increases" means brighter or darker. I say which in each case where it matters.
- "As I read the figure" means I looked at the page image in the saved PDF; those statements are mine, not the authors' words.
- Journal references that I did not see printed in a saved file are marked "from memory, not verified".

---

## Question 1. Does the zenith brightness at dark sites follow the Milky Way (sidereal time), and by how much?

Yes, and it is plotted against sidereal time or right ascension in at least three places. Best sources first.

### 1.1 Plauchu-Frayn and six others 2017: a Sky Quality Meter plotted against sidereal time

I. Plauchu-Frayn, M. G. Richer, E. Colorado, J. Herrera, A. Córdova, U. Ceseña, F. Ávila, "Night sky brightness at San Pedro Martir Observatory", preprint arXiv:1609.00423 (headed "Accepted to Publications of the Astronomical Society of the Pacific"; volume and page from memory, not verified: PASP 129, 035003, 2017). Fetched https://arxiv.org/pdf/1609.00423. Saved `arxiv_1609.00423.pdf`, `arxiv_1609.00423_flow.txt`, `arxiv_1609.00423.txt`. Site: Sierra San Pedro Mártir, Baja California, latitude +31°; one SQM read daily over twenty months, 2014 to 2016.

Section 3.2, "SQM results":

> "In Fig. 5 we show the NSB distribution as a function of Sidereal time before filtering for Galactic latitude or correcting for the zodiacal light contribution. At the latitude of OAN-SPM (+31◦ ), the galactic plane lies near Sidereal time 90◦ and 300◦ , where it can be seen that the NSB is brighter (i.e., lower values), with a contribution to the sky brightness of about 45% inside the field of view of the SQM due to the galactic plane." [file: arxiv_1609.00423_flow.txt]

Caption of its Figure 5 (preprint page 5):

> "Fig. 5.— Distribution of the raw SQM measurements as a function of sidereal time (ST) for clear moonless nights." [file: arxiv_1609.00423_flow.txt]

Section 3.2, first paragraph, the range on clear nights (the sentence begins on the previous page with "The sky brightness on clear nights ranges"):

> "from the brightest value of 13 magSQM arcsec−2 (Full Moon at 30◦ from zenith), to 21.3 magSQM arcsec−2 (Galactic plane at the zenith), to the darkest value of 22 magSQM arcsec−2 on a moonless night." [file: arxiv_1609.00423_flow.txt]

What it shows: the plot you would draw. As I read Figure 5: two bright dips near sidereal time 90° and 300° (about 21.3 to 21.4) and a dark hump near 200° (about 21.7), so roughly 0.4 mag between Milky Way overhead and away. Its Figure 7 then shows the same data, filtered to Galactic latitude above 20° and corrected for zodiacal light, flat against UT. The paper does not go on to say when in the night the minimum falls or how that moves through the year.

### 1.2 Alarcon, Serra-Ricart, Lemes-Perera and Mallorquín 2021: TESS photometers, 44 dark sites

"Natural Night Sky Brightness during Solar Minimum", preprint arXiv:2105.01066 (draft dated June 25, 2021; Astronomical Journal 162, 25 per the search listing, DOI 10.3847/1538-3881/abfdaa). Fetched https://arxiv.org/pdf/2105.01066. Saved `arxiv_2105.01066.pdf`, `arxiv_2105.01066_flow.txt`, `arxiv_2105.01066.txt`.

Section 3.2.3, "Galaxy" (size of the effect):

> "In the region close to the Galactic center (blue line) the zenith sky brightness can increase by up to 1 mag/arcsec2 , while the average elsewhere in the Galactic plane reaches about 0.4 mag/arcsec2 ." [file: arxiv_2105.01066_flow.txt]

> "Therefore, in this work it will be considered that measurements are unaffected by Galactic light when the absolute value of the Galactic latitude at zenith is greater than 40◦ ." [file: arxiv_2105.01066_flow.txt]

End of section 4, with Figure 8 (preprint pages 10 to 11), the nearest thing in print to your sentence about the darkest part moving through the night:

> "For a given location, there are nights of the year when zenithal brightness measurements are inevitably influenced by the different astronomical components. Figure 8 shows the difference in sky brightness for different positions (α, δ) in the sky. Since the zenith decl. is the same as the geographical latitude of the site, each device completes a horizontal line throughout the year." [file: arxiv_2105.01066_flow.txt]

> "On the upper axis, the months have been placed as a reference, taking for this purpose the R.A. of the zenith in the middle of the night, i.e., the sidereal time when the Sun is at lower culmination. It is noted that the best time to measure the zenithal natural NSB is during local spring, as the available time is longer. In the earlier months, measurements can be taken at the end of the night (higher R.A.) while the opposite applies in the later months." [file: arxiv_2105.01066_flow.txt]

> "Furthermore, around the solstices the Galaxy will be present, especially in the southern winter, where the Galactic center will be very high at midnight." [file: arxiv_2105.01066_flow.txt]

Conclusions:

> "– Galactic light can increase the NSB if it is measured at an absolute latitude less than 40◦ and approximately homogeneously for all longitudes." [file: arxiv_2105.01066_flow.txt]

What it shows: Figure 4 plots brightness difference against Galactic latitude of the zenith; Figure 8 plots it on the sky by right ascension (which for a zenith instrument is the local sidereal time) and declination, with months on the top axis. As I read Figure 8, the colour scale runs from 0 to −1.0 mag/arcsec² and the northern band of stations (declination roughly +20° to +55°) reaches roughly −0.4 to −0.6 where the Galactic equator crosses, near R.A. 5 to 6 h and 20 to 21 h. The sentence "at the end of the night ... while the opposite applies in the later months" states the seasonal migration of the Galaxy-free hours in words. It is said as advice on when to measure, not as a result about when the sky is darkest, and nothing is said about towns (the paper is about dark sites only).

### 1.3 Grauer and Grauer 2021: brightness against right ascension, then the remainder against clock time

Albert D. Grauer and Patricia A. Grauer, "Linking Solar Minimum, Space Weather, and Night Sky Brightness", preprint arXiv:2112.01664 dated October 19, 2021 (Scientific Reports, December 2021, DOI 10.1038/s41598-021-02365-1 per the search listing; volume and article number from memory, not verified: 11, 23893). Fetched https://arxiv.org/pdf/2112.01664. Saved `arxiv_2112.01664.pdf`, `arxiv_2112.01664_flow.txt`, `arxiv_2112.01664.txt`. Five sites: two SQMs (Cosmic Campground, New Mexico, "CCIDSS"; Mt. Lemmon above Tucson, "CSSMLS") and three TESS-W photometers of the STARS4ALL network (stars18, stars62, stars211), September 2018 to April 2020. Note the extraction garbles the paper's symbol ΔM(t) as "ΔM(t),M(t)"; I have not quoted sentences containing it.

Methods (preprint pages 5 to 6):

> "A Chi Squared of less than 0.009 for at least 1.5 hours rejects suspect data but not the rising Milky Way." [file: arxiv_2112.01664_flow.txt]

> "Our software calculates the Right Ascension (R.A.), Declination (Dec.) ,Julian Date(JD) , Local Sidereal Time (LST), Solar and Lunar Altitudes and other parameters for each M(t) data point." [file: arxiv_2112.01664_flow.txt]

> "A total of 12,892, M(t), time-series data points, sorted into ½ h bins in R.A., obtained at CCIDSS September 2018 through April 2020 are plotted in Fig. 1." [file: arxiv_2112.01664_flow.txt]

> "This fitted M(t) versus RA light curve is the background contribution from celestial sources and the broadband night airglow when it is at minimum." [file: arxiv_2112.01664_flow.txt]

> "Each site has a unique light curve of quiescent broadband airglow brightness which depends on its latitude and the degree to which it is influenced by anthropogenic light." [file: arxiv_2112.01664_flow.txt]

On a record dark night (7 to 8 February 2019):

> "In the direction away from the disk of the Milky Way (LST 11-14 h) the measured sky brightnesses were: CCIDSS (22.128 mag/arcsec² , stdev = 0.016), CSSMLS (21.456 mag/arcsec² , stdev = 0.009), and Stars 211 (21.469 mag/arcsec² , stdev = 0.038)." [file: arxiv_2112.01664_flow.txt]

On what is left after the right-ascension curve is subtracted, plotted against hours from local midnight (their Fig. 2). The sentence about the site above Tucson begins "At CSSMLS," then the garbled symbol, then:

> "is correlated with automobile driving patterns and scheduled outdoor lighting changes in and around Tucson, AZ." [file: arxiv_2112.01664_flow.txt]

What it shows: Figure 1 is a Sky Quality Meter's zenith brightness against right ascension at a site with no measurable artificial light, with "Galactic Plane" marked at two places. As I read Figure 1, the fitted lower envelope runs from about 21.6 at the two plane crossings (R.A. near 20 h and 6 h) to about 22.2 near R.A. 11 to 12 h: a swing of about 0.5 to 0.6 mag. Figure 2 then shows the residual against clock time: nearly flat at the dark site, and at the Tucson-affected site falling steadily from dusk to a minimum about two to three hours after local midnight (as I read it). So the two halves of your finding, a star-time part and a clock-time part that belongs to town lights, are both here, as steps in a data reduction. The paper does not present them as a finding about when the night is darkest. The same authors' earlier paper (with N. Davies and G. Davies, "Impact of Space Weather on the Natural Night Sky", PASP 2019) I could not open at the journal; its abstract, as reproduced on the instrument maker's forum (https://unihedron.com/forum/index.php?topic=77.0, saved `unihedron_forum_topic77.html` and `.txt`), has:

> "used as single-channel differential photometers, to scan the sky as Earth rotates on its axis" [file: unihedron_forum_topic77.txt]

> "the modulations of the light curves (brightness versus R.A.)" [file: unihedron_forum_topic77.txt]

### 1.4 Masana, Carrasco, Bará and Ribas 2021: the pattern as a model, drawn month by hour

"A multi-band map of the natural night sky brightness including Gaia and Hipparcos integrated starlight", preprint arXiv:2101.01500 (6 January 2021; MNRAS, volume and page from memory, not verified: 501, 5443). Fetched https://arxiv.org/pdf/2101.01500. Saved `arxiv_2101.01500.pdf`, `arxiv_2101.01500_flow.txt`, `arxiv_2101.01500.txt`.

Section 8.3, "Seasonal variation of the zenith sky brightness" (preprint pages 12 to 13):

> "According to our model, for zenith measurements, the natural variation of the night sky brightness along the year due to the variation of the astrophysical contributions can reach more than 0.6 magnitudes." [file: arxiv_2101.01500_flow.txt]

> "The figure plots only the times when the height of the Sun above the horizon is < −18°. The presence of the Milky Way in two different epochs of the year is clearly visible." [file: arxiv_2101.01500_flow.txt]

> "But even for relatively large fields of view of tens of degrees, the variation of the natural night sky brightness is up to several tenths of magV arcsec−2 ." [file: arxiv_2101.01500_flow.txt]

What it shows: its Figure 12 (page 13) is a grid of month across and hour (UT, 18 to 6) down, coloured by modelled zenith brightness from 20.6 to 22.0 mag/arcsec² in V, for latitude 40° and 1000 m. As I read the small figure, the bright bands run diagonally (arriving earlier in the night as the months go on) and the darkest cells are in spring. This is your star-time pattern as a prediction, for a 10° circle at the zenith; an SQM or TESS-W sees a wider cone, so its swing should be smaller than 0.6 (the authors' "several tenths").

### 1.5 Deverchère and others 2022: fixed photometers in France and Chile

P. Deverchère, S. Vauclair, G. Bosch and others, "Towards an absolute light pollution indicator", Scientific Reports 12, 17050 (2022), open access. Fetched https://www.nature.com/articles/s41598-022-21460-5. Saved `deverchere2022_s41598-022-21460-5.html` and `.txt`. Instruments are the authors' own SQM-based "Ninox" stations.

> "First, the Milky Way is absent from zenith in the middle of the night during spring and then becomes progressively more present during summer, resulting in lower NSB values." [file: deverchere2022_s41598-022-21460-5.txt]

> "If we ignore the sunset and sunrise on both sides of the diagram, the large range of NSB variations one can observe is due to natural light sources such as the Galactic plane that creates characteristic wavelike patterns when passing through the zenith." [file: deverchere2022_s41598-022-21460-5.txt]

> "This corresponds to an increase of brightness of more than one magnitude which is by far the largest brightness variation one can get from a natural source in the night sky beside the Moon or an aurora" [file: deverchere2022_s41598-022-21460-5.txt]

What it shows: at a site in the Atacama the Galactic plane at the zenith reads 20.9 to 21.6 against a best clear value of 22.05 (their figures, in the sentence before the last quotation; "lower NSB" here means brighter). The first quotation is about a station in the small town of Gresse-en-Vercors, France, where by the paper's account most public lighting is turned off at 23:00 UTC; it describes the middle of the night, not when the night is darkest. They also list both mechanisms side by side as nuisances for a single reading:

> "time of the night which is linked to human activity hence the quantity of light emitted into the nocturnal environment, presence of the Milky Way at the zenith, atmospheric conditions including aerosol load and humidity level" [file: deverchere2022_s41598-022-21460-5.txt]

### 1.6 Oregon Skyglow Measurement Network, Technical Report Edition #7 (2023): the dark-site and town contrast, stated

A volunteer network's report, not a journal paper. Its title page reads, on four lines, "Oregon Skyglow Measurement Network", "Technical Report Edition #7", "Data from April 2019 to November 2022", "March 6, 2023"; it is a project of the Oregon Chapter of the International Dark-Sky Association (project contact named in it: Bill Kowalik). The copy I found is one filed as public testimony with the Oregon legislature: https://apps.oregonlegislature.gov/liz/2023R1/Downloads/PublicTestimonyDocument/88792. Saved `oregon_testimony_88792.pdf` and `oregon_testimony_88792_flow.txt`. 44 SQMs, five-minute cadence.

On its Figure 3 (page 6), six sites on the single night of 1 to 2 August 2019:

> "Figure 3 shows that the sky overhead at the four dark sites brightens as the Milky Way rises directly overhead, and then darkens as the Milky Way begins descending through the early morning hours. The effect of the Milky Way brightening in the data for the two sites under the City of Bend light dome (Awbrey Butte and Hopservatory), is not obvious because the Milky Way is washed out by the lightpolluted [sic] skies at those two sites. Instead, we see a gradual darkening through the night hours, which we presume is due to some outdoor lights in the City, being dimmed or turned off, and fewer car headlights as most people are sleeping." [file: oregon_testimony_88792_flow.txt]

On its Figure 6, monthly means at four dark sites:

> "Figure 6 shows that, prior to any adjustment for the galactic position and time of night (the brown dots and lines), the skyglow data for these dark sky sites show a dramatic seasonal pattern of darker in springtime (March-April-May) and brighter in late autumn and early winter (Oct-Nov-Dec). This pattern is consistent with the fact that the portion of the Milky Way crossing the zenith in March is in Auriga, which is significantly darker than the portion of the Milky Way crossing zenith in November in much brighter Cygnus." [file: oregon_testimony_88792_flow.txt]

> "As we might expect, the adjustment for galactic position has little impact on the seasonal pattern of the light-polluted sites – after all, the Milky Way is largely invisible due to the light pollution at those locations." [file: oregon_testimony_88792_flow.txt]

What it shows: this is the only place I found where the contrast you describe (dark sites follow the Milky Way, town sites darken with the clock) is stated outright. It rests on one night's figure and on monthly averages; the report then removes both effects (it shifts all data to a fixed Galactic latitude and to 1 AM) to look for long-term trends. As I read Figure 3, the figure itself is annotated "Milky Way Directly Overhead 1:19AM", and the dark-site curves are darkest soon after evening twilight, brightest near that time, and darker again toward morning.

### 1.7 The instrument maker's FAQ

Unihedron, "SQM FAQ", https://www.unihedron.com/projects/darksky/faq.php. Saved `unihedron_faq.html` and `unihedron_faq.txt`.

> "The northern Milky Way contributes about 0.10 mpsas under 21.5 mpsas (moonless) skies." [file: unihedron_faq.txt]

> "The southern Milky Way might be as big an effect as 0.85 mpsas where it goes near-overhead." [file: unihedron_faq.txt]

("mpsas" is magnitudes per square arcsecond.) A comment in the page source beside the second figure reads:

> "was 0.30, but Andrew Cool reports 0.85 on 20190506" [file: unihedron_faq.html]

What it shows: the maker acknowledges the effect, but its 0.10 for the northern Milky Way is several times smaller than what the dark-site records above show (about 0.4 to 0.6). Do not use the FAQ figure as the size.

### 1.8 Shorter mentions

**Posch, Binder and Puschnig 2018**, "Systematic measurements of the night sky brightness at 26 locations in Eastern Austria", arXiv:1803.09811 (https://arxiv.org/pdf/1803.09811; saved `arxiv_1803.09811.pdf`, `_flow.txt`, `.txt`). Only a parenthesis in the caption of its Table 2, on clear moonless values:

> "(col. 3; these values may vary by ± 0.2 mag/arcsec2 depending on the season, visibility of the Milky Way etc.)" [file: arxiv_1803.09811.txt]

and, on the "jellyfish" plots (brightness against hour, all nights overlaid), section 4.4:

> "For natural conditions, the diagrams should be very close to axially symmetrical with respect a vertical line at local midnight." [file: arxiv_1803.09811_flow.txt]

I found no plot against sidereal time in it, and no sentence about the Milky Way moving the minimum. Its seasonal section is about cloud, snow and aerosols.

**Puschnig, Wallner, Schwope and Näslund 2022** (preprint; MNRAS 518, 4449, 2023 per the search listing), "Long-term trends of light pollution assessed from SQM measurements and an empirical atmospheric model", arXiv:2210.09177 (https://arxiv.org/pdf/2210.09177; saved `arxiv_2210.09177.pdf`, `_flow.txt`, `.txt`). A model figure for the natural yearly swing, and a different explanation of the seasonal scatter at their rural station:

> "Note that – given our model constraints – the SKYCALC sky models lead to yearly peak and valley zenithal NSBs (due to changing starlight+zodiacal light) of 21.63 and 21.87 magSQM arcsec−2 for our sites." [file: arxiv_2210.09177_flow.txt]

> "At rural sites such as e.g. BOD, the scatter is dominated by a seasonal variation, caused by variations of albedo (e.g. enhancing NSB during winters due to snow cover) and vegetation" [file: arxiv_2210.09177_flow.txt]

**Puschnig, Wallner and Posch 2020**, "Circalunar variations of the night sky brightness – an FFT perspective on the impact of light pollution", arXiv:1912.05673 (saved `arxiv_1912.05673.pdf`, `_flow.txt`, `.txt`). Searched by keyword for a sidereal-day period among its frequencies; found none. The only hit is that its lunar model leaves out stars and the Milky Way. It works on nightly means, which cannot show a within-night pattern.

**Shah, Peletier and others 2025**, "Beyond the Clouds: Advanced Data Analysis of a Dutch Sky Quality Meter Network", preprint arXiv:2507.11343v2, 17 July 2025 (headed for MNRAS but "Accepted XXX": treat as unrefereed). Fetched https://arxiv.org/pdf/2507.11343. Saved `arxiv_2507.11343.pdf`, `_flow.txt`, `.txt`. Section 3.1.2, "Seasonal trend (effect of the Milky Way)":

> "An important yet overlooked factor in NSB variability is the contribution of natural celestial sources, particularly the Milky Way." [file: arxiv_2507.11343_flow.txt]

> "This method is only useful in extremely dark sites where the Milky Way or galactic core significantly impacts the sky brightness, which is why these three locations were chosen for this analysis." [file: arxiv_2507.11343_flow.txt]

> "Nevertheless, in all three locations, visually there seems to be a gradual increase of darkness of 0.5 magnitudes from Winter to Spring and subsequent drop. Since our data cleaning steps already filtered out data with clouds and the Moon, we attribute this seasonal fluctuation to the geometric position and seasonal visibility of the Milky Way." [file: arxiv_2507.11343_flow.txt]

It fits a one-year sine to monthly values (amplitude 0.191 at Borkum-Ostland, from its Figure 11 caption) and calls the factor "overlooked", which tells you how the authors of a 2025 network paper see the state of the literature. It does not use sidereal time.

**Bertolo, Binotto, Ortolani and Sapienza 2019**, "Measurements of Night Sky Brightness in the Veneto Region of Italy: Sky Quality Meter Network Results and Differential Photometry by Digital Single Lens Reflex", J. Imaging 5, 56. Fetched a copy at https://cielobuio.org/wp-content/uploads/jimaging-05-00056.pdf. Saved `bertolo2019_jimaging-05-00056.pdf` and `_flow.txt`. The text extraction of this file prints every line twice with different breaks, so the following is read from the page image (page 7 of 13) and is not machine-checked: "In the winter months, there was an NSB minimum (more clear in Passo Valles), likely due to the Milky Way and snow cover of the ground [9]. The Milky Way disappears in spring when Monte Baldo and Passo Valles have both a maximum value of NSB." ("Minimum" here means brightest.) Same page, Table 4: on the night of 14 to 15 February 2018 the darkest site, Passo Valles, darkened fastest between 21:00 and 01:00 (0.148 mag/hour against 0.053 at Padova), which the authors put down to traffic and lighting, not to the winter Milky Way leaving the zenith.

**Bará, Lima and Zamorano 2019**, "Monitoring Long-Term Trends in the Anthropogenic Night Sky Brightness", Sustainability 11, 3070 (volume and number from the publisher's address). The publisher's PDF refused my client (HTTP 403); I used the University of Coimbra repository copy, https://estudogeral.sib.uc.pt/bitstream/10316/107395/1/Monitoring-longterm-trends-in-the-anthropogenic-night-sky-brightnessSustainability-Switzerland.pdf. Saved `bara2019_sustainability_coimbra.pdf` and `_flow.txt`. Section 2.2, both mechanisms in one sentence:

> "At ultradian time scales, the zenithal NSB varies due to the time course of the artificial light emissions throughout the night [41–43] and the varying zenithal distance of celestial objects, including the Milky Way." [file: bara2019_sustainability_coimbra_flow.txt]

> "Seasonal variations are also associated with the different celestial bodies present in the upper hemisphere." [file: bara2019_sustainability_coimbra_flow.txt]

**Bará 2016**, "Anthropogenic disruption of the night sky darkness in urban and rural areas", R. Soc. Open Sci. 3(10), 160541 (the densitogram paper). Publisher refused (403); used the PubMed Central copy, https://pmc.ncbi.nlm.nih.gov/articles/PMC5098997/. Saved `pmc_PMC5098997_bara2016.html` and `.txt`. It expects the effect and does not measure it:

> "natural celestial sources, among them the Milky Way, are located at different positions in the sky depending on the local time and the date of the year, and they will contribute in a variable amout [sic] to the recorded measurements." [file: pmc_PMC5098997_bara2016.txt]

**Hänel and thirteen others 2018**, "Measuring night sky brightness: methods and challenges", arXiv:1709.09558 (saved `arxiv_1709.09558.pdf`, `_flow.txt`, `.txt`). By keyword I found nothing in it on the Milky Way in zenith SQM readings; the nearest is that space measurements run "22.1–23.3 magV /arcsec2 , depending on the galactic latitude". Useful only for Question 4.

**Jechow and four others 2016**, "Evaluating the summer night sky brightness at a research field site on Lake Stechlin in northeastern Germany", arXiv:1602.04537 (saved `arxiv_1602.04537.pdf`, `_flow.txt`, `.txt`): one night's camera images, where they

> "clearly show that the NSB at the zenith is dominated by the Milky Way" [file: arxiv_1602.04537_flow.txt]

### Sizes, gathered

| Source | Where, what | Milky Way overhead versus away |
|---|---|---|
| Plauchu-Frayn 2017 | SQM, latitude +31° | 21.3 against 22 (text); about 0.4 between the dips and the hump of Fig. 5 as I read it |
| Alarcon 2021 | TESS, many sites | "about 0.4" in the plane; "up to 1" near the Galactic centre |
| Grauer and Grauer 2021 | SQM, latitude +33° | about 0.5 to 0.6 along the lower envelope of Fig. 1, as I read it |
| Deverchère 2022 | Atacama | "more than one magnitude" (Galactic centre region) |
| Masana 2021 (model) | 40° N, 10° circle, V band | "more than 0.6" over the year, zodiacal light included |
| Puschnig 2022 (model) | 50° to 60° N | 0.24 peak to valley over the year |
| Shah 2025 preprint | Wadden coast, about 53° N | about 0.5 "from Winter to Spring", sine amplitude 0.191 |
| Posch 2018 | Upper Austria | "± 0.2" for season and Milky Way together |
| Unihedron FAQ | maker | 0.10 north, up to 0.85 south |

---

## Question 2. Is it said WHEN in the night a dark site is darkest, and does anyone tie this to the proverb?

When: said in pieces, never as a headline result.

- Alarcon 2021 (quoted in 1.2): the Galaxy-free hours are "at the end of the night" in the earlier months "while the opposite applies in the later months", and spring is best. This is the closest sentence to yours.
- Grauer and Grauer 2021 (quoted in 1.3): darkest "In the direction away from the disk of the Milky Way (LST 11-14 h)". They also report something about the end of the night at their dark site that they cannot explain:

> "On long winter nights, before the onset of astronomical twilight, there does seem to be an increase of approximately 0.07 mag/arcsec2 . The origin of this increase is unclear. There appear to be other reports of this phenomena in the literature.38" [file: arxiv_2112.01664_flow.txt]

  This is in the residual after the right-ascension curve is taken out, so it is not the Milky Way. As I read their Fig. 2 it is a brightening before dawn (the plotted excess grows). Their reference 38 is Chamberlain's 1961 book on aurora and airglow.
- Deverchère 2022 (quoted in 1.5): the Milky Way is "absent from zenith in the middle of the night during spring".
- Oregon report (quoted in 1.6): on an August night the dark sites brighten toward 1:19 AM and darken again; over the year they are darkest in March to May.
- Masana 2021 Fig. 12 draws the whole pattern (month by hour) from a model.
- Plauchu-Frayn 2017, once the Milky Way and zodiacal light are filtered out: "there is no clear trend in NSB after twilight" (quoted in the earlier report `scout.md`, section 2(b), from the same preprint).

The proverb: none of the sources above mentions it. One search for the proverb together with sky-brightness measurement, Milky Way and sidereal terms returned only general explainers (the Weizmann Institute piece already in `scout.md` among them), none connecting the saying to the Milky Way's position. I found no published link between the star-time pattern and "the darkest hour is just before the dawn".

---

## Question 3. Do the zodiacal light or the gegenschein matter for zenith readings near the ends of the night?

The dark-site papers say yes at low latitudes and treat it as something to remove; the maker's FAQ says no; a model puts it at about a quarter of the natural zenith light at 40° N averaged over the year.

**Alarcon 2021** (file as in 1.2). Section 3.2.4 and conclusions; they also drop the first four hours of each night before fitting their zodiacal filter:

> "The sudden increase in brightness from 165◦ onward should be noted; this is indicative of the detection of the Gegenschein with the TESS photometers." [file: arxiv_2105.01066_flow.txt]

> "– The heliocentric longitude has to be taken into account in dealing with zodiacal light, and the possibility of detecting the Gegenschein with broadband photometers has been demonstrated for the first time." [file: arxiv_2105.01066_flow.txt]

Section 5.1, the after-dusk trend when zodiacal light is left in (magnitudes per hour, getting darker):

> "Note that although the former shows, as expected, a higher brightening than the latter, both have similar trends of 0.019 ± 0.002 and 0.017 ± 0.003 mTESS /hr, which are also compatible with those reported by Krisciunas (1997) and Patat (2003)." [file: arxiv_2105.01066_flow.txt]

**Masana 2021** (file as in 1.4). Its Table 4, "Mean contributions to zenith natural night sky brightness for a latitude equal to 40° N" (V band, yearly mean, model), gives airglow 165 nW m−2 sr−1 (47.7 %), zodiacal light 95 (27.5 %), integrated starlight 75 (21.7 %). The zodiacal row as extracted:

> "Zodiacal Light 95 27.5" [file: arxiv_2101.01500.txt]

> "Zodiacal light has a larger impact in locations close to the Equator when we observe near the zenith, as the plane of the ecliptic reaches greater heights above the horizon at these latitudes." [file: arxiv_2101.01500_flow.txt]

**Plauchu-Frayn 2017** (file as in 1.1), section 3.2; its Table 1 gives the mean zodiacal correction for the SQM as 0.26 mag (read from the page image, page 5):

> "The contribution of zodiacal light is almost constant for a given value of | β | for | λ − λ⊙ | >110◦, but it varies from 0.2 to 0.4 mag from | β | = 0◦ to | β | = 55◦ ." [file: arxiv_1609.00423_flow.txt]

**Deverchère 2022** (file as in 1.5), Atacama:

> "The contribution of the zodiacal light to the zenithal night sky brightness is much lower than the contribution of the Galactic plane. Even in Atacama where the ecliptic passes near the zenith, it is quite difficult to notice a seasonal effect of zodiacal light on the zenithal NSB." [file: deverchere2022_s41598-022-21460-5.txt]

> "This tends to show that the zodiacal light increases the zenithal NSB by 0.1 mag" [file: deverchere2022_s41598-022-21460-5.txt]

("increases the zenithal NSB" there means brighter by 0.1.)

**Puschnig 2022** (file as in 1.8), for latitudes 50° to 60°:

> "Thus the contribution of zodiacal light to the zenithal NSB becomes lower at our sites (Masana et al. 2020, see Figure 10), further reducing the overall yearly zenithal NSB variation." [file: arxiv_2210.09177_flow.txt]

**Unihedron FAQ** (file as in 1.7):

> "It is likely to be less than a 1 or 2 percent effect. The primary reason is that the brightest and widest part of the zodiacal light is nearest the horizon where the SQM has almost no sensitivity (due to it being a zenith-looking device)." [file: unihedron_faq.txt]

What this adds up to: the sources disagree by a factor of ten or more. At latitude 30° the working astronomers correct an SQM by about a quarter of a magnitude; at 40° a model gives about a quarter of the zenith light on average; at 50° to 60° it is said to be smaller, with no figure. Nobody I read gives a measured zenith figure for the ends of the night at 40° to 50°. The gegenschein has been detected in TESS zenith data (Alarcon); it sits opposite the Sun, so it can only cross the zenith near midnight and only where the ecliptic passes overhead (my inference, not a quotation).

---

## Question 4. Do these photometers read darker year by year because they age, and how fast?

Yes for the Sky Quality Meter in its weatherproof housing: several independent estimates, mostly 0.02 to 0.06 magnitude per year. For the TESS-W I found no published rate, and the one paper that looked reports no evidence of it.

| Source | Method | Rate (darker per year) |
|---|---|---|
| Puschnig and others 2021 | twilight as calibrator, 3 city SQMs | 0.034, 0.046, 0.053 |
| Bará and others 2021 | side-by-side with unexposed units, 5 SQMs | about 0.06 (0.062 ± 0.004) |
| Puschnig and others 2022 | twilight, 26 SQMs | mean 0.031 ± 0.020; range zero to about 0.075 |
| Fiorentin and others 2022 | twilight, Veneto and La Silla | 0.029 ± 0.005 to 0.086 ± 0.022 |
| Fiorentin and others 2025 | two aged SQMs measured in the laboratory | about 0.010 and under 0.040 (against 0.053 and 0.086 by twilight at the same two sites) |
| Oregon report 2023 | new units beside old ones | 0.019 |
| Pun and others 2014 | Hong Kong, housing window | window loss levelled at about 0.25 (polycarbonate) and 0.10 (glass) after about a year |
| Alarcon and others 2021 | TESS photometers | "we do not observe evidence of this behavior" |

**Puschnig, Näslund, Schwope and Wallner 2021**, "Correcting Sky Quality Meter measurements for aging effects using twilight as calibrator", arXiv:2012.04042 (MNRAS 502, 1095 per the search listing). Fetched https://arxiv.org/pdf/2012.04042. Saved `arxiv_2012.04042.pdf`, `_flow.txt`, `.txt`. Abstract:

> "Twilight SQM observations, calibrated for changing sun altitudes, reveal a linear degradation of the measurement systems (SQM + housing window) with the following slopes: 34±4, 46±2 and 53±2 milli-magSQM arcsec−2 yr−1 for Stockholm, Potsdam-Babelsberg and Vienna." [file: arxiv_2012.04042_flow.txt]

**Bará, Marco, Ribas, Garcia Gil, Sánchez de Miguel and Zamorano 2021**, "Direct assessment of the sensitivity drift of SQM sensors installed outdoors", International Journal of Sustainable Lighting (2021) 1-6 as headed on the preprint, arXiv:2011.15044. Fetched https://arxiv.org/pdf/2011.15044. Saved `arxiv_2011.15044.pdf`, `_flow.txt`, `.txt`. Abstract, then Results:

> "Our preliminary results suggest that SQM detectors installed outdoors steadily increase (darken) their readings at an average rate of +0.036 magSQM/arcsec2 per MWh/m2 of exposure to solar horizontal global irradiation, that for our locations at mid latitudes (39º-43º N) in temperate climate zones translates into approximately +0.06 magSQM/arcsec2 per year." [file: arxiv_2011.15044_flow.txt]

> "Expressed in terms of elapsed time, this amounts to +0.062 (±0.004) magSQM/arcsec2 per year." [file: arxiv_2011.15044_flow.txt]

**Puschnig, Wallner, Schwope and Näslund 2022** (file as in 1.8), section 3.2:

> "We find a relatively large variation between individual SQM sites with aging slopes ranging from zero to ∼-0.075 magSQM arcsec−2 yr−1 . On average, the aging effect leads to a darkening of ∼-0.031±0.020 magSQM arcsec−2 yr−1 ." [file: arxiv_2210.09177_flow.txt]

**Fiorentin, Binotto, Cavazzani, Bertolo, Ortolani and Saviane 2022**, "Long-Time Trends in Night Sky Brightness and Ageing of SQM Radiometers", Remote Sensing 14, 5787. Fetched the University of Padua repository copy, https://www.research.unipd.it/retrieve/(identifier left out)/remotesensing-14-05787.pdf. Saved `fiorentin2022_remotesensing_unipd.pdf` and `_flow.txt`. Abstract:

> "The slope of the observed long-term trends ranges between 29 ± 5 and 86 ± 22 mmagSQM arcsec−2 year−1 ." [file: fiorentin2022_remotesensing_unipd_flow.txt]

**Fiorentin, Cavazzani, Bertolo, Ortolani, Binotto and Saviane 2025**, "SQM Ageing and Atmospheric Conditions: How Do They Affect the Long-Term Trend of Night Sky Brightness Measurements?", Sensors 25(2), 516. Fetched https://pmc.ncbi.nlm.nih.gov/articles/PMC11768471/. Saved `pmc_PMC11768471_sensors2025.html` and `.txt`. Conclusions: the twilight method overstates instrument ageing, part of the trend being cleaner air:

> "the loss of output was about 10 mmagSQM arcsec−2 year−1 for the SQM of the Padova station and less than 40 mmagSQM arcsec−2 year−1 for the SQM at Pennar. These values have to be compared with the trend found by the twilight method of 53 mmagSQM arcsec−2 year−1 and 86 mmagSQM arcsec−2 year−1 for the two sites, respectively." [file: pmc_PMC11768471_sensors2025.txt]

**Pun, So, Leung and Wong 2014**, "Contributions of artificial lighting sources on light pollution in Hong Kong measured through a night sky brightness monitoring network", arXiv:1401.1200. Fetched https://arxiv.org/pdf/1401.1200. Saved `arxiv_1401.1200.pdf`, `_flow.txt`, `.txt`. Sections 2.1 and 2.3:

> "it was discovered that the transparent cover window of the polycarbonate housing suffered from obvious aging and turned visually yellow after ∼ 12 months of outdoor operations." [file: arxiv_1401.1200_flow.txt]

> "It was determined that the long-term optical attenuation for the polycarbonate covers and the glass windows leveled at ∼ 0.25 and 0.10 mag arcsec−2 respectively, nearly 1 year after the commencement of sunlight exposure." [file: arxiv_1401.1200_flow.txt]

**Hänel and others 2018** (file as in 1.8), sections 4 and 7:

> "The long-term behaviour of SQMs is still an issue to be examined in detail." [file: arxiv_1709.09558_flow.txt]

> "while it is known that the plastic window of the SQM housing loses transmission over time, at least under tropical climates (So 2014)." [file: arxiv_1709.09558_flow.txt]

**Oregon report 2023** (file as in 1.6), Processing Step 2:

> "Our estimate is .019 mags/arcsecond2 per year." [file: oregon_testimony_88792_flow.txt]

> "Unihedron (personal communication, 2022) notes that two issues can be involved: 1) development of a translucent film on the blue glass IR filter, which seems related to moisture and 2) yellowing of the plastic case of the semiconductor sensor over time." [file: oregon_testimony_88792_flow.txt]

**Bará, Lima and Zamorano 2019** (file as in 1.8): the Galician network read darker by 0.09 a year over 2015 to 2018, cause left open between ageing, aerosols and real change:

> "Overall, the available data suggest that the zenithal readings in the Sky Quality Meter (SQM) device-specific photometric band tended to increase during this period of time at an average rate of +0.09 magSQM /arcsec2 per year." [file: bara2019_sustainability_coimbra_flow.txt]

**For the TESS photometer: Alarcon and others 2021** (file as in 1.2), section 5.3:

> "The possibility that the TESS photometers suffer from aging effects is on the table. The only systematic study of this with SQM + window devices is the recent one by Puschnig et al. (2021), which suggests that a darkening of up to 0.053 mSQM arcsec−2 yr−1 can occur at midlatitudes. However, we do not observe evidence of this behavior in the continuous measurements of the TESS photometers or any bias in the distributions of photometers manufactured in different years. Further work should be done on this matter." [file: arxiv_2105.01066_flow.txt]

**A cause other than ageing, in print, of the right size: the solar cycle.** Plauchu-Frayn 2017 (file as in 1.1) checked their SQM against telescope photometry and then watched it read darker year by year as the Sun quietened. Its Table 3 (read from the page image, page 6) gives yearly SQM means of 21.42 ± 0.10 (2014), 21.60 ± 0.14 (2015) and 21.72 ± 0.12 (2016) against solar 10.7 cm flux of 152, 116 and 96 units: 0.12 to 0.18 mag darker per year with no ageing invoked.

> "From this figure it can be seen that SQM and CCD measurements are comparable, with no evidence of any drift." [file: arxiv_1609.00423_flow.txt]

> "The correlations in Table 4 indicate that there is a trend in which the NSB in the UBVR and SQM bands (|r| > 0.7) decreases as the solar activity decreases (i.e., lower solar flux), as has been found previously." [file: arxiv_1609.00423_flow.txt]

> "This implies that, since early 2014, the NSB at the OAN-SPM has decreased by ∆U = 0.7, ∆B = 0.5, ∆V = 0.3, ∆R = 0.5 and ∆magSQM = 0.4 mag arcsec−2, respectively, based upon the slopes in Table 4." [file: arxiv_1609.00423_flow.txt]

("NSB decreases" here means the sky got darker.) Alarcon 2021 says the same in general terms:

> "On the other hand, it is known that solar activity can affect NSB by establishing peak-to-peak differences of up to 0.5 mag in B and V during a solar cycle" [file: arxiv_2105.01066_flow.txt]

What this means for your 0.1 mag between 2024 and 2025 at fifteen of sixteen stations (my reading, not a quotation): it is two to three times the usual published ageing rate for an SQM, the published rates are all for SQMs and not for the TESS-W, and ageing would not be expected to step at the same time everywhere. A drop in airglow as the Sun passes its maximum is a published cause of the same size at dark sites. That the present solar cycle peaked around late 2024 is from memory, not verified; the monthly 10.7 cm flux for 2024 and 2025 would settle it, and so would whether your town stations show the step as strongly as your dark ones (airglow is a small part of a town's sky).

---

## What I could not open

- **Grauer, Grauer, Davies and Davies 2019**, "Impact of Space Weather on the Natural Night Sky", PASP (volume and page from memory, not verified: 131, 114508). Not tried at the journal; no preprint found. Known here only from its abstract as reproduced on the Unihedron forum (saved) and from Grauer and Grauer 2021, which cites it as reference 31 for the method.
- **Bará, Lima and Zamorano 2019** at the publisher (mdpi.com): HTTP 403. Read from a university repository copy instead.
- **Bará 2016** at the publisher (royalsocietypublishing.org): HTTP 403. Read from PubMed Central instead.
- **A document at core.ac.uk** (download/77519388.pdf) that a search listed for sidereal-time terms: HTTP 403; I do not know what it is.
- **Europe PMC's full-text service**: connection reset three times; the same articles were read from PubMed Central pages instead.
- **So 2014** (the Hong Kong work on housing-window ageing): not sought. Known only through Hänel and others 2018 and Pun and others 2014.
- **Wallner and others 2023** (a "triangular model" of the seasonal swing at Austrian dark-sky sites): not found by one search. Known only through Shah and others 2025.
- **Duriscoe 2013** (natural sky model for all-sky cameras), **Kolláth**, **Patat 2008** on this point, and **Ribas's Montsec work**: not opened in this pass. Duriscoe 2013 is known here only from Alarcon 2021, which lists it among "semiempirical models" used to correct for starlight and zodiacal light.
- I did not look at any figure in Kyba and others 2015 or Posch and others 2018 beyond what `scout.md` already records for the town side (darkening of about 5 % per hour at lit sites; gradients of 0.0 to 0.14 mag per hour between 10 PM and 2 AM).

## Things to be careful not to claim

1. Not new: that a dark site's zenith reading follows sidereal time, the size of that swing, or that the Galaxy-free hours move from one end of the night to the other through the year (Alarcon and others 2021 say the last in words; Masana and others 2021 draw it from a model).
2. Possibly yours, and to be worded as "I have not found": measuring the time of the nightly minimum itself over several years at many stations, and showing the split between dark sites and towns by that measure. My search was about twenty minutes, in English, with four publishers' pages closed to my client; theses and conference papers (Ribas on Montsec, So on Hong Kong) were not searched.
3. The size: the maker's 0.10 for the northern Milky Way is not what dark-site records show (about 0.4 to 0.6).
4. Seasons: "darkest in spring because of the Milky Way" has rivals in print for the same months (snow and vegetation in Puschnig and others 2022; snow and ski-season lighting in Bertolo and others 2019; an airglow cycle in Alarcon and others 2021, whose conclusions say "There are indications of semiannual oscillations"). The timing within a night is firmer ground than the seasonal mean.
5. Zodiacal light: not to be called negligible at the ends of the night on the maker's word; the dark-site papers remove it and a model makes it about a quarter of the natural zenith light at 40° N.
6. Ageing: the 0.1 mag step from 2024 to 2025 should not be put down to ageing. Published rates are for the Sky Quality Meter, 0.02 to 0.06 a year; none exists for the TESS-W; the solar cycle is a published cause of the right size.
7. Before dawn at a dark site: Grauer and Grauer report an unexplained change of about 0.07 mag before astronomical twilight on long winter nights after the star-time curve is removed, so not everything at the end of the night is the Milky Way.
8. Standing of sources: the Oregon report is a volunteer network's technical report; the 2025 Dutch network paper is a preprint; the Grauer and Grauer and Plauchu-Frayn figures' sizes are my readings of plots.

## Is the star-time pattern at dark sites already in print, and is the contrast with towns?

The dark-site half is in print: that a zenith photometer at a dark site reads the Milky Way's passage, by about 0.4 to 0.6 magnitude at northern mid-latitudes, is plotted against sidereal time or right ascension by Plauchu-Frayn and others (2017, Fig. 5), Grauer and Grauer (2021, Fig. 1) and Alarcon and others (2021, Fig. 8), drawn month by hour from a model by Masana and others (2021, Fig. 12), and Alarcon and others say in words that the Galaxy-free hours come at the end of the night early in the year and at the other end later. The contrast with towns is in print only in passing (the Oregon network's 2023 technical report for one August night and its monthly means; Grauer and Grauer's clock-time residual at the site above Tucson; one sentence in Bará and others 2019): I found no paper that measures the time of the nightly minimum through the year at a set of dark and lit stations and shows it keeping star time at the one and clock time at the other, and none that connects either to the proverb.
