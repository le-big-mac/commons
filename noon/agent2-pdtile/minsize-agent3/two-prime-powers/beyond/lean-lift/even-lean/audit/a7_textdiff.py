"""Text comparisons (whitespace ignored):
1. the definition ExceptionalPair and the two final statements in Pnq/EvenFinal.lean against the block in the plan;
2. exists_signs_all against this morning's exists_signs_odd (Pnq/SignFinal.lean): they should differ only by the
   name, by `(hn : not 2 | n)` and by `(hpair : not ExceptionalPair w)`;
3. S0', S1', S2' against this morning's S0, S1, S2 with F3 for C, Bad3 for BadAt, bad3Set for badSet, classSum3 for
   classSum, and the added hypotheses `(hp3 : p != 3)` and `(h3 : not 3 | d)`.
"""
import re

SK = '/home/agent3/lean/even-skeleton/Pnq/'
CP = '/home/agent3/lean/even-audit-copy/Pnq/'
PLAN = '/home/agent3/lean/even-briefs/plan.md'


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def decl(text, kw, name):
    """the statement of a declaration: from `kw name` up to ':= by' (theorems) or to the end of the body (defs)"""
    i = text.index(f"{kw} {name}")
    if kw == 'theorem':
        j = text.index(':= by', i)
        return norm(text[i:j])
    j = text.index('\n\n', i)
    return norm(text[i:j])


final = open(SK + 'EvenFinal.lean').read()
plan = open(PLAN).read()
block = plan[plan.index('```\n/-- an exceptional pair'):]
block = block[4:block.index('```', 4)]
# the plan's block has no ':= by'; cut each of its statements at the next blank line
def plan_decl(kw, name):
    i = block.index(f"{kw} {name}")
    j = block.find('\n\n', i)
    return norm(block[i:j if j != -1 else len(block)])

print("1. plan against EvenFinal.lean:")
for kw, name in (('def', 'ExceptionalPair'), ('theorem', 'exists_signs_all'),
                 ('theorem', 'not_exists_signs_of_exceptionalPair')):
    a = decl(final, kw, name)
    b = plan_decl(kw, name)
    print(f"   {name}: {'identical' if a == b else 'DIFFERENT'}")
    if a != b:
        print("     file:", a)
        print("     plan:", b)

odd = decl(open(CP + 'SignFinal.lean').read(), 'theorem', 'exists_signs_odd')
new = decl(final, 'theorem', 'exists_signs_all')
t = odd.replace('exists_signs_odd', 'exists_signs_all').replace(' (hn : ¬ 2 ∣ n)', '')
t = t.replace('(hw : ∃ x, w x ≠ 0) :', '(hw : ∃ x, w x ≠ 0) (hpair : ¬ ExceptionalPair w) :')
print("2. exists_signs_odd with the name changed, `(hn : ¬ 2 ∣ n)` removed and `(hpair : ¬ ExceptionalPair w)` added "
      "equals exists_signs_all:", t == new)
second = decl(final, 'theorem', 'not_exists_signs_of_exceptionalPair')
concl = new[new.index('∃ u v'):]
print("   the conclusion of the second final statement is `¬` of the conclusion of the first:",
      second.endswith('¬ ' + concl))

sl = open(CP + 'SignSlice.lean').read()
sc = open(CP + 'SignCount.lean').read()
sp = open(CP + 'SignPivot.lean').read()
es = open(SK + 'EvenSlice.lean').read()
ec = open(SK + 'EvenCount.lean').read()


def conv(s, newname):
    s = re.sub(r'theorem \S+', 'theorem ' + newname, s, count=1)
    s = s.replace('classSum ', 'classSum3 ').replace('BadAt ', 'Bad3 ').replace('badSet ', 'bad3Set ')
    s = s.replace('{η : ℂ}', '{η : F3}')
    s = s.replace('(hp : p.Prime) {i : ℕ}', '(hp : p.Prime) (hp3 : p ≠ 3) {i : ℕ}')
    s = s.replace('(hd : ¬ p ∣ d)', '(hd : ¬ p ∣ d) (h3 : ¬ 3 ∣ d)')
    return norm(s)


pairs = [
    ('S0 -> S0′', decl(sl, 'theorem', 'classSum_eq_of_badAt'), decl(es, 'theorem', 'classSum3_eq_of_bad3'),
     'classSum3_eq_of_bad3'),
    ('S1 -> S1′', decl(sl, 'theorem', 'badAt_of_not_live'), decl(es, 'theorem', 'bad3_of_not_live'), 'bad3_of_not_live'),
    ('S2 (a) -> S2′ pivot', decl(sc, 'theorem', 'card_badSet_mul_two_pow_card_le'),
     decl(ec, 'theorem', 'card_bad3Set_mul_two_pow_card_le'), 'card_bad3Set_mul_two_pow_card_le'),
    ('S2 -> S2′ rank', decl(sp, 'theorem', 'card_badSet_mul_two_pow_rank_le'),
     decl(ec, 'theorem', 'card_bad3Set_mul_two_pow_rank_le'), 'card_bad3Set_mul_two_pow_rank_le'),
]
print("3. this morning's statements, with F3 for ℂ, Bad3/bad3Set/classSum3 for BadAt/badSet/classSum and the two added "
      "hypotheses, against the new ones:")
for label, old, newd, nm in pairs:
    c = conv(old, nm)
    print(f"   {label}: {'identical' if c == newd else 'DIFFERENT'}")
    if c != newd:
        print("     converted:", c)
        print("     new      :", newd)
