"""An independent recount of the census for small periods, with the set-based code of bonds.py (different canonical form)."""
import sys, itertools, pickle
from bonds import Bond, courses, compatible, shift
plan = [tuple(int(v) for v in a.split(":")) for a in sys.argv[1:]]
seen = set()
for h, Wmax in plan:
    for w in range(2, Wmax + 1, 2):
        C = courses(w); n0 = len(seen)
        def ext(seq):
            if len(seq) == h:
                for s in range(w):
                    if compatible(seq[-1], shift(seq[0], s, w)): seen.add(Bond(w, seq, s).canon())
                return
            for J in C:
                if compatible(seq[-1], J): ext(seq + [J])
        for J in C: ext([J])
        print(f"h={h} w={w}: {len(seen) - n0} new (total {len(seen)})", flush=True)
by = {}
for k in seen: by[(k[0], k[1])] = by.get((k[0], k[1]), 0) + 1
print("bonds by least periods (w0, h0):", dict(sorted(by.items())))
