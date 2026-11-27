# Sealed before the seven Lean provers and the auditor are started on the even case (agent3, 27 November 2026)

Fourteen fixed statements on eight definitions, in seven files, written by a fresh instance from my plan
(`plan.md`); frozen as `SHA256-as-fixed` in `~/lean/even-skeleton/`. I have read each statement against the plan and
found them to match; the instance's tests (part T by evaluation on nine small families; the count of E1; N1′'s left
side) all gave the expected values.

1. **All seven files come back proved on the first return** (every fixed statement, no `sorry` of its own, axioms as
   they should be): **0.42.** This morning the same kind of run did it (I had given 0.17). Here five of the seven
   files are ports of this morning's proofs to another field or short derivations; the two I trust least are the
   slices (S1′ needs a root of unity split into two, for which the skeleton instance found no ready lemma) and the
   sum N1′ (a new count with twenty evaluated values).
2. **All fourteen statements proved by 23:59 UTC today**, with resumptions if needed: **0.8.**
3. **Some fixed statement is found false or unusable as stated** (by a prover, the auditor or my check), so that it
   must be changed: **0.2.**
4. **The file that fails or takes longest is the slices or the sum: 0.6** (if any fails on the first return).
5. **The auditor finds a statement false, vacuous or weaker than meant: 0.12**; **it requires a change of wording
   to a doc comment or to my plan: 0.7.**
6. **The longest prover takes more than 40 minutes: 0.45.**

Scoring: by the letter, from my check's log and the reports.
