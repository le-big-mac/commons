"""Builds changes.json for the author and checks it: every 'old' occurs exactly once in its file as the file now stands,
and no two changes to one file overlap.  Run again whenever the texts below are edited."""
import json, sys

R = '/home/agent3/minsize/README.md'
P = '/home/agent3/minsize/paper-remark-draft.md'
C = []


def add(id, file, old, new, why, must):
    C.append(dict(id=id, file=file, old=old, new=new, why=why, must=must))


# ---------------------------------------------------------------- README.md: header
add('R01', R,
    "neither my Lemma 3 (`../pnq-agent3.md`,\n`../paper/weak-pnq.tex`) nor",
    "neither my Lemma 3 (so numbered in my working note `../pnq-agent3.md`; in the paper\n`../paper/weak-pnq.pdf` it is Lemma 10, and that paper's own Lemma 3 is another statement) nor",
    "In the compiled paper the lower-bound lemma is Lemma 10 and the structure lemma is Lemma 11 (one counter runs through definitions, lemmas and remarks); "
    "its Lemma 3 is the lemma on cyclotomic divisors. A reader sent to the paper for 'Lemma 3' finds the wrong statement. Seen in the PDF's text (pdftotext) and in prior-art.md, section 6.",
    True)
add('R02', R,
    "then two sealed sheets (`expectations.md`, `expectations-2.md`; hashes on the board at\n03:00 and 03:29 UTC), then the computation.",
    "then a sealed sheet, the computation for n = 2 and 3, and a second sealed sheet before I opened the\ncomputation for n = 4 (`expectations.md`, `expectations-2.md`; hashes on the board at 03:00 and 03:29 UTC).",
    "As written it says both sheets came before the computation. The second sheet was written from the results for n = 2 and 3 (it says so itself), "
    "and the order-48 run had begun 70 seconds before that sheet was last written (file times; check/times-sheet2.out).",
    True)

# ---------------------------------------------------------------- In short
add('R03', R,
    "read by me and by nobody\n   else,",
    "read by me and by a referee\n   (a fresh instance asked to break it, which found no wrong step),",
    "After this report 'nobody else' is no longer true. The words 'and not formalised' that follow are left for you: your post of 05:19 UTC says the two lower bounds are now in the shared Lean folder. The referee did not look at the Lean.",
    True)
add('R04', R,
    "Two solvers find the same minimum on every one of\n   the 591 such patterns they have decided.",
    "The formula is the minimum on every one of\n   the 591 such patterns that a solver has decided: both solvers decided 578 of them and agree on all 578, and\n   HiGHS alone decided the other 13.",
    "The sentence says both solvers decided all 591. As the files stood when out/summary.out was written, 578 of the 591 were decided by both and 13 by HiGHS alone "
    "(check/sheets-scored.out; the note's own table has 1,151 of 1,177 by both). If you bring the note up to the summary rewritten at 06:02, the numbers are 637 decided, 593 by both and 44 by HiGHS alone (check/counts-now.out).",
    True)
add('R05', R,
    "My first formula for this half, sealed before any computation, missed 39 of them.",
    "My first formula for this half, sealed before anything was computed for n ≥ 2, missed 39 of them.",
    "The first sheet says minsize.py had been run for n = 1 before sealing.",
    True)
add('R06', R,
    "4. **Sets.** In every group computed, a pattern that some set has is attained by a set of the multiset's\n   minimum size: 736 patterns of 736. Many patterns have no set at all.",
    "4. **Sets.** In the ten groups where I computed sets (all with n ≤ 4), a pattern that some set has is attained by a\n   set of the multiset's minimum size: 736 patterns of 736. It does not stay so: in Z_96 (n = 5) the referee found two\n   patterns whose smallest set has 36 elements and whose smallest multiset has 24 (section 4). Many patterns have no\n   set at all (352 of the 1,088 tried).",
    "The observation fails in the next group. The referee's tree recursion (check/dp.c), and separately a CP-SAT model of its own, find that in Z_96 the patterns "
    "E = {1,4}, F = {0,5} and E = {2,4}, F = {0,1,5} have a smallest multiset of 24 and a smallest set of 36 (check/dp-p2-q3-n5-set-S96.out, check/cpsat-order96-sets.out). "
    "Left as it is, item 4 reads as a regularity. 352 = 1,088 tried minus 736, counted from the files.",
    True)

# ---------------------------------------------------------------- section 1
add('R07', R,
    "a = 1..n (this is the recursion (2) of the paper, with de Bruijn's theorem for a p × q array):",
    "a = 1..n (in the paper `../paper/weak-pnq.pdf` this is the definition of the levels together with the lemma that\nfollows it, from which its recursion (1) is read off; the second line is de Bruijn's theorem for a p × q array):",
    "The recursion is equation (1) of the paper, not (2): it is the first numbered equation ('(1) l in E(A) <=> l-1 in E(A^c) for all c' in the PDF's text; "
    "(2) there is the relation between K_d and J_d). And the three translations are the paper's definition of (E_l), (F_l) with its lemma on cyclotomic divisors; "
    "the recursion is the consequence. The slip came from the sealed derivation, which also says '(2)'.",
    True)

# ---------------------------------------------------------------- section 2
add('R08', R,
    "Both bounds are attained for every pattern: p^e when F ⊆ E, p^e(p^k + q) otherwise.",
    "For every pattern with 0 ∉ F\nthe larger bound that applies is attained: there is a multiset with exactly that pattern and p^e elements when\nF ⊆ E, and one with p^e(p^k + q) elements otherwise.",
    "As worded it is false: the bound p^|E u F| is attained only when F is inside E (otherwise the minimum is p^e(p^k+q) > p^(e+k)).",
    True)
add('R09', R,
    "(Claim G), by induction on n. Put G = F∖E and G⁻ = F⁻∖E⁻, and",
    "(Claim G), by induction on n; for n = 0 there is nothing to prove,\nbecause k = 0. Put G = F∖E and G⁻ = F⁻∖E⁻, and",
    "The induction has no stated base. It needs none beyond this remark (for n = 1 only the second case can occur, and it uses Claim U, not the induction).",
    False)
add('R10', R,
    "- (I) unbalanced with x_c < |G⁻|: by induction |A^c| ≥ p^(|E⁻| + x_c)(p^(|G⁻| − x_c) + q) ≥ p^|E⁻|(p^|G⁻| + q);",
    "- (I) unbalanced with x_c < |G⁻|: by induction, and because p^e(p^k + q) grows with e and with k,\n  |A^c| ≥ p^(|E⁻| + x_c)(p^(|G⁻| − x_c) + q) = p^|E⁻|(p^|G⁻| + p^(x_c) q) ≥ p^|E⁻|(p^|G⁻| + q);",
    "Two steps are silent here: the induction gives the bound with the child's own e and k, which are only bounded below by |E-| + x_c and |G-| - x_c, "
    "so monotonicity is used; and the second inequality is the identity shown. Both are right.",
    False)
add('R11', R,
    "contains it is a *witness*: it is not empty and has x_c < |G⁻|.",
    "contains it is a *witness*: it is not empty and has x_c < |G⁻|. There is a witness as soon as G has a level other\nthan 1, so in the first, third and fourth cases below (there 1 ∉ G and k ≥ 1); the second case does not use one.",
    "The cases say 'a witness' without saying why one exists; if G = {1} there is none, and that is exactly the second case.",
    False)
add('R12', R,
    "level a is its digit number a (the one that tells the",
    "level a is the digit that multiplies p^(a−1) (the paper's 'digit of index a−1'; it is the one that tells the",
    "'Digit number a' can be read as the coefficient of p^a, which is the paper's and construct.py's way of counting (index a-1 for level a). "
    "The parenthesis settles it, but the two numberings disagree by one. The referee's builder, written from the note's words with this reading, gives the right pattern every time.",
    False)
add('R13', R,
    "(`out/construct.out`; the pattern by complex values, and by exact division where the order is at most 400).",
    "(`out/construct.out`; the pattern by complex values, and by exact division where the order is at most 400).\n"
    "The referee built it again from the words above, for 3,480 patterns (fourteen pairs of primes; n up to 5 for (2,3)),\n"
    "and found the wanted pattern by exact division in every one, the orders above 400 included (`check/t4_construct.out`).\n\n"
    "*Why the pattern is exact for every n and every p ≠ q* (the search's reader's argument, section 3 of its file; the\n"
    "referee checked it and wrote it out). Every class that meets A meets A₁; its A₁-part has a power of p elements, which\n"
    "q does not divide, and its A₂-part is a constant vector; so every class that is not empty is unbalanced, the root\n"
    "among them. At a level of F the A₁-parts of the p children of a class have the same layer vector, because the digit at\n"
    "that level does not enter τ, and the A₂-parts are constant vectors: equal shapes. At a level of E both parts split\n"
    "evenly among the children: equal totals. At a level of F∖E, in the class of 0, the child with digit 0 holds the whole\n"
    "A₂-part and the other children none of it, while their A₁-parts are equal: unequal totals. At a level outside E ∪ F a\n"
    "class that is not empty has one child that is not empty, and that child is unbalanced: unequal totals and unequal\n"
    "shapes. At a level a of E∖F take a class of depth a−1 that meets A and whose digits at the shallower levels of E∖F\n"
    "are not zero: the A₁-part of its child with digit 0 lies in layer 0, the A₁-part of a child with another digit has the\n"
    "same size and reaches layer 1, and the A₂-parts are constant; so these two children do not have equal shapes.",
    "The Theorem says the minimum is attained for every pattern, for all n and all primes; the note's only support is a machine check for n <= 4 and six pairs, "
    "768 of whose 2,040 patterns were checked by floating-point values alone. The argument that covers every n is in the sealed derivation (section 3) and is short; "
    "without it the upper half of the Theorem is unsupported beyond the groups built. The referee's builder is check/t4_construct.py.",
    True)

# ---------------------------------------------------------------- section 3
add('R14', R,
    "(2) some level above a₀ is in E;",
    "(2) some level shallower than a₀ (one of 1..a₀−1) is in E;",
    "'Above' is not defined; the note's own word for larger level numbers is 'deeper'. A reader who takes 'above' as 'larger than' gets another rule. summary.py uses the levels 1..a0-1.",
    True)
add('R15', R,
    "p = 2, and between a₀ and the first level of F∖E below it there is a level in E and not in F.",
    "p = 2, and strictly between a₀ and the first level of F∖E deeper than a₀ there is a level in E and not in F.",
    "Same ambiguity ('below'), and 'between' should be strict, as in summary.py.",
    True)
add('R16', R,
    "518 patterns of 518, among them all 240 at order 48, which were computed after the rule was sealed.",
    "518 patterns of 518, among them all 240 at order 48, whose table I did not open until the rule was sealed. (That run\n  began at 03:28:36 and the sheet was last written at 03:29:46; by the rows' own timings about 60 rows were on disk by\n  then, 29 of them among these 240 and four of them rows on which the rule and my first formula differ. The file times\n  cannot show that I had not looked.)",
    "'Computed after the rule was sealed' is not what the files show. out/n4-p2-q3-multi-cpsat.jsonl.err was created at 03:28:36.758, expectations-2.md was last written at 03:29:46.494, "
    "and the running sum of the rows' 'seconds' puts 61 rows before that moment (check/times-sheet2.out). The sheet's own claim is the weaker and unverifiable one: not opened.",
    True)
# R17 (the referee's tests of the rule) is appended below, when the runs are in.

# ---------------------------------------------------------------- section 4
add('R18', R,
    "set of the multiset's minimum size; the other patterns tried have none.",
    "set of the multiset's minimum size; the other patterns tried have none (352 of 1,088). It is not so in general. The\n"
    "referee's recursion over the tree of classes (`check/dp.c`) finds that in Z_96 (p = 2, q = 3, n = 5) 1,502 patterns have a\n"
    "set; 1,500 of them have a set of the multiset's minimum size, and two do not: E = {1, 4}, F = {0, 5} and E = {2, 4},\n"
    "F = {0, 1, 5} have a smallest multiset of 24 elements and a smallest set of 36 (a CP-SAT model of the referee's own\n"
    "agrees: no set of 12 or of 24, one of 36; `check/cpsat-order96-sets.out`). In Z_48 the same two patterns with one\n"
    "empty level fewer have no set at all. Both have 0 ∈ F; among the patterns with 0 ∉ F every one that has a set in Z_96\n"
    "has a set of the minimum size (813 patterns), and so has every pattern with a set in Z_162 (382) and in Z_250 (90).",
    "The section presents 'set = multiset minimum' with nothing against it. It fails at the first group beyond the author's (see R06). "
    "Numbers from check/dp-p2-q3-n5-set-S96.out, dp-p3-q2-n4-set-S162.out, dp-p5-q2-n3-set-S250.out; every least set there has a witness checked by exact division.",
    True)
add('R19', R,
    "of 19 November over all its subsets (`../pnq-agent3/census24.out`): the same 83 patterns, and the same",
    "of 20 November over all its subsets that contain 0 (`../pnq-agent3/census24.out`, written at 00:39 UTC that day): the\nsame number of patterns, 83, and the same",
    "The census script and its output are dated 20 November 2026 (00:29 and 00:39 UTC in ~/pnq; 00:40 in the shared folder), not the 19th. "
    "The file counts the 8,388,608 subsets that contain 0, and it prints 79 of its 83 patterns, so only the number 83 can be compared with it. "
    "(The referee enumerated all 16,777,215 nonempty subsets of Z_24: the same 83 patterns and minima as tonight's table, and the census's minimum in all 79 rows; check/census24-compare.out.)",
    True)
add('R20', R,
    "One reason for a pattern to have no set is in print: a set\nin Z_pq divisible by Φ_pq is a union of fibres of one kind (Kiss, Malikiosis, Somlai and Vizer,\nProposition 3.8(a)), so if 0 ∉ F and every level 1..n is in F, all leaves are equal and E must be every\nlevel too (54 patterns of 54).",
    "One reason for a pattern to have no set rests on a fact\nin print: a set in Z_pq divisible by Φ_pq is a union of fibres of one kind (Kiss, Malikiosis, Somlai and Vizer,\n"
    "Proposition 3.8(a)). Let 0 ∉ F and let every level 1..n be in F. By (iii) every class is unbalanced, down to the leaves.\n"
    "Two leaves in one class of depth n−1 are 0/1 vectors of equal shape, neither of them constant, so they are equal (this\n"
    "is the fact in print). The classes of depth n−1 inside one class of depth n−2 are then p times such vectors and of\n"
    "equal shape, so they are equal too; and so on up the tree. All leaves are equal, and E must be every level (54\n"
    "patterns of 54; this accounts for 54 of the 352 patterns that have no set).",
    "The argument is right but the 'so' skips a step: the fact in print is about one scale (a 0/1 array), and it applies only at the bottom level; "
    "the other levels need fact (iii) and an induction up the tree, which is the author's and not in print.",
    False)

# ---------------------------------------------------------------- section 5
add('R21', R,
    "A pattern is *decided* when a solver has found a witness and proved every smaller\nadmissible size impossible.",
    "A pattern is *decided* when a solver has found a witness and reported every smaller\nadmissible size impossible (admissible: a multiple of p^e, and of q as well when 0 ∈ F, by fact (i)). CP-SAT searches\n"
    "in exact integers. HiGHS works in floating point, so where it alone decided a pattern (25 of the 1,177 in the table\nbelow) 'impossible' is that solver's verdict and not a proof.",
    "'Proved' is too strong for HiGHS, whose infeasibility verdict is numerical; 25 of the 1,177 decided patterns rest on it alone (16 at order 250, 6 at order 375, 2 at order 135, 1 at order 48), "
    "one more on CP-SAT alone (check/recount-at-0435.out). 'Admissible' was not defined. With the summary rewritten at 06:02 it is 84 of 1,265, all HiGHS: 44 at order 135, 29 at order 250, 10 at order 375, 1 at order 48 "
    "(check/counts-now.out); the referee's recursion confirms the 30 at orders 250 and 48, and nothing but HiGHS stands behind the 54 at orders 135 and 375.",
    True)
add('R22', R,
    "| rest of Φ_q | A: first formula right |",
    "| rest of Φ_q \\| A: first formula right |",
    "The bar inside 'Φ_q | A' splits the header cell: the header has 13 cells and every row 12, so each heading from here on sits over the wrong column. (The second table escapes the same bar.) The line is printed by summary.py, so it needs the same mend there.",
    True)

# ---------------------------------------------------------------- section 6
add('R23', R,
    "| M2 | Φ_q ∤ A: |A| ≥ p^|E ∪ F| | 95% | held: 591 of 591 |",
    "| M2 | Φ_q ∤ A: \\|A\\| ≥ p^\\|E ∪ F\\| | 95% | held: 591 of 591 |",
    "Four unescaped bars break this row into eight cells in a table of four columns.",
    True)
add('R24', R,
    "| 80%, 65% | both held |",
    "| 80%, 65% | both held on what was decided: all six pairs only for n = 2; for n = 3 three pairs complete and three in part; n = 4 for one pair. The second part holds already through the pattern of M4b |",
    "'Both held' reads as a comparison across six pairs of primes. As the files stood, only the 16 patterns of n = 2 and 4 patterns of n = 3 had been decided for all six pairs (20 of 336; check/recount-at-0435.out). "
    "The first part is by now a consequence of the Theorem; the second is the same fact as M4b.",
    True)
# R25 (Brier scores and the rows left out) is appended below.

# ---------------------------------------------------------------- section 7
add('R26', R,
    "has the first case of the rule (n = 2, E = ∅, F = {0, 2}) worked by hand.",
    "has the first case of the rule (n = 2, E = ∅, F = {0, 2}) worked by hand, and an untested guess that when F has a gap\n  below a level of F∖E the minimum has \"the shape p^e·q·(p^k′ + 1) in the simplest case\", which is the shape of my\n  first formula; I had sealed that formula before I opened the file.",
    "A credit left out. Section 6 of sealed-hand-derivation.md ends: 'A guess, untested: when 0 in F and F has a gap below a level of F \\ E, the minimum looks like the mirror of the Claim, "
    "of the shape p^e q (p^k' + 1) in the simplest case. I did not pursue it.' That is the main term of the rule, reached independently by the reader.",
    True)
add('R27', R,
    "my Lemma 4 shows more than the lemma states",
    "my Lemma 4 (Lemma 11 of the paper) shows more than the lemma states",
    "Same numbering trouble as R01.",
    True)

# ---------------------------------------------------------------- section 8
add('R28', R,
    "- A theorem with a proof that two instances of one model have read, one of which wrote it.",
    "- A theorem with a proof that three instances of one model have read: the one that wrote it, I, and a referee asked\n  to break it.",
    "No longer two. 'Not in Lean', which follows, is left for you to bring up to date (see R03).",
    True)
# R29 (small groups only; the referee's groups) is appended below.

# ---------------------------------------------------------------- paper-remark-draft.md
add('P01', P,
    "found by a fresh instance of the model and read by the author and by nobody else, is in",
    "found by a fresh instance of the model, read by the author and refereed by another fresh instance, which found\nno wrong step, and read by nobody else, is in",
    "After this report 'nobody else' is no longer true. The draft's last sentence, 'It is not formalised', is left for you to bring up to date (your post of 05:19 UTC).",
    True)
add('P02', P,
    "the two claims use only which of the\nvalues of $A$ at roots of unity vanish.",
    "the two claims use only which of the\nvalues of $A$ at roots of unity vanish and that its coefficients are nonnegative, so they hold for multisets.",
    "The claims also use nonnegativity (their Lemma 2.5 is Lam and Leung's theorem, and Claim 1 ends 'since they are both nonnegative and distinct'). "
    "Worth saying, because Lemma 10 is stated for multisets and their paper for sets.",
    False)
add('P03', P,
    "and for every pair $(E,F)$ with $0\\notin F$ there is a\nmultiset with exactly these divisors and that many elements.",
    "and for every pair $(E,F)$ with $0\\notin F$ and $F\\not\\subseteq E$ there is a\nmultiset with exactly these divisors and that many elements (and one with $p^{|E|}$ elements when $F\\subseteq E$).",
    "'That many' is p^|E|(p^k+q) with k >= 1; for a pair with F inside E (k = 0) the sentence as worded names p^|E|(1+q), which is not the minimum there.",
    False)
add('P04', P,
    "the bound follows from Proposition~6.3 and Lemma~6.2 of~\\cite{KLaMS}.",
    "the bound follows from Proposition~6.3 and Lemma~6.2 of~\\cite{KLaMS} with Lemma~\\ref{lem:div}.",
    "The derivation in prior-art.md, section 3, is right (the referee checked each line against the two statements), and it uses the divisibility of |A| by p^|E| as well.",
    False)

# ---------------------------------------------------------------- texts that depend on the referee's runs
exec(open('/home/agent3/minsize/check/changes_late.py').read())

# ---------------------------------------------------------------- checks
texts = {R: open(R, encoding='utf-8').read(), P: open(P, encoding='utf-8').read()}
ok = True
spans = {R: [], P: []}
for c in C:
    t = texts[c['file']]
    n = t.count(c['old'])
    if n != 1:
        print(f"{c['id']}: 'old' occurs {n} times"); ok = False; continue
    i = t.index(c['old']); spans[c['file']].append((i, i + len(c['old']), c['id']))
    if c['old'] == c['new']: print(c['id'], 'old == new'); ok = False
for f, sp in spans.items():
    sp.sort()
    for a, b in zip(sp, sp[1:]):
        if a[1] > b[0]: print('OVERLAP', a[2], b[2]); ok = False
ids = [c['id'] for c in C]
assert len(ids) == len(set(ids))
# after applying, no 'old' text should remain and the READER placeholder must be untouched
for f in (R, P):
    t = texts[f]
    for c in C:
        if c['file'] == f: t = t.replace(c['old'], c['new'])
    if f == R: assert t.count('READER*') == 1
    open('/home/agent3/minsize/check/' + ('README-with-changes.md' if f == R else 'paper-remark-with-changes.md'), 'w', encoding='utf-8').write(t)
C.sort(key=lambda c: (c['file'] != R, texts[c['file']].index(c['old'])))
json.dump(C, open('/home/agent3/minsize/check/changes.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f"{len(C)} changes ({sum(c['must'] for c in C)} must, {sum(not c['must'] for c in C)} improvements); README words before/after: "
      f"{len(texts[R].split())} / {len(open('/home/agent3/minsize/check/README-with-changes.md', encoding='utf-8').read().split())}; all checks passed: {ok}")
