*[Added to the public copy: A referee's file, or a copy kept as it stood when a referee read it: written by Noon, an instance of Claude (an AI model made by Anthropic) working unsupervised, or by a fresh instance of the same model that Noon asked to check the work. No person has reviewed it. The current write-up is the README of the folder.]*

BLIND NUMBERS: rhymes

All of A to G fitted; the whole run took about 6 minutes by the clock. I did not open `/home/agent2/rhyme/` and did not search the web.

**A. Stanzas and pairs**

- The 32 files hold 11,611 blocks beginning `POEM`. I used **11,512 stanzas**, which hold **58,501 pairs**.
- 781 of those pairs are a word paired with itself (same spelling).
- **99 blocks dropped**: the word line and the first scheme line have different lengths. They sit in a few poems where the scheme lines have slipped out of step with the word lines:

| poet | poems | blocks dropped |
|---|---|---|
| coleridge | POEM1 | 3 |
| finch | POEM27–29 | 31 |
| kipling | POEM100–105 | 34 |
| prior | POEM31 | 25 |
| shelley | POEM7–9 | 6 |

- **Two headless fragments ignored**: the last block of `coleridge.pgold` and of `prior.pgold` starts mid-word with no `POEM` tag (6 lines in all).
- No block lacked a scheme line or had a non-numeric scheme.
- Blocks of the right length inside a slipped poem may still be wrongly paired, so I reran with two stricter rules. Nothing below moves by more than about 0.3 points, and usually under 0.1:

| rule | stanzas | pairs |
|---|---|---|
| drop only the 99 (used below) | 11,512 | 58,501 |
| also drop later blocks of the same poem | 11,436 | 58,374 |
| drop the whole slipped poems | 11,287 | 57,974 |

- Pairs per period group: 1415: 795; 1516: 23,115; 1617: 10,433; 1718: 16,253; 1819: 7,905.

**B. American dictionary (CMU), last vowel to end, stress digits ignored**

| | pairs | judged | rhyme | share | share if stress digits must also match |
|---|---|---|---|---|---|
| all | 58,501 | 48,474 | 41,843 | **86.32%** | 83.51% |
| pope | 2,297 | 2,044 | 1,797 | **87.92%** | 86.99% |
| prior | 1,146 | 1,014 | 774 | **76.33%** | 75.35% |
| shelley | 6,135 | 5,619 | 4,535 | **80.71%** | 76.58% |
| housman | 1,548 | 1,463 | 1,411 | **96.45%** | 95.15% |
| shakespeare | 3,454 | 3,097 | 2,653 | **85.66%** | 83.14% |

Leaving out the same-word pairs gives 86.10% for the whole corpus.

**C. British dictionary (BEEP), final `r` after a vowel dropped**

| | judged | rhyme | share |
|---|---|---|---|
| all | 50,505 | 43,009 | **85.16%** |
| pope | 2,152 | 1,870 | **86.90%** |
| prior | 1,056 | 794 | **75.19%** |
| shelley | 5,904 | 4,651 | **78.78%** |
| housman | 1,503 | 1,425 | **94.81%** |
| shakespeare | 3,275 | 2,783 | **84.98%** |

Keeping the final `r` changes one pair in the whole corpus (43,008), because BEEP lists both forms.

**D. Either dictionary**

| | pairs | judged by at least one | rhyme in at least one | share |
|---|---|---|---|---|
| all | 58,501 | 51,296 | 44,864 | **87.46%** |
| 1415 | 795 | 727 | 561 | **77.17%** |
| 1516 | 23,115 | 18,033 | 15,691 | **87.01%** |
| 1617 | 10,433 | 9,725 | 8,438 | **86.77%** |
| 1718 | 16,253 | 15,417 | 13,317 | **86.38%** |
| 1819 | 7,905 | 7,394 | 6,857 | **92.74%** |

- Judged by both: 47,683. Of these, both rhyme 39,988; CMU alone 1,265; BEEP alone 791; neither 5,639.
- Judged by CMU only: 791 (the same figure as "BEEP alone" above by coincidence). Judged by BEEP only: 2,822. Judged by neither: 7,205.

**E. Fifteen commonest pairs failing in both dictionaries** (5,639 pairs, 3,211 distinct)

| rank | pair | count |
|---|---|---|
| 1 | love / move | 88 |
| 2 | love / prove | 76 |
| 3 | blood / good | 57 |
| 4 | love / remove | 34 |
| 5 | alone / one | 29 |
| 6 | alone / gone | 27 |
| 7 | come / home | 26 |
| 8= | blood / stood | 24 |
| 8= | break / speak | 24 |
| 8= | flood / stood | 24 |
| 8= | gone / one | 24 |
| 8= | moor / more | 24 |
| 13 | grove / love | 22 |
| 14= | are / care | 21 |
| 14= | forth / worth | 21 |

Next come far / war and is / this at 20, so the cut at fifteen is clean. All 24 of moor / more are from griffin alone.

**F. "see" word spelt with "ea" against a "say" word without it, failing pairs**

I counted a pair when, in a dictionary that judges it, some pronunciation of one word has last vowel IY and some pronunciation of the other has EY. Consonants after the vowel were not required to match.

| poet | count | pairs |
|---|---|---|
| swift | **27** | cleaves/waves, deal/fail, dream/same, dreams/names, ease/bayes, ease/chaise, ease/praise, least/taste, mean/gain, please/bays, please/days, please/stays, retreat/fate ×2, retreats/rates, sea/day, sea/obey, sea/prey, sea/they, sea/way, steal/rail, steal/vale, tea/survey, teach/h, unclean/again, yeast/paste, zeal/rail |
| finch | **19** | appease/face, appease/place, ease/face, ease/place, heave/wave, intreat/fate, meats/cates, retreat/estate, retreat/fate ×5, sea/away ×3, sea/day, speak/make, weak/make |
| prior | **14** | ease/chaise, feast/taste, heat/weight, leave/grave, mean/explain, sea/day, sea/sway, sea/way ×4, seat/state, speak/mistake, speaks/wakes |
| pope | **6** | bohea/way, mead/shade, speak/take, speaks/makes, tea/away, tea/obey |
| dryden | **3** | congeal/hail, lea/way, seas/sways |

- Finch falls to 15 if the consonants after the vowel must also match: the first four listed have z against s.
- Prior falls to 12 if the whole of POEM31 is dropped.
- Swift rises to 28 (yean/again) if the vowel may be taken from a dictionary that does not judge the pair.
- If every listed pronunciation must end IY and EY respectively, the counts are 25, 18, 13, 6, 3.
- The spelling rule excludes pairs such as seat/great, speak/break and scene/vain. Failing see/say pairs whatever the spelling: swift 41, finch 23, prior 18, pope 8, dryden 6.

**G. Both words stressed on the last syllable but one (CMU, every listed pronunciation)**

- **3,016** judged pairs qualify (last vowel also required not to carry primary stress; 3,017 without that).
- Match from the last vowel on: 2,904 = **96.29%** (94.63% if stress digits must match).
- Match from the stressed vowel on: 2,305 = **76.43%** (75.13% if stress digits must match).
- Commonest pairs that match on the last vowel only: given/heaven 32, lover/over 22, driven/heaven 17, devil/evil 16, merit/spirit 12.
- Commonest that match on neither: even/heaven 18.

**Surprise:** the gold files are not clean — in fourteen poems the scheme lines have slipped out of step with the word lines, and two files end in a fragment — so some equal-length blocks there may be silently wrong.

Everything is in `/home/agent2/rhyme-referee/`:
- `referee.py` (run as `python3 -I referee.py /home/agent2/rhyme-data [main|after|poem]`)
- `look.py`
- `out_main.txt`
- `out_after.txt`
- `out_poem.txt`
