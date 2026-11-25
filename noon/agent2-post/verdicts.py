"""Score the sealed sheet from the result files.   usage: python -I verdicts.py > verdicts.out"""
import json, re, glob
R = json.load(open("results-4-6.json"))["runs"]
def works(q, d, Q):
    r = [x for x in R if x["question"] == q and x["lag"] == d and x["guesses"] == Q]; assert len(r) == 1, (q, d, Q); r = r[0]
    assert r["work"] > 0 or r.get("every opening"), r; return r["work"] > 0
def least(q, d, lo, hi):
    """the least number of guesses that works, read off the runs: needs a 'no' just below a 'yes'"""
    for Q in range(lo, hi + 1):
        if works(q, d, Q): return Q
    raise SystemExit(f"no run settles {q} at lag {d}")
K46 = [least("K", 0, 3, 4), least("K", 1, 4, 5), least("K", 2, 4, 5), least("K", 3, 4, 5), None]
# Lag 4 and more: five guesses are then all blind and fail; six blind guesses work at any lag.
assert not works("K", 4, 5) and works("K", 5, 6); K46[4] = 6
W46 = [least("W", 0, 4, 5), least("W", 1, 5, 7), least("W", 2, 7, 8), least("W", 3, 8, 9)]
W4 = least("W", 4, 9, 10); assert works("W", 5, 11) and works("W", 6, 12)          # lag 4 by search; lags 5 and 6: lag + 6 guesses are enough
boards = {}
for f in sorted(glob.glob("out/table/*-*.out")):
    m = re.search(r"^RESULT (\d) (\d) K ([\d ]+) \| blind (\d+) \| W ([\d ]+) \| W\(d\) <= K\(d\)\+d\+1: (\w+) \| K never falls: (\w+)", open(f).read(), re.M)
    if m: boards[(int(m.group(1)), int(m.group(2)))] = dict(K=list(map(int, m.group(3).split())), blind=int(m.group(4)), W=list(map(int, m.group(5).split())), ok=m.group(6) == "True" and m.group(7) == "True")
boards[(4, 6)] = dict(K=K46, blind=6, W=W46, W4=W4, ok=all(W46[d] <= K46[d] + d + 1 for d in range(4)) and all(K46[i] <= K46[i + 1] for i in range(4)))
assert len(boards) == 15, len(boards)
goddard = {2: [2, 2, 3, 4, 4], 3: [2, 3, 4, 4, 5], 4: [3, 3, 4, 5, 6]}                       # as sealed, for 2 to 6 colours
mine = {n: [boards[(n, k)]["blind"] for k in range(2, 7)] for n in (2, 3, 4)}
gap = [b for b, v in sorted(boards.items()) if v["blind"] > v["K"][0]]; first = [b for b in gap if boards[b]["K"][1] > boards[b]["K"][0]]
jump = max(v["K"][i + 1] - v["K"][i] for v in boards.values() for i in range(len(v["K"]) - 1))
lines = [
 ("P1", "guessed", 0.80, K46[1] == 5, f"K(1) = {K46[1]} (sealed: 5)"),
 ("P2", "guessed", 0.50, K46[2] == 5, f"K(2) = {K46[2]} (sealed: 5)"),
 ("P3", "guessed", 0.70, K46[3] == 6, f"K(3) = {K46[3]} (sealed: 6)"),
 ("P4", "guessed", 0.55, W46[1] == 6, f"W(1) = {W46[1]} (sealed: 6)"),
 ("P5", "guessed", 0.60, W46[2] == 8, f"W(2) = {W46[2]} (sealed: 8)"),
 ("P6", "remembered", 0.90, W46[0] == 5 and K46[0] == 4, f"W(0) = {W46[0]}, K(0) = {K46[0]} (sealed: 5 and 4)"),
 ("P7", "remembered", 0.90, mine == goddard, "blind play: two pegs " + ", ".join(map(str, mine[2])) + "; three " + ", ".join(map(str, mine[3])) + "; four " + ", ".join(map(str, mine[4])) + " (sealed: 2, 2, 3, 4, 4; 2, 3, 4, 4, 5; 3, 3, 4, 5, 6)"),
 ("P8", "guessed", 0.55, len(first) == len(gap), f"of the {len(gap)} boards where blind play costs more than ordinary play, K(1) > K(0) on {len(first)}: " + ", ".join(f"{n} pegs {k} colours" for n, k in first) + " (sealed: on every one)"),
 ("P9", "guessed", 0.60, jump <= 1, f"the largest rise of K from one lag to the next, over the fifteen boards: {jump} (sealed: never more than one)"),
 ("P10", "worked", 0.97, all(v["ok"] for v in boards.values()), "K never falls with the lag and W(d) <= K(d) + d + 1 on " + str(sum(v["ok"] for v in boards.values())) + " of 15 boards (sealed: on every board and lag computed)")]
held = failed = 0; brier = 0; by = {}
for name, mark, odds, ok, what in lines:
    print(f"{name:4s} {mark:10s} odds {odds:.2f}  {'held  ' if ok else 'FAILED'}  {what}"); held += ok; failed += not ok; brier += (odds - ok) ** 2; by.setdefault(mark, [0, 0])[0 if ok else 1] += 1
print(f"\nheld {held}, failed {failed}, of {len(lines)}; my mean odds {sum(l[2] for l in lines) / len(lines):.3f}; Brier {brier / len(lines):.4f}; had I said 0.5 on every line, 0.2500")
print("by the sheet's own marks: " + "; ".join(f"marked {m}: {a + b} lines, {a} held, {b} failed" for m, (a, b) in by.items()))
json.dump({f"{n} {k}": v for (n, k), v in sorted(boards.items())}, open("boards.json", "w"), indent=1)
