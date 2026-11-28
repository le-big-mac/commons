"""The clock page with a pointer, in its short section "What came after", to the one page of statements about signs
(28 November 2026): one sentence in square brackets after the bracket of the evening of 27 November, and one sentence in
"How this page was rebuilt".
usage: apply_signs_pointer.py < README.md > README.candidate-signs.md"""
import sys
s = sys.stdin.read()
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
rep('[Later that evening Lean accepted a proof for those clocks too; the full account tells that under "Added late in the evening".]',
    '[Later that evening Lean accepted a proof for those clocks too; the full account tells that under "Added late in the evening".] '
    '[In the night of 27 to 28 November it was proved on paper (not in Lean; no person has read the proofs) at least how many of the ways of choosing the pluses and minuses do that: on every clock, for three or more marks, at least a quarter of them, at least a half when the number of marks is odd, and for many marks nearly all (the share of the ways that fail is at most 3.12 divided by the square root of the number of marks: less than a third for 100 marks, about 3 in 100 for 10,000). '
    'The full account tells that under "Added on 28 November" and "Added later on 28 November". For mathematicians the statements about signs, with what is in Lean and what is not, are gathered on one page, `signs-where-it-stands.md` (here, and beside the second working note named below).]')
rep("and one more at the end of that paragraph, read at the last look.",
    "and one more at the end of that paragraph, read at the last look. After that an addition in square brackets, of three sentences, was made to the paragraph \"Added in the evening of 27 November\" of the short section \"What came after\", with a pointer to a page of statements for mathematicians; the instance that read that page against the note read the addition with it.")
sys.stdout.write(s)
