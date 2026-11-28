"""The clock page after the shares of good signs were settled as "at least a quarter" (28 November 2026): five paragraphs
"Added on 28 November" in the full account, after the four added late in the evening of 27 November; two sentences in
square brackets at earlier sentences that they overtake; and the count of words of the full account.
usage: apply_quarter_plain.py TEXT-FILE READ-FILE PUBLIC-FILE < README.md > README.candidate-quarter.md
TEXT-FILE: the five paragraphs (ending with PUBLIC-HERE READ-HERE); READ-FILE: the sentences on how they were read;
PUBLIC-FILE: one sentence, with the time at which I looked, on whether section 17 is in the public copy of the note."""
import sys, re
s = sys.stdin.read(); text = open(sys.argv[1], encoding='utf-8').read().strip()
read = open(sys.argv[2], encoding='utf-8').read().strip(); public = open(sys.argv[3], encoding='utf-8').read().strip()
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
assert text.count('READ-HERE') == 1 and text.count('PUBLIC-HERE') == 1
text = text.replace('PUBLIC-HERE', public).replace('READ-HERE', read)
a = "\n**No hour marked twice, on a clock that is larger in the right way.**"
rep(a, "\n" + text + "\n" + a)
# brackets at two earlier places
rep("see the third of the paragraphs added late in the evening, below.]",
    "see the third of the paragraphs added late in the evening, below.] [And in the night that followed: at least a quarter for every number of marks from three on, and at least a half for an odd number of marks; see the paragraphs added on 28 November, below.]")
rep("nothing under 312 in 1,000 (5 in 16) turned up; that is a search and proves nothing.",
    "nothing under 312 in 1,000 (5 in 16) turned up; that is a search and proves nothing. [The bounds of this paragraph that hold on every clock were overtaken in the night that followed, by proofs on paper: at least a quarter for every number of marks from three on, and at least a half for an odd number; for five to eight marks at least a half, 5 in 16, 9 in 16 and 25 in 64, so nothing there is under 5 in 16 (by runs of mine each of the four is reached, so they are the least shares); see the paragraphs added on 28 November, below.]")
# the section on how the page was rebuilt
rep("and with seventeen paragraphs added on 27 November", "and with twenty-two paragraphs added on 27 and 28 November")
rep("four late in the evening, which say themselves who read them;", "four late in the evening and five on 28 November, which say themselves who read them;")
rep("and the count of words was changed again; the brackets were read with the four paragraphs they point to.",
    "and the count of words was changed again; the brackets were read with the four paragraphs they point to. On 28 November two more sentences in square brackets were added, one to the first of the five paragraphs and one to the third of the four, and the count of words changed once more; they were read with the five paragraphs of 28 November that they point to.")
i = s.index("## What came after, in full"); j = s.index("## What this does not say")
n = len(s[i:j].split()); r = int(round(n, -2))
m = re.search(r"it is long, about ([0-9,]+) words", s); assert m
s = s.replace(m.group(0), f"it is long, about {r:,} words")
sys.stdout.write(s)
