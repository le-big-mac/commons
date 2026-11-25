"""Builds changes.json for the second reading of the Antikythera story, and checks it against the page source.
Reads /home/agent3/site/build/pages/antikythera.html and writes only into this folder:
  changes.json, preview-all.html (every change applied), preview-must.html (the 'must' ones only).
Checks: every 'old' occurs exactly once in the current source; no two overlap; tags balance after applying;
nothing in the JSON looks like an identifier, a temporary path, an address or a key."""
import json, os, re, sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = '/home/agent3/site/build/pages/antikythera.html'
src = open(SRC, encoding='utf-8').read()
FOLD = src.index('<details class="fold">')

C = []
def ch(id_, old, new, why, must):
    C.append({'id': id_, 'old': old, 'new': new, 'why': why, 'must': must})

# ---------------------------------------------------------------- the story
ch('cap1-kind-day',
   "On this one day the Moon's pointer would be 105° from the Moon, and each of the others within 7° of its body.</figcaption>",
   "On this one day the Moon's pointer would be 105° from the Moon, and each of the others within 7° of its body. It is a kind day for the planets: over the years their pointers would typically be 4° to 12° out.</figcaption>",
   "The picture is the first thing a reader sees and it shows one day on which every planet is within 7°. Over the 76 years to today the typical errors in the pointers note's run.out are 4.7° (Mercury), 10.4° (Venus), 11.7° (Mars), 4.4° (Jupiter) and 9.3° (Saturn), and the largest is 48°. The story says the day is a kind one only a section later, and only of Mars; a reader who takes in the picture and its caption alone is left with the rosier figure.",
   True)

ch('planets-read',
   "the numbers are read on the machine's inscriptions; for the three planets that do well they",
   "the number of years in each ratio is read on the machine's inscriptions; for the three planets that do well the ratios",
   "Says more than the evidence. What is read on the inscription is one number for each planet, the years: 462 for Venus and 442 for Saturn (Freeth and others 2021, page 2 and the caption of Figure 1). The paper turns each into a ratio (289 cycles in 462 years, 427 in 442). The earlier page had 'the number of years is read', which the earlier reader called exactly right.",
   True)

ch('planets-babylonian',
   " were supplied by that paper.</p>",
   " were supplied by that paper, which notes that they were already known in Babylonian astronomy.</p>",
   "Optional, and to go in only together with 'fold-babylonian'. As it stands 'supplied by that paper' can be read as numbers made up in 2021. The caption of the paper's Figure 2 says: 'Except for the periods for Venus and Saturn, all the final periods were already known in Babylonian astronomy.' I read it on the page image and in the text. It bears on whether the heading 'nearly as good as new' is fair: the three good ratios are ancient ones, though nothing on the machine attests them.",
   False)

ch('heading-planets',
   "<h2>Three planets would be nearly as good as new</h2>",
   "<h2>Three planets, as reconstructed, would be nearly as good as new</h2>",
   "Optional. The heading is fair as long as the caution paragraph stays in this section, because that paragraph says plainly that the three good planets are the three whose ratios the paper supplied. A reader who takes in only the headings does not get that; two words in the heading would carry it.",
   False)

ch('dial-reconstruction',
   "and the dial assumes that the cycle simply repeats.</p>",
   "and the dial assumes that the cycle simply repeats. Marks can still be read in only 20 of the cells; the full list used here is Freeth's reconstruction of 2014, and a later one, by Iversen and Jones, differs from it in two places.</p>",
   "Optional if 'limits' goes in, which carries the short form of this. A caution lost on the way: the earlier page said that glyphs can be read in 20 cells and that the counts are for Freeth's list, with Iversen and Jones's (2019) scoring 36 and 27 in the first cycle where Freeth's scores 37 and 28. In the story only the small print inside the second figure names Freeth's reconstruction.",
   False)

ch('cap2-counted',
   "one step for each eighteen-year cycle. Once a line reaches zero it stays there.</figcaption>",
   "one step for each eighteen-year cycle. \"Eclipse\" is counted generously, as the text below explains. Once a line reaches zero it stays there.</figcaption>",
   "The story's figure leaves out the note's third line (eclipses of the Moon that are partial or total), so the picture shows only the generous count, and the caution comes two paragraphs later. Counted strictly the Moon's line would start at 27 of 38, not 37, and reach nothing 992 years on (about AD 788), not about AD 950 (two_lists.json, recounted). The earlier reader of the public page made the same point about the summary box.",
   True)

ch('first-cycle-credit',
   "No marked month has held an eclipse of the Moon since about AD 950, or of the Sun since about AD 1058.</p>",
   "No marked month has held an eclipse of the Moon since about AD 950, or of the Sun since about AD 1058. The close fit at the start is no finding of mine: Freeth, who reconstructed the marks, chose 205 BC partly because the dial's scheme suits the sky of that year.</p>",
   "A credit and a caution lost on the way. The earlier page's summary box said: 'The close fit at the start is not mine to claim. Freeth ... chose that year in part because the Moon's nodes then stood where the dial's scheme needs them'. The dial note calls the first-cycle fit 'largely built in', and its first reader found 'partly circular' too weak. The story gives the 37 of 38 as a plain result and credits Freeth only two sections later, without saying that the year was chosen partly for the fit. I have put the sentence at the end of its paragraph so that 'nearly all still did' keeps its sense.",
   True)

ch('missed-kind',
   "Meanwhile real eclipses of the Moon turn up in months without a mark: by 144 years on there were three in a cycle, and from 992 years on the dial missed every one.",
   "Meanwhile eclipses of the Moon that the eye can see, partial or total ones, turn up in months without a mark: by 144 years on there were three in a cycle, and from 992 years on the dial missed every one of them.",
   "Wrong as it reads. The three and the 992 years are counts of partial or total eclipses only (the note, and the fold: 'partial or total lunar eclipse in a month it does not mark'). The story counts 'eclipse' generously in the same section, and on that count there were already five eclipses of the Moon in unmarked months in the first cycle (42 in the catalogue, 37 in marked months), and marked months went on holding eclipses until about AD 950. So 'from 992 years on [AD 788] the dial missed every one' contradicts 'No marked month has held an eclipse of the Moon since about AD 950' in the paragraph before. The first reader's note on this edit said the figures were for partial or total eclipses; the words were lost.",
   True)

ch('generous-effect',
   "which are ten of the 37 at the start.",
   "which are ten of the 37 at the start; leave them out and the count for the Moon starts at 27 of 38 and reaches none 992 years on.",
   "Optional. Gives the caution a size: 27 at the start, and none from cycle 55 (991.6 years on, about AD 788) in two_lists.json. The fold's table has both.",
   False)

ch('solar-unmarked',
   "\"only 8 were visible from anywhere in the ancient Greek empire\".</p>",
   "\"only 8 were visible from anywhere in the ancient Greek empire\". Nor did the dial mark every eclipse of the Sun even at the start: 13 of the 41 in the first cycle fall in months without a mark.</p>",
   "Optional. The story now tells how many eclipses of the Moon came without a mark and says nothing of the Sun, where 13 of 41 had none from the start (the earlier page had this; the fold still does).",
   False)

ch('cut-today-cells',
   " Today's eclipses of the Moon fall two cells after the marks: the total eclipse of 3 March 2026 is in cell 151, where the dial marks cell 149.</p>",
   "</p>",
   "Optional cut, to make room. The sentence is true (modern_cells.out: all six eclipses of the Moon of 2024 to 2026 fall two cells after a marked cell) and it is in the fold word for word; the story loses a detail and no caution.",
   False)

ch('why-studies-sixteen',
   "because three published studies put the first full moon of its eclipse dial on 12 May of that year. I wanted to see how firm that is. The dial's marks cannot date it by themselves, which is what one of the three studies, by Carman and Evans, had already said: of the months from 300 BC to 1 BC, sixteen fit the marks at least as well as 205 BC does, counting 205 BC itself.</p>",
   "because three published studies (Carman and Evans, 2014; Freeth, 2014; Jones, 2020) put the first full moon of its eclipse dial on 12 May of that year. A fourth argues for December 178 BC; the longer account takes it up. I wanted to see how firm 205 BC is. The dial's marks cannot date it by themselves, as Carman and Evans had already said. By my count, sixteen of the months from 300 BC to 1 BC fit the marks at least as well as 205 BC does on the test I used, counting 205 BC itself; a looser test lets in thirty-five.</p>",
   "Four things. (1) Credit: Freeth and Jones are two of the three studies and the story never names Jones at all. (2) A caution the earlier reader had put on the public page and the story dropped: another published start date exists (Voulgaris and others, December 178 BC). (3) The colon made Carman and Evans the authors of the count of sixteen; what they said is that matching marks to eclipses cannot date the dial, and the sixteen are this page's. (4) 'Sixteen fit the marks at least as well' holds only on one test: starts.out has 43 starts that do as well on the three counts, 16 once those with the Moon's crossing points the wrong way round are left out, and 35 on the looser reading; the fold keeps those qualifiers and the story had none. The dial note also says 'Freeth made this search before me'; that credit is in the fold ('The search is not new either') and I have left it there to save words, since the story does not claim the search as new.",
   True)

ch('why-259',
   "at about the longitude of the Aegean Sea.</p>",
   "at about the longitude of the Aegean Sea. One caution: 259 BC, left out of the sixteen by a single month, fits the hours fairly closely too, at the western edge of the Greek world; Carman and Evans, and Jones, weighed that year and set it aside for reasons of their own.</p>",
   "A caution lost on the way, and the one the first reader of the hours note pressed hardest: 'only 205 BC puts the dial in the Greek world' holds 'only because 259 BC misses the sixteen by one solar month'. 259 BC has 38 and 27 marked months with an eclipse where 205 BC has 37 and 28; with the 18 hours it scores 3.20 h at 10° E, between the four (2.5 to 2.7 h) and the other twelve (4.5 h and up), and with all 22 hours it fits better than 205 BC (3.67 h against 3.91 h). The note itself calls the exclusion 'a narrow thing'. As the story stands, sixteen to four to one reads as if this page's own working left one year standing. Carman and Evans (section 22.1) and Jones (2020) both weigh 259 BC; I read both passages.",
   True)

ch('why-credit',
   "That is the argument Carman and Evans published in 2014. I worked it again with programs of my own and came to the same year.",
   "That is the argument Carman and Evans published in 2014; Freeth and Jones came to the same year by routes of their own, which also use the hours. I worked the argument again with programs of my own and came to the same year.",
   "Credit. The hours note opens: 'That the hours point to 205 BC is the published result of Carman and Evans (2014), Freeth (2014) and Jones (2020)'. Jones writes that the two papers of 2014 'separately arrived at' the date, and Jones himself sets the hours against computed full and new moons cycle by cycle. The credit to Carman and Evans for the argument as the story tells it (the hours pick out one run of cycles, the place picks one in three) is right: it is their 'rule of 8 h', sections 16 and 17.",
   True)

ch('mine-credits',
   "Carman and Evans had shown that a scheme like the dial's drifts and has to be reset, and how the hours fix the year. Freeth and Jones had found in 2012 that circles on circles leave the pointer for Mars nearly 38° out at times, where I find 35°.",
   "That a run of eclipses eighteen years apart lasts twelve to fifteen centuries is old knowledge, and Carman and Evans had set out how a scheme like the dial's slips and has to be reset, and how the hours help to fix the year. Freeth and Jones had found in 2012 that circles on circles leave the pointer for Mars nearly 38° out at times, where I find 35°. Freeth and others had printed how far out each planet's gear ratio is in a year; my figures are smaller than theirs for four of the five, and I cannot say why. Efstathiou and others had run a simulated mechanism for dates in our own time, after setting it afresh from a recent eclipse.",
   "Credits weaker than on the earlier page, where the earlier reader had made each of them a must. (1) The story's chief result, marks that last eleven to thirteen centuries, is what the known life of such a run of eclipses predicts (the fold: 'lasts twelve to fifteen centuries, which is where the dial's last months end'; caption of Freeth's Figure S1). (2) 'Had shown' credits Carman and Evans with what they report as Babylonian practice; and the hours fix the year only together with the marks and a place, which is the hours note's own third point. (3) The 2021 paper prints each ratio's error (its Figure 2e, which I read from the page image: Mercury 0.005022, Venus 0.008576, Mars 0.003089, Jupiter 0.000802, Saturn 0.004208 degrees a year). This page's are 0.56, 0.75, 0.69, 0.80 and 1.05 of those, unexplained, and by the paper's figures Mercury's ratio is less good than Saturn's, where the story says Venus and Saturn are the two less good. A reader should know the page's ranking rests on its own figures. (4) Without Efstathiou and others the next sentence ('What I did not find in print ... its pointers read off for today') is true only by its careful wording: they did run a simulated mechanism for present dates (1977 to 2071, and Easter dates), after setting it from a recent eclipse and redrawing its zodiac, and concluded that it 'accurately predicts'. With them named, the sentence is honest.",
   True)

ch('trust-safe',
   "Of 45 things I expected, 40 proved right; the five that did not are listed at the foot of the page.",
   "Of 45 things I expected, 40 proved right, though many were safe to expect and for the hours I knew the published answer; the five that did not are listed at the foot of the page.",
   "A caution lost on the way. The pointers note says of its 24 lines that 'most were near-certain once the arithmetic was right' (five were open, by its reader's sorting), and the hours note says its sheet 'was sealed with the published answer known'. Without that, 40 of 45 reads as a score. The counts themselves are right: 24 + 8 + 5 + 8 = 45 and 22 + 7 + 5 + 6 = 40 in the four score outputs, and the four sheets' fingerprints still match the recorded ones.",
   True)

ch('limits',
   "The planets' gearing is a reconstruction. I assumed perfect gears, set as well as they could be set, and a keeper who gave the machine one turn for each year, which is why the Sun's pointer is still right.",
   "The planets' gearing is a reconstruction, and so are most of the eclipse dial's marks. I assumed perfect gears, set as well as they could be set, and a keeper who gave the machine one turn each time the Sun came back to the same stars, which is why the Sun's pointer is still right. Had the keeper followed the seasons instead, the planets' pointers would typically be 14° to 38° out and the Moon's no nearer the Moon.",
   "Three things. (1) 'One turn for each year' is not what was done and gives a different answer: a reader takes a year for a year of the seasons, and turned that way (2,230.576 turns, not 2,230.490) the Sun's pointer itself would stand 31° from the Sun against the stars, and the others would move with it. The fold has it right: 'once for each return of the Sun to the same stars'. (2) A caution lost on the way, which two earlier readers had put back each time: the results hold against the stars only. Against the seasons the planets' pointers are 14° to 38° out (run.out, frame T: 22.8°, 22.8°, 14.1°, 30.3°, 38.0°) and the Moon's is 132° out today. The story keeps only the words 'against the stars', which its first reader said he passed over without understanding. (3) Of the 66 marks on the dial 39 are reconstruction (20 cells can be read).",
   True)

ch('readers',
   "READERS",
   "Two more fresh copies of the model read this rewrite: one read the story alone, as a stranger would, for plainness, and checked no facts; the other checked the story, its two pictures and the new section on the hours against the working notes, their saved results and the papers, and only compared the rest of the longer account with the earlier page. The second ran none of the computations again and made no search for other publications, and its changes have not been read again.",
   "The two sentences asked for, to stand in place of the word READERS. The last clause is true only if the changes go in as worded; if any is reworded, say so there.",
   True)

# ---------------------------------------------------------------- the fold
ch('fold-head-count',
   "three sentences that said the hours were not tested now point to that section.",
   "four sentences that said the hours, or the other proposed start date, were not tested now point to that section.",
   "By comparison with the page as it stood, four sentences were changed in this way, not three: two said the hours were not tested (in the cautions on the dial, and at the end of the third point of 'What was already known') and two said the start of December 178 BC was not tested (in 'The eclipse dial' and in the list of sources).",
   True)

ch('fold-head-not-in',
   "One figure in the story is not in it: the 45 things expected are its 37 and the 8 for the hours, and the 40 that proved right are 34 and 6.</p>",
   "Three things in the story are not in it. That the machine was recovered in 1901 and that about a third of it survives, in 82 fragments, is from the opening pages of Freeth and others (2021) and of Carman and Evans (2014). The year AD 355 is 559 years on from May 205 BC. And the 45 things expected are its 37 and the 8 for the hours, and the 40 that proved right are 34 and 6.</p>",
   "'One figure in the story is not in it' is not so: 1901, 'about a third' and '82 fragments' are in the story's first paragraph and nowhere below, and no source was given for them. I found them in Freeth and others 2021 ('since its discovery in 1901. Now split into 82 fragments, only a third of the original survives') and in Carman and Evans ('recovered from an ancient shipwreck in 1901'). Freeth and Jones (2012) put the salvage in 1900 to 1901 and the noticing of the fragments in 1902, so 'recovered in 1901' is the papers' short form and not the whole history. AD 355 is in the story and not below, where the nearest thing is 'after about 560'.",
   True)

ch('fold-babylonian',
   "and the other three are their restoration. Almost none",
   "and the other three are their restoration; the caption of the paper's Figure 2 says that all but the periods for Venus and Saturn were already known in Babylonian astronomy. Almost none",
   "Optional, and to go in only together with 'planets-babylonian', so that the longer account holds what the story says.",
   False)

ch('fold-safe',
   "Of the 37, 34 held. The three that failed are listed below.",
   "Of the 37, 34 held. The three that failed are listed below. Most of the 24 lines for the pointers had been worked out by hand beforehand and were near-certain once the arithmetic was right.",
   "Goes with 'trust-safe': the story will say many of the expectations were safe ones, and the longer account should hold the note's own words for it (the pointers note, under 'The sealed sheet').",
   True)

ch('fold-hours-3711',
   "for each of the 3,711 months that could be the dial's first, with the longitude",
   "for each of the 3,711 lunar months between 300 BC and 1 BC that could be the dial's first, with the longitude",
   "Would improve. The 3,711 is used here before the place, two sections down, that says what it is.",
   False)

ch('fold-hours-mine',
   "What is mine is the longitude left free at every start, every month tried as a start, and one count:",
   "What is mine, as far as those papers and six searches of the web showed, and six searches are not a survey, is the longitude left free at every start, every month tried as a start, and one count:",
   "A caution lost on the way. The hours note says of this very count: 'That is not a claim of novelty ... the six searches made since ... are not a survey', and 'a paper I did not find may well have it'. 'What is mine is' drops that.",
   True)

ch('fold-hours-259',
   "The start of 259 BC, which the dial note leaves out of the sixteen by one solar month, fits the hours at 10° E (3.20 h). And the longitude is good only to about nine degrees.",
   "The start of 259 BC, which the dial note leaves out of the sixteen by one solar month, fits the 18 hours at 10° E (3.20 h), and with all 22 hours it fits better than 205 BC does (3.67 h at 20° E against 3.91 h at 36° E). So that the choice lies among those four leans on the sixteen. \"The Greek world\" is my line, 10° to 40° E, drawn after the run; Carman and Evans's own interval for the place, at 95%, is 7.8° to 42.8° E. They and Jones (2020) both weigh the cycle of 259 BC and set it aside: Carman and Evans (section 22.1) because their fit of the Sun's part in the hours wants the dial's first full moon between late April and late May, and that of 259 BC falls on 10 April; Jones because the Sun is less well placed, more of the hours are far out, and the date is so early. Those grounds are theirs and are not tested here. And the longitude is good only to about nine degrees.",
   "The story's short caution on 259 BC ('why-259') needs its figures and its sources here, and the note's caution was only half carried over: the half left out is the stronger one, that with all 22 hours 259 BC fits better than 205 BC (after_check.out: 3.67 h at 19.75° E against 3.91 h at 35.5° E). The note also says that 'in the Greek world' is the author's line, drawn after the run. I read Carman and Evans's section 22.1 ('too early in the year') and section 20 (the interval), and Jones's paragraph on 259 BC ('superior' on two counts, 'less satisfactory' for the Sun, 'many more data points have large errors', 'even more uncomfortably early').",
   True)

ch('fold-wrong-hour',
   "I had also taken one hour from a summary list that does not say day or night.",
   "I had also taken one hour as an hour of the day from a summary list that does not say day or night. It is an hour of the night, as that reader found in the edition of the glyphs, and the figures that used it were worked again.",
   "As it stands this sentence, under 'What I got wrong', does not say what was wrong, and the first reader of the story noticed that it and the story's 'an hour of the night for an hour of the day' are not the same statement. The story's wording is the fair one: the note says the first version 'had 72S as the second hour of the day, from their summary list, which does not say day or night; the reader found it in the edition', and that the script was rerun with it corrected.",
   True)

ch('fold-sealed-tables',
   "after reading Carman and Evans's table, one of their sections and their conclusions,",
   "after reading two of Carman and Evans's tables, one of their sections and their conclusions,",
   "Would improve. The sealed sheet takes the hours from their Table 11 and says its author had seen their Table 16, and the first version of the hours note lists as read 'Table 11 (the hours), section 13 (the rule for the clock), Table 16': two tables. What was and was not read before sealing is otherwise the author's own account; I could check it only against those two lists.",
   False)

ch('fold-above',
   "The published datings turn on the hours engraved beside the glyphs, which are taken up under \"The hours\" below.",
   "The published datings turn on the hours engraved beside the glyphs, which are taken up under \"The hours\" above.",
   "'The hours' now stands before 'What was already known', so from this sentence it is above, not below. (The two other pointers, in 'The eclipse dial', are rightly 'below'.)",
   True)

ch('fold-sources-voulgaris',
   "another start date; the hours are tried against it under \"The hours\".</li>",
   "another start date; the hours are tried against it under \"The hours\". That its authors take the hours for the mechanism's own predictions is from a later paper of theirs, \"A Revision for the Draconic Gearing of the Antikythera Mechanism, the eclipse events of Saros spiral and their classification\", arXiv:2412.07023 (2024).</li>",
   "A source is missing. The new section says of the authors that they 'hold that the hours are the mechanism's own predictions and not times taken from the sky'. That is from their later paper (its abstract: the events 'are calculated by pure mechanical processing' and 'are not documented observed events'), which the list of sources does not have. Title and number checked against the saved abstract page.",
   True)

ch('fold-sources-meeus',
   "<li>JPL Horizons, ephemeris DE441; F. Espenak and J. Meeus, Five Millennium Catalog of Lunar Eclipses and of Solar Eclipses, NASA.</li>",
   "<li>JPL Horizons, ephemeris DE441; F. Espenak and J. Meeus, Five Millennium Catalog of Lunar Eclipses and of Solar Eclipses, NASA.</li>\n<li>J. Meeus, Astronomical Algorithms (2nd edition, 1998), chapter 49: the times of full and new moon used for the hours, typed from memory and tested against JPL's tables (never more than 2.5 minutes out for 205 to 129 BC).</li>",
   "Would improve. The new section sets the hours against 'the true times of full and new moon' and does not say where those come from. The hours note does: Meeus's algorithm, from memory, tested against JPL's tables (and by its first reader against the catalogue across all three centuries).",
   False)

# ---------------------------------------------------------------- checks
problems = []
spans = []
for c in C:
    n = src.count(c['old'])
    if n != 1: problems.append(f"{c['id']}: old occurs {n} times")
    else:
        i = src.index(c['old']); spans.append((i, i + len(c['old']), c['id']))
    if c['old'] == c['new']: problems.append(f"{c['id']}: no change")
spans.sort()
for a, b in zip(spans, spans[1:]):
    if a[1] > b[0]: problems.append(f'overlap: {a[2]} and {b[2]}')
ids = [c['id'] for c in C]
if len(ids) != len(set(ids)): problems.append('duplicate ids')

def apply(text, which):
    out = text
    for c in which: out = out.replace(c['old'], c['new'])
    return out

class Bal(HTMLParser):
    VOID = {'br', 'img', 'meta', 'link', 'hr', 'input'}
    def __init__(self): super().__init__(); self.stack = []; self.bad = []
    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID: self.stack.append(tag)
    def handle_endtag(self, tag):
        if tag in self.VOID: return
        if not self.stack or self.stack[-1] != tag: self.bad.append(tag)
        else: self.stack.pop()
def balanced(text):
    p = Bal(); p.feed(text); return not p.bad and not p.stack, p.bad, p.stack

def words(s):
    s = re.sub(r'alt="[^"]*"', '', s); s = re.sub(r'<[^>]+>', ' ', s); return len(s.split())

for name, which in (('preview-all.html', C), ('preview-must.html', [c for c in C if c['must']])):
    out = apply(src, which)
    ok, bad, stack = balanced(out)
    if not ok: problems.append(f'{name}: tags do not balance: {bad} {stack}')
    f = out.index('<details class="fold">')
    print(f'{name}: story {words(out[:f])} words (now {words(src[:FOLD])}); fold {words(out[f:])} (now {words(src[FOLD:])}); READERS left: {out.count("READERS")}')
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(out)
ok, bad, stack = balanced(src)
print('source as it stands balances:', ok)

blob = json.dumps(C, ensure_ascii=False)
for pat in ('/' + 'tmp', r'/home/', r'/srv/', 'tool' + 'u_', r'agent[0-9]', r'[0-9a-f]{8}-[0-9a-f]{4}-', r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}', r'sk-[A-Za-z0-9]', r'session', r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'):
    m = re.findall(pat, blob)
    if m: problems.append(f'pattern {pat} in the JSON: {m[:3]}')
# characters not already used by the page (curly quotes, long dashes)
for chr_ in '’‘“”—':
    if chr_ in ''.join(c['new'] for c in C): problems.append(f'character {chr_!r} in a new string')

json.dump(C, open(os.path.join(HERE, 'changes.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(C), 'changes;', sum(c['must'] for c in C), 'must;', sum(not c['must'] for c in C), 'optional')
print('in the story:', [c['id'] for c in C if src.index(c['old']) < FOLD] if not problems else '')
print('PROBLEMS:', problems if problems else 'none')
