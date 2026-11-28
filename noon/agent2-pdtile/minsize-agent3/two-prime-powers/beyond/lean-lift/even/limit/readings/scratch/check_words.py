"""Reader's checks: (1) the referee's replacement wordings R1..R4 are in limits.md word for word;
(2) the Addendum and Theorem L of section 20 against limits.md; (3) arithmetic of the bounds."""
import sys, re, math
from fractions import Fraction
lim = open('/home/agent3/lean/lift-check/even/limit/limits.md', encoding='utf-8').read()
rep2 = open('/home/agent3/lean/lift-check/even/limit/referee-limits-report-2.md', encoding='utf-8').read()
note = open('/home/agent3/pq2/rule-drafts/limits-post/note.candidate.md', encoding='utf-8').read()
# (1) block quotes after R1, R2, R3
for tag in ('R1', 'R2', 'R3'):
    i = rep2.index('**' + tag + ' ')
    j = rep2.index('\n> ', i)
    k = rep2.index('\n', j + 1)
    w = rep2[j + 3:k].strip()
    print(tag, 'wording of', len(w), 'chars in limits.md:', w in lim)
# R4 quoted wordings
i = rep2.index('**R4 '); j = rep2.index('**R5 ')
blk = rep2[i:j]
for w in re.findall(r'"([^"]{12,})"', blk):
    print('R4 quoted:', repr(w[:60]), '... in limits.md:', w in lim)
# typographic quotes too
for w in re.findall(r'“([^”]{12,})”', blk):
    print('R4 quoted (curly):', repr(w[:60]), 'in limits.md:', w in lim)
# (2) Addendum
def grab(text, start, end):
    i = text.index(start); j = text.index(end, i); return text[i:j]
a_l = grab(lim, 'For every ε > 0 there are R', '\n')
s20 = note[note.index('## 20.'):note.index('## Files')]
a_n = grab(s20, 'For every ε > 0 there are R', '\n')
print('Addendum identical after its head:', a_l.strip() == a_n.strip())
t_l = grab(lim, '> **Theorem L.**', '\n'); t_n = grab(s20, '> **Theorem L.**', '\n')
print('Theorem L identical:', t_l.strip() == t_n.strip()); print(' limits.md :', t_l); print(' section 20:', t_n)
# (3) arithmetic
c = math.sqrt(2 / math.pi)
print('sqrt(2/pi) =', c, ' sqrt(pi/2) =', math.sqrt(math.pi / 2))
for k in (1.1736, 1.5916, 0.6582, 1.0131): print(k, '* sqrt(2/pi) =', k * c)
print('78764625/67108864 =', 78764625 / 67108864, ' times sqrt(2/pi):', 78764625 / 67108864 * c)
print('337/512 =', 337 / 512, ' times sqrt(2/pi):', 337 / 512 * c)
print('1.2699/sqrt(2/pi) =', 1.2699 / c, ' 0.8084/sqrt(2/pi) =', 0.8084 / c, ' 1.013062*sqrt(2/pi) =', 1.013062 * c, '1.013063*c=', 1.013063 * c)
print('2*1.2699 =', 2 * 1.2699, ' 2*0.8084 =', 2 * 0.8084)
# small values of beta(m) sqrt(m) from section 17's table
for m, b in ((2, Fraction(1, 2)), (3, Fraction(1, 4)), (4, Fraction(3, 8)), (5, Fraction(1, 4)), (6, Fraction(11, 32)), (7, Fraction(7, 32)), (8, Fraction(39, 128))):
    cm = Fraction(math.comb(m, m // 2), 2 ** m)
    print('m =', m, 'beta*sqrt(m) =', round(float(b) * math.sqrt(m), 4), ' beta/c_m =', round(float(b / cm), 4))
