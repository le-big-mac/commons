"""ruler.py -- river.c against slow.py, from the same start, through their first cutoffs.

Each case is a small valley run until several loops have been cut.  The two programs share the rules and
nothing else (see the head of slow.py).  A case agrees if, at every unit of time, the node count and the
number of cutoffs are the same, length/LX agrees to 2e-5 and the total length cut off agrees to 0.01.
(They start from the same file; the tiny differences of two ways of adding the same numbers grow as any
difference does in this model, about tenfold every four to twenty units of time, according to P.)

usage: python ruler.py [processes]
"""
import subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
cases = [  # P, DC, LX, T, seed, F0SQ or None
    (3.0, 0.4, 40, 30, 7, None), (3.0, 0.2, 40, 26, 8, None), (3.0, 0.8, 40, 26, 9, None),
    (2.0, 0.4, 40, 80, 10, None), (2.0, 0.8, 40, 80, 11, None),
    (4.5, 0.4, 30, 13, 12, None), (6.0, 0.2, 30, 8, 13, None), (6.0, 0.8, 30, 8, 14, None),
    (3.0, 0.4, 40, 30, 15, 0.1), (6.0, 0.4, 30, 10, 16, 0.5),
]
py = sys.executable
def run(case):
    P, DC, LX, T, seed, F = case
    tag = "P%g-dc%g-L%g-s%d%s" % (P, DC, LX, seed, "" if F is None else "-f%g" % F)
    start = "out/ruler/%s.start" % tag
    fopt = [] if F is None else ["-f", str(F)]
    subprocess.run(["./river", str(P), str(DC), str(LX), "0", str(seed), "-snap", "1", start], capture_output=True)
    a = subprocess.run(["./river", str(P), str(DC), str(LX), str(T), str(seed), "-start", start, "-out", "1"] + fopt, capture_output=True, text=True).stdout
    b = subprocess.run(["nice", "-n", "15", py, "-I", "slow.py", str(P), str(DC), str(LX), str(T), start, "0.1"] + ([] if F is None else [str(F)]), capture_output=True, text=True).stdout
    open("out/ruler/%s.c.out" % tag, "w").write(a); open("out/ruler/%s.slow.out" % tag, "w").write(b)
    ra = [l.split() for l in a.split("\n") if l and not l.startswith("#")]
    rb = [l.split() for l in b.split("\n") if l and not l.startswith("#")]
    ok = len(ra) == len(rb) == int(T) + 1
    worst = 0.0; rows = 0
    for u, v in zip(ra, rb):
        rows += 1
        if u[1] != v[1] or u[3] != v[3]: ok = False
        d = abs(float(u[2]) - float(v[2])); worst = max(worst, d)
        if d > 2e-5 or abs(float(u[4]) - float(v[4])) > 0.01: ok = False
    cuts = int(ra[-1][3]) if ra else -1
    return tag, ok, rows, cuts, worst
os.makedirs("out/ruler", exist_ok=True)
with ThreadPoolExecutor(int(sys.argv[1]) if len(sys.argv) > 1 else 4) as ex:
    res = list(ex.map(run, cases))
bad = 0
print("case                      rows  cutoffs  greatest difference in length/LX")
for tag, ok, rows, cuts, worst in res:
    print("%-24s %5d %8d   %.1e   %s" % (tag, rows, cuts, worst, "agree" if ok else "DIFFER")); bad += not ok
print("%d of %d cases agree; cutoffs covered: %d; cases with none: %d" % (len(res) - bad, len(res), sum(r[3] for r in res), sum(r[3] == 0 for r in res)))
