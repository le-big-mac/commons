"""Referee: my own category counts (mylp, order b, N, R, T, U, H as in the author's exact.py) against the author's settle72.out, pair by pair."""
import re, glob
S = {}
for line in open('/srv/commons/agent2-pdtile/p2q2-proof-agent2/next-case-p3q2/settle72.out'):
    m = re.match(r"Z_\d+ \(p = (\d+), q = (\d+)\): L2 (\d+), a (\d+), b (\d+), N (\d+), R (\d+), T (\d+), U (\d+), H (\d+);  of the \d+ open: M0 (\d+), M2 (\d+), M4 (\d+), left (\d+);  T, U, H patterns with \(T2\): (\d+)", line)
    if m: g = [int(v) for v in m.groups()]; S[(g[0], g[1])] = g[2:]
mine = {}
for f in glob.glob('/home/agent2/p3q2/referee2/out/recheck_*.out'):
    for line in open(f):
        m = re.match(r"\S+ \((\d+), (\d+)\): mine \[L2 (\d+), a (\d+), b (\d+), N (\d+), R (\d+), T (\d+), U (\d+), H (\d+); H: M0 (\d+), M2 (\d+), M4 (\d+), left (\d+); T,U,H with \(T2\): (\d+)\]", line)
        if m: g = [int(v) for v in m.groups()]; mine[(g[0], g[1])] = g[2:]
both = [k for k in S if k in mine]; diff = [k for k in both if S[k] != mine[k]]
print(f"settle72.out has {len(S)} pairs; I recomputed {len(both)} of them; differences in the counts (L2, a, b, N, R, T, U, H, M0, M2, M4, left, TUH with T2): {len(diff)} {diff[:5]}")
print("pairs of settle72.out not recomputed:", sorted(k for k in S if k not in mine))
print("the six direct pairs:", {k: (mine.get(k), S.get(k) == mine.get(k)) for k in [(2, 3), (2, 5), (2, 7), (3, 2), (3, 5), (3, 11)]})
allp = len(mine); print(f"all pairs recomputed: {allp}; with left > 0: {sum(1 for v in mine.values() if v[11])}; with a T, U or H pattern satisfying (T2): {sum(1 for v in mine.values() if v[12])}")
