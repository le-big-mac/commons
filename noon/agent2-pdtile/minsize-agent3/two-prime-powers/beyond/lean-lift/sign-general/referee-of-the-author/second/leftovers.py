"""Second look: every place in the three candidate texts that names the three Lean files for the prime 2, the folder
two-lean, the shared library, or Noon's reading / rebuilding, with some context, so that sentences still saying
"Noon has not read" or "not in the shared library" can be found by eye."""
import re, sys
files = ['/home/agent3/paper/minsize.signs-candidate.tex',
         '/home/agent3/pq2/rule-drafts/beyond-up-sets.signs-candidate.md',
         '/home/agent3/door/README.signs-candidate.md']
pat = re.compile(r'two-lean|not yet|has been asked|own copy|shared one|shared librar|shared development|shared folder|lean-two|'
                 r'Sign\.lean|Lift2|LiftAll|still to come|not read|private|proposed|eight statements|exists\\?_signs|every s|every \$s', re.I)
for f in files:
    print('=' * 20, f)
    txt = open(f, encoding='utf-8').read()
    lines = txt.split('\n')
    seen = set()
    for i, line in enumerate(lines, 1):
        for m in pat.finditer(line):
            a = max(0, m.start() - 150); b = min(len(line), m.end() + 230)
            key = (i, a // 200)
            if key in seen: continue
            seen.add(key)
            print(f'{i}: ...{line[a:b]}...')
