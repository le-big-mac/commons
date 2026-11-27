# The three least-size statements of Pnq/LiftAll.lean against the three of Pnq/LiftMin.lean (finished, audited before), as text:
# after renaming  _lift -> _mul,  the set variable s -> t,  the group factor r -> s,  and removing the binders
# "(p q n r : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime]" (which in LiftAll.lean are the section variables
# "(p q n s : ℕ) [Fact p.Prime] [Fact q.Prime] [NeZero s]") and the hypothesis "(hr : r ≠ 2)", the texts must be identical.
# Likewise sizes_eq_two / sizes_eq_odd / sizes_eq_mul against sizes_eq of Pnq/Lift.lean.
import re, sys
SK = '/home/agent3/lean/two-skeleton/Pnq/'
CP = '/home/agent3/lean/two-audit-copy/Pnq/'

def stmt(path, name):
    s = open(path).read()
    i = s.index('theorem ' + name + ' ')
    j = s.index(':= by', i)
    return ' '.join(s[i:j].split())

ok = True
for a, b in [('minsize_unbalanced', 'U'), ('minsize_balanced_all', 'A'), ('minsize_balanced', 'B')]:
    old = stmt(CP + 'LiftMin.lean', a + '_lift')
    new = stmt(SK + 'LiftAll.lean', a + '_mul')
    t = old.replace(a + '_lift', a + '_mul')
    t = t.replace('(p q n r : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime] ', '').replace(' (hr : r ≠ 2)', '')
    t = t.replace('{s | ', '{t | ').replace('= s ∧', '= t ∧').replace('0 < s ∧', '0 < t ∧')
    t = t.replace('p ^ n * q * r', 'p ^ n * q * s')
    same = (t == new)
    ok &= same
    print(f"{a}_mul against {a}_lift after the renaming: {'identical' if same else 'DIFFERENT'}")
    if not same:
        print('  old:', t); print('  new:', new)
old = stmt(CP + 'Lift.lean', 'sizes_eq')
body_old = old[old.index('{s |'):]
for name, big in [('sizes_eq_two', 'N * 2'), ('sizes_eq_odd', 'N * s'), ('sizes_eq_mul', 'p ^ n * q * s')]:
    new = stmt(SK + ('Lift2.lean' if name == 'sizes_eq_two' else 'LiftAll.lean'), name)
    k = min(i for i in (new.find('{s |'), new.find('{t |')) if i >= 0)
    body_new = new[k:]
    t = body_old.replace('N * r', big)
    if name != 'sizes_eq_two':
        t = t.replace('{s | ', '{t | ').replace('= s ∧', '= t ∧').replace('0 < s ∧', '0 < t ∧')
    if name == 'sizes_eq_mul':
        t = t.replace('ZMod N ', 'ZMod (p ^ n * q) ').replace('d ∣ N →', 'd ∣ p ^ n * q →')
    same = (t == body_new)
    ok &= same
    print(f"{name}: the equation of the two sets against that of sizes_eq with N * r -> {big}: {'identical' if same else 'DIFFERENT'}")
    if not same:
        print('  old:', t); print('  new:', body_new)
    print('   binders and hypotheses:', new[:k].strip())
print('all identical:', ok)
