"""Do the hand-typed outcomes agree with the published scorecards?   usage: python -I checkoutcomes.py outcomes.json COMMONSDIR
The verdict of a scorecard row is its last cell: 'half' or a held/failed split or 'held by the letter only' is 0.5;
otherwise the first word in bold."""
import sys, re, json
out = json.load(open(sys.argv[1]))
found = {}
for d in ('antipodes', 'voices', 'trails', 'snowdrops', 'atlantic', 'clinch', 'pacing', 'plurality', 'aroma'):
    try:
        lines = open(f'{sys.argv[2]}/agent2-{d}/README.md', encoding='utf-8').read().split('\n')
    except FileNotFoundError:
        print("no README yet for", d)
        continue
    for line in lines:
        m = re.match(r"^\|\s*([A-Z]\d+)\s*\|(.*)\|\s*$", line)
        if not m:
            continue
        last = m.group(2).split('|')[-1].lower()
        bold = re.findall(r"\*\*([a-z ]+)\*\*", last)
        if 'half' in last or 'by the letter only' in last:
            v = 0.5
        elif bold and bold[0].startswith('held'):
            v = 1.0
        elif bold and bold[0].startswith('failed'):
            v = 0.0
        else:
            v = None
        found[m.group(1)] = v
bad = [(k, out[k], found.get(k)) for k in out if k in found and found[k] != out[k]]
print(len(found), "scorecard rows read;", len([k for k in out if k not in found]), "outcomes without a published row;", len(bad), "disagree:", bad)
