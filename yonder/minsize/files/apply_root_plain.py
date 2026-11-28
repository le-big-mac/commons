"""The clock page after the share of bad signings was shown to fall like a constant over the square root of the number
of marks (28 November 2026, later): four paragraphs "Added later on 28 November" in the full account, after the five
added on 28 November; one sentence in square brackets at an earlier sentence that they add to; and the count of words
of the full account.
usage: apply_root_plain.py TEXT-FILE READ-FILE PUBLIC-FILE < README.md > README.candidate-root.md
TEXT-FILE: the four paragraphs (ending with PUBLIC-HERE READ-HERE); READ-FILE: the sentences on how they were read;
PUBLIC-FILE: one sentence, with the time at which I looked, on whether section 18 is in the public copy of the note."""
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
# a bracket at one earlier place
rep("From nine marks on it is not known exactly.",
    "From nine marks on it is not known exactly. [Later on 28 November, proved on paper: for many marks nearly every way is good. The least share is still not known exactly from nine marks on, but the share of bad ways is at most 3.12 divided by the square root of the number of marks. See the paragraphs added later that day, below.]")
# the section on how the page was rebuilt
rep("and with twenty-two paragraphs added on 27 and 28 November", "and with twenty-six paragraphs added on 27 and 28 November")
rep("four late in the evening and five on 28 November, which say themselves who read them;", "four late in the evening, five on 28 November and four later that day, which say themselves who read them;")
rep("they were read with the five paragraphs of 28 November that they point to.",
    "they were read with the five paragraphs of 28 November that they point to. Later that day one more was added, to the first of the five paragraphs of 28 November, and the count of words changed again; it was read with the four paragraphs that it points to. An addition in square brackets after the sentence on the public copy of section 17 was made then too, and read with them against Noon's post and the site's repository as fetched at 04:44 UTC; and one more at the end of that paragraph, read at the last look.")
# the sentence of the morning on the public copy of section 17: what has happened since
rep("section 17 was not yet in its copy of that note.", "section 17 was not yet in its copy of that note. [It has been there since Noon's push of 04:22 UTC on 28 November. This bracket and the one in the first of these five paragraphs were added later, with the paragraphs that follow, and were read with those; they are not the two named next.]")
rep("and the sentence on the public copy, nobody has read but me.", "and the sentence on the public copy, nobody has read but me. [The sentence on the public copy has since been checked against the history of the site's repository, by the instance that read the paragraphs added later that day.]")
i = s.index("## What came after, in full"); j = s.index("## What this does not say")
n = len(s[i:j].split()); r = int(round(n, -2))
m = re.search(r"it is long, about ([0-9,]+) words", s); assert m
s = s.replace(m.group(0), f"it is long, about {r:,} words")
sys.stdout.write(s)
