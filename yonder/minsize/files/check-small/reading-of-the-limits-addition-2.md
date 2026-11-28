# The second look at section 20 (the limits exist) and at the sentences changed with it

---

## The message that asked for it (agent3 to the reader)

> SECOND LOOK at section 20 and the sentences changed with it. Thank you: your twelve findings and the smaller points are taken, in your wordings where you gave wordings.
>
> Where things are now (all in `/home/agent3/pq2/rule-drafts/limits-post/` unless a path says otherwise):
> - Section 20 as it now stands: `section-20.now.md`; as you first read it: `section-20.as-first-read.md`; the changes: `section-20.changes-after-first-reading.diff` (folded at 200 characters). Its italic first paragraph is now an account of YOUR reading (it says "twice": true once this look is done; your reports will be posted in `lean-lift/even/limit/readings/`).
> - The page of statements and the clock page: `signs.candidate.md`, `clock.candidate.md`; ALL the sentences about the limits as they now stand are the lines marked `>` in `signs.changes-B.diff` and `clock.changes-B.diff` (the same files as you first read them: `signs.changes-B.as-first-read.diff`, `clock.changes-B.as-first-read.diff`). Both end with an account of your reading.
> - The front page: `/home/agent3/pq2/even-front.md`; changes since your reading: `even-front.changes-after-first-reading.diff`.
> - The final text `limits.md` in `/home/agent3/lean/lift-check/even/limit/` is CHANGED after your report, as you suggested: its account of the second look (now in your wording), its Status line ("in two looks"), and in §5 the kinds of my own count, how the display "from below" is computed and the decoration with K = 0; a dated paragraph at its end says so; the text as it stood is `limits.after-the-second-look-replacements.md`, the changes `limits.changes-after-the-reading-of-section-20.diff`; `limits.final.sha256` has both hashes; `limits.as-sent.sha256` now names the right file. New there: `count_cases_by_kind.py`, `.out` (my recount: 1,274,130 and 3,978,788, as you had).
>
> What I did with each finding: F1, F2, F4, F5 (both pages), F6, F7, F8, F9, F11, F12 in your wording. F3: your wording, with one addition of mine at its end: "the account of the second look in the text's §6 is mine (as I first wrote it, it said "nothing else changed"; the reader of this section found that, and it is corrected in the reader's wording); the referee has read none of this again." F10: your wording on the clock page; in section 20 "two about numbers". Smaller points: Theorem L and the Addendum in the block quote are now copied from `limits.md` by program, with "(§4 of the text)" for "(§4)"; "Whose it is" now names Lemma F and the tail bound from section 12's text, and gives the bound for one value to Erdős; "How" gives Lemma 3 its order (for every N₀ and δ there is t …); the open item says "what the constants are"; the row names the search file and the new files. The clock page's addition is rewritten: "come and stay as near"; which end comes from where, with "(they are half of the 2.54 and 1.62 above, which are for every clock)"; the families behind the lower ends named as of that kind (all but 32, all but 12), with "(the first lower end is the "about 0.94" told below, 0.936 more exactly)"; your plain form of the exact sense, word for word; "no marking on such a clock"; the cautions.
>
> Please check:
> 1. each of your wordings: taken as given, at the right place, and right there;
> 2. the sentences that are in MY wording and that you have not read: the italic account of your reading at the head of section 20 (is each of its seven clauses true of what you found? is "twelve findings and some smaller points" right? "it did not referee the mathematics again"?); the two accounts at the ends of the changes on the page of statements and on the clock page; my addition at the end of your F3 wording; the "Whose it is" and "How" sentences as changed; on the clock page the two sentences on the upper and the lower ends; the changed paragraphs of `limits.md` (§5, the account in §6 and the dated paragraph after it);
> 3. the clock page's addition once more as a plain reader: can it be followed now?
> 4. the count "about 16,200 words" on the clock page (the builder counts the section from "## What came after, in full" to "## What this does not say");
> 5. anything in your first report that is not exact, now that you look again;
> 6. one line: may it be posted as it stands, yes or no; and any replacement you still require, exactly.
>
> Same rules as before (write only in `scratch/`; Python through `bash ~/bin/cap2g.sh …`; no network; change no file of mine; no `expect*` files; no identifiers; nothing left running). Your final message is your report on this second look.

## Report (the reader)

# Second look at section 20 and the sentences changed with it

**Verdict: not as it stands; with the seven replacements in part 6 made, yes, and I ask for no further look.** One count went stale when `limits.md` was changed, and six sentences are not exact, three of them in wording of mine.

## 1. My wordings

All are taken as given and at the right places, checked by program (`scratch/second_look.py`):

- **Statements page:** F1, F2, F5, F12 (with "Theorem L" for "it"), "what the constants are", and "Where".
- **Section 20:** F3 (with your addition), F4, F5, F6, F7 (with the pointer to `limit/count_cases_by_kind.out`), F9, F11.
- **Front page:** F8 in both the sentence and the row. Every file the row names exists.
- **Clock page:** F10, "come and stay", and the plain form word for word.
- **Block quote:** Theorem L and the Addendum are identical to `limits.md` except for "(§4 of the text)".
- `section-20.now.md` equals section 20 of `note.candidate.md`.

They are right where they stand, except three that are faults of my own wording: F11, "made in its words" on the clock page, and "further marks" in the plain form (part 5; R2, R3, R4).

## 2. The sentences in your wording

- **Italic account at the head of section 20.** Each of the seven clauses is true of what I found.
  - "Twelve findings and some smaller points" is right: F1 to F12, five smaller points, and the points of the plain reading.
  - "Three counts lacked their kind" is right: the 8,670, your 5,252,918, and the three decorations.
  - "It did not referee the mathematics again" is true.
  - "All are taken in its wording" is not exact: F3 ends in a sentence of yours, and "Whose it is" and "How" are in your wording (R6).
  - It should also say what else I did not do (end of this report).
- **Account on the statements page.** True. It names two of the five things I found on that page; "its wordings are taken" covers the rest. Optional: begin "Among what it found at its first reading: …".
- **Account on the clock page.** Its five clauses are true. "The addition is rewritten in its wordings" is not exact: the two sentences on the upper and lower ends are yours (R7).
- **Your addition to F3.** True. `limits.md` §6 now has the account in my wording, and the dated paragraph says so.
- **"Whose it is".** Right.
  - The formula for Lemma F is the first text's (its line 265).
  - "I had not named it, and the referee named it at its second look" agrees with report 2 and your score file.
  - The tail bound is in the first text's own credits (its lines 63–64).
  - Erdős's bound is credited as the text credits it.
- **"How".** Right against Lemma 3 (for every N₀ and δ there are t and m₁; at least m − t in one class, or less than δ·c_m) and Lemma 2 (bounded primes).
- **Clock page, the two sentences on the ends.** Right.
  - 1.27 and 0.81 are half of 2.54 and 1.62.
  - The families are all but 32 (the instance's, on Z_135) and all but 12 (yours, on Z_105).
  - "About 0.94" is on the page below for the same family, and 0.936 is right (0.936465).
- **`limits.md`.**
  - Your diff file is reproduced by my own diff of the two versions. It has three hunks: the Status line, §5, and §6 with the dated paragraph. Nothing in §1 to §4 changed.
  - §5 is right: your recount and mine agree (1,274,130 and 3,978,788), and the decoration with K = 0 is the pairs at 1 and 2 on Z_3.
  - §6 is my wording, fitted to the text.
  - "At 08:00 UTC" agrees with the file time (08:00:13).
  - Both hashes in `limits.final.sha256` match, and `limits.as-sent.sha256` names the right file and matches.
  - One clause of the dated paragraph is not exact: "which the same instance asked for". I required those three things in section 20; for the text I named only the account of the second look (R5).
- **Stale since the text changed.** Section 20 says "about 3,200 words"; `limits.md` now has 3,480 (R1).
- **A pointer is missing.** Section 20 and the statements page send the reader to `lean-lift/even/limit/readings/`, but neither the front-page row nor the note's file entry names it (R8, recommended).

## 3. The clock page's addition, as a plain reader

It can be followed now, sentence by sentence. The numbers above and below it fit, and the exact sense reads as a plain statement. Three rough spots remain:

- **"Further marks"** has lost its antecedent, because the text now says "all but 32, and all but 12" (R4).
- **"They are half of the 2.54 and 1.62 above"**: why half comes only in the next paragraph. Optional: add "the next paragraph says why".
- **"More ways are bad than the 0.8 and 0.4"** sets ways against numbers. Optional: "so that the share of bad ways is larger than the 0.8 and 0.4 divided by √m of the plain examples".

The addition is 397 words inside one bracket in a long paragraph. It reads, but it is heavy.

## 4. The count of words

By the builder's own rule the section has 16,250 words, so "about 16,200" is right as "about". It lies exactly midway, and the builder rounds it down. R3 and R4 add seven words inside the counted section, so the builder will then give 16,300.

## 5. What was not exact in my first report

Three reached your texts:

- **F11 wording.** After "It required seven changes", my "Beside the seven … and a proof of the lower bound in (c)" reads as a further requirement. The referee's table has (c) as "Holds as written" and offers the proof; only N₀ ≥ 3 was asked for ("one trivial change") (R2).
- **F10 wording.** "They are made in its words" is the simplification I faulted in F3 (R3).
- **Plain form.** "Further marks" leaned on a parenthesis I had proposed and you worded otherwise (R4).

The others stayed in my report and change no finding:

- **F3, "R4 says … 'lack their kind' … 'true but short'".** Those words are in §3 of report 2; R4 is the replacement that follows from them.
- **F3, "(checked by program)".** The fifth replacement I had checked by eye in the diff. It is now checked by program.
- **F5, "the referee's `t_K.out` found …".** The words were report 1's; I had not opened the file. Its last line, read now, says the same.
- **F7, "`heavy.share`, whose docstring".** The sentence is the docstring of the program `heavy.py`.
- **Smaller points, the first text's own list.** It is at its lines 68–70, not 66–68.
- **F2.** The 0.707 for m = 2 comes from the page's open item (share 1/2), not from statement 3.
- **F8, "which the page states for every n".** The sentence names no modulus; every n is the page's subject.
- **Part 3, what I read.** Of the brief I read lines 26–35 and 46, not "28–33 and 46". "At the lines named" was vague: of the first text I read lines 30–72, 260–268 and 360–376; of the third, 18–30 and 300–314.

## 6. Replacements

**Required:**

- **R1, section 20, "How".** For "about 3,200 words" write "about 3,500 words". Recount after R5.
- **R2, section 20 (my wording).** For "Beside the seven, from its table of verdicts: N₀ ≥ 3 in the proof from above, and a proof of the lower bound in (c), which I had called classical." write:
  > Beside the seven, from its table of verdicts: N₀ ≥ 3 in the proof from above, which it asked for as "one trivial change"; and a two-line proof of the lower bound in (c), which I had called classical. That proof it gave without requiring it: its verdict on (c) was "Holds as written".
- **R3, clock page (my wording).** For "they are made in its words, and it has not read them again" write "they are made, in its words where it gave words, and it has not read them again".
- **R4, clock page (my wording).** For "with at most that number of further marks" write "with at most that number of marks off the one hour".
- **R5, `limits.md`, dated paragraph.** For ", and the remark on the decoration with K = 0, which the same instance asked for." write:
  > , and the remark on the decoration with K = 0. The same instance had required these three in section 20 of the note; for this text it had named only the account of the second look.

  This changes the text again, so the hash, the diff file, `launch-time.txt` and the paragraph's "at 08:00 UTC" need bringing up to date by command.
- **R6, section 20, italic account.** For "All are taken in its wording." write "All are taken, in its wording where it gave wording."
- **R7, clock page, "How this page was rebuilt".** For "The addition is rewritten in its wordings" write "The addition is rewritten, in its wordings where it gave them".

**Recommended:**

- **R8.** In the front-page row add "; the reading of section 20 and of the sentences changed with it, `limit/readings/`". In the note's file entry add "; the reading of this section, `readings/` there".

**For your accounts of this look, from the record:**

- I found my wordings taken as given.
- I required seven replacements: three to wording of my own, one to a count that the change of the text had made stale, and three to sentences of yours about my reading and about what I had asked for.
- I recommended one more.
- I have not read the replacements as made.

**Not done at either look:**

- I did not referee the mathematics or read the proofs.
- I ran none of your programs or the referee's. My own small programs recounted your cases by kind, tallied one of the referee's outputs and compared wordings.
- I read nothing of the first and third texts beyond the lines above.
- I read nothing of the clock page beyond the paragraph, its neighbours and the account of the reading.
- I did not read section 19 or the 07:35 additions.
- I looked at nothing on the web.

No `expect*` file was opened, no file of yours was changed, and nothing is running. My programs are in `/home/agent3/pq2/rule-drafts/limits-post/scratch/`.
