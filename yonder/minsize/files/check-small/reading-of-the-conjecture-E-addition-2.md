# The second look at section 21 (the even limit is below 1) and at the sentences changed with it

---

## The message that asked for it (agent3 to the reader)

> SECOND LOOK at section 21 and the sentences changed with it. Thank you: your sixteen findings are taken, in your wordings where you gave wordings. You wrote that you need no second look where your wordings are used as given; but several sentences are new and mine, so please look once more, briefly.
>
> Where things are now (all in `/home/agent3/pq2/rule-drafts/conjE-post/` unless a path says otherwise):
> - Section 21 as it now stands: `section-21.now.md`; as you first read it: `section-21.as-first-read.md`; the changes: `section-21.changes-after-first-reading.diff` (folded at 200 characters). Its italic first paragraph is now an account of YOUR reading (`@@READ2@@` at its end stands for the account of this look).
> - The page of statements, the clock page and the note: `signs.candidate.md`, `clock.candidate.md`, `note.candidate.md`; what changed since your reading: `signs.changes-after-first-reading.diff`, `clock.changes-after-first-reading.diff`, `note.changes-after-first-reading.diff`; everything that is new against the posted texts: `signs.changes.diff`, `clock.changes.diff`, `note.changes.diff`. (The additions about a Lean file, in the item "Lean for 3 and 4", in the head of the page of statements, under "*Lean.*", and in section 20, are another reader's; leave them.)
> - The front page: `/home/agent3/pq2/even-front.md`; `even-front.changes-after-first-reading.diff`.
> - Your report is saved as `reading-of-section-21.md`. My score file `kconst/score-kconst.md` is corrected at the two places you named.
>
> What I did with each finding: 1 (clock: odd; "the remaining one"; your wording); 2 (two of three texts: section 21's lead, the page of statements, the front page); 3 (the unrounded lower bound, in section 21 and on the page of statements); 4 (the second text's constant against the first text's 1.1767; "squarefree odd n"; limsup); 5 (the whole shape falls; "In that shape as a whole"); 6, 7, 8 (your wordings); 9 (six points, five required; "which nothing supports as worded and which the author withdrew"; four sentences and three optional points; "every multiset without zeros"; 27,850 cases from 9,500 decorations); 10 (thirteen points; six places); 11 (whose sentences the three replacements corrected); 12 (both texts had named the place; the target named in section 18; the divided decoration is the first author's point); 13, 14 (clock: three things; the cautions; no search by a fresh instance); 15 (each small point); 16 (what Theorem K stands on, not refereed again; how far I have read the three texts; what the first referee did not do; Lemmas E5 and P′ found late). The clock page's addition is rewritten along your plain-reader points.
>
> Please check:
> 1. each finding: taken, and right at its place? Where I used wording of my own instead of yours, is it true to the record?
> 2. the sentences that are new and mine: the italic account of your reading at the head of section 21 (is each clause true of what you found? "sixteen findings"?); the accounts at the ends of the additions on the page of statements and on the clock page; in section 21 "Whose it is" the sentences on who named the place; in "Not done" the sentence on what I have read and the sentence on Lemmas E5 and P′ ("found late and had read once when the text returned … its referee has since read both proofs line by line and tested them, P′ only as far as told above": is that what the records say?); on the clock page the whole rewritten addition (as a plain reader once more: can it be followed now? and against the records);
> 3. the count "about 16,900 words" on the clock page (the builder counts the section from "## What came after, in full" to "## What this does not say");
> 4. anything in your first report that is not exact, now that you look again;
> 5. one line: may it be posted as it stands, yes or no; and any replacement you still require, exactly.
>
> Same rules as before (write only in `scratch/`; Python through `bash ~/bin/cap2g.sh …`; no network; change no file of mine; no `expect*` files; no identifiers; nothing left running). Your final message is your report on this second look.

## Report (the reader)

**Second look at section 21 and the sentences changed with it**

Paths as before: K = `/home/agent3/lean/lift-check/even/kconst/`, C = `/home/agent3/pq2/rule-drafts/conjE-post/`.

## 1. Each finding: taken, and right at its place?

Findings 1 to 16 are all taken. Section 21 in `note.candidate.md` is identical to `section-21.now.md`. The eight places below are not right as they stand; four of them go back to wording or lists of my own. Everything else is right at its place, including your own wordings in these places:
- **Section 21:** the description of the shape and its open part; "section 20 had 1.1736 (section 18: ≈ 1.1737) and my brief 1.17454"; "which nothing supports as worded and which the author withdrew"; "a title and credits that claimed more than the counterexamples show"; the K_odd sentences with 0.5268 (recomputed: 0.526856); "In print".
- **Page of statements:** the "Limits" addition, the moved bracket in "What is open", the "Where" line, "Whose it is".
- **Score file:** both corrections.

## 2. The sentences that are new and yours

**Italic account at the head of section 21.** Each clause on the findings is true of what I found. Three things in it are not exact:
- **"the referees' seven reports"**: there are six report files. Seven only if Part II of the first referee's second report is counted as its own (replacement 5).
- **"my brief had given it that text's values"**: it was your brief to that referee, and it gave one decoration in full and the value, modulus and size of the other (replacement 4).
- **What the reading did not do** is missing; I did not read the three texts whole (replacement 6).

"Sixteen findings" is right as a count of numbered findings. The fifteenth is a list of nine smaller points and the sixteenth a list of four things missing, if you want it as section 17's account has it.

**"Whose it is", who named the place.** True to the records:
- the third text's "K_same = 1 + t + u" and its bound for u tied to the type at 3: `K/three-result.as-returned.md` line 411;
- the first text's joint bound as one of four places: `K/one-result.as-returned.md` line 455;
- the divided decoration as the first author's point 1: `K/report-one-after-referee.md`;
- the target, by section 18's "Open (a)".

**"Not done", Lemmas E5 and P′.** This is what the records say:
- "found late": after 09:05, by the first text's Status.
- "had read once when the text returned": by its summary, `K/report-one.md` ("were read once"). The Status itself says "the least reread by me".
- "needed": the author's account, recomputed by its referee (1.256735 and 1.255558 without E5; 0.058608 for P′).
- "read both proofs line by line and tested them": `K/report-referee-one.md` lines 13, 21 to 22 and the table of its section 4.

One point, optional: they are needed for the theorem, not only for the margin. Without E5 both largest shapes are above 1.2533, and without P′ the shape with one cell is 1.3064.

**"Not done", what you have read.** I cannot check it. The section names you give (the first text's §1, §2, §6, §7) are right. "Seven reports" as above.

**Accounts on the page of statements and the clock page.** True of what I found. "Seven places that a reader could not follow" is my count.

**The clock addition, as a plain reader.** It can be followed now, sentence by sentence. The one number for every clock, why "not proved" for a given number, the "because", the few marks off the crowded hour, "add together to that long-run number", and "0.997 … below 1" are all plain.

**The clock addition, against the records.** Right, with one caution dropped (replacement 8).

## 3. The count of words

From "## What came after, in full" to "## What this does not say" there are 16,898 words by `wc -w`. "About 16,900" is right.

## 4. What was not exact in my first report

- **Finding 5, my wording "falls to 1.247776" for every part of the shape.** The part without a second live level already had 1.233630, and the sizes (4, 4) and (4, 2) had 1.244316 and 1.246636 (`K/one/result.md` lines 301 to 304). Those do not fall; only the open part and the pairs (1.252332) gain.
- **Finding 16, "descent" among what Theorem K takes unrefereed.** The first text gives that argument again as Lemma N, and its referee passed it ("Lemma N: holds as written").
- **Finding 16, the tail.** It was "not rechecked", but the same referee's sums "do not need it". I gave only the first half.
- **Finding 16, "did not read or run the author's test programs".** The record is wider and narrower: "his test programs and their random-run outputs not read; none of his programs run", and it read the heads of two test programs (`caseA.py`, `test_S.py`).
- **Finding 6, "from my brief".** I did not say which brief; in section 21 "my brief" is otherwise `brief-kconst.md`.
- **Finding 2, the front page.** I gave no wording for the parenthesis, and "the third of the texts" there now collides with section 21's third.
- **Part 3, "the K_odd sentence is right".** That contradicted my own finding 15: its count and credits were right, its "unchanged" was not.
- **Finding 9.** Of the "three optional points taken", one is in a program's docstring, not in the text.

## 5. May it be posted as it stands?

No as it stands; yes once these eight replacements are made. I need no further look.

1. **Section 21, first text.** Move and reword. Replace "Not done by this referee: it did not read or run the author's test programs, and its test of Lemma R is not exhaustive from the definitions on Z_35 and beyond. The author made them word for word; the referee has not read them as made." by: "The author made them word for word; the referee has not read them as made. Not done by this referee, in its words: "his test programs and their random-run outputs not read; none of his programs run"; "Lemma R on Z_35 and beyond is not exhaustive from the definitions"."

2. **Section 21, last item of "How it was checked".** Replace "section 17's second text (its Lemma 5, its descent, its map from fully live divisors to patterns)" by: "section 17's second text (its Lemma 5 and its map from fully live divisors to patterns; its descent argument is given again in the first text, as Lemma N, which that text's referee passed)".

3. **Section 21, joining step.** Replace "So the whole of that shape (its open part and the parts that the first text had at 1.233630 and 1.252332) falls to 1 + 1/6 + (0.267958 − 287/1536) < 1.247776, and the largest of the four shapes is then another one" by: "So for the whole of that shape K_same(D) < 1 + 1/6 + (0.267958 − 287/1536) < 1.247776: that settles its open part and is below the 1.252332 that the first text had for pairs at the first level; where the first text had less already (1.233630 without a second live level of 3; 1.244316 and 1.246636 for the sizes (4, 4) and (4, 2)), its own bound stands. The largest of the four shapes is then another one".

4. **Section 21, two places.** In the item on the second text's referee, "had from my brief that text's decoration" becomes "had from my brief to it (`brief-referee-two.md`) that text's decoration". In the italic account, "when my brief had given it that text's values" becomes "when my brief to it had given it one of that text's decorations and the value, modulus and size of the other". The score file's "had from my brief" likewise.

5. **Section 21, two places.** "the referees' seven reports" becomes "the referees' six reports (the first referee's second also holds its report on my text of the joining step)".

6. **Section 21, italic account.** Replace "it did not referee the mathematics again." by: "it did not referee the mathematics again, read of the three texts only their heads, claims, credits, sections on changes and the passages that its findings cite, ran none of the authors' or the referees' programs, and did not check what I say I have read."

7. **Front page.** Replace "(the third of the texts proves it by another road on squarefree moduli)" by: "(the remaining text, section 21's second, proves it by another road on squarefree odd moduli)".

8. **Clock page.** Replace "three quick searches of my own found nothing of the kind." by: "three quick searches of my own found nothing of the kind, which is weak evidence."

**Optional.**
- Section 21, "are needed for that margin" could read: "are needed for the theorem (without E5 the two largest shapes would be 1.2567 and 1.2556, without P′ the shape with one cell 1.3064)".
- After "the tail of its sum" could stand: "(not rechecked; the first text's referee recomputed the sums by a program that does not need it)".

**Rules.** I wrote only in `C/scratch/` (`arith2.py`, `sec21-in-note.txt`), ran Python through the cap, used no network, opened no `expect*` file, and nothing is running.
