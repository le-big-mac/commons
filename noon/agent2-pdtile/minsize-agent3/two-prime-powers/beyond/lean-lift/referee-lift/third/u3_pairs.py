"""The audit's pairs of groups (two-audit/t3_compare.out): how many different pairs (N, s) are instances of at least one of the three
statements sizes_eq_two, sizes_eq_odd, sizes_eq_mul, and how the texts' "379" arises.   usage: python -I -B u3_pairs.py"""
import re, collections
kinds = collections.Counter(); per = collections.Counter(); covered = 0; total = 0
for line in open('/home/agent3/lean/two-audit/t3_compare.out', encoding='utf-8'):
    m = re.match(r'N=\s*(\d+) s=\s*(\d+) M=\s*(\d+)\s+(\S+)\s+S=', line)
    if not m: continue
    total += 1; k = m.group(4); kinds[k] += 1
    if k != 'none':
        covered += 1
        for part in k.split('+'): per[part] += 1
print('pairs in all:', total); print('by label:', dict(kinds)); print('per statement (a pair counted once for each statement it is an instance of):', dict(per), 'sum', sum(per.values()))
print('different pairs that are an instance of at least one statement:', covered, '; of none:', kinds['none'])
