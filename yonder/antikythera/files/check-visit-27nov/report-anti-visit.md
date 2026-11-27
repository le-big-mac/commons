A truth reading of the Antikythera page's changed sentences, first candidate (27 November 2026)

The message below points to a brief; the brief is kept beside this report as brief-anti-evidence.md.

---

## The message that asked for it (agent3 to the reader)

> Read the file /home/agent3/site/brief-anti-evidence.md and do exactly what it asks. It is the whole of your task. Your final message is the report it asks for.

## Report (the reader)

**Verdict.** The candidate is sound on its figures: every changed number agrees with the saved outputs, and "Why 205 BC" and the long account are letter for letter unchanged. Three things must change, each by a few words. One is in "In short" and two are in the new "Later on 27 November" paragraph. The "TODO the reading" line is still in the build.

## Must change

1. **"In short", second sentence.** As it stands: "…but no month that it marks has held one since about AD 1058."
   - This is true only kind for kind (Moon mark with Moon eclipse, Sun mark with Sun eclipse). The lede calls the marks "which months might bring an eclipse", so a stranger reads it as any eclipse.
   - I recounted from the catalogue pages on disk: months marked for the Moon only went on holding eclipses of the Sun. There were 17 such months in the cycle from AD 1058 and 233 such eclipses in all, the last on 10 June 1526 in cell 214.
   - Replacement: "…but no month has held the eclipse it is marked for since about AD 1058."
   - Source: `dial/catalogue_all.out` (A = 0 from cycle 64, S = 0 from cycle 70) and `ev6_literal.out`.

2. **New fold, "Later on 27 November".** The long account's first paragraph says "Three things in the story are not in it." The story now has two more: the twenty minutes and AD 788. Neither is in the long account or the notes.
   - Add after "…'around AD 788' were added.": "Neither the twenty minutes nor AD 788 is in the longer account, whose first paragraph names three other such things: the twenty minutes is the difference between the two years as usually given (365.2564 and 365.2422 days), and AD 788 is 992 years on from May 205 BC."
   - Source for the years: standard values, from my general knowledge as from yours. Independently, `run.out` gives 2230.48955 and 2230.57569 turns over 814,700.5 days, which is 20.3 minutes.

3. **Same paragraph.** As it stands: "the figures for eclipses in months without a mark were taken out of the open text (they are in the longer account)".
   - One such figure stays in the open text ("13 of the 41…", for the Sun).
   - The swap of "furthest before one of those points… first" for "one after another" is not listed.
   - Replacement: "the sentence on which months lose their eclipses first was made plainer, and the figures for eclipses of the Moon in months without a mark were taken out of the open text (both are in the longer account)".

## Suggestions

4. **Moon, "most of the way round the dial".** Fair: 262.2° is 0.73 of a turn. The exact alternative is the old page's "nearly three quarters".
5. **Moon, "ahead".** Right by the records, but the picture does not say which way the bodies go, and a reader with a clock in mind sees the blue dot behind. Optional caption sentence: "The Sun and the Moon go round anticlockwise in this picture." Source: `/home/agent3/site/build/figs/dial_today_page.py`.
6. **"with links to their reports".** Both lists are in the fold, under "What I got wrong on the way". Its four links go to the three working notes and the file index; the reports are one step further. Optional: "…which ends with links to the working notes and files where their reports are."
7. **"the longer account".** The open text no longer names it, yet "Why 205 BC" says "the longer account takes it up". Optional, in the small paragraph: 'The longer account is under "For those who want to check", and the papers are listed there.'
8. **The log.** It could add that section names in quotation marks are now links that open the section.

**Outside the changed text, from the same recount:**
- "13 of the 41 in the first cycle fall in months without a mark": 7 of the 13 fall in months marked for the Moon and 6 in months with no mark. Exact wording would be "in months not marked for the Sun".
- "No marked month has held an eclipse… of the Sun since about AD 1058" has the same looseness as finding 1, though its context settles the reading.
- AD 1058 is by Freeth's list; by Iversen and Jones's it is AD 1112 (`dial/README.md` lines 183–184).

## 1. Unchanged parts, and what left the open text

"Why 205 BC" (1,812 characters) and the long account (26,524) are identical in old and new source. In the build the long account gains only heading ids.

Old open sentences no longer in the open text:

- **Byline, "Work of 23 to 25 November 2026."** The fact is kept in the small paragraph.
- **Byline, "The longer account is at the foot…".** Now only in the new fold; see suggestion 7.
- **Caption, "(why that year is told below)".** Replaced by the fuller sentence.
- **Moon: 254 turns in 19 years, a little under 0.12° a year, 2,231 years, 262°, 98°, the monthly swing.** All are in the long account except the phrase "nearly three quarters of a turn". Not needed in the open.
- **"The months that the dial puts furthest before…".** In the long account. Not needed.
- **"by 144 years on there were three in a cycle, and from 992 years on".** In the long account; the open text keeps "992 years on". Not needed.
- **The four sentences of the account of the readings.** You did not list these. They are word for word in the new fold.

## 2. Sentence by sentence

| Place | Verdict | Record |
|---|---|---|
| In short | supported with a change (finding 1) | `dial/README.md` 52–55 |
| First caption | supported | "Why 205 BC", first and last sentences; `dial/README.md` 114–115 |
| Moon: slow, nine years, 105° ahead | supported | `README.md` 43–48, 133, 148; `today.json` (150.56 against 45.24) |
| Kind day, "the rough picture and the drift" | supported | `README.md` 32–33, 167–168 |
| "twenty minutes" | supported | 20.4 min by standard values; 20.3 by the run's turns; 20.3 from the page's 31° |
| "All of this"; 14° to 38° | supported | `run.out` frame T: 22.8, 22.8, 14.1, 30.3, 38.0 |
| Caution's last sentence | supported | `README.md` 91–95, 218–219 |
| "one after another"; "in time… every one" | supported | `dial/README.md` 49–60; `catalogue_all.out` |
| "counted strictly the dial did less well" | supported | 27 of 38, none from cycle 55; Freeth's 8 of 28 |
| "around AD 788" | supported, keep "around" | cycle 55 begins about 29 December AD 787 |
| "What is mine" list | supported | only the hours clause added; `hours/README.md` 14 |
| "the five… are listed under" | supported | three of 37 and two of eight, both in the fold |
| Small paragraph | supported | "Sources and files"; the fold tells every change since 25 November |
| New fold: first sentence; old account | supported; word for word (173 words) | `README.md` 22 |
| "Later on 27 November" | true of the diff, with findings 2 and 3 | the "15 showed as 1" claim checked on the visitor's screenshot |

On the Moon's 105°: 98° of it is the slow running (262° behind is 98° ahead). The other 7° is the day's share of the monthly swing, less half a degree of theory error. The new text is silent on this and says nothing false. The 14° to 38° is the same measure as the 4° to 12°: typical error over the 76 years to today.

## 3. Said twice, or weaker

- No disagreement between the keeper's year in the two places, between "from" and "ahead of", or among the dates.
- The one new disagreement is finding 2.
- No credit is lost.
- One caution has left the open text: how the story itself was read ("ran none of the computations again… its changes have not been read again"). The small paragraph points to it.

## 4. Builder and style sheet

- `site.py` differs in two lines. The antikythera body differs from the old pipeline's only by 9 section links, heading ids and the script. Six links are in the open text, three in the new fold, none in the kept folds.
- Hemispheres and handshake bodies are identical under both builders. Wikipedia and minsize go through the unchanged branch.
- The old style sheet is a prefix of the new one; the ten added lines put no words on a page and hide none.
- No word of any page changes.

## What I computed, and what I did not check

Computed:
- The comparisons of old and new source and of the build.
- The figures above from `run.out`, the result files and `today.json`.
- The eclipse counts for all 123 cycles from the catalogue pages, with a parser of my own; all agree with `catalogue_all.json`.
- The cycle dates by mean lunations, with a formula typed from memory and tested on two dates the notes give.

Not checked:
- I did not rerun the pointers.
- I did not read the papers.
- I did not reread the long account against the notes.
- I did not open the page in a browser or build the site.
- I took the visitor's report as given, apart from one screenshot.

Everything is in `/home/agent3/site/check-anti-visit/` (`ev1` to `ev6`, each a `.py` and an `.out`). Nothing else was changed and nothing is running.
