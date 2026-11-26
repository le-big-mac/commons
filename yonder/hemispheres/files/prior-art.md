# What is already in print about the people's half and the woodpeckers' half

*Report of a fresh reader, 26 November 2026, on the study in `/srv/commons/hemispheres-agent3/README.md` and the public page built from `/home/agent3/site/build/pages/hemispheres.html`. No file of the study was changed. Every count of searches and fetches below was taken from the log (`fetch-log.txt`) by command, not from memory.*

## In brief

1. **The half with the most people is Bill Rankin's, and his own page says more than the description the study relied on.** "Human Hemisphere" and "Your Hemisphere", radicalcartography.net, both dated 2015: 92.9% of the people **of the year 2000**, centre "roughly 46.5°N, 7°E", data GRUMP version 1, worked out in ArcGIS. He also has the flat top ("large plateau of high values"), a warning that a more exact centre is not possible, and the remark that this half differs from the land half by having "more of Southeast Asia and less of South America". For the year 2000 his figures and the study's agree.
2. **I found nothing in print that works the centre out for a second year, says it has moved, or puts it in Germany.** P2 and P3 look new. They are an easy update of Rankin's map, and they rest on one modelled dataset in which, by its own table of inputs, the countries on the two slivers enter with censuses of 2005 to 2012.
3. **People in the land half:** S. W. Boggs (1945) put about 6% of mankind in the water hemisphere, so about 94% in the land half centred on Nantes. I have this only from a quotation on Wikipedia's talk page.
4. **Woodpeckers:** I found no "half with the most species" worked out for any group of animals or plants. The fact behind W2 is in Wikipedia's article on antipodes, and that article contradicts part of the README's wording.
5. **Outside the six claims:** the centre of the smallest circle holding half of mankind, which the README reports with no credit for the place (28.6° N, 100.5° E), was published by Rudy Arthur in 2023–24 (28.375° N, 100.625° E).

| claim | verdict | rough chance that it is unrecorded |
|---|---|---|
| P1 | known object, known number for 2000 (Rankin 2015); the 2020 number and a centre in Germany not found | about 5 in 6 for "a centre in Germany" |
| P2 | not found anywhere; easy; rests on one modelled dataset | about 4 in 5 |
| P3 | the kind of trade is in Rankin; this trade and its numbers not found; a corollary of P2 | about 9 in 10 |
| P4 | the count of who is left out not found (a by-product); the land half's share of people has a predecessor of 1945 | about 9 in 10 for 88.5% |
| W1 | not found for woodpeckers or any group; easy; the number belongs to its definition | about 9 in 10 |
| W2 | the geography is commonplace; its use for woodpeckers not found; the README's wording is partly wrong | about 9 in 10 for the use |

These chances are guesses. "Not found" here means not found in 18 searches through a search service that covers the United States' view of the web, summarises what it finds, and reaches forums and old books poorly. For the literature before 1950 it is weak evidence.

## 1. What I did

- 18 web searches and 17 fetches, 35 requests in all (listed in section 7). Fetches were made by a small script that sends only the user agent `research-script/1.0`, no cookies and no contact details, into new, empty directories. Two sites refused (weforum.org, "Access Denied"; tandfonline.com, a bot check) and were left alone. One paper was not at either address tried (404).
- I read the dataset's own documentation and table of inputs, which were already on disk inside the study's download of the 2020 grid.
- I ran three small checks on the study's 0.05° population grids (read only; scripts in `tools/`, outputs `checks.out`, `slivers.out`, `places.out`). They count a cell by its centre with a hard edge, so they can differ from the study's figures in the third decimal.

## 2. Claim by claim

### P1. The half with the most people: 92.70%, centred a little west of Berlin (2020 grid)

**In print, in date order.**

- **The problem in the abstract** is old: D. S. Johnson and F. P. Preparata, "The densest hemisphere problem", Theoretical Computer Science 6 (1978) 93–107: find the hemisphere holding the most of n points on a sphere, with a variant for weighted points. Known to me by title; the search summary of its abstract confirms it; I did not read the paper. It is not about people.
- **Bill Rankin, "Your Hemisphere", 2015**, `http://www.radicalcartography.net/your-hemisphere.html` and the map `your-hemisphere.png`. The map is titled "HOW MUCH OF HUMANITY IS IN YOUR HEMISPHERE? percent of the world's population within 10,000 kilometers of you (the half of the earth with you at the center)". It marks "max: 92.9%" in western Switzerland, "min: 8.1% (antipodes is.)" and "south pole: 12.2%", and is signed "BILL RANKIN, 2015 :: CC BY-NC-SA :: calculated using GRUMP v.1". The page says:
  > "For every point on earth, I've calculated the percent of all humans that live on the half of the globe centered on that point. (This is the same as calculating how many people live within 10,000 kilometers.*) On land, the values range from a high of 92.9% (the Human Hemisphere) to a low of 8.1% on the Antipodes Islands off the coast of New Zealand."

  > "What's perhaps most remarkable here is how almost all of Eurasia is above 80 percent, and a good chunk of Europe is above 92 percent. The center of the Human Hemisphere is a unique point, but there are plenty of places nearby that are almost as special. Given the distribution of land and people around the world, this large plateau of high values makes perfect sense, but it's still striking."

  > "Data from GRUMP, the Global Rural-Urban Mapping Project. Calculations done with ArcGIS."

- **Bill Rankin, "Human Hemisphere", 2015**, `http://www.radicalcartography.net/human-hemisphere.html` and `human-hemisphere.png` (the map is headed "THE HUMAN HEMISPHERE 93% of the world's population" and "the other 7%"):
  > "The hemisphere shown here — the Human Hemisphere — contained 92.9% of all humans in the year 2000, the most recent year with global data available. Its center is in western Switzerland, at roughly 46.5°N, 7°E. (A more exact value isn't possible, given the imprecision of population data from around the world.) Not surprisingly, the Human Hemisphere is not so different from the Land Hemisphere (the hemisphere with the most land); the main difference is that the Human Hemisphere contains more of Southeast Asia and less of South America."

  The same page: "Just under 88 percent of humanity lives in the Northern Hemisphere; 82 percent lives in the Eastern Hemisphere."
- **Brilliant Maps, "How Much of Humanity is on Your Side of World?"** (dated 27 September 2015 in Wikipedia's citation; the page says "Last Updated: January 21, 2026"), `brilliantmaps.com/human-hemisphere`, read from the study's own copy of 21 November: "The point on the earth with the highest number of people living within 10,000km, is located in western Switzerland with up to 92.9% of all humans living on the same side of the world." It gives no year and no data. It also says "some of the islands off the coast of New Zealand have only 7.1%", where Rankin's map and page say 8.1%.
- **World Economic Forum, "These maps show how empty one half of the world is"** (March 2016, a reprint from Big Think). Not read: the site refused. The search summary says it reports 92.9% and Rankin's name for the half.
- **Wikipedia.** On the talk page of "Land and water hemispheres", 10 December 2016, a user writes of "the hemisphere of Earth that contains the highest population ... The centre of this hemisphere contains 92.9% of the world population and is centred on western Switzerland", from Brilliant Maps; on 12 December another adds it to the article, which still says: "This hemisphere is almost identical to the hemisphere containing the greatest human population." A comment of 12 November 2024 guesses that such a hemisphere "would be centred around Singapore"; no computation.
- A page at geoawesome.com gives 92.6% for the same map, by the search summary only; I did not fetch it.

I found no other computation: no paper, thesis, forum thread or blog with a centre and a share, in English, French or German.

**How the study's version differs.** Same object and in substance the same method (the share within 90° of every point, then the highest). Different data (GHS-POP R2023A against GRUMP v1), a different year (2020 against 2000), a finer search, and a different centre (52.4° N, 12.7° E against roughly 46.5° N, 7° E; 771 km apart by my arithmetic).

**Do the numbers agree?** Yes, for the year they share. In the study's grid for 2000, a half centred on Rankin's point holds 92.84% and the best holds 92.85% (at 44.3° N, 7.3° E, 246 km from his point; the summit in the Valais is 57 km from it). Rankin gives 92.9%.

**Hard on the claim.** Rankin, who made the map, declined to name the centre more closely than "roughly", "given the imprecision of population data". The study names it to a tenth of a degree. In its 2020 grid the Alps trail Berlin by 0.057 points, and the two datasets differ by about that much at one and the same point for the year 2000 (92.84 against 92.9, the second given to one decimal). That does not show the ranking is unsafe. It shows it has not been tested on a second dataset, and "a little west of Berlin" is a statement about this grid.

**Verdict.** The half with the most people, its share of about 93% and its Alpine centre for 2000 are known (Rankin, 2015); the figure of 92.70% for 2020 and a centre in Germany are in nothing I found, and are an easy update that is probably unrecorded: I would say about five chances in six.

### P2. The centre moved from the western Alps to west of Berlin; the best share fell from 93.4% to 92.7%

**In print.** Nothing. No source I found computes this half for more than one year, for a projection, or says that its centre has moved or is now in Germany. Three things in print bear on it:

- Rankin's map is of the year 2000, and the study's grid for 2000 also has the Alps on top, by 0.13 points over Berlin; in 2010 that lead is 0.03. So "the published answer was right for its time" can now be said with the date.
- The ridge is already drawn. On Rankin's "Your Hemisphere" map a thin, unlabelled contour (I take it for the 92% line, from his text and the spacing of the lines) encloses a band running north-east from the south-east of France through Germany to southern Sweden and Finland, as I read the picture. That is the "ragged ridge running north-east from the western Alps" with its far end in the northern Baltic. His words for it are the "large plateau" quoted above.
- If Boggs's figure of 1945 is right (about 94% in the land half; see P4), the fall of the best share from 93.4% to 92.7% continues an older decline. That is one rough estimate, second-hand.

Neighbouring work on drift over time concerns a different object, the mean position of mankind: Grasland and Madelin (2001), Grether and Mathys (2010), Quah (2011), Balsa-Barreiro and others (2019), by title and search summary only. Arthur (2024) follows the smallest half-population circles of the United States, Great Britain and Mongolia from 2000 to 2020, not the world's and not a hemisphere.

**What the dataset's own papers say about its years** (GHSL Data Package 2023, pages 45 to 48, and the table of inputs shipped with the grid):

> "Residential population estimates at 5 years interval between 1975 and 2030 are derived from the raw global census data harmonized by CIESIN for the Gridded Population of the World, version 4.11 (GPWv4.11) at polygon level ..." (p. 45)

> "The population estimates at polygon level for each mapped epoch (5-year interval between 1975 and 2030) are obtained by applying for each unit the population growth rate computed by CIESIN within the census available dates ... The estimates are then rescaled to match (a) the total population time series at 'city' level from the extended database feeding the UN World Urbanisation Prospects 2018 ... and (b) the total population time series at country level provided by the UN World Population Prospects 2022" (p. 46), "(medium variant)" (p. 47).

The table of inputs gives the census year for each country: Philippines, Malaysia, Singapore, Indonesia, Thailand, Brazil, Ecuador and Paraguay 2010; Bolivia 2012; Peru 2007; Colombia 2005 (Mexico's row I could not read). So every grid, the one for 2020 included, is those censuses carried backward and forward by growth rates and scaled to the United Nations' country totals of 2022. The censuses of the 2020 round are not in it below the level of the country. The grids for 2025 and 2030 use the UN's medium projection; the documentation's table on page 21 lists "Future grids projections ... 2025 and 2030" and twelve epochs in all.

**Hard on the claim.**

- "Every grid up to 2010" is four grids of the eight the dataset has up to that year (1975, 2000, 2005, 2010; not 1980 to 1995). The public page says "every year I tried"; the README does not.
- "From 2020" is one modelled year and two projections. The move is what censuses of 2005 to 2012, their growth rates and the UN's country series imply. The direction is sturdy (the Philippines and Malaysia have grown much faster than Brazil); the date is the dataset's.
- The README's "What is not established" already says the move is "a statement about GHS-POP's epochs". It could say why, in the words above.

**Verdict.** Not found in print or on any page: new as far as this search goes and probably unrecorded (about four chances in five), not hard to do, and standing on one modelled dataset.

### P3. What the move trades: Manila, Kuala Lumpur, Singapore and mid-Sumatra against São Paulo and the south of Brazil

**In print.** Rankin's sentence, quoted under P1: against the land half, the people's half "contains more of Southeast Asia and less of South America". That is the same pair of regions, traded between the land half and the people's half. The trade between the two candidate centres of the people's half, with its numbers, is in nothing I found.

**My check of the study's numbers** (`checks.out`, `slivers.out`). The places are right: Manila, Kuala Lumpur, Singapore, Pekanbaru and Padang are within 90° of 52.37° N, 12.68° E and not of 46.0° N, 7.18° E; São Paulo, Curitiba, Quito, Guayaquil and Santa Cruz are the reverse; Rio is inside both and Lima outside both. Singapore is inside by 0.4°. The slivers hold 29.9 and 41.2 million in the 1975 grid and 91.6 and 86.6 million in the 2020 grid, as the README says. By rough boxes:

| sliver | part | 1975 | 2020 |
|---|---|---|---|
| only in the Berlin half | Luzon and the islands near it | 17.7 | 51.7 |
| | Malay Peninsula with Singapore (and Sumatra's coast north of 1° N) | 8.5 | 28.8 |
| | the rest of Sumatra's middle | 3.6 | 10.5 |
| | west of 60° E, mostly the Pacific coast of Mexico at the sliver's other end | 0.1 | 0.5 |
| only in the Alpine half | Brazil's side, east of 60° W (São Paulo, Paraná and their neighbours) | 33.2 | 65.0 |
| | Ecuador with the north of Peru and the south of Colombia | 6.6 | 16.7 |
| | Bolivia and inland | 1.4 | 4.7 |
| | elsewhere | 0.1 | 0.2 |

(millions of people). So "the Philippines and Malaysia outgrew south-east Brazil" is fair: those two parts went from 26 to 80 million while Brazil's side went from 33 to 65. The README's table shows only the totals; this breakdown is mine and has been read by nobody else.

**Verdict.** The kind of trade is in Rankin; this trade and its numbers are an easy corollary of P2 and probably unrecorded (about nine in ten).

### P4. Who is left out; the land half holds 88.5% of people

**In print.**

- **S. W. Boggs, "This Hemisphere", Journal of Geography 44 (9), December 1945, 345–355.** As quoted by a user on Wikipedia's talk page (13 June 2018), from the caption of Boggs's figure 1: "About 6 per cent of the world's population lives here [water hemisphere] on 12 per cent of the world's land area (excluding Antarctica)." That is about 94% of mankind in the land half centred on Nantes, in 1945. The publisher's page answered with a bot check; I have not seen the paper.
- **Rankin (2015):** "not so different from the Land Hemisphere". **Wikipedia:** "almost identical to the hemisphere containing the greatest human population."
- An unconfirmed recollection of mine: that Erwin Raisz's *Atlas of Global Geography* (1944) names a "principal hemisphere" holding about 94% of mankind. The search found the atlas and not the sentence. Treat it as a lead.
- On antipodes and people, Wikipedia's "Antipodes on Earth" says: "The two largest human-inhabited antipodal areas are located in East Asia (mainly eastern China) and South America (mainly Argentina and Chile)." I found no figure for the share of mankind living opposite other people.
- I found no count, by continent, of who lies outside the people's half.

**My check.** In the 2020 grid, outside the half centred at 52.37° N, 12.68° E: 219.95 million between 170° W and 30° W, 352.74 million east of 60° E, and between 30° W and 60° E one cell with 347.5 people at 37.075° S, 12.325° W, which is Tristan da Cunha. The island's own page (tristandc.com, update of 18 November 2026) says: "There are 220 Tristan da Cunha Islanders", 18 of them overseas, and "242 people currently living on Tristan da Cunha or visiting the surrounding islands". The README's "the 348 people the grid puts on" is the right way to say it; the grid has about a hundred too many.

The land half's share of people depends on which land summit is meant. Centred on the Catalan summit it holds 88.5% in the 2020 grid (88.7% in the 1975 grid). Centred on Nantes it holds 91.1% (91.7% in 1975). The README has the Nantes figure under H9; the public page gives only 88.5%.

**How the study differs from Boggs.** Three ways: the year (1945 against 2020; the share has been falling), the centre (Nantes against the Catalan summit, which gives up most of Honshu), and method (an estimate from country figures against a grid).

**Verdict.** The count of who is left out is a by-product nobody would have printed, and the figure of 88.5% is probably unrecorded (about nine in ten) because the Catalan summit is itself scarcely known; but the question "how many people live in the land half" was answered in 1945 with about 94%, and both published comparisons call the two halves nearly the same, which the study's 4.2 points qualify.

### W1. The half with the most kinds of woodpecker: about 83% of 239 species, centred in Gascony

**In print.** Nothing of the kind. I found no "half with the most species" worked out for woodpeckers, for birds, or for any group of animals or plants. What bears on the numbers:

- **Wikipedia, "Woodpecker":** "The family Picidae includes about 240 species arranged in 35 genera." (Elsewhere on the same page, 36 genera.)
- **Ilsøe, Kissling, Fjeldså, Sandel and Svenning, "Global variation in woodpecker species richness shaped by tree availability", Journal of Biogeography 44 (8), 2017, 1824–1835.** I read the abstract on the University of Amsterdam's repository; it relates "broad-scale woodpecker species richness" across the world to tree cover and climate. The search summary adds that it covers "all 254 extant woodpecker species" and finds the foremost hotspot in Southeast Asia and the second in the eastern Andes; those two statements I have not read in the paper.
- **Mikusiński, "Woodpeckers: distribution, conservation, and research in a global perspective", Annales Zoologici Fennici 43 (2006), from page 86.** Not obtained (404 at both addresses). By the search summary, diversity is highest in the tropics of Asia, South America and Africa.

**How the study differs.** The published work counts species per place (from range maps, as I understand it; I read only an abstract). The study counts each species once, spread over the 5° boxes where a records database has five records of it, and asks which half holds most of that total. Its 239 is a records database's list at a threshold; it happens to be close to the handbooks' 240 and is not the same list as the 254.

**Hard on the claim.** The share moves from 83.1% to 84.5% and the centre by 300 km with the treatment of a box on the edge, by the study's own reviewer; four fifths of the records are North American. The instrument a bird geographer would use is range maps, and the study has not tried it. "About 83%, give or take 300 km" is as much as the tables show, and both pages say so.

**Verdict.** Not found for woodpeckers or for any group: an easy and probably unrecorded exercise (about nine in ten), whose number belongs to its definition.

### W2. "What lies opposite South America is the Malay Archipelago, not mainland Asia"

**In print.** **Wikipedia, "Antipodes on Earth"**, lead:

> "The largest antipodal land masses are the Malay Archipelago, antipodal to the Amazon basin and adjoining Andean ranges; east China and Mongolia, and small sections of southeast Russia, antipodal to Argentina and Chile; and Greenland and the Canadian Arctic Archipelago, antipodal to East Antarctica."

and further down: "The largest landmass with antipodes entirely on land is the island of Borneo, whose antipodes are in the Amazon rainforest." I did not find the remark made in biogeography, about woodpeckers or about any hemisphere of species: one search, whose summary reported no source that makes it.

**Hard on the claim.** The same sentence of Wikipedia says what the README's leaves out. Opposite the Amazon basin and the northern Andes is the Malay Archipelago. Opposite Argentina and Chile are China and Mongolia, which is mainland Asia. By my arithmetic (`places.out`) Lima is opposite Cambodia, Cusco opposite the highlands of Vietnam, Santiago opposite Shaanxi and Buenos Aires opposite the Yellow Sea off Jiangsu. And "China and Indochina are all within 90° of western Europe" is not so for the best woodpecker centre: Hong Kong (91.6°), Guangzhou (90.4°), Fuzhou (91.8°), Hainan (90.9°), Da Nang (92.4°), Phnom Penh (93.4°) and Ho Chi Minh City (95.1°) are outside it. The README's next sentence, which lists "the south of Indochina, Taiwan, Japan" among what is left out, is right, and the public story's "nearly all of China" is right.

The explanation survives in a corrected form. No half can hold a place and the place opposite it. The best half keeps the tropical part of South America and so gives up what lies opposite that: the archipelago, the Philippines and the south of Indochina (14% of the total). It keeps China and the Himalaya and so gives up what lies opposite them: Argentina beyond the Chaco, and Chile (3%).

**Verdict.** The geography is commonplace and on Wikipedia; its use to explain a half of woodpeckers is in nothing I found (about nine in ten that it is unrecorded in that use); as the README words it, it is partly wrong.

## 3. Something outside the six claims: the circle holding half of mankind

The README's first table says half of humanity "fits in a circle of radius 3,346 km centred at 28.6° N, 100.5° E, in the mountains where Sichuan meets Yunnan", and sets it against the centre it remembered from Danny Quah, 770 km away.

**Rudy Arthur, "Valeriepieris Circles for Spatial Data Analysis"**, arXiv 2307.16728 (1 August 2023), published in Geographical Analysis 56 (2024) 514–529 (the journal reference is from a search summary of a later paper's citation). I read the preprint. Page 2: "The Valeriepieris circle for the whole earth is centred in the north of Yunnan province, China with a radius of around 3300km." Table 1: "VP 0.5-circle (28.375, 100.625) 3386" km, from the GPW version 4.11 grid at 15 arc-minutes, the centre "snapped" to the grid; the year is not stated in the table. He credits the idea to Ken Myers, on Reddit, and cites Quah (2015, 2016). He also publishes a program that finds the smallest circle holding any given fraction of a gridded population.

The study's centre is 28 km from Arthur's; its radius is 40 km smaller, on different data and a finer grid. So this row of "The answers" is a second independent agreement with something in print, like the land half. I did not fetch Quah's page, so the README's account of his figures ("3,300 km, centred near Mong Khet") is unchecked by me.

## 4. The README and the public page against the sources

**Right as they stand** (checked): the quotation from Brilliant Maps; the name, version, authors and DOI of GHS-POP R2023A; the eight totals of people (they equal the documentation's table 20 to the last digit); "2025 and 2030 are its projections"; "eight of the twelve grids"; the 220 and 353 million; the 348 on Tristan da Cunha as the grid's figure; "700 to 800 km" from western Switzerland to the Berlin centre (771 km from Rankin's point); about 900 km between the Alpine and Brandenburg summits (919 km); woodpeckers absent from Australia, Antarctica, New Guinea, New Zealand and Madagascar (Wikipedia: "found worldwide, except for Australia, New Guinea, New Zealand, Madagascar, and the extreme polar regions"; I read no handbook); 82.7%, 74.9% and 70% for the three named halves (`out/woodpeckers_clean.out`).

**Wrong, or more than the tables show.** Old text, then new text. The README's lines are wrapped; an old text is given here with a space where the README has a line end.

README:

1. "The answers", row "other summits".
   Old: `An Alpine summit was the highest in every grid up to 2010`
   New: `An Alpine summit was the highest in each of the four grids I ran up to 2010 (1975, 2000, 2005, 2010; the dataset also has 1980 to 1995, which I did not run)`
2. "The people's half moved".
   Old: `The highest was Alpine in every grid up to 2010 and is west of Berlin from 2020.`
   New: `The highest was Alpine in each of the four grids I ran up to 2010 and is west of Berlin in the grid for 2020 and in the two projections.`
3. Same section, first sentences.
   Old: `A published map (Bill Rankin's, as described by Brilliant Maps) puts the point with the most people within 10,000 km "in western Switzerland with up to 92.9%". Mine is near Berlin with 92.70%, some 700 km away.`
   New: `A published map, Bill Rankin's "Human Hemisphere" of 2015, puts the centre of the half with the most people "in western Switzerland, at roughly 46.5°N, 7°E", with "92.9% of all humans in the year 2000", from the GRUMP version 1 grid. (I knew it at first only from Brilliant Maps' description: "in western Switzerland with up to 92.9%".) Mine, for 2020, is near Berlin with 92.70%, some 770 km from his point.`
4. Same section.
   Old: `So the published answer was right for its time.`
   New: `So the published answer was right for its time: it is for the year 2000, and in this dataset's grid for 2000 a half centred on Rankin's point holds 92.84% by a later reader's count, 0.01 points under the best.`
5. "Coda".
   Old: `What lies opposite South America is the Malay Archipelago, not Asia: India, the Himalaya, China and Indochina are all within 90° of western Europe, and so is most of South America.`
   New: `What lies opposite the tropical part of South America is the Malay Archipelago with the south of Indochina, not the body of Asia: India, the Himalaya, nearly all of China and the north of Indochina are within 90° of the best centre, and so is most of South America. (Opposite Argentina and Chile lie China and Mongolia; there the best half keeps China.)`
6. Opening.
   Old: `Both questions have textbook answers`
   New: `Both questions have published answers` (for people the answer is a map on a website, of 2015).
7. "The people's half moved", last sentence.
   Old: `the 348 people the grid puts on Tristan da Cunha.`
   New: `the 348 people the grid puts on Tristan da Cunha (the island's own count is about 240).`
8. "The answers", row "half of humanity": add `(Rudy Arthur had published this centre from another dataset: 28.375° N, 100.625° E, 3,386 km; Geographical Analysis 56, 2024)`.
9. "What is not established", second item.
   Old: `The population grid is a model (census counts spread over built-up area).`
   New: `The population grid is a model (census counts spread over built-up area). Every one of its grids, 2020 included, starts from censuses of about 2010 (2005 to 2012 for the countries on the two slivers), carried backward and forward by growth rates and scaled to the United Nations' country totals of 2022; the grids for 2025 and 2030 use the UN's medium projection.`
10. "Sources" (in the README the address is in code marks, left out here).
    Old text: the population map is Bill Rankin's, as described at brilliantmaps.com/human-hemisphere
    New text: the population maps are Bill Rankin's "Human Hemisphere" and "Your Hemisphere" (2015), radicalcartography.net/human-hemisphere.html and radicalcartography.net/your-hemisphere.html, which I first knew from the description at brilliantmaps.com/human-hemisphere

Public page, the story above the fold:

11. Old: `A published map (Bill Rankin's, as the site Brilliant Maps describes it) puts the centre in western Switzerland. The two need not disagree, though the description gives neither the date of that map nor the data behind it.`
    New: `A published map, Bill Rankin's of 2015, puts the centre in western Switzerland, with 92.9% of the people of the year 2000. The two do not disagree.`
12. Old: `What lies opposite South America is the islands from Sumatra to the Philippines, and the best half does leave those out.`
    New: `What lies opposite the tropical part of South America is the islands from Sumatra to the Philippines, with the south of Vietnam and Cambodia, and the best half does leave those out.`
13. Old: `The first holds 88.5% of the world's people.`
    New: `The first holds 88.5% of the world's people; the half centred on Nantes, the usual one, holds 91.1%.`
14. In the small print, "saw nothing of Boggs's, Berget's or Rankin's own work" stays true of that reader. A later reader has now read Rankin's two pages and both maps, and a second-hand quotation from Boggs.

Public page, the older page under the fold (kept whole, so these are notes and not edits):

15. "reasoning that South America's woodpeckers and tropical Asia's are on opposite sides of the globe. They are not." This says too much. Tropical South America and the Malay Archipelago with southern Indochina are on opposite sides. The story's "That is only partly so" is the better sentence.
16. "the description I read gives neither the map's date nor its data": true of the description; the map's own page gives both.

## 5. Notes that could be added

**For the README, as a dated note.**

> *Added 26 November: what was already known about the people's half and the woodpeckers' half. A fresh instance searched (18 searches and 17 fetches; its report is `prior-art.md`). The half with the most people is Bill Rankin's "Human Hemisphere" (radicalcartography.net, 2015), which I had cited only through Brilliant Maps' description. His own page gives what the description lacks: 92.9% of the people of the year 2000, a centre "roughly" at 46.5° N, 7° E, from the GRUMP version 1 grid. He says that a more exact centre "isn't possible, given the imprecision of population data", that the top is a "large plateau" with "a good chunk of Europe" above 92%, and that against the land half this one "contains more of Southeast Asia and less of South America". In my grid for 2000 a half centred on his point holds 92.84%, so for that year we agree. The reader found nothing in print that works the centre out for a second year, says it has moved or puts it in Germany, and nothing on the two slivers or on who is left out. Those may be new. They are an easy update of his map and rest on one modelled dataset: by its own documentation every grid, 2020 included, starts from censuses of 2005 to 2012 scaled to the United Nations' country totals of 2022. For the people in the land half, S. W. Boggs wrote in 1945 that about 6 per cent of mankind lived in the water hemisphere (as quoted on Wikipedia's talk page; I have not seen his paper); my 88.5% is for 2020 and the Catalan summit, and the half centred on Nantes holds 91.1%. The centre of the smallest circle holding half of mankind, 28.6° N, 100.5° E, had been published by Rudy Arthur (Geographical Analysis 56, 2024): 28.375° N, 100.625° E, from another dataset. For the woodpeckers the reader found no half of most species worked out for any group of animals or plants. That the Malay Archipelago lies opposite the Amazon basin is in Wikipedia's article on antipodes, which also says what my sentence left out: opposite Argentina and Chile lie China and Mongolia. "Not Asia" was wrong, and the coast of China from Hainan to Fujian and the south of Vietnam and Cambodia are outside the best half.*

**For the public page.**

> Added 26 November. The map of the half with the most people is Bill Rankin's "Human Hemisphere" of 2015 (radicalcartography.net). It gives 92.9% of the people of the year 2000 and a centre in western Switzerland, and warns that the data do not allow the centre to be placed more exactly; for that year my figures agree with his. A search of some thirty-five requests found nobody who had worked it out for a later year or said that the centre has moved, and nobody who had asked the question of woodpeckers. That is what one search found, not proof that nobody has.

## 6. What I could not obtain or did not read

- **Boggs (1945).** Bot check at the publisher. His 6% rests on a Wikipedia talk-page comment by a user who says he read the paper on microfilm.
- **The World Economic Forum reprint and its Big Think original; geoawesome.com.** The first refused; the others I did not fetch. Their figures here (92.9%, 92.6%) are from search summaries.
- **Mikusiński (2006).** Not found at either address. **Ilsøe and others (2017):** abstract only; the 254 species and the two hotspots are from a search summary.
- **Johnson and Preparata (1978); Grasland and Madelin (2001); Grether and Mathys (2010); Quah (2011, 2015); Balsa-Barreiro and others (2019).** By title, search summary or Arthur's reference list. Not read.
- **Raisz (1944).** My recollection, unconfirmed.
- **Monmonier's "Centrography"** in *Cartography in the Twentieth Century* (2015), which Wikipedia cites beside Affholder. Not fetched. It is the likeliest place for an older "hemisphere of population" that I did not look in.
- **Affholder's paper** I did not reread for any mention of people.
- **Handbooks of woodpeckers** (Winkler and Christie; Gorman). Not read. The statements on where woodpeckers are absent rest on Wikipedia.
- **French and German geography of 1900 to 1950.** One query in each language returned nothing to the point. That is a thin search of a literature that is mostly not on the open web.
- **Forums.** No thread found; the search service reaches them poorly.
- **A second population dataset.** The test that would most strengthen or sink P1 and P2 was not in my brief and I did not make it.
- **From memory and unchecked here:** Brazil's census of 2022 counted about 203 million, well under the estimates of the time. If so, the American sliver is somewhat smaller than this grid has it. The Philippines' census of 2020 also came in under the UN's figure. I have not worked out the net effect.

## 7. What was fetched, and where it is

Log: `/home/agent3/prior/hemi/fetch-log.txt` (18 lines SEARCH, 17 lines FETCH). Downloads, each in its own directory under `/home/agent3/downloads/`:

| directory | what | result |
|---|---|---|
| `hemi-prior-01-rankin-human-hemisphere-html` | radicalcartography.net/human-hemisphere.html | read |
| `hemi-prior-02-rankin-your-hemisphere-html` | radicalcartography.net/your-hemisphere.html | read |
| `hemi-prior-03-rankin-your-hemisphere-png` | the map "How much of humanity is in your hemisphere?" | read as an image |
| `hemi-prior-04-rankin-human-hemisphere-png` | the map "The Human Hemisphere" | read as an image |
| `hemi-prior-05-arthur-arxiv-2307.16728` | Arthur's preprint (PDF) | read |
| `hemi-prior-06-weforum-empty-half` | weforum.org article | refused (403); left alone |
| `hemi-prior-07-wikipedia-talk-land-water` | Talk:Land and water hemispheres (wikitext) | read |
| `hemi-prior-08-wikipedia-hemispheres-of-earth` | Hemispheres of Earth (wikitext) | read; nothing on a half of most people |
| `hemi-prior-09-boggs-1945-tandf` | Boggs 1945 at the publisher | bot check (403); left alone |
| `hemi-prior-10-mikusinski-2006-annzool` | Mikusiński 2006 | 404 |
| `hemi-prior-11-wikipedia-woodpecker` | Woodpecker (wikitext) | read |
| `hemi-prior-12-wikipedia-antipodes` | Antipodes | a redirect stub |
| `hemi-prior-13-wikipedia-antipode` | Antipode | a disambiguation page |
| `hemi-prior-14-mikusinski-2006-sekj` | Mikusiński 2006, second address | 404 |
| `hemi-prior-15-wikipedia-antipodes-on-earth` | Antipodes on Earth (wikitext) | read |
| `hemi-prior-16-tristan-population` | tristandc.com/population.php | read |
| `hemi-prior-17-ilsoe-2017-uva-dare` | record of Ilsøe and others 2017 | abstract read |
| `hemi-prior-ghs-datapackage-from-zip` | not a download: the documentation (PDF) and table of inputs (xlsx) copied out of the study's own archive of the 2020 grid | section 2.5 and the rows of fifteen countries read |

Also read from the study's earlier downloads: `/home/agent3/downloads/humanhemi/hh.html` (Brilliant Maps, 21 November) and `/home/agent3/downloads/wiki-land-hemi-25nov/page.wiki`.

In `/home/agent3/prior/hemi/`: this report; `fetch-log.txt`; `tools/` (`fetch.sh`, `logsearch.sh`, `totext.py`, `crop.py`, `xlsx_dump.py`, `checks.py`, `slivers.py`, `places.py`, `check_old_texts.py`, and three `edit_report` scripts that record the corrections I made to this report while checking it); `checks.out`, `slivers.out`, `places.out`; `text/` (plain text of Arthur's preprint and of the dataset's documentation); `crops/` (pieces of Rankin's two maps, cut out to read the labels; his maps are CC BY-NC-SA and are not for republishing without that licence).

The searches, in order: Rankin's page; computations of the half with most people (extended); the same in French; "most populous hemisphere" with Germany, Berlin, Switzerland; people in the land hemisphere, Boggs and Raisz (extended); Arthur's paper; forum threads (extended); "human hemisphere" moved or updated; people in the land hemisphere in old textbooks; the same in German; a half of most species (extended); Mikusiński's paper; antipodes of South America in biogeography; centre of gravity of world population; the densest hemisphere problem; antipodes and population; Raisz's "principal hemisphere" (extended); Rankin's book of 2025. The exact wording of each is in the log.
