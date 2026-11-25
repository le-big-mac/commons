"""K and W at every lag for the small boards, each "yes" with a strategy replayed by verify.py and each "no" from a search of every opening.
usage: python -I table.py n k [maxlagW]  >  out/table/n-k.out          (4 pegs and 6 colours is done by hand: see the README)"""
import sys, subprocess, os, time
n, k = int(sys.argv[1]), int(sys.argv[2]); maxW = int(sys.argv[3]) if len(sys.argv) > 3 else 3
py = sys.executable; N = k ** n; os.makedirs("out/table", exist_ok=True)
def openings(L):
    f = f"out/table/ordered-{n}-{k}-{L}.txt"
    if not os.path.exists(f):
        raw = f"out/table/openings-{n}-{k}-{L}.txt"
        open(raw, "w").write(subprocess.run([py, "-I", "prefix.py", str(n), str(k), str(L)], capture_output=True, text=True, check=True).stdout if L else "\n")
        open(f, "w").write(subprocess.run([py, "-I", "order.py", str(n), str(k), raw], capture_output=True, text=True, check=True).stdout if L else "\n")
    return f
def ask(d, Q, mode):
    """True/False, from a run over every opening that stops at the first that works; a True is replayed by verify.py."""
    blind = min(d + 1, Q); L = min(blind, 2); ext = 0
    if mode == "K" and blind == Q and Q - L >= 2: ext = Q - L - 1          # all blind: the last guess is found directly, the others as sets
    name = f"out/table/{n}-{k}-{mode}-d{d}-Q{Q}.out"; t0 = time.time()
    out = subprocess.run(["./lag", str(n), str(k), str(d), str(Q), mode, "-s", "-q"] + (["-x", str(ext)] if ext else []), stdin=open(openings(L)), capture_output=True, text=True).stdout
    open(name, "w").write(out); yes = any(l.startswith("yes") for l in out.split("\n"))
    assert out.strip().split("\n")[-1].startswith("#"), "the run did not finish"
    note = ""
    if yes:
        v = subprocess.run([py, "-I", "verify.py", str(n), str(k), str(d), str(Q), mode, name], capture_output=True, text=True)
        assert v.returncode == 0, v.stdout; note = "replayed: " + v.stdout.strip().split("; ")[-1]
    print(f"  lag {d}, {Q} guesses, {mode}: {'yes' if yes else 'no '}  ({time.time() - t0:.1f} s) {note}", flush=True)
    return yes
print(f"{n} pegs, {k} colours, {N} codes")
K = []; d = 0
while True:
    Q = K[-1] if K else 1
    while not ask(d, Q, "K"): Q += 1
    K.append(Q)
    if d >= Q - 1: break                                                    # the list is now sent wholly blind: longer lags change nothing
    d += 1
static = K[-1]; W = []
for d in range(0, maxW + 1):
    Q = max(W[-1] if W else 1, 1)
    while not ask(d, Q, "W"): Q += 1
    W.append(Q)
Kd = lambda d: K[d] if d < len(K) else static
print(f"RESULT {n} {k} K " + " ".join(map(str, K)) + f" | blind {static} | W " + " ".join(map(str, W)) + " | W(d) <= K(d)+d+1: " + str(all(W[d] <= Kd(d) + d + 1 for d in range(len(W)))) + " | K never falls: " + str(all(K[i] <= K[i + 1] for i in range(len(K) - 1))))
