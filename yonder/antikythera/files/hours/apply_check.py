"""Apply the reader's changes (check-scripts/changes.json) to README.md, each old string exactly once, in the reader's own words.
usage: apply_check.py   (under -I)"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(HERE, 'README.md'), encoding='utf-8').read()
ch = json.load(open(os.path.join(HERE, 'check-scripts', 'changes.json'), encoding='utf-8'))
for c in ch:
    assert t.count(c['old']) == 1, (c['id'], t.count(c['old']))
    t = t.replace(c['old'], c['new'])
open(os.path.join(HERE, 'README.md'), 'w', encoding='utf-8').write(t)
print('applied', len(ch), 'changes;', len(t.split()), 'words')
