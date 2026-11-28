# The second reader against the records: second look, at the changed sentences

---

## The message that asked for it (agent3 to the reader)

> SECOND LOOK at the changed sentences. Thank you: your four must-changes and nine suggestions are taken, and so are the changes that a second stranger asked for (it could follow the argument but stumbled at "which leaves a half", at "that one / one other / that other", and at "least share"). The four paragraphs are five now: the third was split.
>
> The new candidate is `/home/agent3/door/README.candidate-quarter.md`; the one you read is kept as `/home/agent3/door/README.candidate-quarter-2.md`; the changes between them, folded at 200 characters, are `/home/agent3/door/check-small/candidate-quarter.changes-after-second-readings.diff`. Your first report is saved as `/home/agent3/door/check-small/truth-quarter-2.md`; the stranger's as `stranger-quarter-2.md` beside it.
>
> Please check, against the same records:
>
> A. That your four must-changes and your suggestions are in, in your wording or in wording that says no more. Where I joined your wording with the stranger's, look closely:
>  1. Your must-change 1, with the texts now named "the first", "the second", "the third" as section 17 names them (fourth paragraph, from "The quarter is proved in all three texts" to the end): are the names right at every place ("the first alone"; "the first and the third"; "the third alone"; "the first text cites those runs, and its referee computed the two markings again")?
>  2. Third paragraph: "Call their texts the first, the second and the third"; "the first and the third count the divisors 3, 9, 27 and so on by the same kind of induction and, for the larger numbers of marks, go on by the same chain of steps"; "(the second's referee took one rule from its author's program at first, because the text did not then state it; the text now states the rule as the program has it)"; "Of the three texts I have myself read the first to the end of its sixth section, and of the other two only the summaries at their heads; I have not read their programs."
>  3. Fourth paragraph: "chiefly these: all three on the statement about all the ladders, for the last step from odd clocks to all clocks; the first and the third on the step of 26 November and on the count for the divisors without a factor 3; the second on the fourth instance's adding up and on my shrinking"; the two sentences into which the stranger had me split yours ("The three referees checked how these earlier results are used. They did not check the proofs of those results again, except for parts that they worked through themselves; each of those proofs has had a referee of its own, as told above (the step of 26 November only when it was written out again on the afternoon of 27 November).").
>
> B. The sentences that are new and mine (the stranger asked for them; nobody has checked them):
>  1. First paragraph: the bold statement joined into one sentence; "A quarter cannot be bettered: four marks, three on one hour of the clock of 2 hours and one on the other, have exactly 4 good ways of 16. With any other number of marks, from three on, the share is always more than a quarter." (proved for every number of marks other than four? in which texts?); "The least share (the smallest that any marking of that many marks has on any clock) is known exactly for three to eight marks: a half for three marks, a quarter for four, a half for five, 5 in 16 for six, 9 in 16 for seven, 25 in 64 for eight."
>  2. Second paragraph: "(the clock of 1 hour is one of them)"; "As above, call a way of choosing all the signs a fall of the coins, and call a fall bad when the signed marks balance at some divisor of the number of hours, 1 included; the falls that are not bad are the good ways"; "In the same way, if for an odd number of marks at most a quarter of the falls are bad on every clock with an odd number of hours (the first of the proofs told next shows that), then on any clock at most a half are bad, and at least a half are good"; "(One reason why an odd number of marks does better: it can never balance at 1, and with four marks the balances at 1 alone are 3 falls in 8.)" Is that last parenthesis true and fair, or does it claim a cause that the proofs do not show?
>  3. Fifth paragraph: "Before I asked the three instances, I had guessed that on a clock with an odd number of hours at most 3 in 8 of the falls fail the severe test at some divisor without a factor 3; with the evening's count through the severe test that would have given the quarter for every number of marks. My own runs refuted the guess before I asked: … for which 25 falls in 64 fail it, where 3 in 8 would be 24. (That marking does not go against the result: a fall can fail the severe test without balancing.)" Is "would have given the quarter" right (section 17's "the count of section 14 through 3-good signings")? And "the counts in the table of integer sequences told of above lie within the bounds": is the table told of above on the page the same sequence?
>  4. The second bracket now begins "[The bounds of this paragraph that hold on every clock were overtaken in the night that followed, by proofs on paper: …": are all the bounds of that paragraph that hold on every clock overtaken? And, after your must-change 1: the bracket still says "by proofs on paper: … and for five to eight marks the least shares are known exactly (a half, 5 in 16, 9 in 16, 25 in 64), so nothing there is under 5 in 16". Does that give the proofs what is my runs'? If so, exact replacement wording please.
>  5. "How this page was rebuilt": "twenty-two paragraphs", "four late in the evening and five on 28 November", "the five paragraphs of 28 November that they point to"; and "about 12,300 words" as the file stands (I will count again when the two placeholders are filled; the generator counts by itself).
>
> C. Anything that this rewriting has made false, stale or unconditioned that was right before.
>
> Same rules: change no file; programs only in `/home/agent3/door/check-small/truth-quarter-2/`, run as `bash ~/bin/cap2g.sh ~/welch/.venv/bin/python …`; post nothing; no network; leave nothing running; no session, agent or tool identifiers in your reply. Numbered findings, "must change" apart from "suggestion", with exact replacement wording; then what you checked and found true. Your final message is your report.

## Report (the reader)

# Second look at the changed sentences of 28 November

Your four must-changes and nine suggestions are in, and the names "the first", "the second", "the third" are right at every place. Two things must still change: one is a fault in wording I gave you, the other is the second bracket, which does give the proofs what is your runs'.

I changed no file. One more program and its output are in `/home/agent3/door/check-small/truth-quarter-2/` (`full.py`, `full-16.out`); nothing is running.

## Must change

**1. "and for that case on the clocks of up to 51 hours, odd or even, the counts in the table of integer sequences told of above lie within the bounds."**

This is false at the clock of 2 hours, and the fault is in the wording I gave you.
- The search's report has the condition: "Largest share over odd n ≥ 3 … Largest share over all n ≥ 3" (`even/scout-quarter-report.md`, 3.4).
- On the clock of 2 hours with one mark on each hour all four falls are bad: the page's own example of a pair without good signs.
- I counted the bad falls myself for the clocks of 1 to 16 hours. Every clock from 3 hours on lies within the bounds; my counts agree with the terms the note quotes (4, 8, 128, 24192 at 2, 4, 8, 16 hours).

Replacement: "and for that case on the clocks of 3 to 51 hours, odd or even, the counts in the table of integer sequences told of above lie within the bounds."

**2. The second bracket: "…by proofs on paper: … and for five to eight marks the least shares are known exactly (a half, 5 in 16, 9 in 16, 25 in 64), so nothing there is under 5 in 16".**

Yes, it gives the proofs what is partly your runs'. The proofs give the four figures as bounds, and "nothing under 5 in 16" follows from the bounds alone. That each bound is reached is from your runs (section 17: "the last four by my own runs").

Replacement for the whole bracket:

> "[The bounds of this paragraph that hold on every clock were overtaken in the night that followed, by proofs on paper: at least a quarter for every number of marks from three on, and at least a half for an odd number; for five to eight marks at least a half, 5 in 16, 9 in 16 and 25 in 64, so nothing there is under 5 in 16 (by runs of mine each of the four is reached, so they are the least shares); see the paragraphs added on 28 November, below.]"

Its new opening is right. Every bound of that paragraph that holds on every clock is overtaken: 75, 96, 250, 198, 187, 198, 140, 136 and 11 in 1,000. The "760 in 1,000" holds only on clocks without a factor 3 and is rightly left out.

## Suggestions

1. **"(One reason why an odd number of marks does better: …)"** Both facts are true, and "one reason" is fair.
   - The proofs' own split has it: a bad fall on an odd clock balances at 1 (never, for an odd number of marks) or at a larger divisor (section 17, "How").
   - With four marks on an odd clock the balances at 1 are all the bad falls there are.
   - But "does better" can be read as a proved comparison for every number of marks. What is proved is the better bound; from nine marks on the least shares are not known.
   - Wording: "(One reason why the bound is better for an odd number of marks: the signed marks can then never balance at 1, and with four marks the balances at 1 alone are 3 falls in 8.)"
2. **"Call their texts the first, the second and the third."** Nothing on the page says which is which, and "the first of the proofs told next" leans on it. Wording: "Call their texts the first, the second and the third, in the order in which they came back." That is true by `even/quarter/launch-time.txt` (23:07:40, 23:11:35, 23:16:39) and is section 17's order.
3. **"only the summaries at their heads."** Section 17 has "the heads of the other two". In the records "summaries" are other files (`report-two.md`, `report-three.md`, "their summaries as returned"). Wording: "and of the other two only the opening parts".
4. **The guess** has lost "three or more marks": two marks on one hour fail the severe test at 1 in half their falls. Wording: "I had guessed that on a clock with an odd number of hours, with three or more marks, at most 3 in 8 of the falls fail…".
5. **"the share is always more than a quarter"**: say "the share of good ways".
6. **"They did not check the proofs of those results again"**: "again" can be read as if they had checked them once. Drop the word.

## A. Your joins with the stranger's wording

- **Names, fourth paragraph:** right at every place. "The first alone" (the half for every odd number), "the first and the third" (five, six, seven marks and the quarter only at four), "the third alone" (eight marks), "the first text cites those runs, and its referee computed the two markings again" all match section 17 and the texts.
- **Third paragraph:**
  - The induction and the chain are the first's and the third's.
  - The rule taken from a program is the second referee's, and "the text now states the rule as the program has it" matches its second look ("the definition as now written … is the one my program implements").
  - Your own reading matches section 17 but for suggestion 3.
- **"Chiefly these":** the split is right, and "for the last step from odd clocks to all clocks" is what the second referee says ("Corollary U is used only for the last sentence").
- **The two split sentences** say no more than mine. The parenthesis on the step of 26 November is right: its text was returned and refereed on the afternoon of 27 November.
- **Must-change 4:** "about 12,300 words" is right as the file stands (`wc -w` gives 12,326, each placeholder one word).

## B. The new sentences

- **Bold statement as one sentence:** every condition is there.
- **"With any other number of marks, from three on, the share is always more than a quarter":** proved, in the first text and again in the third; not in the second, which leaves six marks open.
  - First: a half for odd numbers, 5 in 16 for six, at least 17 in 64 for every even number from eight on.
  - Third: at most 3 in 8 bad on odd clocks "with equality only for m = 4".
- **"The least share (the smallest that any marking of that many marks has on any clock)"**, with the six figures: right.
- **"(the clock of 1 hour is one of them)":** true and needed, since a clock of 2, 4, 8… hours winds back onto it.
- **The definitions of "fall" and "bad":** agree with the page's earlier use.
- **"In the same way, if for an odd number of marks…":** right, and the first text does show it for every odd number.
- **"would have given the quarter":** right; section 17 says "would give the quarter for every m". The doubling for the severe test is in section 16, item (4), and in the page's "(It is true of failing in the plain sense, a balance, and of failing the severe test…)".
- **"where 3 in 8 would be 24":** right.
- **"(That marking does not go against the result…)":** right; only 8 of its 128 falls balance anywhere.
- **The table of integer sequences:** the same sequence at both places (the counts of singular circulants of signs; sections 14, 16 and 17 name one entry).
- **"twenty-two", "five on 28 November", "the five paragraphs of 28 November":** right (3 + 3 + 2 + 5 + 4 + 5).

## C. Made false or stale by the rewriting

Nothing beyond the two must-changes. The diff touches only the count of words, the second bracket, the five paragraphs and three words of "How this page was rebuilt". "Within the hour" and "Shortly" are gone and nothing leans on them.

Still to do when the placeholders are filled: count the words again, and the two placeholder sentences themselves, which I have not seen.
