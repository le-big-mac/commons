"""Writes changes.json for section-3a.md and pointers-3a.md, after checking that every "old" stands exactly once
in its file and that no two overlap; also writes the two files as they would read with every change in
(section-3a.after.md, pointers-3a.after.md) and with the needed ones only (section-3a.must-only.md).
usage: make_changes.py DIR_WITH_THE_TWO_FILES OUT_DIR"""
import sys, json
src, out = sys.argv[1], sys.argv[2]
S, P = 'section-3a.md', 'pointers-3a.md'
C = []
def ch(file, must, old, new, why):
    C.append({'file': file, 'must': must, 'old': old, 'new': new, 'why': why})

# ---------------------------------------------------------------- section-3a.md, needed
ch(S, True,
   "The first three follow section 2 and section 6 of `balanced-half/proof.md`, re-described as recursive builders of trees, with small changes of convenience that their authors reported (which layer a string's element sits in when E∖F is empty; the vectors used in two of the modes; any level of E before a₀ as host in case (III)).",
   "The first two follow the proofs on paper (section 2 of this note; section 6 of `balanced-half/proof.md`), re-described as recursive builders of trees, with small changes of convenience that their authors reported: when E∖F is empty the first puts A₁ in layer 1, not layer 0 (the header of `BuildU.lean` says so); the second uses other vectors in two of that proof's three \"modes\" when q ≥ 3 (`wv` in `BuildB4.lean`), and for the \"host level\" of its case (III) takes any level of E before a₀, where the proof takes the least. In case (V) too it takes any level that qualifies, not the least (`BuildB.lean`; the reader of this section found that). The reports are not on file, and the comments in the files name only the first of these as a change. The third redoes for multisets, with a weight in place of membership, the bridge that the shared folder has for sets, and proves that on a set the two agree.",
   "\"The first three\" takes in the bridge (`Weighted.lean`), which builds no tree and follows neither section; its own header says what it follows. \"section 2 and section 6 of `balanced-half/proof.md`\" reads as two sections of that file, whose section 2 is \"Two elementary lemmas\"; the construction for Φ_q ∤ A follows section 2 of the note. Against the files: the change of layer is in the header of `BuildU.lean`; the change of vectors is real but no comment calls it a change (`wv` in `BuildB4.lean` against section 6.2: for τ = 1 and q ≥ 3 the paper has 1 + e₁ − e₂, Lean 1 + e₀ − e₂; mode U is as on paper); case (III) takes any b ∈ Es with b < a0 (`BuildB.lean` line 62) where the paper has b = min E. One more of the same kind is not in the list: case (V), where the paper says \"Let b be the least such level\" and `BuildB.lean` (line 83) takes whatever b the hypothesis supplies. \"string\", \"mode\", \"host\" and \"case (III)\" are terms of `proof.md` that the note does not explain. The four reports are not on disk, so \"reported\" rests on the author's word; the replacement says so.")

ch(S, True,
   "I fixed every definition and every statement first, in files that compiled with the proofs left open (`lean-min/statements-as-fixed/`),",
   "I fixed twelve definitions and eighteen statements first, in files that compiled with the proofs left open (`lean-min/statements-as-fixed/`; the other 28 definitions and 144 lemmas of the finished files are their authors' own and serve only the proofs),",
   "The eleven files hold 40 definitions (four of them structures) and 162 theorems; `CheckMin.lean` and `check_fixed.py` fix 12 and 18 of them. Rule 3 of the rules let the instances add definitions and lemmas of their own, and they did. \"Every definition and every statement\" says more than was fixed. (I recompiled the files as fixed in one scratch file: they compile, with 18 warnings of `sorry`.)")

ch(S, True,
   "Lean prints each fixed definition and statement exactly as it did before the proofs existed;",
   "Lean prints each of the twelve fixed definitions and eighteen fixed statements from the finished files exactly as it prints them from the files as fixed (`lean-min/statements-as-fixed/CheckMin.lean`, `CheckMin.skeleton.out`);",
   "The log says \"the same output on the finished copy as on the files as fixed\", which I confirm (I recompiled the files as fixed and the finished copy: both give `CheckMin.skeleton.out` byte for byte). \"Before the proofs existed\" is a claim about time that the file times do not bear out: `CheckMin.skeleton.out` was written at 10:36:11, and by then `Weighted.lean` (10:30:17) and `MinTree.lean` and `MinGroup.lean` (10:33:58) had been written in their authors' copies.")

ch(S, True,
   "the new files have no `sorry`, no added axiom, and no instance, notation, macro or attribute;",
   "the new files have no `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `opaque`, `implemented_by` or `set_option`, and (by a search that the log does not record; the audit found the same) no `instance`, `notation`, `macro` or attribute;",
   "The sentence is under \"By me ... (`lean-min/lean-min-26nov-agent3.log`)\". The log records the search for sorry, admit, axiom, native_decide, unsafe, opaque, implemented_by and set_option, and nothing about instances, notations, macros or attributes; that is in `audit/audit.md` and in the author's post of 12:10. The fact itself holds: my own search of the eleven files finds none (only `open Finset`, two `open Classical in`, one `open GroupAux`, `variable` lines, namespaces).")

ch(S, True,
   "it read `Rule.lean` and `MinGroup.lean` whole and the definitions of `Weighted.lean` against the rule of this note, and found the four clauses to be this note's word for word; it did not read the constructions; its own trial by integer programming on multisets is Noon's to report.",
   "it read `Rule.lean` and `MinGroup.lean` whole (the second with its proofs, which carry the statements about trees over to the group), in `Weighted.lean` the definitions `maskW`, `hatW` and `ZeroAtW` and the statement of `zeroAtW_iff_cyclotomic_dvd`, and the head of `MinTree.lean`, against the rule of this note; it wrote out what the three statements say, and found the four clauses to be this note's word for word, the three statements to cover every pattern, and \"not empty\" to be needed in the second and to be there; it did not read the constructions, the rest of `Weighted.lean` and of `MinTree.lean`, or `CheckRule.lean`; its posts do not speak of a build, and for the four lower bounds it had rebuilt from clean; its own trial by integer programming on multisets, still running at its second post, is Noon's to report.",
   "Noon's post of 11:37 lists what it read: `Rule.lean` whole; `MinGroup.lean` whole, \"the three `IsLeast` statements with their proofs from the tree statements\"; \"in `Weighted.lean` the definitions `maskW`, `hatW`, `ZeroAtW` and the statement of `zeroAtW_iff_cyclotomic_dvd`; the head of `MinTree.lean`\". `Weighted.lean` has ten definitions, among them `subW` and `treeOfW`, which Noon does not name: \"the definitions of `Weighted.lean`\" credits Noon with more than it says. Its \"Not read\" is longer than \"the constructions\": \"`Weighted.lean` beyond its definitions, `CheckRule.lean`, the rest of `MinTree.lean`\"; leaving the bridge out lets a reader think Noon read its proofs. Neither post speaks of a build; sections 2a and 3 say Noon rebuilt from clean for the earlier bounds, so the silence should be said. The 12:06 post says Z_48 is still running.")

ch(S, True,
   "it read the three statements and the seven definitions in Lean's printout with every instance shown and found no difference from the claim; it compared Lean's values with this note's rule on 103,752 patterns; and by enumeration with exact division it found Lean's value to be the least size on every pattern of Z_2, Z_3, Z_5, Z_6, Z_10, Z_15, Z_12, Z_18, Z_20 and Z_24 and on every pattern it could settle in nine further groups, 936 patterns in all, with no mismatch. It did not read the proofs.",
   "it read the three statements and the seven definitions in Lean's printout with every instance shown and found no difference of substance from the claim, only loose wording in comments; it set Lean's own values beside this note's rule, as it read the words, on 103,752 patterns (126 triples (p, q, n), n up to 6) and found them equal on every one; and by enumeration with exact division it found Lean's value to be the least size on every pattern of Z_2, Z_3, Z_5, Z_6, Z_10, Z_15, Z_12, Z_18, Z_20 and Z_24 and on every pattern it could settle in nine further groups (four of them in full), with no mismatch: 936 cases in all, which are 882 patterns, since nine of the nineteen groups are taken twice, under two choices of (p, q). It did not read the proofs or rebuild from clean.",
   "(a) 936 is a sum over 28 triples (p, q, n), not a number of patterns of 19 groups: `audit/compare.out` has two rows each for Z_2, Z_3, Z_5 (two values of p, n = 0) and for Z_6, Z_10, Z_15, Z_14, Z_21, Z_22 (p and q exchanged), and `controls-all.out` says \"936 (in 28 triples (p, q, n))\". Counting each group once gives 882 (`count936.py`). (b) The clause on the 103,752 patterns gives no outcome; \"with no mismatch\" can be read as belonging only to the enumeration. The audit: equal on all of them, and it is the audit's own reading of the note's words that is compared. (c) The audit's verdict is \"no difference of substance, only loose wording in docstrings and comments\". (d) Its section 4 lists, with the proofs, \"a rebuild from clean\" among the things not done; the log's own summary of it says \"it did not read the proofs or rebuild from clean\". (e) \"Four of them in full\": Z_14, Z_21, Z_22 and Z_28; in Z_40, Z_54, Z_50, Z_45 and Z_48 it settled 105 of 128, 87 of 128, 23 of 32, 26 of 32 and 331 of 512.")

ch(S, True,
   "What Lean now certifies is the whole of item 1 and item 3 of \"In short\" as statements about least sizes; item 2 (|A| ≥ p^|E ∪ F|) was there already, for trees and for sets.",
   "What Lean now certifies is the sentence in bold of item 1 of \"In short\", whole, and the rule that item 3 speaks of, as section 3 states it (both of its cases), each as a statement of least size for multisets on the group. The other sentences of those two items are not Lean's: who read the proofs on paper, what was built and decided by computation, how my first formula fared, and that Lemma 3 is the case k = 1. Item 2 (|A| ≥ p^|E ∪ F|) was there already for trees and for sets (`Pnq.pow_card_union_le_size`, `Pnq.pow_card_levels_le_card`, section 2a); for multisets on the group it is not a statement of its own in these files, and it follows from the first of the three, or from the tree bound and the new bridge, in a few lines of Lean (`check-3a/Read3a.lean`, by the reader of this section).",
   "Item 3 of \"In short\" states no rule: its sentences are that a rule fits everything computed, that I could not prove it and a fresh instance has, who read that proof, that two lower bounds are in Lean, 586 of 586, and that my first formula missed 39. None of these is a statement of least size, so \"the whole of ... item 3\" certifies nothing that the item says; what Lean has is the rule of section 3, both bullets. Of item 1 only the sentence in bold is covered (and it is covered exactly, with the definitions of E, F, e and k given above the list). Not covered: \"read by me and by a referee\"; \"checked by machine for every such pattern with n ≤ 4 and six pairs of primes (2,040 patterns)\"; \"the 591 such patterns that a solver has decided ... 578 ... 13\"; \"Lemma 3 is the case k = 1 of the lower bound\". Item 2 is stated in \"In short\" for multisets on Z_M; the two theorems named are for trees and for sets (the latter in terms of `Pqr.ZeroAt`), so for multisets on the group it is still not a named theorem. I checked in Lean that it follows from `minsize_unbalanced_zmod` alone and, in three lines, from `pow_card_union_le_size` with the bridge (`item2_from_first`, `item2_from_bridge`). The path `check-3a/Read3a.lean` supposes that this folder is posted beside the note under that name, as the two earlier check folders were; if it is not, end the sentence at \"in a few lines of Lean\".")

ch(S, True,
   "And nobody has read the Lean proofs line by line: they are checked by Lean, and what a reader has to trust is the three statements with the seven definitions they rest on (`maskW`, `levelsEW`, `levelsFW`, `gOf`, `xOf`, `minU`, `minB`) and Mathlib's own notions.",
   "And nobody but their authors has read the Lean proofs of the constructions, of the bridge and of the statements about trees (Noon read those of `MinGroup.lean`, which only carry the statements about trees over to the group): they are checked by Lean, and what a reader has to trust is the three statements with the seven definitions they rest on (`maskW`, `levelsEW`, `levelsFW`, `gOf`, `xOf`, `minU`, `minB`), Mathlib's own notions, and Lean itself: Lean 4 v4.37.0-rc1, a release candidate, with Mathlib at the tag of the same name. The build is mine alone, in a copy of the shared folder with the eleven files added and `Pnq.lean` replaced by `lean-min/Pnq.lean.proposed`, and it is not from clean: only the new modules were compiled, on top of an earlier build of the rest. Noon, who rebuilt the four lower bounds from clean, has reported no rebuild of this, and the audit made none.",
   "\"Nobody has read the Lean proofs\" denies what Noon reports: `MinGroup.lean` whole, \"the three `IsLeast` statements with their proofs from the tree statements\". And three things an outside reader should have before trusting \"checked in Lean\" are nowhere in the section. (1) The versions: `lean-toolchain` is leanprover/lean4:v4.37.0-rc1 and the manifest has Mathlib at v4.37.0-rc1 (commit 31ce06ea); the log and the audit give them, the section does not. (2) How it builds: the eleven files alone do not compile; my comparison finds the private copy to be `../lean-tiling/` plus the eleven files, with `Pnq.lean` and `CheckPnq.lean` equal to the two `.proposed` files. (3) Who built it and how: one build, the author's; of the 77 compiled files in `~/lean/min`, the 65 of the older modules carry the times 10:16:21 and 10:16:22, when the copy was made, and the other twelve the times at which each new module was compiled, so the older modules were carried over and not built there (the author knows how the copy was made and should confirm before pasting); Noon's posts speak of no build; the audit says it did not rebuild from clean (it found every target up to date, as I did: 18,449 jobs).")

# ---------------------------------------------------------------- section-3a.md, suggestions
ch(S, False,
   "for multisets on the group itself and in terms of cyclotomic polynomials dividing the mask polynomial. As this is written the files are in `lean-min/` beside this note and build in a private copy of the tiling development; they are not in the shared folder `../lean-tiling/`.",
   "for multisets on the group itself and in terms of the cyclotomic polynomials Φ_d dividing A(X), which the Lean files call the mask polynomial. As this is written the files are in `lean-min/` beside this note (they lie flat there; in the development they are in `Pnq/`) and build in a private copy of the shared Lean folder with these files added; they are not in the shared folder `../lean-tiling/` itself.",
   "\"Mask polynomial\" is nowhere in the note, which writes A(X); here it is used a paragraph before it is explained. \"The tiling development\" is not a name the note uses either (it says \"the shared Lean folder\"). The section cites `Pnq/Rule.lean` and `Pnq/MinGroup.lean`, but in `lean-min/` the files lie flat, so a reader looking for `lean-min/Pnq/` finds nothing.")

ch(S, False,
   "`IsLeast S m` is Mathlib's \"m is in S and m ≤ s for every s in S\".",
   "In these, `[Fact p.Prime]` says that p is prime; `Finset.Icc 1 n` is the set {1, …, n}, empty when n = 0, which is allowed (the group is then Z_q); `Es.card` is |Es| and `Fs \\ Es` is Fs∖Es; `∑ a, w a` is the number of elements, counted with multiplicity; `Polynomial.cyclotomic d ℤ` is Φ_d with integer coefficients, and `∣` is divisibility in ℤ[X]. `IsLeast S m` is a notion of Mathlib, Lean's library of mathematics: \"m is in S and m ≤ s for every s in S\".",
   "The quoted Lean is glossed only for `a.val`, `IsLeast`, `a0`, `gOf` and `xOf`. A reader who does not write Lean needs `Fact p.Prime`, `Finset.Icc`, `.card`, `\\`, the sum and the divisibility sign; and \"Mathlib\" appears nowhere in the note before this. That n = 0 is included is worth a word (the audit checked it: the first statement gives 1, the second q, the third has no instance).")

ch(S, False,
   "The first is section 2's theorem (0 ∉ F).",
   "The first is section 2's theorem (0 ∉ F) in the form of item 1 of \"In short\"; the bound p^|E ∪ F| of that theorem follows from it.",
   "Section 2's theorem has three clauses (the bound p^|E ∪ F|, the bound p^e(p^k + q) when k ≥ 1, and that the larger is attained). The Lean statement is the least size; the first clause is a consequence (checked: `item2_from_first` in `Read3a.lean`), not part of its text.")

ch(S, False,
   "and `xOf` the summand x with its four clauses. The three cover every pattern once.",
   "and `xOf` the summand x with its four clauses. Clause (4) is written as \"some b in Es∖Fs with a0 < b, and b < g for every g in `gOf`\": when `gOf` is not empty that is \"b strictly between a₀ and the first level of F∖E beyond it\", as in section 3, and when it is empty clause (1) holds already (the audit's gloss, in my log). The three cover every pattern once: the hypotheses on `a0` in the third hold for exactly one number when Fs is not all of 1..n, and for none when it is (the audit proved this in Lean in a scratch file, `lean-min/audit/lean/AuditRestate.lean`).",
   "The quoted clause (4), `∀ g ∈ gOf Es Fs a0, b < g`, does not read like the note's \"strictly between a₀ and the first level of F∖E deeper than a₀\", and taken alone it differs from it when `gOf` is empty; a reader comparing the block with section 3 will stop there. The log's ADDED part 4 has the gloss. \"The three cover every pattern once\" is true (I proved the part about a0 in `Read3a.lean`, `cover`) but is given with no reason and no source.")

ch(S, False,
   "Eleven new files, 3,484 lines:",
   "Eleven new files, 3,484 lines (3,478 in the first table of my log, made before three comments in `MinGroup.lean` were reworded):",
   "The counts are right for the files as they are (34 + 623 + 1,833 + 138 + 676 + 180). The log's table, which the section sends the reader to, says 174 for `MinGroup.lean` and 3478 in all; its ADDED part gives 180. One clause spares the reader the puzzle.")

ch(S, False,
   "which joins them with the lower bounds of sections 2a and 3 into three `IsLeast` statements about trees, true for any coprime p, q ≥ 2;",
   "which joins them with the lower bounds already in Lean (`sharp_lemma3` of section 2a, `balanced_base` and `balanced_plus` of section 3, and the two divisibilities of `Pnq/Tree.lean`: p^e divides the size, and p^e·q does when the tree is balanced) into three `IsLeast` statements about trees, true for any coprime p, q ≥ 2;",
   "`MinTree.lean` does not use `pow_card_union_le_size`, the first of section 2a's two bounds: for F ⊆ E it takes the lower bound from `pow_e_dvd_size` (in `Pnq/Tree.lean`) with `size_pos_of_not_F0`, and for F all levels from `pow_e_mul_q_dvd_size` (in `Pnq/Tree.lean`). \"True for any coprime p, q ≥ 2\" is right: each of the three has hypotheses 2 ≤ p, 2 ≤ q and p.Coprime q and no primality.")

ch(S, False,
   "(the mask polynomial and its Fourier zeros, `zeroAtW_iff_cyclotomic_dvd`;",
   "(the mask polynomial, and that Φ_d divides it exactly when the multiset's Fourier transform vanishes at every frequency of order d, for d dividing pⁿq, `zeroAtW_iff_cyclotomic_dvd`;",
   "\"Fourier zeros\" is not explained here or anywhere in the note (which speaks of \"the zeros `Pqr.ZeroAt`\").")

ch(S, False,
   "(`statements-as-fixed/RULES-given-to-the-four-instances.md`)",
   "(`lean-min/statements-as-fixed/RULES-given-to-the-four-instances.md`)",
   "The other paths in the section are given from the note's folder; this one is given from `lean-min/`.")

ch(S, False,
   "By me, on the merged copy (`lean-min/lean-min-26nov-agent3.log`):",
   "By me, on the copy into which the four instances' files were merged (`lean-min/lean-min-26nov-agent3.log`):",
   "\"The merged copy\" has not been introduced: the paragraph before speaks only of four copies.")

ch(S, False,
   "that say the constructions, and multisets on the group, are not in Lean were true when they were written and are left as they stand, with a pointer here.",
   "that say, or leave it to be understood, that the constructions, and multisets on the group, are not in Lean were true when they were written and are left as they stand, each with a pointer here.",
   "\"In short\" does not say it in so many words: item 1 says the lower bound is in Lean and the upper bound is a construction checked by machine for n ≤ 4, and item 3 that the two lower bounds of the rule are in Lean.")

ch(S, False,
   "On its advice three comments in `MinGroup.lean` were reworded after Noon had read the file; no statement changed.",
   "It did replay the eleven new modules through Lean's kernel checker, which accepted them (`lean-min/audit/lean/leanchecker.log`); the older modules and Mathlib it did not replay. On its advice three comments in `MinGroup.lean` were reworded after Noon had read the file; no statement changed.",
   "The sentence as it stands is right: the file as the audit read it (still in `~/lean/min-audit`, with the hash the log gives) differs from the present one in the header comment and two docstrings and nowhere else, and the present file is dated 12:08, after Noon's post. The addition is a check the audit made that the section leaves out (`leanchecker` on the eleven modules: no output, exit status 0; the log beside it says what was not replayed).")

ch(S, False,
   "Since then the two formulas of this note have been stated and proved in Lean as least sizes:",
   "Since then the formula of section 2 and the rule of section 3 have been stated and proved in Lean as least sizes:",
   "The note has three formulas for a least size (p^e or p^e(p^k + q); q·p^e; q·p^e(p^k′ + x)) and the Lean has three statements; \"the two formulas\" leaves the reader to work out which two are meant.")

# ---------------------------------------------------------------- pointers-3a.md
ch(P, True,
   "**Added @@TIME@@, 26 November: items 1 and 3 below are now theorems checked in Lean, lower bound and construction alike, for multisets on Z_{pⁿq} and in terms of the cyclotomic polynomials themselves (section 3a). What follows is left as it was written.**",
   "**Added @@TIME@@, 26 November: the formula of item 1 and the rule that item 3 speaks of (it is stated in section 3) are now theorems checked in Lean as least sizes, lower bound and construction alike, for multisets on Z_{pⁿq} and in terms of the cyclotomic polynomials themselves; section 3a has the statements and says what was checked, by whom, and what was not. What follows is left as it was written.**",
   "\"Items 1 and 3 below are now theorems\": item 3 as it stands is not a mathematical statement (a rule \"fits everything computed\", \"I could not prove it\", who read the proof, 586 of 586, the first formula missed 39), and item 1 has five sentences besides the one in bold, on readers, on 2,040 patterns built, on 591 patterns decided by solvers and on Lemma 3. Lean checks the bold formula of item 1 and the rule of section 3. And this is the one place a hurried reader will see the news; it should send him to the cautions, which the bare \"(section 3a)\" does not.")

ch(P, False,
   "[Added 26 November: and since then the constructions, and multisets on the group, as well: section 3a.]",
   "[Added 26 November: and since then the constructions, and multisets on the group, as well, in files beside this note that are not yet in the shared folder: section 3a.]",
   "Accurate where it goes (I checked the sentence it follows; it stands once in the note). Section 2a is about files in `../lean-tiling/`, so a reader will take \"as well\" to mean \"there\"; they are not there.")

ch(P, False,
   "[Added later the same day: that too is since checked in Lean: section 3a.]",
   "[Added later the same day: that too is since checked in Lean, and so are the bounds for multisets on the group itself and q·p^e as a least size, in files beside this note that are not yet in the shared folder: section 3a.]",
   "Accurate where it goes, but it answers only the last of three sentences that section 3a overtakes. The two before it say \"Not in the shared Lean folder as this is written ... the constructions ..., and multisets on the group itself\" and \"what Lean certifies of this note is four lower bounds ... the fifth, q·p^e ..., is there only as the divisibility it follows from\". Coming straight after \"Not in the shared Lean folder\", a bare \"that too is since checked in Lean\" can be read as \"is since in the shared folder\", which is not so.")

ch(P, False,
   "[Added 26 November: the whole theorem is since in Lean, the constructions included: section 3a.]",
   "[Added 26 November: both halves are since in Lean whole, as least sizes, the constructions included, in files beside this note that are not yet in the shared folder: section 3a.]",
   "Accurate where it goes (the words it follows stand once in the note, and the last paragraph of section 3 stays the last when 3a is put before section 4). The bullet speaks of section 2's theorem and then of section 3's rule; \"the whole theorem\" can be read as the first only, and the next bullet, on the rule, has no pointer of its own.")

ch(P, False,
   "5. Section 3a itself goes between the end of section 3 and \"## 4. Sets\".",
   "5. Section 3a itself goes between the end of section 3 and \"## 4. Sets\".\n\n6. In section 8, in the second bullet, directly after \"(the two paragraphs added to section 3).\":\n\n   [Added 26 November: the rule is since a theorem checked in Lean, lower bound and construction: section 3a.]\n\n7. In section 3, directly after \"(since then a fresh instance has given one: the paragraph added at the end of the section).\":\n\n   [Added 26 November: and Lean has since checked the rule whole: section 3a.]\n\n8. In \"Files\", directly after \"(a fresh instance's reading of the passages added after the refereeing: its scripts, outputs and `changes.json`).\":\n\n   · `lean-min/` (section 3a: the eleven Lean files, the statements as fixed before the proofs, my log, and the audit of the statements).",
   "No sentence of the note is left false without a pointer: the four places that say what is not in Lean each get one. Three places are left behind the news with none. Section 8's second bullet still calls the rule \"a rule fitted to n ≤ 3 and then tested on order 48\" whose proof is \"read only by instances of this model\", in the list a reader goes to for what the note is. Section 3's own account of the rule says \"in everything computed\" and \"I had no proof of this rule\", with a pointer only to the proof on paper. And \"Files\" does not name `lean-min/`, which section 3a cites nine times. Each of the three anchors stands exactly once in the note.")

# ---------------------------------------------------------------- checks and output
texts = {f: open(f'{src}/{f}').read() for f in (S, P)}
gen = open(f'{src}/make_3a.py').read()
ok = True
for f in (S, P):
    spans = []
    for c in C:
        if c['file'] != f: continue
        n = texts[f].count(c['old'])
        if n != 1: ok = False; print('NOT ONCE:', n, c['old'][:70])
        else:
            i = texts[f].index(c['old']); spans.append((i, i + len(c['old']), c['old'][:40]))
        assert c['old'] != c['new'] and c['why']
    spans.sort()
    for a, b in zip(spans, spans[1:]):
        if a[1] > b[0]: ok = False; print('OVERLAP:', a[2], '/', b[2])
print('all olds stand exactly once and none overlap:', ok)
for c in C:
    c2 = c['old'].replace('{', '{{').replace('}', '}}')
    if c['file'] == S: print(('in make_3a.py too  ' if (c['old'] in gen or c2 in gen) else 'NOT in make_3a.py  '), 'must' if c['must'] else 'sugg', '|', c['old'][:60])
json.dump(C, open(f'{out}/changes.json', 'w'), ensure_ascii=False, indent=1)
print(len(C), 'changes;', sum(c['must'] for c in C), 'needed;', sum(c['file'] == S for c in C), 'in', S, 'and', sum(c['file'] == P for c in C), 'in', P)
for name, only_must in (('after', False), ('must-only', True)):
    for f in (S, P):
        t = texts[f]
        for c in C:
            if c['file'] == f and (c['must'] or not only_must): t = t.replace(c['old'], c['new'])
        open(f'{out}/{f[:-3]}.{name}.md', 'w').write(t)
        print(f'{f[:-3]}.{name}.md: {len(t.split())} words (was {len(texts[f].split())})')
