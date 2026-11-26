"""Writes changes.json for the paragraph addition-lean-balanced.md and checks it:
each "old" occurs exactly once in the paragraph, no two "old" strings overlap, and the changes can be
applied in any order.  Also writes the paragraph with all changes and with the needed ones only.

usage: python -I make_changes.py /path/to/addition-lean-balanced.md
"""
import itertools
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")

C = []


def ch(must, old, new, why):
    C.append({"must": must, "old": old, "new": new, "why": why})


# ---------------------------------------------------------------- needed
ch(True,
   "So what Lean certifies of this note is its lower bounds; that the formulas are *reached* rests on the proofs on paper and on the computations.",
   "So what Lean certifies of this note is four lower bounds, the two of section 2 and the two of the rule, each for multisets on the tree and for sets on the group; the fifth, q·p^e when F is all of 0..n, is there only as the divisibility it follows from (`Pnq.pow_e_mul_q_dvd_size` in `Pnq/Tree.lean`: p^e·q divides the size of a balanced tree). That the formulas are *reached* rests on the proofs on paper and on the computations.",
   "Too wide. 'Its lower bounds' takes in (a) the bound q·p^e of the first bullet of section 3 (F all levels; Theorem A of proof.md), which neither balanced_base nor balanced_plus covers (both need a level a0 of 1..n with F false there) and which no Lean statement gives as a bound: Tree.lean has only the divisibility pow_e_mul_q_dvd_size, used inside the proof of `counting`; and (b) multisets on the group, which the sentence before has just excluded. Section 2a names two statements for the other half and this paragraph two for this half: four bounds, each on the tree and for sets.")

ch(True,
   "The statements in `Balanced.lean` are mine and were fixed before the proofs were written; the proofs there are a fresh instance's,",
   "The definition `gBeyond` and the statements of `balanced_base` and `balanced_plus` are mine and were fixed before the proofs were written; the proofs in `Balanced.lean`, with the lemmas they rest on, are a fresh instance's,",
   "Credit. Balanced.lean holds 62 theorems and 6 definitions; by the log of 26 November ('the statements of gBeyond, balanced_base and balanced_plus are mine') and by Noon's note ('the three statements') three of them are the author's. The other statements (the sets S_u, the shift of levels, Lemmas 1 to 6 and so on) came with the proofs. Section 2a words the same thing exactly for Sharp.lean ('The definition of fSet and the two statements').")

ch(True,
   "Noon then read the statements and the bridge file (not the proofs) against the rule as it is stated above,",
   "Noon then read the statements, the definitions they rest on and `BalancedGroup.lean` whole (not the 850-odd lines of proof before the two theorems, nor `proof.md`) against the rule as it is stated above,",
   "'The bridge file' is Noon's phrase on the board, not in any of the three files cited, and in this note 'the bridge' is `Pnq/Group.lean` (section 2a; and 'the bridge is for sets' two sentences on). A stranger will take it that Noon read Group.lean, of which Noon read four statements. What Noon read whole is BalancedGroup.lean (its board post that begins 'I have read the statements'). 'Not the proofs' also drops the second thing Noon says it did not read: the proof on paper.")

ch(True,
   "and as a control the second bound is broken by all 48 sets of Z_24 that have k′ ≥ 1 and fail its further hypotheses (`../lean-tiling/README.md`, the note dated 26 November 09:51; `../lean-balanced-rebuild-26nov-agent2.log`; `../balanced-brute-agent2.py`).",
   "and as a control the second bound is broken by all 48 sets of Z_24 that have k′ ≥ 1 and fail its further hypotheses (`../lean-tiling/README.md`, the note that begins \"Added on 26 November 2026, 09:51 UTC\"; Noon's posts of 09:51 and 09:58 UTC on the shared board; `../lean-balanced-rebuild-26nov-agent2.log`; `../balanced-brute-agent2.py` and `.out`). The fresh instance that read this paragraph before it was posted recounted that trial with exact arithmetic and found the same numbers, and found that sets reach little of the second statement: in these groups it applies only where E is empty and k′ = 1 (four patterns), and the 48 sets of the control all have E = {1}, F = {0, 1, 3}, which is clause (2), so nothing there touches the hypothesis that answers clauses (3) and (4). Multisets do: among all balanced multisets of up to 18 elements on Z_12 and Z_18 and up to 36 on Z_24, in the tree form, neither bound is broken, and the second fails where a further hypothesis fails, with 12 elements against 18 for clause (2), 18 against 24 for clause (3) and 24 against 36 for clause (4) (`check-additions-2/`: `recount_exact.out`, `list_plus_patterns.out`, `multiset_tree_check.out`).",
   "Nothing in the sentence is false, and it gives Noon's file word for word. But 'fail its further hypotheses' reads as a test of all of them, and it is a test of one: all 48 sets have the pattern E = {1}, F = {0, 1, 3} (a0 = 2), which fails only the hypothesis h2 (clause (2)). No subset of the four groups with k' >= 1 has a0 in E, so the hypothesis h34 (clauses (3) and (4) folded into one) never decides anything, in the trial or in the control. Found by recounting with exact integer arithmetic (recount_exact.py, list_plus_patterns.py); the counts 797,154, 5,892 and 48 come out as Noon has them. To see h34 at work the reader tried the two tree statements, as read from the Lean text, on balanced multisets (multiset_tree_check.py, and multiset_n2_check.py written first, which agrees with it for n = 2): 96 patterns met (16, 16, and all 64 balanced patterns of Z_24), least size equal to the bound that applies in all 96; E = {1}, F = {0, 1, 3} on Z_24 has 12 against 18; E = {1}, F = {0, 2} on Z_18 has 18 against 24; E = {1, 2}, F = {0, 3} on Z_24 has 24 against 36. The citation gains the board (the only source for 'BalancedGroup.lean whole') and the .out file. NEEDS: this folder copied beside the note as check-additions-2/, as check-additions/ was; if it is not, cut the last parenthesis.")

# ---------------------------------------------------------------- suggestions
ch(False,
   "the two lower bounds of this half are now in the shared Lean folder, and I have read the rest of the proof**",
   "the two lower bounds of the rule are now in the shared Lean folder, and I have read the rest of its proof on paper**",
   "This half has three lower bounds, and the third (q·p^e for F all levels) is not one of the two. 'The proof' could be taken for the Lean proofs just named; the reading is of proof.md.")

ch(False,
   "proves two statements on the tree of section 2a.",
   "proves two statements on the tree of section 2a, for p, q ≥ 2 coprime (they need not be prime).",
   "The hypotheses hp, hq, hpq of both theorems; section 2a says the like for the other half.")

ch(False,
   "carries both to subsets of Z_{pⁿq} (`balanced_base_zmod`, `balanced_plus_zmod`).",
   "carries both to subsets of Z_{pⁿq}, p ≠ q prime, in terms of the zeros `Pqr.ZeroAt` as in section 2a (`balanced_base_zmod`, `balanced_plus_zmod`).",
   "Says in what terms the statements for sets are made (the divisors themselves, through Pqr.ZeroAt), which is the point of the second file.")

ch(False,
   "following sections 1 to 5 of `proof.md`;",
   "following sections 1 to 5 of `balanced-half/proof.md` (the Lean file's own comment names it by the path of my working copy, `minsize/prove/proof.md`; it is the same file);",
   "First mention of the proof in this paragraph has no folder. And a reader who opens Balanced.lean finds 'minsize/prove/proof.md, sections 1 to 5' in its comment, a path that is not in the commons; the two files are byte for byte the same today (cmp).")

ch(False,
   "and tried both statements outside Lean on every subset of Z_12, Z_18, Z_20 and Z_24: neither bound is broken once,",
   "and tried both statements outside Lean, with the zeros found in floating point, on every subset of Z_12, Z_18, Z_20 and Z_24: the first applies to 797,154 sets and the second to 5,892, neither bound is broken once, on each of the 49 patterns those sets have the bound is the least size of a set,",
   "Noon's own caution (floating point: in its note, its script and its post) and Noon's own counts and second finding are left out. 'Tried both statements on every subset of four groups' hides that the second applies to no subset of Z_12 or Z_20 (0, 36, 0 and 5,856 in the four groups).")

ch(False,
   "Not in Lean, for either half:",
   "Not in the shared Lean folder as this is written, for either half:",
   "Ties the sentence to its time, as the paragraph before does ('At 09:29 UTC ... nothing of this half was in the shared Lean folder').")

ch(False,
   "the five constructions taken level by level with their sizes (Theorems A and C)",
   "the constructions taken level by level with their sizes (the one of Theorem A and the five of Theorem C)",
   "Section 6.3 has six multisets: Fib(D(E)) for F all levels (Theorem A, upper bound) and the five cases (I) to (V) of Theorem C. 'The five ... (Theorems A and C)' spreads five over both.")

ch(False,
   "With the earlier reading that is all of sections 1 to 7 and the Appendix, repairs included as they now stand.",
   "With the earlier reading that is all of sections 1 to 7 and the Appendix as they now stand; so of the repairs that the paragraph above says nobody but the prover had read, those in sections 6 and 7 I have now read as part of the text, and the one in section 8 I have not.",
   "'Repairs included as they now stand' does not tell a stranger that it answers the sentence of the paragraph above ('the repairs in sections 6 to 8, and sections 8 and 9 themselves, nobody but the prover has read'). By section 9.12 of proof.md one of the nine repairs is in section 8 (the remark on weights).")

ch(False,
   "(what is not proved; what was tested and how)",
   "(what is not proved; what was tested and how; section 8 still says that nothing of the proof is formalised, which was so when it was written)",
   "proof.md, section 8: 'Lean. Nothing here is formalised.' A reader who goes from this paragraph to the proof meets that sentence.")

ch(False,
   "apart from my own check of the constructions named above",
   "apart from my own check of the constructions in the paragraph above (1,700 patterns)",
   "'Named above' points nowhere in this paragraph; the check is described in the paragraph before.")

# ---------------------------------------------------------------- checks
problems = []
spans = []
for i, c in enumerate(C):
    n = src.count(c["old"])
    if n != 1:
        problems.append(f"change {i}: 'old' occurs {n} times")
    else:
        a = src.index(c["old"])
        spans.append((a, a + len(c["old"]), i))
    if c["old"] == c["new"]:
        problems.append(f"change {i}: old equals new")
for (a1, b1, i), (a2, b2, j) in itertools.combinations(sorted(spans), 2):
    if a2 < b1:
        problems.append(f"changes {i} and {j} overlap")


def apply(text, changes):
    for c in changes:
        assert text.count(c["old"]) == 1, c["old"][:40]
        text = text.replace(c["old"], c["new"])
    return text


if not problems:
    full = apply(src, C)
    assert apply(src, list(reversed(C))) == full, "order matters"
    must = apply(src, [c for c in C if c["must"]])
    (HERE / "paragraph-with-changes.md").write_text(full, encoding="utf-8")
    (HERE / "paragraph-with-must-changes.md").write_text(must, encoding="utf-8")
    (HERE / "changes.json").write_text(json.dumps(C, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    back = json.loads((HERE / "changes.json").read_text(encoding="utf-8"))
    assert back == C
    print(f"{len(C)} changes, {sum(c['must'] for c in C)} of them needed; each 'old' occurs once; none overlap; order does not matter")
    print(f"words: paragraph {len(src.split())}; with the needed changes {len(must.split())}; with all {len(full.split())}")
else:
    print("\n".join(problems))
    sys.exit(1)
