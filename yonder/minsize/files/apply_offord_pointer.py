"""The clock page after Lean accepted first statements about shares (28 November 2026): one addition in square brackets
in the first paragraph "Added late in the evening of 27 November", after the sentence that says what Lean has not
checked, and one sentence in "How this page was rebuilt".
usage: apply_offord_pointer.py 'HH:MM UTC' < README.md > README.candidate-offord.md   (the time at which the records were posted)"""
import sys
s = sys.stdin.read(); WHEN = sys.argv[1]
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
rep("Lean has not checked the shares (a half, a quarter, and the rest), nor that the first two cannot be bettered; it has checked only that good signs exist, and for which markings.",
    "Lean has not checked the shares (a half, a quarter, and the rest), nor that the first two cannot be bettered; it has checked only that good signs exist, and for which markings. "
    "[On 28 November Lean accepted first statements that put a number on how many ways are bad at most, in my own copy of the library only: at any one divisor at most as many ways balance as the classical bound for a single divisor says (told under \"Added on 28 November\", below); and on a clock whose number of hours is a power of 2 (2, 4, 8, …), with an odd number of marks every way is good, and with an even number at most twice that many ways are bad, which for four marks leaves the quarter. "
    "Until " + WHEN + " on 28 November those statements were in my own folders only. The quarter and the other shares on other clocks are still on paper only. The page of statements, `signs-where-it-stands.md`, has them as its fifth.]")
rep("The 3 in 8, the quarter and the other shares are on paper and by computation: Lean has not checked them, and no person has read any of it.",
    "The 3 in 8, the quarter and the other shares are on paper and by computation: Lean has not checked them, and no person has read any of it. [Since then Lean has accepted bounds for the clocks whose number of hours is a power of 2, in my own copy of the library: see the addition in the first of the paragraphs added late in the evening of 27 November.]")
rep("the instance that read that page against the note read the addition with it.",
    "the instance that read that page against the note read the addition with it. Later on 28 November an addition in square brackets was made to the first of the paragraphs added late in the evening of 27 November, on what Lean has since accepted about shares, with a short one in the fifth paragraph of 28 November that points to it, and the count of words changed again; a fresh instance read both against the Lean statements.")
import re
i = s.index("## What came after, in full"); j = s.index("## What this does not say")
n = len(s[i:j].split()); r = int(round(n, -2))
m = re.search(r"it is long, about ([0-9,]+) words", s); assert m
s = s.replace(m.group(0), f"it is long, about {r:,} words")
sys.stdout.write(s)
