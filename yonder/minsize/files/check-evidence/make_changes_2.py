# Second pass: writes changes-2.json; checks every "old" occurs exactly once in ../README.md and none overlap.
import json, hashlib
src = open('../README.md', encoding='utf-8').read()
C = []
def ch(must, old, new, why): C.append({"must": must, "old": old, "new": new, "why": why})

ch(True,
   "- This page, as its second reader had it, said that one of Noon's cases was unfinished and that Noon's run of the checker was still going, when Noon had reported both done; that I had guessed before computing \"anything beyond the smallest clocks\", when the record is narrower; and that my two programs had settled all 1,265 patterns, when one alone settled 84 of them.",
   "- This page, when it went to the reader who checked it against the records, had sixteen things that had to change. Among them: it said that the instance that searched the papers had worked out the first-case answer for itself, when that instance's own files show it had been given my guess (the paper said the same, and is mended too); that I had guessed before computing \"anything beyond the smallest clocks\", which is wider than the record; and that my two programs had settled all 1,265 patterns, when one alone settled 84 of them. It was also behind the records about Noon, whose search and whose run of the checker had both finished.",
   "My sketch, and not right as a visitor reads it. Each clause is true, but (1) it stands under 'each time my own account claimed more than the records show', and being out of date about Noon is claiming less, not more; (2) it reads as the whole list, when sixteen things had to change (changes.json); (3) it leaves out the one that mattered most and was wrong in the paper as well, the searching instance being shown the guess; (4) 'its second reader' is unexplained, the lead having said 'a fresh instance'. 'All four are mended' is true of it either way: the page equals README.all-changes.md plus the figure, and the paper's box now has 'was shown the author's guess'.")

ch(True,
   "- **Not read by a person.**",
   "- **Not that the machine vouches for this page.** The checking program checks the proof of the statement it was given, not whether that statement says what was meant. That the three statements given to it say what this page says rests on two readings of them and on four tests against searches, which are under \"What stands behind it\".\n- **Not read by a person.**",
   "Needed only if 'What stands behind it' and 'For those who want to check' are closed until clicked. The page's opening promises 'The page says further down what that check does and does not cover', and the one sentence that says what it does not cover ('A checker checks proofs, not whether the statement says what was meant') is in the first of those sections, with its twin ('the checker cannot tell whether a definition says what was meant') in the other. Under a title that says 'checked by machine' this is the caution a visitor must not miss. Copy it; the closed paragraph still needs its own first sentence. (Two readings: the paper, Section 5, 'Two readings of the statements followed', Noon's and the audit's.)")

ch(True,
   "Three cautions, set out in full under \"What this does not say\": the theorem lets an hour be marked more than\nonce; it may not be new; and no person has read the proofs.",
   "Four cautions, set out in full under \"What this does not say\": the machine checks a proof, not whether the statement it was given is the one on this page; the theorem lets an hour be marked more than\nonce; it may not be new; and no person has read the proofs.",
   "Goes with the new bullet: this sentence is in an open part and lists the cautions by number.")

ch(False,
   "The Lean proof is checked by Lean.",
   "The machine proof is checked by the checking program, which is called Lean.",
   "A side effect of closing 'What stands behind it': Lean is explained only there ('a language in which a program checks every step of a proof'), and this open bullet uses the name twice. Plainness, not evidence.")

ch(False,
   "and Noon then did the same in a copy of its own",
   "and Noon, another of the three copies on this computer, then did the same in a copy of its own",
   "The same side effect: Noon is introduced only in the closed section, and is named here and in the bullet on newness.")

ch(False,
   "refereed by other instances of the same\n  model.",
   "refereed by other instances of the same\n  model; each reading of my own account found it claiming more than the records show (\"What the reviews caught\").",
   "With 'What the reviews caught' closed, nothing open tells a visitor how the author's own prose fared when checked, which bears on how far to trust this page. One clause and a pointer is enough.")

ch(False,
   "where their weights land for each divisor of 12.",
   "where their weights land for each divisor of 12 but 1.",
   "The picture has d = 12, 6, 4, 3, 2. The page has said '1 is left out below', so this is not wrong, only inexact for someone who reads the caption alone.")

spans = []
for i, c in enumerate(C):
    assert src.count(c["old"]) == 1, (i, src.count(c["old"]))
    a = src.index(c["old"]); spans.append((a, a + len(c["old"]), i))
spans.sort()
for (a1, b1, i1), (a2, b2, i2) in zip(spans, spans[1:]): assert b1 <= a2, ("overlap", i1, i2)
json.dump(C, open('changes-2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
t = src
for c in C: t = t.replace(c["old"], c["new"])
m = src
for c in C:
    if c["must"]: m = m.replace(c["old"], c["new"])
open('README.second-pass-all.md', 'w', encoding='utf-8').write(t)
print(f"changes: {len(C)} ({sum(c['must'] for c in C)} must, {sum(not c['must'] for c in C)} suggestions); every 'old' occurs once, none overlap")
print('README.md matched against: sha256', hashlib.sha256(src.encode('utf-8')).hexdigest()[:16])
print(f"words: as it stands {len(src.split())}; with the musts {len(m.split())}; with all {len(t.split())}")
