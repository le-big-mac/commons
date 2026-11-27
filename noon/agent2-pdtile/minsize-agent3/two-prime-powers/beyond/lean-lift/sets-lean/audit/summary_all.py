# summary_all.py -- the numbers quoted in audit.md, recomputed from the output files.
import json, glob, re, collections

# censuses
tot = {'set': 0, 'multi': 0}
groups = {'set': {}, 'multi': {}}
longest = (0, None)
for fn in sorted(glob.glob('census/*.json')):
    c = json.load(open(fn))
    tot[c['kind']] += c['visited']
    key = c['G']
    groups[c['kind']][key] = max(groups[c['kind']].get(key, 0), c['T'])
    if c['seconds'] > longest[0]:
        longest = (c['seconds'], fn)
print("census files:", len(glob.glob('census/*.json')))
print("sets visited (all files; a group censused to two bounds is counted twice):", tot['set'], "on", len(groups['set']), "groups")
print("  groups and bounds:", dict(sorted(groups['set'].items())))
print("multisets visited:", tot['multi'], "on", len(groups['multi']), "groups")
print("  groups and bounds:", dict(sorted(groups['multi'].items())))
print("longest single census run: %.0f s (%s)" % longest)
# without double counting: the largest bound for each group
best = {}
for fn in sorted(glob.glob('census/set_*.json')):
    c = json.load(open(fn))
    best.setdefault((c['G'], c['T']), 0)
    best[(c['G'], c['T'])] += c['visited']
uniq = sum(v for (G, T), v in best.items() if T == groups['set'][G])
print("sets visited, largest bound of each group only:", uniq)
print()

# t2
rows = json.load(open('t2_compare.json'))
for control in (False, True):
    rs = [r for r in rows if r['control'] == control]
    wc = [r for r in rs if r['Q'] > 1]
    print("%s: pairs %d (with a claim, Q > 1: %d); (t,P) with t < Q: %d; both true %d; both false %d; mismatches %d" % (
        'control' if control else 'statement', len(rs), len(wc), sum(r['claimed'] for r in rs), sum(r['true'] for r in rs),
        sum(r['false'] for r in rs), sum(len(r['mismatches']) for r in rs)))
    print("   groups G:", sorted(set(r['G'] for r in wc)))
    print("   M:", sorted(set(r['M'] for r in wc)), " s:", sorted(set(r['s'] for r in wc)))
    print("   full coverage of the claim (T >= Q-1): %d pairs; partial: %d" % (
        sum(1 for r in wc if r['T'] >= r['Q'] - 1), sum(1 for r in wc if r['T'] < r['Q'] - 1)))
    by = collections.Counter()
    for r in wc:
        f = [x for x in (3, 5, 7, 11, 13) if r['Q'] % x == 0][0]
        by[(f, r['Q'])] += 1
    print("   pairs by Q:", dict(sorted(by.items())))
    b = [r for r in rs if r['beyond_sizes'] > 0]
    print("   pairs compared beyond the claim: %d; with a difference: %d" % (len(b), sum(1 for r in b if r['nbeyond'])))
    odd = [r for r in b if r['nbeyond'] and r['Q'] > 1]
    print("   with Q > 1 and a difference at some t >= Q: %d; first differences: %s" % (
        len(odd), sorted((r['G'], r['M'], r['s'], 'Q=%d' % r['Q'], 'first t=%d' % r['first_beyond'], 'M*s=%d' % r['G']) for r in odd)))
    ev = [r for r in rs if r['Q2'] > r['Q'] and r['Q2'] > 1]
    print("   even s with 2-part above Q: %d pairs; with a difference at some Q <= t < 2-part: %s" % (
        len(ev), [(r['G'], r['M'], r['s'], r['two'][:3]) for r in ev if r['ntwo']]))
    print("   set but no multiset anywhere:", sum(1 for r in rs if r['set_no_multiset']))
print()

# t3
c = collections.Counter()
groups3 = set()
trip = set()
kinds = collections.Counter()
Vs = collections.Counter()
for l in open('t3_minsize.out'):
    m = re.match(r"G=(\d+) M=(\d+) s=(\d+) Q=(\d+) T=(\d+) \('(\w)', (\d+), (\d+), (\d+),.* V=(\d+) least=(\w+) : (.*)", l)
    if not m:
        continue
    G, M, s, Q, T, k, p, q, n, V, least, res = m.groups()
    V = int(V)
    if res.startswith('equal'):
        c['claimed, equal'] += 1
        groups3.add(int(G))
        trip.add((int(p), int(q), int(n)))
        kinds[k] += 1
        Vs[V] += 1
    elif res.startswith('open'):
        c['claimed, open'] += 1
    elif res.startswith('DISAGREE') or res.startswith('SET SMALLER'):
        c['DISAGREE'] += 1
    elif res.startswith('not claimed; equal'):
        c['not claimed, equal'] += 1
        if int(Q) > 1:
            c['not claimed with Q > 1, equal'] += 1
    elif res.startswith('not claimed; open'):
        c['not claimed, open'] += 1
    else:
        c['not claimed, differs'] += 1
print("least sizes:", dict(c))
print("   claimed and equal: groups", len(groups3), sorted(groups3))
print("   triples (p, q, n):", len(trip), sorted(trip))
print("   by statement:", dict(kinds), "; by value V:", dict(sorted(Vs.items())))
print(open('t3_minsize.out').read().split('\n\n')[-1])
