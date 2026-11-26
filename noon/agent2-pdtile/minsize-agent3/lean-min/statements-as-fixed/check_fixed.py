"""Every fixed declaration of a skeleton file must stand, character for character and exactly once, in the finished file.
A fixed declaration: for a theorem, the text from `theorem NAME` up to and including `:= by`; for a def, the text from
its `def` line up to the next blank line.  Also greps the finished file for escape hatches.
usage: check_fixed.py SKELETON.lean FINISHED.lean [MORE_FINISHED.lean ...]   (extra files are only grepped)"""
import sys, re
sk = open(sys.argv[1]).read(); fin = open(sys.argv[2]).read()
blocks = []
for m in re.finditer(r'^(?:noncomputable )?(theorem|def) (\S+)', sk, re.M):
    rest = sk[m.start():]
    if m.group(1) == 'theorem':
        j = rest.index(':= by'); blocks.append((m.group(2), rest[:j + len(':= by')]))
    else:
        j = rest.find('\n\n'); blocks.append((m.group(2), rest[:j if j >= 0 else len(rest)]))
bad = 0
for name, b in blocks:
    n = fin.count(b)
    if n != 1: bad += 1; print('  CHANGED OR MISSING:', name, '(found', n, 'times)')
print(f'{sys.argv[2]}: {len(blocks)} fixed declarations, {len(blocks) - bad} stand character for character, each once')
for f in sys.argv[2:]:
    t = open(f).read(); hits = [(i + 1, l.strip()[:90]) for i, l in enumerate(t.split('\n')) if re.search(r'\b(sorry|admit|native_decide|unsafe|opaque|implemented_by)\b|^\s*axiom\b|set_option', l)]
    print(f'{f}: {len(t.splitlines())} lines; lines with sorry, admit, axiom, native_decide, unsafe, opaque, implemented_by or set_option: {len(hits)}', hits[:5] if hits else '')
sys.exit(1 if bad else 0)
