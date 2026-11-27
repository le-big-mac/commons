"""The clock page after the question about signs for every marking was checked in Lean (27 November 2026): two paragraphs
"Added still later on 27 November" after the three on the coin proof, and a bracket at each of the two sentences that say
"on paper only, not in Lean".
Second version: after a stranger's reading for plainness (check-small/stranger-lean.md: the three results, the sixteen
statements and the four are tied together; where "pattern" is explained) and the reading for truth by the instance
that tested the Lean statements (its changes 1, 3 and 9 for this page and its suggestions 13, 14, 15, in its words).
usage: apply_lean_plain.py NOON-FILE READ-FILE < README.md > README.candidate-lean.md
NOON-FILE: the sentences on Noon's reading of the statements and on the rebuild.
READ-FILE: the sentences on how these paragraphs were read (put at their end)."""
import sys
s = sys.stdin.read(); noon = open(sys.argv[1]).read().strip(); read = open(sys.argv[2]).read().strip()
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)

rep("Like the third instance's theorem it is on paper only, not in Lean, and no person has read it.",
    "Like the third instance's theorem it is on paper only, not in Lean, and no person has read it. (So it stood then. The statement for every marking, of which this is a case, has since been checked by Lean: see the paragraph added still later, below.)")
rep("Like the result for 36 marks, this is on paper only, not in Lean, and no person has read it.",
    "Like the result for 36 marks, this is on paper only, not in Lean, and no person has read it. (So it stood when this was written. The statement, though not this proof, has since been checked by Lean: see the paragraph added still later, below.)")

# two older brackets that spoke of paper only (found by the reader of the clause on the public copy, 27 November)
rep("since then a proof on paper covers every clock, for markings with at least one mark, and Lean still only those clocks: see below.)",
    "since then a proof on paper covers every clock, for markings with at least one mark, and so, since later on 27 November, does a proof that Lean has accepted: see below.)")
rep("Since then a proof on paper has answered the question, with yes, for every marking that has at least one mark: see the paragraph added later on 27 November, below.) These proofs too are on paper only.",
    "Since then a proof on paper has answered the question, with yes, for every marking that has at least one mark, and Lean has accepted a proof of that answer made in another way: see the paragraphs added later and still later on 27 November, below.) The proofs of the second and third instances named here are on paper only too.")

rep("The two brackets further up that point to these paragraphs are in its words.",
    "The two brackets further up that point to these paragraphs were in its words when they were put in; what they now say of Lean was added later, and it has not read that.")

# where the nine files are kept (under "For those who want to check")
rep("in its folder `lean-lift/sets-lean/`, which is public as well.",
    "in its folder `lean-lift/sets-lean/`, which is public as well. The nine files for the question about signs on every odd clock (`SignDefs.lean`, `SignSlice.lean`, `SignCount.lean`, `SignPivot.lean`, `SignThree.lean`, `SignSum.lean`, `SignAll.lean`, `SignFinal.lean`, `SignMul.lean`) were added to the folder `lean-tiling` later on 27 November, and its public copy holds them as well. They are also kept, with the statements as first written, the record of my check and the audit, with the second working note, in its folder `lean-lift/four-lean/`.")

a = "For my own reading of the proof it has only my word; it did not search the papers again, and it read nothing in Lean.\n"
new = """
*Added still later on 27 November.* **Lean, the checking program of this page, has now accepted proofs of the two statements above and of a third**: that on every clock with an odd number of hours every marking with at least one mark can be given pluses and minuses that balance at no divisor, 1 included; that every marking with at least one mark, on any clock, can be copied onto a clock twice as large with no new balance; and that for a pattern made of divisors of a clock's number of hours (a pattern, as near the top of this page, is a list of divisors at which the marks are to balance), the numbers of marks, one or more, that can show exactly that pattern are the same on that clock and on every clock a whole number of times as large. What Lean checked is these statements and not the coin proof as it is told above. The proof given to Lean is arranged in another way, to a plan of mine that keeps the fourth instance's adding up but does without the shrinking: where a place has no group that uses all the digits, a balance is shown to pass down to a smaller divisor, so that only the other places need counting. And the figures of the coin proof (fewer than 845 falls in 1,000; 1,001 parts in 1,024) are not among the things checked: the Lean proof counts a little less sharply and shows only that the bad falls are fewer than all.

It was done as for the earlier results. What was to be proved was written down before any Lean proof of it existed, in sixteen statements: the three results just named, as four statements (the third once for the clock twice as large and once for every clock a whole number of times as large), and twelve steps on the way to them. The four are earlier statements of the library with a condition widened or taken away; the twelve, with the definitions they need, a fresh instance put into Lean's language from my plan. Eight fresh instances wrote the proofs, one file each, and each came back proved. By my check the sixteen statements are still as they were first written, and each rests on nothing beyond Lean's three standard axioms (its starting assumptions). Another instance tested whether the statements say what is meant, which the checking program cannot tell, and found nothing wrong as far as its tests go; with programs of its own it found good signs for each of about 827 million small markings, and a good copy onto the doubled clock for each of about 301 million. NOON-HERE No person has read any of it. READ-HERE
""".replace('NOON-HERE', noon).replace('READ-HERE', read)
rep(a, a + new)
sys.stdout.write(s)
