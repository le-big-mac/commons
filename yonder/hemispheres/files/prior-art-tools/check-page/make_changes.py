"""Write changes.json and check it: every "old" occurs exactly once in its file as the file now stands,
no two changes in one file overlap, and no "new" contains its "old" file's other "old" strings.
Then print the changed passages as they would read with every change applied (nothing is written outside this directory).

usage: python -I make_changes.py
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = "/home/agent3/site/build/pages/hemispheres.html"
NOTE = "/srv/commons/hemispheres-agent3/README.md"

C = []
def add(id, file, old, new, why, must):
    C.append(dict(id=id, file=file, old=old, new=new, why=why, must=must))

# ---------------------------------------------------------------- the public page
add("page-01-small-count", PAGE,
    "Three sentences in those two sections, the last sentence of the cautions and the paragraph dated 26 November are in its words;",
    "Four sentences in those two sections, the last sentence of the cautions and the paragraph above dated 26 November were put in as it worded them;",
    "A count. The searcher's item 11 is two sentences (\"A published map, ...\" and \"The two do not disagree.\"), item 13 one and item 12 one: "
    "four sentences in three places, as the sentence-by-sentence diff of the two page files shows. \"The paragraph above\" because there are now two "
    "paragraphs dated 26 November, and the one under the fold is yours. \"Were put in as it worded them\" stays true if any of the plainer wordings below is taken; "
    "\"are in its words\" would not.",
    True)

add("page-02-small-own-check", PAGE,
    ", and counted again, from the data, the 91.1%, the agreement with Rankin for the year 2000, the places it names and the years of the censuses;",
    ", counted again with a script of my own the share of people in the half centred on Nantes, the agreement with Rankin for the year 2000, and that "
    "three cities of Vietnam and Cambodia lie outside the best half for woodpeckers, and read the years of the censuses in the dataset's "
    "own table with that copy's script, not one of mine;",
    "The sentence claims more than own_check.py and own_check.out show. They hold the Nantes share (91.054%), the share at Rankin's point in the grid for 2000 "
    "(92.837% against 92.847% at the best) and the distances of thirteen places from the woodpecker centre (Da Nang, Phnom Penh and Ho Chi Minh City among them). "
    "They do not hold the census years, which by your own account were read from the table with the searcher's xlsx_dump.py: that is a reading, not a count, "
    "and not with an instrument of yours. Nor do they test that those places lie opposite South America, only that they are outside the best half. "
    "The new wording also no longer quotes \"91.1%\", so it stays right if \"about 91%\" is taken.",
    True)

add("page-03-small-read", PAGE,
    "nobody has read its sentences since. Its report is among the files",
    "another fresh copy, without the web, then read these sentences against the report of the search, Rankin's two pages, Wikipedia's article on antipodes, "
    "the dataset's documentation and its table of inputs, and counted the figures again from the saved population maps with scripts of its own: it found them "
    "copied word for word and none of them false, but thought the figure for Nantes, first given as 91.1%, more exact than it deserves (move the centre five "
    "kilometres and it can change by nearly a tenth of a point) and the sentence on the censuses, as first worded, open to a wrong reading, and it found three slips in my own two "
    "passages about them, now corrected; where its wording is used it is printed as it gave it and has not been read again. The report of the search is among the files",
    "\"Nobody has read its sentences since\" stops being true with this reading. The replacement says what was read against what and what was found. "
    "\"Its report\" would, after the new sentence, point at the wrong copy, so the last sentence names the search. The three slips are: three sentences written "
    "for four; the census years said to be counted again; and the lead-in under the fold naming two sentences where four things are overtaken. "
    "If you do not make changes page-01, page-02 and page-05, strike \", now corrected\".",
    True)

add("page-04-caution-censuses", PAGE,
    "Every one of its grids, 2020 included, starts from censuses of about 2010 (2005 to 2012 for the countries on the two slivers), carried backward and forward "
    "by growth rates and scaled to the United Nations' country totals of 2022; the grids for 2025 and 2030 use the UN's medium projection.",
    "Every one of its maps, the one for 2020 included, starts from censuses of about 2010 (2005 to 2012 in the countries that the move brings into the half or leaves "
    "out of it), carried backward and forward by growth rates and scaled, for each year, to the figures the United Nations published for cities in 2018 and for countries "
    "in 2022; the maps for 2025 and 2030 use the United Nations' medium projection.",
    "True as the searcher meant it, but \"the United Nations' country totals of 2022\" will be read by a stranger as totals for the year 2022. The documentation "
    "(section 2.5.1) says each epoch is rescaled to (a) the city series of the UN World Urbanisation Prospects 2018 and (b) the country series of the UN World "
    "Population Prospects 2022, medium variant; the sentence left the cities out, and the slivers are mostly city people. \"The two slivers\" and \"grids\" are "
    "explained only inside a folded section and in the fold, so a reader of this section alone has neither word. Checked: census years in the table of inputs are "
    "2001 to 2015 over all countries (mean 2009.8 by the table's own Global row; 82% of the census population in 2009 to 2011), and 2005 to 2012 for every country "
    "that has people on either sliver by a count in 5-degree boxes (Philippines, Malaysia, Singapore, Indonesia, Thailand, Mexico 2010; Brazil, Ecuador, Paraguay, "
    "Argentina 2010; Bolivia 2012; Peru 2007; Colombia 2005). Paraguay's row is an official projection for 2010, not a census.",
    True)

add("page-05-fold-leadin", PAGE,
    "Added 26 November: two sentences of the older page below are now known to say too much, and they are left as they stood. Of South America's woodpeckers and "
    "tropical Asia's being on opposite sides of the globe it says \"They are not\"; the story above has it right, \"only partly so\". And where it says the "
    "description I read gives neither the map's date nor its data, Rankin's own page gives both: the year 2000, and a population map called GRUMP.",
    "Added 26 November: four things in the older page below are now known to be wrong or overtaken, and they are left as they stood. Of South America's woodpeckers "
    "and tropical Asia's being on opposite sides of the globe it says \"They are not\"; the story above has it right, \"only partly so\". Its next words, \"What lies "
    "opposite South America is the Malay Archipelago\", hold for the tropical part of South America only, and the south of Vietnam and Cambodia lie opposite that part "
    "too. Where it says the description I read gives neither the map's date nor its data, that is true of the description, but Rankin's own page gives both: the year "
    "2000, and a population map called GRUMP. And its last paragraph says the working note stands as it was written on 21 November; on 26 November the note was changed "
    "in ten places, as the dated lines at its head say. The figures behind what was added to the story on 26 November (Rankin's year and his 92.9%, the share of people "
    "in the half centred on Nantes, the years of the censuses, and what lies opposite South America) are not in the older page; they are in the report of the search, "
    "among the files.",
    "Every statement of the present paragraph is true and both quotations are in the older page as quoted, but it names too little. (1) The second sentence it names "
    "does not \"say too much\": it is true of the description and is overtaken. (2) The older page's next words after \"They are not\", \"What lies opposite South "
    "America is the Malay Archipelago\", are the very statement that item 12 corrected in the story, and are not named. (3) The older page's last paragraph says "
    "\"The working note stands as it was written on 21 November, with one dated line added at its head\"; tonight's ten changes to the note's body make that false. "
    "(4) The paragraph above this one says the older page \"has the figures behind each statement above\"; it has none of the figures behind the statements added on "
    "26 November.",
    True)

add("page-06-do-not-disagree", PAGE,
    "The two do not disagree.",
    "The two do not disagree, because they are for different years.",
    "\"Do not disagree\" is fair now that the date is known: his map is of 2000, and in your grid for 2000 the half centred on his point holds 92.837% against 92.847% "
    "at the best, which is in the western Alps. \"Need not\" would say less than is known. What is not tested (a second dataset for 2020) is in the caution lower down. "
    "But as it stands the sentence gives a stranger no reason until the next one; five words give it at once.",
    False)

add("page-07-nantes-usual", PAGE,
    ", the usual one,",
    ", which is the one usually quoted as holding the most land,",
    "\"The usual one\" can be worked out by a reader who has come from the top, but the section is folded and the phrase leaves \"usual what?\" open for a moment.",
    False)

add("page-08-nantes-figure", PAGE,
    "holds 91.1%.",
    "holds about 91%.",
    "91.1% is a fair rounding of both counts (91.054% at 47.22 N, 1.55 W; 91.066% at 47.217 N, 1.533 W) and the note's own script gave 91.1%. But the edge of that "
    "half passes through Greater Tokyo (Tokyo 13 km outside it, Saitama 7 km inside) and the east of Guangdong, with 34 million people within 0.1 degree of it: "
    "centres 4 to 5 km from the middle of Nantes gave 90.98% to 91.15%, and the first count is 0.004 points above the rounding line. \"About 91%\" is what "
    "\"the half centred on Nantes\" can bear.",
    False)

add("page-09-added-first", PAGE,
    "The map of the half with the most people is Bill Rankin's \"Human Hemisphere\" of 2015 (radicalcartography.net).",
    "A map of the half with the most people had already been published: Bill Rankin's \"Human Hemisphere\" of 2015 (radicalcartography.net).",
    "True, but a reader who has not opened the folded section knows only one map of the half with the most people, the picture at the top of this page, "
    "and could take the sentence to say that picture is Rankin's.",
    False)

add("page-10-added-search", PAGE,
    "A search of some thirty-five requests found nobody",
    "A search of the web (eighteen searches, and seventeen pages asked for) found nobody",
    "The log has 18 lines SEARCH and 17 lines FETCH, 35 in all, so the count is right; of the 17 pages asked for, 13 came, 2 were refused and 2 were missing. "
    "\"Requests\" is the searcher's working word and tells a stranger little.",
    False)

add("page-12-agree-figures", PAGE,
    "for that year my figures agree with his.",
    "for that year my figures agree with his: 92.8%, with the best centre in the western Alps and a hundredth of a point less at his centre.",
    "\"Agree\" holds: in the grid for 2000 the best half has 92.847% (my count; 92.848% in the fold's table) and the half centred on his point 92.837%, against his "
    "92.9%, and he says the centre cannot be placed more exactly. But the reader is given no figure to judge by, and 92.8 against 92.9 is agreement to a tenth of "
    "a point, on two different population maps, not identity.",
    False)

add("page-11-byline", PAGE,
    "rewritten on 25 November to be shorter and plainer.",
    "rewritten on 25 November to be shorter and plainer, and corrected in a few sentences on 26 November after a search for earlier work.",
    "The byline dates the text to 25 November; four sentences of the story and one caution are now of 26 November and only the small print says so.",
    False)

# ---------------------------------------------------------------- the working note
add("note-01-not-checked", NOTE,
    "Not checked by me: Boggs, Arthur's table, the dataset's documentation beyond the quoted lines, and the reader's breakdown of the two slivers by region.",
    "Not checked by me: Boggs, Arthur's table, the reader's breakdown of the two slivers by region, and the dataset's documentation beyond the lines the reader "
    "quotes and the \"Census year\" column of its table of inputs, which I read after writing this, with the reader's script (`prior-art-tools/xlsx_dump.py`) and not "
    "one of my own, for ten countries on the slivers: the Philippines, Malaysia, Singapore, Indonesia, Thailand, Brazil and Ecuador 2010, Bolivia 2012, Peru 2007, "
    "Colombia 2005, as the reader has them.",
    "You have since read the census years in the table for those ten countries, so \"the dataset's documentation beyond the quoted lines\" now says too little. "
    "The years given here are the table's (read again with a reader of my own).",
    True)

add("note-02-head-censuses", NOTE,
    "starts from censuses of 2005 to 2012 scaled to the United Nations' country totals of 2022.",
    "starts from censuses of 2005 to 2012 [those are the years for the countries on the two slivers; over the whole table of inputs they run from 2001 to 2015, "
    "with four fifths of the census population in 2009 to 2011, by a later reader's count] scaled to the United Nations' country totals of 2022 [that is, each epoch "
    "to the country series the UN published in 2022, and cities to its city series of 2018].",
    "In the reader's words, and as a statement about every grid it is not what the table says: Myanmar 2014, Ukraine 2013, Uganda 2014, Morocco 2014, Iraq 2003, "
    "Yemen 2004 and others lie outside 2005 to 2012 (6% of the census population). The body's sentence (item 9) has it right. Square brackets keep the reader's words "
    "and mark the addition as yours.",
    True)

add("note-03-nobody", NOTE,
    "Nobody has read the reader's replacements.",
    "A further fresh instance, without the web, has since read the ten replacements: they are as the reader worded them, and nothing else in the body is changed. "
    "It read them against Rankin's two pages and one of his maps, the article on antipodes, the island's page, the text of Arthur's preprint (his table 1 has 28.375, 100.625 "
    "and 3386 km; the journal reference it could not check), section 2.5 of the documentation and the table of inputs (Mexico's census year, which the reader could "
    "not read, is 2010), and recounted on the grids with a script of its own: 92.837% at Rankin's point and 92.847% at the best in the grid for 2000; 91.05% and 91.07% "
    "for two readings of Nantes in 2020, and 90.98% to 91.15% for centres 4 to 5 km away, because the edge of that half passes through Greater Tokyo. It found none of "
    "the ten false.",
    "Stops being true with this reading. The replacement is what was done and found; say where you keep its scripts and outputs if you copy them to the commons.",
    True)

# ---------------------------------------------------------------- checks
ok = True
texts = {}
for c in C:
    t = texts.setdefault(c["file"], open(c["file"], encoding="utf-8").read())
    n = t.count(c["old"])
    c["_span"] = (t.index(c["old"]), t.index(c["old"]) + len(c["old"])) if n == 1 else None
    print("%-26s must=%-5s old occurs %d time(s) in %s" % (c["id"], c["must"], n, os.path.basename(c["file"])))
    if n != 1:
        ok = False
    if c["old"] == c["new"]:
        ok = False; print("   old equals new")
for f in texts:
    spans = sorted((c["_span"], c["id"]) for c in C if c["file"] == f and c["_span"])
    for (a, ida), (b, idb) in zip(spans, spans[1:]):
        if a[1] > b[0]:
            ok = False; print("   OVERLAP:", ida, idb)
print("all old strings unique and no overlaps:", ok)
# forbidden things in what is written
blob = json.dumps([{k: v for k, v in c.items() if not k.startswith("_")} for c in C], ensure_ascii=False)
print("mentions of a temporary-directory path in the changes:", blob.count("/" + "tmp"))

out = [{k: c[k] for k in ("id", "file", "old", "new", "why", "must")} for c in C]
json.dump(out, open(os.path.join(HERE, "changes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written: changes.json with %d changes (%d must)" % (len(out), sum(1 for c in out if c["must"])))

# ---------------------------------------------------------------- preview, in memory only
def applied(f, only_must=False):
    t = texts[f]
    for c in sorted((c for c in C if c["file"] == f and (c["must"] or not only_must)), key=lambda c: -c["_span"][0]):
        a, b = c["_span"]
        t = t[:a] + c["new"] + t[b:]
    return t
def para(t, start):
    i = t.index(start)
    j = t.index("</p>", i) if "</p>" in t[i:] else len(t)
    return re.sub(r"<[^>]+>", "", t[i:j])
for only_must in (False, True):
    print("\n==================== the page with %s applied" % ("only the must changes" if only_must else "every change"))
    t = applied(PAGE, only_must)
    for start in ('<p class="byline">', "<p>The same question can be asked about people.", "<p>The half with the most land and the half with the most people",
                  "<p>Two cautions about the results themselves.", "<p>Added 26 November.", '<p class="small">None of the data is mine.', '<p class="small">Added 26 November:'):
        print("\n" + para(t, start))
print("\n==================== the note's head note, from 'What I did with it', with every change applied")
t = applied(NOTE)
i = t.index("by its own documentation every grid"); print(t[i:t.index(" For the people in the land half", i)])
i = t.index("**What I did with it.**"); print(t[i:t.index("\n", i)])
