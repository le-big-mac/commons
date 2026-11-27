"""The clock page after Lean accepted the answer for clocks with an even number of hours, and after the statement about
one ladder was found to hold for all the ladders at once (27 November 2026, late evening): four paragraphs "Added late
in the evening of 27 November" in the full account, after the five of the evening; four short brackets at earlier
sentences that they overtake; and the count of words of the full account.
usage: apply_late_plain.py TEXT-FILE READ-FILE < README.md > README.candidate-late.md
TEXT-FILE: the four paragraphs (ending with READ-HERE); READ-FILE: the sentences on how they were read."""
import sys, re
s = sys.stdin.read(); text = open(sys.argv[1], encoding='utf-8').read().strip(); read = open(sys.argv[2], encoding='utf-8').read().strip()
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
assert text.count('READ-HERE') == 1
text = text.replace('READ-HERE', read)
a = "\n**No hour marked twice, on a clock that is larger in the right way.**"
rep(a, "\n" + text + "\n" + a)
# brackets at four earlier sentences
rep("for clocks with an even number of hours the answer is proved on paper only, and no person has read it. The full account tells it under the same date.",
    "for clocks with an even number of hours the answer is proved on paper only, and no person has read it. The full account tells it under the same date. [Later that evening Lean accepted a proof for those clocks too; the full account tells that under \"Added late in the evening\".]")
rep("and with five or more, more than 75 in 1,000. The first two cannot be bettered; the third is only what the proof gives.",
    "and with five or more, more than 75 in 1,000. The first two cannot be bettered; the third is only what the proof gives. [More was proved on paper later that evening: at least a quarter with five marks, and more than 96 in 1,000 with any number from five on; see the third of the paragraphs added late in the evening, below.]")
rep("and a table of integer sequences has it exactly for clocks of twice an odd prime number of hours. **No person has read any of this, and for clocks with an even number of hours none of it has been checked by Lean.**",
    "and a table of integer sequences has it exactly for clocks of twice an odd prime number of hours. [The same preprint has more than this says: see the last of the paragraphs added late in the evening.] **No person has read any of this, and for clocks with an even number of hours none of it has been checked by Lean.** [Since then Lean has accepted the result itself, without the shares: see the next paragraph.]")
# the section on how the page was rebuilt
rep("and with thirteen paragraphs added on 27 November to \"What came after, in full\", each group marked there with the word \"Added\" (three on markings of at most 36 marks, three on every marking, two on the Lean proof, five on clocks with an even number of hours;",
    "and with seventeen paragraphs added on 27 November to \"What came after, in full\", each group marked there with the word \"Added\" (three on markings of at most 36 marks, three on every marking, two on the Lean proof, five on clocks with an even number of hours, four late in the evening, which say themselves who read them;")
rep("Since then one paragraph has been added to \"What came after\" (in the evening of 27 November) and the count of words in its first paragraph changed; who read them is told with the five paragraphs they point to.",
    "Since then one paragraph has been added to \"What came after\" (in the evening of 27 November) and the count of words in its first paragraph changed; who read them is told with the five paragraphs they point to. Later that evening a sentence in square brackets was added to that paragraph, and three more to the five paragraphs, and the count of words was changed again; the brackets were read with the four paragraphs they point to.")
# the count of words of the full account
i = s.index("## What came after, in full"); j = s.index("## What this does not say")
n = len(s[i:j].split()); r = int(round(n, -2))
m = re.search(r"it is long, about ([0-9,]+) words", s); assert m
s = s.replace(m.group(0), f"it is long, about {r:,} words")
sys.stdout.write(s)
