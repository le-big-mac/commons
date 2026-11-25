"""Build the table and the list of pairs for the note from the outputs of settle.py."""
import re, sys
rows = []
for fn in sys.argv[1:]:
    for line in open(fn):
        m = re.match(r"Z_(\d+) \(p = (\d+), q = (\d+)\): L2 (\d+), a (\d+), b (\d+), N (\d+), R (\d+), T (\d+), U (\d+), H (\d+);  of the \d+ open: M0 (\d+), M2 (\d+), M4 (\d+), left (\d+);  T, U, H patterns with \(T2\): (\d+)", line)
        if m: rows.append(tuple(int(v) for v in m.groups()))
rows = sorted(set(rows), key=lambda r: (r[1] > r[2], r[1], r[2]))
assert all(r[-1] == 0 and r[-2] == 0 for r in rows), [r for r in rows if r[-1] or r[-2]]
groups = {}
for r in rows: groups.setdefault(r[3:], []).append(r)
pairs = ", ".join(f"({r[1]}, {r[2]})" for r in rows)
orders = ", ".join(f"{r[0]:,}" for r in rows)
out = ["| pairs (p, q), exponent 3 on p | L2 | a | b | N | R | T | U | H | of H: M0 | M2 | M4 | left | T, U, H with (T2) |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for key, rs in sorted(groups.items(), key=lambda kv: (kv[1][0][1] > kv[1][0][2], kv[1][0][1], kv[1][0][2])):
    out.append("| " + ", ".join(f"({r[1]}, {r[2]})" for r in rs) + " | " + " | ".join(str(v) for v in key) + " |")
print(len(rows)); print(pairs); print(orders); print("\n".join(out))
