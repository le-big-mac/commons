"""What the fuller tables (my solver's values and the referee's programme's) say about the lines of the two sheets and about the
sub-lattices, computed from note/rows-36.json and note/rows-100.json (written by make_tables2.py).  The sheets' own scores are
out/score36.txt and out/score100.txt and are not changed by this.   usage: after_referee.py"""
import json, itertools, collections
exec(open('score100.py').read().split('def load')[0].split('import sys')[1].split('\n', 1)[1])   # rule, z20, z50 as in the sheet's scoring
def z12(D): return rule(2, 3, 2, [a for a in (1, 2) if 2 ** a in D], ([0] if 3 in D else []) + [a for a in (1, 2) if 2 ** a * 3 in D])
def z18(D): return rule(3, 2, 2, [a for a in (1, 2) if 3 ** a in D], ([0] if 2 in D else []) + [a for a in (1, 2) if 3 ** a * 2 in D])
T = {}
for M in (36, 100):
    T[M] = {frozenset(r['D']): r for r in json.load(open(f'note/rows-{M}.json'))}
    dec = {D: r['size'] for D, r in T[M].items() if r['by']}
    print(f'Z_{M}: {len(T[M])} patterns; decided {len(dec)}; distinct decided values {len(set(dec.values()))}: {sorted(collections.Counter(dec.values()).items())}')
    for name, f, top in (((12, z12, {9, 18, 36}), (18, z18, {4, 12, 36})) if M == 36 else ((20, z20, {25, 50, 100}), (50, z50, {4, 20, 100}))):
        sub = [(sorted(D), r['size'], f(D), bool(r['by'])) for D, r in T[M].items() if not (D & top)]
        d = [t for t in sub if t[3]]
        print(f'   patterns inside the divisors of {name}: {len(sub)}; decided {len(d)}; equal to the rule for Z_{name}: {sum(1 for t in d if t[1] == t[2])}; decided and different: {[t for t in d if t[1] != t[2]]}; '
              f'not decided: {[(t[0], t[1], t[2]) for t in sub if not t[3]]}  (pattern, smallest found, rule)')
    ups = [r for r in T[M].values() if r['up']]
    print(f'   up-sets {len(ups)}; decided {sum(1 for r in ups if r["by"])}; equal to the corner sum {sum(1 for r in ups if r["by"] and r["size"] == r["bound"])}')
    print(f'   decided below the bound of Corollary P: {[r["D"] for r in T[M].values() if r["by"] and r["size"] < r["bound"]]}; any found below it: {[r["D"] for r in T[M].values() if r["size"] is not None and r["size"] < r["bound"]]}; '
          f'not up-sets with size equal to the bound: {[r["D"] for r in T[M].values() if not r["up"] and r["size"] == r["bound"]]}')
tr = lambda D: frozenset({3: 5, 9: 25, 6: 10, 12: 20, 18: 50, 36: 100}.get(d, d) for d in D)
both = [(D, T[36][D]['size'], T[100][tr(D)]['size']) for D in T[36] if T[36][D]['by'] and T[100][tr(D)]['by']]
eqp = same = 0
for (D1, m1, n1), (D2, m2, n2) in itertools.combinations(both, 2):
    if m1 == m2: eqp += 1; same += (n1 == n2)
print(f'Y3 on the fuller tables: patterns decided on both {len(both)}; pairs with equal least size on Z_36: {eqp}; of these equal on Z_100 too: {same} ({100 * same / max(eqp, 1):.1f}%)')
