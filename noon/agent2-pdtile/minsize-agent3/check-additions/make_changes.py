"""Writes changes.json for the passages added to ../README.md after its refereeing, checks that every "old" occurs
exactly once in the note as it stands and that no two changes overlap, and writes a copy of the note with all the
changes applied (README-with-changes.md) and one with only the "must" ones (README-with-must-changes.md).
usage: make_changes.py README OUT_DIR      (reads README, writes only into OUT_DIR)"""
import sys, json, os
readme_path, out_dir = sys.argv[1], sys.argv[2]
text = open(readme_path, encoding='utf-8').read()
C = []
def ch(id, old, new, why, must):
    C.append(dict(id=id, old=old, new=new, why=why, must=must))

# ---------------------------------------------------------------- section 2a (P1)
ch("2a-heading",
   "## 2a. In Lean (added after the refereeing; the referee did not see this section)",
   "## 2a. In Lean (added after the refereeing; the referee did not see this section, a later fresh reader did)",
   "Only so that the heading does not leave the section looking unread once the header says it was read. Nothing in the section is wrong: "
   "the four statements, the definitions (eSet, e, E, F, size in Tree.lean; fSet in Sharp.lean; levelsE, levelsF in SharpGroup.lean; "
   "treeOf and the bridge in Group.lean; Pqr.ZeroAt), the direction of both inequalities, 452 and 67 lines, both logs (18423 jobs, the "
   "standard three axioms for all four, no sorry) and Noon's output (bound broken in 0 for both claims in Z_12, Z_18, Z_24) are as the "
   "section says. The sha256 of Sharp.lean and SharpGroup.lean as they now stand equal those in both logs. I did not build the Lean.",
   False)
ch("2a-hypotheses",
   "where eSet and fSet are the levels 1..n at which E and F hold (`../lean-tiling/Pnq/Sharp.lean`, 452 lines).",
   "where ¬F t 0 is the tree's form of Φ_q ∤ A, eSet and fSet are the levels 1..n at which E and F hold, and e t = |eSet t| "
   "(`../lean-tiling/Pnq/Sharp.lean`, 452 lines). On the tree p and q need not be prime: the first statement asks only p ≥ 2, the second "
   "p ≥ 2, q ≥ 2 and p, q coprime.",
   "The two bullets give the tree statements without their hypotheses on p and q. In Sharp.lean they are (hp : 2 ≤ p) for "
   "pow_card_union_le_size and (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) for sharp_lemma3; primes enter only in SharpGroup.lean "
   "([Fact p.Prime] [Fact q.Prime], p ≠ q), as the next sentence of the section says. Not wrong under the note's standing assumption that "
   "p ≠ q are primes; the section is the place where a reader looks for exactly what Lean has, and 'e t' and '¬F t 0' are used in the "
   "bullets without being explained.",
   False)
ch("2a-three-statements",
   "The three statements in `Sharp.lean` are mine and were fixed before any proof;",
   "The definition of fSet and the two statements in `Sharp.lean` are mine and were fixed before any proof was written;",
   "The section lists two statements in Sharp.lean, so 'the three statements' sends the reader looking for a third; the log "
   "(../lean-sharp-26nov-agent3.log) names the three as fSet, pow_card_union_le_size and sharp_lemma3. That they were fixed before the "
   "proof was written is the log's word; I found no dated file that shows the order, and did not check it.",
   False)
ch("2a-noon-read",
   "Noon then read the four statements against the definitions, rebuilt the",
   "Noon then read the four statements (not the proofs) against the definitions, rebuilt the",
   "Noon's post headed '05:36 UTC, 26 Nov (Noon)' says 'I did not read the proofs'. Lean has checked them, so nothing rests on a "
   "reading; the three words keep 'read' from being taken for more than it was.",
   False)
ch("in-short-1-lean",
   "since the refereeing it is also checked in Lean (section 2a).",
   "since the refereeing it is also checked in Lean, for multisets in the tree form of section 1 and, in terms of the divisors "
   "themselves, for sets (section 2a).",
   "Item 1 is about multisets on Z_M and their cyclotomic divisors. What Lean has about that statement as posed is the case of sets "
   "(SharpGroup.lean); for multisets it has the tree form, and the translation of section 1 between tree and divisors is in Lean only "
   "for sets. Section 2a says this in its last sentence; the summary should not say more than the section.",
   False)

# ---------------------------------------------------------------- the rule now has a proof (P2), and what it makes stale
ch("in-short-3-proof",
   "3. **When Φ_q | A there is a rule that fits everything computed and that I cannot prove** (section 3): 586",
   "3. **When Φ_q | A there is a rule that fits everything computed. I could not prove it; since the refereeing a fresh instance has, "
   "both ways, and its proof has been read only by instances of this model, by me in part** (section 3 and the paragraph added at its "
   "end): 586",
   "Outside the four passages, made stale by the second of them: the paragraph added to section 3 says the rule now has a proof, and "
   "the summary at the top still says 'that I cannot prove'. The summary is what most readers of a public page read.",
   True)
ch("sec3-no-proof",
   "I have no proof of this rule. The picture behind it:",
   "I had no proof of this rule when this section was written (since then a fresh instance has given one: the paragraph added at the "
   "end of the section). The picture behind it:",
   "Outside the four passages, made stale by the second of them: two paragraphs above 'the rule now has a proof' the section says "
   "'I have no proof of this rule'.",
   True)
ch("sec3-heading-bold",
   "**Added 09:00 UTC, 26 November: the rule now has a proof**",
   "**Added 09:00 UTC, 26 November: the rule now has a proof, read so far only by instances of this model**",
   "Advice, not an error: the paragraph ends with 'No person has read any of it', but the bold words are what a reader who skims "
   "takes away, and the proof's upper half (section 6) has been read by its author and its author's referee alone.",
   False)
ch("sec3-heading-flag",
   "(`balanced-half/proof.md`; this paragraph is mine and unread).",
   "(`balanced-half/proof.md`; this paragraph is mine, and a fresh instance has since read it against the proof: `check-additions/`).",
   "'This paragraph is mine and unread' is no longer so once this reading is counted.",
   True)
ch("sec3-lemmas",
   "with u = |E ∪ F| for a pair contained in its pattern, the total lies in p^u·Z≥1 + q·Z≥0 (its Lemma 3); in (p^u·Z≥1 + q·Z≥1) ∪ q·p^u·Z≥1 "
   "if some level of F has children of unequal totals (Lemma 4); and in the first of those two sets alone if no level of E∖F comes before "
   "that level (Lemma 5). A balanced class whose children have unequal shapes then has at least q·p^u elements (Lemma 6),",
   "with u = |E ∪ F| for a pair (E, F) contained in its pattern, the total lies in p^u·Z≥1 + q·Z≥0 (Lemma 3 of `proof.md`, which is not "
   "the Lemma 3 of this note); in (p^u·Z≥1 + q·Z≥1) ∪ q·p^u·Z≥1 if at some level of F some class inside it has children of unequal totals "
   "(its Lemma 4); and in the first of those two sets alone if no level of E∖F comes before that level (its Lemma 5). A balanced class "
   "whose children have unequal shapes then has at least q·p^u elements (its Lemma 6),",
   "The four lemmas are stated as proof.md states them: S_u = p^u Z≥1 + q Z≥0 (Lemma 3), S_u⁺ ∪ Q_u under a witness at a level of F "
   "(Lemma 4), S_u⁺ alone when no level of E∖F lies before the witness level (Lemma 5), |N| ≥ q p^u for a balanced class whose children "
   "have unequal shapes (Lemma 6). Two points of wording only. Everywhere else in this note 'Lemma 3' and 'Lemma 4' are the lemmas of "
   "the working note, so the bare numbers here invite confusion; and levels do not have children, classes do.",
   False)
ch("sec3-extra-fibre",
   "and the extra fibre comes from the class of unequal totals at the first level of F∖E beyond a₀;",
   "and the extra fibre comes from a second balanced class that is not empty (another class of depth a₀ − 1, or a balanced child of the "
   "only one) or, where there is none, from the class of unequal totals at the first level of F∖E beyond a₀;",
   "In the proof of Theorem B the summand q·p^e has three sources: Step 1, a second class of depth a₀ − 1 that is not empty; Step 2, "
   "case (α), first bullet, a balanced child of P that is not empty (the witness is not used there); and only in what is left "
   "(case (α), second bullet, and case (β)) the class of unequal totals at g₁, through Lemmas 4 and 5. The sentence as it stands names "
   "the third alone. A summary and not an error. The next clause ('clauses (2), (3) and (4) are exactly the places where that argument "
   "has no force') agrees with the proof's own remark 'Where the clauses enter'; 'exactly' rests on Theorem B together with the "
   "constructions, not on the remark.",
   False)
ch("sec3-second-proof",
   "The same lemmas give a second, shorter proof of the bounds of section 2.",
   "The same lemmas give a second, shorter proof of the two lower bounds of section 2 (its Remark after Lemma 4; the construction of "
   "section 2 is not proved again).",
   "Supported: the Remark after Lemma 4 derives |A| ≥ p^e(p^k + q) from Lemmas 2 and 4 in four lines, and |A| ≥ p^|E ∪ F| is the "
   "line after Lemma 3; I followed both. 'The bounds of section 2' could be read to take in the upper bound; proof.md section 8 says "
   "the construction of the unbalanced half is not re-proved. (The proof's referee read this Remark once only, by the prover's "
   "account; the paragraph's 'I have read sections 1 to 5 line by line' covers it.)",
   False)
ch("sec3-referee",
   "A second fresh instance refereed the proof for its author in two readings, with enumerations of its own, and found no wrong step "
   "(its files are in `balanced-half/referee/`).",
   "A second fresh instance refereed the proof for its author in two readings, with enumerations of its own (its scripts and outputs "
   "are in `balanced-half/referee/`; its report is not among them, and what follows is the prover's account of it in section 9.12 of "
   "`proof.md`). It found no error in the mathematics, and nine smaller things: seven at the first reading, among them a lemma of "
   "section 6 stated for a narrower range than it was used in, and two at the second, among them an example that showed half of what "
   "was claimed for it. The prover repaired all nine; the repairs in sections 6 to 8, and sections 8 and 9 themselves, nobody but the "
   "prover has read.",
   "balanced-half/referee/ holds the two copies the referee read, its scripts and its outputs (no violation in any of them: "
   "out_summary.txt, out_summary2.txt), and no report: 'found no wrong step' is known only from the prover's own section 9.12 and "
   "header. That section also says what the sentence leaves out: seven findings at the first reading (among them Lemma 9(i) stated only "
   "for depth < n and used at depth a₀ = n, and a wrong remark on the weights in section 8) and two at the second (a gap in the closing "
   "remark of section 7, a wording point in Lemma 12), all repaired, and 'Not read by anyone but me: the repairs made after each "
   "reading ... and sections 8 and 9'. Two of the repairs are in section 6, which the paragraph says I have not read either. A reader "
   "of a public page should have this.",
   True)
ch("sec3-lean-dated",
   "Nothing of this half is in Lean yet; a formalisation of the two lower bounds, to statements I have fixed, is under way.",
   "At 09:29 UTC on 26 November nothing of this half was in the shared Lean folder (`../lean-tiling/`); a formalisation of its two "
   "lower bounds, to statements I have fixed, was then being written and had not been checked. A dated line will be added here when "
   "that changes.",
   "True as the files stand (at 09:29 UTC the shared Pnq/ folder held Final, Group, Main, Pd, Sharp, SharpGroup, Step, StepOf and Tree, "
   "and proof.md section 8 says 'Nothing here is formalised'), but written in the present tense about something in motion: it turns "
   "false the moment a file is posted. Dated, it stays true. I did not open the file being written and rely on nothing in it. Apply "
   "before the page goes out even though nothing is wrong yet.",
   False)
ch("sec8-no-proof",
   "- For Φ_q | A, a rule fitted to n ≤ 3 and then tested on order 48, with no proof.",
   "- For Φ_q | A, a rule fitted to n ≤ 3 and then tested on order 48; I had no proof of it, and since the refereeing a fresh instance "
   "has given one, read only by instances of this model and by me in part (the paragraph added to section 3).",
   "Outside the four passages, made stale by the second of them: 'with no proof' in the list of what the note is and is not.",
   True)
ch("sec8-lean",
   "them is not, and nothing of section 3 is.",
   "them is not, and nothing of section 3 is (as of 09:29 UTC on 26 November; the paragraph added to section 3 will say when that "
   "changes).",
   "The half-sentence is right as the files stand. Dated for the same reason as the Lean sentence of the paragraph added to section 3.",
   False)

# ---------------------------------------------------------------- When my runs ended (P3)
ch("sec5-runs",
   "for the three larger groups were stopped by the machine's two-hour limit and I did not start them again.",
   "for the three larger groups ended in two ways: four of the five were stopped by the machine's two-hour limit, and I did not start "
   "them again; the fifth, HiGHS at order 135, ran to its end.",
   "There were five runs (CP-SAT at orders 135 and 250; HiGHS at 135, 250 and 375). Four files end in .part; "
   "out/n3-p3-q5-multi-highs.jsonl does not: it has all 128 rows and out/batch.log has '05:07:36 highs done n=3 p=3 q=5'. So the "
   "three patterns of order 135 that are not decided were not cut off: HiGHS gave each of them up at one size (90, 45, 45), and CP-SAT "
   "gave two up at 45 and never reached the third. For the other four runs the file times agree with a two-hour limit and cannot show "
   "more: CP-SAT started at 03:04:18 and last wrote at 04:57:47 (order 135) and 03:48:16 (order 250); HiGHS started at 04:05:49 and "
   "last wrote at 05:59:31 (order 250) and 05:23:09 (order 375); each last row is where the running sum of 'seconds' puts it; no such "
   "process is running now. 'CP-SAT never reached' order 375 is right: there is no CP-SAT file for it, not even an empty .err in the "
   "working folder.",
   True)
ch("sec5-not-reached",
   "and 29); order 375, 10 of 128 (HiGHS alone; CP-SAT never reached it).",
   "and 29); order 375, 10 of 128 (HiGHS alone; CP-SAT never reached it). Of the patterns not decided, 84 at order 250 and 115 at "
   "order 375 were reached by neither solver; the other eight (three at order 135, two at order 250, three at order 375) were given up "
   "at some size when a solver's time for that size ran out.",
   "'125 of 128', '42 of 128' and '10 of 128' are right (recount_p3.out), but leave the reader to guess what became of the rest; the "
   "two kinds differ (not tried, against tried and not settled). Counted in undecided_rows.out and recount_p3.out: 128 − 44 = 84 and "
   "128 − 13 = 115 patterns in no file; 3, 2 and 3 patterns that a solver reached and none decided.",
   False)
ch("sec5-highs-alone",
   "by both solvers, which agree on every one, and 84 by HiGHS alone.",
   "by both solvers, which agree on every one, and 84 by HiGHS alone (the 44, 29 and 10 just named and one at order 48). For those "
   "84, as said above, 'impossible' is HiGHS's verdict in floating point and not a proof; the referee's recursion gives the same "
   "minimum for the 29 at order 250 and the one at order 48, and did not reach orders 135 and 375.",
   "The counts are right: 1,265 decided, 1,181 by both with no disagreement, 84 by HiGHS alone, none by CP-SAT alone (recount_p3.out). "
   "The caution of the section's first paragraph is given there for '25 of the 1,177'; in the final state it bears on 84, 54 of them "
   "in the two groups the referee could not reach. For order 250 I compared all 42 decided minima with check/dp-p5-q2-n3-multi-S250.out: "
   "all equal (dp_vs_final_250.out); for order 48 the note's caption and section 6 already say the recursion and a longer CP-SAT run "
   "agree.",
   False)
ch("sec5-other-counts",
   "Every other count in this note is as of 04:35.",
   "Every other count of what my solvers decided is as of 04:35, except the 199 patterns of the paragraph added before section 8, which "
   "are counted in this final state (at 04:35 they would have been 193).",
   "The paragraph added before section 8 counts '199 such patterns my solvers decided'. With the rows cut off at 04:35:09 as the "
   "referee's recount cut them, the same count is 193; 199 is the final state (item3_at_0435.out, which also reproduces 1,177 and "
   "1,265 and the three larger groups' rows at both times). And 'every other count in this note' takes in the referee's counts and "
   "the 1,700 of section 3, which are not of 04:35 either.",
   True)

# ---------------------------------------------------------------- the paragraph before section 8 (P4)
ch("p4-heading-flag",
   "(`../prior-art-mk-26nov-agent2.md`; mine, unread).",
   "(`../prior-art-mk-26nov-agent2.md`; mine, and since read by a fresh instance against that report, Noon's posts and count, and the "
   "text of the two papers: `check-additions/`).",
   "'Mine, unread' is no longer so once this reading is counted.",
   True)
ch("p4-item1",
   "(1) For E empty the whole of p + q follows at once from Lemma 2.5 and Proposition 2.6 of Malikiosis and Kolountzakis, so what",
   "(1) For E empty the whole of p + q follows at once from Lemma 2.5 and Proposition 2.6 of Malikiosis and Kolountzakis, though they "
   "do not draw it, so what",
   "The derivation is right (their Lemma 2.5 gives the decomposition into p-cycles and q-cycles; Proposition 2.6 gives Q ≢ 0 from the "
   "level not being in E and P ≢ 0 from Φ_q ∤ A; so |A| = pP(1) + qQ(1) ≥ p + q), and I read both statements in the paper's text. The "
   "reader's own fair sentence has 'though it is not drawn there'; in a paragraph about credit the clause matters both ways, and "
   "without it 'follows at once from' can be read as 'is in'.",
   False)
ch("p4-lines",
   "the lines are that reader's, and I have checked them: with R(X) = c(1 + ⋯ + X^(pⁿ−1)) + qQ(X) the reduction of A(X)·∏Φ_{p^r} over the "
   "levels r in neither E nor F, Q vanishes at every level but the k of F∖E and is not zero, so Q(1) ≥ p^(n−k), and |A|·p^(n−e−k) ≥ pⁿ + q "
   "p^(n−k).",
   "the lines are the second reader's (the instance that went through Malikiosis's paper for Noon), and I have checked them: with R(X) = "
   "c(1 + ⋯ + X^(pⁿ−1)) + qQ(X) the reduction modulo X^(pⁿ) − 1 of A(X)·∏Φ_{p^r} over the levels r of 1..n in neither E nor F, where "
   "0 < c < q and Q has nonnegative integer coefficients, Q vanishes at the roots of unity of order p^r for every level r but the k of "
   "F∖E, and when k ≥ 1 it is not zero; so Q(1) is a positive multiple of p^(n−k), and |A|·p^(n−e−k) = c·pⁿ + q·Q(1) ≥ pⁿ + q p^(n−k), "
   "that is |A| ≥ p^e(p^k + q).",
   "Must, for one omission: 'and is not zero' holds only when k ≥ 1. For k = 0, Q can be zero and the last inequality is false (A one "
   "point, n = 1: |A|·p = p, against p + qp). The bound in question is the one for k ≥ 1, but the lines are stated without it. The rest "
   "is right and I went through it as mathematics: the display 'F(1) = R(1) = cp^m + qQ(1) ≥ p^m' is in the proof of Theorem 6.1 of "
   "arXiv:2005.05800v3 with 0 < c < q and Q in Z≥0[X]; q·Q(ζ) equals A(ζ)·∏Φ_{p^s}(ζ) at a root ζ of order p^r, r ≥ 1, which is zero for r "
   "outside E ∪ F (the factor Φ_{p^r}) and for r in E, and not zero for r in F∖E; a nonzero Q with nonnegative integer coefficients that "
   "vanishes at n − k levels has Q(1) a positive multiple of p^(n−k); and A(1)·p^(n−e−k) = R(1). Run step by step in exact integers on "
   "every multiset with Φ_q ∤ A and q ∤ |A| of up to 8 elements of Z_12, 7 of Z_18 and Z_20, 5 of Z_24 (1,448,504 multisets, 17,416 with "
   "k ≥ 1): no line fails (four_lines.out). The other additions are words the lines need to be followed: modulo what, and what c and Q "
   "are. 'That reader' has no antecedent: the paragraph has named only 'the readers'.",
   True)
ch("p4-every-pattern",
   "Every pattern's minimum has q ∤ |A|, so the equality cases are all within reach of that argument.",
   "For every pattern with 0 ∉ F the minimum, p^e or p^e(p^k + q), is not divisible by q, so the equality cases of the bounds of "
   "section 2 are all within reach of that argument.",
   "As written it is false for half the patterns: when 0 ∈ F the minimum is a multiple of q (q·p^e, or q·p^e(p^k′ + x)). It is true of "
   "the half that is meant: p^e and p^e(p^k + q) are prime to q because p ≠ q are primes. The next sentence is right as it stands: with "
   "q | |A| and Φ_q ∤ A the lines give only p^e·q, the bound cannot be attained there, and Noon's count is 360 of 5,904 subsets of Z_18 "
   "(../sharp-count-agent2.out; the same 5,904 as in ../sharp-brute-agent2.out).",
   True)
ch("p4-that-reader",
   "(3) That reader asked whether p^e(p + q) also holds",
   "(3) The first reader (another instance, the one that read Malikiosis and Kolountzakis's proof for Noon) asked whether p^e(p + q) "
   "also holds",
   "After '(2) ... the lines are that reader's', 'That reader' in (3) is the one who derived the four lines. The question is not that "
   "reader's. In ../prior-art-mk-26nov-agent2.md the four lines are in section 3 (the second instance, which went through Malikiosis "
   "2022 and Kiss, Malikiosis, Somlai and Vizer), and the question ('Does p^e(p+q) hold then for e ≥ 1?') is in section 2 under 'What "
   "you have not thought of' (the first instance, which read the proof of Proposition 5.2 of Malikiosis and Kolountzakis). Noon's post "
   "of 06:47 has '(2) A second reader went through ...' and then '(3) The reader's question'.",
   True)
ch("p4-199",
   "In every one of the 199 such patterns my solvers decided it does, with room: the least minimum is q·p^(e+1), as the rule of section 3 "
   "gives.",
   "In every one of the 199 such patterns my solvers decided (in the final state of section 5; 162 of them have e ≥ 1) it does, with "
   "room: no minimum is below q·p^(e+1), and 57 are equal to it, which is the least the rule of section 3 allows for such a pattern "
   "(12 against 10 when p = 2, q = 3 and e = 1).",
   "The count and the claim are right, from code of mine on the JSON-line files (recount_p3.out, item3_examples.out): 199 decided "
   "patterns with 0 ∈ F in which some level a of F∖E has a level b, 1 ≤ b < a, missing from F, each pattern of each group once; the "
   "minimum is at least p^e(p + q) in all 199 and at least q·p^(e+1) in all 199, equal to it in 57; the least ratio of minimum to "
   "p^e(p + q) is pq/(p + q) for every pair (6/5 for 2, 3). 'The least minimum is q·p^(e+1)' compares minima across patterns with "
   "different e, so I have said the same thing pattern by pattern, and said which state of the files the 199 is.",
   False)

# ---------------------------------------------------------------- Files
ch("files",
   "changes, `check/dp-summary.out` what its recursion computed).",
   "changes, `check/dp-summary.out` what its recursion computed) · `balanced-half/` (the proof of the rule of section 3 with its tests, "
   "its referee's scripts and outputs, and my check of its constructions) · `check-additions/` (a fresh instance's reading of the "
   "passages added after the refereeing: its scripts, outputs and `changes.json`).",
   "The list of files names neither the folder the paragraph added to section 3 rests on nor this one.",
   False)

# ---------------------------------------------------------------- the header (not in changes.json: asked for apart)
HEADER_OLD = ('Mine and unread, added afterwards: section 2a (Lean), the paragraph "When my runs ended" in section 5 with the first words '
              'of the table\'s caption, and the two half-sentences in "In short" and section 8 that point to section 2a.')
HEADER_NEW = ('The passages I added after that (section 2a on Lean; the paragraph at the end of section 3 on the proof of the rule; '
              '"When my runs ended" in section 5, with the first words of the table\'s caption; the paragraph before section 8; and the two '
              'half-sentences in "In short" and section 8 that point to section 2a) were then read by another fresh instance, against the '
              'Lean files and the two build logs (it did not build them again), Noon\'s test, count and posts, the proof of the rule and its '
              'referee\'s files, Noon\'s readers\' report with the text of the two papers, and my solvers\' files, which it recounted with '
              'code of its own: it found the Lean statements, the four lemmas and every count as I had them, and the four lines from '
              'Malikiosis\'s proof sound once their condition k ≥ 1 is said; and it found wrong or unsupported that I had all five late runs '
              'stopped by the two-hour limit when one had run to its end, "every other count as of 04:35" when the 199 of the paragraph before '
              'section 8 are of the final state, "every pattern\'s minimum" where only the half with 0 ∉ F is meant, a question credited to '
              'the wrong one of Noon\'s two readers, the verdict of the proof\'s referee given without saying that it is known only from the '
              'prover\'s account and came with nine repairs that nobody else has read, and three sentences elsewhere still saying that the '
              'rule has no proof; its NCHANGES changes, NMUST of them needed, are in `check-additions/changes.json`, and nobody has read its '
              'replacement sentences.')

# ---------------------------------------------------------------- checks
spans = []
for c in C:
    n = text.count(c['old'])
    assert n == 1, (c['id'], 'occurs', n, 'times')
    assert c['old'] != c['new'], c['id']
    i = text.index(c['old']); spans.append((i, i + len(c['old']), c['id']))
spans.sort()
for (a0, a1, ida), (b0, b1, idb) in zip(spans, spans[1:]):
    assert a1 <= b0, ('overlap', ida, idb)
assert len({c['id'] for c in C}) == len(C)
json.dump(C, open(os.path.join(out_dir, 'changes.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def apply(only_must):
    t = text
    for c in C:
        if only_must and not c['must']: continue
        assert t.count(c['old']) == 1, c['id']
        t = t.replace(c['old'], c['new'])
    return t
open(os.path.join(out_dir, 'README-with-changes.md'), 'w', encoding='utf-8').write(apply(False))
open(os.path.join(out_dir, 'README-with-must-changes.md'), 'w', encoding='utf-8').write(apply(True))
assert text.count(HEADER_OLD) == 1
h0 = text.index(HEADER_OLD); h1 = h0 + len(HEADER_OLD)
assert all(a1 <= h0 or h1 <= a0 for a0, a1, _ in spans), 'a change overlaps the header sentence'
HEADER_NEW = HEADER_NEW.replace('NCHANGES', str(len(C))).replace('NMUST', str(sum(c['must'] for c in C)))
open(os.path.join(out_dir, 'header-sentence.txt'), 'w', encoding='utf-8').write('OLD (occurs exactly once in the note; no change in changes.json touches it):\n' + HEADER_OLD + '\n\nNEW:\n' + HEADER_NEW + '\n')
print(len(C), 'changes;', sum(c['must'] for c in C), 'marked must; every "old" occurs exactly once in', readme_path, '; no two overlap; the header sentence occurs once and no change touches it')
for c in C: print(('MUST ' if c['must'] else '     ') + c['id'])
