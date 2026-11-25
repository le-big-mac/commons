"""The sheet for the blind classing: each claim as sealed, beside the passages quoted from the sources read.  No classes.
usage: python -I pairs.py > pairs.md"""
import json, re
sheet = open("expectations.md").read(); F = json.load(open("found.json")); claims = dict(re.findall(r"^(W\d+)\. \([a-z]+\) (.*?)\s+odds 0\.\d+", sheet, re.M | re.S))
print("# Sixteen claims, each beside what was found\n\nFor each claim: the passages quoted from the sources that were read (at most three), word for word. The quoted passages were checked by script against the saved text of each source. The rule for classing is at the foot.\n")
for k in sorted(F, key=lambda s: int(s[1:])):
    print(f"## {k}\n\n**The claim:** {' '.join(claims[k].split())}\n")
    for e in F[k]:
        print(f"- **Source:** {e['cite']} ({e['url']})")
        for q in e['quotes']: print(f"  - \"{q}\"")
    print()
rule = re.search(r"\"Found\":.*?within the budget\.", sheet, re.S).group(0); print("## The rule, from the sealed sheet\n\n" + ' '.join(rule.split()))
