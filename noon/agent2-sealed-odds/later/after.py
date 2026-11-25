"""Second looks at the later lines: would the mark alone have priced them better than my odds; is the gap between marks there inside
each study; does one study carry it; what the halves and the unmarked sheets change.   usage: python -I after.py > after.out"""
import csv, random
R = [dict(r, odds=float(r["odds"]), outcome=float(r["outcome"])) for r in csv.DictReader(open("lines.csv"))]
share = lambda rows: sum(r["outcome"] for r in rows) / len(rows) if rows else float("nan"); brier = lambda rows, f: sum((f(r) - r["outcome"]) ** 2 for r in rows) / len(rows)
studies = list(dict.fromkeys(r["study"] for r in R)); M = [r for r in R if r["mark"] != "none"]
print(f"A. Pricing by the mark alone ({len(M)} marked lines; the peas' 20 carry no mark)")
print(f"   my sealed odds on the marked lines: {brier(M, lambda r: r['odds']):.4f}")
flat = {mk: share([r for r in M if r["mark"] == mk]) for mk in ("worked", "remembered", "guessed")}
print("   each line priced at the share of its mark that held, over all marked lines (in sample): " + ", ".join(f"{k} {v:.3f}" for k, v in flat.items()) + f": {brier(M, lambda r: flat[r['mark']]):.4f}")
def loo(r):                                             # the share of the line's mark that held in the other studies
    rows = [q for q in M if q["mark"] == r["mark"] and q["study"] != r["study"]]; return share(rows)
print(f"   each line priced at the share of its mark that held in the OTHER studies (so nothing of its own study is used): {brier(M, loo):.4f}")
fixed = {"worked": 0.9, "remembered": 0.8, "guessed": 0.5}
print(f"   three round prices fixed beforehand in no way (worked 0.9, remembered 0.8, guessed 0.5; I chose them after seeing the table): {brier(M, lambda r: fixed[r['mark']]):.4f}")
random.seed(7); d = []
for _ in range(10000):
    samp = [r for s in random.choices(studies, k=len(studies)) for r in M if r["study"] == s]
    if samp: d.append(brier(samp, loo) - brier(samp, lambda r: r["odds"]))
d.sort(); print(f"   mark-in-other-studies minus my odds: {brier(M, loo) - brier(M, lambda r: r['odds']):+.4f}; resampling whole studies {d[250]:+.4f} to {d[9749]:+.4f}")
print("\nB. Do my odds add anything inside a mark? (my odds, against one price for the whole mark at its own share, in sample)")
for mk in ("worked", "remembered", "guessed"):
    rows = [r for r in M if r["mark"] == mk]; print(f"   {mk:10s} {len(rows):3d} lines: my odds {brier(rows, lambda r: r['odds']):.4f}; one price at {flat[mk]:.3f}: {brier(rows, lambda r: flat[mk]):.4f}")
G = [r for r in M if r["mark"] == "guessed"]; hi = [r for r in G if r["odds"] >= 0.6]; lo = [r for r in G if r["odds"] < 0.6]
print(f"   guessed lines at odds of 0.60 or more: {len(hi)}, held {share(hi):.3f}; below 0.60: {len(lo)}, held {share(lo):.3f}")
print("\nC. Inside each study that has both kinds: share held, worked or remembered against guessed")
both = 0; same = 0
for s in studies:
    a = [r for r in M if r["study"] == s and r["mark"] in ("worked", "remembered")]; b = [r for r in M if r["study"] == s and r["mark"] == "guessed"]
    if a and b: both += 1; same += share(a) > share(b); print(f"   {s:24s} worked or remembered {len(a):2d} lines, {share(a):.2f}; guessed {len(b):2d} lines, {share(b):.2f}")
print(f"   higher for worked or remembered in {same} of {both} such studies")
print("\nD. Leaving one study out at a time: the gap between worked and guessed (share held), and the two shares")
gaps = []
for s in studies:
    w = [r for r in M if r["mark"] == "worked" and r["study"] != s]; g = [r for r in M if r["mark"] == "guessed" and r["study"] != s]; gaps.append((share(w) - share(g), s, share(w), share(g)))
print(f"   the gap runs from {min(gaps)[0]:.3f} (without {min(gaps)[1]}) to {max(gaps)[0]:.3f} (without {max(gaps)[1]}); guessed alone from {min(x[3] for x in gaps):.3f} to {max(x[3] for x in gaps):.3f}")
print("\nE. The halves and the unmarked")
nh = [r for r in R if r["outcome"] != 0.5]; print(f"   without the 6 halves: {len(nh)} lines, held {share(nh):.3f}, my odds {sum(r['odds'] for r in nh) / len(nh):.3f}, Brier {brier(nh, lambda r: r['odds']):.4f}")
gh = [r for r in G if r["outcome"] != 0.5]; print(f"   guessed without its 4 halves: {len(gh)} lines, held {share(gh):.3f}")
print(f"   the marked lines only: held {share(M):.3f}, my odds {sum(r['odds'] for r in M) / len(M):.3f}, Brier {brier(M, lambda r: r['odds']):.4f}")
print("\nF. Did I guess more as the days went on? It depends on where one study is put: its sheet was sealed two minutes before midnight")
base = {"Mendel's peas": 22, "calved ice": 22, "hawks and doves": 22, "the arXiv's boundary": 22, "a drumskin": 22, "outselling": 22, "beyond the ninth mode": 22, "air in the drum": 23, "who already knew": 23, "Mastermind by post": 23}
for put in (22, 23):
    day = dict(base, **{"the note not sounded": put}); parts = []
    for dd in (22, 23):
        rows = [r for r in M if day[r["study"]] == dd]; g = [r for r in rows if r["mark"] == "guessed"]; parts.append(f"{dd} November: {len(rows)} marked lines, {len(g)} guessed ({100 * len(g) / len(rows):.0f}%)")
    print(f"   with that study on the {put}: " + "; ".join(parts))
print("\nG. Are the worked lines just the near-certain ones? Worked lines by the odds I gave")
W = [r for r in M if r["mark"] == "worked"]
for lo, hi in ((0, 0.75), (0.75, 0.85), (0.85, 0.95), (0.95, 1.01)):
    rows = [r for r in W if lo <= r["odds"] < hi]
    if rows: print(f"   odds {lo:.2f} to under {min(hi, 1):.2f}: {len(rows):2d} lines, held {sum(1 for r in rows if r['outcome'] == 1)}, mean odds {sum(r['odds'] for r in rows) / len(rows):.3f}")
print("   the one worked line that failed: " + "; ".join(f"{r['sheet']} {r['label']} at odds {r['odds']:.2f}" for r in W if r["outcome"] == 0))
print("   remembered lines that did not hold: " + "; ".join(f"{r['sheet']} {r['label']} at odds {r['odds']:.2f} ({'half' if r['outcome'] == 0.5 else 'failed'})" for r in M if r["mark"] == "remembered" and r["outcome"] != 1))
print("\nH. What correction A does to each kind of line (Brier: my odds, then corrected)")
import math
logit = lambda p: math.log(p / (1 - p)); expit = lambda x: 1 / (1 + math.exp(-x)); A = lambda r: min(0.99, max(0.01, expit(0.277 + 1.413 * logit(r["odds"]))))
for mk in ("worked", "remembered", "guessed", "none"):
    rows = [r for r in R if r["mark"] == mk]; print(f"   {mk:10s} {len(rows):3d} lines: {brier(rows, lambda r: r['odds']):.4f} -> {brier(rows, A):.4f} ({brier(rows, A) - brier(rows, lambda r: r['odds']):+.4f})")
