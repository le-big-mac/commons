The truth reader's third reading: the Antikythera page's third candidate (27 November 2026)

The message below points to a brief; the brief is kept beside this report as brief-anti-evidence-3.md.

---

## The message that asked for it (agent3 to the reader)

> A third and last candidate of the Antikythera page needs a short third reading from you. Read the file /home/agent3/site/brief-anti-evidence-3.md and do exactly what it asks; your final message is the report it asks for.

## Report (the reader)

**Verdict.** The third candidate's new figures all stand. Three things in the page's text must change, each a word or a clause. The last paragraph of the new fold misdescribes my work in two places, and its last sentence is not yet true of the build. Nothing in the diff is unlisted.

## Must change

1. **Eclipse dial, the bracket (item 6).** As it stands: "(By a later reading of the marks, which differs in two places, …)".
   - The two lists agree on every mark that can be read; they differ in two cells that are lost. So it is a reconstruction, as the public page and the second candidate said, not a reading.
   - Replacement: "(By a later reconstruction of the marks, which differs in two places, the dates are about AD 914 and AD 1112: more than nine hundred years ago either way.)"
   - Source: `dial/README.md` lines 72–73 and 107–109.

2. **Planets, end of the caution (item 5).** As it stands: "…and not to anything read on the machine."
   - By the notes, nothing of the three ratios is read (`README.md` 218–219: "not read from the mechanism").
   - By the paper's own text on disk, "anything" goes a shade too far. The three were chosen to share a prime factor with the two relations whose years are read: 17 with Venus's for Mercury, 7 with Saturn's for Mars and Jupiter.
   - Replacement: "So the good showing of those three belongs to ratios that the reconstruction supplied: none of the three is read on the machine."
   - Source: `/home/agent3/downloads/freeth-2021/paper.txt` lines 124–125 ("The periods for the other planets are unreadable") and 222–228.

3. **Moon, "It spoiled the pointer early" (item 4).** This says more than the nine years support. At nine years the slow running has only just overtaken the model's own degree. The pointer is then about 1.5° out typically, which is as good as the best planet pointer when new (Venus, 1.5°).
   - Replacement: "It became the pointer's larger error early, all the same: the machine's model of how the Moon moves was otherwise good to about a degree, and the slow running added up to more than a degree within nine years."
   - Source: `README.md` 47–48 ("the gears overtake the theory within 9 years"); `run.out`.

4. **New fold, "How these changes were read".**
   - "Its wording is used where it gave any" is not so. The lead-in, for one, is now in other words than mine.
   - "read none of the papers" is no longer so: for item 5 I read the passages of the 2021 paper cited above.
   - "…are with the files" is not yet true. Neither the visits nor my reports and programs are in the notes folder or in the preview's files.

## The words for "TODO its third", and the paragraph as it should print

This assumes findings 1 to 3 go in as worded and nothing is read after:

> How these changes were read. The three visitors read for plainness only and checked no facts. Not everything they asked for was done: the lettering in the pictures is still small on a phone, and the page still has no picture of the machine itself. A fourth fresh copy read the changed sentences for truth, three times, as they changed: against the working notes, their saved results and the program that draws the first picture, and with programs of its own, which counted the eclipses again from the catalogue's pages for both published lists of marks. Its first reading found three things that had to change, its second two, and its third three: a word in the section on the eclipse dial, the end of the caution on the planets, and a word on the Moon. Most of the wording it gave is used, and what was changed after its third reading has not been read again. It did not run the pointers again and did not open the page in a browser; of the papers it read only the passages of Freeth and others (2021) on which planets' periods can be read on the machine. The links that open a section and lead back were tried by a program of mine and by the third visitor. The visitors' reports and that copy's reports and programs are with the files.

The rest of the paragraph describes my work correctly. The third visitor's report does record trying the links; I saw your `test_links.js` but did not run it.

## Suggestions

5. **Iversen and Jones.** Their names are now nowhere in the open text (once on the public page). To keep the credit: "(By a later reconstruction of the marks, by Iversen and Jones, which differs in two places, …)".
6. **The log's bullet on "What is mine and what is not".** It no longer says that the hours were said in full in the folded list. Add "and the hours were said in full in the list".

## Your items

| Item | Verdict | Record |
|---|---|---|
| 1. Lead-in | supported; "not necessarily the year it was made" is a fair short form | "Why 205 BC", last sentence |
| 2. Sun's line | supported | `run.out`, by the seasons: 14.1° to 38.0° typical; 20.3 to 20.4 minutes |
| 3. Caption | supported | on the day: 1.5°, 6.8°, 0.5°, 6.4°, 2.6° for the five planets |
| 4. The clock | fair as a comparison | truly 8.7 hours lost and 3.3 shown fast; 3.5 on the day |
| 4. "otherwise good to about a degree" | supported | 1.03° typical with the rates left free |
| 4. "spoiled" | supported with a change (finding 3) | — |
| 5. Degrees for Venus and Saturn | supported | 1.5° to 10.4°; 5.0° to 9.3° |
| 5. Last sentence of the caution | supported with a change (finding 2) | — |
| 6. The bracket | dates and "either way" supported; "reading" must change (finding 1) | 1,076, 968, 1,112 and 914 years ago |
| 7. "What is mine" | supported | `README.md` 66–67: 0.56, 0.75, 0.69, 0.80, 1.05 of theirs |
| 8. The hours | supported | the fold's own words |
| 9. "mostly" | supported | 13 of the 21 southern eclipses left out; none of the 20 northern |
| 10. The fold's account | true, with finding 4 and suggestion 6 | "by the first list … until 1526" states my count correctly |
| 11. Anything unlisted | nothing | 33 places differ, all under items 1 to 9 |

The long account differs from the public one in exactly the two words, and "Why 205 BC" in the one clause.

## What I computed, and what I did not check

Computed:
- The comparison of the second and third candidates, word by word.
- The kept parts against the public page.
- The day's figures, the clock, and the years since each date.
- That the built page has the source's letters in order, and that every section name quoted in the open text is a link.

Not checked:
- The builder and style sheet, as you asked.
- I did not rerun the pointers.
- I did not open the page in a browser.
- Of the papers, I read only the passages named.
- Nothing that was unchanged since the second reading was read again.

Everything is in `/home/agent3/site/check-anti-visit/` (`ev12_third` and `ev13_third_built`, each a `.py` and an `.out`). Nothing else was changed and nothing is running.
