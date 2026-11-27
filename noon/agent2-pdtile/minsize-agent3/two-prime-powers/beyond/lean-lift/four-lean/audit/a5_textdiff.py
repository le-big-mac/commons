"""Text comparison of the final statements: with the plan's fixed block, and with the audited statements of
Pnq/Sign.lean and Pnq/Lift2.lean (same text after removing the hypotheses on p, q, k, a, b)."""
import re
import sys

skel = '/home/agent3/lean/signs-skeleton/Pnq/'
copy = '/home/agent3/lean/signs-audit-copy/Pnq/'
plan = open('/home/agent3/lean/signs-briefs/plan.md').read()


def stmt(text, name):
    """the text from 'theorem name' up to ':= by'"""
    a = text.index('theorem ' + name + ' ')
    b = text.index(':= by', a)
    return ' '.join(text[a:b].split())


final = open(skel + 'SignFinal.lean').read()
block = plan[plan.index('```lean') + 7: plan.index('```', plan.index('```lean') + 7)]


def stmt_plan(name):
    a = block.index('theorem ' + name + ' ')
    rest = block[a:]
    nxt = rest.find('theorem ', 8)
    return ' '.join((rest if nxt < 0 else rest[:nxt]).split())


for name in ('exists_signs_odd', 'exists_lift_two_all'):
    s1 = stmt(final, name).replace('Lift.reduce', 'reduce')
    s2 = stmt_plan(name)
    print('%s: skeleton text equals the plan\'s block (up to spaces and the prefix "Lift."): %s' % (name, s1 == s2))
    if s1 != s2:
        print('   skeleton:', s1)
        print('   plan    :', s2)

sign = open(copy + 'Sign.lean').read()
lift2 = open(copy + 'Lift2.lean').read()
old = stmt(sign, 'exists_signs')
new = stmt(final, 'exists_signs_odd')
old2 = old.replace('theorem exists_signs (p q : ℕ) [Fact p.Prime] [Fact q.Prime] (hp : p ≠ 2) (hq : q ≠ 2) (hpq : p ≠ q) (a b : ℕ)',
                   'theorem exists_signs_odd (n : ℕ) [NeZero n] (hn : ¬ 2 ∣ n)').replace('(p ^ a * q ^ b)', 'n').replace('p ^ a * q ^ b', 'n')
print('exists_signs_odd = exists_signs with the head replaced and p ^ a * q ^ b -> n:', old2 == new)
if old2 != new:
    print('  ', old2); print('  ', new)
old = stmt(lift2, 'exists_lift_two')
new = stmt(final, 'exists_lift_two_all').replace('Lift.reduce', 'reduce')
old2 = old.replace('theorem exists_lift_two ', 'theorem exists_lift_two_all ').replace(
    ' (p q : ℕ) [Fact p.Prime] [Fact q.Prime] (hp : p ≠ 2) (hq : q ≠ 2) (hpq : p ≠ q) (k a b : ℕ) (hN : N = 2 ^ k * (p ^ a * q ^ b))', '')
print('exists_lift_two_all = exists_lift_two without its hypotheses on p, q, k, a, b:', old2 == new)
if old2 != new:
    print('  ', old2); print('  ', new)
old = stmt(lift2, 'sizes_eq_two')
new = stmt(final, 'sizes_eq_two_all')
old2 = old.replace('theorem sizes_eq_two ', 'theorem sizes_eq_two_all ').replace(
    ' (p q : ℕ) [Fact p.Prime] [Fact q.Prime] (hp : p ≠ 2) (hq : q ≠ 2) (hpq : p ≠ q) (k a b : ℕ) (hN : N = 2 ^ k * (p ^ a * q ^ b))', '')
print('sizes_eq_two_all = sizes_eq_two without its hypotheses on p, q, k, a, b:', old2 == new)
if old2 != new:
    print('  ', old2); print('  ', new)
# every file of the skeleton and of the copy has "sorry" exactly as the proof of each theorem; count them
import os
for f in sorted(os.listdir(skel)):
    t = open(skel + f).read()
    same = t == open(copy + f).read()
    print('%-16s theorems %d, sorry %d, identical in the audit copy: %s' % (f, len(re.findall(r'^theorem ', t, re.M)), len(re.findall(r'^\s*sorry\s*$', t, re.M)), same))
