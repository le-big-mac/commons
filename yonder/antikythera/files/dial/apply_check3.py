"""Apply the fifteen changes of the narrow third reading (check-3.md) to README.md as the reader worded them.
Each replacement must match exactly once. The header's last sentence is the reader's, with one sentence of mine after it."""
p = 'README.md'; s = open(p).read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
def w(t): return ' '.join(t.split())      # match across the file's line breaks
import re
def repw(a, b):
    """Replace text that may be broken across lines in the file: match on words, keep the replacement on one logical run."""
    global s
    pat = r'\s+'.join(re.escape(x) for x in a.split())
    m = re.findall(pat, s)
    assert len(m) == 1, (a[:70], len(m))
    s = re.sub(pat, lambda _: b, s)

# 1 header
repw("After that reading I reached Freeth's supplementary notes and his paper of 2019, and added",
     "While that reading was under way I reached Freeth's supplementary notes and his paper of 2019, which the\nreader did not have, and afterwards added")
repw("READER3*", "A third reading (`check-3.md`) was narrow: it checked these\nseven additions word for word against Freeth's supplementary notes and tables and the text of his 2019 paper,\nre-scored the eight dates of his Table S5, and compared this text with the second reader's wording; it did\nnot go over the counts, the sealed sheets or the rest of the note again, and it could not see the figures of\neither paper. Its fifteen changes are made as it worded them (`apply_check3.py`) and have not been read\nagain.*")
# 2 point 1
repw("For Freeth's list this is his own finding, re-made: his supplementary note says",
     "For Freeth's list the first of these counts (37 of 38 and 28 of 28) is his own finding, re-made: his\n   supplementary Note S5 says")
repw('and that "Otherwise, all the glyphs are matched with corresponding eclipses."',
     'and that "Otherwise, all the glyphs are matched with corresponding eclipses." (He does not say\n   there that penumbral eclipses count; ten of the matches need them.)')
# 3 point 2
repw("with a second condition on the Moon's apogee; Carman and Evans tabulate the candidates a Saros apart). The count puts it in months.",
     "with a second condition on\n   the Moon's apogee, and his supplement reports the search I make here, over 400 BC to 1 BC, with 35 starts\n   at which every glyph of his model is matched; Carman and Evans tabulate the candidates a Saros apart). My\n   count adds which starts they are and how each scores.")
# 4 where the two lists differ
repw("Jones (2020) keeps 213 in his text; his Table 1 of the 38 full moons lists cell 214.",
     "Jones (2020) keeps\n213 in his text; his Table 1 of the 38 full moons lists cell 214. Freeth for his part says in Note S3 that the\nindex letter on which the solar glyph of month 207 rests is uncertain and \"not essential for the theory\":\nwith the southern limit at 6 units in place of 7 his model drops that glyph and no other. The 49 cells\nagainst 51 turn on one character in the text beside the dial. Freeth (2019) traces it, grants that it \"looks\nsomewhat like a lower case ω\" and takes it for an unknown extra symbol; Iversen and Jones read it as the\nbarred omega that ends the second alphabet, which makes month 213 the 48th glyph and leaves no room for\nglyphs in 207 and 214.")
# 5 other start dates: a bullet before M4, and three changes inside M4
repw("- Freeth's own eight candidates (Table S5 of his supplement:",
     "- Freeth made this search before me. His Note S5 takes every start month from 400 BC to 1 BC (\"just under\n  5,000 lunar months\") and finds 113 at which the surviving glyphs \"match the actual eclipse record, both in\n  position and type of eclipse\", all of them only with penumbral eclipses let in, and 35 at which \"the full\n  sequence predicted by EYM\" does. He gives the numbers and no dates, and says of the first that it is \"not\n  very promising for determining the epoch\". In the three centuries I have, every glyph of his model is\n  matched at 31 starts (the 31 above; 13 of them the right way round) and at none without penumbral eclipses.\n  205 BC is not one of them, for want of month 125, as he notes.\n- Freeth's own eight candidates (Table S5 of his supplement:")
repw("chosen by the node and by the Moon's distance at the first full moon)",
     "those where the Sun's distance from the node at the new moon before month 1 is within 5° of his model's and\n  the Moon's disc at the first full moon within 2% of its smallest)")
repw("are among my 16; the other four", "are among my 16 and all eight among the 35; the other four")
repw("(The first two dates in his table are half a month after the full moons that lie whole cycles before 12 May 205 BC; I took those full moons.)",
     "(The first two dates printed in his table are new moons, half a month\n  after the full moons that lie two and one whole cycles before 12 May 205 BC; the other figures in those rows\n  step by a whole cycle like the rest, so I took those full moons.)")
# 6
repw("once penumbral eclipses were let in,", "once penumbral eclipses were let in\n(the 113 of Freeth's note),")
# 7 the slip
repw("which fits the catalogue's verdict that 223 BC does slightly better.",
     "which fits the catalogue's verdict that 223 BC does slightly better.\nFreeth's Table S5 has the same slip from another ephemeris: the Sun's distance from the descending node at the\nnew moon before month 1 is 54.12°, 54.59°, 55.06°, 55.54° and 56.01° for his five starts a cycle apart, 0.47°\na step. For 205 BC my fit makes it 55.3°. His note sets the model's own figure at 53.27°, which would put\n205 BC 1.8° out where I say 0.6°; that figure counts the node point's 66 units from the new moon, where the\nmodel of his main text, as I coded it, counts them from the start of the month 2 units later, which makes it\n54.9°.")
# 8 first bullet of what this is
repw("at which the real node falls where the model has it and the Moon is at apogee",
     "at which the real node falls within 5° of where the model\n  has it and the Moon is at apogee")
repw("What I add is the count of months for the whole of both lists, the same count for every other start in three centuries, and the decay over twenty-two centuries.",
     "What I add is the count for Iversen and Jones's list, the dates and scores of the\n  other starts (Freeth gives only how many match), and the decay over twenty-two centuries.")
# 9 visibility
repw("is another matter, and the hours inscribed on the glyphs are not tested here.",
     "is another matter: Freeth's Note S4 says that of the 28 solar eclipses of this cycle\n  \"only 8 were visible from anywhere in the ancient Greek empire\". The hours inscribed on the glyphs are not\n  tested here.")
# 10 limits
repw("**The limits in degrees are mine.** The dial's limits are in its own units; I turned them into latitudes with the mean inclination.",
     "**The limits in degrees are a conversion.** The dial's limits are in its own units; I turned them into\n  latitudes with the mean inclination. Freeth's Note S3 has a conversion of his own, 0.0720° of latitude to\n  the unit, which gives 1.44° and 0.50° where I have 1.43° and 0.51°. (The same note gives 7 units as 5.4°\n  from the node; his own factor of 180/223 of a degree to the unit makes it 5.65°, my 5.7°.)")
# 11 slip bullet
repw("Jones (2020) works out that the error of the hours grows with each cycle,",
     "Freeth's Table S4 follows one lunar and one solar eclipse through nine later cycles (the error in\n  the hour reaching \"more than five hours over nine Saros periods\"), and Jones (2020) works out that the error\n  of the hours grows with each cycle,")
repw("and in Freeth's Notes S3 and S5.",
     "and in Freeth's Notes S3\n  and S5. The third reader went through Notes S1 and S4 and the tables as well and found the matches counted\n  for the first cycle and for other starts, and nothing on the cycles after; the caption of Figure S1 gives a\n  Saros series 12 to 15 centuries, which is where my last months end.")
# 12 Voulgaris
repw("and they number the cells one off from everyone else (their section 3.2), so my scan of starts does not speak to it.",
     "and they number the cells one off from everyone\n  else and put a solar glyph in their first cell (their section 3.2), so my scan, which keeps the usual\n  glyphs, does not test their scheme; the three lunations it tries nearest that date score 0, 33 and 43 of 66.")
repw("I have read only their abstract and have not tested that date;", "I have read only their abstract and section 3.2 and have not\n  tested that date;")
# 13 M3
repw("regroups the letters that index the glyphs and keeps the model and its count",
     "moves two index letters from one group to another in the text beside the dial and\nkeeps the model, its months and its count")
# 14 M7
repw("which hold his own match of the glyphs to the eclipses of 205 to 187 BC, I reached only after both sheets and both readers",
     "which hold his own match of the\n  glyphs to the eclipses of 205 to 187 BC and his own search of other starts, I reached only after both sheets\n  and the first reader, while the second was reading")
# 15 sources
repw("Of its supplement I have read Notes S3 and S5 and Table S5, and not the figures or the other notes.",
     "Of its supplement I\n  have read Notes S3 and S5, the passages of Note S4 on visibility and on Table S4, and Tables S4 and S5, and\n  not the figures (only S1 is on disk) or the rest.")
# files
repw("`README-as-second-read.md`, `apply_check2.py` (the changes as applied).",
     "`README-as-second-read.md`, `apply_check2.py` (the changes as applied); `check-3.md`,\n`README-as-third-read.md`, `apply_check3.py`.")
open(p, 'w').write(s)
print('applied')
