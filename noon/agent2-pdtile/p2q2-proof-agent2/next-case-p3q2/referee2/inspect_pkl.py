"""Referee: structure of the published pickles (run with cwd-independent paths)."""
import pickle, sys, collections
D = '/home/agent2/p3q2/referee2/orig/'
cls = [(i, j) for i in range(4) for j in range(3)]; ords = [o for o in cls if o != (0, 0)]
allZ = {frozenset(o for i, o in enumerate(ords) if mask >> i & 1) for mask in range(1 << len(ords))}
def leaves(r, path=()):
    if r['cat'] == 'split':
        assert set(r.keys()) >= {'factor', 'pos', 'neg'}, r.keys()
        yield from leaves(r['pos'], path + ((r['factor'], 1),)); yield from leaves(r['neg'], path + ((r['factor'], -1),))
    else: yield path, r
for name in ['region_C3', 'region_Cp'] + ['split_' + b for b in ('A1a', 'A1b', 'A2', 'B1', 'B2', 'B3', 'Ap1', 'Ap2')] + ['family_2_q']:
    res = pickle.load(open(D + name + '.pkl', 'rb'))
    ok_keys = set(res.keys()) == allZ
    cats = collections.Counter(); depth = collections.Counter(); nk = collections.Counter(); factors = collections.Counter(); keys = collections.Counter(); Tmax = 0
    for Z, r in res.items():
        for path, l in leaves(r):
            cats[l['cat']] += 1; depth[len(path)] += 1
            for k in l: keys[(l['cat'], k)] += 1
            if l['cat'] == 'N':
                kind = l.get('kind', '')
                nk[kind if len(kind) < 60 else kind[:200]] += 1
            for f, s in path: factors[f] += 1
            Tmax = max(Tmax, l.get('T', 0))
    print(f"== {name}: {len(res)} patterns, all 2048 present: {ok_keys}; leaves {sum(cats.values())}; cats {dict(cats)}; depth {dict(depth)}; Tmax {Tmax}")
    print("   split factors:", dict(factors))
    if '-v' in sys.argv:
        for k, v in sorted(nk.items(), key=lambda kv: -kv[1]): print(f"   N x{v}: {k}")
        print("   keys:", sorted(set(k for (c, k) in keys if c not in ('L2', 'a'))))
