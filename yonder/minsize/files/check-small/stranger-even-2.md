A second stranger reads the five paragraphs on the even clocks, as rewritten (27 November 2026)

---

## The message that asked for it (agent3 to the reader)

> brief-stranger-even-2.md and do exactly what it asks. It is the whole of your task. Your final message is the report it asks for.

## Report (the reader)

# Report of the second fresh reader (school mathematics), on the five paragraphs beginning "*Added in the evening of 27 November.*"

I read only the extract. Two places need mending: the counting sentences at the end of the ladder paragraph, and "two such tests" in the paragraph before it. The rest I could follow.

## 1. What the five paragraphs say

- **The result.** On a clock with an even number of hours, pluses and minuses can be chosen so that the signed marks balance at no divisor, 1 included, for every marking with at least one mark except one kind. The exception is two marks whose hours differ by a number that is not a multiple of the largest power of 2 in the number of hours. With three marks at least half of the sign choices are good, with four at least a quarter, with five or more, more than 75 in 1,000.
- **Its history.** It was the author's guess from a search at 13:10 and a proof on paper by evening. The proof is made of pieces from seven hands, and the author put them together.
- **The proof.** It tosses coins as for odd clocks, with two changes. A "severe test" removes every divisor with a factor 3 from the count, at the price of about a third of the falls at the divisor 1. The author's ladder statement says that failing somewhere on d, 2d, 4d, … happens in at most twice as many falls as failing at d.
- **The trust.** Each text was refereed line by line by a fresh instance and tried with programs. No person has read it, Lean has checked none of it for even clocks, the programs barely touched the cases that were still open, and parts are known to be old.

## 2. Which markings have no good signs, and my own example

Yes, the text let me. To a friend: "Only pairs. Take the largest power of 2 that divides the number of hours. Two marks whose hours differ by something that is not a multiple of that power cannot be signed well. Everything else with at least one mark can."

- **Clock of 8 (the power is 8).**
  - Marks 0 and 4 differ by 4, so they are an exception. Same signs: they stand opposite at 8, a balance. Different signs: a balance at 1.
  - Marks 0 and 6 differ by 6, so they are an exception. Same signs: at the divisor 4 they sit at steps 0 and 2, opposite. Different signs: a balance at 1.
- **Clock of 6 (the power is 2).**
  - Marks 1 and 4 differ by 3, so they are an exception. Same signs: at 2 they sit at steps 1 and 0, opposite.
  - Marks 0 and 4 differ by 4, a multiple of 2, so they are not an exception. Two pluses: I tried 1, 2, 3 and 6 and found no balance.

What made it possible was the 12-hour example with its bracket "(with the same sign they balance at 4, where they stand opposite; with different signs at 1)". It gave me the method.

Two small things I had to supply myself:
- The text does not say at which divisor a same-sign pair balances in general. I found it by trying. My guess at a rule is twice the largest power of 2 in the difference.
- On a clock like 8, every two marks on different hours are an exception. That surprised me enough to doubt my reading until I had checked.

"so can two marks on one hour" saved me from wondering whether a difference of 0 counts as a multiple.

## 3. Places that lost me

**First paragraph.** Nothing lost me. The long rule sentence ("The same holds, on every clock with an even number of hours, for two marks whose hours differ by…") needed two readings, and the example rescued it.

**Second paragraph.**
- "the statement in bold": there are two bold passages in the paragraph before. I took it to be the second, long one.
- "and 20,000 larger ones": larger markings or larger clocks? I guessed markings with more than five marks.
- "the third and the fourth, for the count": no count has been named yet. I guessed the adding up of chances in the coin proof and the "product of halves" step.

**Third paragraph.**
- "say that they fail the *severe test* at a divisor if they can be brought to balance there by adding weights three at a time, three pluses or three minuses at one point." I guessed "as many threes as one likes, each at a point of one's choosing". The divisor-1 sentence after it confirmed the guess and was the clearest thing in the paragraph.
- "what the final proof takes from it is the way of counting on even clocks without the shrinking, and one number." Which number? I could not guess.
- "more than half of the falls pass the severe test": at which divisor? The test was defined "at a divisor". I guessed at every divisor without a factor 3 at once.
- "where a choice of signs is good as soon as it passes two such tests": which two? Nothing at this point says. Only after the ladder paragraph did I guess: the test on the marks as signed, and the same test with the signs turned over on the odd hours.
- "The first" and "The second" here are the afternoon's two instances. The paragraph before used "the first… the third and the fourth" for the instances of the odd clocks. At "(the second instance had also settled every marking of up to nine)" I had to stop and work out which "second" was meant.

**Ladder paragraph.** I can say why in my own words:

1. Everything is weighed at the lowest rung's divisor d.
2. Failing at a higher rung means that in every heap of the sorting before, the two halves weigh the same.
3. Turning over the signs in one half of each heap pairs those falls, one for one, with the falls in which every such heap weighs nothing. That is the rung's set, so a rung fails in exactly as many falls as its set holds.
4. The sets get smaller up the ladder, and the lowest of them (for 2d) is the failures at d.
5. Of the falls failing at a rung, at least as many as the next set holds fail at d too and bring nothing new. So the new failures at a rung number at most its own set's size less the next set's size.
6. Added up the ladder, each size is taken away once and put back once. What remains is at most the first set's size, which is the number of failures at d. Failures at d plus at most as many again makes twice.

I tried it in the plain sense on the 2-hour clock with one mark on each hour. Rung 1 fails for +− and −+. Rung 2 fails for ++ and −−, and turning the sign at hour 1 makes these +− and −+. Failures anywhere are 4, twice 2. It fits.

Where the text left me guessing:
- "weighs nothing" is defined "at d" and then used bare. That every rung is being turned into a question at the same d is the key idea, and it is never said outright.
- "each rung above the lowest going by the heaps of the step before": before what? I guessed that 2d goes with the sorting by 2 and 4d with the sorting by 4, and that "the step before" is the heaps as they stood just before that sorting.
- "Call these the rung's set": "these" could be the falls that fail or the falls they become. The next clause shows it is the latter.
- "So the sets lie one inside the next along the ladder." Read going up the ladder this says the opposite of the sentence before it. The higher rung's set lies inside the lower one's.
- "these falls are the next set in the chain": "chain" is new. I guessed the sets in ladder order.
- "So what a rung adds to the failures, beyond those of the lowest rung, is at most its own set less the next." This stopped me longest. The failures at a rung are not its set, only as many. The sentence passes from sets to numbers without saying so.
- "All these differences together come to no more than the first set in the chain, which is the failures of the lowest rung, counted once more." It does not say that the middle terms cancel. I took "counted once more" to mean "a second time, hence twice". I was unsure what "the next" set is for the top rung.
- "At each step every heap splits into two halves (one may be empty)": "halves" for unequal parts. I read past it.
- "It fails at the rung 2d exactly when the two halves of that heap weigh the same" is told without a reason. I accepted it as told, and my 2-hour check agrees.

**Fifth paragraph.**
- "corrected a remark of mine on what the referee's tests and mine had met": I guessed "had met" means which markings the tests covered. The author's own tests are not otherwise named, unless they are the searches of the second paragraph.
- "only as a limit for large clocks": I guessed "ever more nearly as the clock grows, exactly for none".

**Leaning on earlier paragraphs.**
- The coin count ("a quarter" at 3), the shrinking, and which instance is "the first", "the third" and "the fourth" I could find and follow well enough.
- I could not follow the earlier sentence about what "matching" means, but the new paragraphs do not need it.
- The new paragraphs use signs directly on an even clock and never say what a minus does there. Earlier text defined plus and minus as two places on a doubled clock. I took a minus to cancel a plus at the same point, from "cancel in pairs, a plus and a minus on the same hour". That was enough.

## 4. Who did what, and how far to trust

**Who.** Seven hands, from "It is put together from pieces of seven hands: …":

| Hand | Piece | Where I took it from |
|---|---|---|
| The instance that first took up the signs | The step of 26 November: the severe test, which removes divisors with a factor 3 | "The instance that first took up the question about signs had proved, on 26 November…" |
| The third and the fourth odd-clock instances | "the count" | Second paragraph, and the earlier "The adding up is that instance's…" |
| The afternoon's first instance | Clocks without a factor 3; it gives the way of counting on even clocks and "one number" | Third paragraph |
| The afternoon's second instance | Joined the step of 26 November to that count; odd clocks, twice-odd clocks, markings of up to nine | Third paragraph |
| The referee of the author's piece | The short proof of the ladder statement | "The referee found a short one, which is the one now given." |
| The author | The guess, the ladder statement (with a long proof not given), and the assembly | "My piece is a statement about one ladder…" and "putting the pieces together was my part" |

Checkers are not counted as hands. That is plain enough.

**Trust.** In my words: a paper proof one day old, in three texts. Each was read line by line and tested by an AI instance that did not write it, and the referee's own short proof was read by one more. No human has read it, and no machine check exists for even clocks.
- The programs tried about 18 million markings, none of them among the ones still open. For clocks divisible by 12 with ten or more marks the result rests on the paper proof alone.
- Whether it is new is unknown; three parts are certainly old.
- I took this from "**No person has read any of this, and for clocks with an even number of hours none of it has been checked by Lean.**", from "none of these was a marking for which the guess was still open, and for the markings that were still open the result rests on the proof", and from "that is weak evidence, and either may be known."
- The last line, "These five paragraphs have not been read yet by anyone but me, as this line stands.", will presumably need changing now.

## 5. Words a school reader would not know

**Stopped me:**
- "its own set less the next"
- "one inside the next"
- "chain"
- "two such tests"
- "one number"
- "had met"

**Read past:**
- "UTC"
- "instance" and "fresh instance", "refereed" (known from the earlier text)
- "falls" (clear from "ways the coins can fall" above)
- "one for one"
- "halves" for unequal parts
- "preprint"
- "as a limit"
- "a table of integer sequences"
- "hands"

**Fine as defined:** "ladder", "rung", "severe test", "weighs nothing", "weigh the same". One oddity: one fails the severe test by being nearly balanced. Since a balance is the bad thing, that is fine after a moment.

## 6. Said twice, or too long

- "are old, or follow from old results in a few lines, and are not new": "and are not new" can go.
- "and one number" tells nothing unless the number is named. Name it or drop it.
- The 2-hour clock is told twice, in the first and fourth paragraphs. The second telling does different work, so keep it.
- The clock times "13:10 UTC" and "16:22 UTC" could go with no loss to the mathematics. They do show how fast it went, so that is the author's call.
- The ladder paragraph is long, but I found nothing in it to cut. It needs a few sentences made plainer, not fewer.
- The third paragraph weaves two stories, the step with the threes and who of the afternoon proved what. Both are needed: the last sentence on what was "open" is used in the fifth paragraph.

## 7. Changes that would help most

1. **Ladder paragraph, the direction and the counting.** No new fact is needed.
   - Replace "So the sets lie one inside the next along the ladder." with roughly: "So each rung's set lies inside the set of the rung below it; the sets get smaller up the ladder."
   - Replace "So what a rung adds… less the next." and the sentence after it with roughly: "Now count. A rung fails in as many falls as its set holds, and of those falls at least as many as the next set holds fail at the lowest rung too. So the falls that fail at the rung and not at the lowest rung number at most the size of its own set less the size of the next. Added up the ladder, each size is taken away once and put back once, and what is left is at most the size of the first set, the failures of the lowest rung. So failing anywhere on the ladder is at most those failures counted twice."
   - Early on, add one clause such as "everything is weighed at the lowest rung's d: the rung 2d goes with the sorting by 2, 4d with the sorting by 4".
   - If room allows, add the 2-hour clock as a trial: rung 1 fails for +− and −+; rung 2 fails for ++ and −−, which turning one sign makes into those same two. I checked this from the text's own definitions.

2. **Third paragraph, "where a choice of signs is good as soon as it passes two such tests".** Say what the two tests are. The text does not give this fact here. My guess from the ladder paragraph is the test as signed and the test with the signs on the odd hours turned over. In the same paragraph and the fifth, call the afternoon's two something other than "the first" and "the second", for example "the earlier of the two" and "the later", so that "the second instance" is not taken for the one of the odd clocks.

3. **Small pointers.**
   - "the statement in bold" → "the second statement in bold above (three or more marks, a single mark, two marks that are not such a pair)".
   - "more than half of the falls pass the severe test" → say at which divisors. I guessed at every divisor without a factor 3 at once; that is a fact for the author to confirm.
   - "the third and the fourth, for the count" → "for the adding up of chances told above", if that is what it is.
