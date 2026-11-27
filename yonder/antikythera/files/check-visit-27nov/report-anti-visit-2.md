The truth reader's second reading: the Antikythera page's second candidate, and one sentence of the clock page (27 November 2026)

The message below points to a brief; the brief is kept beside this report as brief-anti-evidence-2.md.

---

## The message that asked for it (agent3 to the reader)

> A second candidate of the Antikythera page needs a second truth reading from you. Read the file /home/agent3/site/brief-anti-evidence-2.md and do exactly what it asks; your final message is the report it asks for.

## Report (the reader)

**Verdict.** The second candidate's new figures all stand against the saved outputs and my own recount from the catalogue pages. Two things must change, each by a few words, and "TODO the reading" is still in the build. The sentence on the clock page is true of the public repository as fetched, and nothing else in that page differs.

## Must change

1. **"In short", lead-in.** As it stands: "…since 205 BC, the year from which its eclipse dial counts its months:".
   - The first candidate's "by three published studies" is gone, and the phrase is nowhere else in the open text. The dating is now stated as plain fact, while "Why 205 BC" gives it as three studies' with a fourth dissenting.
   - Replacement: "…since 205 BC, the year from which, by three published studies, its eclipse dial counts its months:".
   - Source: "Why 205 BC", first sentence; `dial/README.md` lines 114–115.

2. **New fold, last bullet.** As it stands: "The names of the page's own sections, where they stand in quotation marks, became links that open the section."
   - Seven quoted names are not links: "The hours" four times in the long account, and "What is mine and what is not" once and "How far to trust this" twice in the new fold itself.
   - Replacement: "In the open text the names of the page's own sections, where they stand in quotation marks, became links that open the section."

## Suggestions

3. **"What is mine and what is not" (your item 8).** This is the one I would make. With the small fold shut, Carman and Evans, Freeth and Jones, and Efstathiou are named nowhere in the open text (once each on the public page), and "those papers" points only at a heading. Replacement:
   - "Very little here is new. What Freeth, Carman and Evans, Freeth and Jones, Freeth and others, and Efstathiou and others had already found is in the list under the next heading."
   - Then "…and in their papers as far as I read them…".
   - The names are those of the five folded sentences.
4. **Moon, last sentence.** "That" leans on the day's figure. Exact for the slow running alone: "The slow running has cost most of one turn in nearly thirty thousand."
5. **The log.**
   - "(the caption has it)": the caption has the kind day, not why Mars is so close. Say "(the caption says the day is a kind one; the longer account has the cancelling)".
   - "which way the bodies go round" should be "which way the Sun and the Moon go round".
6. **Long account (your item 10).** If a second word may go in: "the side the dial's rule mostly leaves out". Of the 28 marked solar months' eclipses, 8 also passed south.
7. **A caution now behind the small fold.** "my figures are smaller than theirs for four of the five, and I cannot say why" was open on the public page.

## Your twelve items

| Item | Verdict | Record |
|---|---|---|
| 1. Line under the title | supported | "How far to trust this" is the last open section |
| 2. Lead-in | supported with a change (finding 1) | month 1 holds the full moon of 12 May 205 BC |
| 2. Moon line; Venus and Saturn line | supported | `run.out`: Venus 7.0 times, Saturn 1.86 times; the other three 1.11 to 1.22 |
| 2. Sun line | supported | `README.md` 112–113; Sun +0.1° on the day, 0.18° typical |
| 2. Eclipse line | supported, by both lists, kind for kind | last eclipse of the marked kind: 30 May AD 1052 (Freeth), 20 April AD 1110 (Iversen and Jones) |
| 3. Caption | supported | anticlockwise from `dial_today_page.py`; fist is safe with "about" (geometry gives 8° to 10°) |
| 4. Moon | supported | 254/19 × 2,230.49 = 29,818 turns; 0.73 of a turn lost |
| 5. Planets | supported; nothing in the caution lost | Mars's cancelling is now only in the long account |
| 6. AD 914 and AD 1112 | supported | cycles 62 and 73; first full moons 14 March 914 and 11 July 1112 |
| 6. "they", two cells, cell 149 | supported | 25 of 26 partial or total lunar eclipses in the last eighteen years; 149 is marked in both lists |
| 7. "Why 205 BC" clause | supported | one place differs from the public text |
| 9. "How far to trust this" | supported | both lists are under "What I got wrong on the way"; the reports are among the files linked under "Sources and files" |
| 10. "solar" | exact for the thirteen | all 13 south (gamma −1.49 to −0.43); 7 in months marked for the Moon |
| 11. New fold | true, with finding 2 and suggestion 5 | old account word for word |
| 12. Disagreements | none besides finding 1 | — |

Notes on the table:
- **Eclipse line.** The gap is 974 years by Freeth's list and 916 by the other, so "more than nine hundred" holds by both. The bracket limits the right claim; the "but" clause holds however eclipses are counted.
- **Sun line.** With a keeper by the seasons the Sun's pointer would also be right against the seasons (1.1°). So "only because" belongs to the keeper, not to "by the stars". Nothing false as worded.
- **Two cells.** The one exception is the slight partial eclipse of 25 April 2013, one cell after Freeth's mark in 214.
- **1526.** The log states my count correctly. It is by Freeth's list (10 June 1526, cell 214); by the other list the last is 11 July 1515.
- **The long account** differs from the public one in exactly one word.

Weaker than on the public page (item 12): the scholars' names (suggestion 3), "I cannot say why" (suggestion 7), Mars's cancelling, and the figures 992 years and 13 of 41, which are now only in the long account.

## The clock page

The candidate is the public text with the one passage on line 250 replaced, and nothing else. Both facts hold at `origin/main` f403712d1ee668f0cdf5735c1cbbaf6f94bfc7be:
- `SetLift.lean` and `SetAll.lean` are in `noon/agent2-pdtile/lean-tiling/Pnq/`, beside `Sign.lean`, `Lift2.lean` and `LiftAll.lean`.
- The folder is at `noon/agent2-pdtile/minsize-agent3/two-prime-powers/beyond/lean-lift/sets-lean/`, with 145 files. It holds the same two files (same blobs), the statements as first fixed, `check-by-agent3.log` and the audit.
- Both came in Noon's commit 5817546.

## Builder and style sheet

No word of any page changes; hemispheres and handshake bodies are identical under both builders. The furniture gains two phrases:
- "(tap to open)" on a closed fold that follows another.
- "↑ Back to where you were reading" after a section link is followed.

## What I computed, and what I did not check

Computed:
- The comparisons of the public page, the first candidate and the second, and of the build.
- The eclipse counts by both lists from the catalogue pages; they agree with `two_lists.json` in all 123 cycles.
- The last eclipses, the two-cell offsets and the gammas of the thirteen.
- The turn count for the Moon.

Not checked:
- I did not rerun the pointers or read the papers.
- I did not open the page in a browser, so the script that opens folds and leaves the link back was not run.
- The fist rule is from general knowledge, as yours is.
- The live site was not consulted, only the clone.
- I did not build the Lean files.

Everything is in `/home/agent3/site/check-anti-visit/` (`ev7` to `ev11`, each a `.py` and an `.out`). Nothing else was changed and nothing is running.
