A truth reading of the changed sentences of the page on cooperation, first candidate (27 November 2026)

The message below points to a brief; the brief is kept beside this report as brief-hand-evidence.md.

---

## The message that asked for it (agent3 to the reader)

> Read the file /home/agent3/site/brief-hand-evidence.md and do exactly what it asks. It is the whole of your task. Your final message is the report it asks for.

## Report (the reader)

**Verdict.** The kept parts are intact, by program. Most new and changed sentences are supported, but three places in the open text do not stand as written, and the new log has one untrue clause and two omissions. Both faults you named came up: a dropped "must" in the live-page steps, and a sentence true only in `bedtime.js`'s convention. A third fault is a new fact that came in with the visitor's wording ("gains nothing").

## Findings, most serious first

**1. MUST. "The machine", the added sentences.**
- As it stands: "A player who always defects does get through the opening, but gains nothing by it. … Against this machine the player who always defects collects the 5 only every third round (the third game above) and falls behind."
- What is wrong: "gains nothing" is false as a reader takes it. With no slips the defector gets 1, 1, 5 from the machine, which is 7 points in three rounds (2.33 a round).
  - A defector earns 1 a round from another defector, so it gains.
  - The machine it is playing gets 0.67 a round, so it wins that pairing.
  - Two machines earn 3 a round from each other; that is the only thing it "falls behind".
- The comparison was lost in the move: in the folded section it stands just before the sentence ("exactly what cooperators earn from each other").
- "Gains nothing" is in no record and not on the old page. It is the visitor's phrase (`visit-hand-1.md`, lines 112 and 198).
- It also sits badly with "among defectors a single machine of this kind does worse than they do" lower down, and with the working note's "The handshake's weakness is that all-defect collects a sucker payment from it every third round" (`README.md` line 188).
- "Does get through the opening" is right: the machine cooperates in rounds 3, 6, 9 and 12 of the third game.
- Replacement for the three sentences:
  > A player who always defects does get through the opening, but earns less by it than the machines earn from each other. If one player defects and the other cooperates, the defector gets 5 points and the cooperator gets nothing; when both cooperate each gets 3, and when both defect each gets 1. Against this machine the player who always defects collects the 5 only every third round (the third game above): 7 points in three rounds, where two of the machines collect 9 each from one another. So among these machines the defector falls behind.
- Sources: `README.md` lines 191–196 (2.96 against 2.32 with no slips, 2.55 against 2.30 at 5%); `check-story-evidence.md` line 56 ("2.33 from yours"); my `steps.out`.
- "Among these machines" is needed: the machine out-earns defectors only above a share of 37% at 1% slips and 55% at 5% (`README.md` line 234).

**2. MUST. "Watch it happen", first step.**
- As it stands: "Wait, and after a while the machine tends to take over the bed. … in the eight times I opened it on the computer I work on, the take-over came after between one and thirteen seconds."
- What is wrong: this drops the first point of the earlier evidence reader's must H08 ("wrong for about half of visitors", `check-story-evidence.md` line 49).
  - `bedtime.js` counts a take-over by any of the three starting states.
  - In `bedtime-25nov.out` only runs 1, 5, 6 and 8 are "the handshake"; runs 2, 4 and 7 are the shifty handshake (one thorn) and run 3 the stiffened wooer (no thorn).
  - With the reader's reruns it is 22 of 40.
- So without "by any of the three" the timing is true only in the script's convention. That the four two-thorn runs also span 1.1 to 13.3 seconds is a coincidence of four openings.
- A visitor who has just read "two thorns at the bottom" and sees "the shifty handshake — 95% of the bed" will think something else won.
- Replacement for the first `<li>`:
  > Wait, and after a while the machine tends to take over the bed: about half the time as a plant with two thorns at the bottom, otherwise as the same machine begun at another of its three states, with one thorn or none. That can take tens of thousands of generations, which the page gets through in seconds: in the eight times I opened it on the computer I work on, the take-over, by any of the three, came after between one and thirteen seconds.
- These are the old paragraph's words. "The same machine begun at another of its three states" is the page's own idiom ("begun at any of its three states").

**3. MUST. "Watch it happen", the line before the steps, and the pointer in the second paragraph.**
- As it stands: "It starts running by itself." and "(its settings are not quite the study's: see "Watch it happen")".
- What is wrong: the third point of H08, a caution the reader added, is now only behind the fold: selection twice as strong, "which makes the take-over quicker and more lasting".
  - The reader's runs gave the machine 73% of generations at the page's strength against 43% at the study's.
  - The open text now says the settings differ but not that they favour the machine.
  - The pointer sends the reader to a section whose open text names no setting.
- Replacement:
  > You can open the bed and try it. It starts running by itself, with selection twice as strong as in my runs, which makes the take-over quicker and more lasting.
- These are the old words, less the 3% and the fifty rounds, which the live page shows on its own sliders. With this the pointer in the second paragraph is honoured.
- If you would rather keep "selection" out of the open, the least that is true is to change the pointer to: "(its settings are not quite the study's, and favour the machine more: see "Watch it happen", where they are given in full behind a heading)".

**4. MUST (small). The new log, three lines of the list.**
- First bullet. It omits that the pointer to the longer account was cut. Replacement:
  > The line under the title says in plain words where the page tells how far to trust it, where it named the section; its pointer to the longer account was taken out; the dates that stood there are now at the end of "How far to trust this".
- Third bullet. "They are from the folded section" is untrue of the first added sentence. Only the points sentence is word for word from the fold, and the last sentence in part (`split.out`). Replacement, to go with finding 1:
  > Under "The machine" the rule stands above the picture (the paragraph was split after its second sentence; no word of it was changed), and four sentences were added on the player who always defects, which is the third game of the picture. The points, and the words "collects the 5 only every third round", are from the folded section "Why two defections and not one"; the sum beside them (7 points in three rounds, against 9) was worked out again by the reader named below.
- Fourth bullet. It does not say what the steps leave out. Replacement of its last sentence, to go with findings 2 and 3:
  > The paragraph on trying the live page is told in three steps, which leave out the live page's share of slips and its length of game; it stands whole, word for word, behind a heading of its own.

**5. Suggestion. The sentence before "A disagreement not settled".**
- It is supported; "I have not found out why" is a fair short form of the fold's sentence.
- But it now follows the bullet about the literature search, so "the other way" has nothing to be the other way from.
- Replacement, in the fold's own words with its "each kind" condition kept:
  > One published study seems to go the other way on what mistakes do: in it a machine which always defects won most runs once each kind of mistake came 2% of the time. I have not found out why: that is told under "A disagreement not settled".

**6. Suggestion. The small paragraph.**
- "This is work of 18 and 19 November 2026 … what has been done to the page since": "This" reads as the page, which was written on 25 November; the study is what dates from the 18th and 19th.
- Replacement:
  > The study is work of 18 and 19 November 2026, corrected on 25 November; what has been done to this page, and who read it, is told under "How this page was written and read".

**7. Suggestion. The log's first paragraph.**
- Add after "its first two screens": "; it followed no link, so it did not see the live page".
- Source: `visit-hand-1.md` line 19. The steps for the live page were rewritten after a visit that never opened it.

**8. Suggestion (slight). The caption.**
- "Of the eight times I opened the page" reads as if those were all the openings; the earlier reader's rerun has eight more (0.8 to 6.7 seconds).
- "Of eight times that I opened the page and timed it, this was the longest wait" is exact.

## 1. Kept parts (`kept.out`, `kept2.out`, `split.out`)

- **Source, letter for letter:** "Why two defections and not one" (1,359 characters), "A disagreement not settled" (1,239) and "For those who want to check" (6,283) are identical. Only the long account's opening tag gained an `id`.
- **The live-page paragraph** (204 words) stands once, word for word, inside the fold "The same in full, with the live page's settings", and not in the open text.
- **The account of the readings** (190 words) stands once, word for word, in the last fold, which is the last element of the page. What follows it is `hand-log-new.html` character for character.
- **Built pages:** the same holds. The only word-level difference in a kept fold is the new "See the picture at full size." in the first one, which the log mentions.
- **Rule paragraph:** old paragraph = new first paragraph + new second paragraph, no word changed; the rule stands before the picture.
- **Script:** `hand_visit.py` remakes the candidate byte for byte. Each built page equals its source plus the full-size links.

Old open-text sentences no longer anywhere in the open text, and whether an open-text reader needs them:

| Old sentence or clause | Where it is now | Needed in the open? |
|---|---|---|
| "The longer account is at the foot, under "For those who want to check"." | Nowhere | No: the heading is visible and two "at the foot" pointers remain. The log should say it was cut (finding 4). |
| "and, in full, under "For those who want to check"" (second paragraph) | Nowhere | No, once finding 3 is in. |
| "with 3% of moves slipping, games of fifty rounds on average" | Fold | No. |
| "selection twice as strong as in my runs, which makes the take-over quicker and more lasting" | Fold | Yes (finding 3). |
| "about half the time as a plant with two thorns at the bottom, otherwise … with one thorn or none" | Fold | Yes (finding 2). |
| "by any of the three" | Fold | Yes (finding 2). |
| The five sentences of the account of the readings | Last fold | No. The open text now claims no reading of the page, so "the second's own runs are checked by nobody" has nothing to qualify there; the long account still says "Nobody has checked those runs". |

The byline's dates are kept in substance in the small paragraph. The other differences are rewordings with nothing lost.

## 2. The new and changed sentences

| Sentence | Verdict | Record |
|---|---|---|
| Line under the title | Supported | "How far to trust this" is the last open section. |
| Opening: the rule clause | Supported; a fair short form | Table in `README.md` lines 176–178; the full rule and the table agree on every sequence of the other side's moves up to 12 rounds (`steps.out`). |
| Opening: "see "Watch it happen"" | Supported with a change | Finding 3. |
| "The machine": rule above the picture | Supported, word for word | `split.out`. |
| "The machine": three added sentences | Not supported as worded | Finding 1. The picture's third game does show what the last sentence says. |
| Caption: "stopped soon after the machine had taken over the bed" | Supported | `bedtime-25nov.out` run 1: "the handshake — 96% of the bed" at generation 74,800, shot at 83,300. |
| Caption: "this was the longest wait" | Supported | 13.3 seconds is the longest of the eight (finding 8). |
| First step | Supported with a change | Finding 2. |
| Second and third steps, and the paragraph after | Word for word from the old paragraph | `kept.out`. |
| Tit-for-tat gloss | Supported | Same words as the gloss already under "What I got wrong". |
| "the one-defection machine of "Why two defections and not one"" | Supported | The fold uses those words. |
| Sentence before the second fold | Supported | Finding 5. |
| Small paragraph | Supported | Finding 6. |
| Log: first paragraph | True of the visitor's brief and report | `visit-hand-1.md` line 19; finding 7. |
| Log: bullets 2, 5, 6, 7 and the closing line | True | In the built page all four section names in the open text are links with existing targets; the public page has none. |
| Log: bullets 1, 3, 4 | Need the changes above | Finding 4. |

Two notes that need no change:
- On the opening, the "it" of "in 2012 it was analysed" is the same three states begun at the cooperating one. The lede had that looseness before, and "What was already known" says it.
- In the 2012 paper's setting, tit-for-tat's "did" means "was seen to do".

## 3. Said twice, or weaker

- **Disagreeing as it stands:** the open first step against the fold (finding 2); "gains nothing" against "a single machine … does worse than they do" (finding 1); the second paragraph's pointer against a section that names no setting in the open (finding 3).
- **Said twice and agreeing:** the points sentence, the tit-for-tat gloss, and "One published study seems to go the other way".
- **Weaker than the public page:** the three cautions of findings 2 and 3. Nothing else, and no credit is lost.

## 4. Description and card

Both are unchanged from the public front page and still true to the candidate. The card's rule ("…and begin again when they cheat") is the full rule; the description keeps "begun at another state".

## Paragraph for the last line

True if the four musts go in as worded, whether or not the suggestions do.

> Another fresh copy of the model then read the changed sentences, one by one, for truth: against the page as it stood before, the working note, the two earlier readings of this page, the report on what was in print, the visitor's report and the programs behind the pictures. By program it found the two folded sections of the story and the longer account letter for letter as before, and the two moved passages word for word, each standing once. It stepped the machines again and ran the program of the two pictures of games, which gave the same files. It asked for three changes to the open text as necessary, which are in as it worded them, and suggested smaller ones. The new sentence on the player who always defects had said that such a player "gains nothing" by getting through the opening; it gets 7 points in three rounds, more than defectors earn from each other and less than the 9 that the machines earn from each other, and the sentences now say that. The first step for the live page had lost that the take-over is, about half the time, by the machine begun at another of its states, and that the timing counts any of the three. And the live page's stronger selection had gone from the open text. Three lines of the list above were corrected too. It did not rerun the evolving populations or the live page, did not read the papers, read the built page as text and not in a browser, and its sums are checked by nobody.

## What I computed

Everything is in `/home/agent3/site/check-hand-visit/`.
- `kept.py`, `kept2.py`, `split.py`, `built_from.py`: the comparisons of section 1 and the origin of the added sentences.
- `steps.py`: the rule against the table; the four games; and the earnings in the table below.
- `handshake_strip_phone.py` rerun into the check folder: both pictures byte-identical to the page's.

| Slips | Machine against machine | Defector against machine |
|---|---|---|
| None, long run | 3 | 7/3 (the machine gets 2/3) |
| 1% (100-round games, by the study's `ipd.py`) | 2.87 | 2.32 |
| 2% | 2.78 | 2.31 |
| 3% | 2.70 | 2.31 |
| 5% | 2.55 | 2.30 |
| 10% | 2.29 | 2.28 |

These agree with the working note's table. The share of machines above which the machine out-earns defectors comes out at 37%, 55% and 97% for 1%, 5% and 10% slips, as the note has it.

## What I did not check

- I did not run the live page or `bedtime.js`. I relied on `bedtime-25nov.out` and the earlier reader's outputs, which nobody has checked.
- I did not rerun the evolving populations, the censuses or the Ioannou runs.
- I did not read the papers, beyond one search of the 2012 text for tit-for-tat.
- I did not view the page in a browser or at phone size, so I did not see the links open the folds. I read the script and confirmed the targets exist.
- I looked at the strip picture as an image, but not the bed or population pictures.
- I checked the content of the kept folds for identity only.
- I did not run a leak scan, check the `files/` pages, or look at the thumbnail.

Nothing outside the check folder was changed, nothing was posted, and nothing is left running.
