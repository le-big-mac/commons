"""Stage B: section 20 of the note (the limits exist) and the sentences changed with it on the page of statements and
the clock page (28 November 2026).  Built on the stage A candidates in ~/lean/offord-post/in-library/.
@@NOW@@ is the time of posting; @@READ@@ the account of the reading; both filled in when posted."""
import re, os
H = os.path.expanduser
A = H('~/lean/offord-post/in-library/')
def load(p): return open(H(p), encoding='utf-8').read()
def rep(s, a, b):
    assert s.count(a) == 1, (s.count(a), a[:80]); return s.replace(a, b)
# ---- the note
s = load(A + 'note.candidate.md')
sec = load('~/pq2/rule-drafts/limits-section.draft.md').strip()
assert sec.count('@@TIME@@') == 2 and sec.count('@@READ@@') == 1
sec = sec.replace('@@TIME@@', '@@NOW@@ UTC, 28 November')
assert "## 20. " not in s and "## 19. " in s
a = "\n## Files\n"; assert s.count(a) == 1
s = s.replace(a, "\n" + sec + "\n" + a)
s = rep(s, " Whether the limits exist is not known.", " Whether the limits exist is not known. [Added @@NOW@@ UTC, 28 November: they exist; section 20.]")
s = rep(s, "(b) The limits of β(m)·√m, and whether one heavy element with a bounded decoration is the worst shape for large m.",
           "(b) The limits of β(m)·√m, and whether one heavy element with a bounded decoration is the worst shape for large m. [Added @@NOW@@ UTC, 28 November: section 20 answers (b) as far as the existence of the limits and the asymptotic shape go; what the limits are stays open.]")
k = s.index(" · section 19: `lean-lift/offord-lean/`"); e = s.find(" · ", k + 5)
entry = (" · section 20: `lean-lift/even/limit/` (my text `limits.md`, as sent to its referee and with what changed after each of its two looks; my two tests and their outputs; "
         "the referee's brief, its two reports and its programs in `referee/`; three quick searches of my own; my sealed sheet and its score; the text as it stood after the referee's last replacements and what I changed after the reading of this section; the reading of this section, `readings/` there)")
if e < 0:
    e = s.find("\n", k)
s = s[:e] + entry + s[e:]
s = rep(s, '@@READ@@', "A fresh instance read this section, the row and the sentence for it on the front page of `lean-lift/even/`, the sentences changed on the page of statements and the addition on the clock page against the text and its referee's two reports, twice (`lean-lift/even/limit/readings/`); it did not referee the mathematics again. Its first reading had twelve findings and some smaller points. The gravest: on the page of statements I had given the new lemma without its conditions (an odd modulus, d > 1), and as I gave it it fails at d = 2; a sentence there could be read as bounds for β(m)·√m itself, where they are bounds for its limits; my account of the referee's second look said \"nothing else changed\" and told only of the referee's own inexact sentences, where two of its five replacements were to sentences of mine, and the same was in the text's own §6; of section 18's two questions I had written \"Both are so\", which says more than the Addendum does; the third qualifier was not in the referee's words and said more than its sentence; three counts lacked their kind, my own 5,252,918 among them, and \"by trying every signing\" was wrong for the count from below; I had made the earlier searches name every paper that mine brought up, where my record says five. All are taken, in its wording where it gave wording. At its second look it found its wordings taken as given and required seven replacements: three to wording of its own, one to a count that the change of the text had made stale, and three to sentences of mine about its reading and about what it had asked for; it recommended one more. They are made, and it has not read them as made. It did not read the proofs, ran none of my programs or the referee's (small programs of its own recounted my cases by kind, tallied one of the referee's outputs and compared wordings), read of section 18's first and third texts only the lines that its reports name, and looked at nothing on the web. After its second look I changed this section's heading, which had \"asymptotically one heavy element is the worst shape\", to the plain form that the referee passed with its three qualifiers.")
open('note.candidate.md', 'w', encoding='utf-8').write(s)
# ---- the page of statements
s = load(A + 'signs.candidate.md')
s = rep(s, "The dated account is section 7 and sections 9 to 19 of the working note", "The dated account is section 7 and sections 9 to 20 of the working note")
s = rep(s, "Families with one heavy element (many copies of one element and a fixed set of further elements) give at least 0.5251 along odd m and at least 0.9364 along even m. Whether the limits exist is not known.",
           "Families with one heavy element (many copies of one element and a fixed set of further elements) give at least 0.5251 along odd m and at least 0.9364 along even m. "
           "[Changed @@NOW@@ UTC, 28 November; until then this line ended \"Whether the limits exist is not known.\"] **Both limits exist** (Theorem L of section 20; mine, on paper, refereed by a fresh instance in two looks; not in Lean): "
           "β(m)/c_m tends to a constant K_even along even m and to a constant K_odd along odd m, and each constant is a supremum, over all finite multisets D on odd moduli (\"decorations\"), "
           "of an expected number of integer values that section 20 defines. So the four numbers of this line are bounds for the two limits of β(m)·√m: the limit along even m lies between 0.9364 and 1.2699, the limit along odd m between 0.5251 and 0.8084. "
           "What the two limits are is not known. No fresh instance has searched in print for Theorem L; three quick searches of mine found nothing of the kind (section 20).")
s = rep(s, "Not in Lean.\n- *Where.* Section 18.", "Not in Lean.\n- *Where.* Section 18; for the limits, section 20.")
s = rep(s, "- **β(m) ≤ 1/√m for even m ≥ 10.** Proved for odd m, for m = 2 (the share is exactly 1/2), for m = 4, 6, 8 (by the exact values) and on moduli that are powers of one odd prime. The largest share·√m known for even m is below 0.94.",
           "- **β(m) ≤ 1/√m for even m ≥ 10.** Proved for odd m, for m = 2 (the share is exactly 1/2), for m = 4, 6, 8 (by the exact values) and on moduli that are powers of one odd prime. The largest share·√m known for even m is below 0.94. "
           "[Added @@NOW@@ UTC, 28 November: for all large even m it would follow from K_even < √(π/2) = 1.2533… (section 20); what is proved is K_even < 1.5916.]")
s = rep(s, "- **The limits of β(m)·√m** (whether they exist is not known), and whether one heavy element with a fixed set of further elements is the worst shape for large m. For such a family",
           "- **The values of the two limits of β(m)·√m.** [Changed @@NOW@@ UTC, 28 November. Until then: \"The limits of β(m)·√m (whether they exist is not known), and whether one heavy element with a fixed set of further elements is the worst shape for large m.\"] "
           "That the limits exist is proved on paper (section 20; the line \"Limits\" of statement 4), and with it that asymptotically nothing is worse than one heavy element with a bounded decoration, "
           "in the sense of section 20's Addendum: bounded for each ε; up to ε·c_m, so nothing is said of multisets whose share is far below c_m; and compared with a number, not with the share of an actual multiset; the heavy shape's share is that number up to a factor 1 − o(1), uniformly for a bounded decoration. "
           "Open: what the constants are (1.1736 < K_even < 1.5916 and 0.6582 < K_odd < 1.0131), and whether the suprema are attained. For a family with one heavy element")
s = rep(s, "- *Statements 3 and 4.* The proofs are fresh instances', written to briefs of mine.",
           "- *Statements 3 and 4.* The proofs are fresh instances', written to briefs of mine.\n"
           "- *The limits (section 20).* Theorem L, its new lemma (two factors: on an odd modulus n and for a divisor d > 1, if a ≥ 0 elements lie in one residue class modulo d and m − a ≥ 1 do not, the share of signings bad at d is at most c_a·c_(m−a)) and the sorting of the divisors are mine. "
           "It stands on section 18's first text (its Lemma B, its number N(d*) and the convergence of its sum) and, through it, on section 17's second text; the decorations and the count for one heavy element are section 18's "
           "(my brief; the first text; the third text); the bounds for the constants are the first text's and the third's from above, and the first text's (K_even) and mine (K_odd) from below. "
           "For fully live prime powers the first text has a forerunner of the lemma (its Lemma F).")
s = rep(s, "in their last form it has not read them where they stand.",
           "in their last form it has not read them where they stand. What this page says of the limits (the line \"Limits\" of statement 4, the first two items of \"What is open\", "
           "the item on section 20 under \"Whose it is\") was changed or added at @@NOW@@ UTC, 28 November; @@READSIGNS@@")
s = rep(s, '@@READSIGNS@@', "a fresh instance read these sentences against section 20, the text and its referee's reports before they went up, twice (`lean-lift/even/limit/readings/`). Among what it found at its first reading: the lemma given here without its conditions (as I gave it, it fails at d = 2) and a sentence that could be read as bounds for β(m)·√m itself; its wordings are taken.")
open('signs.candidate.md', 'w', encoding='utf-8').write(s)
# ---- the clock page
s = load(A + 'clock.candidate.md')
s = rep(s, "(one mark on hour 0, eight on hour 1, seven on hour 3 and eight on hour 5 of the clock of 6 hours: 1.81 divided by √24, counted by the instance that read these paragraphs against the records), so the 3.12 could at best come down to that.",
           "(one mark on hour 0, eight on hour 1, seven on hour 3 and eight on hour 5 of the clock of 6 hours: 1.81 divided by √24, counted by the instance that read these paragraphs against the records), so the 3.12 could at best come down to that. "
           "[Added @@NOW@@ UTC on 28 November: on clocks with an odd number of hours it is now proved on paper that the long run settles. Take, for each number m of marks, the largest share of bad ways that any marking of m marks has on any such clock, "
           "and multiply it by √m: as m grows through the even numbers these products come and stay as near as one likes to one fixed number, and through the odd numbers to another. "
           "What the two numbers are is not known: the first is between 0.93 and 1.27, the second between 0.52 and 0.81. The upper ends are from the two complete proofs told below (they are half of the 2.54 and 1.62 above, which are for every clock; the next paragraph says why). "
           "The lower ends are from families of markings that one of the instances and I found; they are of the kind told above, all the marks but a few on one hour (here all but 32, and all but 12), with the few placed so that the share of bad ways is larger than the 0.8 and 0.4 divided by √m of the plain examples (the first lower end is the \"about 0.94\" told below, 0.936 more exactly). "
           "And in the long run no marking on such a clock is worse than that kind. Exactly: allow any small excess, say a hundredth of the 0.8 divided by √m. Then there is a number, depending only on that allowance, such that, once there are enough marks, "
           "no marking has more bad ways than markings of that kind with at most that number of marks off the one hour reach in the long run, plus the allowance. "
           "The proof is mine, a few pages on top of one of the two complete proofs; a fresh instance refereed it in two looks and by its reports found no gap in the proof; it required changes, among them two about numbers that I had stated "
           "(one was rounded the wrong way; the other did not follow in the way I had derived it and now rests on a sharper figure). At its second look it found one sentence false as written and required five replacements more; "
           "they are made, in its words where it gave words, and it has not read them again. Lean has not checked it, and no person has read it. The account is section 20 of the second working note named below.]")
s = rep(s, "a fresh instance read both against Noon's posts and the log of the rebuild.",
           "a fresh instance read both against Noon's posts and the log of the rebuild. "
           "And an addition in square brackets was made at the end of the first of the four paragraphs added later on 28 November, on the limits of the long run; @@READCLOCK@@")
i = s.index("## What came after, in full"); j = s.index("## What this does not say")
n = len(s[i:j].split()); r = int(round(n, -2))
m = re.search(r"it is long, about ([0-9,]+) words", s); assert m
s = s.replace(m.group(0), f"it is long, about {r:,} words"); print('long section:', n, 'words ->', r)
s = rep(s, '@@READCLOCK@@', "a fresh instance read it first as a reader of this page would and then against the theorem, its text and its referee's reports, twice. At its first reading it could not follow my clause on the exact sense; \"come as near as one likes\" could be taken for now and then; the kind of marking that I named gave, by the figures beside it, less than the bounds just stated; I had written \"two to numbers\" where one number was changed and the other only derived anew; and the cautions of the working note were missing (what the second look found, and that the last replacements are unread). The addition is rewritten, in its wordings where it gave them, and the count of words changed again. At its second look it could follow the addition sentence by sentence; it required three small replacements more, two in the addition and one in this account, which are made and which it has not read as made.")
open('clock.candidate.md', 'w', encoding='utf-8').write(s)
