"""Apply the second reader's nineteen changes (check-2.md) to README.md as they worded them, then my own additions
from Freeth's supplementary notes and his 2019 paper (marked M below). Each replacement must match exactly once."""
import sys
p = 'README.md'; s = open(p).read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)

# 2 (reader) and M1: point 1
rep("(27 partial or total, 10\n   penumbral only), and all 28 of its solar months",
    "(27 partial or total; 10\n   penumbral only, the Moon passing through the Earth's faint outer shadow, which the eye can hardly see),\n   and all 28 of its solar months")
rep("""list of Iversen and Jones (2019), which differs in four entries, the counts are 36 of 38 and 27 of 28.
""", """list of Iversen and Jones (2019), which differs in four entries, the counts are 36 of 38 and 27 of 28.
   For Freeth's list this is his own finding, re-made: his supplementary note says there is no lunar eclipse
   in month 125 and that "Otherwise, all the glyphs are matched with corresponding eclipses."
""")
# 3: point 2, whole
a = s[s.index("2. **That fit is what the start date was chosen for"):s.index("3. **It goes wrong slowly")]
rep(a, """2. **That fit is what the start date was chosen for, and about one start in 230 gives it.** Freeth picked
   205 BC from the dates at which the real node falls where his model has it, so the fit is not a discovery;
   nor is it news that such dates are few (Freeth has eight between 250 and 1 BC, with a second condition on
   the Moon's apogee; Carman and Evans tabulate the candidates a Saros apart). The count puts it in months.
   Of the 3,711 lunar months between 300 BC and 1 BC that could be the dial's month 1, six in ten score
   nothing at all and one in five scores half of the 66 or more. Sixteen do as well as 205 BC with the nodes
   the right way round: 299 BC, then one or two in every cycle from 223 BC to 17 BC. Thirteen of the 16
   score all 66, which 205 BC does not; 223 BC and 299 BC are among them (38 and 28). Three leave no northern
   solar eclipse unmarked: 205 BC itself, 223 BC and 299 BC. In 205 BC the dial is centred on the real nodes
   to 0.6°, where its own zone for a lunar eclipse is 16° either side.
""")
# 4: point 3
rep("The node slips 0.47° a cycle against the dial (0.475° by the\n   books). Counted",
    "The node slips 0.47° a cycle against the dial (0.475° by the\n   books), so the months the model puts furthest before a node point lose their eclipses first (lunar months\n   125, 37, 172 and 84, in that order; solar months 13 and 60), and no month that has lost its eclipse gets\n   one back. Counted")
# 5: point 5
rep("The eclipses of 2024 to 2026 fall two\n   cells after the dial's marks.",
    "The six lunar eclipses of 2024 to 2026\n   each fall two cells after a lunar glyph, and four of the six solar eclipses two cells after a solar one.")
# 6: point 6, whole
a = s[s.index("6. **Where the two published lists differ"):s.index("![how long the dial's months kept their eclipses]")]
rep(a, """6. **Where the two lists differ, the months Freeth marks held eclipses from 205 BC and the months Iversen
   and Jones mark did not. That does not tell which was engraved.** Freeth has a lunar glyph in month 214 and
   a solar one in month 207; Iversen and Jones have them in 213 and 196 (Carman and Evans set out both lunar
   patterns in 2014 and chose 213). In the sky, months 214 and 207 held an eclipse in each of the first six
   cycles; month 213 held none after 224 BC and month 196 none before 171 BC. But where the stone can be read
   it sides against the sky in the same way: month 125, whose lunar glyph survives, held no eclipse after
   213 BC, and month 126 next to it, which has no glyph, held one in every cycle. Iversen and Jones say as
   much: by their reckoning the lunar glyphs imply a node 2° to 3° from the one the solar glyphs imply, and it
   is the solar one that agrees with 205 BC. The cells in question are lost, and they argue from the letters
   that index the glyphs to the text beside the dial.

""")
# 18: under the figure
rep("![how long the dial's months kept their eclipses](dial-kept.png)\n",
    "![how long the dial's months kept their eclipses](dial-kept.png)\n\nFreeth's list. The axis stops at 1,680 years; nothing returns after.\n")
# 7: the nodes explained
rep("the Sun passes the Moon's nodes at 66 and 289. A month gets a",
    "the Sun passes the Moon's nodes at 66 and 289 (the nodes are the two points where the Moon's path crosses\nthe Sun's; there can be an eclipse only when a full or new moon falls near one). A month gets a")
# M2: the consecutive-month rule, from Note S3 (replaces the first reader's change 5, which the supplement overtakes)
rep("""(The paper says only that "the consecutive month rule excludes a second lunar
eclipse prediction in the same month"; I read that as the later of the two. Dropping the earlier gives the
same totals but removes months 125 and 172, whose lunar glyphs survive.)""",
"""(The paper says only that "the consecutive month rule excludes a second lunar
eclipse prediction in the same month". His supplementary Note S3 makes it the later of the two: an earlier
model "generated lunar glyphs in both Months 125 and 126", its authors "justified exclusion of the second
lunar glyph", and "The current model has the same defect in the same month—as well as two additional
months—and the same solution is adopted." Months 125 and 172, the first of their pairs, have lunar glyphs
that survive.)""")
# M3 and 19 (second half): how Iversen and Jones was found; Freeth 2019
rep("""I found this
paper only in the searches before the second sheet, after the first run. By its account Freeth (2019) keeps
51 cells; I have not read that paper.""",
"""I found this
paper after the first run and after the second sheet was sealed: its link was among the results of the
searches made before that sheet, and I did not see what it was until I fetched it afterwards with two others.
Freeth's own revision (2019) regroups the letters that index the glyphs and keeps the model and its count
("there were almost certainly 51 glyphs in all").""")
# 8: the sky
rep("So the\ncatalogue's numbers place every eclipse in a month of the dial, in any century.",
    "The\nnumbers run without a break: set against the calendar dates, all 11,450 eclipses fall in the lunation their\nnumber gives, across the calendar change of 1582 and the year 0 (`check-2-scripts/run1.out`). Carman and\nEvans's Table 16 pairs 18 of the surviving glyphs with catalogue eclipses of 205 to 187 BC by lunation number,\nand all 18 fit the same rule. So the catalogue's numbers place every eclipse in a month of the dial, in any\ncentury.")
# 9
rep("The last whole cycle is 122, which ended in 2013.", "The last whole cycle is 122, which ended with the new moon of 1 January 2014.")
# 17: catalogue heading
rep("`catalogue_all.out`, `two_lists.out`. Each cell gives Freeth's list and then Iversen and Jones's.",
    "(19 of the 123 cycles; all are in the json files.) `catalogue_all.out`, `two_lists.out`. Each cell gives\nFreeth's list and then Iversen and Jones's.")
# 10
rep("By Freeth's list no count of marked months ever rises from one cycle to the next; by Iversen and Jones's\nthe solar count rises once",
    "By Freeth's list neither the lunar months with an eclipse of any kind nor the solar months ever rise from\none cycle to the next; the partial-or-total count rises once, from 27 to 28 after the first cycle (months 73\nand 214 turn partial, month 2 turns penumbral). By Iversen and Jones's the solar count rises once")
# 11
rep("| 213 | no lunar glyph | lunar | no lunar eclipse in any of the six cycles (in the tables' four cycles the full moon is at −1.59° to −1.78°) |",
    "| 213 | no lunar glyph | lunar | no lunar eclipse in any of the six cycles; its last, a faint penumbral one, was in 224 BC (in the tables' four cycles the full moon is at −1.59° to −1.78°) |")
# 12: closing paragraph of "Where the two lists differ"
a = s[s.index("So Iversen and Jones's list scores one lower than Freeth's on each count in cycle 0."):s.index("### The glyphs read on the fragments")]
rep(a, """So Iversen and Jones's list scores one lower than Freeth's on each count in cycle 0. Their list is not an
attempt to fit the sky, and the sky of 205 BC is a poor judge of it. Carman and Evans (2014) had already set
out the two lunar patterns, with 214 and with 213, and chosen 213. Iversen and Jones hold that the dial's
lunar months were those where a mean full moon is nearer the node than its neighbours, which by their own
account leaves 213 or 214 open, and that the solar months were chosen by a mean latitude between about −0.45°
and +1.45°. What settles 213, and rules out a glyph in 207, is the index letters: two letters that the text
beside the dial lists together must belong to cells 213 and 219. The lower limit is then drawn so that month
207 (−0.54° by their reckoning) falls just outside; month 196 (+1.41°) falls just inside the upper one, and
they call it "The only remaining uncertainty". They report that the lunar pattern implies an elongation from
the node of 127.1° to 127.7° at the start of the dial where the solar pattern implies 125.0° and Ptolemy's
theory gives 124.6° for 205 BC, and that with 125.0° the lunar glyphs would be "in cell 38 instead of 37, in
cell 126 instead of 125 (which is a surviving lunar glyph), and in cell 214 instead of 213". The catalogue
shows the same: in cycle 0 month 126 has an eclipse and 125 none, 214 has one and 213 none (37 and 38 both
have one). Since the glyph that survives is in 125, agreement with the sky of 205 BC is no guide to the lost
cells. Nor is the solar pair a clean test: month 2, which neither list marks, held a total solar eclipse in
cycle 0 (gamma −0.43), less far south than that of month 78 (−0.50), whose glyph survives. Jones (2020) keeps
213 in his text; his Table 1 of the 38 full moons lists cell 214.

""")
# 13: other start dates, first three bullets
a = s[s.index("- A start chosen blindly scores nothing: the median"):s.index("- Whole cycles before 205 BC score 38 lunar months")]
rep(a, """- Most starts score nothing: 62% have A + S of 0 of 66, and the median is 0. The glyphs come six months
  apart, as eclipses do, so a dial out of step by two to four months misses them all. But a dial in step
  scores well whichever node it starts at: 20% of starts score 33 or more, 5.6% score 60 or more, and 79 score
  65 or 66.
- 43 starts do at least as well as 205 BC on A, S and U, and 31 of them score 66 of 66, which 205 BC does
  not. But 27 of the 43 have the nodes the wrong way round: they are an odd number of eclipse seasons from a
  start like 205 BC, so the Moon is going south where the dial has it going north, and the dial's lopsided
  solar rule leaves out 12 to 15 northern eclipses where it should leave out southern ones.
- Of the 16 left, three have no such eclipse, as 205 BC has none: 299 BC, 223 BC and 205 BC. The other 13
  have one or two and lie between 187 BC and 17 BC (`readme_check.out`). These are small partial eclipses in
  the far north (magnitude 0.01 to 0.47). Thirteen of the 16 score 66 of 66; 205, 187 and 169 BC score 65. The
  16 depend on how "as well" is put: asking for A + S of 65 or more with U of 0 gives 35 starts the right way
  round, among them the whole cycles from 295 to 241 BC (38 and 27). For Iversen and Jones's list the same
  three have none, and 15 others have one or two.
""")
# M4: Freeth's own table of starts, after the whole-cycles bullet
rep("""one cycle on, in month 196.

So the months narrow""", """one cycle on, in month 196.
- Freeth's own eight candidates (Table S5 of his supplement: 241, 223, 205, 187 and 169 BC, and 49, 31 and
  13 BC, chosen by the node and by the Moon's distance at the first full moon) all score 65 or 66 of 66 by this
  count (`freeth_starts.out`). Four of them, 223, 205, 187 and 169 BC, are among my 16; the other four have 27
  solar months where I asked for 28.

So the months narrow""")
# 14: closing paragraph of other starts
a = s[s.index("So the months narrow 3,711 possible starts to 16, and 205 BC"):s.index("### The slip")]
rep(a, """So the months narrow 3,711 possible starts to 16 (35 on the looser reading), and 205 BC is among them but is
not the best of them. Carman and Evans have this in another form. The solar eclipse that each of the 16 puts
in month 13 is, for the 14 that fall within it, an entry of their Table 10, the candidates for that eclipse a
Saros apart in series 42, 44, 46 and 48; the step of 47 months from one run of starts to the next is the
Babylonian re-calibration they describe. They report that Freeth and others (2008) fitted the glyphs to
computed eclipses and found "over a hundred possible fits for epoch date" once penumbral eclipses were let in,
and they call it "a fallacy to suppose that the epoch of the Antikythera mechanism's Saros dial could be
reliably determined simply by matching its predictions against real eclipses". The months cannot choose
within the 16; the published datings do that with the hours inscribed on the glyphs, which I have not tested.

""")
# 15 and M5: first bullet of "what this is and is not"
rep("""has it and the Moon is at apogee at the first full moon; the Sun's anomaly picks 205 BC among them. So the
  centring in point 2 is his criterion, measured, and most of point 1 follows from it.""",
"""has it and the Moon is at apogee at the first full moon; the Sun's anomaly picks 205 BC among them. So the
  centring in point 2 is his criterion, measured, and most of point 1 follows from it. He also made the
  comparison of point 1 himself: his supplementary Note S5 sets the glyphs against the actual eclipses of the
  cycle from 205 BC and finds every one matched but the lunar glyph of month 125, where "the Moon was just a
  bit too far North for an actual eclipse to occur".""")
rep("What I add is the count of months, how few other starts match it, and the\n  decay over twenty-two centuries.",
    "What I add is the count of months for the whole of both lists, the same count for every\n  other start in three centuries, and the decay over twenty-two centuries.")
# 16 (with M6 in place of the reader's "which I have not seen", since I have now read Note S5)
a = s[s.index("What I did not find is a count of which marked months\n  held an eclipse, cycle by cycle."):s.index("- **Another start has been proposed.**")]
rep(a, """They also give the first step of the decay: "by year −149, solar Saros series 44
  had ended—this was no longer an actually occurring eclipse", which is my month 13 losing its eclipse in
  cycle 3. Their Table 16 pairs 18 of the surviving glyphs with catalogue eclipses of 205 to 187 BC, and
  Freeth's Note S5 matches all the glyphs of his model with the eclipses of the same years. Jones (2020) finds
  the cycle beginning in 259 BC "superior" to that of 205 BC on the node and the apogee and sets it aside on
  the hours. What I did not find is a count of all the marked months that held an eclipse, carried cycle by
  cycle. I looked in four searches; in Carman and Evans as far as I read it (the introduction, the passage on
  the Saros, the two lunar patterns, section 12 with its Table 10, Table 16, the conclusions, and the passages
  that searches of its text turned up, not all 82 pages; the second reader read further, `check-2.md`); in
  Iversen and Jones's section 4; in the passages of Jones (2020) on the Saros dial; and in Freeth's Notes S3
  and S5.
""")
# M7: last bullet, how late the supplement came
rep("""wrong: by its own limits solar months fail from the first cycle, and the eclipse it called missed in cycle 2
  was penumbral. The reader found both.""",
"""wrong: by its own limits solar months fail from the first cycle, and the eclipse it called missed in cycle 2
  was penumbral. The reader found both.
- **I read the sources in the wrong order.** Freeth's supplementary notes, which hold his own match of the
  glyphs to the eclipses of 205 to 187 BC, I reached only after both sheets and both readers (the copy I had
  tried first was behind a bot check; the publisher's own site serves them). Iversen and Jones I read after
  the second sheet. Both should have come before the first.""")
# sources
rep("""Antikythera Mechanism", PLoS ONE 9(7): e103275 (2014): the model, from its main text. Its supplementary notes
  I have not read.""", """Antikythera Mechanism", PLoS ONE 9(7): e103275 (2014): the model, from its main text. Of its supplement I
  have read Notes S3 and S5 and Table S5, and not the figures or the other notes.
- T. Freeth, "Revising the eclipse prediction scheme in the Antikythera mechanism", Palgrave Communications 5,
  7 (2019): read only for what it keeps and what it changes.""")
# 19 (first half): files
rep("`starts.py` and `.out`, `modern_cells.out`,\n`readme_check.py` and `.out` (this note's numbers recomputed).",
    "`starts.py` and `.out`, `freeth_starts.py` and `.out`,\n`modern_cells.py` and `.out`, `readme_check.py` and `.out` (this note's numbers recomputed).")
rep("The reader: `check.md`, `check-scripts/`, `after_check.py` and\n`.out` (my own look at the report's findings), `README-as-first-read.md`.",
    "The readers: `check.md`, `check-scripts/`, `after_check.py` and\n`.out` (my own look at the first report's findings), `README-as-first-read.md`; `check-2.md`,\n`check-2-scripts/`, `after_check2.py`, `after_check2b.py` and their `.out` (my own look at the second's),\n`README-as-second-read.md`, `apply_check2.py` (the changes as applied).")
open(p, 'w').write(s)
print('applied')

# Applied by hand straight after this script (25 Nov, before the narrow re-reading):
#  - in the slip bullet, "They also give the first step of the decay" became "Carman and Evans also give ...",
#    because a sentence about Jones now stands before it;
#  - M4 gained a parenthesis on the first two dates of Freeth's Table S5;
#  - the header's placeholder was replaced.
#  - four of my own changes to the second reader's words: point 6's headline says "in the cycle from 205 BC"
#    (month 196 does hold eclipses from 171 BC); "where the stone can be read" became "where the dial can be
#    read" (the dial is bronze); Jones sets 259 BC aside "on the Sun's anomaly and the hours"; the Voulgaris
#    bullet says they number the cells one off (the reader's finding 7);
#  - seven overlong lines rewrapped, no words changed.
