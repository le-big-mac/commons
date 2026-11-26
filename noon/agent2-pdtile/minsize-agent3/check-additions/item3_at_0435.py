"""Is the 199 of item (3) a count of the final state or of 04:35?  The rows of the five runs of the three larger groups
are cut off at 04:35:09 (start of a run = time of its .err file in the author's working folder, a row's time = start +
running sum of 'seconds', as the referee's recount did), and the patterns of item (3) are counted again.
usage: item3_at_0435.py OUT_DIR ERR_DIR"""
import sys, json, os, glob, re, collections, datetime
od, ed = sys.argv[1], sys.argv[2]
CUT = 4 * 3600 + 35 * 60 + 9
def rows(path, cut):
    name = os.path.basename(path).replace('.part', '')
    out = {}
    start = None
    if cut:
        st = os.stat(os.path.join(ed, name + '.err')).st_mtime
        d = datetime.datetime.fromtimestamp(st, datetime.timezone.utc); start = d.hour * 3600 + d.minute * 60 + d.second + d.microsecond / 1e6
    t = 0.0
    for l in open(path):
        if not l.startswith('{'): continue
        r = json.loads(l); t += r['seconds']
        if cut and start + t > CUT: break
        out[frozenset(r['E']), frozenset(r['F'])] = r
    return out
dec = lambda r: r['min'] is not None and not r['undecided']
for label, cutting in (('at 04:35:09', True), ('final state', False)):
    table = {}; per = {}
    for path in sorted(glob.glob(os.path.join(od, 'n*-multi-*.jsonl*'))):
        m = re.fullmatch(r'n(\d+)-p(\d+)-q(\d+)-multi-(cpsat|highs)\.jsonl(\.part)?', os.path.basename(path))
        if not m: continue
        n, p, q = int(m[1]), int(m[2]), int(m[3])
        late = (n == 3 and p ** n * q in (135, 250, 375))
        R = rows(path, cutting and late)
        for k, r in R.items():
            if dec(r): table.setdefault((n, p, q) + k, set()).add(r['solver'])
    for g in ((3, 3, 5), (3, 5, 2), (3, 5, 3)):
        ks = [k for k in table if k[:3] == g]
        per[g] = (len(ks), sum(1 for k in ks if len(table[k]) == 2))
    cnt = sum(1 for (n, p, q, E, F) in table if 0 in F and any(a >= 1 and a not in E and any(b not in F for b in range(1, a)) for a in F))
    print(f"{label}: decided {len(table)}; orders 135, 250, 375 decided (by both): {per[(3, 3, 5)]}, {per[(3, 5, 2)]}, {per[(3, 5, 3)]}; patterns of item (3): {cnt}")
