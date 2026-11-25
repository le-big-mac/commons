"""Apply the first reader's changes to the README, as worded, and re-wrap. Not part of the study."""
import re, sys, textwrap
src, out = sys.argv[1:3]
W = 112
def unwrap(text):
    blocks = text.rstrip('\n').split('\n\n'); res = []
    for b in blocks:
        ls = b.split('\n')
        if ls[0].startswith(('#', '|', '!')): res.append(('raw', b)); continue
        if re.match(r'(- |\d+\. )', ls[0]):
            items = []
            for l in ls:
                if re.match(r'(- |\d+\. )', l): items.append(l)
                else: items[-1] += ' ' + l.strip()
            res.append(('list', items)); continue
        res.append(('para', ' '.join(l.strip() for l in ls)))
    return res
def rewrap(blocks):
    o = []
    for kind, b in blocks:
        if kind == 'raw': o.append(b)
        elif kind == 'para': o.append('\n'.join(textwrap.wrap(b, W, break_long_words=False, break_on_hyphens=False)))
        else:
            ls = []
            for it in b:
                ind = ' ' * len(re.match(r'(- |\d+\. )', it).group(1))
                ls += textwrap.wrap(it, W, subsequent_indent=ind, break_long_words=False, break_on_hyphens=False)
            o.append('\n'.join(ls))
    return '\n\n'.join(o) + '\n'
CH = [
 ("were sealed before any table of the real sky was read", "were sealed before the analysis read any of the fourteen sky tables (they were already on disk; I had looked at one ten-row test table of the Moon to check the request)"),
 ("This first version has not yet been read by anyone but me.", "A fresh instance checked the first version by measurements of its own (`check.md`, `check-scripts/`): the numbers stood and a good deal of the wording did not. Its changes are made as it worded them; figures marked as the reader's are from its scripts and not from mine."),
 ("**Against the stars, the five planets are nearly as good as new.**", "**Against the stars, three of the five planets are nearly as good as new.**"),
 ("(for Mars and Saturn the theory's error and the gears' drift happen to cancel)", "(for Mars the theory's error and the gears' drift happen to cancel, for Saturn they cancel in part, and Mercury stands where its 6° of phase error does not show)"),
 ("are scarcely worse than", "are only a tenth to a fifth worse than"),
 ("**The reason is that the circle theory was always the larger error.**", "**The reason is that for those three the circle theory is still the larger error.**"),
 ("lose only 1.4° (Jupiter) to 14.4° (Venus) of phase in 2,231 years", "are out by only 1.4° (Jupiter) to 14.4° (Venus) of phase after 2,231 years"),
 ("the theory had from the start.", "the theory had from the start (figures beyond 2,231 years assume the measured rate goes on). For Venus and Saturn the gears have been the larger error for most of the span."),
 ("Its pointer stands 105° ahead of the Moon.", "Its pointer stands 105° ahead of the Moon (the gears' Moon has fallen 262° behind, which is 98° ahead; the misplaced apsides and the theory's own error make up the rest)."),
 ("**Against the seasons everything but the Sun is tens of degrees out**, because the period relations count returns to the same stars, and the maker's time knew no precession (31.0° over the span, read from the Sun).",
  "**Against the seasons the planets' pointers are 14° to 38° out** (rms over the 76 years to today; 8° to 38° today), because the planets' period relations count returns to the same stars and take no account of precession (31.0° over the span, read from the Sun). The Moon's Metonic ratio is the exception: it fits the seasons better than the stars (121° against 262°)."),
 ("**The eclipse dial has nothing left.** A dial engraved", "**The eclipse dial has nothing left.** (The dial is a spiral of 223 cells, one for each lunation of an eighteen-year eclipse cycle; a glyph marks a cell whose month has an eclipse.) A dial engraved"),
 ("turned one cell a lunation, it catches none. The pattern itself survives: turn the scale 43 cells and all 41 solar eclipses fall on a glyph again.",
  "with the dial stepped one cell for each real lunation, it catches none, where chance would catch 7.5 and 3.6. (Turned by the Sun instead, the dial would stand 0.7 of a cell behind against the stars: 6 of 41 solar, no lunar; the reader's figures.) The pattern itself survives: turn the scale 43 cells and all 41 solar eclipses and 25 of the 28 lunar ones fall on a glyph again. Arithmetic gives the same 43: 223 lunations fall 0.48° short of 242 returns to the node, 59° in 123 cycles, and 43 lunations move the Moon 59° from a node."),
 ("of theirs in size.", "of theirs in size; for Mars the sign differs too (mine −0.0021° a year, theirs +0.0031)."),
 ("and 0.99. Their definition", "and 0.99 (the tables catch a slow swing of Jupiter and Saturn against each other, which long-run rates leave out). Their definition"),
 ("Their definition is in a supplement I could not fetch, so this is a difference to note and not an error found.",
  "Their definition is in a supplement I could not fetch. Their second column (error per synodic cycle) is the first times the years per cycle for four planets, so it is an error of synodic phase like mine; for Saturn the two columns disagree (0.004509 printed, 0.004356 implied). Read with a sidereal year, their errors imply true synodic periods of 115.8772, 583.927 and 779.960 days for Mercury, Venus and Mars, against 115.8775, 583.921 and 779.936 from JPL's rates (the reader's reckoning). A difference to note and not an error found."),
 ("| Venus | 289/462 | the same (read on the front cover inscription) |", "| Venus | 289/462 | the same (the 462 years are read on the front cover inscription) |"),
 ("| Saturn | 427/442 | the same (read on the front cover inscription) |", "| Saturn | 427/442 | the same (the 442 years are read on the front cover inscription) |"),
 ("the same, as corrected; a hand the paper calls hypothetical", "the same; a hand the paper calls hypothetical"),
 ("which is the kindest setting a maker could have reached", "which is kinder than any setting a maker could have reached"),
 ("one of them more than half a turn", "two of them (the Moon's and the apsides') more than half a turn"),
 ("was 0.4° out for the outer planets (`trial-first-runs.out`); ellipses mended it.", "was 0.4° out for the outer planets (that output was not kept; `trial_dbg.py` prints the bias); ellipses mended it (`trial-first-runs.out` is the run after the mend, with the span still between window centres)."),
 ("√2 times the floor.", "√2 times the floor. Above 2,231 years it extrapolates the measured rate."),
 ("Mercury −1.5° = theory −1.6° and drift +0.1°", "Mercury −1.5° = theory −1.6° and phase +0.1°"),
 ("Mars +0.5° = −4.7° and +4.7°;", "Mars +0.5° = −4.7° and +4.7°, and +0.5° because the epicycle fitted then is a hundredth larger than today's;"),
 ("+5.7° and −8.3°.", "+5.7° and −8.3°. \"Theory\" is what today's own best circle fit leaves today; \"phase\" is the effect of the pointer's phase standing off that fit's (+4.3° Mars, −1.7° Jupiter, −7.7° Saturn). These are not quite the drifts of the table (+4.7°, −1.4°, −9.8°): a circle fitted to an ellipse, read at the window's edge, puts the mean longitude up to 1.4° off, differently in each window. Set over the first window at the gears' own rates instead, today's errors would be Moon +110°, Mars −0.9°, Saturn −3.3°, the others within 0.3° of the above (the reader's figures, `check-scripts/check5.out`)."),
 ("| the 223 lunations to today (cycle 123) |", "| the 223 lunations to today (122.7 to 123.7 cycles after the engraved one) |"),
 ("for the lunar ones the best turn is 125 cells, 26 of 28.", "the same turn catches 25 of the 28 lunar ones (125 cells catches 26; with the lunar threshold at 0.9° or 1.1° the best turn is 43). None is caught at thresholds from 1.2°/0.8° to 1.8°/1.6° (the reader's figures)."),
 ("against 0.25 for always saying 50% (`score.out`).", "against 0.25 for always saying 50% and 0.077 for always saying 90% (`score.out`)."),
 ("near-certain once the arithmetic was right.", "near-certain once the arithmetic was right. Five were open (K11, K16a, K18, K19a, K19b); three of those held."),
 ("showing the new and full moons and eclipses of 1977 to 2071 on the right days", "its zodiac redrawn for 30° of precession and its pointers set from a recent eclipse (within about 100 years, the authors say), showing new and full moons and eclipses on ten dates from 1977 to 2071"),
 ("Three searches found no one who had turned it on from its own epoch and read every pointer.", "Three searches (for the mechanism \"if it had been running\" and its accumulated error after two thousand years; for its period relations against sidereal and tropical years; for a simulation set to the present day and compared with today's sky) found no one who had turned it on from its own epoch and read every pointer."),
 ("![The dial today](dial-today.png)", "![The dial today](dial-today.png)\n\n*Rings from the centre: Moon, Mercury, Venus, Sun, Mars, Jupiter, Saturn; each label sits on its ring.*"),
 ("![Then and now](then-and-now.png)", "![Then and now](then-and-now.png)\n\n*Twenty of the 76 years are drawn; the figures in the titles are for all 76.*"),
 ("`after2.out` (after the fact); `plots.py`, `dial-today.png`, `then-and-now.png`.", "`after2.out` (after the fact); `plots.py`, `dial-today.png`, `then-and-now.png`; `README-as-first-read.md`, `check.md` (the reader's brief and report), `check-scripts/` (the reader's own measurements; its 15 MB cache of the tables and its page renders of a paper are left out). A note in `gears.py` says the node ratio is \"as corrected\"; the paper as I fetched it prints −5/93 and I have not seen what the correction changed."),
]
blocks = unwrap(open(src).read())
done = [0] * len(CH)
res = []
for kind, b in blocks:
    def rep(s):
        for i, (a, c) in enumerate(CH):
            n = s.count(a)
            if n: done[i] += n; s = s.replace(a, c)
        return s
    if kind == 'list': res.append((kind, [rep(it) for it in b]))
    else: res.append((kind, rep(b)))
bad = [CH[i][0][:50] for i, n in enumerate(done) if n != 1]
assert not bad, (bad, done)
# captions were inserted inside raw blocks: split them out again so they are wrapped as paragraphs
text = rewrap(res)
open(out, 'w').write(text)
print('applied', sum(done), 'changes')
