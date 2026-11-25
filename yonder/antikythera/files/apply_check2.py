"""Apply the second reader's changes to the mended README, as worded, and re-wrap. Not part of the study.
(One change between the two scripts was made by hand: the Sources line about the author correction.)"""
import sys
sys.path.insert(0, '/home/agent3/antikythera')
import importlib.util, re, textwrap
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
 # 1
 ("For Venus and Saturn the gears have been the larger error for most of the span.", "For Venus the gears have been the larger error for most of the span, for Saturn for half of it."),
 # 2 (the fuller form, with the second reader's figures, so marked)
 ("Its pointer stands 105° ahead of the Moon (the gears' Moon has fallen 262° behind, which is 98° ahead; the misplaced apsides and the theory's own error make up the rest). The Metonic ratio, 254 turns of the Moon in 19 of the Sun, loses the gears' Moon 262° against the stars over the span (it gains 121° if the Sun is kept true to the seasons instead).",
  "Its pointer stands 105° ahead of the Moon. The Metonic ratio, 254 turns of the Moon in 19 of the Sun, loses the gears' Moon 262° against the stars over the span (it gains 121° if the Sun is kept true to the seasons instead). On the dial 262° behind is 98° ahead; the Moon's 6° monthly swing about its mean place, applied 73° from the right point of its cycle, adds 8°, and the theory's own error takes off half a degree (the second reader's reckoning from my fits)."),
 # 3
 ("(mine −0.0021° a year, theirs +0.0031)", "(mine −0.0021° a year, theirs +0.0031; mine is the error of synodic phase, which for an outer planet is the deferent's drift of the table below with its sign turned)"),
 # 4
 ("against 0.25 for always saying 50% and 0.077 for always saying 90% (`score.out`).", "against 0.25 for always saying 50% (`score.out`) and 0.077 for always saying 90% (the reader's sum; lower is better)."),
 # 5
 ("None is caught at thresholds from 1.2°/0.8° to 1.8°/1.6° (the reader's figures).", "Unturned, the dial still catches none with the thresholds (new moon/full moon) at 1.2°/0.8°, 1.4°/0.9°, 1.6°/1.1° or 1.8°/1.6° (the reader's figures, as are the 25 of 28 and the best turn at other thresholds: `check-scripts/check4.out`)."),
 # 6, with the second reading named after it
 ("the numbers stood and a good deal of the wording did not. Its changes are made as it worded them; figures marked as the reader's are from its scripts and not from mine.",
  "the numbers stood (all but one borderline eclipse in the third cycle) and a good deal of the wording did not. Its changes are made as it worded them, with a few sentences and the attributions added by me; any figure they brought in that my outputs do not hold is from its scripts, marked as the reader's or not. A second instance checked what the mending had changed (`check-2.md`); its changes are made as it worded them and have not been read again."),
 # 7
 ("(the reader's figures, `check-scripts/check5.out`)", "(the reader's figures, `check-scripts/check5.out`; the +0.5° and the 1.4° above are the reader's too, `check2-S.out` and `check8.py`)"),
 # 8
 ("`check.md` (the reader's brief and report)", "`check.md` (my brief to the reader and its report), `check-2.md` (the same for the second reader)"),
 # 9
 ("the paper as I fetched it prints −5/93 and I have not seen what the correction changed.", "the PDF as I fetched it is marked \"corrected publication 2021\" and prints −5/93; I have not seen what the correction changed."),
 # 10
 ("An author correction to it exists, which I have not read.", "The PDF I fetched is marked \"corrected publication 2021\"; I have not read the correction notice."),
 # 11
 ("(the tables catch a slow swing of Jupiter and Saturn against each other, which long-run rates leave out)", "(for Jupiter and Saturn the two differ because the sky tables catch a slow swing of the pair against each other, which long-run rates leave out)"),
 # 12
 ("so it is an error of synodic phase like mine", "so it reads as an error of synodic phase like mine"),
 # 13
 ("Five were open (K11, K16a, K18, K19a, K19b); three of those held.", "By the reader's sorting, made after the scores, five were open (K11, K16a, K18, K19a, K19b); three of those held."),
 # 14 and 15 (the same sentence pair)
 ("(31.0° over the span, read from the Sun). The Moon's Metonic ratio is the exception: it fits the seasons better than the stars (121° against 262°).",
  "(31.0° over the span, read from the Sun); Mars loses least, 14° against 12° by the stars. The Moon's Metonic ratio is the exception: it fits the seasons better than the stars (121° against 262°), though the pointer is no nearer for it: 132° out today against 105°, since 262° behind is 98° ahead."),
 # 16
 ("(Turned by the Sun instead, the dial would stand 0.7 of a cell behind against the stars: 6 of 41 solar, no lunar; the reader's figures.)", "(Turned by the Sun instead, kept true to the stars, the dial would stand 0.7 of a cell behind and catch 6 of 41 solar, no lunar; the reader's figures.)"),
 # 17
 ("a glyph marks a cell whose month has an eclipse", "a glyph marks a cell whose month is predicted to have an eclipse"),
 # 18
 ("242 returns to the node", "242 returns of the Moon to its node (where its path crosses the Sun's)"),
 # 19
 ("on ten dates from 1977 to 2071", "on a dozen or so dates from 1977 to 2071 (ten in its Table 2)"),
 # 20
 ("to check the request) (`expectations.md`; hash on the board at 12:27 UTC)", "to check the request; `expectations.md`; hash on the board at 12:27 UTC)"),
 # 21
 ("are only a tenth to a fifth worse than", "are only 11% to 22% worse than"),
]
blocks = unwrap(open(src).read())
done = [0] * len(CH)
res = []
def rep(s):
    for i, (a, c) in enumerate(CH):
        n = s.count(a)
        if n: done[i] += n; s = s.replace(a, c)
    return s
for kind, b in blocks:
    res.append((kind, [rep(it) for it in b] if kind == 'list' else rep(b)))
bad = [CH[i][0][:50] for i, n in enumerate(done) if n != 1]
assert not bad, (bad, done)
open(out, 'w').write(rewrap(res))
print('applied', sum(done), 'changes')
