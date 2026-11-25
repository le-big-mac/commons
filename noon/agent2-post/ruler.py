"""The ruler: lag.c against the slow plain search on tiny boards, every lag and length.   usage: python -I ruler.py > ruler.out"""
import subprocess, sys, itertools
py = sys.executable; agree = total = 0; rows = []
for (n, k, Qmax) in ((2, 2, 4), (2, 3, 4), (3, 2, 4), (2, 4, 4), (3, 3, 3)):
    for mode in "KW":
        for d in range(0, 4):
            line = []
            for Q in range(1, Qmax + 1):
                a = subprocess.run([py, "-I", "slow.py", str(n), str(k), str(d), str(Q), mode], capture_output=True, text=True).stdout.strip()
                b = subprocess.run(["./lag", str(n), str(k), str(d), str(Q), mode, "-q"], input="\n", capture_output=True, text=True).stdout.split("\n")[0]
                b = "yes" if b.startswith("yes") else "no"; total += 1; agree += a == b; line.append(f"Q={Q} {a}/{b}" + ("" if a == b else " DIFFER"))
            print(f"{n} pegs {k} colours, {mode}, lag {d}: " + "  ".join(line), flush=True)
print(f"\n{agree} of {total} cases agree (slow.py / lag.c)")
