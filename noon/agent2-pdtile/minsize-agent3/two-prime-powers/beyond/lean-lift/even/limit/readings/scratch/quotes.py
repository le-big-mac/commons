import re
note = open('/home/agent3/pq2/rule-drafts/limits-post/note.candidate.md', encoding='utf-8').read()
i18 = note.index('## 18.'); i19 = note.index('## 19.'); i20 = note.index('## 20.'); iF = note.index('## Files')
s18 = note[i18:i19]; s20 = note[i20:iF]
p = s20[s20.index('**What it changes above.**'):]
for q in re.findall(r'"([^"]+)"', p):
    print(repr(q[:70]), '-> in section 18:', q in s18)
lim = open('/home/agent3/lean/lift-check/even/limit/limits.md', encoding='utf-8').read()
for q in re.findall(r'"([^"]+)"', s20[:s20.index('**How.**')]):
    print(repr(q[:70]), '-> in limits.md:', q in lim, '| in section 18:', q in s18)
r1 = open('/home/agent3/lean/lift-check/even/limit/referee-limits-report.md', encoding='utf-8').read()
for q in ['means bounded for each ε', 'The comparison is up to ε·c_m, so it says nothing about multisets whose share is far below c_m', 'compares B with the number K_π(D′)·c_(m−r)', 'up to a factor', 'not with the share of an actual multiset']:
    print(repr(q), '| referee report 1:', q in r1, '| section 20:', q in s20, '| limits.md:', q in lim)
