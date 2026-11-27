"""Re-arranges the skeleton of the statement on signs into seven proof files, one job each, WITHOUT changing a statement:
every `theorem … := by\n  sorry` block (with its doc comment) is moved verbatim.
  SignSlice  S0, S1                      (unchanged)
  SignCount  S2 (a), S4 (two halves)
  SignPivot  occupied classes, S2 (b), S2, S3
  SignThree  S5
  SignSum    N1                          (unchanged)
  SignAll    A1
  SignFinal  the three final statements
usage: resplit.py FROZEN-SKELETON-DIR WORKING-COPY-DIR   (reads FROZEN/Pnq/*.lean, writes WORKING/Pnq/*.lean)"""
import sys, re, os
src, dst = sys.argv[1], sys.argv[2]
def blocks(name):
    """the theorem blocks of a file: doc comment + theorem + ':= by\\n  sorry\\n', keyed by theorem name"""
    t = open(os.path.join(src, 'Pnq', name), encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'/-- (?:(?!-/).)*?-/\ntheorem (\S+)(?:(?!\n\n).)*?:= by\n  sorry\n', t, re.S):
        out[m.group(1)] = m.group(0)
    return out
B = {}
for f in ['SignSlice.lean', 'SignCount.lean', 'SignCountB.lean', 'SignSum.lean', 'SignAll.lean']:
    b = blocks(f); assert not (set(b) & set(B)); B.update(b)
want = ['classSum_eq_of_badAt', 'badAt_of_not_live', 'card_badSet_mul_two_pow_card_le', 'rank_lt_card_image', 'exists_isPivot',
        'card_badSet_mul_two_pow_rank_le', 'rank_lt_card', 'badAt_one_iff', 'card_badSet_one', 'card_badSet_three_pow_mul_le',
        'lhsN1_lt_one', 'exists_not_badAt', 'exists_signs_odd', 'exists_lift_two_all', 'sizes_eq_two_all']
assert sorted(B) == sorted(want), sorted(B)
FIXED = "(Statements fixed on 27 November 2026, before any Lean proof of them.)"
VAR = "variable {ι : Type*} [Fintype ι]\n\n"
def write(name, head, imports, names, var=True):
    body = "/-\n" + head + "\n" + FIXED + "\n-/\n" + "".join(f"import {i}\n" for i in imports) + "\nopen Finset\n\nnamespace Pnq\n\n"
    body += (VAR if var else "") + "\n".join(B[n] for n in names) + "\nend Pnq\n"
    open(os.path.join(dst, 'Pnq', name), 'w', encoding='utf-8').write(body)
write('SignCount.lean',
      "The statement on signs for every odd `n`: two counts.  S2 (a): a pivot set `J` for the level `i` of `p` bounds the number\n"
      "of signings bad at `p^i d` by `2^(m - |J|)`.  S4: the signings bad at `1`.\n"
      "The numbers of signings are cardinalities of the finite sets `badSet e d`; `m` is `Fintype.card ι`.",
      ['Pnq.SignSlice'], ['card_badSet_mul_two_pow_card_le', 'badAt_one_iff', 'card_badSet_one'])
write('SignPivot.lean',
      "The statement on signs for every odd `n`: pivot sets and ranks.  The number of occupied classes modulo `p^j` is at least\n"
      "`(p - 1) rank + 1`; a live level has a pivot set with `(p - 1) rank` elements (S2 (b)); so a live level `i` of `p` costs a\n"
      "factor `2^((p-1) rank)` (S2); and ranks are small (S3).",
      ['Pnq.SignCount'], ['rank_lt_card_image', 'exists_isPivot', 'card_badSet_mul_two_pow_rank_le', 'rank_lt_card'])
write('SignThree.lean',
      "The statement on signs for every odd `n`: S5, the first live level of the prime `3`, counted more exactly.",
      ['Pnq.SignPivot'], ['card_badSet_three_pow_mul_le'])
write('SignAll.lean',
      "The statement on signs for every odd `n`: A1, the theorem in elements.  For an odd `n` and a nonempty finite family of\n"
      "exponents there is a signing that is bad at no `d ∣ n`.",
      ['Pnq.SignSlice', 'Pnq.SignCount', 'Pnq.SignPivot', 'Pnq.SignThree', 'Pnq.SignSum'], ['exists_not_badAt'], var=False)
write('SignFinal.lean',
      "The statement on signs for every odd `n`, and the lifting along the prime 2 for every `N`: the final statements.\n"
      "The statement on signs for multisets on `ZMod n`, `n` odd (`Lift.exists_signs` of `Pnq/Sign.lean` with `p^a * q^b`\n"
      "replaced by an odd `n`), the lemma on lifts for the prime 2 for every `N`, and the equality of the sets of sizes on\n"
      "`ZMod (N * 2)` and on `ZMod N`.  All three from A1 (`exists_not_badAt` of `Pnq/SignAll.lean`).",
      ['Pnq.SignAll', 'Pnq.Lift2'], ['exists_signs_odd', 'exists_lift_two_all', 'sizes_eq_two_all'], var=False)
os.remove(os.path.join(dst, 'Pnq', 'SignCountB.lean'))
# every block is in exactly one new file, verbatim
new = ""
for f in ['SignSlice.lean', 'SignCount.lean', 'SignPivot.lean', 'SignThree.lean', 'SignSum.lean', 'SignAll.lean', 'SignFinal.lean']:
    new += open(os.path.join(dst, 'Pnq', f), encoding='utf-8').read()
for n in want: assert new.count(B[n]) == 1, n
print('15 theorem blocks, each verbatim in exactly one of 7 files')
