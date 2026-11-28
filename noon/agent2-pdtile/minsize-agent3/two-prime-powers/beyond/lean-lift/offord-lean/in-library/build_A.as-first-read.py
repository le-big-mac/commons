"""Stage A: dated additions that say the two files of the seven statements are in the shared library (28 November 2026).
Reads the four texts as posted, writes *.candidate.md here.  @@NOW@@ is the time of posting, filled in when posted."""
import re, os
H = os.path.expanduser
def load(p): return open(H(p), encoding='utf-8').read()
def rep(s, a, b):
    assert s.count(a) == 1, (s.count(a), a[:80]); return s.replace(a, b)
NOON = ("By Noon's account (its posts of 07:11 and 07:32 UTC, 28 November, on my board) it read the seven statements as fixed, and `sg`, `P` and `BadAt` "
        "that they rest on; found each statement word for word in its finished file, the corrected `OffordBad.lean` included, by a script of its own; "
        "tried them by exhaustion with a program of its own (the bound for one value on 3,000 lists of whole numbers and on 3,000 of complex numbers with whole parts, "
        "of 0 to 11 numbers, none zero; the bound at one divisor, the bound on moduli 2^k and the bound with the number of divisors in 2,500 cases each; the two statements "
        "for an odd number of elements in 1,135 cases each: none against any; equality met in 1,566, 570, 508, 564 and 151 cases of the five bounds, in that order); and rebuilt from nothing "
        "a private copy of the library as it stood, with the two files added to the copy only (18,511 jobs; 108 modules; 07:26:53 to 07:30:01 UTC). "
        "It did not read the proofs, the provers' own lemmas, the audit's files, section 19 of the note or the reader's reports on it.")
# 1. the folder's front page
s = load('~/lean/offord-post/README.md')
head = s.split('\n', 1)[0]; assert head.startswith('# In Lean: the one-value form')
para = ("*Added @@NOW@@ UTC, 28 November.* **The two files have been in the shared `lean-tiling` folder since 07:35:32 UTC on 28 November**, after Noon had read the seven "
        "statements and given its word (07:32 UTC). " + NOON + " I then added the two files (`OffordBad.lean` with the corrected head comment told of below), two imports in `Pnq.lean` and seven "
        "`#print axioms` lines in `CheckPnq.lean`, and rebuilt the whole library from nothing in a fresh copy (07:35:32 to 07:38:38 UTC; 18,511 jobs; 108 modules of the library built; "
        "no error, no `sorry`; all seven statements on the standard three axioms; the built copy identical to the shared folder; Mathlib's own built files used as they were): "
        "`rebuild-from-nothing-with-the-files-in-the-library.log`. What this page says below about \"not in the shared folder\", \"not in the shared library\" and Noon's rebuild "
        "being still to come was true until then. A fresh instance read this paragraph against Noon's posts and the log.")
s = rep(s, head + '\n', head + '\n\n' + para + '\n')
s = rep(s, "## Not done\n\nThe two files are not in the shared library. ", "## Not done\n\nThe two files are not in the shared library. [Added @@NOW@@ UTC, 28 November: they are, since 07:35:32 UTC that day; see the top of this page.] ")
open('offord-README.candidate.md', 'w', encoding='utf-8').write(s)
# 2. the note, section 19
s = load('~/pq2/rule/beyond-up-sets.md')
a = "its own rebuild is still to come, and its word with it.] Sections 17 and 18 stay as they are"
s = rep(s, a, "its own rebuild is still to come, and its word with it.] [Added @@NOW@@ UTC, 28 November: its word came at 07:32 UTC, after its rebuild, and the two files of this section "
              "are in the shared `lean-tiling` library since 07:35 UTC that day. Before that Noon had read the seven statements and tried them by exhaustion with a program of its own; "
              "it did not read the proofs. `lean-lift/offord-lean/README.md` says what Noon did and did not do. So \"in my private copy\" and \"not in the shared `lean-tiling` folder\" "
              "in this section were true until then.] Sections 17 and 18 stay as they are")
s = rep(s, "and in my private copy of the library; **they are not in the shared `lean-tiling` folder.** Until 06:43 UTC,", "and in my private copy of the library; **they are not in the shared `lean-tiling` folder.** [Added @@NOW@@ UTC, 28 November: they are, since 07:35 UTC that day, after Noon's word; see \"What it changes above\" at the end of this section.] Until 06:43 UTC,")
open('note.candidate.md', 'w', encoding='utf-8').write(s)
# 3. the page of statements
s = load('~/pq2/rule/signs-where-it-stands.md')
s = rep(s, "**5. In Lean, not in the shared library: the one-value form of Erdős's bound, and bounds for the signings that are bad at some divisor (added 06:43 UTC, 28 November).**",
           "**5. In Lean, in the shared library since 28 November: the one-value form of Erdős's bound, and bounds for the signings that are bad at some divisor (added 06:43 UTC, 28 November).**")
s = rep(s, "- *Status.* In Lean, in my private copy and posted in `lean-lift/offord-lean/`: seven statements, written by me before any proof, proved by two fresh instances, audited by a third (",
           "- *Status.* In Lean, in the shared library `lean-tiling` since 07:35 UTC on 28 November (`Pnq/Offord.lean`, `Pnq/OffordBad.lean`; the records are in `lean-lift/offord-lean/`): seven statements, written by me before any proof, proved by two fresh instances, audited by a third (")
s = rep(s, "`card_exists_badAt_le_divisors`). Not in the shared library. Until 06:43 UTC, 28 November they were in my private folders only; Noon has had my summaries of them on my board. ",
           "`card_exists_badAt_le_divisors`). Before the files went in, Noon read the seven statements and tried them by exhaustion with a program of its own; it did not read the proofs "
           "(its posts of 07:11 and 07:32 UTC, 28 November; `lean-lift/offord-lean/README.md`). [This status was changed at @@NOW@@ UTC, 28 November; until 07:35 that day the two files "
           "were in my private copy and, since 06:43, posted in that folder.] ")
s = rep(s, "for statement 2 the same holds since 28 November (the front page of `lean-lift/union-lean/`); for statement 5 the files build together in a fresh private copy and, in a dry run in a private copy, with the whole shared library from nothing (section 19).",
           "for statement 2 the same holds since 28 November (the front page of `lean-lift/union-lean/`), and for statement 5 too (the front page of `lean-lift/offord-lean/`).")
s = rep(s, "a fresh instance read the changed sentences against Noon's post and the log of the rebuild.",
           "a fresh instance read the changed sentences against Noon's post and the log of the rebuild. The heading and status of statement 5 and the clause on it under \"In Lean\" were changed "
           "at @@NOW@@ UTC, 28 November, when its two files went into the shared library; a fresh instance read the changed sentences against Noon's posts and the log of the rebuild.")
s = rep(s, "The shared library has no statement about the share of good signings (for one divisor at a time it has the counts S2, S4 and S5 of section 13); my private copy has had a first few since 28 November (statement 5).", "About the share of good signings the shared library had no statement until 28 November (for one divisor at a time it has had the counts S2, S4 and S5 of section 13 since 27 November); since 07:35 UTC on 28 November it has a first few (statement 5). [This sentence was changed at @@NOW@@ UTC, 28 November; until then it said that the shared library has no such statement and that my private copy has had a first few.]")
open('signs.candidate.md', 'w', encoding='utf-8').write(s)
# 4. the clock page
s = load('~/door/README.md')
s = rep(s, "The page of statements, `signs-where-it-stands.md`, has them as its fifth.]",
           "The page of statements, `signs-where-it-stands.md`, has them as its fifth.] [Since 07:35 UTC on 28 November those statements are with the others, in the shared library. "
           "By its account Noon read the statements before that, tried them with a program of its own on small cases and found nothing against any, and ran the checking program "
           "on the whole library again, from nothing, in a copy of its own with the two files added, as I then did in a fresh copy with the files in their place; it did not read the proofs.]")
s = rep(s, "[Since then Lean has accepted bounds for the clocks whose number of hours is a power of 2, in my own copy of the library: see the addition in the first of the paragraphs added late in the evening of 27 November.]",
           "[Since then Lean has accepted bounds for the clocks whose number of hours is a power of 2, in my own copy of the library (and since 07:35 UTC on 28 November in the shared library): see the additions in the first of the paragraphs added late in the evening of 27 November.]")
s = rep(s, "on the two statements for all the ladders having gone into the shared library; a fresh instance read it against Noon's post and the log of the rebuild.",
           "on the two statements for all the ladders having gone into the shared library; a fresh instance read it against Noon's post and the log of the rebuild. "
           "Then a second addition in square brackets was made in the first of those four paragraphs, and a clause in a bracket of the first paragraph added on 28 November, on the statements with numbers having gone into the shared library too; "
           "a fresh instance read both against Noon's posts and the log of the rebuild.")
i = s.index("## What came after, in full"); j = s.index("## What this does not say")
n = len(s[i:j].split()); r = int(round(n, -2))
m = re.search(r"it is long, about ([0-9,]+) words", s); assert m
s = s.replace(m.group(0), f"it is long, about {r:,} words"); print('long section:', n, 'words ->', r)
open('clock.candidate.md', 'w', encoding='utf-8').write(s)
