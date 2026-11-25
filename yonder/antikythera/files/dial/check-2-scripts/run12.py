"""Third reading, step 1: were the nineteen changes of check-2.md applied to README.md as worded?
For every quoted 'New:' text in section 3 of check-2.md, split it into sentences and report the sentences NOT found
(whitespace-normalised) in README.md.  usage: run12.py CHECK2 README SECONDREAD"""
import sys, re
c2, readme, second = (open(p, encoding='utf-8').read() for p in sys.argv[1:4])
norm = lambda s: re.sub(r'\s+', ' ', s).strip()
R = norm(readme); S2 = norm(second)
sec = c2[c2.index('## 3. Changes I would make'):c2.index('## 4. What I could not check')]
items = re.split(r'\n(?=\d+\. \*\*)', sec)
for it in items[1:]:
    head = it.split('\n')[0]
    news = re.findall(r'(?:New[^:]*:|add|insert:|Add) "(.*?)"(?=\n|\.?$|\.\n)', it, flags=re.S)
    missing = []
    for new in news:
        new = norm(new).replace('**', '')
        for sent in re.split(r'(?<=[.;:]) ', new):
            sent = sent.strip()
            if len(sent) < 25: continue
            if sent not in R.replace('**', ''): missing.append(sent)
    print(f'{head[:60]:62s} quoted new texts: {len(news)}; sentences not found verbatim in README: {len(missing)}')
    for m in missing: print('      NOT FOUND:', m[:260])
# also: every "Old:" text should be gone from README
olds = re.findall(r'Old: "(.*?)"\n', sec, flags=re.S)
for o in olds:
    o = norm(o)
    print(('still present ' if o in R else 'gone          ') + '| old: ' + o[:90])
