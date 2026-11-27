"""Fourth pass: the author's search run again to 18 marks (table12/table12.out) against my search of the third pass
(evidence/third/table12check.out), and against the sentence after the table.  The author's instances are tested in whole numbers.
usage: table12compare.py AUTHORS_OUT MY_OUT"""
import sys, re
def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]
def polydivexact(a, b):
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        c = a[i + len(b) - 1] // b[-1]; q[i] = c
        for j, y in enumerate(b): a[i + j] -= c * y
    assert not any(a); return q
_phi = {}
def phi(n):
    if n in _phi: return _phi[n]
    p = [-1] + [0] * (n - 1) + [1]
    for d in divisors(n):
        if d < n: p = polydivexact(p, phi(d))
    _phi[n] = p; return p
def rem(a, b):
    a = a[:]
    for i in range(len(a) - len(b), -1, -1):
        c = a[i + len(b) - 1]
        if c:
            for j, y in enumerate(b): a[i + j] -= c * y
    return a[:len(b) - 1]
def pattern(marks):
    a = [0] * 12
    for x in marks: a[x] += 1
    return tuple(d for d in (2, 3, 4, 6, 12) if not any(rem(a, phi(d))))
def read(path, rx):
    out = {}
    for m in re.finditer(rx, open(path).read()):
        p = () if m.group(1) == 'nothing' else tuple(int(x) for x in m.group(1).strip('[]').split(','))
        out[p] = (int(m.group(2)), [int(x) for x in m.group(3).split(',')])
    return out
theirs = read(sys.argv[1], r'balance at exactly (\[[^\]]*\]|nothing): least (\d+) marks, for instance \[([^\]]*)\]')
mine = read(sys.argv[2], r'balance at exactly (\[[^\]]*\]|nothing): least (\d+); e\.g\. \[([^\]]*)\]')
print('progress lines of the author\'s run:', [l for l in open(sys.argv[1]).read().split('\n') if l.startswith('size')][-2:])
print('patterns in the author\'s output:', len(theirs), '; in mine:', len(mine))
print('least numbers that differ:', {p: (theirs[p][0], mine[p][0]) for p in theirs if theirs[p][0] != mine.get(p, (None,))[0]})
bad = [p for p, (n, inst) in theirs.items() if len(inst) != n or pattern(inst) != p]
print('the author\'s instances that do not have the stated number of marks or do not balance exactly as stated:', bad)
one_or_more = {p: n for p, (n, _) in theirs.items() if p}
print('lists of one or more of the divisors 2, 3, 4, 6, 12:', len(one_or_more), '; with least number 12 or less:', sum(1 for n in one_or_more.values() if n <= 12),
      '; the others:', {p: n for p, n in one_or_more.items() if n > 12})
