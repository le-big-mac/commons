# compares the Lean evaluation (B_reduce_eval.out) with the expected reductions (b_reduce_expected.json)
import json, re, sys
exp = json.load(open("b_reduce_expected.json"))
seen = {"CASE": 0, "CAST": 0, "VALS": 0}; bad = 0
for line in open("B_reduce_eval.out"):
    m = re.match(r"(CASE|CAST) (\d+) (\d+) (\d+) \[(.*)\]", line)
    if m:
        kind, i, N, r = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
        got = [int(t) for t in m.group(5).split(",")] if m.group(5).strip() else []
        e = exp[i]
        assert e["N"] == N and e["r"] == r
        seen[kind] += 1
        if got != e["reduce"]:
            bad += 1; print("MISMATCH", kind, i, N, r, e["w"], "lean", got, "python", e["reduce"])
        continue
    m = re.match(r"VALS (\d+) \[(.*)\]", line)
    if m:
        N = int(m.group(1)); got = [int(t) for t in m.group(2).split(",")]
        seen["VALS"] += 1
        if got != list(range(N)):
            bad += 1; print("VALS MISMATCH", N, got)
        continue
    if line.strip():
        print("OTHER LINE:", line.rstrip()[:200])
print("cases compared:", seen, "of", len(exp), "expected; mismatches:", bad)
pairs = sorted(set((e["N"], e["r"]) for e in exp)); print("pairs (N, r):", pairs)
