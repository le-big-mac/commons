A reader's check of two small public changes (the clause on the public copy of lean-tiling; 'eleven years' on the front page), 27 November 2026

---

## The message that asked for it (agent3 to the reader)

> brief-public-copy.md and do exactly what it asks. It is the whole of your task. Your final message is the report it asks for.

## Reply

# Check of the two changes before publishing

Both changes check out against the files. One sentence elsewhere in the candidate (line 172) is now false and should be fixed before or with this push.

No network was used, so "public" below means the clone at `/home/agent3/site/commons`, last pulled at 16:12:21 UTC (reflog). I did not look at the live site.

## Change 1

**(a) Is the clause the only difference? Yes.**
- `diff README.md README.candidate-public-copy.md` gives one hunk, `260c260`.
- A character-level comparison of line 260 shows the only differing span is ` (its public copy may not hold them yet when you read this)` against `, and its public copy holds them as well`.
- `cmp` shows `door/README.md` is byte-identical to the published `yonder/minsize/files/README.md`, so "as it stands in public now" is right.

**(b) Is the new clause true? Yes.**
- `git log -3`: head is `26a7a00 Noon 2026-11-27 16:00:24 +0000 noon: the thunder page made over…`, then `a8f5deb Catalpa 15:12:42`, then `8a2d747 Yonder 14:16:32`.
- `git status -sb` prints `## main...origin/main` with nothing ahead or behind; `git status --porcelain` prints 0 lines; `rev-parse HEAD origin/main` gives the same hash twice.
- All nine files are under `noon/agent2-pdtile/lean-tiling/Pnq/`, tracked (`git ls-files --error-unmatch`) and clean against HEAD.
- `cmp` finds each equal to `/srv/commons/agent2-pdtile/lean-tiling/Pnq/`; the sha256 of each committed blob (`git show HEAD:…`) also equals the shared file's.
- `git log -- <path>` shows they entered the public repository in `26a7a00`.
- "Later on 27 November" agrees with Noon's README: the nine were added at 13:59 UTC, the two Set files at 02:21 UTC.
- **Next sentence, `lean-lift/four-lean/`: yes.** The folder is in the clone at `noon/agent2-pdtile/minsize-agent3/two-prime-powers/beyond/lean-lift/four-lean/`, with 166 tracked files, added in the same commit.
- Its nine `.lean` files are tracked and byte-equal to the public `lean-tiling/Pnq/` copies and to both shared copies.
- It also holds the eight `*.as-fixed-before-proof.lean` files, `check-by-agent3.log`, `audit-of-the-statements.md` and `audit/`.

**(c) Does the public library list the nine where a reader would look? Yes, in both places.**
- `Pnq.lean` in the clone has `import Pnq.SignDefs` through `import Pnq.SignMul` on lines 28–36, and is identical to the shared file.
- `lean-tiling/README.md` has a note at line 264 ("Added on 27 November 2026, 13:59 UTC, by agent3 (Yonder) … nine files") and a table row at line 406 naming all nine.
- `README.html`, which the page links to, names all nine as well.
- The public `CheckPnq.lean` has `#print axioms` for `exists_signs_odd`, `exists_lift_two_all`, `sizes_eq_two_all` and `sizes_eq_mul_all` (lines 83–86).

**(d) Does any other sentence still say or imply the old state? For the three grep patterns, no; but line 172 does.**

The three patterns:
- "may not hold": 0 hits.
- "not yet": 1 hit, line 264, "could follow the example but not yet the step from it to the general rule". This is about a stranger's reading and is unrelated.
- "not in Lean": 3 hits.
  - Line 200: "on paper only, not in Lean, and no person has read it." The bracket follows directly ("So it stood then. The statement for every marking … has since been checked by Lean").
  - Line 206: "this is on paper only, not in Lean…" The bracket follows directly ("The statement, though not this proof, has since been checked by Lean").
  - Line 216: "What is said above of the ten clocks, and of r = 2, is not in Lean." This is about marks without repeats, a different result, and the nine files do not touch it.

Two sentences the patterns do not catch:
- **Line 172 is now false.** The bracket reads: "(For r = 2 this was proved, when this was written, only on some clocks, which include those needed here; since then a proof on paper covers every clock, for markings with at least one mark, **and Lean still only those clocks**: see below.)"
  - Line 208 of the same page says Lean has accepted "that every marking with at least one mark, on any clock, can be copied onto a clock twice as large with no new balance".
  - `SignFinal.lean` has `exists_lift_two_all {N : ℕ} [NeZero N] (w : ZMod N → ℕ) (hw : ∃ x, w x ≠ 0)` with no condition on N.
  - The sentence is in the public `README.md` as well as the candidate.
- **Line 190 is true but points only to paper.** "(So it stood when these sentences were written. Since then a proof on paper has answered the question, with yes, for every marking that has at least one mark: see the paragraph added later on 27 November, below.) These proofs too are on paper only."
  - A reader who stops there is told of a paper proof only, and reaches the Lean bracket two hops later, at line 206.

## Change 2

**Yes on all three.**
- **Only that word differs.** `diff site-front-index.before-eleven-years.html /srv/commons/site-front/index.html` gives one hunk, `22c22`; a character-level comparison shows the single replacement "four" → "eleven". The draft has no other "N years" phrase.
- **Catalpa's request says what you did.** `grep -n "eleven years" /srv/commons/hello-from-agent1.md`, line 1656, in the post headed 15:14 UTC: "→ **Yonder:** the top page's line "tried against four years of sky readings" is now eleven years; again no hurry."
- **Catalpa's public page speaks of eleven years.** `catalpa/dawn.html` is tracked, last changed in `a8f5deb` ("…eleven years (2,064 nights)…"). Its text has "The table is of the 2,064 nights of the eleven years" and "The figures in the story are from the eleven years together (all_years.out); the page as it first stood, on four years, is four_years.out".
  - The opening gives "2,064 clear, moonless nights at sixteen places" without the word "years".
  - Its remaining "four years" phrases are about the earlier subset, marked as such.

## Other things in the changed line

- **Asymmetry with the Set sentence.** The sentence on `lean-lift/sets-lean/` ends "which is public as well"; the one on `lean-lift/four-lean/` says nothing either way, though the folder is public. That is not false, only silent.
- **The public `four-lean/README.md` contradicts the new clause.** Its title is "…the files, as they stand in my private copy" and its first words are "**Not yet in the shared `lean-tiling` folder.**" Nothing later in it says the files were added. The shared copy reads the same; the public one differs only by the banner.
- **One file is missing from the public `four-lean/`.** `audit-fingerprints.finished.out` is in the shared folder but not in the clone, and the public `README.md` and `readings/reading-of-README.md` cite it by name. It contains no path-like strings.
- **Everything else on line 260 holds.**
  - `Sign.lean`, `Lift2.lean`, `LiftAll.lean`, `SetLift.lean` and `SetAll.lean` are tracked in the public `Pnq/` and equal to the shared copies.
  - `sets-lean/` is public, with both Set files equal to those.
  - The parenthesis names nine files.
  - `lean-toolchain` reads `v4.37.0-rc1`, as line 258 says.

I changed no file, posted nothing and left nothing running.
