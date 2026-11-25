"""Lists every sealed line whose own text (from its label to the next label) contains a word of doubt, without outcomes.   usage: python doubts-scan.py HOME"""
import sys, re
sys.path.insert(0, '.')
H = sys.argv[1]
FILES = ['birth/expectations.md', 'battles/expectations.md', 'transits/expectations.md', 'vacancy/expectations.md', 'vacancy/meta.md', 'authors/expectations.md', 'authors2/expectations.md', 'authors2/expectations-quick.md', 'float/expectations.md', 'onset/expectations.md', 'onset/meta.md'] + [f'onset/{k}-prediction.md' for k in ('plateau', 'long', 'climb', 'dip', 'long2', 'long3', 'long4', 'long5', 'long6', 'long7')] + ['taffy/expectations.md', 'taffy/meta.md', 'impetus/expectations.md', 'aztec/expectations.md', 'aztec/corners-prediction.md', 'aztec/tw-prediction.md']
WORDS = r"Marked down|doubt|less sure|guess|memory|remember|I believe|not sure|unsure|cannot check|do not know|may never|may be|might"
n = 0
for f in FILES:
    t = open(f"{H}/{f}", encoding='utf-8').read()
    parts = re.split(r"^(?=[A-Z]+\d+\. )", t, flags=re.M)
    for p in parts[1:]:
        lab = p.split('.')[0]; body = " ".join(p.split()); n += 1
        hits = re.findall(WORDS, body)
        par = "(" in body
        if hits: print(f"{f:32s} {lab:4s} {sorted(set(hits))} :: {body[:260]}")
print(n, "blocks")
