"""The clock page after the question about signs was answered for every clock, with its one kind of exception
(27 November 2026, evening): five paragraphs "Added in the evening of 27 November" in the full account, after the two
paragraphs on Lean; one short paragraph under "What came after"; and the count of words of the full account.
usage: apply_even_plain.py TEXT-FILE READ-FILE < README.md > README.candidate-even.md
TEXT-FILE: the five paragraphs (ending with READ-HERE); READ-FILE: the sentences on how they were read."""
import sys, re
s = sys.stdin.read(); text = open(sys.argv[1], encoding='utf-8').read().strip(); read = open(sys.argv[2], encoding='utf-8').read().strip()
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
assert text.count('READ-HERE') == 1
text = text.replace('READ-HERE', read)
a = "\n**No hour marked twice, on a clock that is larger in the right way.**"
rep(a, "\n" + text + "\n" + a)
a = "Not known: a rule for the patterns on clocks such as 36 and 100 that neither of the first two results covers.\n"
rep(a, a + "\n*Added in the evening of 27 November.* A question that came up on the way to the first of the three has since been answered for every clock: can the marks be given pluses and minuses so that, with their signs, they balance nowhere? For every marking with at least one mark they can, with exactly one kind of exception: certain pairs of marks on clocks with an even number of hours. For clocks with an odd number of hours, where there is no exception, Lean has accepted a proof; for clocks with an even number of hours the answer is proved on paper only, and no person has read it. The full account tells it under the same date.\n")
# the section on how the page was rebuilt: two sentences that the additions of 27 November had made stale
rep("a fresh instance read them four times against the records, the last time as they stand but for one sentence that it changed.",
    "a fresh instance read them four times against the records, the last time as they stand but for one sentence that it changed. Since then one paragraph has been added to \"What came after\" (in the evening of 27 November) and the count of words in its first paragraph changed; who read them is told with the five paragraphs they point to.")
rep("and with three paragraphs added later on 27 November to \"What came after, in full\", the first of them marked there (on markings of at most 36 marks: the instance",
    "and with thirteen paragraphs added on 27 November to \"What came after, in full\", each group marked there with the word \"Added\" (three on markings of at most 36 marks, three on every marking, two on the Lean proof, five on clocks with an even number of hours; of the first three: the instance")
# the count of words of the full account
i = s.index("## What came after, in full"); j = s.index("## What this does not say")
n = len(s[i:j].split()); r = int(round(n, -2))
m = re.search(r"it is long, about ([0-9,]+) words", s); assert m
s = s.replace(m.group(0), f"it is long, about {r:,} words")
sys.stdout.write(s)
