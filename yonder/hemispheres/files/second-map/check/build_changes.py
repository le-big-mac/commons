"""Write changes.json (the checker's replacements for the note and for the proposed page changes), check that every
"old" occurs exactly once in its file as it now stands and that no two changes overlap, and write copies of the two
files with all changes applied (after/README.md.txt, after/page-additions.md.txt) for proof-reading.
usage: python3 build_changes.py"""
import json, os
R = '/home/agent3/hemi2/README.md'
P = '/home/agent3/hemi2/page-additions.md'
C = []
def ch(id, file, old, new, why, must):
    C.append(dict(id=id, file=file, old=old, new=new, why=why, must=must))

# ------------------------------------------------------------------ the note
ch('R1', R,
   "found nobody who had worked the centre out for a\nsecond year or on a second dataset, and its reader named this test",
   "found the centre worked out once in print, by Bill Rankin\nfor the year 2000 from another grid (GRUMP version 1), and nothing for a second year or a second dataset; its reader named this test",
   "The search did find the centre worked out, by Rankin, on a dataset that is not GHS-POP; the sealed sheet says so (\"worked out once in print, by Bill Rankin for the year 2000\") and the note's header dropped it. As it stands the sentence reads as if nobody had computed the centre before.",
   True)
ch('R2', R,
   "The newer\n   series begins in 2015 and has the centre near Berlin already then.",
   "The newer\n   series begins in 2015 and has the centre near Berlin already then. So the move itself is seen only on the two series that share the censuses of about 2010; the series that knows the censuses of about 2020 shows where the centre is from 2015 on, not that it moved.",
   "The note has both facts (the older series shares GHS-POP's censuses; the newer begins in 2015) but never draws the consequence, and the page draft drew the opposite one (\"the move is seen on three maps\"). The sealed sheet itself claimed only that \"from 2020 on\" would stand on a map that knows the 2020 censuses.",
   False)
ch('R3', R,
   "about\n   0.06% of mankind at most.",
   "about\n   0.06% of mankind at most. Best centre against best Alpine centre (45.05° N, 6.70° E on all three), counted with a hard edge by a fresh instance, the leads are smaller: 2.3, 3.8 and 4.5 million.",
   "The Valais point is not the best Alpine centre in 2020 on any of the three maps; summit against summit the margin is 2.28, 3.76 and 4.46 million (check/out/search2-all.out). The fixed-point figures are right, but the smaller ones are the margin by which the best centre is \"near Berlin\".",
   False)
ch('R4', R,
   "the newer WorldPop\n   series, 5 million.",
   "the newer WorldPop\n   series, 5 million. They differ on the pace before the projections too: from 2015 to 2020 the lead grows by 3.7 million on GHS-POP and by 1.0 million on the newer WorldPop series.",
   "The disagreement is not only in the projections: 1.24 to 4.95 million on GHS-POP against 3.24 to 4.19 on the newer WorldPop series over the same five years. The figure shows it; the note does not say it.",
   False)
ch('R18', R,
   "Each point is one map of the world's people for\none year, summed onto a grid of 0.05°.*",
   "Each point is one map of the world's people for\none year, summed onto a grid of 0.05°. The grey band marks the projections of GHS-POP and of the newer WorldPop series; the older WorldPop series was made in 2018, so its point for 2020 is a projection too.*",
   "The figure prints \"projections\" over 2025 and 2030 only, and the note's caption does not mention the band. The release statement dates the older series: \"the global datasets constructed in 2018 that represented the 2000-2020 period\".",
   False)
ch('R5', R,
   "the two fixed halves are counted with a hard\nedge on the 0.05° grid.",
   "the two fixed halves are counted with a hard\nedge on the 0.05° grid, the best centre's share with `hemilib`'s soft edge. GHS-POP's 2015 is a tie, as `../README.md` says: the Upper Palatinate summit (49.4° N, 12.4° E) is 0.002 points below the one near Berlin with the soft edge and 0.003 above it in a fresh instance's hard-edged search.",
   "The table gives 52.08° N, 12.78° E as the best centre for GHS-POP 2015 with no flag. An independent hard-edged search puts the best centre for that grid in the Upper Palatinate, 300 km away (92.7094% at 49.39° N, 12.38° E against 92.7066% near Berlin); the author's own output has them 0.002 apart the other way. Every other row's best centre was reproduced within 15 km. Also the column \"its share\" is soft-edged while the two columns beside it are hard-edged, which the footnote did not say.",
   True)
ch('R6', R,
   "The older mosaics mark sea and empty land\nwith the largest number a 32-bit float can hold, and",
   "The older mosaic for 2000 marks sea and large lakes\nwith the largest number a 32-bit float can hold (those for 2010 and 2020 use the same number with a minus sign, which the first script already left out), and",
   "Only the 2000 file has GDAL_NODATA = +3.4028235e38 (587,977,639 pixels). The 2010 and 2020 files have -3.4028235e38, which popgrid.py's test `> 0` excludes. And the marker is on sea and lakes, not on empty land: the Sahara, Greenland's interior and the Taklamakan hold zeros or small positive values (check/out/points.out, check/out/regrid-g1-*.out).",
   True)
ch('R7', R,
   "The totals then come to 6.03, 6.81 and 7.97 thousand million.",
   "The totals then come to 6.03, 6.81 and 7.97 thousand million. This is the one departure from the sealed sheet, which names `popgrid.py`. A fresh instance counted every value in all seven mosaics and found nothing else that is not a count of people; the 2000 file's own statistics give the same total.",
   "Improvement: says plainly that the instrument named in the sealed sheet was changed after sealing, and records the check that the change is complete (check/regrid.py: no NaN, no negative but the markers, largest value 672,315 in one pixel of the older 2020 mosaic; STATISTICS_MEAN 27.301392503861 x 220,726,361 valid pixels = 6,026,137,017.6, the grid's total).",
   False)
ch('R8b', R,
   "I was too\ncautious.",
   "I was too\ncautious in the chances, and not right in every reason: E1's expected the newer totals to raise the lead by about a million, and the lead is 0.8 million lower.",
   "The note says \"I was too cautious\" without saying that the reasoning of E1 pointed the wrong way. The sheet: \"Brazil down about 2% takes about 1.3 million from the American sliver ... Net, the lead grows by about a million.\" On the newer map the sliver only in the Valais half is 87.28 million against GHS-POP's 86.61 (larger, not smaller), and the lead is 0.76 million lower.",
   False)
ch('R8a', R,
   "the difference in 2020 is 0.7 million.",
   "the difference in 2020 is 0.8 million (4.95 against 4.19), and that is from every cause together, not from the spreading alone.",
   "4.9493 - 4.1895 = 0.76, which is 0.8, not 0.7 (the 0.7 comes from subtracting the rounded figures). The sentence also sets a net difference from all causes (censuses, UN revision, date, model) against an allowance that was for the spreading alone.",
   True)
ch('R9', R,
   "All three spread census counts over the ground by a\n  model.",
   "All three spread census counts over the ground by a\n  model, and the newer WorldPop series builds its map of settlements on the same GHSL built-up layers (GHS-BUILT, release R2023A) by which GHS-POP spreads its people: so say its release statement and GHS-POP's documentation.",
   "A dependence the note leaves out. Release statement, \"Built settlement growth model\": \"Global Human Settlement Layer (GHSL) data were adopted as the base for the model, specifically the BUILT-S (Pesaresi & Politis, 2023) and BUILT-V (Pesaresi & Politis, 2023) products\". GHSL Data Package 2023: \"GHS-BUILT-V_GLOBE_R2023A, version 1.0) was used as target for disaggregation of population estimates\".",
   False)
ch('R10', R,
   "GHS-POP and the older WorldPop series start from the same collection of censuses of about 2010.",
   "GHS-POP and the older WorldPop series start from the same collection of censuses of about 2010 (GPW version 4): GHS-POP by its documentation, the older WorldPop series by my reading of the newer one's release statement, which says that \"previous global datasets\" relied on \"the single timepoint extrapolations from the GPW4 database\".",
   "The release statement's sentence is: \"rather than being reliant on the single timepoint extrapolations from the GPW4 database that led to many problems with previous global datasets\"; 'Global1' is named only in the next sentence. That the older series is meant is a fair inference, and the note should show it is one. The statement nowhere mentions GHS-POP's censuses; that half comes from the GHSL documentation (GPWv4.11).",
   False)
ch('R11', R,
   "and for the question here that is the difference that matters: the halves cut\n  through few countries, so the totals of countries count for more than the spreading inside them.",
   "and for the question here that is the difference that matters, though not because the totals of countries decide it: the two slivers are parts of countries (Luzon, the Malay Peninsula, the middle of Sumatra; the south-east of Brazil, Ecuador, the north of Peru), so what counts is how many people the censuses put in which provinces and cities. A fresh instance tested the spreading below that scale (`check/edge.py`): spread every cell's people evenly over a square about half a degree across (60 km) and the 2020 lead moves by 0.2 million at most on each map; over one degree it falls by about 2 million, and over two the Alpine half is ahead. The edge runs that close to big cities: on each map some 90 million people live within one degree of the edge of the Berlin half, among them greater Manila, Singapore and Rio de Janeiro, all just inside it.",
   "Tested and not supported as written. The halves do cut few countries, but the slivers ARE parts of countries, so country totals cannot decide: with one map's totals held in blocks of 5, 10 or 30 degrees and the other map's pattern inside, the lead swings between 1.7 and 7.4 million (check/out/edge-2020.out). What the tests support is the narrower thing: the model's fine spreading hardly matters (blur over 0.55 degrees: -0.14, -0.08, -0.21 million on GHS-POP, newer and older WorldPop; one map's totals in 1-degree blocks with the other's pattern inside: -0.08, +0.12). Blur over 1.05 degrees: -2.04, -1.85, -1.98; over 2.05 degrees the lead becomes -1.63, -2.05, -3.85. People within 1 degree of the Berlin half's edge: 92.4, 90.3, 92.9 million; Manila is 90 km inside, Singapore 42 km, Rio de Janeiro 47 km (check/out/cities.out).",
   True)
ch('R12', R,
   "The older WorldPop series has the Alpine half ahead in 2010\n  and the Berlin half in 2020;",
   "The older WorldPop series has the Alpine half ahead in 2010\n  and the Berlin half in 2020 (a year which that series, made in 2018, projects);",
   "The release statement dates the older series to 2018. Its 2020 is a projection as much as the points in the figure's grey band.",
   False)
ch('R13', R,
   "The sheet allowed 3%.",
   "The sheet allowed 3% \"from the UN's figure\" and named no revision; against the 2024 revision the 2010 grid may be at the limit (not looked up). Only E10 and E11 use that grid, and both hold without it.",
   "Comparing with GHS-POP's totals (the UN's 2022 revision, per the GHSL documentation) is a fair reading of a rule that names no revision, but the 2010 grid passes by half a point, and the sheet's own E12 cites the 2024 revision. The checker recalls, from memory only and without the network, about 7.02 thousand million for the middle of 2010 in the 2024 revision, which would make the grid 3.0% low; the author can look it up and replace \"may be at the limit (not looked up)\" with the figure. No line's outcome depends on it.",
   False)
ch('R14', R,
   "- **No error bar exists for any of these numbers.**",
   "- **The years are not the same days.** The newer WorldPop series is for 1 January of each year, by its release statement; I have not looked up the day for the other two. Half a year of GHS-POP's trend is 0.4 million of lead.\n- **No error bar exists for any of these numbers.**",
   "Release statement: \"constrained at the national level to the January 1st estimates of the 2024 iteration of the UN World Population Prospects\". GHS-POP's lead grows 4.95 to 8.59 million from 2020 to 2025, 0.36 million per half year. Small beside the differences between maps, but a reader comparing the three 2020 points should know the dates may differ.",
   False)
ch('R15', R,
   "The Palatinate summit is within 0.05 points of the best on every map for\n  2015 and for 2020.",
   "The Palatinate summit is within 0.05 points of the best on every map for\n  2015 and for 2020, and so is the best Alpine summit except on GHS-POP's 2020; on the older WorldPop series' 2020 it is 0.03 points behind, 2.3 million people. On none of the fifteen grids does a centre outside 43° to 62° N, 5° to 24° E come within 0.1 points of the best (a fresh instance's hard-edged search of the whole sphere).",
   "Checked and true as written (Palatinate level on GHS-POP 2015; behind by 0.028, 0.032, 0.026, 0.037 points on the newer 2015, GHS-POP 2020, older 2020, newer 2020). Added what the same search shows: the Alpine summit is also inside 0.05 points on four of those five maps (0.017, 0.040, 0.029, 0.048; 0.057 on GHS-POP 2020), and nothing outside the ridge from the western Alps to the northern Baltic comes near (check/out/worldbox.out, check/out/summary.out).",
   False)
ch('R16', R,
   "The mosaics themselves (3.6 GB)",
   "The mosaics themselves (4.4 GB)",
   "The seven sizes in fetch-log.txt add up to 4,358,395,192 bytes (4.36 GB, or 4.06 GiB); the checksums and sizes in the log match the files.",
   True)
ch('R17', R,
   "`people2_fig.py`, `second-map.png`.",
   "`people2_fig.py`, `second-map.png` · `check/` (the reader's scripts and their outputs, without its copies of the grids).",
   "Needed only if change R11's pointer to `check/edge.py` is kept and the reader's directory is copied with the note. Leave out check/grids/ (1.4 GB, identical to the author's grids), the *.npy files in check/out/ and check/after/.",
   False)

# ------------------------------------------------------------------ the page changes
ch('P7', P,
   "Three changes are proposed.",
   "Four changes are proposed; the fourth, a credit, was added by the reader.\n\n## 4. Under \"How far to trust this\", in the paragraph \"None of the data is mine.\"\n\nOLD:\n\n> the population maps from the European Commission's Joint Research Centre,\n\nNEW:\n\n> the population maps from the European Commission's Joint Research Centre and, for the check of 26 November, from WorldPop (www.worldpop.org) at the University of Southampton,",
   "The page will show a figure made from WorldPop's data and state results from it, and neither of its two credit passages names WorldPop. The note says the data are under CC BY 4.0, which requires the credit (the checker could not confirm the licence without the network). The credits \"in full\" at the foot are inside the part printed \"as it stood until 25 November\", so the story's own paragraph is the place. It is put here at the head of the file because no other text in the file can anchor it.",
   True)
ch('P1', P,
   "> Two other population maps, made by another group, tell the same story: the Alps in 2000 and 2010, near Berlin in 2020. One of them is built on the censuses taken around 2020, which the maps I first used are not.",
   "> Two other series of population maps, made by another group, agree as far as they go. The older series has the centre in the Alps in 2000 and 2010 and near Berlin in 2020. The newer series begins in 2015 and has the centre near Berlin from then on; unlike the maps I first used, it knows the censuses taken around 2020. On all three the lead is thin: in 2020 the half centred near Berlin holds between 2.6 and 4.9 million more people than the half centred in the Alps, out of nearly 8,000 million.",
   "As written, both maps \"tell the same story: the Alps in 2000 and 2010\", and the next sentence lets the reader think the map that knows the 2020 censuses is one of the tellers. It is not: the newer series has no map before 2015. The draft also puts the good news in the main text and every caution further down; a stranger who reads only this section should meet the thin margin here.",
   True)
ch('P2', P,
   "(twelve things; all twelve came out as expected)",
   "(twelve things, some of which stand or fall together; all twelve came out as expected)",
   "The note says the lines \"are not twelve separate tests\"; the page should not let twelve of twelve sound like twelve independent confirmations.",
   False)
ch('P3', P,
   "The newer series is built on the censuses of about 2010 and about 2020.",
   "The newer series, by its makers' account, is built on the censuses of about 2010 and about 2020.",
   "This rests on the release statement alone (\"Population and boundary data were gathered for the two most-recent census rounds (c.2010 and c.2020)\", with other sources where there was no census); the note says \"by its own account\" and the page should too.",
   False)
ch('P4', P,
   "So the move is seen on three maps. But the three are not independent: all of them spread census counts over the ground by a model, none gives a margin of error, and the lead of one half over the other in 2020 is between 3 and 5 million people out of nearly 8,000 million.",
   "So three sets of maps agree on where the centre is in 2020. The move itself is seen on only two of them, the two that go back before 2015, and those two start from the same censuses of about 2010; the newer series, the only one that knows the censuses of about 2020, begins when the centre is already near Berlin. Nor are the three independent: all of them spread census counts over the ground by a model, the newer series starts its map of buildings from the one that the maps I first used are built on, none gives a margin of error, and the lead of one half over the other in 2020 is between 2.6 and 4.9 million people out of nearly 8,000 million. The edge of the half centred near Berlin passes within 100 km of Manila, Singapore and Rio de Janeiro, with all three just inside it.",
   "\"The move is seen on three maps\" is not so: the newer WorldPop series starts in 2015 with the Berlin half already 3.2 million ahead, so it shows no move; the two that show one (GHS-POP and the older WorldPop series) share the censuses of about 2010, which is the very weakness this paragraph was written to confess. That caution is in the note and was left out here. \"Between 3 and 5 million\" is not true of 2.6. The last sentence (from the checker's own count: Manila 90 km, Singapore 42 km, Rio 47 km inside the edge) may be dropped without harm to the rest.",
   True)
ch('P5', P,
   "The line for the map this page used starts",
   "The line for the maps this page first used starts",
   "After the change the page uses three sets of maps, so \"the map this page used\" no longer picks one out. Goes with relabelling the figure (see the report).",
   False)
ch('P6', P,
   "Where a line crosses \"level\", the best centre passes from the Alps to near Berlin. The years in the grey band are projections.",
   "Where a line crosses \"level\", the half centred near Berlin overtakes the half centred in the Alps. The best centre is found separately, by a search over the whole globe: on each set of maps it is in the Alps in every year below the level and near Berlin in every year above it, except that in 2015, on the maps this page first used, a place in Bavaria ties with it. The years in the grey band are projections, and so is the older WorldPop point for 2020: those maps were made in 2018. The whole scale is small: 5 million people is 0.06% of the world's.",
   "The lines compare two fixed halves; the best centre is a separate search, and the caption stated as a rule what is only an observed coincidence at five- and ten-year steps (and not quite that for GHS-POP's 2015, where the line is above level and the Palatinate ties). The checker's own search confirms the coincidence for the other fourteen points. The grey band marks 2025 and 2030 only, but the older WorldPop series was made in 2018, so its 2020 is projected too. And a stranger looking at an axis that runs from 10 fewer to 10 more needs telling that the whole range is about a quarter of one percent of mankind.",
   True)

# ------------------------------------------------------------------ checks
texts = {R: open(R).read(), P: open(P).read()}
spans = {R: [], P: []}
for c in C:
    t = texts[c['file']]
    n = t.count(c['old'])
    assert n == 1, (c['id'], 'old occurs', n, 'times')
    assert c['old'] != c['new'], c['id']
    i = t.index(c['old']); spans[c['file']].append((i, i + len(c['old']), c['id']))
for f, sp in spans.items():
    sp.sort()
    for a, b in zip(sp, sp[1:]):
        assert a[1] <= b[0], ('overlap', a, b)
    print(os.path.basename(f), 'order in file:', ' '.join(s[2] for s in sp))
here = os.path.dirname(os.path.abspath(__file__))
json.dump(C, open(f'{here}/changes.json', 'w'), indent=1, ensure_ascii=False)
os.makedirs(f'{here}/after', exist_ok=True)
for f, name in ((R, 'README.md.txt'), (P, 'page-additions.md.txt')):
    t = texts[f]
    for c in C:
        if c['file'] == f: t = t.replace(c['old'], c['new'])
    open(f'{here}/after/{name}', 'w').write(t)
    print(name, 'words before', len(texts[f].split()), 'after', len(t.split()))
print(len(C), 'changes;', sum(c['must'] for c in C), 'marked must; every old string occurs exactly once; no overlaps')
