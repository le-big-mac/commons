"""Fourth look: every place in the three round-3 texts with one of the phrases that the changes of this round may have
overtaken, with context, to be read by eye."""
import re
files = ['/home/agent3/paper/minsize.round3.tex', '/home/agent3/pq2/rule-drafts/beyond-up-sets.round3.md', '/home/agent3/door/README.round3.md']
pat = re.compile(r'on paper only|paper only|not formalised|not in Lean|Not in Lean|has not yet|not yet|no machine|118[,{]?\{?,?\}?125|still to come|'
                 r'is open|still open|are open|nothing of this section|six further|six files|nineteen|19 pages|19-page|this proof|This proof|the proof just told|not been checked', re.I)
for f in files:
    print('=' * 20, f)
    for i, line in enumerate(open(f, encoding='utf-8').read().split('\n'), 1):
        seen = -1000
        for m in pat.finditer(line):
            if m.start() - seen < 200: continue
            seen = m.start()
            a = max(0, m.start() - 170); b = min(len(line), m.end() + 200)
            print(f'{i}: ...{line[a:b]}...')
