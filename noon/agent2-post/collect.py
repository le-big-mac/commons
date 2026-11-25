"""Every run behind the table for 4 pegs and 6 colours, made again with the program as it now stands (the two long ones are read from the
files par.sh left), each "yes" replayed by verify.py.   usage: python -I collect.py > collect.out     Writes results-4-6.json."""
import subprocess, sys, json, hashlib, os, re, time, math
py = sys.executable; os.makedirs("out/final", exist_ok=True)
RUNS = [  # question, lag, guesses, openings file, options, expected kind, long?
    ("K", 0, 3, "openings-4-6-1.txt", ["-a"], False), ("K", 0, 4, "openings-4-6-1.txt", ["-s"], False),
    ("K", 1, 4, "ordered-4-6-2.txt", ["-a"], False), ("K", 1, 5, "ordered-4-6-2.txt", ["-s"], False),
    ("K", 2, 4, "ordered-4-6-3.txt", ["-a", "-q"], False), ("K", 2, 5, "ordered-4-6-3.txt", ["-s"], False),
    ("K", 3, 4, "ordered-4-6-2.txt", ["-x", "1", "-a", "-q"], False), ("K", 3, 5, "ordered-4-6-2.txt", ["-x", "2", "-s", "-q"], False),
    ("K", 4, 5, "ordered-4-6-2.txt", ["-x", "2", "-a", "-q"], True),
    ("W", 0, 4, "openings-4-6-1.txt", ["-a"], False), ("W", 0, 5, "openings-4-6-1.txt", ["-s"], False),
    ("W", 1, 5, "ordered-4-6-2.txt", ["-a"], False), ("W", 1, 6, "ordered-4-6-2.txt", ["-a"], False), ("W", 1, 7, "ordered-4-6-2.txt", ["-s"], False),
    ("W", 2, 7, "ordered-4-6-3.txt", ["-a", "-q"], False), ("W", 2, 8, "ordered-4-6-3.txt", ["-s"], False),
    ("W", 3, 8, "ordered-4-6-3.txt", ["-a", "-q"], True), ("W", 3, 9, "out/quad.txt", ["-s"], False),
    ("W", 4, 9, "ordered-4-6-3.txt", ["-a", "-q"], True), ("W", 4, 10, "out/quad.txt", ["-s"], False),
    ("W", 5, 11, "out/quad.txt", ["-s"], False), ("W", 6, 12, "out/quad.txt", ["-s"], False)]
res = {"lag.c sha256": hashlib.sha256(open("lag.c", "rb").read()).hexdigest(), "runs": []}
print("lag.c sha256", res["lag.c sha256"])
for mode, d, Q, ops, opt, long in RUNS:
    name = f"out/{mode}-d{d}-Q{Q}.out" if long else f"out/final/{mode}-d{d}-Q{Q}.out"; t0 = time.time()
    if not long: open(name, "w").write(subprocess.run(["./lag", "4", "6", str(d), str(Q), mode] + opt, stdin=open(ops), capture_output=True, text=True).stdout)
    txt = open(name).read(); sums = re.findall(r"^# .*?: (\d+) openings tried, (\d+) work", txt, re.M); assert sums, name
    tried, work = sum(int(a) for a, _ in sums), sum(int(b) for _, b in sums); row = dict(question=mode, lag=d, guesses=Q, file=name, openings=ops, options=" ".join(opt), tried=tried, work=work)
    if work:
        v = subprocess.run([py, "-I", "verify.py", "4", "6", str(d), str(Q), mode, name], capture_output=True, text=True); assert v.returncode == 0, v.stdout
        row["replayed"] = v.stdout.strip(); row["opening"] = re.search(r"^yes (.*)$", txt, re.M).group(1)
    else:
        lines = sum(1 for _ in open(ops)); per = math.comb(1296, int(opt[opt.index("-x") + 1])) if "-x" in opt else 1; assert tried == lines * per, (name, tried, lines * per); row["every opening"] = True
    res["runs"].append(row)
    print(f"{mode} lag {d}, {Q} guesses: {tried} openings tried, {work} work" + (f"; first that works: {row['opening']}; {row['replayed'].split('; ')[-1]}" if work else "; every opening in the file was tried") + ("" if long else f"  ({time.time() - t0:.0f} s)"), flush=True)
lst = "out/K-static-Q6.out"; v = subprocess.run([py, "-I", "verify.py", "4", "6", "5", "6", "K", lst], capture_output=True, text=True); assert v.returncode == 0
res["runs"].append(dict(question="K", lag=5, guesses=6, file=lst, tried=1, work=1, replayed=v.stdout.strip(), opening=" ".join(l.split(":")[1] for l in open(lst).read().splitlines() if l.startswith("S "))))
print("K lag 5 and more, 6 guesses: a blind list found by static.py; " + v.stdout.strip().split("; ")[-1])
json.dump(res, open("results-4-6.json", "w"), indent=1)
