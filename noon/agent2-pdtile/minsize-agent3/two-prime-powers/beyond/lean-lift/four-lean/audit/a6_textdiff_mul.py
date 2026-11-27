"""The sixteenth statement as text: against Lift.sizes_eq_odd of Pnq/LiftAll.lean (same text without the hypothesis
`(hs : Odd s)`), against the brief's and the file's own words, and against the proved file in signs-M (the fixed
statement must stand there character for character).  Reads only."""
import hashlib
import os

fixed_path = '/home/agent3/lean/signs-skeleton/SignMul.as-fixed.lean'
fixed = open(fixed_path).read()
rec = open('/home/agent3/lean/signs-skeleton/SignMul.as-fixed.sha256').read().split()[0]
print('sha256 of SignMul.as-fixed.lean equals the recorded one:', hashlib.sha256(fixed.encode()).hexdigest() == rec)


def stmt(text, name):
    a = text.index('theorem ' + name + ' ')
    b = text.index(':= by', a)
    return ' '.join(text[a:b].split())


new = stmt(fixed, 'sizes_eq_mul_all')
liftall = open('/home/agent3/lean/signs-audit-copy/Pnq/LiftAll.lean').read()
old = stmt(liftall, 'sizes_eq_odd')
old2 = old.replace('theorem sizes_eq_odd ', 'theorem sizes_eq_mul_all ').replace(' (hs : Odd s)', '')
print('sizes_eq_mul_all = sizes_eq_odd without "(hs : Odd s)", as text:', old2 == new)
if old2 != new:
    print('  ', old2)
    print('  ', new)
final = open('/home/agent3/lean/signs-skeleton/Pnq/SignFinal.lean').read()
two = stmt(final, 'sizes_eq_two_all')
new_at_2 = new.replace('theorem sizes_eq_mul_all {N : ℕ} [NeZero N] (s : ℕ) [NeZero s] ', 'theorem sizes_eq_two_all {N : ℕ} [NeZero N] ')
new_at_2 = new_at_2.replace('N * s', 'N * 2').replace('{t |', '{s |').replace('= t ∧ 0 < t', '= s ∧ 0 < s')
print('sizes_eq_mul_all with s replaced by 2 (and the set variable renamed) = sizes_eq_two_all, as text:', new_at_2 == two)
if new_at_2 != two:
    print('  ', new_at_2)
    print('  ', two)
for copy in ('/home/agent3/lean/signs-M/Pnq/SignMul.lean', '/home/agent3/lean/signs-all/Pnq/SignMul.lean'):
    if os.path.exists(copy):
        t = open(copy).read()
        a = fixed.index('/-- **Sizes are the same')
        b = fixed.index(':= by', a) + len(':= by')
        block = fixed[a:b]
        print('%s: the fixed statement with its comment stands character for character %d time(s); lines %d; '
              'lines with sorry/admit/axiom/native_decide: %d'
              % (copy, t.count(block), t.count('\n'),
                 sum(1 for l in t.split('\n') if any(w in l for w in ('sorry', 'admit', 'axiom', 'native_decide')))))
    else:
        print(copy, 'not present')
