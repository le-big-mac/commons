# Scout report: zenith twilight brightness, multiple scattering, volcanic haze, the TESS-W ceiling, and the Hunga haze at southern middle latitudes

Search began 23:56:44 UTC on 27 November 2026 and this file was assembled at 00:20 UTC on 28 November 2026, inside the 40 minutes allowed. Questions 3 and 4 were searched in parallel with questions 1 and 2. Saved copies of everything relied on are in `/home/agent1/night/lit/src5/` (files for questions 3 and 4 carry the prefixes `q3_` and `q4_`); a few sources saved by the earlier search are cited from `/home/agent1/night/lit/src4/`. Nothing downloaded was run. Numbers are table values, sentences, or readings from plotted curves, and each says which. Where a number is from memory it says so.

The shortest statement of what was and was not found:

- Question 1: published single-scattering shares at the zenith exist for the Sun on the horizon (tables and a model figure), one value at 96 degrees read from a figure (about 0.44 at 540 nm), one old computed table (0.65, 0.36, 0.027, 0.023 at depressions of 4, 6, 10, 14 degrees at 0.58 micrometres), and sentences that the multiple-scattering share reaches practically 100 percent at 98 to 99 degrees. No full-model curve of the share from 96 to 102 degrees was found.
- Question 2: the Pinatubo "second purple light" curve was read from the figure: brighter than the pre-eruption curve by a factor of about 2 at 96 to 97 degrees, rising to about 10 at 100 to 102 degrees, at 713 nm and 60 degrees from the zenith (not the zenith). The body of Coulson 1983 could not be read; its abstract gives no elevations or amounts.
- Question 3: the value 50000 is written by the firmware as an out-of-range mark, not measured; the makers assert linearity by citing the sensor datasheet, whose nonlinearity figure covers 0 to 10 kHz only.
- Question 4: optical depths, heights and sizes are given below, nearly all the mid-2022 optical depths being figure readings; two satellite retrievals disagree by nearly a factor of two in mid-2022.

## Question 1. Share of the zenith twilight light that has been scattered more than once, against the Sun's depression (no volcanic haze, visible light)

How the sources were read. PDFs were fetched with a plain client name and converted with `pdftotext -layout`; figures were read from page images rendered with `pdftoppm`. Files are in `/home/agent1/night/lit/src5/` unless marked `src4/`. Two of the older files are two-column layouts or scans: quotations from them were put together by hand from the column text and, for the one table that matters (1.7), checked against the page image. "Depression" h and solar zenith angle z0 are related by z0 = 90° + h. Shares are given as the source gives them: some give the single-scattering share, some the multiple-scattering share; I have not converted one into the other except where marked "my arithmetic".

What the sources give, in one view (each line is traced below):

| solar zenith angle | single-scattering share at the zenith | band | kind of value | source |
|---|---|---|---|---|
| 90° | 0.587 to 0.705 (12 twilights) | V | table | 1.1 |
| 90° | 0.530 to 0.672 (7 twilights) | B | table | 1.1 |
| 90° | 0.388 to 0.441 (356 nm), 0.432 (U), 0.818 (R, one evening, starred as uncertain) | | table | 1.1 |
| 90° | model lines about 0.63 to 0.68 with aerosol, about 0.85 pure Rayleigh | 550 nm | read from figure | 1.3 |
| 90° to 94-95° | "about 0.6" (0.57 to 0.64, five twilights), "almost constant" | 525 nm | sentence | 1.4 |
| 94° | 0.65 | 0.58 µm | table (computed) | 1.7 |
| 96° | about 0.44 | 540 nm, 90 nm wide | read from figure | 1.6 |
| 96° | 0.36 | 0.58 µm | table (computed) | 1.7 |
| 98-99° | multiple scattering "practically reaching 100%" | visible | sentence | 1.4 |
| 99° to 100° | "totally dominated by multiple scattering" | | sentence | 1.5 |
| 100° | 0.027 | 0.58 µm | table (computed) | 1.7 |
| 104° | 0.023 | 0.58 µm | table (computed) | 1.7 |

At 96° the two numbers found (about 0.44 from polarimetry in 2014, 0.36 computed in the 1960s) differ; both are given. I found no table or curve of the share at 97°, 98°, 101° or 102° for the zenith in visible light, and no Monte Carlo curve of the share against solar zenith angle beyond 96° for a clean atmosphere at the zenith.

### 1.1 Ugolnikov and Maslov 2002 (polarimetry, 356 nm and U, B, V, R)

O. S. Ugolnikov (printed "Ougolnikov"), I. A. Maslov, "Multi-Color Polarimetry of the Twilight Sky. The Role of Multiple Scattering as the Function of Wavelength", Cosmic Research 40, 224 (2002); read as arXiv:physics/0112090. Fetched: https://arxiv.org/pdf/physics/0112090 . Saved: `arxiv_physics_0112090.pdf`, `.txt`.

Table 1, "The single scattering contribution at z=h=0 for 1997 and 2000 observation dates" (z = zenith distance of the point looked at, h = depth of the Sun, so this is the zenith at sunrise or sunset). The column AT is the share "for total sky background"; "The star symbol (*) near these values means their possible inaccuracy". Table values of AT:

- 356 nm (1997): 0.441*, 0.413, 0.388
- U (17.VII.2000, evening): 0.432
- B (2000, seven twilights): 0.530, 0.565, 0.624*, 0.624, 0.672, 0.639, 0.635*
- V (2000, twelve twilights): 0.587, 0.587, 0.670, 0.705, 0.702, 0.682*, 0.700, 0.676*, 0.645, 0.676*, 0.639, 0.673
- R (4.VIII.2000, evening): 0.818*; the three other R evenings are left blank in the table.

Sentences:

> "As we can see from the table, at z=h=0 single scattering contains less than the half of total sky background brightness in a violet part of spectrum but with increase of wavelength its contribution becomes more sufficient and can reach 70% in a green-yellow part of spectrum."

> "This ratio remains almost constant until the depth of the sun under horizon about 4-5°, then the role of single scattering rapidly decreases"

> "At h about 10° single-scattered light completely disappears on the multiple-scattered background."

For the red they write that the value "is expected to be not less than 80%". For a point 60° from the zenith in the glow region they write that "multiple scattering is completely dominant for z=60° (in the glow region) at h>10°. Correspondingly, this situation occurs earlier at the zenith region".

No table of the share against h is given for the zenith in the visible bands; Figure 11 of the paper plots the Rayleigh single-scattering share against h for 356 nm only (31.VII.1997), which I did not read.

### 1.2 Postylyakov, Ugolnikov, Maslov and Masleev 2003 (polarimetry compared with the Monte Carlo code MCC++)

O. V. Postylyakov, O. S. Ugolnikov, I. A. Maslov, A. N. Masleev, "Polarization of the Twilight Sky: Measurements, Empirical Model, Radiative Transfer Simulation and Application to Aerosol Profile Retrieval", arXiv:physics/0306070 (where else it was printed is not stated in the saved copy as far as I read). Fetched: https://arxiv.org/pdf/physics/0306070 . Saved: `arxiv_physics_0306070.pdf`, `.txt`.

> "The percentage of single scattered light at the zenith during twilight is equal to about 40% for 360 nm, 60% for 440, 70% for 550 nm and reaches 80% for 700 nm, what confirmed by both the semi-empirical model based on the measurements, and the radiative transfer calculations."

> "These percentages remain almost constant until the sun’s depth under horizon 4-5°, when the part of single scattering rapidly decreases, and the sky polarization falls. At the sun’s depth about 10° single scattered light completely disappears on the multiple scattered background."

Limits of the model run: "Calculations were carried out for the solar zenith angle up to 96° at wavelengths equal to 360, 440, 550, 700, 800 nm." (read from the page image of page 4). Their Figure 4 gives the share against wavelength at "Solar zenith angle is equal to 90°" only.

### 1.3 Ugolnikov, Postylyakov and Maslov 2004 (the same comparison; the figure read here)

O. S. Ugolnikov, O. V. Postylyakov, I. A. Maslov, "Effects of Aerosol and Multiple Scattering on the Polarization of the Twilight Sky", arXiv:physics/0311007. (Printed in J. Quant. Spectrosc. Radiat. Transfer; the volume and page, 88, 233, 2004, are from memory and not checked against a saved copy.) Fetched: https://arxiv.org/pdf/physics/0311007 . Saved: `arxiv_physics_0311007.pdf`, `.txt`.

Model: "Monte-Carlo linear radiation transfer model MCC++", "taking into account all orders of scattering"; "Calculations were carried out for the solar depressions under horizon up to 6° for the same wavelengths where 2000-2003 observations were made: 360, 440, 550 and 700 nm."; "Lambertian surface albedo was assumed to be equal to 0.5."; aerosol models "urban, continental and maritime types of aerosol from 0 to 10 km and stratospheric aerosol above 10 km".

Figure 2, "The contribution of single scattering in the twilight sky background at the zenith at the moment of sunrise (sunset) obtained by the observational method (dots) and radiation transfer simulation (lines)." Read from the figure (enlarged page image; each reading good to about 0.02):

| J1/J at the zenith, Sun on the horizon | 360 nm | 440 nm | 550 nm | 700 nm |
|---|---|---|---|---|
| model, pure Rayleigh | 0.52 | 0.70 | 0.85 | 0.93 |
| model, urban aerosol | 0.38 | 0.54 | 0.68 | 0.78 |
| model, continental aerosol | 0.37 | 0.51 | 0.63 | 0.72 |
| model, maritime aerosol | 0.36 | 0.50 | 0.63 | 0.67 |
| observational method (dots) | 0.39 to 0.44 | 0.53 to 0.67 | 0.59 to 0.70 | 0.82 (one dot) |

Sentences on what happens after sunset, V band (550 nm), zenith:

> "From the sunset until the sun depression about 5° the polarization is almost constant, then it begins to decrease and after the Sun depression about 9° in the moonless sky the polarization becomes constant again"

> "almost constant at light period of twilight, then the contribution of single scattering is decreasing completely vanishing at the Sun depression about 9°."

The paper plots the model's polarization against depression (Figures 3, 4) but not the model's single-scattering share against depression.

### 1.4 Ugolnikov and Maslov 2007 (a summary in sentences, and five more measured values)

O. S. Ugolnikov, I. A. Maslov, "Detection of Leonids meteoric dust in the upper atmosphere by polarization measurements of the twilight sky", arXiv:astro-ph/0612586 (journal reference not in the part of the saved copy I read). Fetched: https://arxiv.org/pdf/astro-ph/0612586 . Saved: `arxiv_astro-ph_0612586.pdf`, `.txt`. Instrument band "with effective wavelength 525 nm", zenith.

> "the multiple scattering contribution near the sunrise (or sunset) rises from about 30% in the red spectral region up to 60% in violet one in the case of stable clear skies. Being almost constant until the solar zenith angle 94-95°, the multiple scattering contribution increases after that, practically reaching 100% at the solar zenith angle 98-99°. These results were confirmed by the numerical solution of radiative transfer equation made by vector code MCC++ (Postylyakov, 2004)."

> "Light twilight, SZA from 90-91° to 94-95° ... The intensity contribution of single scattering for the instrumental spectral band is about 0.6 (0.59 in the evening of November, 21, 0.60 and 0.57 in the morning and evening of November, 27, respectively, 0.64 for the morning of November, 30 and for the basic reference morning twilight of December, 11)."

The same paper says of the older literature that the multiple-scattering share "was sufficiently underestimated later, during the dark twilight period with solar zenith angle SZA>95°, when multiple scattering starts to take over the single scattering" (its reference there is Rozenberg 1966).

### 1.5 Ugolnikov and Maslov 2011 (the stages, zenith)

O. S. Ugolnikov, I. A. Maslov, "Undisturbed Mesosphere Optical Properties from Wide-Angle Frequent Twilight Sky Polarimetry", arXiv:1108.2827. Fetched: https://arxiv.org/pdf/1108.2827 . Saved: `arxiv_1108.2827.pdf`, `.txt`. Evening of 1 June (2011), central Russia; the band was not looked up.

> "light twilight (z0 from 93° to 95°) with maximal polarization and almost constant ratio of single and multiple scattering; transitive twilight (z0 from 95° to 99°), when the polarization falls due to decrease of single scattering contribution; dark twilight (z0 from 99° to 100°) totally dominated by multiple scattering with constant polarization and, finally, nightfall (z0 more than 100°) when polarization decreases due to the night sky background contribution."

### 1.6 Ugolnikov, Maslov and Kozelov 2017 (a value at 96°, read from a figure)

O. S. Ugolnikov, I. A. Maslov, B. V. Kozelov, "Detection of Molecular Scattering Field by Polarization Analysis of Sky Background During the Transitive Twilight and Temperature Measurements near the Stratopause", arXiv:1711.08170. Fetched: https://arxiv.org/pdf/1711.08170 . Saved: `arxiv_1711.08170.pdf`, `.txt`. Camera near Moscow, band "effective wavelength 540 nm and FWHM 90 nm".

Figure 3, "Intensity and polarization of sky background and its components in solar vertical at solar zenith angle 96° (effective shadow altitude in the zenith 50 km), the same twilight as in Figure 1" (evening of 31 May 2014). A dashed curve labelled "J/I" (J = single scattering, I = total) is drawn against the left-hand axis, which runs from -0.2 to 1.0. Read from the figure (good to about 0.02; I take the left axis because a ratio cannot be read on the right-hand intensity axis, the figure itself does not say):

| point in the solar vertical | J/I at solar zenith angle 96° |
|---|---|
| zenith | about 0.44 |
| 55° from the zenith, away from the Sun | about 0.35 |
| 55° from the zenith, towards the Sun | about 0.61 |

Sentences:

> "multiple scattering contribution is high even at sunset, reaching 50% in blue part of spectrum."

> "single scattering vanishes on the multiple scattered background when the effective altitude of single scattering reaches 90 km. In the zenith point this corresponds the solar depression under the horizon at 9° [21]."

> "When solar zenith angle reaches 99°, the fall of sky polarization gets slower (or stops for a little time if the night sky background is weak). This corresponds to the dark stage of twilight when single scattering vanishes on the less polarized multiple scattering background."

### 1.7 Divari, Zaginayilo and Kovalchuk 1973 (a printed table of the share against depression, computed in the 1960s)

N. B. Divari, Y. I. Zaginayilo, L. V. Kovalchuk, "Optical Properties of Atmospheric Dust From Twilight Observations", paper 28 in the volume "Evolutionary and Physical Properties of Meteoroids", pages 281 and following (a NASA volume; its series number and year, SP-319, 1973, are from memory, not read from the saved copy). Fetched: https://ntrs.nasa.gov/api/citations/19740011351/downloads/19740011351.pdf . Saved: `ntrs_19740011351.pdf`, `.txt`. A scan; the table was read from the page image, not from the text layer.

"Table 2.—Values of Coefficient K1 = B1/(B1+B2) Used for the Wavelengths λ = 0.37 and λ = 0.58 µ (Transmission Coefficients p = 0.59 and p = 0.89) and Computed According to the Data of Divari and Plotnikova (1965) for A = 0°". B1 is the "primary brightness" and B2 the "secondary one"; g is the Sun's depression ("g = z − 90°, where z is the zenith distance of the Sun"). Row for the zenith (z = 0), table values:

| depression g | 4° | 6° | 10° | 14° |
|---|---|---|---|---|
| λ = 0.37 µ, p = 0.59 | 0.63 | 0.47 | 1.6 × 10⁻² | 1.5 × 10⁻² |
| λ = 0.58 µ, p = 0.89 | 0.65 | 0.36 | 2.7 × 10⁻² | 2.3 × 10⁻² |

The table also has rows for points 20° to 80° from the zenith on both sides. The authors' own caution: these values "may be considered only as a first approximation." The underlying computation (Divari and Plotnikova 1965) was not obtained; the scanned-article server refused the request.

### 1.8 Patat, Ugolnikov and Postylyakov 2006 (where a single-scattering model leaves the measurements; sentences not in the earlier notes)

Reference and address as in the earlier notes; file `src4/arxiv_astro-ph_0604128_flow.txt`. Paranal, zenith, UBVRI.

> "As expected, the single scatter model drops much faster than the actual observations. Whilst for VRI the model deviates from the data around ζ ∼97◦ , for B and especially for U the model underestimates the surface brightness already at ζ ≤96◦ , indicating that multiple scattering is more efficient at shorter wavelengths."

> "the contribution of single scattering in the phases immediately following sunset is about 40%, 60%, 70% and 80% in U, B, V and R respectively. These fractions remain roughly constant until ζ ≤95◦ , after which the role of single scattering becomes weaker and weaker and multiple scattering takes rapidly over."

(The second is their report of Ugolnikov and Maslov 2002, not a new measurement. The quotation is broken by a page of figure captions in the text file.) I did not read the ratio of data to single-scattering model from their Figures 3 to 7.

### 1.9 Mateshvili and others 2013 (Monte Carlo, 780 nm, not the zenith)

Reference and address as in the earlier notes; file `src4/mateshvili2013_amt-6-2563-2013.pdf`. Monte Carlo code Siro, "at 780 nm", for their viewing direction (their Table 1: 40 to 50° from the zenith), "number of photons was 10^6", repeated 10 times. Figure 5a plots the "multiple scattering correction factor", "the modelled averaged ratio ... between the total light intensity I and the single scattering Iss component", for solar zenith angles 86° to 95° only. Case 1 is a profile "typical for volcanically quiet" conditions, case 2 "volcanically disturbed". Read from the figure (enlarged; good to about 0.05, worse on the steep part beyond 94°):

| solar zenith angle | 88° | 90° | 92° | 93° | 94° | 95° |
|---|---|---|---|---|---|---|
| I/Iss, case 1 (quiet) | 1.13 | 1.15 | 1.20 | 1.25 | 1.4 | 1.75 |
| I/Iss, case 2 (disturbed) | 1.43 | 1.5 | 1.5 | 1.55 | 1.9 | 2.75 (dashed bounds 2.5 to 3.0) |

My arithmetic, not the source's: a factor of 1.15 means a multiple-scattering share of 13 percent, 1.75 means 43 percent, 2.75 means 64 percent.

> "Figure 5a also shows that single scattering plays a dominant role in the SZA range 88–94◦ . However, the relative multiple scattering contribution depends on the aerosol loading."

These shares at 780 nm are lower than the red-light figures of 1.1 to 1.4 (20 to 30 percent multiple at sunset); the wavelength, the viewing direction and the method all differ.

### 1.10 Wu and Lu 1988 (abstract only)

Wu Beiying, Lu Daren, "Simulation of the intensity and polarization of skylight during twilight period", Advances in Atmospheric Sciences, February 1988 (volume and pages not read). Fetched: https://link.springer.com/article/10.1007/BF02657342 . Saved: `springer_BF02657342.html`. The full text is behind a subscription; abstract only.

> "Monte-Carlo method is applied to simulate the intensities and degrees of polarization in twilight sky after the eruption of the El Chichon volcano and during the 1977 volcanically quiet period, respectively. The results coincide well with the observations. It is found that the significance of multiple scattering is completely different in these two periods"

No figures are given in the abstract.

## Question 2. How a layer of stratospheric haze changes the zenith brightness in twilight, against the Sun's depression

### 2a. Mateshvili and others 2013: the "second purple light" after Pinatubo

Reference, address and file as in the earlier notes (`src4/mateshvili2013_amt-6-2563-2013.pdf`, `_flow.txt`). What the earlier notes did not extract:

What was measured. Their Table 1: a filter photometer, "713 ± 2.5 nm", field 1°, 60° from the zenith, at Abastumani, November 1991. So this is not the zenith. Figure 14 shows "The measured pre-Pinatubo (black dashed line) and post-Pinatubo (8 November 1991, red dashed line) twilight curves", as log10 of radiance against solar zenith angle from 90° to about 107°. The date of the pre-Pinatubo curve is not given in the caption or in the text I searched.

Read from Figure 14 (rendered at 330 dots per inch; curve positions measured in the image with a small script and the dashed curves told from the solid ones by their gaps; each curve good to about 0.05 in the logarithm, so each difference to about 0.1):

| solar zenith angle | post-Pinatubo, log10 radiance | pre-Pinatubo, log10 radiance | difference | as a factor (my arithmetic) |
|---|---|---|---|---|
| 94° | -0.29 | -0.52 | +0.23 | 1.7 |
| 95° | -0.92 | -1.14 | +0.22 | 1.7 |
| 96° | -1.39 | -1.64 | +0.25 | 1.8 |
| 97° | -1.72 | -2.07 | +0.35 | 2.2 |
| 98° | -1.97 | -2.52 | +0.55 | 3.5 |
| 99° | -2.15 | -2.95 | +0.80 | 6 |
| 100° | -2.40 | -3.35 | +0.95 | 9 |
| 101° | -2.70 | -3.76 | +1.06 | 11 |
| 102° | -3.12 | -4.21 | +1.09 | 12 |
| 103° | -3.60 | -4.48 | +0.88 | 8 |
| 104° | -4.00 | -4.75 | +0.75 | 6 |
| 105° | -4.32 | -4.89 | +0.57 | 4 |

(Units on the axis: mW/(m² nm). At 99° to 101° the measured and one modelled red curve lie on top of each other, so the post-Pinatubo readings there are the least sure. Beyond about 103° both measured curves flatten towards the night level.) The paper itself states no factor; in words it says "a twilight sky brightness enhancement at large SZAs of 97–102◦ (Fig. 14, red dashed line)".

What was modelled (Monte Carlo code Siro), and how much haze. Three model curves for three aerosol profiles (Figure 15):

- The profile retrieved from the measured curve: "There is no second purple light signature on the modelled curve; it is very close to the twilight curve measured in the background conditions (black dashed)."
- A profile modified low down (blue): "At larger SZAs the twilight sky brightnesses are higher than ones calculated using the unmodified aerosol profile, showing weak second purple light signature."
- A "strongly modified" profile (red): "The second purple light is prominent, but the modelled curve does not fit well the measured one at small SZAs."

Read from Figure 15 (logarithmic axis, page image at 110 dots per inch; rough): the retrieved profile has extinction near 10⁻² km⁻¹ between about 20 and 25 km, falling steeply above 25 km, and about 2 to 5 × 10⁻³ km⁻¹ between about 12 and 18 km. The "strongly modified" profile sets the extinction to about 10⁻⁴ km⁻¹ from about 7.5 km up to about 18.5 km; the blue one does so from about 7 to about 10.5 km only. The paper gives no optical depth for the 8 November 1991 layer in the text I searched. (My arithmetic from the figure reading, very rough: 10⁻² km⁻¹ over 5 km is 0.05 at 713 nm.)

The authors' condition: "The necessary condition to observe the “second purple light” is a high transparency zone below the SAL." And their caution: "A limitation of our model seems to be the reason why the same aerosol profile does not fit both the first and the second purple lights."

Orders of scattering in the "strongly modified" model, read from Figure 16 (same method; good to about 0.05 in the logarithm):

| solar zenith angle | total | 1st order | 2nd order | 3rd order | 1st order as a share of the total (my arithmetic) |
|---|---|---|---|---|---|
| 94° | 0.09 | -0.21 | -0.38 | about -0.9 (by eye) | 50 % |
| 95° | -0.70 | -2.17 | -1.00 | -1.24 | 3 % |
| 96° | -1.10 | -2.67 | -1.47 | -1.50 | 3 % |
| 97° | -1.54 | -3.23 | -1.94 | -2.00 | 2 % |
| 98° | -1.84 | -3.95 | -2.17 | -2.39 | 0.8 % |
| 99° | -2.11 | -5.14 | -2.46 | -2.58 | 0.1 % |
| 100° | -2.38 | below the axis (under -6.4) | -2.75 | -2.91 | |
| 101° | -2.71 | | -3.13 | -3.27 | |
| 102° | -3.25 | | -4.16 | -3.69 | |

This is for a heavy volcanic layer with an artificially clear zone under it, 60° from the zenith, at 713 nm; it is not an ordinary twilight and not the zenith.

The earlier paper on the same measurements, abstract only: N. Mateshvili, D. Fussen, F. Vanhellemont, C. Bingen, E. Kyrölä, I. Mateshvili, G. Mateshvili 2005, "Twilight sky brightness measurements as a useful tool for stratospheric aerosol investigations", J. Geophys. Res. 110, doi:10.1029/2004JD005512. Fetched (a reference-database record carrying the abstract): https://earthref.org/ERR/86415 . Saved: `earthref_ERR_86415.html`. "The twilight sky brightness was measured at 9 wavelengths (422, 474, 496, 542, 610, 642, 678, 713, and 820 nm) for solar zenith angles from 89" to 107 degrees; "There are clear indications of a growth of the stratospheric aerosol layer after the eruption of Mount Pinatubo that manifests itself by humps in twilight sky brightness dependences versus solar zenith angle." The full text (which would hold the curves at 542 nm and the other visible wavelengths) was not fetched; the publisher refuses automated clients.

### 2b. Coulson 1983 on El Chichón

Still abstract only. The full text at the publisher is not openly readable, and I found no open copy. From the saved abstract (`src4/coulson1983_optica_abstract.txt`), words the earlier notes did not quote:

> "It is shown here that the magnitude of the skylight intensity is modified very significantly from its clear sky value by the volcanic cloud, as is its change with solar depression angle during twilight and its distribution over the sky during the day. Emphasis is on measurements at a wavelength of 0.07 μm."

("0.07 μm" is what the page prints.) The abstract gives no Sun elevations, no amounts, and mentions a brightening only for the daytime sky ("a considerable enhancement of intensity over the sky throughout the main part of the day"), not in twilight. So: at which depressions the zenith was dimmer, and by how much, I could not find.

Looked for the numbers in the observatory's own annual reports, which are open:

- "Geophysical Monitoring for Climatic Change No. 11, Summary Report 1982" (NOAA Environmental Research Laboratories). Fetched: https://gml.noaa.gov/publications/summary_reports/summary_report_11.pdf . Saved: `gmcc1982_summary.pdf`, `.txt` (a scan; the text layer has spelling damage, repaired in the quotation). "It was found that the cloud had particularly pronounced effects on the polarization field, although the skylight intensity also changed significantly. ... The results have been described by Coulson (1983a, 1983b)". Its section 4.5, "Measurements of Skylight Polarization at MLO", gives twilight curves of polarization at 700 nm only (Figures 56, 57), no intensity curve. It does give heights: on 11 April 1982 "The cloud top, however, was restricted at that time to an altitude of about 26 km"; "By 14 May, the cloud top had risen to at least 35 km".
- "Summary Report 1983" (No. 12). Fetched: https://gml.noaa.gov/publications/summary_reports/summary_report_12.pdf . Saved: `gmcc1983_summary.pdf`, `.txt`. Searched for "Coulson", "twilight", "zenith": no twilight intensity results.

The saved abstract page lists two earlier papers by the same author that I did not open and that may hold the clear-sky curves he compared with: "Characteristics of skylight at the zenith during twilight as indicators of atmospheric turbidity. 1: Degree of polarization" and "2: Intensity and color ratio"; and one by another author, "Volcanic turbidity, skylight scattering functions, sky polarization, and twilights in New England during 1983".

### 2c. Other sources

Ashok, Bhatt, Chandrasekhar and Desai 1982 (El Chichón, near infrared, a brightening; abstract only). N. M. Ashok, H. C. Bhatt, T. Chandrasekhar, J. N. Desai, "Twilight IR brightening over India due to El Chichón's eruption in Mexico", Nature 300, 620 (December 1982). Fetched: https://www.nature.com/articles/300620a0 (the PDF address returned no PDF to an automated client). Saved: `nature_300620a0_page.html`.

> "Approximately 8 min after sunset the sky brightness increases with time for about 8–10 min in the I band (γeff = 0.87 µm). This may be explained by a variation in the extinction of the illuminating solar radiation during its passage through the aerosol layer before being scattered into the observer's line of sight. Here, we estimate a mean height of 22 km, a thickness of 10 km and a drift speed of 19 km h−1 for the layer over Ahmedabad in June 1982."

The abstract does not say where in the sky the instrument pointed, gives no solar depression in degrees and no size of the brightening.

Wu and Lu 1988 (El Chichón against 1977, Monte Carlo; abstract only): see 1.10. It says intensities were simulated for both periods and that multiple scattering mattered differently in the two; no numbers in the abstract.

Ugolnikov and Maslov 2021 (Raikoke 2019): the journal version of the preprint already in the earlier notes is O. S. Ugolnikov, I. A. Maslov, "Postvolcanic Aerosols: Measurements of Altitude and Particle Sizes with Twilight-Sky Polarimetry", Cosmic Research 59, 89 (March 2021). Fetched: https://link.springer.com/article/10.1134/S0010952521020076 . Saved: `springer_S0010952521020076.html`. Abstract: "The increase in brightness paired with the decrease in polarization was registered, and the changes were especially noticeable in the dusk segment"; "the aerosols were mostly concentrated in the upper troposphere and near the tropopause rather than in the stratosphere." No brightness ratio at stated depressions in the abstract.

Adams, Plass and Kattawar 1973 (a model with more and less aerosol, single scattering only). C. N. Adams, G. N. Plass, G. W. Kattawar, "The Influence of Ozone and Aerosols on the Brightness and Color of the Twilight Zone" [so on the title page of the report], Report No. 7, Texas A&M University, NASA contract report. Fetched: https://ntrs.nasa.gov/api/citations/19730020661/downloads/19730020661.pdf . Saved: `ntrs_19730020661.pdf`, `.txt`. "The radiance and color of the twilight sky are calculated for single scattered radiation"; models with "aerosol concentrations of 1, 3, and 10 times normal" at all altitudes (not a separate stratospheric layer), for solar zenith angles 90°, 92°, 94° and 96°. The authors say of the heavy-aerosol model: "Multiple scattering effects would be especially important for the larger optical depths of this model." Its radiance figures were not read; being single-scattering only, it cannot answer the question for depressions where multiple scattering dominates.

Mateshvili and others 2013, Figure 5a (see 1.9) is also an answer of a kind for the bright end: at 780 nm, 40 to 50° from the zenith, the ratio of total to single-scattered light at 95° is about 2.75 with the volcanically disturbed profile against about 1.75 with the quiet one. It gives the ratio within each case, not the brightness of one case against the other.

### What I looked for under Questions 1 and 2 and did not find

- A Monte Carlo or other full radiative-transfer curve of the multiple-scattering share at the zenith against solar zenith angle from 96° to 102° in visible light for a clean atmosphere. The MCC++ runs in the papers read stop at 96° and are shown as a share only at 90°.
- G. V. Rozenberg, "Twilight: A Study in Atmospheric Optics" (1966): no open copy found; known here only through the citing papers, which say it underestimated the multiple-scattering share.
- O. S. Ugolnikov 1999, Cosmic Research 37, 159 (356 nm), and O. V. Postylyakov 2004, J. Quant. Spectrosc. Radiat. Transfer 88, 297 (the MCC++ paper): cited in the papers read; not found in open form.
- W. G. Blättner, H. G. Horak, D. G. Collins, M. B. Wells 1974, "Monte Carlo Studies of the Sky Radiation at Twilight", Applied Optics 13, 534: found only as a citation (a search result gives the reference); not opened, no open copy found.
- N. B. Divari and L. I. Plotnikova 1965/1966, the computation behind 1.7: the scanned-article server refused an automated request.
- Coulson 1983, full text: not openly readable; the Sun elevations and the amount of dimming are not in the abstract or in the two observatory reports.
- Zenith twilight brightness with and without haze at stated depressions for Krakatoa, Agung, El Chichón, Pinatubo or Hunga in visible light: none found as a table or readable curve. What exists in the material read is 60° from the zenith at 713 nm (2a), near infrared (Ashok 1982; the Hunga sources in the earlier notes), or words without numbers.
- F. E. Volz and R. M. Goody 1962 (J. Atmos. Sci. 19, 385), C. N. Adams and others 1974 (J. Atmos. Sci. 31, 1662, the journal version of the report above), G. M. Shah 1969 (Tellus 21, 636): the journals' sites returned a check page, not the paper, to an automated client; not read. F. E. Volz 1969 (Applied Optics 8, 2505), J. V. Dave and C. L. Mateer 1968 (J. Geophys. Res. 73, 6897), G. E. Shaw 1980 full text, R. L. Lee and J. Hernández-Andrés 2003 on the purple light: not tried in the time.
- Patat and others 2006, Figures 3 to 7 (ratio of measured brightness to the single-scattering model at each zenith angle), and Ugolnikov and Maslov 2002, Figure 11: present in saved files, not read for values.

## Question 3. The TESS-W photometer: its largest count (50,000 Hz) and whether the count is proportional to the light up to that ceiling

All files named below are in `/home/agent1/night/lit/src5/`. PDFs were read with `pdftotext -layout`; web pages were turned to text with a small script of my own; source code was saved as text and read, never run. One image-only poster was rendered to a picture and read by eye. Spanish quotations are followed by my own translation in brackets.

What the sources say, in brief (each point is traced below):

- The 50,000 Hz value is in the published firmware, where it is a mark and not a measured frequency: in firmware versions 2.0 and 3.2 for the TESS-W's WiFi module, when the sensor's own microcontroller reports "out of range", the WiFi module sets the frequency to 50000 and the magnitude to 0.
- The firmware author's note for the sensor microcontroller says it reads the sensor frequency "between 0.01 Hz and 50KHz". The code beside that note sends real numbers up to 65,000 Hz and the out-of-range mark above that; a comment on the same lines says "f > 60KHz". The three numbers (50, 60, 65 kHz) are all in the one source and disagree.
- The network's database software calls these daytime readings "saturated" and identifies them by magnitude = 0.
- On proportionality: the makers' papers say the sensor's frequency "depends linearly on the irradiance" and is "linear across several decades", citing the sensor datasheet; I found no linearity measurement of a TESS-W by its makers, and none that reaches tens of kHz. The datasheet gives the sensor's own saturation ("full-scale frequency") as MIN 500 kHz, MAX 1000 kHz, and specifies nonlinearity (±1 % of full scale) only for 0 to 10 kHz. The firmware author's bench table for the frequency counter shows 50000 Hz in read as 50078 Hz.

### 3.1 Firmware for the sensor microcontroller ("tess-u"), by the photometer's designer

Reference: C. García, repository "TESS-W (Telescope Encoder & Sky Sensor Wifi). Firmware an documentation", GitHub user cristogg, files `tess-u/Readme.md` and `tess-u/tess-u.c` (header: "version operativa desde 11/04/2014").
Fetched: `https://raw.githubusercontent.com/cristogg/TESS-W/master/tess-u/Readme.md` and `.../tess-u/tess-u.c` (file list from `https://api.github.com/repos/cristogg/TESS-W/git/trees/master?recursive=1`).
Saved: `q3_gh_cristogg_TESS-W_tess-u_Readme.md.txt`, `q3_gh_cristogg_TESS-W_tess-u_tess-u.c.txt`, `q3_gh_cristogg_TESS-W_tree.json`.

Readme, whole relevant sentence:

> "Lee la frecuencia generada por el sensor de brillo entre 0.01 Hz y 50KHz." [It reads the frequency generated by the brightness sensor between 0.01 Hz and 50 kHz.]

Source file, comment above the measuring routine `CuentaTSL()` (lines 594 to 597):

> "//Mide frecuencia en todo el rango. //En funcion de esta f: //si f<50 Hz, se usa Timer0 para medir periodo //si f>50 y f<50000, se cuentan pulsos en 1/2 sg" [Measures frequency over the whole range. Depending on this f: if f<50 Hz, Timer0 is used to measure the period; if f>50 and f<50000, pulses are counted in 1/2 s.]

Same routine, the counting branch and the output (lines 655 to 697), exact code lines:

> `if(TH1== 0xFF) break;	  //evita desbordar contadores` [avoids overflowing the counters]
> `fTSL = 2.0*(float)(auxiT);// doble de pulsos par el sg entero` [twice the pulses, for the whole second]
> `if(fTSL<65000.0) { //si la frecuencia cabe en 5 cifras` [if the frequency fits in 5 digits]
> ... `xprint("<fH ");` ... `auxiT = (word)(fTSL); // pone Hz`
> `else					// f > 60KHz muy alta y no` [f > 60 kHz, very high and not]
> `xprint("<fH-00001");`

So in this file the out-of-range string `<fH-00001` is sent when the computed frequency is not below 65000.0; the comment on that branch says "f > 60KHz"; the Readme and the routine's heading say 50 kHz / 50000. The source does not reconcile these.

Bench table in the header comments of the same file ("Medidas de frecuencia 20-03-2014", "lecturas medias promediando lecutras durante 60sg" [mean readings averaging readings over 60 s]), columns "f IN Hz / f OUT Hz / Mag V estimada", table values as printed (decimal commas as in the source):

| f IN Hz | f OUT Hz | Mag V estimada |
|---|---|---|
| 0,080 | 0,0800 | 23,78 |
| 0,100 | 0,1000 | 23,54 |
| 0,200 | 0,2000 | 22,77 |
| 0,500 | 0,5000 | 21,77 |
| 1 | 1 | 21,01 |
| 2 | 2 | 20,26 |
| 5 | 5,0018 | 19,26 |
| 10 | 10,0048 | 18,50 |
| 20 | 19,975 | 17,74 |
| 50 | 49,841 | 16,75 |
| 100 | 100,0 | 15,99 |
| 200 | 200,0 | 15,23 |
| 500 | 500,0 | 14,23 |
| 1000 | 1002 | 13,47 |
| 2000 | 2003 | 12,74 |
| 5000 | 5007 | 11,72 |
| 10000 | 10015 | 10,96 |
| 20000 | 20031 | 10,20 |
| 50000 | 50078 | 9,20 |

This table is about the counter (a known input frequency against the frequency the microcontroller reports), not about the light sensor. Its last row is 50000 Hz. The source does not say what generated the input frequencies.

Caution on which unit this is: the file header says "uP AT89C51" and the Readme says "AT49S4051"; the file is dated 2014 (the paper describing the TESS-W was received in November 2016, see 3.6b). That the TESS-W's WiFi module talks to such a microcontroller with this same message format is shown by 3.2. I did not find a statement of which build of this code is in the units sold.

### 3.2 Firmware for the TESS-W's WiFi module: where 50000 is written

Reference: same repository, files `tess-w.ino` (earliest, "Arduino 1.6.5"), `tess-w-v2_0/tess-w-v2_0.ino` (release note `tess-w-v2_0/version20`: "TESS-W firmware 2.0 ... 4 de mayo del 2018", signed "Cristobal Garcia"), `tess-w-v32/tess-w-v32.ino` (header: "13/09/2021-----Version 3.2").
Fetched: `https://raw.githubusercontent.com/cristogg/TESS-W/master/` + each path.
Saved: `q3_gh_cristogg_TESS-W_tess-w.ino.txt`, `q3_gh_cristogg_TESS-W_tess-w-v2_0_tess-w-v2_0.ino.txt`, `q3_gh_cristogg_TESS-W_tess-w-v2_0_version20.txt`, `q3_gh_cristogg_TESS-W_tess-w-v32_tess-w-v32.ino.txt`, `q3_gh_cristogg_TESS-W_README.md.txt`.

Version 3.2, lines 1760 to 1773 (the same block is at lines 1661 to 1669 of version 2.0):

> `if(Meteo[2] == 'H') {   // H son hercios, mucha luz` [H is hertz, much light]
> `   if(Meteo[3] != '-'){ //con "-" el micro indica fuera de rango` [with "-" the microcontroller indicates out of range]
> `     Frecuencia =  atoi(Cad.c_str());`
> `     Magnitud = HzToMag(Frecuencia) ;`
> `   }`
> `   else {`
> `     Magnitud = 0;`
> `     Frecuencia =50000;`
> `   }`
> `}`
> `else if (Meteo[2]== 'm') {  //m son milihercios, cielo oscuro` [m is millihertz, dark sky]

An example message in the header comments of version 3.2 (line 20) shows the pair as transmitted:

> `{"seq":15, "rev":2, "name":"pru21", "freq":50000.00, "mag":0.00, "tamb":23.85, "tsky":22.87, ...}`

and the raw string from the sensor microcontroller in the same state is shown in the header comments of the version 4.33.1 file (line 47): `<fH-00001><tA +2385><tO +2287>...`.

A commented-out block a few lines below (version 3.2, lines 1798 to 1810) treats the value the same way: `if (Frecuencia < 50000 ) {` ... display values ... `else {` ... `"--"; //fuera de rango` [out of range].

The earliest file `tess-w.ino` (lines 640 to 651) has the same test but writes zero instead: `Magnitud = 0; Frecuencia =0;`. So the value written for "out of range" changed from 0 to 50000 between the earliest file and version 2.0.

The transmitted frequency is a mean over the strings received in the sending interval, and the 50000 mark is included in that mean: version 3.2 lines 1774 to 1777, `MagnitudM += Magnitud; CuentaRxMag++; FrecuenciaM += Frecuencia; CuentaRxFrecuencia++;`, and lines 749 to 756 (`CalculaMedias`), `F_Frecuencia = FrecuenciaM/CuentaRxFrecuencia;` and `F_Magnitud = MagnitudM /CuentaRxMag;`. The magnitude conversion in version 3.2 (line 1207) is `mv = ConstI - 2.5*log10(HzTSL);` with no correction term other than the constant.

### 3.3 Later firmware (version 4.33.1, ESP32 boards, one or four channels): a different ceiling

Reference: same repository, `tess-w-v4331/tess-w-v4331_DLog.ino` and `tess-w-v4331/cambios.txtr`. Header comments: "24/11/2021 Version 4.0 PCB TESS-W4C", "12/2/2022 Version 4.1 ESP32".
Fetched: `https://raw.githubusercontent.com/cristogg/TESS-W/master/tess-w-v4331/tess-w-v4331_DLog.ino` and `.../cambios.txtr`.
Saved: `q3_gh_cristogg_TESS-W_tess-w-v4331_tess-w-v4331_DLog.ino.txt`, `q3_gh_cristogg_TESS-W_tess-w-v4331_cambios.txtr.txt`.

Here the frequency is timed directly by the WiFi processor (lines 1318 to 1368):

> `if (frec < 100000) {`
> `  frec = 1000000.0/ Tius2;  //frecuencia medida` [measured frequency]
> ... `else {` ... `FrecOver = 4; //inicia 4 sg de espera antes de reactivar ints` [starts a 4 s wait before re-enabling interrupts] `Serial.println("Frec Over: ");`
> ... `if (FrecOver == 0) {` `//frec = 0;` `frec = 90000;`
> `Magnitud = ZP1 -2.5*log10(frec);`
> `if (Magnitud < 5) Magnitud = 0;`
> `  else if (Magnitud > 25) Magnitud = 25;`

The value 50000 is not assigned anywhere in this file (it occurs only in the copied header comment). A change note reads: "26/05/2022-- v4.11 ... Se evita mag = 24 en RGB con saturacion de brillo." [mag = 24 is avoided in RGB with brightness saturation.]

### 3.4 The network's database software: daytime readings are "saturated", marked by magnitude 0

Reference: STARS4ALL, `tessdb-server` (R. González), README at tags 2.6.9 and 3.0.3 (identical), README at tags 2.1.0 and 2.4.0, and current `files/config.toml`; STARS4ALL `tessdb-api`, `src/tessdbapi/filter.py`.
Fetched: `https://raw.githubusercontent.com/STARS4ALL/tessdb-server/3.0.3/README.md` (and `/2.6.9/`, `/2.4.0/`, `/2.1.0/`), `https://raw.githubusercontent.com/STARS4ALL/tessdb-server/master/files/config.toml`, `https://raw.githubusercontent.com/STARS4ALL/tessdb-api/main/src/tessdbapi/filter.py`.
Saved: `q3_gh_tessdb-server_README_tag_3.0.3.md`, `q3_gh_tessdb-server_README_tag_2.6.9.md`, `q3_gh_tessdb-server_README_tag_2.4.0.md`, `q3_gh_tessdb-server_README_tag_2.1.0.md`, `q3_gh_tessdb-server_files_config.toml.txt`, `q3_gh_tessdb-api_src_tessdbapi_filter.py.txt` (also `q3_gh_tessdb-server_src_tessdb_filter.py.txt`, `q3_gh_tessdb-api_tests_filter_conftest.py.txt`).

README, tag 3.0.3, section "Sunrise / Sunset filtering":

> "A configurable window (7 samples by default) is stored in the server for each photometer. A filter process analyzes the middle sample in this window, if it finds all saturated values (magnitude=0) around this middle sample (past and future), this sample is discarded, otherwise it is elegible to be written to the database."

Same README, message format table: "freq | float | Hz | mand | Raw reading as a frequency with 3 decimal digits precision (millihertz) NNNNN.NNN" (five whole-number digits).

Current `config.toml`: "# Enable/disable daylight filtering, which reduce database size # by not storing daylight, saturated readings." and, of readings let through during a flush, "unfiltered data, possibly with saturated readings".

`tessdbapi/filter.py`, method `is_saturated`: "# saturated magnitudes have a value of zero" followed by `return sum(mag_list) == 0`. The test is on magnitude only; the frequency value is not examined. The filter drops a reading only when the whole window of seven is at magnitude 0 (and, when the window is full, the sequence numbers are consecutive).

Earlier READMEs (tags 2.1.0 and 2.4.0) describe a different filter by computed sunrise and sunset times: "It is recommended to activate the sunrise/sunset filter to reject TESS readings coming in daytime and avoid unnecessary grouth in the database." They do not use the word "saturated".

### 3.5 The sensor datasheet (TSL237): its own saturation and the range over which nonlinearity is specified

Reference: TAOS (Texas Advanced Optoelectronic Solutions; later ams), "TSL237S High-Sensitivity Light-to-Frequency Converter", TAOS052, January 2004; and "TSL237" datasheet TAOS052G, September 2007. Both are copies on a datasheet archive, not the manufacturer's own site.
Fetched: `https://static.datasheets.com/doc/25980512-ams-tsl237s-ds.pdf`, `https://static.datasheets.com/doc/2604079-ams-tsl237sm-lf-ds.pdf`.
Saved: `q3_ams_tsl237s_ds_25980512.pdf` (+ `.txt`), `q3_ams_tsl237sm_lf_ds_2604079.pdf` (+ `.txt`).

Table values (identical in both revisions; VDD = 5 V, TA = 25 °C, λp = 524 nm):

- "Full-scale frequency‡": MIN 500, MAX 1000, unit kHz; no TYP value. (Column placement checked on a rendering of the page of the 2004 copy, because the extracted text leaves the column of the 1000 unclear.) Footnote: "‡ Full-scale frequency is the maximum operating frequency of the device without saturation."
- "fO Output frequency", test condition "Ee = 21.8 µW/cm2": MIN 40, TYP 50, MAX 60, unit kHz.
- "fD Dark frequency", "Ee = 0 µW/cm2": MIN 0, TYP 0.1 Hz; at TA = 50 °C: 0 to 2 Hz.
- "Re Irradiance responsivity": 2.3 kHz/(µW/cm2).
- "Nonlinearity §", test condition "fO = 0 kHz to 10 kHz": "± 1%", unit "%F.S." Footnote: "§ Nonlinearity is defined as the deviation of fO from a straight line between zero and full scale, expressed as a percent of full scale."
- "Temperature coefficient of output frequency", "Wavelength < 700nm, fO = 50 kHz": ± 200 ppm/°C.

Sentences: "Output is a square wave (50% duty cycle) with frequency directly proportional to light intensity (irradiance) on the photodiode." and "The frequency at the output pin (OUT) is given by: fO = fD + (Re) (Ee)".

Neither revision gives a nonlinearity figure for the range 10 kHz to 50 kHz. Both have a typical-characteristics plot "Output Frequency vs Irradiance" with a frequency axis reaching 1000 kHz; I did not read values from it.

### 3.6 What the makers say in their papers about proportionality

(a) Bará, S., Tapia, C. E., Zamorano, J. 2019, "Absolute Radiometric Calibration of TESS-W and SQM Night Sky Brightness Sensors", Sensors 19(6), 1336, doi:10.3390/s19061336.
Fetched: `https://pmc.ncbi.nlm.nih.gov/articles/PMC6470928`. Saved: `q3_bara2019_pmc6470928.html` (+ `.txt`).

> "a monolithic irradiance-to-frequency converter chip whose electrical output is a square wave whose frequency depends linearly on the irradiance incident on the chip surface"
> "Both the SQM-LU-DL and the TESS-W use a TSL237 light-to-frequency converter (ams AG, Premstaetten, Austria) [28], that combines a silicon photodiode and a current-to-frequency converter on a single monolithic CMOS integrated circuit, and whose frequency response is linear across several decades of incident irradiance."
> (Appendix) "Irradiance-to-frequency photodiode converter chips like the TSL237 used in the TESS-W and SQM-LU-DL detectors provide an electric signal with output frequency f whose logarithm (once f is corrected from the dark frequency fD) depends linearly on the logarithm of the spectrally weighted irradiance E′ incident on the chip, with unit slope and non-zero intercept [28]."

Reference [28] is the sensor datasheet. A search of the page text for "saturat", "kHz", "daylight", "daytime" and "dynamic range" found nothing; the paper states no upper frequency limit and reports no linearity test of its own that I could find.

(b) Zamorano, J., García, C., González, R., Tapia, C., Sánchez de Miguel, A., Pascual, S., Gallego, J., González, E., Picazo, P., Izquierdo, J., Nievas, M., García, L., Corcho, O., and the STARS4ALL consortium, "STARS4ALL Night Sky Brightness Photometer", International Journal of Sustainable Lighting 35 (2016) 49-54 (as printed on the paper; received 21 November 2016, accepted 12 December 2016; it is often cited as 2017).
Fetched: the journal's host did not resolve from this machine, so the copy is the Internet Archive's capture of 10 June 2026: `http://web.archive.org/web/20260610091318id_/https://lightingjournal.org/index.php/path/article/download/21/24/74` (abstract page: `http://web.archive.org/web/20260610091430id_/https://lightingjournal.org/index.php/path/article/view/21`).
Saved: `q3_zamorano2017_ijsl_wayback_20260610.pdf` (+ `.txt`), `q3_zamorano2017_ijsl_abstract_wayback_20260610.html`.

> "The sky brightness detector is a TSL237 photodiode that convers light to frequency. It is the same sensor used by the SQM photometers."

Nothing in the paper on a maximum frequency, saturation, daylight or linearity (searched the text for those words and for "Hz").

(c) UCM laboratory note on a replacement sensor: "S9705-01DT photodiode for light pollution studies" (LICA report, in J. Zamorano's online light-pollution book).
Fetched: `https://guaix.fis.ucm.es/~jaz/lp-book/docs/LICA-report_Hamamatsu_S9705-01DT.html`. Saved: `q3_lica_report_hamamatsu_S9705.html` (+ `.txt`).

Table 1 (integrating sphere, a TSL237 unit "TAS8C5" against a Hamamatsu unit "TASF84"): test 1, magnitude 17.08, f 21.677 Hz against 31.046 Hz; test 2, magnitude 22.17, f 0.1995 Hz against 0.2679 Hz. Text: "A similar value of around 50% efficiency gain is obtained for high brightness (31/22) and around 30% for lower light intensity (0.27/0.20)" and "More tests should be performed with several samples and in a range of brightness to check linearity but the tests performed indicate that the S9705-01DT photodiode is between 30 and 50% more sensible depending on the brightness." These tests are at 0.2 to 31 Hz, on TAS units, not at high frequencies and not on a TESS-W.

### 3.7 Others (not the makers) on the same sensor

Alarcon, M. R., Puig-Subirà, M., Serra-Ricart, M., Lemes-Perera, S., Mallorquín, M., López, C. 2021, "SG-WAS: a new Wireless Autonomous Night Sky Brightness Sensor", Sensors 21, 5590, doi:10.3390/s21165590; read as arXiv:2108.10891v1.
Fetched: `https://arxiv.org/pdf/2108.10891`. Saved: `q3_arxiv_2108.10891.pdf` (+ `.txt`).

> "According to the manufacturer [23], the sensor linearity is fulfilled in the range between 1 Hz and 1 MHz when illuminated with a spectral lamp at 524 nm at ambient temperature. This has been verified before with several SQM devices down to 19 mag/arcsec2 [24]."
> "Linearity is maintained down to 0.01 Hz, equivalent to about 24 mag/arcsec2, with an R2 very close to 1. The TSL237 sensor is therefore linear in the measurement of NSB in both light-polluted and natural dark locations."

Their own test is of a bare TSL237 in their own instrument, and its stated aim is the dark end. The "1 Hz and 1 MHz" attributed to the manufacturer does not match the datasheet copies in 3.5, which specify nonlinearity only for 0 to 10 kHz; both statements are given here as printed.

Alarcon, M. R., Serra-Ricart, M., Lemes-Perera, S., Mallorquín, M. 2021, "Natural Night Sky Brightness during Solar Minimum", arXiv:2105.01066v2 (doi:10.3847/1538-3881/abfdaa as listed by the search engine; not checked on the journal page).
Fetched: `https://arxiv.org/pdf/2105.01066`. Saved: `q3_arxiv_2105.01066.pdf` (+ `.txt`).

> "It is a silicon photodiode with a light-to-frequency converter, which has a spectral response that varies from 300 to 1100 nm approximately, with a sensitivity maximum around 700 nm, responding linearly to frequency over several irradiance orders (Bará et al. 2019)."

### 3.8 Maker documents read in which nothing on the ceiling or on linearity was found

Each was searched for "satur", "50000", "50 000", "50,000", "kHz", "Hz", "linear", "daylight", "daytime", "dynamic range", "frequen":

- J. Zamorano, slides "Monitoring with TESS v1": `https://guaix.fis.ucm.es/~jaz/TESS/Monitoring_with_TESS_v1.pdf`, saved `q3_Monitoring_with_TESS_v1.pdf`. Says only "The sky brightness detector is a TSL237 photodiode that converts light to frequency."
- Poster on TESS calibration, LPTMM June 2017: `https://guaix.ucm.es/wp-content/uploads/2020/02/2017_06_LPTMM_poster_TESS_calibration.pdf`, saved `q3_2017_06_LPTMM_poster_TESS_calibration.pdf`.
- Poster, ALAN 2016: `https://guaix.ucm.es/wp-content/uploads/2020/02/2016_09_ALAN2016_Zamorano.pdf`, saved `q3_2016_09_ALAN2016_Zamorano.pdf`.
- Poster, IAU Vienna 2018 (García, Zamorano, García and others, "STARS4ALL TESS-W night sky brightness photometer"): `https://guaix.ucm.es/wp-content/uploads/2020/02/2018_08_IAU_Viena_TESS-W.pdf`, saved `q3_2018_08_IAU_Viena_TESS-W.pdf`. Image only; read by eye from a rendering. Nothing on range or linearity.
- TESS-W manual, version 4, English: `https://guaix.fis.ucm.es/~jaz/TESS/v4_TESS-W_manual_english.pdf`, saved `q3_v4_TESS-W_manual_english.pdf`; and quick guide `http://observatorioremoto.com/TESS-W_quick-guide.pdf`, saved `q3_TESS-W_quick-guide.pdf`.
- Assembly document `docs/MontajeTESS-w-4.pdf` in the firmware repository, saved `q3_gh_cristogg_TESS-W_docs_MontajeTESS-w-4.pdf`.
- TESS pages at `https://guaix.fis.ucm.es/tess/` (home, `/models`, `/software`, `/node/9`), saved `q3_guaix_tess_index.html`, `q3_guaix_tess_models.html`, `q3_guaix_tess_software.html`, `q3_guaix_tess_node9.html`.
- READMEs of the network's tools: `TESS-IDA-TOOLS` (data file header ends "# Comment: MSAS = ZP - 2.5*log10(Frequency)"; no note on daytime values), `tess-publisher`, `tessw-publisher`; saved `q3_gh_TESS-IDA-TOOLS_README.md`, `q3_gh_tess-publisher_README.md`, `q3_gh_tessw-publisher_README.md`. Repository lists: `q3_github_stars4all_repos.json`, `q3_gh_cristogg_repos.json`.

### 3.9 Looked for and not found

- Any statement by the makers, in a paper, manual, poster or web page, that the TESS-W's readings stop at 50,000 Hz. The only places the number appears are the firmware source and its notes (3.1, 3.2).
- Any measurement by the makers of whether a TESS-W's frequency is proportional to the light between about 10 kHz and 50 kHz (twilight and daylight levels). The calibration paper (3.6a) asserts linearity by citing the datasheet; the datasheet's nonlinearity figure covers 0 to 10 kHz only.
- Any statement of which sky brightness or irradiance corresponds to the out-of-range mark for a TESS-W as built (with its collector and filter). The firmware author's table pairs 50000 Hz with "Mag V estimada" 9,20; the zero point behind that column is not stated in the file.
- Which build of the sensor-microcontroller code is in production units, and so whether the mark is raised at 50, 60 or 65 kHz in practice (the one published source file contains all three numbers).
- A reason given by the makers for choosing 50000 as the written value.
- The manufacturer's own current copy of the TSL237 datasheet (the two copies read are from a datasheet archive; two other hosts refused the request).
- Not opened: Pravettoni and others 2016 (J. Quant. Spectrosc. Radiat. Transf. 181, 74), a linearity test of Sky Quality Meters, which use the same sensor; a search summary of an earlier repository version says the calibration covered 6 to 19 mag/arcsec2 and confirmed linearity, but I did not fetch or save it, so that is unverified here.
- Pages that gave nothing: the Instructables page for the TESS-W (text is loaded by script; no body text retrieved); the firmware author's site observatorioremoto.com and two of his blog posts on the TESS (no mention of range or linearity; not kept).

## Question 4. The Hunga haze over 20 to 45 S in mid-2022: optical depth, heights, particle size; and the optical depth before the eruption

How the sources were read. PDFs were fetched with a plain client name and converted with `pdftotext`; quotations below are copied from the resulting text files (`*_flow.txt`, saved beside each PDF in `lit/src5/`, or in `lit/src4/` for sources saved by the earlier search). Values marked "read from figure" were read by eye from page images rendered with `pdftoppm`; colour-map readings are good to about one colour step, curve readings to roughly 10 to 15 percent, and each is labelled. Nothing here is from memory unless marked. What the earlier notes already hold (APARC executive-summary sentences on timing, decay, "below 30 km", "effective radius of 0.4 µm"; the eye reading of APARC Figure 3.1c) is not repeated.

One thing to keep in view throughout: the sources give optical depth at different wavelengths (525/532, 550, 745/756, 869, 997/1020 nm), over different height ranges (above the 380 K level; 17 to 40 km; tropopause + 1 km to 35 km; 15 km to top), and in the first half of 2022 two limb-scatter retrievals from the same instrument differ by nearly a factor of two, with the solar-occultation values between them (4.1c). The numbers below are not interchangeable.

### 4.1 Optical depth in mid-2022

**(a) S. Khaykin and others 2026**, "Global transport of stratospheric aerosol produced by Ruang eruption from EarthCARE", Atmos. Chem. Phys. 26, 607-622. Address: https://acp.copernicus.org/articles/26/607/2026/acp-26-607-2026.pdf (saved by the earlier search). File: `src4/khaykin2026_acp-26-607-2026.pdf`, `_flow.txt`.

Figure 6, titled in the plot "GloSSAC+SAGE III stratospheric AOD@525 nm above 380 K", caption: "Time series of stratospheric aerosol optical depth (SAOD) at 525 nm from GloSSAC merged satellite record and SAGE III since January 2024 for different latitude bands." Monthly points for three bands; the red curve is 60 S to 25 S. Read from figure (linear axis, 0 to 30 x 10^-3; reading good to about 0.5 x 10^-3):

| 60 S to 25 S, 525 nm, above 380 K | value (x 10^-3) |
|---|---|
| quiet years 2000 to 2004 | about 3.5 to 4.5 |
| 2017 to early 2018 | about 4.5 to 5 |
| mid-2021 | about 8.5 to 9 |
| last points before the eruption (end of 2021) | about 7 |
| on the rise, about May to June 2022 | about 19 to 23.5 |
| peak (one point, about August 2022) | about 25 |
| first half of 2023 (plateau) | about 15 |
| early 2024 | about 7 |

The tropical band (25 S to 25 N, black) in the same figure: about 6.5 to 7 before the eruption, peak about 22 in early 2022, about 13.5 to 15 by mid-2022.

**(b) APARC 2025**, The Hunga Volcanic Eruption Atmospheric Impacts Report, chapter 3 (full reference and address in the earlier notes). File: `src4/aparc_hunga_report_chapter_3.pdf`, `_flow.txt`.

Figure 3.7 (report page 71), caption: "Time series of aerosol optical depth above the 380 K potential temperature level from ground-based lidars at different sites, compared with GloSSAC V2.21 merged satellite data and SAGE III/ISS observations zonally averaged within corresponding 10° latitude bands: (a) Lauder (45° S); (b) La Réunion (21° S) ...". Panel titles: "a) SAOD @ 532 nm, above 380K, Lauder (45°S) and satellite zonal/monthly means 40°S–50°S"; "b) SAOD @ 532 nm, above 380K, Reunion (21°S) and satellite zonal/monthly means 25°S–15°S". Read from figure (linear axis 0 to 40 x 10^-3; good to about 1 x 10^-3):

| 532 nm, above 380 K | 40 to 50 S (panel a) | 25 to 15 S (panel b) |
|---|---|---|
| 2000 to 2005 | Lauder lidar about 2.5 to 3.5; GloSSAC about 3.5 to 4 | GloSSAC about 3.5 |
| 2021 (before) | SAGE III about 6.5 to 7.5; Lauder lidar dips to about 5 at the turn of 2021/2022 | SAGE III and GloSSAC about 6.5 to 7 |
| Hunga peak | SAGE III about 29 to 29.5; Lauder lidar about 27 to 28 (mid-2022) | Réunion lidar off the top of the scale (above 40) in January 2022; SAGE III about 35.5 in early 2022 |
| mid-2022 | at or near the peak (the text says "the peak of the SAOD perturbation at Lauder (45° S) was observed during June–July 2022") | SAGE III about 26 to 30; GloSSAC about 20 to 25 |
| 2023 | plateau about 15 to 16, then about 11 (SAGE III) and 8.5 (lidar) at the turn of 2023/2024 | about 14 early 2023, about 8 by early 2024 |

Figure 3.1a (report page 66), "(a) Stratospheric AOD 997 nm (OMPS-LP NASA v2.1)", colour scale 0 to 30 x 10^-3. Read from figure (colour reading, about one step of 2 to 3 x 10^-3): a patch in the top (magenta to white) part of the scale, about 25 to 30 x 10^-3, centred near 40 S and reaching from about 33 S to 47 S, from about June to late November 2022 (with a data gap in August); at 20 to 30 S in June to August 2022 yellow-green to orange, about 12 to 18 x 10^-3; at 40 S in February to March 2022, before the haze arrived there, blue to light blue, about 3 to 6 x 10^-3. This refines the earlier note, which put the bright patch at "about 30 to 45 S from about May to September 2022".

**(c) M. R. Schoeberl, Y. Wang, G. Taha, D. J. Zawada, R. Ueyama, A. Dessler 2024**, "Evolution of the climate forcing during the two years after the Hunga Tonga-Hunga Ha'apai eruption", J. Geophys. Res. Atmospheres, doi 10.1029/2024JD041296 (the saved copy shows issue stamp "2024, 14"; volume number not read from the copy). Address: https://ntrs.nasa.gov/api/citations/20240010660/downloads/Schoeberl_etal_JGR2024.pdf (NASA report server copy of the open-access article). File: `q4_schoeberl2024_ntrs_20240010660.pdf`, `_flow.txt`.

Height range and wavelength: "For both NASA OMPS and USask OMPS, we integrate the 745 nm extinction from 1 km above the tropopause to 35 km to obtain SAOD." Conversion: "To convert the SAOD at the 745 nm wavelength to 550 nm we use the Ångström exponent from SAGE III/ISS".

The disagreement, in their words: "Figure 4 shows the range of SAOD values with USask nearly a factor of two smaller than NASA OMPS after the eruption. ... However, from the SAGE measurements, it is apparent that USask is low biased while the NASA is high biased. Figure 4d shows that after" (page break in the copy) "August 2022, NASA OMPS comes into agreement with SAGE and all three SAOD estimates converge in mid‐ 2023". And: "NASA and USask SAOD distributions both show an initial high value between 30°S and the equator until May‐June when the SAOD shifts south." And: "An anomaly in the USask SAOD during May/June/July 2022 from 45°S to 60°S is not seen NASA SAOD and is possibly a retrieval artifact." And: "by the end of 2,023 the SAOD anomalies have largely disappeared."

Figure 4d, "SAOD 20° S", converted to 550 nm, logarithmic axis. Read from figure (curve reading, about 10 to 15 percent):

| 20 S, 550 nm | NASA OMPS | USask OMPS | SAGE III/ISS |
|---|---|---|---|
| first days of January 2022 (before) | about 0.006 | about 0.006 | about 0.0065 |
| May 2022 (NASA peak) | about 0.04 | about 0.02 | about 0.027 |
| June to July 2022 | about 0.031 to 0.036 | about 0.018 | about 0.024 to 0.027 |
| August 2022 | about 0.025 to 0.027 | about 0.015 to 0.016 | about 0.022 |
| end of 2023 | about 0.006 | about 0.006 | about 0.006 |

Figure 4a ("NASA OMPS 745 nm SAOD") and 4c ("SAGE 756 nm SAOD"), latitude against time, colour scale 0 to 0.06 in steps of 0.003. Read from figure (colour reading, about one or two steps): NASA OMPS at about 38 to 47 S from July to September 2022 is yellow-green to yellow, about 0.04 to 0.05, with a small orange-red spot (about 0.05 to 0.055) near 42 S in mid-August 2022; at 20 to 30 S in June to July 2022, light blue to green, about 0.02 to 0.03. SAGE at 756 nm at about 35 to 45 S from July to September 2022 is light blue to cyan, about 0.024 to 0.03; at 20 S in June to July, blue, about 0.015 to 0.02. Both panels show the two lowest colour steps (below about 0.006) at 30 to 45 S in January 2022. So at 40 to 45 S in July to September 2022 the two disagree at nearly the same wavelength: about 0.04 to 0.05 (NASA OMPS, 745 nm) against about 0.024 to 0.03 (SAGE, 756 nm).

**(d) M. Sicard and others 2025**, "Radiative impact of the Hunga stratospheric volcanic plume: role of aerosols and water vapor over Réunion Island (21° S, 55° E)", Atmos. Chem. Phys. 25, 367-381. Address: https://acp.copernicus.org/articles/25/367/2025/acp-25-367-2025.pdf . File: `q4_sicard2025_acp-25-367-2025.pdf`, `_flow.txt`. One site at the northern edge of the band; OMPS version 2.0, 745 nm, "integrating the extinction profiles from 17 to 40 km".

"The sAOD peak produced by the Hunga volcano (0.035) is the highest in the last decade"; "While the monthly OMPS sAOD peak is reached in April and May 2022, the instantaneous lidar sAOD peaks just a few days after the eruption, reaching 0.40 on 21 January."; "A decrease in the monthly sAOD is observed after April/May and until November. Then sAOD stabilizes until today (sAOD = 0.012, almost 5 times the background sAOD)." Conclusions: "reaches a peak at 0.035 (∼ 13 times the background sAOD) in April 2022 ... From April to November 2022, the sAOD decreases and then stabilizes at a value of 0.012 (∼ 5 times the background sAOD)." Their Figure 3a (daily OMPS curve, logarithmic axis) read from figure (curve reading, about 10 percent; the scale was checked against the drawn background line, which reads 0.0026 as the text says): about 0.004 in the days before the eruption; about 0.038 at the highest point of the daily curve in April to May 2022; about 0.031 in June 2022; about 0.026 to 0.028 in July 2022; about 0.019 to 0.025 in August 2022; about 0.015 to 0.018 in September 2022; about 0.011 to 0.013 from October 2022 on. The lidar values were converted from 355 nm "using a constant Ångström power law, AE355/745, of −0.14".

**(e) C. Duchamp and others 2026**, "Aerosol Composition and Extinction of the 2022 Hunga Plume Using CALIOP", Atmos. Meas. Tech. 19, 1675-1696. Address: https://amt.copernicus.org/articles/19/1675/2026/amt-19-1675-2026.pdf . File: `q4_duchamp2026_amt-19-1675-2026.pdf`, `_flow.txt`. Covers 16 January to 25 March 2022 and 20 to 10 S only, so it is earlier and further north than asked; kept for what it says about disagreement between instruments.

"The AOD of the plume at 532 nm is between 0.5 and 1.25 on the first four days, then decreases rapidly and stabilizes at 0.047 ± 0.011 for March 2022." (Plume layer, "between 17.5 and 31.5 km altitude and averaged between 20 and 10° S".) "The AOD curve from OSIRIS is far below the others with values ∼ 0.01. ... The unusual aerosol size distribution of the Hunga plume leads to the significant quantitative disagreements in AOD estimates from scattered light measurements due to the different size distribution assumptions, as well as the sensitivity of the instrument."

**(f) C. Kloss and others 2026**, "Cross-hemispheric transport of the Hunga aerosol plume: in situ evidence and radiative effects from the northern hemisphere", Atmos. Chem. Phys. 26, 8981. Address: https://acp.copernicus.org/articles/26/8981/2026/acp-26-8981-2026.pdf . File: `q4_acp-26-8981-2026.pdf`, `_flow.txt`. Northern latitudes; one sentence bears on the south: "Marked anomalies in the sAODs were observed at southern hemispheric mid- and high-latitudes starting from April 2022 (Sellitto et al., 2024)." And a caution on rank: the load "was recorded as the largest since Pinatubo (Taha et al., 2022; Sellitto et al., 2022), but peak values are not significantly larger than what was observed following Raikoke (Vernier et al., 2025)."

**(g) From papers saved by the earlier search, sentences not extracted then.** Khaykin and others 2022 (`src4/khaykin2022_s43247-022-00652-x.txt`): "Figure 10c provides evidence that the Hunga eruption led to a 4-5-fold increase in the stratospheric aerosol optical depth (SAOD)" and "The stratospheric aerosol perturbation by the Hunga eruption has reached its peak in early June". (Their Figure 10 is not in the saved page text; I did not see the curve.) Legras and others 2022 (`src4/legras2022_acp-22-14957-2022_flow.txt`): "By June, the hemispheric stratospheric aerosol optical depth perturbation of the HTHH plume is twice as large as the peak perturbation of the 2019 Raikoke eruption".

### 4.2 Heights between which it lay

**(a) C. Duchamp, F. Wrana, B. Legras, P. Sellitto, R. Belhadji, C. von Savigny 2023**, "Observation of the aerosol plume from the 2022 Hunga Tonga-Hunga Ha'apai eruption with SAGE III/ISS", Geophys. Res. Lett., doi 10.1029/2023GL105076 (the saved copy is the accepted manuscript, marked "In press"; volume and article number not in it). Address: https://hal.science/hal-04206495/document . File: `q4_duchamp2023_hal-04206495.pdf`, `_flow.txt`.

Text: "Until May 2022 the plume was mainly contained between 30°S and 10°N and then started to spread towards higher latitudes in the southern hemisphere. ... The plume descended constantly until November 2022 but with a latitude dependent speed, in agreement with the BrewerDobson circulation [so in the text copy; a hyphen is lost at a line end], the descent being faster at high latitudes. Since November 2022, the maximum extinction altitude has been stalling at mid-latitudes and slightly rising in the equatorial band. It is noticeable that for all latitudes north of 30°S the aerosol layer does not disperse in altitude and keeps a fairly constant thickness."

Figure 2, first row ("SAGE III extinction (km-1) at 0.755 µm in latitude bands", altitude 15 to 30 km against month, November 2021 to June 2023, colour scale 0 to 0.005 km^-1, half-kilometre cells). Read from figure (colour reading; heights good to about 1 km, extinction to about 0.0005 km^-1):

| band | months | layer clearly above the surroundings (about 0.0015 km^-1 and more) | strongest part | strongest extinction |
|---|---|---|---|---|
| 50 S to 30 S | July to September 2022 | about 17 to 24.5 km | about 19 to 21.5 km | about 0.004 km^-1 |
| 30 S to 10 S | June to August 2022 | about 19.5 to 25 km | about 21.5 to 23.5 km | 0.0045 km^-1 or more (top of scale) |

In the 50 S to 30 S panel the layer first shows about May 2022, and by early 2023 its strongest part has sunk to about 17 to 20 km and weakened to about 0.002 to 0.003 km^-1. Fig. 3 of the same paper takes the plume "at altitude of maximum extinction averaged between months of June and August 2022" in the 30 to 10 S range and the background "at 24.5 km".

**(b) Sicard and others 2025** (as 4.1d), Réunion, 21 S: "The time–height plot of the extinction (Fig. 3b) clearly shows the height and vertical extension of the volcanic plume which is still present on 15 April 2023 and is located at 18.5–23.5 km height (sAOD = 0.012). The plume peak height has a decreasing tendency since April 2022 at an average steady rate of −244 m per month or ∼ −8 m d−1." And: "Except during the first week of detection above Réunion Island, the Hunga volcanic plume is not detected above 30 km." Their Figure 3b (OMPS extinction at 745 nm against height, with a red line for the peak height) read from figure (heights good to about 0.5 km): the peak height is about 23.5 km in April 2022, about 21.5 km in July 2022, about 21 km in October 2022 and about 20.5 km in April 2023; in June to August 2022 the top of the clearly enhanced layer is at about 25 km. I did not read the lower edge for 2022.

**(c) APARC 2025 chapter 3** (as 4.1b), on the Lauder (45 S) balloon profiles: the "mid-stratosphere region, with potential temperature from 550 K to 750 K (approximately 22–28 km altitude at this latitude)" and the "lower-stratosphere region, with potential temperature from 380 K to 550 K (approximately 14–22 km altitude at this latitude)" both held the volcanic particles (see 4.3c); "These results from POPS profiles from Lauder demonstrate the sedimentation of larger particles, initially formed in the mid-stratosphere, to the lower stratosphere." For the tropics (10 S to 10 N) the report gives the SAGE III/ISS extinction peak "near 25 km" just after the eruption and "remaining near 22 km" after August 2022 (the second sentence is already in the earlier notes).

**(d) T. N. Knepp, M. Kovilakam, L. Thomason, S. J. Miller 2024**, "Characterization of stratospheric particle size distribution uncertainties using SAGE II and SAGE III/ISS extinction spectra", Atmos. Meas. Tech. 17, 2025-2054. Address: https://amt.copernicus.org/articles/17/2025/2024/amt-17-2025-2024.pdf . File: `q4_knepp2024_amt-17-2025-2024.pdf`, `_flow.txt`. "the main plume contained particles with re > 400 nm, in March 2022, and this plume was centered near 10° S and 24 km. ... the plume of the largest particles was centered at ≈ 20 km near the Equator and descended to lower altitudes toward the higher latitudes. This is in contrast to the persistence of smaller particles at higher altitudes, well past 25 km." (Their Figure 20, monthly zonal medians; not read for the mid-latitude heights.)

**(e) G. Taha and others 2022** (`src4/taha2022_ntrs_20220016184_flow.txt`), for the band 30 S to 10 N in the first five months: "the main volcanic layer was between 20 and 26 km altitudes and exhibited a rapid descent of the aerosol layer during the first few weeks and a second slower descent in April".

### 4.3 Particle size

**(a) Duchamp and others 2023** (as 4.2a). Abstract: "The persisting volcanic aerosols – with a mode width of 1.25 and an effective radius of 0.4 µm – differ from the significantly smaller background aerosols and from those measured during recent stratospheric eruptions." Text: background points "match the values reported in Wrana et al. (2021) with width σ of 1.4-1.5 and radius rm of 0.15-0.2 µm. Instead, all the plume points south of 10°N but a couple of outliers lay between the 1.2 and 1.3 σ curves and cluster around rm ≈ 0.35 µm." "From σ and rm, we calculate reff which is near 0.4 µm in the plume while we find 0.2 µm or less for the background in agreement with Khaykin et al. (2022)." "April 2022 for the 40°S latitude band is a mixed case between background and plume conditions when aerosols begin to reach these latitudes". "It also shows that at all latitudes the mean size decreases with time albeit by a small amount but no trend can be detected for the width." Number density: "Values of 3.5 cm−3 are maintained until September 2022 and are slowly declining afterwards. This density is not very different from that of the background, here around 2 cm−3 at the altitudes of the plume".

Figure 3 legend values (30 S to 10 S): 1.23, rm = 0.35 µm, N0 = 3.4 cm^-3 and 1.37, rm = 0.18 µm, N0 = 1.1 cm^-3 (the width symbol is lost in the text copy; by the caption and the text the first set is the plume, June to August 2022, the second the background at 24.5 km, November 2021 to January 2022). The formula used: effective radius = rm exp(5/2 ln² σ) (garbled in the text copy as "reff = rm exp 52 ln2 σ"; Sellitto and others 2025 give the same, "re = rm e2.5ln σ" in their text copy). Figure 2 third row (effective radius, colour scale 0 to 0.5 µm), read from figure (colour reading on an enlarged crop; radius good to about 0.05 µm, heights to about 1 km). 50 S to 30 S: before May 2022 the whole column from 17 to 30 km shows about 0.15 to 0.25 µm; in July 2022 the colours for about 0.4 µm lie between about 17 and 21 km, with about 0.3 to 0.35 µm above them up to about 23 km and smaller values higher; in September 2022 about 0.4 µm from about 15.5 to 19.5 km and 0.3 to 0.35 µm up to about 22 km; in the first half of 2023 about 0.4 µm and a little more from the bottom of the plot (15 km) up to about 18 to 19 km. 30 S to 10 S, June to August 2022: about 0.4 µm between about 18.5 and 22 km, about 0.3 to 0.35 µm up to about 23.5 km. So in the 50 S to 30 S band the largest particles sit at and below the strongest extinction (about 19 to 21.5 km, 4.2a), not above it.

**(b) M. Boichu and others 2023**, "Growth and global persistence of stratospheric sulfate aerosols from the 2022 Hunga Tonga-Hunga Ha'apai volcanic eruption", J. Geophys. Res. Atmospheres 128 (23), doi 10.1029/2023JD039010. Address: https://hal.science/hal-04272377/document (author's manuscript). File: `q4_boichu2023_hal-04272377.pdf`, `_flow.txt`. Ground sun photometers (AERONET), so column values, with the peak radius of the fine-mode volume size distribution as the measure.

"For all four stations with enough data situated to the south of ∼33◦ S (AU NSW Lidcombe, Univ of Auckland, Trelew, CEILAP-Comodoro), the volcanic mode becomes visible in the time series of rpeak only after a time lag of several months, e.g. 3 months after eruption over Australia/AU NSW Lidcombe station (34◦ S) and 4 months over Argentina/Trelew station (43◦ S)". "These stacks show that, from the eruption until May 2023 (time of writing), HT-HH aerosol rpeak values range in 0.35-0.5 µm (Fig. 8b). Until June 2022, an overall decrease in particle size is observed". "After June 2022, slow temporal variations of the HT-HH aerosol size are observed (Fig. 8b), with a minimum radius of 0.35 µm reached in July 2022, followed by a progressive increase up to 0.50 µm in late January 2023". "this hypothesis of an homogeneization of the HT-HH aerosol layer most likely extends to the scale of the southern hemisphere, at least down to 45◦ S." Before the eruption: "background fine mode aerosols visible in the months prior to eruption, which have generally a smaller size (<0.30 µm)".

They also record a disagreement with sizes inferred from settling speed: "Schoeberl et al. (2022) report a radius of 1.2 µm in March–June 2022, whereas Legras et al. (2022) estimate a decrease from 2 µm in February 2022 to 0.5 µm in late July 2022. In contrast, a more recent study by Khaykin et al. (2022) yields a smaller aerosol radius of 0.35–0.54 µm in April-May 2022".

**(c) APARC 2025 chapter 3** (as 4.1b), text not in the earlier notes. "the aerosol grew within a week from a typical stratospheric background radius centred around 0.15 µm to a narrower pseudolognormal size distribution with a modal radius of approximately 0.35 µm (e.g. Duchamp et al., 2023; Li et al., 2024)." "The peak effective radius reached just above 0.4 µm in the early stage in the southern tropics. The larger particles are observed later in the southern mid-latitude reaching similar values of effective radius." Lauder (45 S) balloon counters, surface-area size distribution: at 550 to 750 K, "From background conditions with a modal radius below 0.1 µm, the perturbed distribution shifted to peak around 0.35 µm (Figure 3.5a, red–purple curve) during the first six months after the eruption. With time, this decreased to approximately 0.25 µm in early 2023"; at 380 to 550 K, "Six months after the eruption, the modal radius of the aerosol surface size distribution was centred at approximately 0.25 µm but increased with time to peak around 0.35 µm in 2023." Sun photometers: "a distinct increase in aerosol peak radius of the calculated fine-mode volume size distribution (r peak) to values in the range 0.3–0.5 µm was reported across the 23 AERONET stations of the Southern Hemisphere. This persisted until at least March 2024". For the tropics, before the eruption: "the particle effective radius (shown in red) was approximately 0.25 µm for most of the lower stratosphere."

Note the two different "before" sizes in print: effective radius "0.2 µm or less" (Duchamp 2023), "approximately 0.25 µm" (APARC, tropics, SAGE III/ISS by the Knepp method), "~ 0.2 µm" baseline (Asher 2023, below), "~0.22 µm" (conference slides, below).

**(d) Knepp and others 2024** (as 4.2d), one profile, 15 February 2022: "The estimated mode radius at 24 km was 345 ± 20 nm with a distribution width (σ) of 1.3 ± 0.05. We note that the inferred re value at 24 km (410 ± 5 nm) is in good agreement with the estimate of 460 nm from data collected by a Portable Optical Particle Spectrometer (Asher et al., 2023)". And later growth low down: "re approached 500 nm in March/June 2023." The method is stated as "≈ 25 % accurate for mode radius".

**(e) P. Sellitto, R. Belhadji, B. Legras, A. Podglajen, C. Duchamp 2025**, "The optical properties of the stratospheric aerosol layer perturbation of the Hunga Tonga-Hunga Ha'apai volcano eruption of 15 January 2022", Atmos. Chem. Phys. 25, 6353. Address: https://acp.copernicus.org/articles/25/6353/2025/acp-25-6353-2025.pdf . File: `q4_sellitto2025_acp-25-6353-2025.pdf`, `_flow.txt`. "larger particles (0.35–0.45 µm effective radius) and a smaller SD width (1.20–1.30 spread in a modelled mono-modal size distribution) compared to the background stratospheric aerosol layer".

**(f) E. Asher and others 2023**, "Unexpectedly rapid aerosol formation in the Hunga Tonga plume", Proc. Natl. Acad. Sci. USA, doi 10.1073/pnas.2219547120. Address: https://univ-reunion.hal.science/hal-04301363/document (author's manuscript). File: `q4_asher2023_hal-04301363.pdf`, `_flow.txt`. Balloons from Réunion in the first weeks, so early and at 21 S: "The mode of the size distribution occurred at ~ 560 nm diameter, and the aerosol effective radius exceeded 0.3 µm"; lower, drier part: "the aerosol effective radius was not noticeably different from baseline values (~ 0.2 µm; Fig. S2)"; "a maximum effective radius (> 0.4 µm) observed in early February".

**(g) Conference slides (not a reviewed paper)**: Xi Chen and others, "Stratospheric particle size growth and cooling by water vapor after the 2022 Hunga Tonga eruption", SAGE III/ISS science meeting, 12 September 2023. Address: https://sage.nasa.gov/wp/wp-content/uploads/2023/11/XiChen_SAGEIII_STM_2023.pdf . File: `q4_xichen_sage3_stm_2023.pdf`, `_flow.txt`. "Reff can reach the largest of 0.35 ~ 0.45 µm at 22-24 km from March 2022, larger than background of ~0.22 µm and smaller than Pinatubo aerosols with the largest size of 0.5-0.6 µm."

### 4.4 Optical depth of the stratospheric haze there before the eruption

Collected from the sources above; all for the months just before January 2022 unless a year is given.

| source | where, how | wavelength | value |
|---|---|---|---|
| Khaykin 2026 Fig. 6 (read from figure) | 60 S to 25 S, GloSSAC, above 380 K | 525 nm | about 7 x 10^-3 at the end of 2021; about 8.5 to 9 x 10^-3 in mid-2021; about 3.5 to 4.5 x 10^-3 in 2000 to 2004 |
| APARC 2025 Fig. 3.7a (read from figure) | 40 to 50 S, SAGE III/ISS; Lauder lidar; above 380 K | 532 nm | about 6.5 to 7.5 x 10^-3 in 2021 (SAGE III); lidar about 5 x 10^-3 at the turn of 2021/2022; lidar about 2.5 to 3.5 x 10^-3 in 2000 to 2005 |
| APARC 2025 Fig. 3.7b (read from figure) | 25 to 15 S, SAGE III/ISS and GloSSAC, above 380 K | 532 nm | about 6.5 to 7 x 10^-3 in late 2021 |
| Schoeberl 2024 Fig. 4d (read from figure) | 20 S, tropopause + 1 km to 35 km | 550 nm (converted from 745/756) | about 0.006 (OMPS, both retrievals), about 0.0065 (SAGE), first days of January 2022 |
| Schoeberl 2024 Fig. 4a, 4c (read from figure) | 30 to 45 S, January 2022 | 745 and 756 nm | the two lowest colour steps, that is below about 0.006 |
| Sicard 2025 (sentence) | Réunion 21 S, OMPS, 17 to 40 km | 745 nm | "The background sAOD is measured over the unperturbed years 2012 and 2013. It is (2.6 ± 0.1) × 10−3." |
| Sicard 2025 Fig. 3a (read from figure) | Réunion 21 S, OMPS, 17 to 40 km, days before the eruption | 745 nm | about 0.004 |
| APARC 2025 Fig. 3.1a (read from figure) | 40 S, February to March 2022 (haze not yet there), OMPS-LP | 997 nm | about 3 to 6 x 10^-3 |
| earlier notes, APARC Fig. 3.1c (read from figure) | southern-hemisphere mean, OMPS-LP | 997 nm | about 0.003 |

Two things the sources say about this "before". Sicard and others: "since the eruption of Ambae in July 2018, the sAOD over Réunion Island has never turned back to its background value", so the level just before Hunga was above their 2012 to 2013 background: about 0.004 at 745 nm in the days before the eruption by my reading of their Figure 3a, against their stated 0.0026. And Khaykin 2026 Figure 6 marks the 2019/2020 Australian fires (peak about 18 x 10^-3 at 525 nm in 60 S to 25 S) and the 2021 La Soufrière eruption in the two years before, with the southern band still falling from about 9 to about 7 x 10^-3 through the second half of 2021.

For comparison only (northern, not the band asked about): Kloss and others 2026, Table 2, SAGE III/ISS, 30 to 50 N, "integrated between 15 km and the TOA", "Background Nov 2017–Feb 2018": (6.9 ± 1.3) x 10^-3 at 384 nm, (3.1 ± 0.5) x 10^-3 at 756 nm, (1.6 ± 0.3) x 10^-3 at 1020 nm; "Background + Hunga Nov 2022–Feb 2023": (8.5 ± 1.4), (4.1 ± 0.5), (2.2 ± 0.5) x 10^-3; "Hunga only": (1.7 ± 1.2), (1.1 ± 0.1), (0.7 ± 0.3) x 10^-3; Ångström exponent 1.0 ± 0.2.

### 4.5 Where the sources disagree (both given above)

1. Optical depth near 40 to 45 S in July to September 2022 at about 750 nm: about 0.04 to 0.05 from NASA OMPS-LP (745 nm) against about 0.024 to 0.03 from SAGE III/ISS (756 nm), both read from Schoeberl 2024 Figure 4; the authors call NASA "high biased" and the Saskatchewan retrieval "low biased" until about August 2022.
2. At 20 S in June to July 2022 at 550 nm: about 0.031 to 0.036 (NASA OMPS), about 0.018 (Saskatchewan OMPS), about 0.024 to 0.027 (SAGE), same figure.
3. Peak in the visible at southern mid-latitudes: about 25 x 10^-3 for the wide band 60 to 25 S at 525 nm (Khaykin 2026 Fig. 6, GloSSAC) against about 29 x 10^-3 for 40 to 50 S at 532 nm (APARC Fig. 3.7a, SAGE III/ISS) and about 27 to 28 x 10^-3 for the Lauder lidar; different bands, so not a contradiction, but not one number.
4. Time of the southern peak: "early June" (Khaykin 2022, perturbation overall), "June–July 2022" at Lauder (APARC), a single highest monthly point about August 2022 for 60 to 25 S (Khaykin 2026 Fig. 6, my reading), July to October for the brightest colours at 997 nm (APARC Fig. 3.1a, my reading).
5. Particle size: optical methods agree on an effective radius of about 0.35 to 0.45 µm; sizes inferred from settling speed were larger (1.2 µm, Schoeberl 2022; 2 µm falling to 0.5 µm by late July 2022, Legras 2022), as quoted by Boichu 2023.

### 4.6 Looked for and not found, or not read

- A table (not a figure) of zonal-mean optical depth for 20 to 45 S by month in 2022 at a visible wavelength: not found. Every mid-2022 optical depth above is a figure reading of mine; the only optical depths given in sentences are Sicard's April 2022 peak and November 2022 plateau, and the CALIOP value for March 2022.
- The optical depth at 20 to 45 S integrated over the whole visible band, or at 500 to 550 nm from a limb-scatter instrument other than through the conversion in Schoeberl 2024: not found.
- A. Bourassa and others 2023, "Tomographic retrievals of Hunga Tonga-Hunga Ha'apai volcanic aerosol", Geophys. Res. Lett.: the publisher's site refused an automated client (status 403); not read. Known here only through Schoeberl 2024's description of it.
- Schoeberl and others 2024 preprint on the open-archive site: bot check; not read (the journal version was read instead from the NASA server).
- A NOAA repository page that a search returned (item 52562): refused an automated client (403); not read, content unknown.
- A Lauder (45 S) or other southern mid-latitude ground lidar paper giving the layer's base and top month by month in 2022: not found in two searches. The Lauder lidar appears only as the optical-depth curve in APARC Figure 3.7a.
- Sicard 2025 Figure 2 (the ten-year optical-depth record over Réunion) and the lower edge of the layer in their Figure 3b for mid-2022: not read.
- Knepp 2024 Figure 20 and APARC Figure 3.3 (effective radius against height at southern mid-latitudes, month by month): not read.
- Khaykin 2022 Figure 10c (the "4-5-fold increase"): the saved copy is page text without the figure; not seen.
- Taha 2022 Figure 3a (OMPS-LP at 869 nm, zonal mean, first five months of 2022): present in `src4`, not read for values.
- Saved but not quoted (early plume at 21 S in January 2022, or not about Hunga): `q4_kloss2022_insu-03776982.pdf` (Kloss and others 2022, Geophys. Res. Lett., balloon and lidar at Réunion), `q4_baron2023_hal-04097273.pdf` (Baron and others 2023, Geophys. Res. Lett., lidar at Réunion), `q4_zhu2022_insu-03857159.pdf` (Zhu and others 2022, Commun. Earth Environ., model), `q4_wrana2023_acp-23-9725-2023.pdf` (Wrana and others 2023, Atmos. Chem. Phys. 23, 9725-9743; mentions Hunga in one sentence only). The file `src4/li2023_acp-23-15351-2023.pdf` is about the 2021 La Soufrière eruption, not Hunga.
- Journal volume numbers for Duchamp 2023 and Schoeberl 2024 were not in the saved copies and are left out rather than given from memory.
