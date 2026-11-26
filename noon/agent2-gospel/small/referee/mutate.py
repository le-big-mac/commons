# mutate.py -- make broken copies of the page in my folder (the page itself is not touched).
import sys
src = open('/home/agent2/gospel/double.html', encoding='utf8').read()
out = '/home/agent2/gospel/small-referee/'
muts = {
    'A-threshold-back-to-1e-6': [('S.gain < 1e-7', 'S.gain < 1e-6'), ('S.gain > 1e-7', 'S.gain > 1e-6')],
    'B-headway-constant': [('Number((n / S.gain).toPrecision(3))', 'Number((232 / S.gain).toPrecision(3))')],
    'C-millionths-only-below-2e-5': [("S.gain >= 0.0005 ? S.gain.toFixed(3)", "S.gain >= 0.00002 ? S.gain.toFixed(3)")],
    'D-second-program-sentence': [('found the same turtle and the same miss', 'found a different turtle and a smaller miss')],
}
allr = []
for name, reps in muts.items():
    t = src
    for a, b in reps:
        print(name, 'occurrences of', repr(a), ':', t.count(a))
        assert t.count(a) == 1
        t = t.replace(a, b)
    open(out + 'mutant-' + name + '.html', 'w', encoding='utf8').write(t)
    allr += reps
t = src
for a, b in allr:
    t = t.replace(a, b)
open(out + 'mutant-ALL.html', 'w', encoding='utf8').write(t)
print('written')
