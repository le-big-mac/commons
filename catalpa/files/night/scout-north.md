# Northern sky-brightness meter records for 2018 to 2020: sources, formats, fetch recipes

Scouted 28 Nov 2026, 07:56 to 08:26 UTC. No readings are given anywhere below; in every row layout each reading is replaced by `x`.

**Result in one line: I found no source that meets all the conditions and can be fetched from this machine today.** One network (Kraków) might meet them for up to three stations if its server answered; I could not verify its months or its twilight coverage. One (Upper Austria, 23 stations) offered minute values for chosen periods until its download was withdrawn; I could not check its twilight coverage either. Everything else falls short on a named condition. Details follow.

## 1. Sources that meet every condition

None verified.

| Network | Stations meeting the conditions | Why the row is empty |
|---|---|---|
| (none) | 0 | See section 3. The two nearest are Kraków (server did not answer; archive copies are cut at 1 MB) and Upper Austria (download no longer offered). |

## 2. Fetch recipes

Because nothing qualifies, these are recipes for the sources that can actually be fetched now (each falls short on one condition, stated), plus the recipe to try for Kraków from another network.

### 2a. Kraków network (Cracow University of Technology, light pollution monitoring laboratory) — to try from another machine

- Listing page: `http://lightpollution.pk.edu.pl/CLPRG/pomiary.php` (station list with one link per station). Per-station pages with several files: `CLPRG/Dobczyce.php`, `Skala.php`, `Zabierzow.php`, `Wieliczka.php`, `NowaHuta.php`.
- Files (same host, under `/CLPRG/Dane/` and also `/Dane/`):
  - `Dane/Dobczyce/SQMReadings2014-2020.tar` (the page says 21.02.2014 to 14.09.2020), then `20220301_075128_.dat`, `20230317_084425_.dat`, `20230801_133347_.dat`
  - `Dane/Suhora/SQMReadings.txt`
  - `Dane/MOA/sqmSQMReadings.txt`
  - `Dane/Botaniczny/SQMReadings.txt`
  - `Dane/Kasinka/`, `Jerzmanowice/`, `Lagiewniki/`, `Poronin/`, `Klecza/`, `Bolecina/` each `SQMReadings.txt`
  - `Dane/Skala/OAUJ.txt`, `Dane/Skala/Skala_2021-.zip`; `Dane/Zabierzow/Zabierzow_2012-2019.txt`; `Dane/Wieliczka/SQMReadings_2019_2021.txt`
- What "not there" looked like from here: no answer at all. `curl` to `lightpollution.pk.edu.pl` ((server address left out)), ports 80 and 443, timed out three times (25 to 30 s each). I do not know whether the server is down or drops this machine's network.
- Fallback that does not work: the Internet Archive has copies (`https://web.archive.org/web/<timestamp>id_/<address>`, range requests honoured), but each text file is cut at 1,048,576 bytes (OAUJ.txt at 5,242,880), and the Dobczyce tar is not archived.

### 2b. Dutch, German and Danish coast network "Was het donker" (no 2018)

- Listing first: `https://www.washetdonker.nl/data/?dir=<Station>` gives year folders; `?dir=<Station>/<YYYY>` gives months; `?dir=<Station>/<YYYY>/<MM>` gives files.
- File: `https://www.washetdonker.nl/data/<Station>/<YYYY>/<MM>/<YYYYMMDD>_120000_SQM-<Station>.dat` (one file per noon-to-noon day, about 100 kB; range requests honoured).
- Not there: a missing file answers 404 (236 bytes of HTML). A missing folder answers **200 with the top-level listing**, so a program must check that the page contains links beginning `?dir=<Station>/<YYYY>/`.

### 2c. Madrid, Universidad Complutense (no twilight)

- `https://zenodo.org/api/records/4633001` (JSON; `files[].key`, `size`, `links.self`).
- File: `https://zenodo.org/api/records/4633001/files/SQM_evol.csv/content` (26,812,838 bytes; range requests honoured, answer 206).
- Not there: Zenodo answers 404 with a JSON body.

### 2d. Galicia, MeteoGalicia (latest ten minutes only)

- Stations: `https://servizos.meteogalicia.gal/mgrss/observacion/listaEstacionsMeteo.action` (JSON, 167 stations: `idEstacion`, `estacion`, `lat`, `lon`, `altitude`, `concello`, `provincia`).
- Latest record: `https://servizos.meteogalicia.gal/mgrss/observacion/ultimos10minEstacionsMeteo.action?idEst=<id>` → `listUltimos10min[].instanteLecturaUTC` and `listaMedidas[]` with `codigoParametro`, `nomeParametro`, `unidade`, `valor`, `lnCodigoValidacion`. The sky meter is `BCN_AVG_1.5m` ("Brillo do Ceo Nocturno", unit printed as `mag/arsec2`).
- History, hourly only: `.../datosHorariosEstacions.action?idEst=<id>&dataIni=dd/MM/yyyy HH:mm&numHoras=<n>[&idParam=<code>]`. Not there: `{"dataIni": "...", "listHorarios": []}`. Asking for `BCN_AVG_1.5m` gives that empty answer for 2018, 2019 and 2020; without `idParam` the 2018 and 2026 answers list 11 or 12 weather parameters and no sky brightness.

### 2e. Veneto, ARPAV (last few days only)

- `https://api.arpa.veneto.it/REST/v1/meteo_brillanza_tabella?codseqst=<station code>` (JSON). The page that calls it is `https://www.arpa.veneto.it/dati-ambientali/dati-in-diretta/luminosita-del-cielo/brillanza`. Not called by me; the page's own code passes no date.

### 2f. Smaller things that answer

- Las Cumbres weather service: `https://weather-api.lco.global/query?site=<elp|ogg|tfn>&datumname=Weather%20Sky%20Brightness%20Value&start=<ISO>&end=<ISO>&agg=False`. Not there: the body is the JSON word `null`.
- Spanish network repository: `http://sdc.cab.inta-csic.es/pdd/jsp/busSQM.jsp?ins=<instrument>&date_d_i=01&date_m_i=01&date_y_i=<YYYY>&date_d_e=31&date_m_e=12&date_y_e=<YYYY>&order=sqm_end&result=100&pag=1&submit=Buscar`; files at `descargarSQM.jsp?id=<n>&type=sqm`. Not there: the words "Sin resultados".
- Svalbard: `https://data.iadc.cnr.it/erddap/tabledap/skyquality_meters_sqm_gruvebadet` and `..._antonswerk` (ERDDAP).

## 3. Sources that nearly meet the conditions, and why they fall short

Ordered by how close they come.

### 3.1 Kraków network, Poland (about 49.5 to 50.2 N) — server unreachable from here

What I could establish, all from Internet Archive copies (pages captured 4 Dec 2024 and 13 Jan 2025; file heads and tails only):

- **Stations** (the network's own page): 1 DOB Dobczyce reservoir water intake; 2 SUH Suhora observatory; 3 FSK Fort Skała observatory; 4 ZAB Zabierzów; 5 MOA youth observatory, Niepołomice; 6 BOT Botanical Garden, Kraków; 7 WIE Wieliczka; 8 KAS Kasinka Mała; 9 JER Jerzmanowice; 10 KLA Kraków-Łagiewniki; 11 POR Poronin; 12 KLD Klecza Dolna; 13 ABO Andrychów-Bolęcina; 14 NHU Nowa Huta. The page says the databases are from SQM-LE and SQM-LU-DL meters.
- **Stations that could cover 2018 and 2019:**

| Station | File | Format | First time stamp | Step | Size at the origin (from the archive's record) | Covers 2018–2020? |
|---|---|---|---|---|---|---|
| DOB | `SQMReadings2014-2020.tar` | not seen | page says 21.02.2014 | not seen | not known | Page says to 14.09.2020. Not archived, not opened. |
| SUH | `Suhora/SQMReadings.txt` | CSV, first header `Date/Time,MPSAS,NELM,SerialNo,Protocol,Model,Feature,Temp(C)`; by 29 Aug 2015 the rows have 13 fields | 2015-02-02 12:44:02 | 10 min at the start | 30,906,528 bytes, modified 3 Jun 2024 | Likely by size; not verified. The archived megabyte ends 2015/08/29. |
| MOA | `MOA/sqmSQMReadings.txt` | "Produced by SQM Reader Pro 3.0.0.0", then `Year/Month/Day,Hour/Minute/Second,MPSAS,NELM,SerialNo,Protocol,Model,Feature,Temp(C),EncOffset,SolarAlt(deg),LunarAlt(deg),LunarPhase` | 2017/12/14 09:56:17 | 5 min | 17,905,416 bytes, modified 13 Jan 2025 | Possibly; not verified. The archived megabyte ends 2018/04/17. |
| BOT | `Botaniczny/SQMReadings.txt` | IDA-style header (37 lines), SQM-LU-DL-R1, serial 3704, firmware 4-6-48 | 2018-12-20T09:10:08 UTC | 10 min | 17,849,289 bytes, retrieved from the logger 2021-11-25 | No: starts 20 Dec 2018. |

- **Other stations start too late or stop too early:** KAS from 10 Nov 2019 (serial 3706, 5 min); JER from 20 Dec 2020 (serial 4772); KLA from 22 Dec 2020 (serial 3705); POR from 22 Feb 2021 (serial 4854); KLD from 11 Feb 2023 (serial 5317); ABO from 16 Jun 2023; FSK 27.08.2014 to 21.03.2018 then from 22.07.2021 (serial 2744 in the first file); ZAB "selected nights" 2012 to 2019; WIE has a file named `SQMReadings_2019_2021.txt` whose caption gives the period as "25.08.2021 to 28.03.2021" (inconsistent as printed), then data from 28.04.2022; NHU from 27.04.2022.
- **Row layouts.** SQM-LU-DL files: `2019-11-10T15:40:08.000;2019-11-10T16:40:08.000;x;x;x` (UTC; local; Celsius; Volts; mag/arcsec^2; newer files add a sixth field `Init/Subs`). Suhora at the start: `2015-02-02 12:44:02,x,x,x,x,x,x,x`. Reader Pro files: `2017/12/14,15:28:06,x,x,x,x,x,x,x,x,x,x,x`.
- **Time zone.** The logger files carry both UTC and local time and name the zone (`Europe/Warsaw`; the Botanical Garden file says `Europe/Vienna`). The Suhora and MOA files have one time column with no zone stated; the MOA file's `SolarAlt(deg)` column would let the zone be checked.
- **Twilight.** Not established. Suhora's first rows run through midday at 10-minute steps, so it logged round the clock at least at the start. At MOA, after three test rows in the morning, the first evening's rows begin at 15:28:06 on 14 Dec 2017 and continue every 5 minutes. By my formula the Sun was then 0.3° above the horizon if the stamp is Central European Time, and 7.8° below if it is UTC (I took Niepołomice as 50.03 N, 20.22 E from memory, not from the file). In the first case the meter logs from sunset and twilight is in the file; in the second it is not. The archived megabyte holds 124 days at about 62 bytes a row, that is about 136 rows or 11 hours a day on average, a little less than whole nights for December to April.
- **Positions in the headers:** Kasinka 49.6833, 20.0333 (an earlier copy: 49.691628, 20.038596); Jerzmanowice 50.2, 19.75, 450 m; Łagiewniki 50.002777, 19.941668, 250 m. Blank for the Botanical Garden, Klecza and Poronin. The Fort Skała header says 54.0, 22.5, which is not where Kraków is; treat it as a placeholder. Suhora and MOA files carry no position.
- **Unit changes:** one serial number per logger file; nothing else is said. The Suhora file changes its column layout during 2015, which may mean a change of logging program.
- **Terms** (on `pomiary.php`, my translation from Polish): the owners "consent to the use of the data contained in the above databases by authorised users on condition that the source of the information is given. Copying and publication of the data contained in the databases requires the owner's separate consent each time." The logger files' headers also carry the line "ODbL 1.0", which is the default text the Unihedron program writes.
- **Why it falls short:** not fetchable from here (see 2a); the 2018–2020 months are inferred from file sizes and a page caption, not seen.

### 3.2 Upper Austria (23 SQM stations, 47.5 to 48.7 N) — download withdrawn

- The network's page `https://www.land-oberoesterreich.gv.at/159659.htm` now says the earlier meters were replaced by TESS-W photometers in the STARS4ALL network, and links only to those. (That is the network you already have.)
- The archived copy of 15 Apr 2021 linked "Licht - Messwerte (Daten-Download) … über frei wählbare Zeiträume" at `www2.land-oberoesterreich.gv.at/imm/Start.jsp?...forward=IMM2013LuftgueteAktuellDetail&controllerKategorie=Lichtmessnetz&showLichtmessnetz=true`. That form still opens, titled "Licht - Messwerte", and still offers "MMW (Minutenmittelwert)" and "TMW/NMW", but its station list and component list are empty. With `controllerKategorie=AlleMessnetzte` it lists 20 air stations and 16 air and weather components, no light.
- Not tested: whether the service still answers if given the old light-station codes directly. I could not find the codes (the Internet Archive went offline while I was looking), and I did not guess.
- Stations, positions and start dates from `https://nightsky.univie.ac.at/` (decimal degrees converted by me): BOD Bodinggraben 47.7919, 14.3939 (2016-06-29); BRA Braunau 48.2611, 13.0447 (2014-09-06); GIS Giselawarte 48.3842, 14.2531 (2014-09-01); GRI Grieskirchen 48.2344, 13.8258 (2015-05-21); GRU Grünbach 48.5306, 14.5750 (2014-09-06); KID Kirchschlag-Davidschlag 48.4419, 14.2739 (2014-12-15); KRI Krippenstein 47.5231, 13.6933 (2015-11-04); LSM Linz Schlossmuseum 48.3053, 14.2828; LGO Linz Goethestraße 48.3053, 14.3083; LSW Linz Sternwarte 48.2933, 14.2683; STY Steyr 48.0492, 14.4422; STW Steyregg Weih 48.2886, 14.3536; MUN Münzkirchen 48.4792, 13.5581; WEL Wels 48.1564, 14.0247; ZOE Zöblboden 47.8383, 14.4411 (these eight, LSM to ZOE, all 2014-09-06); LOS Losenstein Hohe Dirn 47.9061, 14.4111 and ULI Ulrichsberg Schöneben 48.7056, 13.9456 (2015-05-21); MAT Mattighofen 48.0972, 13.1517, PAS Pasching 48.2586, 14.2100, VOE Vöcklabruck 48.0058, 13.6453 (2014-12-15); TRA Traun 48.2356, 14.2531 (2014-12-05). The 2018 plot page also lists FEU and FRE, which are not in that table.
- The Central European inventory (`https://darkersky4ce.inaf.it/instrument-sheet-upper-austrian-light-measurement-network/`) describes it as SQM, "every minute", "pointing 10° N of the zenith", download format "XLSX, PDF", policy "not specified".

### 3.3 Vienna, Mitterschöpfl, Graz, Potsdam-Babelsberg, Stockholm (University of Vienna site) — pictures only

- `https://nightsky.univie.ac.at/` gives yearly plot pages 2011 to 2024 (2018: BA1, IFA, FOA, GRA, STO and 23 Upper Austrian stations; 2019 without GRA; 2020 without FOA and GRA). All links on the 2018 page are PNG images.
- `https://nightsky.univie.ac.at/sqm/lv.php` offers a night-by-night picture (GIF) for SQM-LE at IFA, FOA2, BA1, GRZ, STO and five others, 3,593 nights from 23 Nov 2011 to 9 Jan 2023 in the list shown for IFA. Its text says the raw data have "a time resolution of about 7 seconds" (Graz 90 seconds). No data file is linked; the folder `.../sqm/IFA/` answers 403.
- Positions from the same table: IFA Vienna 48.2317, 16.3342 (since 2012-03-01); FOA Mitterschöpfl 48.0842, 15.9233 (2012-11-16); GRA Graz-Lustbühel 47.0672, 15.4936 (2014-01-01).

### 3.4 "Was het donker" (Netherlands, north German and Danish coast) — no 2018

- 89 station folders. None has a year folder before 2019. Eleven have 2019, with these months: Groningen-DeHeld 08–12; Groningen-ZernikeCampus 09–12; Roodeschool 09–12; Lauwersoog 10–12; Sellingen 10–12; Hornhuizen 11–12; Lochem, Heerenveen-Station, DeZilk, Boerakker, Ameland-Natuurcentrum-Nes 12 only. All eleven have a 2020 folder (months not listed by me). The full station-by-year list is in `scout9_tools/whd_years.out`.
- So it fails January to June of both years and all of 2018; one station has August to December 2019.
- Format (one file read, Lauwersoog 30 Oct 2019): 35 header lines starting `# Definition of the community standard for skyglow observations 1.0`; licence line "ODbL 1.0"; `Device type: SQM-LU`; `Instrument ID: SQM_LU-Lauwersoog`; `Position: 53.4, 6.6, 0`; `Local timezone: UTC+1`; `Time Synchronization: NTP`; `SQM serial number: 4602`; `SQM cover offset value: -0.11`; capture program PySQM. Columns: `UTC Date & Time, Local Date & Time, Temperature, Counts, Frequency, MSAS` in `Celsius;number;Hz;mag/arcsec^2`. Row: `2019-10-30T14:43:00.000;2019-10-30T15:43:00.000;x;x;x;x`. Step 42 s. The first row of that day is at 14:43 UTC, when the Sun was about 10° above the horizon there by my formula, so evening twilight is in the file. About 100 kB a day.
- An inventory sheet gives the network as "around 70" SQMs, "since 2020", format DAT, policy not specified.

### 3.5 Galicia, MeteoGalicia (42 to 43.5 N) — history not openly fetchable

- A paper found by search describes 14 SQM detectors in MeteoGalicia weather stations. I confirmed the parameter `BCN_AVG_1.5m` in the latest ten-minute record of Guísamo (id 19005; 43.307995, −8.276487), Paramos (19008; 43.00191, −8.6992) and Labrada (19015; 43.405445, −7.502042). Santiago-EOAS (10124) did not have it. Time stamps are UTC (`instanteLecturaUTC`), ten-minute averages.
- The documented open services give only the latest record (2d). The hourly history has no sky-brightness parameter.
- Ten-minute history exists in the website's interactive history page (`https://www.meteogalicia.gal/web/observacion/rede-meteoroloxica/historico`), but that page calls a different service (`apis-ext.xunta.gal/meteo2api/...`) with an application key built into the site's own code, and carries a captcha key. I did not use it.
- The old page `https://www.meteogalicia.gal/Caire/brillodoceo.action` (archived copy of 22 Sep 2023 has a "Descarga Datos" link and yearly reports 2014 to 2020) now answers 404, as does the old history address it linked to.

### 3.6 Madrid, UCM roof (40.45 N) — night only

- Zenodo record 4633001, "Evolution of Brightness and Color of the Night Sky in Madrid" (Robles and others, 24 Mar 2021), CC BY 4.0. `SQM_evol.csv`, 26,812,838 bytes. Header `Time(UTC);Magnitude`. Row `2012-10-10 19:12:45;x`.
- First stamp 2012-10-10 19:12:45, last 2020-02-05 05:47:27. Step 60 s in 2012, 42 s in the 2018, 2019 and 2020 samples. One station, so January to June and August to December of 2018 and 2019 may well be there (two mid-file samples fell on 14 Feb 2018 and 29 Jan 2019), but months were not listed.
- Why it fails: by my reckoning the Sun stood at −18.0° at the first stamp and −18.1° at the last, so the file is cut at astronomical twilight. Nothing between 3° and 5° can be in it. No unit information in the file.

### 3.7 Veneto, ARPAV (45 to 46.5 N) — no history offered

- The agency's page says 21 stations, readings "every five minutes during the whole night", including the University of Padova's meters at Cima Ekar and Pennar. The live service gives recent days (an inventory sheet says "last 3 days", JSON, policy not specified). The file folder of the theme holds PDF reports only (among them "scheda dati 2010_2020" and "Inquinamento luminoso e lockdown"). No historical data file found.

### 3.8 Others, each with the condition it fails

- **Spanish network repository** (`sdc.cab.inta-csic.es`): 43 SQM-LE and SQM-LU instruments, one file per night. The date menu stops at 2017 and a search for 1 Jan 2018 to 31 Dec 2020 returns "Sin resultados" (the same search for SQM_LE-VILLAVERDE in 2017 returns 183 results). No 2018–2020.
- **Baja Observatory, Hungary** (46.18028 N, 19.01093 E; SQM-LE; "every minute"; measurements began 2010-02-22): the open download (`http://www.bajaobs.hu/sqm/sqm_dat.php?mod=vesszo`) is described as "from the previous day's midnight"; the date-range download form has a password field. No open history. (My one sample request with a byte range got the answer "Nem nem nem"; I did not retry.) Two more meters on the same server, Kisgyőr (`/sqm2/`) and Hortobágy (`asterope.bajaobs.hu/sqm3/`), began in 2022.
- **Majadahonda, Madrid** (Zenodo 5709962, `tesstractor.tar.gz`, 576,158 bytes, CC BY 4.0): "SQM measurements at Majadahonda station 2019". One year only; not opened.
- **Tuscany** (Zenodo 17366428, Massetti, CC BY 4.0, one text file of 18,431,034 bytes, 2016 to 2019): the title says hourly data. Interval too long; not opened.
- **Wuxi, China** (Mendeley Data `tdypkrz755`, CC BY NC 3.0, `NSB data.xls` 630,784 bytes and a Spring Festival file): not opened; too small to be minute data for two years.
- **Teide and Roque de los Muchachos** (`https://ocan.iac.es/ot-sky-brightness/`): SQM-L, one reading every 20 s, but "starts taking data only when the Sun is 10 deg below the horizon"; a plot per night, no file seen.
- **Svalbard** (CNR, CC-BY-NC-SA-4.0): Gruvebadet 2024-02-18 to 2024-04-06, Antonswerk 2024-02-21 to 2024-03-11. Wrong years.
- **Las Cumbres northern sites** (McDonald `elp`, Haleakala `ogg`, Tenerife `tfn`): ten-minute windows in March 2018, October 2019 and October 2020 returned nothing at all three; October 2022 returned rows at `elp` and `tfn`. Nothing before 2022.
- **Central European inventory** (`https://darkersky4ce.inaf.it`, 16 ground-based sheets read): Rhön, 16 SQMs since 2020, interactive plots only (`himmelsmonitoring.de`); Peterberg since 2019, plots of the last two months; Goßdorf 2014 to 2020, one plot; Varese (Schiaparelli) since Aug 2017, plot of the current day; Gersbach since 2020 (file refused, see section 4); Lungau from 2025; Vienna's Kuffner network is a different instrument (Lightmeter, not a zenith meter) and unpublished; the project's own SQM-LE network (ODbL) is recent.
- **Oregon Skyglow network**: 5-minute SQM logs, but data are collected by volunteers and given on request by e-mail. Not open.
- **Unihedron user database** (your saved file): columns UT_datetime, Type, Brightness, Zenith, Conditions, Latitude, Longitude, Moon_alt, Moon_illum, ClearSkyClock, Site description, User. Single hand-entered readings, not logs (as the earlier scout found).

## 4. Searched and not found; what refused or failed

**Searched, nothing usable found:**
- Zenodo (ten queries) and DataCite (ten queries, datasets only; covers Figshare, Dryad, PANGAEA, Mendeley Data): only the records named above. RODBUK (Kraków's research data repository): nothing for the Kraków network.
- Hong Kong's older network: the university's data page links only the Globe at Night network.
- Japan: only the environment ministry's seasonal star-watching tables and a modelled map (Zenodo 22795811); no continuous log.
- Catalonia (Montsec, the regional network of SQM-LE meters begun in 2014): papers and a quality map, no download.
- Germany (Potsdam, Berlin, Bochum): papers only; Potsdam-Babelsberg appears only as pictures on the Vienna site.
- Ballyhoura and Ireland: a 2014 survey paper; no log.
- Czechia: a weather-service pilot with three SQM-LE meters; no download found. Slovakia: nothing found.
- Arizona, Kitt Peak, McDonald, Canada: papers and a photograph of the meters; no archive.
- Dutch earlier network (2009 to 2019): only the report PDF (Zenodo 4293366, CC BY 4.0, 3.4 MB; not opened). RIVM's data sets are calculated maps.
- Białystok (`https://labfiz.uwb.edu.pl/obserwatorium/sqmle/`): a plotting page with scripts dated Dec 2025; it returned no time stamps for a day in 2018 or in Nov 2026.

**Refused or failed:**
- `lightpollution.pk.edu.pl`: connection timed out (three tries).
- `https://staernwarten.de/wp-content/uploads/sqm/SQMReadings.txt` (Gersbach): 403.
- `https://nightsky.univie.ac.at/sqm/IFA/`: 403.
- `web.archive.org`: intermittent after some twenty requests from me. One file request was refused, two index queries got no connection, and a third got 503 "Temporarily Offline"; page fetches in between worked.
- `http://vivaldi.ll.iac.es/OOCC/ot-sky-brightness/`: no connection (the same page is at `ocan.iac.es`).
- `https://www.data.gv.at/katalog/api/3/action/package_search`: 404 (five queries).
- `https://noc.edu.pl/` (linked from the Kraków pages): redirects to an unrelated shop, 403.
- ARPAV's `++api++` content address: 504; the `/api/` address worked.

**Not done:**
- Months were not listed for any source except the Dutch 2019 folders.
- The Madrid Sun altitudes are from a short formula of my own (good to about a tenth of a degree), not from an ephemeris.
- I saw a few numbers I should not pass on (a dataset's range attributes, and a search summary quoting a paper); none is in this report.

**Files.** Samples and pages: `/home/agent1/night/lit/src9/` (178 files, 11 MB; includes about 1.7 MB of the Galician site's page code). Scripts: `/home/agent1/night/lit/scout9_tools/` (`peek.py` masks readings; `whd_years.py` and its output; `ds4ce_sheets.py`; `wb_headtail.py`). Several one-off checks were run inline and are not saved as scripts.
