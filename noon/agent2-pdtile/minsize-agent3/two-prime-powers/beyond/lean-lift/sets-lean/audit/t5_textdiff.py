# t5_textdiff.py -- the three least-size statements for sets (frozen Pnq/SetAll.lean) as text, against the three audited
# statements for multisets (Pnq/LiftAll.lean, finished): after these replacements in the multiset statement
#     name  ..._mul  ->  ..._set
#     "(hpq : p ≠ q)"  ->  "(hpq : p ≠ q) (hr : r ≠ 2) (hs : r ^ j ∣ s)"
#     "∃ w : ZMod (p ^ n * q * s) → ℕ, ∑ a, w a = t"  ->  "∃ A : Finset (ZMod (p ^ n * q * s)), A.card = t"
#     "maskW w"  ->  "maskW (indW A)"
#     one more hypothesis before the colon:  (hm : <the value> < r ^ j)
# the two texts must be equal up to white space.  Also the `variable` lines of the two sections are shown.
import re, sys

SK = '/home/agent3/lean/sets-skeleton/Pnq/SetAll.lean'
OLD = '/home/agent3/lean/sets-audit-copy/Pnq/LiftAll.lean'


def stmt(text, name):
    i = text.index('theorem ' + name + ' ')
    j = text.index(':= by', i)
    return text[i:j]


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


new = open(SK).read()
old = open(OLD).read()
print("variable line (sets):     ", [l for l in new.splitlines() if l.startswith('variable')])
print("variable line (multisets):", [l for l in old.splitlines() if l.startswith('variable')][-1:])
allok = True
for base, value in [('minsize_unbalanced', 'minU p q Es Fs'), ('minsize_balanced_all', 'q * p ^ Es.card'),
                    ('minsize_balanced', 'minB p q Es Fs a0')]:
    a = norm(stmt(new, base + '_set'))
    b = norm(stmt(old, base + '_mul'))
    b = b.replace(base + '_mul', base + '_set')
    assert b.count('(hpq : p ≠ q)') == 1
    b = b.replace('(hpq : p ≠ q)', '(hpq : p ≠ q) (hr : r ≠ 2) (hs : r ^ j ∣ s)')
    assert b.count('∃ w : ZMod (p ^ n * q * s) → ℕ, ∑ a, w a = t') == 1
    b = b.replace('∃ w : ZMod (p ^ n * q * s) → ℕ, ∑ a, w a = t', '∃ A : Finset (ZMod (p ^ n * q * s)), A.card = t')
    b = b.replace('maskW w', 'maskW (indW A)')
    # the hypothesis hm goes just before the colon that ends the binders, i.e. before " : IsLeast"
    assert b.count(' : IsLeast') == 1
    b = b.replace(' : IsLeast', ' (hm : %s < r ^ j) : IsLeast' % value)
    same = (a == b)
    allok = allok and same
    print(base + '_set', ': equal to the transformed multiset statement up to white space:', same)
    if not same:
        print('  sets     :', a)
        print('  expected :', b)
# the last argument of IsLeast is the value named in hm
for base, value in [('minsize_unbalanced', 'minU p q Es Fs'), ('minsize_balanced_all', 'q * p ^ Es.card'),
                    ('minsize_balanced', 'minB p q Es Fs a0')]:
    a = norm(stmt(new, base + '_set'))
    print(base + '_set', ': ends with the value of hm:', a.endswith('(' + value + ')'), '; hm present:',
          ('(hm : %s < r ^ j)' % value) in a)
print('ALL EQUAL' if allok else 'DIFFERENCES FOUND')
