# The C enumerator against a plain Python enumeration with exact division (polylib), on small cases:
# least size for each pattern among all multisets with <= S marks that contain hour 0.
import subprocess, re
from itertools import combinations_with_replacement
from polylib import pattern_exact
for M, S in [(6, 6), (10, 10), (12, 8), (18, 6), (20, 5), (24, 5)]:
    py = {}
    n = 0
    for s in range(1, S + 1):
        for rest in combinations_with_replacement(range(M), s - 1):
            marks = (0,) + rest; n += 1
            P = pattern_exact(marks, M)
            if P not in py: py[P] = s
    out = subprocess.run(["./enum", f"table_{M}.txt", str(S), "0", "1"], capture_output=True, text=True).stdout
    c = {}
    for L in out.splitlines():
        m = re.match(r"pat(.*) \| size (\d+) \|", L)
        if m: c[frozenset(int(x) for x in m.group(1).split())] = int(m.group(2))
    nodes = int(out.splitlines()[0].split()[-1])
    print(f"clock {M}, up to {S} marks: Python {n} multisets, C {nodes}; patterns found: Python {len(py)}, C {len(c)}; least sizes {'identical' if py == c else 'DIFFERENT'}")
