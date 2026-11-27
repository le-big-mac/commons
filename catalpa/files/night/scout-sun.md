# Scout report: the Sun's activity cycle in dark-site night sky brightness, and what is already in print

Written 27 November 2026 (searches and downloads 13:21 to 13:35 UTC that day).

**How to read this.** Every line that starts with `>` and ends with `[file: ...]` is an exact quotation, checked by machine against text extracted from the named saved PDF (106 block quotations, all found, by `/tmp/scout3/qcheck_report.py`, which reads the quotations out of this file itself; it also checks twenty short phrases quoted inside sentences). Where a sentence runs across a page break in the source I give it as two quotations and say so. File paths are relative to `/home/agent1/night/lit/`: `src3/` is this session's downloads; `src/` and `src2/` are the earlier scouts' downloads, re-read here. Numbers read from a figure or from a page image are marked as such. Anything marked "from memory, not verified" was not checked against a saved page. All conversions were computed by `/tmp/scout3/conv.py`; its output lines are reproduced under the table and in Question 4.

**Sign convention used throughout.** In magnitudes per square arcsecond a larger number is a darker sky. Where authors write "NSB increases" I say which way they mean. In my own table every size is given as "brighter by so many magnitudes for 100 more solar flux units", so a positive number is a brighter sky at an active Sun.

**Units.** 1 solar flux unit (sfu) = 10^-22 W m^-2 Hz^-1 = 10^4 Jy, so 1 MJy = 100 sfu. Patat's slopes "per MJy" are therefore already "per 100 sfu".

> "1 sfu = 0.01 MJy." [file: src3/arxiv_1205.2003.pdf]

---

## Short answers

1. **Size of the effect.** Published broad-band slopes at dark sites, converted to one unit, run from about 0.17 mag per 100 sfu (Paranal, B and V, nightly values, Patat 2008) through 0.25 to 0.31 (Cerro Tololo and Mauna Kea, V, yearly means, Krisciunas) and 0.38 to 0.40 (the ESO sky model) to 0.4 to 0.5 (San Pedro Mártir, V and SQM, Plauchu-Frayn 2017; Calar Alto 525 nm, Leinert 1998, read from a figure). Over a whole cycle the printed ranges are 0.3 mag in V (Paranal, cycle 23), 0.4 ± 0.1 (La Palma, 1990 against 1995), 0.6 (Mauna Kea, cycle 22), and 0.8 to 1.0 (Walker 1988, cycle 21, as others cite him). The one published slope for an SQM is -0.005 mag per sfu (0.5 mag per 100 sfu), from three yearly means.
2. **Cycle 25 in zenith photometers.** One conference abstract (Barentine, Grauer, Gröller and Falco, ALAN 2025) reports three SQM-L sites in Arizona and New Mexico about 0.5 mag brighter from the last minimum to the present maximum. One volunteer technical report (Oregon, 2023) expected the rise and subtracted an estimate of it. One preprint (Komarova and others 2025, a telescope camera, not a zenith photometer) attributes about 15 percent of a brightening to the Sun. I found no refereed paper on the cycle 25 rise in SQM or TESS networks, and none using TESS-W.
3. **A solar term and an ageing term together.** Not as a joint fit, as far as I could find. The Oregon report applies both to the same SQM records, but each is imposed from outside (ageing from side-by-side new units, the solar part from Krisciunas 2007's line) and neither is fitted to the record. Plauchu-Frayn 2017 fitted the solar term alone and argued from a camera comparison that there was no drift.
4. **Physics.** Sources below (Noll and others 2012 and 2025; Leinert and others 1998).
5. **TESS-W ageing rate.** None published that I could find. The only statement is still Alarcon and others 2021 ("we do not observe evidence of this behavior"), repeated by the Oregon report. Zamorano's "Monitoring with TESS photometers" (version 2.0, April 2026) and the TESS photometer manual (version 4.1, September 2026) contain none of the words ageing, aging, drift or degradation in their extracted text.

---

## Question 1. The size of the solar-cycle effect at dark sites

### 1.1 Patat 2008: Paranal, UBVRI, the only source that prints a slope per unit flux with errors in every band

F. Patat, "The Dancing Sky: 6 years of night sky observations at Cerro Paranal", arXiv:0801.2270 (Astronomy & Astrophysics 481, 575, 2008: volume and page from memory, not verified). Saved earlier as `src/patat2008_arxiv_0801.2270.pdf` (from https://arxiv.org/pdf/0801.2270). Data April 2001 to January 2007, the descent of cycle 23; nightly averages from a large-telescope camera, corrected for zodiacal light.

Abstract:

> "A clear dependency on the solar activity is detected in all passbands and it is particularly pronounced in the U band, where the sky brightness decreased by ∼0.6 mag arcsec−2 from maximum to minimum of solar cycle n. 23. No correlation is found between solar activity and the intensity of the Na I D doublet and the OH bands." [file: src/patat2008_arxiv_0801.2270.pdf]

("Decreased" here means the sky got darker.) Section 4:

> "During this interval the Solar Flux Density (hereafter S FD) spans from 0.8 to 2.4 MJy, a range which is very close to that of a full cycle" [file: src/patat2008_arxiv_0801.2270.pdf]

> "All passbands show very good linear correlations, an example of which is presented in Fig. 6 for the V filter. In order to give a quantitative representation of the effect, I have fitted a relation of the type m = m0 +γ S FD to the data." [file: src/patat2008_arxiv_0801.2270.pdf]

> "the slope (γ, mag arcsec−2 MJy−1 )" [file: src/patat2008_arxiv_0801.2270.pdf]

> "the Table includes also the estimated full solar cycle variation (∆m = |(2.4 − 0.8)γ|)" [file: src/patat2008_arxiv_0801.2270.pdf]

Table 4 (page 6; columns: filter, m at solar minimum, m at average flux, ∆m, m0 with error, γ with error, scatter σ, correlation r, number of nights N). I also checked these five rows against the page image.

> "U 22.86 22.58 0.61 23.15 (0.12) −0.36 (0.07) 0.15 0.47 32" [file: src/patat2008_arxiv_0801.2270.pdf]

> "B 23.11 22.98 0.29 23.25 (0.04) −0.17 (0.02) 0.12 0.40 127" [file: src/patat2008_arxiv_0801.2270.pdf]

> "V 21.99 21.86 0.30 22.13 (0.05) −0.17 (0.03) 0.14 0.42 148" [file: src/patat2008_arxiv_0801.2270.pdf]

> "R 21.26 21.09 0.37 21.33 (0.04) −0.22 (0.02) 0.15 0.44 202" [file: src/patat2008_arxiv_0801.2270.pdf]

> "I 19.81 19.72 0.20 19.90 (0.06) −0.11 (0.04) 0.18 0.28 144" [file: src/patat2008_arxiv_0801.2270.pdf]

The negative γ means a brighter sky at higher flux. The fit is linear in magnitude. Note the modest correlation coefficients (0.28 to 0.47) and the scatter of 0.12 to 0.18 mag about the line.

What Patat says of others' sizes, and of cycles differing:

> "Walker (1988) quoted maximum ranges of ∆V ≃1.0 and ∆B ≃0.8 mag arcsec−2 for solar cycle n. 21, while Krisciunas (1997) reports ∆V=0.6 for solar cycle n. 22, and similar values are reported by Leinert et al. (1995) and Mattila et al. (1996)." [file: src/patat2008_arxiv_0801.2270.pdf]

> "These facts seem to suggest that not all solar cycles have identical effects on the night glow." [file: src/patat2008_arxiv_0801.2270.pdf]

Conclusions:

> "The excursion between sunspot maximum and minimum of solar cycle n. 23 is 0.6, 0.3, 0.3, 0.4 and 0.2 mag arcsec−2 in U, B, V, R and I passbands, respectively." [file: src/patat2008_arxiv_0801.2270.pdf]

> "The reaction of the nightglow to the solar variations seems to take place with a time delay of the order of 2-3 weeks." [file: src/patat2008_arxiv_0801.2270.pdf]

What it shows: 0.17 mag per 100 sfu in B and V, 0.22 in R, 0.36 in U, 0.11 in I, at one site over one cycle, with the best correlation against flux averaged over weeks, not the previous day.

### 1.2 Krisciunas 1997: Mauna Kea, V and B, a whole cycle, a line fitted in brightness (not magnitude)

K. Krisciunas, "Optical Night-Sky Brightness at Mauna Kea over the Course of a Complete Sunspot Cycle", arXiv:astro-ph/9706111 (PASP 109, 1181, 1997: from memory, not verified). Saved earlier as `src/krisciunas1997_arxiv_astro-ph9706111.pdf`. September 1985 to August 1996, one telescope and photometer; yearly averages, corrected to the zenith, in nanoLamberts (nL).

> "In Fig. 3 we give the yearly averages of sky brightness converted to nL as a function of the 10.7 cm solar flux on the dates when sky brightness was measured." [file: src/krisciunas1997_arxiv_astro-ph9706111.pdf]

> "Bzen = (47.021 ± 2.784) + (0.2019 ± 0.0222) × (10.7 cm solar flux) ." [file: src/krisciunas1997_arxiv_astro-ph9706111.pdf]

> "Taking the extrema of the observed daily solar flux, the implied range of Bzen is 59.74 to 124.43 nL, or 21.89 > I(µV ) > 21.09." [file: src/krisciunas1997_arxiv_astro-ph9706111.pdf]

> "Equation 5 implies that the airglow contribution ranged from 11.0 to 49.5 nL, a factor of 4.5." [file: src/krisciunas1997_arxiv_astro-ph9706111.pdf]

> "We have shown that the zenith V -band sky brightness at the mid-level of Mauna Kea varies between 21.3 to 21.9 magnitudes per square arc second over the course of a complete sunspot cycle." [file: src/krisciunas1997_arxiv_astro-ph9706111.pdf]

> "The color of the sky is B − V = 0.930 and does not change discernibly over the course of the sunspot cycle." [file: src/krisciunas1997_arxiv_astro-ph9706111.pdf]

What it shows: 0.20 nL per sfu on a floor of 47 nL. In magnitudes that is 0.31 mag from 70 to 170 sfu and 0.29 mag from 100 to 200 sfu (arithmetic below). Because the line is straight in brightness, the size in magnitudes depends on where on the flux axis you stand and on how bright the non-airglow floor is.

### 1.3 Krisciunas and others 2007: Cerro Tololo, V, a line drawn in a figure and no equation in the text

K. Krisciunas and six others, "Optical Sky Brightness at Cerro Tololo Inter-American Observatory from 1992 to 2006", arXiv:0705.1153 (PASP 119, 687 to 696, as listed in the Barentine abstract's references). Saved earlier as `src/krisciunas2007_arxiv_0705.1153.pdf`.

Conclusions (the sentence crosses a page break; two quotations):

> "The resulting database demonstrates a correlation of the V -band sky brightness with the phase of the solar cycle, as has been found by others over the past 80 years. A solar cycle effect can be seen to a lesser extent in the B-band data, but there appears to be no significant solar cycle effect" [file: src/krisciunas2007_arxiv_0705.1153.pdf]

> "in the R- and I-band data." [file: src/krisciunas2007_arxiv_0705.1153.pdf]

> "We find that the V -band sky brightness is most tightly correlated with the solar flux obtained 5 days prior to the night in question." [file: src/krisciunas2007_arxiv_0705.1153.pdf]

> "Fig. 5.— Yearly averages of zenith V -band sky brightness obtained from CCD imagery at Cerro Tololo (converted to flux) vs. the average of the 10.7-cm solar flux 4.5 days prior to when the sky brightness was measured." [file: src/krisciunas2007_arxiv_0705.1153.pdf]

The paper prints no equation for the line. Read from the figure's page image (page 24) by me: the line runs from about (65 sfu, 56.3 nL) to about (220 sfu, 81 nL), a slope of 0.159 nL per sfu and an intercept of about 46 nL. Two other readers have read the same figure, and both are in print:

> "ZenithV-Band-Brightness = 46. + 0.1575 x SolarFlux," [file: src2/oregon_testimony_88792.pdf]

> "The range of these CCD broadband night sky brightness data correspond to approximately a (nL, s.f.u) of from (55 nL, 70 s.f.u.) to (80 nL, 215 s.f.u). These data indicate a V-band increase of -0.41 mag/arcsec2 corresponds to an increase of in 10.7 cm solar flux of 145 s.f.u over the course of a solar cycle." [file: src2/arxiv_2112.01664.pdf]

(Grauer and Grauer's "increase of -0.41" means brighter by 0.41 mag.) What it shows: 0.25 to 0.28 mag per 100 sfu in V at Cerro Tololo, less in B, nothing in R and I.

### 1.4 Benn and Ellison 1998: La Palma, 1990 against 1995

C. R. Benn and S. L. Ellison, "La Palma night-sky brightness", arXiv:astro-ph/9909153 (New Astronomy Reviews 42, 503 to 507, as listed in the Barentine abstract's references). Fetched https://arxiv.org/pdf/astro-ph/9909153; saved `src3/arxiv_astro-ph_9909153.pdf`, `.txt`, `_flow.txt`.

> "The measured sky brightness varies with solar cycle, being 0.4 ± 0.1 mag brighter in 1990 than in 1995 (Fig. 2)." [file: src3/arxiv_astro-ph_9909153.pdf]

> "The curve indicates the expected variation of sky brightness with date, using the S10.7cm flux density as an indicator of solar activity." [file: src3/arxiv_astro-ph_9909153.pdf]

What it shows: 0.4 ± 0.1 mag between a maximum year and a minimum year, B and V combined (Fig. 2 plots "combined B −0.8, V"). The paper gives no flux values and no slope, so I have not converted it. (If the yearly mean flux was about 190 sfu in 1990 and about 77 in 1995, which is from memory, not verified, that would be about 0.35 mag per 100 sfu.)

### 1.5 Plauchu-Frayn and others 2017, Table 4: the only printed slope for an SQM

I. Plauchu-Frayn and six others, "Night sky brightness at San Pedro Martir Observatory", arXiv:1609.00423 (PASP 129, 035003, 2017: from memory, not verified). Saved earlier as `src2/arxiv_1609.00423.pdf`. Table 4 is on page 8; I read it from the page image as well as from the extracted text, and the two agree.

| Filter | a (mag arcsec^-2 per sfu) | b | r | P |
|---|---|---|---|---|
| U | -0.009 | 23.37 | -0.97 | 0.03 |
| B | -0.006 | 23.31 | -0.99 | 0.01 |
| V | -0.004 | 22.08 | -0.79 | 0.21 |
| R | -0.006 | 21.59 | -0.81 | 0.19 |
| I | -0.0003 | 19.38 | -0.08 | 0.92 |
| SQM | -0.005 | 22.22 | -0.99 | 0.02 |

> "a and b are the slope and intercept, respectively, of the linear fit, NSB = a × Flux⊙ + b, r is the correlation coefficient, and P is the probability of obtaining the result by chance." [file: src2/arxiv_1609.00423.pdf]

> "SQM −0.005 22.22 −0.99 0.02" [file: src2/arxiv_1609.00423.pdf]

> "V −0.004 22.08 −0.79 0.21" [file: src2/arxiv_1609.00423.pdf]

> "These trends have a high statistical significance (P < 0.05) only for the UB and SQM bands." [file: src2/arxiv_1609.00423.pdf]

Section 4.1 (the sentence crosses from page 7 to page 8; three quotations in order):

> "Since 1947, the minimum and maximum of the monthly average solar 10.7 cm flux are approximately 60 and 250 sfu" [file: src2/arxiv_1609.00423.pdf]

> "and the slopes reported in Table 4, the total variation" [file: src2/arxiv_1609.00423.pdf]

> "in NSB due to the solar activity over a complete cycle would be 1.8, 1.2, 0.7, and 1.1 mag in the UBVR bands, respectively, and 0.9 mag for SQM band." [file: src2/arxiv_1609.00423.pdf]

> "This implies that, since early 2014, the NSB at the OAN-SPM has decreased by ∆U = 0.7, ∆B = 0.5, ∆V = 0.3, ∆R = 0.5 and ∆magSQM = 0.4 mag arcsec−2, respectively, based upon the slopes in Table 4." [file: src2/arxiv_1609.00423.pdf]

("NSB has decreased" means the sky got darker.) Their compilation of many observatories (Table 6, B slope -0.003 and V slope -0.005 mag per sfu):

> "From Table 6, we estimate a maximum variation over a solar cycle of 0.6 mag and 0.9 mag in the B and V bands, respectively, supposing that the solar activity varies from a minimum of 60 sfu to a maximum of 250 sfu." [file: src2/arxiv_1609.00423.pdf]

What it shows: an SQM slope of 0.5 mag per 100 sfu, the largest in print. It rests on three yearly SQM means (2014, 2015, 2016: 21.42, 21.60, 21.72 at 152, 116 and 96 sfu, from the earlier scout's reading of Table 3), all on the declining side of one cycle, so in that record time and solar flux cannot be told apart. The authors' ground for ruling out drift is a comparison with camera photometry:

> "From this figure it can be seen that SQM and CCD measurements are comparable, with no evidence of any drift." [file: src2/arxiv_1609.00423.pdf]

### 1.6 Leinert and others 1998: one figure, no number in the text

Ch. Leinert, S. Bowyer, L. K. Haikala, M. S. Hanner, M. G. Hauser and others, "The 1997 reference of diffuse night sky brightness", Astronomy and Astrophysics Supplement Series 127, 1 to 99 (1998; reference as printed on the repository's cover page). The journal site refused automated clients; fetched the HAL open repository copy https://insu.hal.science/insu-03527749/document; saved `src3/leinert1998_hal_insu-03527749.pdf`, `.txt`, `_flow.txt`.

> "An example for the variation of sky brightness with solar activity is given in Fig. 10." [file: src3/leinert1998_hal_insu-03527749.pdf]

> "Fig. 10. Correlation between the night sky brightness observed at Calar Alto at 525 nm with the solar activity, measured by the 10.7 cm radio flux density (in units of 104 Jy)" [file: src3/leinert1998_hal_insu-03527749.pdf]

Read from the page image of Fig. 10 (PDF page 15, journal page 14) by me, so approximate: about fourteen points, dated 1989 to 1993 in the legend, at 91 to 236 sfu; the fitted line runs from about 268 at 91 sfu to about 470 at 236 sfu, in units of 10^-9 erg cm^-2 s^-1 sr^-1 Å^-1. The plot carries the heading L134/L183 (read from the image; it is not in the extracted text), so the field is a dark cloud and not the zenith, and 525 nm is a medium band chosen to sit in a gap of the night-sky spectrum. That line is 0.50 mag from 70 to 170 sfu and 0.44 mag from 100 to 200 sfu.

### 1.7 Patat 2003: the previous day's flux predicts nothing

F. Patat, "UBVRI Night sky brightness during sunspot maximum at ESO-Paranal", arXiv:astro-ph/0301115 (A&A 400, 1183, 2003: from memory, not verified). Saved earlier as `src/patat2003_arxiv_astro-ph0301115.pdf`.

> "Walker (1988b) found that B and V sky brightness is well correlated with the 10.7 cm solar radio flux and reported a range of ∼ 0.5 mag in B and V during a full sunspot cycle. Similar values were found by Krisciunas (1990), Leinert et al. (1995) and Mattila et al. (1996), so that the effect of solar activity is commonly accepted (Leinert et al. 1998)." [file: src/patat2003_arxiv_astro-ph0301115.pdf]

> "A linear least squares fit to the data (solid line) gives a slope of 0.14±0.01 mag arcsec−2 MJy−1 , which turns into a variation of 0.24±0.11 mag arcsec−2 during a full solar cycle." [file: src/patat2003_arxiv_astro-ph0301115.pdf]

> "seem to indicate no short–term dependency from the 10.7 cm solar flux." [file: src/patat2003_arxiv_astro-ph0301115.pdf]

> "no firm prediction on the night sky brightness can be made on the basis of the solar flux measured during the day preceeding the observations" [file: src/patat2003_arxiv_astro-ph0301115.pdf]

What it shows: within eighteen months near maximum (April 2000 to September 2001, flux 1.2 to 2.4 MJy), nightly R brightness against the previous day's flux gave a weak slope (correlation 0.19) and B and V gave nothing. The solar effect is a slow one. Note that Patat 2003 and Patat 2008 cite Walker 1988 for different sizes (about 0.5 mag in one, 0.8 to 1.0 in the other).

### 1.8 Noll and others 2012: what the ESO sky model predicts for broad bands

S. Noll and six others, "An atmospheric radiation model for Cerro Paranal. I. The optical spectral range", arXiv:1205.2003 (A&A 543, A92, 2012: from memory, not verified). Fetched https://arxiv.org/pdf/1205.2003; saved `src3/arxiv_1205.2003.pdf`, `.txt`, `_flow.txt`. Section 5.2:

> "he estimated a flux increase of 0.6, 0.3, and 0.2 mag for a change in the solar radio flux from 80 to 240 sfu." [file: src3/arxiv_1205.2003.pdf]

> "In contrast, Walker (1988) gives ∆B ≈ 0.8 mag and ∆V ≈ 1.0 mag for a similar solar activity change. About 0.5 mag are reported by Mattila et al. (1996) for blue wavelengths and by Krisciunas et al. (1997) for the V band." [file: src3/arxiv_1205.2003.pdf]

> "the sky model gives 0.7, 0.5, 0.6, 0.6, and 0.3 mag for the U BVRI filters." [file: src3/arxiv_1205.2003.pdf]

> "For B to R, the solar activity appears to be responsible for about half the night-sky variability." [file: src3/arxiv_1205.2003.pdf]

("He" is Patat 2008, for U, V and I.) What it shows: the model that most observatories now use gives 0.6 mag in V for 80 to 240 sfu, that is 0.38 mag per 100 sfu, twice Patat's measured 0.17 at the same site.

### Published sizes gathered, in one unit

"Per 100 sfu" is magnitudes per square arcsecond brighter for 100 more flux units. Where the source's line is straight in magnitude the figure holds anywhere on the flux axis; where it is straight in brightness I give it for 70 to 170 sfu and for 100 to 200 sfu.

| Source | Site, years, flux range | Band, instrument, averaging | As printed | Per 100 sfu |
|---|---|---|---|---|
| Patat 2008, Table 4 | Paranal, 2001 to 2007, 80 to 240 sfu | B, camera, nightly | γ = -0.17 ± 0.02 mag per MJy | 0.17 |
| same | same | V | -0.17 ± 0.03 | 0.17 |
| same | same | R | -0.22 ± 0.02 | 0.22 |
| same | same | U; I | -0.36 ± 0.07; -0.11 ± 0.04 | 0.36; 0.11 |
| Krisciunas 1997, eq. 5 | Mauna Kea, 1985 to 1996 | V, photometer, yearly | 47.021 + 0.2019 F nL | 0.31 (70 to 170); 0.29 (100 to 200) |
| Krisciunas and others 2007, Fig. 5 | Cerro Tololo, 1992 to 2006, about 70 to 215 sfu | V, camera, yearly | line only; read as 46 + 0.1575 F nL (Oregon report) or 55 to 80 nL over 70 to 215 sfu (Grauer and Grauer 2021) | 0.27 (70 to 170); 0.25 (100 to 200); 0.28 (Grauer) |
| Benn and Ellison 1998 | La Palma, 1990 against 1995 | B and V combined, camera | 0.4 ± 0.1 mag between the two years | not convertible from the paper |
| Leinert and others 1998, Fig. 10 | Calar Alto, 1989 to 1993, 91 to 236 sfu | 525 nm medium band, dark-cloud field | figure only (my reading: 268 to 470 over 91 to 236 sfu) | 0.50 (70 to 170); 0.44 (100 to 200), from a figure |
| Plauchu-Frayn and others 2017, Table 4 | San Pedro Mártir, 2013 to 2016, 96 to 152 sfu (yearly) | SQM, yearly, three points | a = -0.005 mag per sfu | 0.50 |
| same | same | V; B; R; U; I, camera, yearly | -0.004; -0.006; -0.006; -0.009; -0.0003 | 0.40; 0.60; 0.60; 0.90; 0.03 |
| Plauchu-Frayn and others 2017, Table 6 | many observatories together | B; V | -0.003; -0.005 | 0.30; 0.50 |
| Noll and others 2012, sky model | Paranal model, 80 to 240 sfu | U; B; V; R; I | 0.7; 0.5; 0.6; 0.6; 0.3 mag over 160 sfu | 0.44; 0.31; 0.38; 0.38; 0.19 |
| Komarova and others 2025 (a run of the ESO sky model) | La Silla, model, 70 to 140 sfu | V | 21.97 to 21.69 | 0.40 |
| Walker 1988, not opened, as cited | San Benito Mountain (site from memory, not verified), cycle 21 | B, V | "∼ 0.5 mag" (Patat 2003); "∆V ≃1.0 and ∆B ≃0.8" (Patat 2008); the same "for a similar solar activity change" as 80 to 240 sfu (Noll 2012) | 0.3 to 0.6, depending on which citation |
| Barentine and others 2025 (abstract) | three SQM-L sites, Arizona and New Mexico, 2020 to 2025 | SQM-L | "about 0.5" mag brighter, minimum to maximum | no flux range given |
| Patat 2003 | Paranal, 2000 to 2001, 120 to 240 sfu, previous day's flux | R; B, V | 0.14 ± 0.01 per MJy (r = 0.19); consistent with zero | a short-term null, not a cycle slope |

Output of `/tmp/scout3/conv.py` (the arithmetic):

```
Krisciunas 1997, Mauna Kea V, B = 47.021 + 0.2019 F (nL)
  F 70->170: 61.15 -> 81.34 nL, ratio 1.3302, 0.310 mag
  F 100->200: 67.21 -> 87.40 nL, ratio 1.3004, 0.285 mag
  check of their own range: 2.5 log10(124.43/59.74) = 0.797 mag (they give 21.89 - 21.09 = 0.80)
Krisciunas 2007, Cerro Tololo V, line as written in the Oregon report: 46 + 0.1575 F (nL)
  F 70->170: 57.02 -> 72.78 nL, ratio 1.2762, 0.265 mag
  F 100->200: 61.75 -> 77.50 nL, ratio 1.2551, 0.247 mag
  my reading of Fig. 5 line ends (65, 56.3) and (220, 81): slope 0.1594 nL/sfu, intercept 45.9 nL
  Grauer 2021 reading: 55 -> 80 nL over 70 -> 215 sfu: 0.407 mag per 145 sfu = 0.281 mag per 100 sfu
  absolute: 0.1575 nL/sfu x 3.18310 = 0.5013 microcd/m2 per sfu = 50.1 microcd/m2 per 100 sfu
Leinert 1998 Fig. 10, Calar Alto 525 nm, line ends read from the figure: (91, 268) and (236, 470)
  slope 1.393 per sfu; F 70->170: 238.7 -> 378.1, ratio 1.5835, 0.499 mag
  slope 1.393 per sfu; F 100->200: 280.5 -> 419.8, ratio 1.4966, 0.438 mag
Noll 2012 sky model, 80 -> 240 sfu (160 sfu):
  U: 0.7 mag / 1.6 = 0.437 mag per 100 sfu
  B: 0.5 mag / 1.6 = 0.312 mag per 100 sfu
  V: 0.6 mag / 1.6 = 0.375 mag per 100 sfu
  R: 0.6 mag / 1.6 = 0.375 mag per 100 sfu
  I: 0.3 mag / 1.6 = 0.187 mag per 100 sfu
Patat 2008 as restated by Noll 2012 (80 -> 240 sfu): U 0.6, V 0.3, I 0.2; Patat's own gamma is per MJy = per 100 sfu directly
Komarova 2025 (ESO sky model run): 21.97 - 21.69 = 0.28 mag over 70 sfu = 0.40 mag per 100 sfu
Plauchu-Frayn 2017 Table 4: a x 100:
  U: -0.009 x 100 = -0.90 mag per 100 sfu
  B: -0.006 x 100 = -0.60 mag per 100 sfu
  V: -0.004 x 100 = -0.40 mag per 100 sfu
  R: -0.006 x 100 = -0.60 mag per 100 sfu
  I: -0.0003 x 100 = -0.03 mag per 100 sfu
  SQM: -0.005 x 100 = -0.50 mag per 100 sfu
  SQM yearly means 21.42 (152 sfu), 21.60 (116), 21.72 (96): end-to-end slope -0.00536 mag/sfu
  their cycle totals: 0.005 x (250-60) = 0.95 (they give 0.9); since early 2014: 0.005 x (162-82) = 0.40 (they give 0.4)
  Table 6 (several observatories together): B -0.003 x 100 = -0.30, V -0.005 x 100 = -0.50
```

Three things make these numbers hard to compare with a photometer fit, and they are worth saying when you compare. First, the airglow adds brightness, so a slope in magnitudes depends on how bright everything else in the beam is: a wide-beam photometer takes in more starlight than a camera measuring between the stars, which dilutes the same airglow change into fewer magnitudes. Second, the averaging differs (nightly values against weeks of flux at Paranal, yearly means elsewhere), and the scatter about the line is 0.12 to 0.18 mag at Paranal. Third, the cycles differ: the sources cover cycles 21, 22, 23 and 24, and Patat says outright that they do not behave alike.

---

## Question 2. The rise of cycle 25 (2020 to 2025) in SQM or TESS records

### 2.1 Barentine, Grauer, Gröller and Falco, ALAN 2025 (conference abstract): three SQM-L sites, about 0.5 mag

J. C. Barentine, A. D. Grauer, H. Gröller and E. Falco, "Natural influences on night sky brightness and implications for site quality characterization", abstract for the ALAN 2025 conference (theme: Measurement and Modeling). Fetched https://www.johncbarentine.com/uploads/7/8/0/8/78081652/barentine-nsb-abstract.pdf; saved `src3/barentine_alan2025_nsb_abstract.pdf`, `.txt`, `_flow.txt`. Three pages, one figure, no table, no slope against flux. I searched for a full paper and found none.

> "We use data from three Unihedron Sky Quality Meter-Lens (SQM-L) devices at sites in the southwestern U.S. spanning a distance of 300 km" [file: src3/barentine_alan2025_nsb_abstract.pdf]

> "The temporal window of the data set brackets the time between the minimum of Solar Cycle 24 to the ongoing maximum of Cycle 25; over this time we see an average NSB increase of about 0.5 magnitudes per square arcsecond (mpsa)." [file: src3/barentine_alan2025_nsb_abstract.pdf]

> "We searched for, but did not find, strong evidence of a time delay between the onset of solar geomagnetic events and elevated NSB reported by, e.g., Krisciunas et al. 2007." [file: src3/barentine_alan2025_nsb_abstract.pdf]

> "the dispersion of NSB measurements for all three monitors is roughly the same at solar minimum as at solar maximum, ranging up to ±0.3 mpsa." [file: src3/barentine_alan2025_nsb_abstract.pdf]

("NSB increase" here means brighter: the same abstract speaks of "elevated NSB" and "high NSB values" for bright episodes.) The sites are Kitt Peak, Mount Lemmon and Cosmic Campground. They compare with the interplanetary magnetic field and solar wind proton energy, not with the 10.7 cm flux. No ageing correction is mentioned. What it shows: the cycle 25 rise has been reported from SQM-type zenith photometers at dark sites, with a size, in a conference abstract.

### 2.2 The Oregon Skyglow Measurement Network report, 2023: expected the rise and subtracted it

Oregon Skyglow Measurement Network, Technical Report Edition #7, "Data from April 2019 to November 2022", dated March 6, 2023 (a volunteer project's report, filed as legislative testimony; not a refereed paper). Saved earlier as `src2/oregon_testimony_88792.pdf`.

> "So, space weather may cause our SQM data to read brighter since our SQM project began in mid-2019, by increased airglow, independently of any changes in light pollution from the ground." [file: src2/oregon_testimony_88792.pdf]

> "Note the increase in estimated airglow (yellow dots) since September 2021." [file: src2/oregon_testimony_88792.pdf]

What it shows: an SQM network that, by early 2023, treated the rising Sun as a known bias in trend estimates and removed a modelled amount. It did not measure the rise in its own data (see Question 3).

### 2.3 Komarova and others 2025: a telescope camera at a brightening site, about 15 percent put down to the Sun

I. A. Komarova and six others, "The BVRcIc sky brightness of the Caucasian Mountain Observatory of MSU", arXiv:2501.13266 (22 January 2025). Fetched https://arxiv.org/pdf/2501.13266; saved `src3/arxiv_2501.13266.pdf`, `.txt`, `_flow.txt`. Camera frames from a 60 cm telescope, 2019 to 2024; not a zenith photometer; a site with growing light pollution.

> "In 5 years the sky brightness had increased by 0.7m in B and V , by 0.45m in Rc , and ∼ 0.1m in Ic . We found that the brightness growth is mostly (up to ∼ 85%) due to the increasing light pollution from nearby cities, while the remainder can be attributed to the increase of solar activity after the 2019 minimum." [file: src3/arxiv_2501.13266.pdf]

> "We found high correlation between sky brightness and radio flux (r = 0.76), and no correlation between sky brightness and the Kp index (r ≈ 0.1)." [file: src3/arxiv_2501.13266.pdf]

> "monthly radio flux from the Sun of 70 sfu for the minimum and 140 sfu for the maximum of solar activity. As a result, we derived the model V sky brightness at La Silla of 21.97m /arcsec2 for the solar activity minimum and 21.69m /arcsec2 for the solar activity maximum. Thus, the contribution of solar activity to the value of sky brightness is ∼ 0.3m /arcsec2 ." [file: src3/arxiv_2501.13266.pdf]

> "found that the additive effect is ∼ 0.1m /arcsec2 during the solar maximum period." [file: src3/arxiv_2501.13266.pdf]

("Increased" means brighter.) The solar share is not fitted: it is taken from a run of the ESO sky model and scaled to the site's brighter sky. The correlation of 0.76 with radio flux is partly shared with the light-pollution trend, since both rose over the same years.

### 2.4 What the 2021 photometer papers said they could not yet see

Alarcon and others 2021 (TESS photometers, saved earlier as `src2/arxiv_2105.01066.pdf`), section 5.3:

> "The correlation has been checked by taking different time delays and no conclusive trend has been found. This does not mean that it cannot be detected with broadband photometers, but it is a consequence of the quiescence of the Sun at minimum, when the range of F10.7 cm intensities is too low to check these relations. More measurements will be accumulated in the coming years to try to verify this relationship." [file: src2/arxiv_2105.01066.pdf]

Grauer and Grauer 2021 (SQM-LU-DL and TESS-W photometers at five sites, 4 September 2018 to 30 April 2020, saved earlier as `src2/arxiv_2112.01664.pdf`):

> "Variations in broadband night sky airglow are not always accompanied by changes in 10.7 cm solar flux (Fig. 5)." [file: src2/arxiv_2112.01664.pdf]

> "The broadband brightness changes we observed are not correlated with changes in solar EUV flux." [file: src2/arxiv_2112.01664.pdf]

What these show: the TESS network's own paper left the solar relation as future work, and I found no follow-up from that group or any other using TESS-W through the maximum. Searches run: four web searches on cycle 25 with SQM, TESS-W, airglow and named authors, and the arXiv listing for abstracts holding "sky brightness" with "solar cycle", "solar cycle 25", "solar activity" or "solar maximum", and all titles holding "sky brightness" since mid 2021. Two recent preprints were opened and had nothing on the Sun or on ageing (arXiv:2610.09028, sky brightness in central Portugal, October 2026; arXiv:2310.05429, Kottamia UBVRI, 2023); they are not kept.

---

## Question 3. Has anyone fitted a solar term and an ageing term to the same zenith-photometer record?

I found no paper that fits both at once. The nearest things in print:

**The Oregon report (2023) applies both corrections to the same SQM records, each fixed beforehand.** Abstract and processing steps 2 and 6:

> "apply a serial adjustment for an apparent aging phenomenon of the SQMs." [file: src2/oregon_testimony_88792.pdf]

> "Our estimate is .019 mags/arcsecond2 per year. Accordingly, we subtract values proportional to this assumed aging effect from our data, based on the progressive, serial exposure over time of measurements from each SQM in our network." [file: src2/oregon_testimony_88792.pdf]

> "We then subtract the brightness attributable to airglow caused by variation in the solar flux over time." [file: src2/oregon_testimony_88792.pdf]

> "We use the relationship shown in Figure H2 and the hourly solar flux data from the Canadian Solar Radio Monitoring Program to estimate the contribution of natural airglow to the visible band zenith sky brightness, and subtract that estimate from our measured SQM data." [file: src2/oregon_testimony_88792.pdf]

> "Because we are interested in the change of V-band brightness due to the solar flux, we eliminate the Yintercept (46.) from the correction" [file: src2/oregon_testimony_88792.pdf]

So the ageing rate (0.019 mag a year) came from two new units run beside two old ones, and the solar amount (0.1575 nL per sfu, about 50 microcandela per square metre per 100 sfu) was carried over from a V-band camera at Cerro Tololo to SQMs in Oregon using the hourly flux nearest each reading. Neither was estimated from the records being corrected, and the report gives no test of whether the carried-over solar slope fits its SQMs. Its data end in November 2022, before the maximum.

**Plauchu-Frayn and others 2017** fitted the solar term alone to an SQM (three yearly means) and set drift aside on the strength of the camera comparison quoted in 1.5.

**Bertolo and others 2019** (SQM network in the Veneto, saved earlier as `src2/bertolo2019_jimaging-05-00056.pdf`) name both window ageing and the falling Sun as possible causes of a darkening trend and correct for neither:

> "We also did not correct the data for the decrease of solar activity. This could be an explanation for the observed decrease in the sky brightness but, since it is a small amount, further work is still needed to confirm this." [file: src2/bertolo2019_jimaging-05-00056.pdf]

**Bará and others 2021** (saved earlier as `src2/arxiv_2011.15044.pdf`) note why town stations can separate the two: the darkening trends appear

> "even in strongly light polluted urban locations where the yearly variations of airglow associated with the solar cycle are not expected to be a relevant factor." [file: src2/arxiv_2011.15044.pdf]

**The twilight method** (Puschnig and others 2021 and 2022; Fiorentin and others 2022, which includes the SQM at La Silla) measures ageing where the sky is thousands of times brighter than airglow, so it needs no solar term and has none. The saved texts of Puschnig 2022 and Fiorentin 2022 hold no mention of solar activity or the solar cycle as a cause of night-time trends (Puschnig 2022 sets "a monthly averaged solar flux" as a fixed input of the sky model only). Nobody in those papers checked whether the night-time residual after the twilight correction follows the Sun at the dark sites.

**Komarova and others 2025** split a trend into solar and light-pollution parts (not ageing), with the solar part taken from a model.

What this means for the claim: a simultaneous least-squares fit of a term proportional to 10.7 cm flux and a linear drift to one zenith-photometer record, at dark sites, over a minimum and a maximum, appears not to be in print. Both ingredients are, and one report has applied both as fixed corrections.

---

## Question 4. The physics, in citable sentences

### Which emissions, and why they follow the Sun's short-wavelength output

**Noll and others 2025**, "PALACE v1.0: Paranal Airglow Line And Continuum Emission model", arXiv:2504.10683 (physics.ao-ph, 14 April 2025; I believe it was submitted to Geoscientific Model Development: from memory, not verified). Fetched https://arxiv.org/pdf/2504.10683; saved `src3/arxiv_2504.10683.pdf`, `.txt`, `_flow.txt`. Ten years of spectra from the Very Large Telescope. Abstract and introduction:

> "Excluding aurorae, the emission is caused by chemical reaction chains which are driven by the daytime photolysis and photoionisation of constituents of the middle and upper atmosphere by hard ultraviolet photons from the Sun." [file: src3/arxiv_2504.10683.pdf]

> "The most crucial atomic airglow lines are located between about 500 and 800 nm including prominent atomic oxygen (O) emission at 558, 630, 636, and 777 nm, the sodium Na D doublet at 589 nm, and the nitrogen (N) doublet at 520 nm." [file: src3/arxiv_2504.10683.pdf]

> "Various weak bands of iron monoxide (FeO) form a broad emission structure near 600 nm" [file: src3/arxiv_2504.10683.pdf]

How the model scales each emission with flux (equation 1), and the sizes (the "Variability" section and Table 4):

> "f (mbin, tbin, srf) = f0 (mbin, tbin) (1 + 0.01 mSCE (mbin, tbin) (srf − 100))," [file: src3/arxiv_2504.10683.pdf]

> "where mSCE is the regression slope relative to 100 sfu." [file: src3/arxiv_2504.10683.pdf]

> "Hence, a resulting ⟨mSCE ⟩ of +0.75 MJy−1 is not unexpected. The ESO Sky Model (Noll et al., 2012) uses +0.87 MJy−1 ." [file: src3/arxiv_2504.10683.pdf]

> "Very strong positive solar impacts are present for the lines originating in the ionosphere, where photoionisation depends on extreme UV photons from the Sun. The red O and N lines show about +1.5 MJy−1 , which is much higher than +0.68 MJy−1 for the red O lines in the ESO Sky Model." [file: src3/arxiv_2504.10683.pdf]

> "The emission of Na D returned a moderate value of +0.24 MJy−1 , whereas Noll et al. (2012) measured +0.11 MJy−1 ." [file: src3/arxiv_2504.10683.pdf]

> "The same study also revealed the weakly positive effect for FeO (+0.09 MJy−1 ) in Table 4." [file: src3/arxiv_2504.10683.pdf]

The OH sentence crosses a page break (two quotations):

> "For OH, ⟨mSCE ⟩ increases with increasing emission height (Noll et al., 2022), at least for low v ′ and N ′ , from about +0.12 to" [file: src3/arxiv_2504.10683.pdf]

> "+0.20 MJy−1 . According to Noll et al. (2023b)" [file: src3/arxiv_2504.10683.pdf]

So, per 100 sfu and relative to the level at 100 sfu, at Paranal: the green oxygen line (557.7 nm) rises by about 75 percent, the red oxygen lines (630 and 636 nm) by about 140 percent (Table 4 prints +0.754 and +1.432), sodium by 24 percent, the OH bands by 12 to 20 percent, and the FeO pseudo-continuum near 600 nm by only 9 percent (+0.086). The sample's 27-day mean flux ran only from 67 to 166 sfu:

> "For the whole X-shooter data set that almost covers an entire solar cycle, the 27-day averages only ranged from 67 to 166 sfu." [file: src3/arxiv_2504.10683.pdf]

> "There might be a flattening of the SCE for very high SRF not present in the X-shooter data set (maximum of 166 sfu)." [file: src3/arxiv_2504.10683.pdf]

**Noll and others 2012** (file as in 1.8), sections 4.3.2 and 4.4 and Table 2, from 1186 spectra of 1999 to 2005:

> "The solar activity strongly influences the intensities of O I and O2 , where the slopes are 0.0063 to 0.0087 sfu−1 . On the other hand, weak or no significant correlations are present for sodium and hydroxyl." [file: src3/arxiv_1205.2003.pdf]

> "Solar activity directly affects the Earth’s atmosphere by the amount of hard UV photons. The higher the photon energy, the more the production rate depends on solar activity (see Nicolet 1989). This relation appears to be important for O I and O2 airglow emission, which depends on the dissociation or ionisation of molecular oxygen by hard UV photons" [file: src3/arxiv_1205.2003.pdf]

> "For the airglow continuum, which is a major contribution to the night-sky brightness in the optical" [file: src3/arxiv_1205.2003.pdf]

> "The dependence of the continuum emission on solar radio flux is significant and comparable to O I (green and red) and O2 ." [file: src3/arxiv_1205.2003.pdf]

Table 2's slope row, in the order [O I] 5577, Na I D, [O I] 6300 and 6364, OH(7,0) to (6,2), O2(b-X)(0-1), continuum at 0.543 µm, with its footnote:

> "0.0087 0.0011 0.0068 0.0001 0.0063 0.0061" [file: src3/arxiv_1205.2003.pdf]

> "Slope for solar activity correction relative to mean solar radio flux for cycles 19 to 23 (≈ 129 sfu)." [file: src3/arxiv_1205.2003.pdf]

> "We obtained a mean airglow continuum for Cerro Paranal with an intensity of about 4.3 R nm−1 at 0.543 µm" [file: src3/arxiv_1205.2003.pdf]

The same table gives mean line strengths of 190 rayleighs for the green line, 43 for sodium and 190 for the red lines. A continuum of 4.3 rayleighs per nanometre across a band some 90 nm wide (my assumption for a V-like band) is about 390 rayleighs, twice the green line: in a broad visual band the continuum, not the green line, carries most of the airglow.

**The two Paranal models disagree about that continuum, and the newer one says so:**

> "Noll et al. (2012) measured the continuum variability only at 543 nm, which would best fit to the FeO class. However, an SCE of +0.61 MJy−1 and different climatological patterns as for Na do not match the expectations (see Table 4)." [file: src3/arxiv_2504.10683.pdf]

What those slopes mean for each emission taken alone, from 70 to 170 sfu (the rest of the output of `/tmp/scout3/conv.py`; my arithmetic from the two tables, not figures printed by the authors):

```
Noll 2012 Table 2, airglow parts alone, relative to 129 sfu; 70 -> 170 sfu:
  [OI]5577: factor 2.79 = 1.11 mag (that emission alone)
  NaD: factor 1.12 = 0.12 mag (that emission alone)
  [OI]6300: factor 2.14 = 0.82 mag (that emission alone)
  OH: factor 1.01 = 0.01 mag (that emission alone)
  O2(b-X): factor 2.00 = 0.75 mag (that emission alone)
  continuum 543 nm: factor 1.95 = 0.73 mag (that emission alone)
PALACE 2025 Table 4, relative to 100 sfu; 70 -> 170 sfu:
  O green 557.7: factor 1.97 = 0.74 mag (that emission alone)
  O red 630/636: factor 3.51 = 1.36 mag (that emission alone)
  Na D: factor 1.25 = 0.24 mag (that emission alone)
  FeO (+other) continuum: factor 1.09 = 0.09 mag (that emission alone)
  OH (low): factor 1.12 = 0.12 mag (that emission alone)
  OH (high): factor 1.21 = 0.21 mag (that emission alone)
  O2 b-X: factor 1.45 = 0.41 mag (that emission alone)
Noll 2012 means: continuum 4.3 R/nm x 90 nm (a V-like width, my assumption) = 387 R against 190 R for the green line
```

This matters for the broad-band size. If the visual continuum rises 61 percent per 100 sfu (2012), a V-like band should brighten by about 0.38 mag per 100 sfu, as the 2012 model says. If it rises only 9 percent (2025), the broad-band effect must come mostly from the oxygen lines and would be smaller, nearer Patat's measured 0.17. The 2025 paper does not give broad-band magnitudes, and I have not computed them.

**Krisciunas 1997** (file as in 1.2) on what the V band holds:

> "The V -band airglow, which is due to continuum plus 557.7 nm [O I] emission," [file: src/krisciunas1997_arxiv_astro-ph9706111.pdf]

**Benn and Ellison 1998** (file as in 1.4), the plain version:

> "The airglow is emitted by atoms and molecules in the upper atmosphere which are excited by solar UV radiation during the day. Its intensity correlates with solar activity, being ≈ 0.5 mag brighter at solar maximum, and can also vary randomly, by up to a few 10s of %, with position on the sky and with time during the night." [file: src3/arxiv_astro-ph_9909153.pdf]

**Leinert and others 1998** (file as in 1.6), section 6:

> "The airglow emissions vary considerably with time, on short (minutes) and long timescales, mainly due to changes in the atmosphere and in solar activity." [file: src3/leinert1998_hal_insu-03527749.pdf]

**The two photometers do not see the same mix.** Alarcon and others 2021 (file as in 2.4), section 2.1:

> "The SQM uses a Hoya CM500 filter for nominally limiting its effective bandpass to 400-–650 nm, whereas TESS is fitted with a dichroic filter that limits it to the 400-–740 nm spectral band" [file: src2/arxiv_2105.01066.pdf]

The TESS band takes in the red oxygen lines fully and more of the OH bands; Patat 2008 (file as in 1.1) on the red end:

> "Less clear is the behavior at longer wavelengths, which are dominated by the OH emissions, whose intensity is uncorrelated with solar activity (see Sec. 6)." [file: src/patat2008_arxiv_0801.2270.pdf]

### The same all night, or stronger early?

The sources say the part that comes from the high ionosphere (the red oxygen lines) fades through the night, and that is the part most sensitive to the Sun; the rest shows no simple nightly decline.

> "Often a systematic decrease of airglow emission during the course of the night is observed, explained as result of the energy stored during day in the respective atmospheric layers." [file: src3/leinert1998_hal_insu-03527749.pdf]

> "Only the red O I lines show a clear decrease by a factor of 1.4 from the beginning to the end of the night." [file: src3/arxiv_1205.2003.pdf]

> "The intensities of the ionospheric emissions clearly decrease in the course of the night with the exception of two local maxima in March and October at about 02:30 LT. The general trend is expected as photoionisation is limited to daytime, which causes a decrease of the ion density due to recombination at nighttime." [file: src3/arxiv_2504.10683.pdf]

> "It is well known that, during the first hours of the night, the [OI]6300 line shows a steady decline in brightness" [file: src/patat2008_arxiv_0801.2270.pdf]

On whether the solar-cycle effect itself changes through the night, the only source is the 2025 model, and its answer is not "strongest at dusk":

> "The green line as highest emission would need to peak in the evening, which is the case." [file: src3/arxiv_2504.10683.pdf]

> "As the strongest positive effects are located around midnight, this leads to a significant change of the intensity pattern in Fig. 9l for high SRF." [file: src3/arxiv_2504.10683.pdf]

(The first is about the green line's solar-cycle effect, the second about the red lines'.) And a caution on carrying Paranal's red-line behaviour elsewhere:

> "In any case, this equatorial ionisation anomaly causes unusually high ionospheric line intensities at Cerro Paranal." [file: src3/arxiv_2504.10683.pdf]

So a fair expectation from print is: a solar term somewhat larger in the first hours of the night in a band that includes 630 nm (both photometers do, the TESS more fully), with the size of that difference depending on magnetic latitude. Nobody has reported it from broad-band photometers. The earlier scout's sources (Patat 2003, Alarcon 2021, Plauchu-Frayn 2017) found no systematic nightly darkening in broad bands at all.

### Which flux average to use

> "Note that the analysis for PALACE was based on centred 27day averages" [file: src3/arxiv_2504.10683.pdf]

Patat 2008 found the correlation best for flux averaged over weeks with a lag of two to three weeks (quoted in 1.1); Krisciunas 2007 preferred the flux five days earlier; Patat 2003 found the previous day's flux useless; the Barentine abstract found no evidence of a delay; the Oregon report used the hourly flux nearest each reading. There is no agreed choice.

---

## Question 5. An ageing rate for the TESS-W

None found in print. What exists:

**Alarcon and others 2021** (file as in 2.4), section 5.3, from records made during the solar minimum that began in 2018:

> "However, we do not observe evidence of this behavior in the continuous measurements of the TESS photometers or any bias in the distributions of photometers manufactured in different years. Further work should be done on this matter." [file: src2/arxiv_2105.01066.pdf]

**The Oregon report 2023** repeats that and adds nothing of its own on the TESS:

> "Other researchers (Alarcon and others, 2021) found no evidence of aging of a different photometer, the TESS instrument." [file: src2/oregon_testimony_88792.pdf]

**The network's own current documents say nothing either way.** J. Zamorano, "Monitoring with TESS photometers for Light Pollution studies", a slide set marked

> "version 2.0 April 2026" [file: src3/zamorano_monitoring_with_tess_v1.pdf]

fetched from https://guaix.fis.ucm.es/~jaz/TESS/Monitoring_with_TESS_v1.pdf (saved with `_flow.txt`), and the "TESS Photometer Manual", version 4.1, September 2026 (L. García, J. Zamorano, C. Tapia), fetched from https://guaix.fis.ucm.es/~jaz/TESS/v4_TESS-W_manual_english.pdf (saved `src3/tessw_manual_v4_english.pdf` and `_flow.txt`). A search of both extracted texts for aging, ageing, drift, degrad, recalib and stability found nothing. Caution: both are slide-like documents and some of their text may be in pictures, which the search does not reach; the manual's extracted text is only 12 kB.

Searches run for this question: three web searches (TESS-W with ageing, drift, sensitivity loss, twilight calibration, dichroic filter degradation) and the arXiv listing for abstracts holding "TESS-W" (no entries). So the honest statement is: as of 27 November 2026 I found no published ageing rate for the TESS-W; the latest refereed statement is Alarcon and others 2021, which saw none in its solar-minimum records and asked for further work.

---

## What I could not open

- **Walker 1988**, PASP 100, 496 (title as listed in another paper's references: "The effect of solar activity on the V and B band sky brightness"). The ADS scan service answered HTTP 500 at one address and HTTP 202 with an empty body at two others (it looks like a challenge to automated clients); I did not pursue it. Not tried at the publisher. Known here only from Patat 2003, Patat 2008, Noll 2012, Krisciunas 1997 and Krisciunas 2007, which do not agree on its size (about 0.5 mag in one citation, 0.8 to 1.0 in two others). Its slope per unit flux is not quoted by any of them.
- **Mattila and others 1996** (La Silla) and **Leinert and others 1995** (Calar Alto), both A&A Supplement Series: the journal site (aas.aanda.org) answered HTTP 403 with a page asking for JavaScript from a captcha service. Not pursued; no open repository copy looked for beyond the one search. Known from Patat 2003 ("Similar values were found by"), Patat 2008 ("similar values are reported by") and Noll 2012 ("About 0.5 mag are reported by Mattila et al. (1996) for blue wavelengths").
- **Leinert and others 1998** at the journal site: the same refusal. Read from the HAL repository copy instead.
- **Krisciunas 1997** as printed in PASP: the ADS scan failed as for Walker. Read from the arXiv preprint instead; the printed version may differ in small ways.
- **Grauer, Grauer, Davies and Davies 2019**, PASP 131, 114508: not opened (as in the earlier scout). Cited by the Barentine abstract for the solar-cycle variation of natural sky brightness.
- **Hart 2019**, PASP 131, 015003 (airglow in Sloan survey spectra): seen only in a search listing; not opened and not used.
- **A full paper behind the Barentine abstract**: one search, none found.
- **Li and others 2026**, arXiv:2607.01923 (near-infrared sky at Dome A, said in a search summary to be brighter near the 2024 maximum): seen only in the search summary; near-infrared and polar, so not opened.

---

## Things to be careful not to claim

1. **Not "the first sight of cycle 25 in zenith photometers".** The Barentine abstract (three SQM-L sites, about 0.5 mag) is in print, and the Oregon report expected the rise in 2023. What I did not find is a refereed paper, a TESS-W result, or a slope against 10.7 cm flux for cycle 25.
2. **Not "nobody has corrected one record for both ageing and the Sun".** The Oregon report did, with fixed outside values. The narrower claim that survives my search is that nobody has printed a joint fit of both terms to the same record. Say "I found none", not "there is none": this was a search of under half an hour, the grey literature (network reports, conference abstracts) is where both nearest hits came from, and I have not searched it thoroughly.
3. **Not "agrees with the published slope", as if there were one.** In V-like bands the printed values run from 0.17 to 0.5 mag per 100 sfu, a factor of three, and the only SQM value (0.5) rests on three yearly means on one side of one cycle, where drift and Sun cannot be separated. Name the source you agree with and the one you do not.
4. **Not a slope in magnitudes without its baseline.** The physical law in the sources is additive brightness (Krisciunas fits in nanoLamberts). A slope in magnitudes shrinks at a brighter site, in a wider beam with more starlight, and at higher flux. If your fit is linear in magnitude, say so, and expect town stations to show a smaller magnitude slope for the same airglow.
5. **Not "0.5 mag in B and V over a cycle" as a measured constant.** It is a round figure passed along from Walker 1988, which I could not open and which is cited for 0.5 by some and 0.8 to 1.0 by others. The directly readable ranges are 0.3 (Paranal V), 0.4 ± 0.1 (La Palma) and 0.6 (Mauna Kea V).
6. **Not "the green oxygen line" as the cause.** The broad visual band is mostly continuum. The 2012 Paranal model has that continuum following the Sun as strongly as the oxygen lines; the 2025 model from the same group has it nearly flat (9 percent per 100 sfu) and calls the older value unexpected. Which emission carries a broad-band solar term is unsettled in print.
7. **Not that the SQM and the TESS-W should give the same solar slope.** Their bands differ (to 650 nm against 740 nm), and the extra red holds both the most Sun-sensitive lines (630 and 636 nm) and the least (OH).
8. **Not that the 10.7 cm flux is the driver.** It is a stand-in for the Sun's extreme ultraviolet output. Grauer and Grauer 2021 show large brightness changes at constant flux; the Barentine abstract ties bright episodes to the solar wind and the interplanetary field. A flux term will absorb whatever else rose with the cycle.
9. **Not that a daily flux value is the right regressor.** The sources that tested it prefer averages over weeks (Patat 2008, Noll 2025) or a lag of days (Krisciunas 2007), and Patat 2003 found the previous day's flux useless. Say which average you used; if only one was tried, say that too.
10. **Not a TESS-W ageing rate "confirming" or "contradicting" a published one.** There is none to compare with. The SQM rates (0.02 to 0.06 mag a year in the earlier report) are for a different filter and housing.
11. **Not that the twilight ageing papers "missed" the Sun.** Their method does not need a solar term. What can be said is that they did not test the night-time residual against solar flux at dark sites.
12. **Mind the direction words when quoting.** Plauchu-Frayn's "NSB has decreased" and Patat's "sky brightness decreased" mean darker; the Barentine abstract's "NSB increase" means brighter; Grauer and Grauer's "increase of -0.41 mag" means brighter; Bará's and Puschnig's "darkening" is a rise in the magnitude number.
