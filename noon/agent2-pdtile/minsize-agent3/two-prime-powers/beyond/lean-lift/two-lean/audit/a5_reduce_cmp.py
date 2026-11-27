# compares Lean's evaluation of `reduce` (A5_reduce_eval.out) with the expected values (a5_reduce_expected.json)
import json, re
exp = json.load(open('a5_reduce_expected.json'))
got = {}
for line in open('A5_reduce_eval.out'):
    m = re.match(r'^\("case (\d+)", \[([0-9, ]*)\]\)$', line.strip())
    if m:
        got[int(m.group(1))] = [int(x) for x in m.group(2).split(',')]
bad = [e['case'] for e in exp if got.get(e['case']) != e['reduce']]
print(f"cases {len(exp)}, evaluated by Lean {len(got)}, mismatches {len(bad)} {bad}")
