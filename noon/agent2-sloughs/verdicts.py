"""verdicts.py -- the sealed lines of expectations.md against the runs, by the letter.
Reads out/grid/settings.json and out/extra/settings.json (written by analyse.py)."""
import json, math, re
import os
G = json.load(open("out/grid/settings.json")); E = json.load(open("out/extra/settings.json"))
E = [r for r in E if r["DS"] == 0.1] + (json.load(open("out/fine/settings.json")) if os.path.exists("out/fine/settings.json") else [])   # the runs at spacing 0.05 are in out/fine (made in legs)
def g(P, dc): return [r for r in G if r["P"] == P and r["DC"] == dc and r["LX"] == 200 and r["DS"] == 0.1 and not r["FEED"]][0]
def e(**kw): return [r for r in E if all(r[k] == v for k, v in kw.items())][0]
sheet = open("expectations.md").read()
odds = {m.group(1): float(m.group(2)) for m in re.finditer(r"\*\*(M\d+)\*\* \(guessed, (?:odds )?([\d.]+)\)", sheet)}
cod = [float(x) for x in re.findall(r"agree within 5% \(([\d.]+)\)", sheet)]
base = g(3, 0.4); S = base["Sbar"]; se = base["se"]
lines = []
def line(name, o, held, text, close=False): lines.append((name, o, held if held == "part" else bool(held), text, close))
line("M1", odds["M1"], 2.6 <= S <= 4.2, "base case S-bar = %.3f (se %.3f; seeds %s) (sealed: between 2.6 and 4.2)" % (S, se, ", ".join("%.2f" % v for v in base["each"])))
a, b, c = g(3, 0.2), g(3, 0.4), g(3, 0.8)
line("M2", odds["M2"], a["Sbar"] > b["Sbar"] > c["Sbar"], "at P = 3, S-bar = %.3f, %.3f, %.3f (se %.3f, %.3f, %.3f) at dc = 0.2, 0.4, 0.8 (sealed: falling)" % (a["Sbar"], b["Sbar"], c["Sbar"], a["se"], b["se"], c["se"]),
     close=min(abs(a["Sbar"] - b["Sbar"]) / math.hypot(a["se"], b["se"]), abs(b["Sbar"] - c["Sbar"]) / math.hypot(b["se"], c["se"])) < 2)
fall = (a["Sbar"] - c["Sbar"]) / b["Sbar"]
line("M3", odds["M3"], fall > 0.15, "S-bar(0.2) - S-bar(0.8) is %.1f%% of S-bar(0.4) (sealed: more than 15%%)" % (100 * fall), close=abs(fall - 0.15) * b["Sbar"] < 2 * math.hypot(a["se"], c["se"]))
p2, p6 = g(2, 0.4), g(6, 0.4); diff = abs(p2["Sbar"] - p6["Sbar"]) / max(p2["Sbar"], p6["Sbar"])
line("M4", odds["M4"], diff < 0.15, "at dc = 0.4, S-bar = %.3f at P = 2 and %.3f at P = 6 (se %.3f, %.3f): %.1f%% of the larger apart (sealed: less than 15%%)" % (p2["Sbar"], p6["Sbar"], p2["se"], p6["se"], 100 * diff),
     close=abs(diff - 0.15) * max(p2["Sbar"], p6["Sbar"]) < 2 * math.hypot(p2["se"], p6["se"]))
line("M5", odds["M5"], p6["Sbar"] < p2["Sbar"], "at dc = 0.4, S-bar(P = 6) = %.3f against S-bar(P = 2) = %.3f (sealed: the first below the second)" % (p6["Sbar"], p2["Sbar"]),
     close=abs(p6["Sbar"] - p2["Sbar"]) < 2 * math.hypot(p2["se"], p6["se"]))
line("M6", odds["M6"], abs(S - math.pi) <= 0.15, "base case S-bar = %.3f, %.3f from pi (sealed: within 0.15)" % (S, abs(S - math.pi)), close=abs(abs(S - math.pi) - 0.15) < 2 * se)
grid = [g(P, dc) for P in (2, 3, 4.5, 6) for dc in (0.2, 0.4, 0.8)]
lo = min(grid, key=lambda r: r["Sbar"]); hi = max(grid, key=lambda r: r["Sbar"])
line("M7", odds["M7"], lo["Sbar"] <= math.pi <= hi["Sbar"], "on the grid S-bar runs from %.3f (P = %g, dc = %g) to %.3f (P = %g, dc = %g) (sealed: pi between them)" % (lo["Sbar"], lo["P"], lo["DC"], hi["Sbar"], hi["P"], hi["DC"]))
line("M8", odds["M8"], base["peak_rel"] >= 1.3, "base case: the first peak is %.2f times S-bar, mean of four seeds (sealed: at least 1.3). The sheet did not say what a first peak is: I took the greatest value before the first fall of 5%%; the greatest value in the first tenth of the run is %.2f times S-bar" % (base["peak_rel"], base["early_rel"]))
line("M9", odds["M9"], 0.03 <= base["sd_rel"] <= 0.10, "base case: the standard deviation of S(t) is %.1f%% of S-bar, mean of four seeds (sealed: 3%% to 10%%)" % (100 * base["sd_rel"]))
fb = e(FEED=1, LX=200.0, DS=0.1); d10 = abs(fb["Sbar"] - S) / S
line("M10", odds["M10"], d10 <= 0.10, "with the feedback on, S-bar = %.3f (se %.3f) against %.3f off: %.1f%% apart (sealed: within 10%%)" % (fb["Sbar"], fb["se"], S, 100 * d10),
     close=abs(d10 - 0.10) * S < 2 * math.hypot(fb["se"], se))
l1, l4 = e(LX=100.0, FEED=0, DS=0.1), e(LX=400.0, FEED=0, DS=0.1); dl = abs(l1["Sbar"] - l4["Sbar"]) / max(l1["Sbar"], l4["Sbar"])
line("check 1", cod[0], dl <= 0.05, "S-bar = %.3f at LX = 100 and %.3f at LX = 400 (se %.3f, %.3f; %.3f at 200): %.1f%% apart (sealed: within 5%%)" % (l1["Sbar"], l4["Sbar"], l1["se"], l4["se"], S, 100 * dl),
     close=abs(dl - 0.05) * max(l1["Sbar"], l4["Sbar"]) < 2 * math.hypot(l1["se"], l4["se"]))
pending = not [r for r in E if r["DS"] == 0.05]
if not pending:
    # the two runs at spacing 0.05 were stopped by the two-hour limit on a background command, at t = 1392 and 1370 of 1492.8, and not taken up again:
    # their mean is from 746.4 to 1370 (out/fine, analyse.py out/fine 1370).  The base case is given over the same stretch as well as over its full half.
    import numpy as np, glob
    f5 = e(DS=0.05, FEED=0, LX=200.0); same = []
    for fn in sorted(glob.glob("out/grid/P3-dc0.4-s*.out")):
        r = np.array([[float(v) for v in l.split()[:3]] for l in open(fn) if l.strip() and not l.startswith("#")]); same.append(float(r[(r[:, 0] >= 1492.8 / 2) & (r[:, 0] <= 1370 + 1e-9), 2].mean()))
    Ss = float(np.mean(same)); ses = float(np.std(same, ddof=1) / 2); d5 = abs(f5["Sbar"] - Ss) / max(f5["Sbar"], Ss); d5full = abs(f5["Sbar"] - S) / max(f5["Sbar"], S)
    line("check 2", cod[1], "part" if (d5 <= 0.05 and d5full <= 0.05) else False, "S-bar = %.3f at spacing 0.05 (two seeds, se %.3f) and %.3f at 0.1 over the same stretch of time (four seeds, se %.3f): %.1f%% apart (sealed: within 5%%). NOT AS SEALED: the two runs at 0.05 were stopped by the machine's two-hour limit at t = 1392 and 1370 of 1493, so their mean is from 746 to 1370 and not over the whole second half; against the base case's full half (%.3f) they are %.1f%% apart" % (
         f5["Sbar"], f5["se"], Ss, ses, 100 * d5, S, 100 * d5full), close=abs(d5 - 0.05) * max(f5["Sbar"], Ss) < 2 * math.hypot(f5["se"], ses))
full = [l for l in lines if l[2] != "part"]; part = [l for l in lines if l[2] == "part"]
held = sum(1 for l in full if l[2]); br = sum((l[1] - (1 if l[2] else 0)) ** 2 for l in full) / len(full)
for name, o, h, text, close in lines:
    print("%-8s guessed  odds %.2f  %-6s  %s%s" % (name, o, "PART" if h == "part" else "held" if h else "FAILED", text, "  [the margin is within two standard errors of the seeds]" if close else ""))
print()
print("held %d, failed %d, of the %d lines run as sealed; my mean odds on those %.3f; Brier %.4f; had I said 0.5 on every line, 0.2500" % (held, len(full) - held, len(full), sum(l[1] for l in full) / len(full), br))
if part: print("PART: %d line was not run as sealed (%s); it holds on the part that was run and is counted as neither held nor failed" % (len(part), ", ".join(l[0] for l in part)))
if pending: print("check 2 (spacing 0.05 against 0.1, odds %.2f) is not in yet: its runs are still going" % cod[1])
ten = lines[:10]; chk = lines[10:]
print("the ten lines alone: held %d, failed %d; the two priced checks: held %d, failed %d, in part %d" % (sum(1 for l in ten if l[2] is True), sum(1 for l in ten if l[2] is False), sum(1 for l in chk if l[2] is True), sum(1 for l in chk if l[2] is False), sum(1 for l in chk if l[2] == "part")))
