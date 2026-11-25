"""Completeness of the pages: per query, API total vs distinct ids, sort order, overlap of the two cs.CL queries, window edges."""
import sys, re, glob, os
from collections import defaultdict, Counter

data = sys.argv[1]
entry_re = re.compile(r"<entry>(.*?)</entry>", re.S)
id_re = re.compile(r"<id>\s*http://arxiv\.org/abs/(.+?)v(\d+)\s*</id>")
pub_re = re.compile(r"<published>\s*([^<]+?)\s*</published>")
cat_re = re.compile(r"<arxiv:primary_category[^>]*\bterm=\"([^\"]+)\"")
tot_re = re.compile(r"<opensearch:totalResults[^>]*>(\d+)<")
q = defaultdict(list)   # query -> list of (id, published, primary) in page order
tots = defaultdict(set)
for f in sorted(glob.glob(os.path.join(data, "*.xml"))):
    name = os.path.basename(f).rsplit("-", 1)[0]
    t = open(f, encoding="utf-8", errors="replace").read()
    tots[name].add(int(tot_re.search(t).group(1)))
    for m in entry_re.finditer(t):
        e = m.group(1)
        q[name].append((id_re.search(e).group(1), pub_re.search(e).group(1), cat_re.search(e).group(1)))
print("query        API total(s)  entries  distinct  out-of-order steps  first published        last published         primary==query")
for name, L in q.items():
    ids = [x[0] for x in L]
    ooo = sum(1 for a, b in zip(L, L[1:]) if b[1] < a[1])
    base = name.replace(".late", "")
    print(f"{name:12s} {sorted(tots[name])}  {len(L):6d}  {len(set(ids)):6d}  {ooo:4d}   {L[0][1]}  {L[-1][1]}  {sum(1 for x in L if x[2] == base)}")
a = set(x[0] for x in q["cs.CL"]); b = set(x[0] for x in q["cs.CL.late"])
print("cs.CL: first query distinct", len(a), "late distinct", len(b), "overlap", len(a & b), "union", len(a | b))
la = max(x[1] for x in q["cs.CL"]); fb = min(x[1] for x in q["cs.CL.late"])
print("cs.CL first query ends", la, "; late query begins", fb)
# every paper of first query published >= late begin must be in late query
miss = [x for x in q["cs.CL"] if x[1] >= fb and x[0] not in b]
print("first-query papers stamped at or after the late query's start but absent from it:", len(miss))
# papers in late query earlier than first query's end but absent from first query
miss2 = [x for x in q["cs.CL.late"] if x[1] < la and x[0] not in a]
print("late-query papers stamped before the first query's end but absent from it:", len(miss2))
# window edges
allp = {}
for name, L in q.items():
    for i, p, c in L:
        allp[i] = p
out = [p for p in allp.values() if not ("2025-01-01T00:00:00Z" <= p <= "2025-06-30T23:59:59Z")]
print("distinct ids", len(allp), "; published outside the half-year:", len(out), sorted(out)[:3], sorted(out)[-3:])
print("stamped 2025-06-30T23:59:xx:", sorted(p for p in allp.values() if p.startswith("2025-06-30T23:59")), " latest:", max(allp.values()), " earliest:", min(allp.values()))
print("stamped in second :00 of 00:00 on Jan 1:", sorted(p for p in allp.values() if p.startswith("2025-01-01T00:0"))[:5])
