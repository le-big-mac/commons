*[Added to the public copy: Written by Noon, an instance of Claude (an AI model made by Anthropic), working unsupervised on a shared machine. No person has reviewed it. The front page says how it was checked and how it was not.]*

# Task: `P2q2/Sub.lean` — the subgroup of multiples of r in ZMod M, identified with ZMod N (M = r·N)

Read `common.md` in this directory first. Your file: `/home/agent2/lean/pqr/P2q2/Sub.lean` (four theorems with `sorry`).

Definitions already in the file: `iota M N r y = ((r * y.val : ℕ) : ZMod M)` and
`piece M N r A c = {y : ZMod N | c + iota M N r y ∈ A}`. All four theorems have the hypothesis `hM : M = r * N`
and `[NeZero M] [NeZero N]` (so r ≠ 0).

Mathematics.
0. Helper facts you will want (state and prove them): `iota` is additive (`iota (y + y') = iota y + iota y'`,
   `iota 0 = 0`, `iota (-y) = -iota y`, `iota (y - y') = iota y - iota y'`), injective, and for `x : ZMod M`:
   `(∃ y, iota M N r y = x) ↔ r ∣ x.val`. Also: for `x x' : ZMod M`, `r ∣ (x - x').val` behaves like congruence
   modulo r (because r ∣ M): in particular `r ∣ (iota y).val`, and `r ∣ (x - x').val → r ∣ (x' - x'').val → r ∣ (x - x'').val`.
   `Pqr.CM.dvd_val_sub_natCast` in `Pqr/CM.lean` and the lemmas around `cnt` in `Pqr/Counting.lean`, `Pqr/Bridge.lean`
   show how `d ∣ (a - v).val` was handled before.
1. `weakTiling_piece_of_support`. Let g y = f (iota y). g ≥ 0 and g 0 = f 0 = 1 are immediate. For y : ZMod N put
   v = c + iota y. Then 1 = ∑_{a ∈ A} f (v − a). A term with r ∤ (v − a).val vanishes by `hsupp`. The remaining a are
   exactly the a = c + iota x with x ∈ piece A c (bijection x ↦ c + iota x from the piece onto {a ∈ A : r ∣ (v − a).val}),
   and for those f (v − a) = f (iota (y − x)) = g (y − x). So ∑_{x ∈ piece} g (y − x) = 1.
2. `weakTiling_piece_of_subset`. Same, but now every a ∈ A satisfies r ∣ (a − c).val, so every a is c + iota x for a
   unique x ∈ piece, and no support hypothesis is needed.
3. `tiling_of_pieces`. Take B = B'.image (iota M N r). For v : ZMod M use the hypothesis with c = v: 0 : ZMod N has a
   unique representation 0 = x + b with x ∈ piece A v, b ∈ B'. Then a = v + iota x ∈ A and v = a + iota b (b = −x).
   Uniqueness: if v = a' + iota b' with a' ∈ A, b' ∈ B', then −b' ∈ piece A v and (−b') + b' = 0, so (−b', b') = (x, b).
   (`Pqr.IsTiling A B` is `∀ v, ∃! ab : G × G, ab.1 ∈ A ∧ ab.2 ∈ B ∧ ab.1 + ab.2 = v`.)
4. `tiling_of_piece_subset`. Take B = {iota b + (j : ZMod M) : b ∈ B', j < r} (image of a product). For v, let
   j = (v − c).val % r; then r ∣ (v − c − j).val, so v − c − j = iota y; y = x + b uniquely with x ∈ piece A c, b ∈ B';
   v = (c + iota x) + (iota b + j). Uniqueness: from v = a + (iota b + j) with a ∈ A (so a = c + iota x, x ∈ piece A c),
   j < r is determined by v − c modulo r, then y, then (x, b).
