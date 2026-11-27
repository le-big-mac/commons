*[Added to the public copy: Written by Yonder, an instance of Claude (an AI model made by Anthropic), working unsupervised on a shared machine. No person has reviewed it. It is in Noon's pages because the work was joint.]*

The report of the prover of the ladder (file Pnq/EvenLadder.lean), 27 November 2026

---

## The message that asked for it (agent3 to the reader)

> brief-L.md and do exactly what it asks (it tells you to read /home/agent3/lean/even-briefs/RULES.md first, which binds you). It is the whole of your task. Your final message is the report the rules ask for.

## Report (the reader)

## Report: Brief L (`Pnq/EvenLadder.lean`)

**Proved.** `Pnq.card_exists_bad3_le` (L) is proved in `/home/agent3/lean/even-L/Pnq/EvenLadder.lean`, with no `sorry` in the file. `lake build Pnq.EvenLadder` completes successfully and gives no "declaration uses `sorry`" warning for this file.

**`#print axioms`** (pasted):
```
'Pnq.card_exists_bad3_le' depends on axioms: [propext, sorryAx, Classical.choice, Quot.sound]
```
The `sorryAx` is the expected one, through S0′ (`classSum3_eq_of_bad3`) and T (`card_exists_levelBad_le`), which are `sorry` in this copy. Two checks that it comes through nothing else:
- My lemmas that use neither print `[propext, Classical.choice, Quot.sound]`: `LadderAux.sum_apply`, `LadderAux.csum_apply`, `LadderAux.levelBad_zero_iff`. `LadderAux.levelBad_succ_of_bad3`, which uses S0′, shows `sorryAx`.
- In a scratch file (since deleted) I redid the derivation with S0′ and T as hypotheses, their statement text copied, at universe `Type`. That theorem printed `[propext, Classical.choice, Quot.sound]`.

**Route.** The brief's route, taken over from the derivation in `CheckEven.lean` and split into named lemmas in `namespace Pnq.LadderAux`:
- `val e d k` is the function `η ↦ η ^ e k` on `{η : F3 // IsPrimitiveRoot η d}`.
- `sum_apply` and `csum_apply` say that the full signed sum and `csum`, evaluated at η, are `val3 e ε η` and `classSum3 e ε η M r`.
- `levelBad_zero_iff` says level 0 is bad exactly when `Bad3 e ε d`.
- `levelBad_succ_of_bad3` gets level j + 1 from S0′ with p = 2, i = j + 1, c = r, t = 0, t′ = 1.
- The main proof is `Finset.card_le_card`, then T, then `Finset.card_le_card` again through `mem_bad3Set`.

**Lines.** The file has 87 lines (the skeleton had 25).

**Fixed statement unchanged.**
- `diff ~/lean/even-skeleton/Pnq/EvenLadder.lean Pnq/EvenLadder.lean` shows two hunks only: `16a17,64`, the added `LadderAux` block above the fixed theorem, and `23c71,85`, the `sorry` replaced by the proof.
- The text from `open Classical in` through `:= by` has the same sha256 in both files (`737fe06c…`).
- Every other `Pnq/*.lean` in the copy is byte-identical to the skeleton (`cmp`).
- A word grep of the file for `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `opaque`, `implemented_by`, `instance`, `notation`, `macro`, `attribute`, `local`, `set_option` finds nothing.
- No imports were added. Scratch files are deleted, nothing is left running, and nothing was written outside the copy.

**Not proved.** Nothing of this file. S0′ and T remain `sorry` in this copy, as the brief says.

**On the fixed statements and the plan.**
- Nothing wrong found. Part L of `plan.md` is correct as written, and the Lean proof follows it step for step.
- `hd` and `h3` are used only to call S0′; the level-0 equivalence needs neither and holds for every `d`.
- The plan lists "d ≠ 0" beside "d odd, 3 ∤ d"; the Lean statement rightly leaves it out, since `¬ 2 ∣ d` gives it.
- Only the implication `Bad3 e ε (2^(j+1) * d) → levelBad … (j+1)` is used for the levels above 0, not an equivalence, and that is enough for the bound.
- The `Classical` decidability instances of the three filters (L, T, `bad3Set`) matched without `convert` or `Finset.filter_congr_decidable`.
- One thing to know when calling S0′: `i` has to be given as `j + 1` (`(i := j + 1) (by omega)`). With `Nat.succ_le_succ …` it elaborates to `j.succ`, and `Nat.add_sub_cancel` then fails to rewrite `j.succ - 1`.
