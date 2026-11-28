# Southern SQM records that log through twilight: sources and formats

Search made on 28 November 2026, 04:50 to 05:16 UTC (26 of the 40 minutes allowed; nothing was cut off by the clock, but see "What I could not check" at the end).
Downloads are in `/home/agent1/night/lit/src6/`. No readings were compared between years. The only values quoted are the two ends of the range in one sample file per station, as asked.

**Short answer.** Four stations meet every condition, and all four come from one source: the Globe at Night Sky Brightness Monitoring Network (GaN-MN). They are Buenos Aires (Argentina), Oamaru (New Zealand), Ouro Fino (Brazil) and NamibRand (Namibia). The observatory sites (Sutherland, Cerro Tololo, Siding Spring) do have an open SQM series through the Las Cumbres Observatory weather service, but it holds 2022 and not the same months of 2021 or 2024. The La Silla SQM of Fiorentin and others is on request only.

## 1. Stations that meet every condition

All four are in the same files, so the address, format and licence are given once below the table.

| Station (file code) | Place | Lat | Lon | Model (as listed by the network) | Interval | Months present, 2021 to 2024 | Address and format | Twilight readings in the sample (June 2022) | Licence |
|---|---|---|---|---|---|---|---|---|---|
| Almendra HackLab Observatory (`AHO`) | Buenos Aires, Argentina | -34.58868 | -58.41320 | SQM-LU-DL-R1, serial 4633 | 30 s, day and night | 2021: all twelve months. 2022: Jan to Sep, Nov, Dec (Apr: seen on 3 Apr only; Aug: only 1 to 4 Aug; Oct: not seen). 2023: Jan to about 10 Jun, then not seen. 2024: 11 Jan to Dec | GaN-MN monthly network CSV, rows with `device_code` = `AHO`; comma-separated, time in UTC, reading in column `nsb` | Yes. Readings run from 17.92 down to 5.88; 0 is written when saturated in daylight. 5104 rows with the Sun 2 to 10 degrees down | None stated |
| The Rogue Astronomer (`Oam`) | Oamaru, South Island, New Zealand | -45.077068 | 170.980597 | SQM-LE, serial 5601 | 30 s, day and night | 2021: Sep to Dec (installed 24 Aug 2021). 2022, 2023, 2024: every month | GaN-MN monthly network CSV, rows with `device_code` = `Oam`; comma-separated, time in UTC, reading in column `nsb` | Yes. 21.12 down to 5.96; 0 in daylight. 6111 rows with the Sun 2 to 10 degrees down | None stated |
| Polo Astronomico Ouro Finense (`PAOF`) | Ouro Fino, Minas Gerais, Brazil | -22.35 | -46.2 | SQM-LE, serial 2993 | 49 s, from about sunset to about sunrise | 2021: Jan to Mar, Aug to Dec. 2022: Jan to Oct, Dec. 2023: Jan to Sep, Dec. 2024: Mar to Dec | GaN-MN monthly network CSV, rows with `device_code` = `PAOF`; comma-separated, time in UTC, reading in column `nsb` | Yes. 22.20 down to 5.99. 2776 rows with the Sun 2 to 10 degrees down | None stated |
| NamibRand Nature Reserve (`Nrnr`) | Namib Desert, Namibia | -24.94899 | 16.03956 | SQM-LU, serial 1918 | 300 s, from about sunset to about sunrise | 2021: none (installed 10 Apr 2022). 2022: Apr to Aug, Oct to Dec. 2023: Jan to Aug, Oct to Dec. 2024: every month | GaN-MN monthly network CSV, rows with `device_code` = `Nrnr`; comma-separated, time in UTC, reading in column `nsb` | Yes. 23.96 down to 7.36. 269 rows with the Sun 2 to 10 degrees down | None stated |

Coordinates, model, serial and interval are from the network's own device table (inside `http://(the network's map server)/map/map.php`, the map frame of `http://globeatnight-network.org/map.html`). The Ouro Fino position is rounded in that table.

**The pairs of months each station gives** (the condition was June, July or August 2022 and the same month of 2021 or 2024):

| Station | 2022 | 2021 | 2024 |
|---|---|---|---|
| `AHO` | June: all 30 days. July: every day sampled (all 31). August: 1 to 4 Aug only | June, July, August: present on days 1 and 2 (the only days looked at) | June, July, August: every day sampled |
| `Oam` | June: all 30 days. July, August: every day sampled | None before 24 Aug 2021; not seen on 1 to 2 Aug; late August not looked at | June, July, August: every day sampled |
| `PAOF` | June: all 30 days. July: at least 22 days. August: at least 19 days | August: present on 1 to 2 Aug. Not present at the start of June or July | June: at least 18 days. July: at least 20. August: at least 20 |
| `Nrnr` | June: 22 of 30 days. July: at least 18 days. August: at least 15 days | None | June: at least 16 days. July: at least 15. August: at least 16 |

"At least" is because I did not download those months whole. I took 48 short slices spread through each file, and a slice only shows a night-only logger when it falls in that station's night. June 2022 was downloaded whole, so its day counts are exact.

**Where the files are.** Page: `https://globeatnight.org/gan-mn/`. One CSV per month holds the whole network (170 to 280 MB each, every station mixed together). For 2022 onward each month is a separate file on Google Drive, reached by a short link on that page. The 2021 months are inside one zip. No login is needed. A direct fetch works with

`https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t`

and the file arrives named `GaN-MN_<Month>_<Year>.csv` (for example `GaN-MN_June_2022.csv`). Byte ranges are honoured, so part of a file can be fetched.

| Month | Short link on the page | Drive ID | Bytes |
|---|---|---|---|
| 2021, all months (`GaN-MN_2021.zip`, members `2021/GaN-MN_<Month>_2021.csv`, deflated, 17 to 26 MB each) | `https://bit.ly/4u9eA9W` | `1qAOBOc81KCCV3sibYhzVMD378Nh1F5ag` | 267879844 |
| Jun 2022 | `https://bit.ly/3H5CsWS` | `1PN3rrCQ7z8f48tSm6QWEsfnd6tmcyBBo` | 212139801 |
| Jul 2022 | `https://bit.ly/3Z487OD` | `1bL1LW_FCnUqHWLGtN9savbQRHwLNX0z9` | 242994848 |
| Aug 2022 | `http://bit.ly/40hFpdP` | `1t5d_BE2gnrh_usEXnx9n1nrR7Jn1uZHc` | 231717891 |
| Jun 2023 | `https://bit.ly/46Es4OL` | `1yXlU75dIJ4KayIhB5VNaH4377VXhEu6O` | 200355883 |
| Jul 2023 | `https://bit.ly/3S3mG3u` | `145TbQIsXg2wRy3OJAjKp86wNN78v4vcN` | 220231536 |
| Aug 2023 | `https://bit.ly/3So1UKV` | `1Czbu6U_4dSLc0LcJ-kppfiFGvLtk9stO` | 208961293 |
| Jun 2024 | `https://bit.ly/3ZvT1DR` | `1y7UsA9TX3xJQ5hqIPjRiSSZBnwucQ-wo` | 179557476 |
| Jul 2024 | `https://bit.ly/4fAjvJi` | `1LIvDTLYou6t58zaVC-MCRvA-wMEaC0Qn` | 183299229 |
| Aug 2024 | `https://bit.ly/40BzVf7` | `1kmigc71PlrGfXshc4nHC5S5LzHlgDfN5` | 178002243 |

The other months of 2022 to 2024 are linked the same way from the page; all 36 resolved to a Drive file when I tried them.

**Format.** CSV, UTF-8 with a byte-order mark, one header line:

`id,created,received_utc,received_adjusted,sqmle_serial_number,nsb,sensor_frequency,sensor_period_count,sensor_period_second,temperature,device_code`

- `received_utc` is the time of the reading in UTC (`YYYY-MM-DD HH:MM:SS`); the file is sorted on it.
- `received_adjusted` is the station's local clock time (a fixed offset per station: 3 hours behind UTC for `AHO` and `PAOF`, 12 ahead for `Oam` in the June sample).
- `created` is the server's clock, stamped in batches (4 hours behind UTC in the sample). Not the time of the reading.
- `nsb` is the reading in magnitudes per square arcsecond. The other sensor columns are the raw output of the unit; `temperature` is the unit's own.
- `device_code` is the station.
- `AHO` and `Oam` log round the clock and write `nsb` = 0 while saturated in daylight, so 0 is a flag, not a reading. `PAOF` and `Nrnr` log at night only; in June 2022 they started and stopped with the Sun between 0 and 2 degrees above the horizon, so both twilights are inside the record.

**Licence.** Not stated for these files. The GaN-MN page says only: "Data released are provisional as there is only limited quality check. Please contact GaN-MN ((address on the network's page)) for details." Two neighbouring statements point in different directions and neither names these files:
- `https://globeatnight.org/maps-data/` says "Globe at Night data is made available under a Creative Commons Attribution 4.0 International License."
- `https://nightsky.physics.hku.hk/en-hk/research/data-visualization-download`, the University of Hong Kong page that also links the download, carries general terms forbidding copying or redistribution of that website's content unless otherwise specified.

**Sample.** `src6/ganmn_2022-06.csv` (whole June 2022 file, 212 MB). Slices of other months are in `src6/ganmn_probes/`.

## 2. Stations that nearly meet the conditions

**Tura Beach, Merimbula, New South Wales, Australia (GaN-MN code `Tura`).** -36.8477, 149.935. SQM-LE, serial 1727, 60 s, day and night. Same files and format as above. Present from 11 Jan 2022 to about 10 Feb 2024: all 30 days of June 2022, every day sampled in July 2022, at least 29 days of August 2022, and every month of 2023. Missing: there is no 2021 (not yet installed), and it was not in any slice of June, July or August 2024. Twilight readings: yes; in June 2022 they run from 22.74 down to 5.83, with 0 in daylight, and 2638 rows have the Sun 2 to 10 degrees down.

**Las Cumbres Observatory sites: Sutherland (`cpt`), Cerro Tololo (`lsc`), Siding Spring (`coj`).** This is the nearest thing to the observatory logs asked about.
- Positions (Brown and others 2013, Table 1; read as arXiv:1305.2437, saved as `src6/arxiv_1305.2437.pdf`): Sutherland -32.3806, 20.8101; Cerro Tololo -30.1673, -70.8046; Siding Spring -31.2729, 149.0708.
- Instrument: the same paper says "We employ a Campbell Scientific CR1000 data logger, with Vaisala pressure and temperature/humidity sensors, Boltwood cloud sensors, Unihedron SQM-LE sky brightness monitors".
- Address: `https://weather-api.lco.global/query?site=<cpt|lsc|coj>&datumname=Weather%20Sky%20Brightness%20Value&start=<YYYY-MM-DDTHH:MM:SS>&end=<...>&agg=False`. No login. Documented at `https://developers.lco.global/#weather` ("The weather API does not require authentication"). As documented, it returns 15-minute averages, at most 1000 of them (about 12 days) per call. With `agg=False` it returns every stored row. That switch is in the published source (`https://github.com/LCOGT/weatherapi`, file `weather.go`) and is used by the observatory's own weather page, but it is not in the documentation.
- Format: a JSON list of `{"TimeStamp", "Value", "ValueString", "TimeStampMeasured"}`. Times are UTC (ISO, ending in Z). `Value` is in magnitudes per square arcsecond. At Sutherland every time step has a second row with `Value` 0 and `ValueString` "NaN".
- Interval in the samples: 15 s at Sutherland and Siding Spring, about 75 s at Cerro Tololo.
- Twilight: yes in the samples (evening of 15 June 2022). Sutherland, 15:00 to 18:00 UTC: 20.76 down to 5.77. Siding Spring, 06:30 to 09:30 UTC: 20.08 down to 5.76. Cerro Tololo, 21:10 to 24:00 UTC: 21.48 down to 1.95.
- What is missing: the years. Whole-month queries for June, July and August of 2021 and of 2024 returned nothing at all three sites. Ten-minute windows at local midnight on the 15th of every month show data from January 2022 to May 2024 and again in December 2024, nothing in 2021, nothing June to November 2024. Within that span Siding Spring has nothing after March 2023, Cerro Tololo is thin (1 to 12 rows per ten minutes) and has gaps, and Sutherland from November 2022 mostly returns one repeated value.
- A doubt about the twilight part: the paper describes this channel as "sky brightness (solar insolation in daytime, sky brightness in V mag arcsec-2 at night)". So the bright end may come from a different sensor than the SQM. The Sutherland and Siding Spring values carry 4 to 6 decimals, which is not what an SQM-LE prints. I found nothing that says which sensor feeds the twilight values.
- Licence: none stated for the data. The API code is GPL-3.0.
- Samples: `src6/lco_cpt_skybrightness_2022-06-15_probe.json`, `src6/lco_lsc_skybrightness_2022-06-15_evening.json`, `src6/lco_coj_skybrightness_2022-06-15_evening.json`; month probes in `src6/lco_probes/`. (`src6/lco_cpt_skybrightness_2022-06_aggTrue_probe.json` is a second Sutherland piece, 1 to 2 June 2022, fetched while testing the switch.)

**Anglo-Australian Telescope, Siding Spring.** About 31.28 S, 149.07 E (from memory, not on the page).
- Instrument, from `https://aat-ops.anu.edu.au/AATdatabase/met.html`: "We have a Unihedron Sky Quality Meter (SQM-LR - serial port interface) mounted near the AAT. It points slightly south of the zenith and records data during the night once per minute."
- Address: `https://aat-ops.anu.edu.au/met/metdata.file` is a rolling file of about the last ten days (1.1 MB). The same directory, `https://aat-ops.anu.edu.au/met/`, holds a few saved copies: `metdata.file.20240827a` (16 to 26 Aug 2024), `metdata.file_cr20240826` (saved 21 Aug 2024, not opened), `metdata.file.saved_cr_20230310`, three from August and October 2020, and older ones.
- Format: tab-separated; a date line (`" mm-dd-yyyy."`) before each one-minute row; local standard time with no daylight saving; 20 columns named in `https://aat-ops.anu.edu.au/met/metdata_headers.txt`; the last column, "Sky Quality", is the SQM, and is 0.00 in daylight. (An earlier column named "Sky Brightness" is a different sensor, in counts.)
- Twilight: in the 16 to 26 Aug 2024 copy the nonzero readings run from 23.46 down to 2.0.
- What is missing: 2022 altogether, and any whole month. The long archive ("AAT Weather Data", `https://datacommons.anu.edu.au/DataCommons/item/anudc:4897`, 172 files, 178 MB, from 29 Jan 2013) is behind a "Request data files" form, so I did not go further; I do not know whether it reaches 2021 or carries the SQM column.
- Licence: the archive record points to `http://site.aao.gov.au/copyright.html`; not read.

**Bundaberg Urban Glow, Queensland, Australia** (about 24.9 S). `https://data.gov.au/data/dataset/bundaberg-urban-glow-data`. 75 "Sky Quality Meter (SQM) sensors", Creative Commons Attribution 4.0, one zip per night holding an ArcGIS file geodatabase, times in Australian Eastern Standard Time. Missing: the interval is 15 minutes (the limit was 11); the nights run March 2020 to September 2021 only, so no 2022; a search summary says readings are taken between 8 pm and 2 am only, which would leave out twilight (I did not open a zip to confirm). The page does not say the sensors are Unihedron's.

**SAAO, Cape Town (GaN-MN code `SAAO`).** -33.93, 18.478, SQM-LE, serial 2819, listed since 2015. No rows in any slice of any month of 2021 to 2024.

**Skynet Observatory, Lima, Peru (GaN-MN code `SkO`).** Present from July 2022, but at about 12 S it is north of the 15 S limit.

**La Silla, Chile (Fiorentin and others 2025, Sensors 25, 516).** Not open. The data availability statement reads: "Data underlying this paper will be shared on reasonable request to the corresponding author". The paper's text gives no address for the data. Its monthly values cover 2018 to early 2024.

## 3. Sources looked at that gave nothing

- Unihedron SQM database, `https://unihedron.com/projects/darksky/database/` (CSV at `...index.php?csv=true`): about 17,300 single hand-entered readings, not time series; 68 of them south of 15 S in 2021 to 2024.
- Unihedron user contributions, `https://www.unihedron.com/projects/darksky/downloads/index.txt`: programs and map files only.
- ESO ambient conditions database, `https://archive.eso.org/eso/ambient-database.html`: weather and seeing for La Silla and Paranal; no sky brightness product.
- Zenodo (`https://zenodo.org/api/records`, eleven queries on the instrument names and on each southern country): no southern SQM time series. Nearest: record 3248992, a talk on La Silla sky brightness (slides only); record 24070878, a notebook for SQM-LU-DL data from Panama (north).
- DataCite (`https://api.datacite.org/dois`, seven queries; covers Zenodo, Figshare, Dryad, PANGAEA, Mendeley Data and institutional repositories): no southern SQM time series.
- Spanish network, `https://guaix.fis.ucm.es/reecl/SQM-REECL`: Spain only.
- Angeloni and others 2024 (Astronomical Journal 167, DOI 10.3847/1538-3881/ad165c; arXiv:2312.10542), Chilean night sky: all-sky camera campaigns, not continuous SQM logs.
- SAAO Sutherland: web search found only the all-sky transmission monitors (a different instrument) and student project notes; no SQM log.
- Mount John (New Zealand): web search found only hand-held SQM readings in a 2015 dark-sky reserve report.
- Cerro Tololo, Cerro Pachon, Las Campanas, Paranal own pages; the HESS site; Reunion; Argentine and Brazilian observatories (CASLEO, Pico dos Dias): web searches in English, Spanish and Portuguese found no published SQM log.
- Svalbard SQMs (`https://data.iadc.cnr.it/erddap/tabledap/skyquality_meters_sqm_gruvebadet`), the Dutch, Austrian, Italian and central European networks, Ballyhoura (Ireland): open SQM data, but northern.
- Heidelberg light-pollution service, `https://dc.zah.uni-heidelberg.de/lightmeter/q/data/form`: a different make (Lightmeter); not opened.

## 4. What I could not check

- **Month lists for the GaN-MN stations rest on slices, not whole files**, except June 2022. For 2022 to 2024 each month had four slices of about an hour; June, July, August of 2022 and 2024 had 48 more. For 2021 I could only read the first one to one and a half days of each month (the members of the zip are compressed, so only their beginnings can be read without taking the whole). "Not seen" for a night-only station can mean the slices missed its nights.
- **Twilight was checked in June 2022 only** for the GaN-MN stations. I did not check that the other months, or 2021 and 2024, log the same hours.
- **A TESS-W beside an SQM:** I found no southern site where this is stated. I did not compare the positions above against a TESS-W station list.
- **Las Cumbres:** why 2021 and June to November 2024 return nothing (never stored, or removed), and which sensor gives the twilight values.
- **Pages that refused or failed:** `https://www.mdpi.com/1424-8220/25/2/516` and `https://darksky.org/night-sky-data-to-the-people` (refused; the paper was read at `https://pmc.ncbi.nlm.nih.gov/articles/PMC11768471/`); `https://data.gov.au/data/dataset/bundaberg-urban-glow-data` (refused; read through `https://data.gov.au/data/api/3/action/package_show?id=bundaberg-urban-glow-data`); `https://suthweather.saao.ac.za/` (certificate error, left alone).
- **Not searched at all:** Figshare, PANGAEA and Dataverse through their own search pages (only through DataCite); national data portals other than Australia's; GitHub beyond one web search.
- Scripts used are in `/tmp/scout6/`.
