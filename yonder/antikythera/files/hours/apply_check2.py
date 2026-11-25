"""Apply the second reader's changes (check-2-scripts/changes2.json) to README.md in the reader's words, then the few things of
my own that follow from their report. The version the second reader saw is README-as-reread.md.
usage: apply_check2.py   (under -I)"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, 'README.md'); t = open(p, encoding='utf-8').read()
def rep(old, new):
    global t
    assert t.count(old) == 1, (old[:60], t.count(old)); t = t.replace(old, new)
n = 0
for c in json.load(open(os.path.join(HERE, 'check-2-scripts', 'changes2.json'), encoding='utf-8')):
    if c['id'] == 'header-before-pasting': continue     # the reader left this to me: the order was as the note says (see below)
    rep(c['old'], c['new']); n += 1
print('second reader:', n, 'changes pasted')

# mine, after the second reading (read by nobody)
rep("Before pasting them I checked their quotations",
    "Before pasting them (the file of `after_check.py` is later than the pasting only because I added the 178 BC date to it afterwards) I checked their quotations")
rep("That is six searches and not a survey; a paper I did not find may well have it.",
    "The search for the 767 months found nothing on them; the search for a fitted longitude found only Carman and Evans's; and the later paper "
    "of Voulgaris and others (2024) came up in the last of the six. That is six searches and not a survey; a paper I did not find may well have it.")
rep("Then I made the\nsearches neither of us had made and added what is marked \"added after the reading\" below.*" if "Then I made the\nsearches" in t else
    "Then I made the searches neither of us had made and added what is marked \"added after the reading\" below.*",
    "Then I made the searches neither of us had made and added what is marked \"added after the reading\" below.*\n\n"
    "*A second reader, a fresh instance without the network, read only what was added after the first reading (the end of this paragraph, the three points marked \"added after the reading\", the entry for Voulgaris and others under Sources, the end of Files and the figure's footnote) and went once through the header and \"In short\" for consistency: they reran `after_check.py` and `hours_after.py` and got the kept outputs, recomputed the four starts about December 178 BC from JPL's tables and the catalogue's ΔT with code of their own (the same scores to 0.01 h), tried the starts one and two Saros and Metonic cycles later, read both papers of Voulgaris, Mouratidis and Vossinakis through, checked the four slips against the sealed files and redrew the figure (the same picture); they found the figures right, the headline on the 178 BC date stronger than the test, and \"recomputed their other new figures\" true of some of those figures only; they did not check that the searches were made or what they found, did not read the third paper to which Voulgaris and others refer for the hours, could not check the arXiv number of their first paper, and did not go again over what the first reader had checked; their scripts and the changes they asked for are in `check-2-scripts/`. "
    "(That sentence is the second reader's; their report is `check-2.md`, and the text they read is `README-as-reread.md`.) Thirteen of their fourteen changes are in, in their words (`apply_check2.py`); the fourteenth they left to me, and I kept my three words and say why. "
    "The figure's footnote now has the wording they proposed. Read by nobody: the clause about the file of `after_check.py`, one sentence on what three of the searches found, and this last paragraph from \"Thirteen\" on.*")
rep("`apply_after.py` (my own additions to the text, all but the entry for Voulgaris and others under Sources, which that script does not hold).",
    "`apply_after.py` (my own additions to the text, all but the entry for Voulgaris and others under Sources, which that script does not hold). "
    "The second reader: `check-2.md`, `check-2-scripts/`, `apply_check2.py`; the text they read is `README-as-reread.md`.")
open(p, 'w', encoding='utf-8').write(t)
print('done;', len(t.split()), 'words')
