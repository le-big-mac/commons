"""A ruler for the second sheet: on small boards, W at each lag from the numbers m(j) of name.c and the formula
    W(d) = least of N and of d + 1 + j over j <= d + 1 with m(j) <= d + 1 - j
set beside W found directly by lag.c's search. The formula speaks only when its answer is at most 2d + 2 letters (the j questions must
all be blind); elsewhere it is left blank.   usage: python -I ruler4.py > ruler4.out"""
import subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
py = sys.executable; os.makedirs("out/ruler4", exist_ok=True)
def m(n, k, j):
    pre = f"out/ruler4/pre-{n}-{k}-{j - 1}.txt"
    if not os.path.exists(pre): open(pre, "w").write(subprocess.run([py, "-I", "prefix.py", str(n), str(k), str(j - 1)], capture_output=True, text=True, check=True).stdout if j > 1 else "\n")
    out = subprocess.run(["./name", str(n), str(k), str(j)], stdin=open(pre), capture_output=True, text=True, check=True).stdout
    return int(out.strip().split("\n")[-1].split()[2])
def direct(n, k, d):
    for Q in range(1, 13):
        out = subprocess.run(["./lag-final", str(n), str(k), str(d), str(Q), "W", "-q"], input="\n", capture_output=True, text=True, timeout=900).stdout
        if out.startswith("yes"): return Q
    return None
def board(nk):
    n, k = nk; N = k ** n; ms = {0: N}; j = 0
    while ms[j] > 0 and j < 6: j += 1; ms[j] = m(n, k, j)
    rows = []
    for d in range(0, 7):
        f = min([N] + [d + 1 + j for j in ms if j <= d + 1 and ms[j] <= d + 1 - j]); f = f if f <= 2 * d + 2 else None
        try: w = direct(n, k, d)
        except subprocess.TimeoutExpired: w = "slow"
        rows.append((d, f, w))
    return nk, ms, rows
agree = total = 0
with ThreadPoolExecutor(5) as ex:
    for (n, k), ms, rows in ex.map(board, [(2, 2), (2, 3), (3, 2), (2, 4), (4, 2), (3, 3), (2, 5), (2, 6), (3, 4), (4, 3)]):
        cells = []
        for d, f, w in rows:
            if f is not None and isinstance(w, int): total += 1; agree += f == w
            cells.append(f"lag {d}: {'-' if f is None else f}/{w}" + (" DIFFER" if f is not None and isinstance(w, int) and f != w else ""))
        print(f"{n} pegs {k} colours: m(1..) = " + ", ".join(str(ms[j]) for j in sorted(ms) if j) + " | formula/search: " + "  ".join(cells), flush=True)
print(f"\n{agree} of {total} lags agree where the formula speaks (formula / lag.c's own search)")
