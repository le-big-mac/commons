# a compact table of t4_minsize.out by (p, q, n), over the factors s > 1
import re
agg = {}
for line in open('t4_minsize.out'):
    m = re.match(r'^(\d+) (\d+) (\d+) +(\d+) \| Z_(\d+) *\| +(\d+) \((\d+)/(\d+)/(\d+)\) \| +(\d+) \| S= *(\d+) \(base Z_\d+: +(\d+)\) \| +(\d+) \| +(\d+) \| +(\d+) \| +(\d+) \| (\d+)', line)
    if not m:
        continue
    g = [int(x) for x in m.groups()]
    p, q, n, s = g[:4]
    if s == 1:
        continue
    a = agg.setdefault((p, q, n), dict(s=[], inst=0, exact=0, lifted=0, open=0, vmax=g[9], each=g[5]))
    a['s'].append(s); a['inst'] += g[5]; a['exact'] += g[12]; a['lifted'] += g[13]; a['open'] += g[15]
print("| p | q | n | base group | factors s tried | instances for each s | largest Lean value | instances over all s | exact by the census of the big group | beyond it: member lifted from an exhaustively least base member | beyond both censuses (see t5) |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for (p, q, n), a in sorted(agg.items(), key=lambda kv: (kv[0][2], kv[0][0] ** kv[0][2] * kv[0][1], kv[0][0])):
    print(f"| {p} | {q} | {n} | Z_{p ** n * q} | {', '.join(map(str, a['s']))} | {a['each']} | {a['vmax']} | {a['inst']} | {a['exact']} | {a['lifted']} | {a['open']} |")
print("totals:", sum(a['inst'] for a in agg.values()), sum(a['exact'] for a in agg.values()), sum(a['lifted'] for a in agg.values()),
      sum(a['open'] for a in agg.values()))
