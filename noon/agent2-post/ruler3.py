"""The third ruler, made after the referee showed that the first two hardly reach the cases that could catch a wrong shortcut in W
(those whose answer is "yes", at lags of 2 and more). Longer lists and lags up to 5, on small boards:
  A. lag.c against slow.py (written apart from it), on the three smallest boards;
  B. lag.c against lag-plain.c (itself with every shortcut cut out) on nine boards.
For each board, question and lag the lengths go up until the slower program takes too long.   usage: python -I ruler3.py > ruler3.out"""
import subprocess, sys, collections
from concurrent.futures import ThreadPoolExecutor
py = sys.executable
def fast(n, k, d, Q, mode):
    out = subprocess.run(["./lag-final", str(n), str(k), str(d), str(Q), mode, "-q"], input="\n", capture_output=True, text=True, timeout=1200).stdout
    return "yes" if out.startswith("yes") else "no"
def other(kind, n, k, d, Q, mode, limit):
    cmd = [py, "-I", "slow.py", str(n), str(k), str(d), str(Q), mode] if kind == "slow" else ["./lag-plain", str(n), str(k), str(d), str(Q), mode, "-q"]
    try: out = subprocess.run(cmd, input="\n", capture_output=True, text=True, timeout=limit).stdout
    except subprocess.TimeoutExpired: return None
    return "yes" if out.strip().startswith("yes") else "no"
def series(job):
    kind, n, k, Qmax, mode, d, limit = job; row = []
    for Q in range(1, Qmax + 1):
        a = other(kind, n, k, d, Q, mode, limit)
        if a is None: row.append((Q, None, None)); break
        row.append((Q, a, fast(n, k, d, Q, mode)))
    return job, row
jobs = [("slow", n, k, Qmax, mode, d, 240) for (n, k, Qmax) in ((2, 2, 7), (2, 3, 6), (3, 2, 6)) for mode in "KW" for d in range(6)]
jobs += [("plain", n, k, Qmax, mode, d, 45) for (n, k, Qmax) in ((2, 2, 9), (2, 3, 9), (3, 2, 9), (2, 4, 9), (4, 2, 9), (3, 3, 9), (2, 5, 9), (2, 6, 8), (3, 4, 8)) for mode in "KW" for d in range(6)]
tally = collections.Counter(); differ = 0
with ThreadPoolExecutor(8) as ex:
    for (kind, n, k, Qmax, mode, d, limit), row in ex.map(series, jobs):
        cells = []
        for Q, a, b in row:
            if a is None: cells.append(f"Q={Q} too slow"); tally[(kind, "left out")] += 1; continue
            cells.append(f"Q={Q} {a}/{b}" + ("" if a == b else " DIFFER")); differ += a != b; tally[(kind, mode, d, a)] += 1; tally[(kind, "agree" if a == b else "differ")] += 1
        print(f"{'A slow.py ' if kind == 'slow' else 'B lag-plain'} {n} pegs {k} colours, {mode}, lag {d}: " + "  ".join(cells), flush=True)
for kind, name in (("slow", "A. lag.c against slow.py"), ("plain", "B. lag.c against lag-plain.c")):
    print(f"\n{name}: {tally[(kind, 'agree')]} of {tally[(kind, 'agree')] + tally[(kind, 'differ')]} cases agree; {tally[(kind, 'left out')]} series stopped because the slower program took too long")
    for mode in "KW": print(f"  {mode}, cases whose answer is yes, at lags 0 to 5: " + ", ".join(str(tally[(kind, mode, d, 'yes')]) for d in range(6)) + "; whose answer is no: " + ", ".join(str(tally[(kind, mode, d, 'no')]) for d in range(6)))
print("\nDIFFERENCES: " + str(differ))
