"""The referee's second reading applied to the note: reads the text that make_note2.py writes (stdin) and the second report as saved
(note/referee-2.md), makes each change, and writes the note (stdout).  The referee's replacement wordings are cut from its report.
usage: make_note2.py READ-FILE LEAN-FILE | apply_second.py > note/README.md"""
import sys, re, json
s = sys.stdin.read()
t = open('note/referee-2.md').read(); rep_text = t[t.index('## Report (the referee)'):]
Q = [l[2:] for l in rep_text.split('\n') if l.startswith('> ')]
assert len(Q) == 5 and Q[0].startswith('a value from a theorem') and Q[2].startswith('For one of them, {2, 5, 50}') and Q[3].startswith('So the "least" column') and Q[4].startswith('It stays in the one group')
c100 = json.load(open('note/counts2-100.json')); c36 = json.load(open('note/counts2-36.json'))
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (s.count(old), old[:90])
    s = s.replace(old, new)
def between(a, b):
    i = rep_text.index(a) + len(a); return rep_text[i:rep_text.index(b, i)]

# ---- must 1: what "by theorem" is for the 55 patterns inside p^2 q or p q^2
a, b = Q[0].split('. In each of these 55 rows', 1)
rep("the least size by theorem where a theorem gives it (Theorem S for the 19 up-sets, the theorem for Z_{pⁿq} for 55 more patterns that use only the divisors of p²q or only those of pq²), whether the pattern is an up-set, and the bound of Corollary P. `make_tables2.py` stops if a value proved by a programme differs from the theorem's.",
    a + ", whether the pattern is an up-set, and the bound of Corollary P. In each of these 55 rows" + b + ". `make_tables2.py` stops if a smaller multiset turns up or if a value proved by a programme differs from the theorem's.")
assert c100['by_theorem_not_by_programme'] == [[[2, 5, 50], 50, 50]]
rep(" For one of them the theorem for Z_{pⁿq} gives the least size, and the smallest multiset found has that size.", " " + Q[2])
# ---- must 2
rep("from statements I had fixed before any proof of them existed (section 6).", "from statements I had fixed before any Lean proof of them was begun (section 6).")
rep("before any proof was begun; I had also checked", "before any Lean proof was begun; I had also checked")
# ---- must 3
m3 = between('Replacement: "My solver decided 248 and 172 of them, at', '".'); assert m3 == ' a minute a pattern except that eight of the 248 came from a second run that allowed 400 seconds;', m3
rep("My solver decided 248 and 172 of them in a minute each;", "My solver decided 248 and 172 of them, at" + m3)
# ---- must 4
rep('So the "least" column of the table as I first made it was not least in nine of the rows it did not mark proved; nothing contradicts', Q[3] + '; nothing contradicts')
# ---- must 5
rep("It stays in the one group Z_M, and uses neither Lemma A nor a second modulus.", Q[4])

# ---- suggestion 6: what a reader has to trust; what is not in Lean
s6 = between('Replacement for the parenthesis: "', '". Source: the audit')
rep("(they speak of a multiset as a function w : ZMod (pⁿq^m) → ℕ, of its mask polynomial Σ w(a)·X^a, and of two definitions, `IsUpSet` and `corners`, which are the only definitions of this file that a reader has to trust)", s6)
s6b = between('"Not in Lean": add at the front "', '".\n'); assert s6b == 'the corner formula of S1 (in Lean the corners are the maximal divisors outside D, by definition), Lemma A,'
rep("Not in Lean: Corollaries T and P,", "Not in Lean: " + s6b + " Corollaries T and P,")
# ---- suggestion 7: the proof in words
s7a = between('After "collect the summands by corner. ∎" add: "', '" I compiled this'); assert s7a == '(The other direction of Theorem S is (F1) alone: an order in D divides no corner.)'
rep("collect the summands by corner. ∎", "collect the summands by corner. ∎ " + s7a)
rep("*Claim:* for each k, a function A ≥ 0 that is N_k-periodic and has Â = 0 at every character whose order is in D is a sum of functions ≥ 0, each periodic",
    "*Claim:* for each k, a function A with values in ℕ that is N_k-periodic and has Â = 0 at every character whose order is in D is a sum of functions with values in ℕ, each periodic")
rep("(263 lines of lemmas: F1, F2, F3 and sums)", "(263 lines of lemmas: F1, F2, F3 and sums; the labels there and in my brief are not those of this section: there F2 is the uniqueness of the transform, and the lemma `dd_eq_zero`, which is (F2) here, is marked \"F1 and F2\")")
s7d = between('Replacement for the last clause: "', '" By search'); assert s7d.startswith('and then r^j·r′ and r^j·r″') and len(s7d) < 260
rep("and then r^j·p and r^j·p′, for two other primes p, p′ of M, are divisors of M that do not divide N and do not divide each other.", s7d)
# ---- suggestion 8
s8 = between('reads as if Mathlib were rebuilt. Your log and Noon\'s both say Mathlib\'s built files were shared. Replacement: "', '". The count of 79')
rep("a fresh copy of the 85 files of the shared folder was rebuilt from nothing: 18,453 jobs, no error", s8)
# ---- suggestion 9 (my wording, from what the referee found; it goes back to the referee)
rep("I had also checked by evaluation in Lean that the sum of M/c over `corners` equals the least size my solver had proved on the 34 up-sets it had decided in Z_36 and Z_100 (`lean/CheckUpsetTable.lean`).",
    "I had also checked by evaluation in Lean that the sum of M/c over `corners` equals the least size my solver had proved on the 34 up-sets it had decided in Z_36 and Z_100 (`lean/CheckUpsetTable.lean`; that file's hash is in the same list, but the only run of it kept on file is the one on the finished library, in the build log).")
rep("and `#print axioms` gives `[propext, Classical.choice, Quot.sound]` for each of the three theorems (`lean/lean-upset-private-build.log`).",
    "and `#print axioms` gives `[propext, Classical.choice, Quot.sound]` for each of the three theorems. Of these checks `lean/lean-upset-private-build.log` holds the rebuild, the axioms, the comparison of the printed statements, the table and the line counts; the comparison character for character and the search for `sorry` and the rest were run by me without a log, and were done again by Noon (the first; its post on my board at 15:51 UTC), by the audit (the second) and by the referee (both).")
# ---- suggestion 10
rep("and tested the three statements, translated from the Lean text, by exhaustive search in 22 small groups", "and tested the three statements, translated from the Lean text, by exhaustive search up to a size for each pattern in 22 small groups")
rep("Its remarks: the hypothesis p ≠ q is not needed", "Among its remarks: the hypothesis p ≠ q is not needed")
# ---- suggestion 11 (mine, from the referee's figures and files)
assert c36['decided_only_HiGHS'] == 1 and c100['decided_only_HiGHS'] == 68
rep("the least size is now known for 256 and 240 of the 256 patterns.", "the least size is now known for 256 and 240 of the 256 patterns (for one pattern of Z_36 and 68 of Z_100 on the word of the solver HiGHS alone, whose proofs that nothing smaller exists are in floating point).")
rep("their rows give the smallest size found, which in four of them is the referee's programme's and smaller than my solver's (or my solver had none).",
    "their rows give the smallest size found, which in four of them is the referee's programme's and smaller than my solver's (or my solver had none). In its second reading the referee settled three of the sixteen with CP-SAT, in exact integers and one size at a time, the size having to be a multiple of the prime powers that the pattern forces: no smaller admissible size has a multiset for {2, 4, 5, 100} (60), {2, 4, 5, 50, 100} (100) or {2, 5, 50, 100} (70) (`referee/second/out/sizes-*.jsonl`). The tables do not yet count these three as proved.")
# ---- suggestion 12: one parenthesis in section 1
rep("which gives the 248 of sections 3 and 4.) (The parenthesis before this one is the referee's wording; the 248 it speaks of is now in \"In short\" and in section 4. My board post of 13:47",
    "which gives the 248 of \"In short\" and section 4. This much is the referee's wording. My board post of 13:47")
# ---- suggestions 13, 14, 15
rep("is in square brackets or headed as the referee's, and is dated 26 November 2026; I have read each of them", "is in square brackets or headed as the referee's; all are of 26 November 2026; I have read each of them")
rep("(each below one term of the corner sum)", "(each at most one term of the corner sum)")
rep("It says it read S1 to S3 line by line, and it reports on each step of S4 and S5.", "It read S1 to S6 line by line.")
# ---- suggestion 16: the referee's own proof of Corollary T, last clause as it now words it
s16 = between('Replacement from "since for a prime p": "', '"\n'); assert s16.startswith('since for a prime r in which s has a higher exponent than c') and s16.endswith('∎') and len(s16) < 260, s16
i = s.index("*Proof (added by the referee, 26 November 2026; the instance gave none).*"); j = s.index("since for a prime p in which s has a higher exponent than c", i); k = s.index("∎", j) + 1
s = s[:j] + s16 + s[k:]
# ---- suggestion 17 (mine, from the referee's report and files)
rep("with D empty there is nothing to fail).", "with D empty there is nothing to fail). My multisets are sums of cosets, for which the conclusion holds by construction; the referee ran the induction with a program of its own on 1,346 multisets not built from cosets, in 15 groups, four of them with p = q: every step held, and with one point added 375 of 375 failed (`referee/second/peel.py`).")
# ---- suggestion 18: small things
rep("hash on my board at 11:06 UTC)", "hash on my board, the file `hello-from-agent3.md` at the top of the commons, at 11:06 UTC)")
rep("added with Noon's word after Noon had read the statements (my board, 15:51 UTC)", "added with the word of Noon, another instance on this machine, who keeps that library, after Noon had read the statements (my board, 15:51 UTC)")
rep("Proposition 5.1 and, under (T2), Theorem 9.4", "Proposition 5.1 and, under the Coven–Meyerowitz condition (T2), Theorem 9.4")
rep("in the referee's files the paths under `/home/agent3/pq2/` are this folder.", "in the referee's files `/home/agent3/pq2/referee/two-powers/` is `referee/` here, `/home/agent3/pq2/note/` is this folder itself, and other paths under `/home/agent3/pq2/` are this folder; in `lean/SHA256-as-fixed` the name `Upset.lean` means the file kept here as `lean/Upset.as-fixed-before-proof.lean`. Two of the files in `out2/` also hold lines printed by the solver that are not JSON.")
rep("`referee.md` (my brief to the referee and its report), `referee/` (its programs and outputs)", "`referee.md` (my brief to the referee and its report), `referee-2.md` (its second reading, of the changed text), `referee/` (its programs and outputs; `referee/second/` for the second reading)")
sys.stdout.write(s)
