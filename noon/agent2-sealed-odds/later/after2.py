"""The referee's controls, redone in my own script.   usage: python -I after2.py > after2.out"""
import csv, math, random
R = [dict(r, odds=float(r["odds"]), outcome=float(r["outcome"])) for r in csv.DictReader(open("lines.csv"))]
logit = lambda p: math.log(p / (1 - p)); expit = lambda x: 1 / (1 + math.exp(-x)); clip = lambda p: min(0.99, max(0.01, p))
A = lambda r: clip(expit(0.277 + 1.413 * logit(r["odds"]))); B = lambda r: clip(expit(logit(r["odds"]) + 0.581)); own = lambda r: r["odds"]
brier = lambda rows, f=own: sum((f(r) - r["outcome"]) ** 2 for r in rows) / len(rows); share = lambda rows: sum(r["outcome"] for r in rows) / len(rows); mo = lambda rows: sum(r["odds"] for r in rows) / len(rows)
studies = list(dict.fromkeys(r["study"] for r in R)); M = [r for r in R if r["mark"] != "none"]; W = [r for r in M if r["mark"] == "worked"]; G = [r for r in M if r["mark"] == "guessed"]
def rng(stat, rows, seed=11, n=10000):
    """the middle 95% of n resamplings of whole studies"""
    random.seed(seed); st = list(dict.fromkeys(r["study"] for r in rows)); out = []
    for _ in range(n):
        samp = [r for s in random.choices(st, k=len(st)) for r in rows if r["study"] == s]; out.append(stat(samp))
    out.sort(); return out[int(0.025 * n)], out[int(0.975 * n) - 1]
def halves(rows, v): return [dict(r, outcome=v) if r["outcome"] == 0.5 else r for r in rows]
print("1. Correction A and B minus my odds, under other lawful ways of counting")
X1 = [r for r in R if not (r["sheet"] == "drum/verdicts3.out" and r["label"] == "X1")]
var = [("as published", R), ("X1 left out as void (its scorecard calls the verdict my scoring, not the letter's)", X1), ("halves left out", [r for r in R if r["outcome"] != 0.5]), ("a half counted 1", halves(R, 1.0)), ("a half counted 0", halves(R, 0.0)),
       ("without Mastermind's second sheet, which no referee saw", [r for r in R if r["sheet"] != "post/verdicts2.out"]), ("without the drumskin's third file", [r for r in R if r["sheet"] != "drum/verdicts3.out"]), ("without the unmarked sheets", M)]
var += [(f"without {s}", [r for r in R if r["study"] != s]) for s in studies]
dA = []; dB = []
for name, rows in var: a = brier(rows, A) - brier(rows); b = brier(rows, B) - brier(rows); dA.append(a); dB.append(b); print(f"   {name:86s} A {a:+.4f}   B {b:+.4f}")
print(f"   A is below my odds in {sum(1 for x in dA if x < 0)} of these {len(dA)} and above in {sum(1 for x in dA if x > 0)}; B is above in {sum(1 for x in dB if x > 0)}, from {min(dB):+.4f} to {max(dB):+.4f}")
flips = sum(1 for i in range(len(R)) if brier(R[:i] + R[i + 1:], A) < brier(R[:i] + R[i + 1:])); print(f"   lines whose removal alone puts A below my odds: {flips} of {len(R)}")
sa = sorted(s for s in studies if brier([r for r in R if r["study"] == s], A) < brier([r for r in R if r["study"] == s])); sb = sorted(s for s in studies if brier([r for r in R if r["study"] == s], B) < brier([r for r in R if r["study"] == s]))
sheets = list(dict.fromkeys(r["sheet"] for r in R)); print(f"   the studies that score better under A: {', '.join(sa)}; under B: {'the same' if sa == sb else ', '.join(sb)}; by sheet, A is better in {sum(1 for s in sheets if brier([r for r in R if r['sheet'] == s], A) < brier([r for r in R if r['sheet'] == s]))} of {len(sheets)}")
print("\n2. Share that held minus my mean odds, with the middle 95% of 10,000 resamplings of whole studies")
gap = lambda rows: share(rows) - mo(rows)
for name, rows in (("all 135 later lines", R), ("worked", W), ("guessed", G)): lo, hi = rng(gap, rows); print(f"   {name:22s} {gap(rows):+.3f} ({lo:+.3f} to {hi:+.3f}), over {len({r['study'] for r in rows})} studies")
lo, hi = rng(share, R); lo2, hi2 = rng(brier, R); print(f"   share that held, all later lines: {share(R):.3f} ({lo:.3f} to {hi:.3f}); the first 142 had 0.82.   Brier of my odds: {brier(R):.4f} ({lo2:.4f} to {hi2:.4f}); the first 142 scored 0.134")
drum = ("a drumskin", "beyond the ninth mode", "the note not sounded", "air in the drum"); gd = [r for r in G if r["study"] in drum]; go = [r for r in G if r["study"] not in drum]
print(f"   guessed lines of the four drum studies: {len(gd)}, held {share(gd):.3f}, I said {mo(gd):.3f}; the other guessed lines: {len(go)}, held {share(go):.3f}, I said {mo(go):.3f}")
print(f"   lines about the drum: {sum(1 for r in R if r['study'] in drum)} of {len(R)}")
print("\n3. The rule for next time, tried the way yesterday's corrections were: each study priced from the other studies only")
shiftG = lambda r: clip(r["odds"] + gap([q for q in G if q["study"] != r["study"]])); priceW = lambda r: share([q for q in W if q["study"] != r["study"]])
print(f"   guessed lines, my odds moved by the other studies' gap: {brier(G, shiftG):.4f} against {brier(G):.4f} as sealed; in sample (moved by {gap(G):+.3f}): {brier(G, lambda r: clip(r['odds'] + gap(G))):.4f}")
print(f"   worked lines, priced at the other studies' share: {brier(W, priceW):.4f} against {brier(W):.4f} as sealed")
rule = lambda r: priceW(r) if r["mark"] == "worked" else shiftG(r) if r["mark"] == "guessed" else r["odds"]; lo, hi = rng(lambda rows: brier(rows, rule) - brier(rows), M)
print(f"   the whole rule on the 115 marked lines (remembered left alone): {brier(M, rule):.4f} against {brier(M):.4f}; difference {brier(M, rule) - brier(M):+.4f} ({lo:+.4f} to {hi:+.4f})")
onlyW = lambda r: priceW(r) if r["mark"] == "worked" else r["odds"]; print(f"   the worked half alone: {brier(M, onlyW):.4f}")
print("\n4. Do my odds carry anything inside the guessed lines?")
half5 = lambda rows: sum((0.5 - r["outcome"]) ** 2 for r in rows) / len(rows); gp = [r for r in G if r["study"] != "who already knew"]
lo, hi = rng(lambda rows: brier(rows) - half5(rows), G); print(f"   all 67: my odds {brier(G):.4f}, one half {half5(G):.4f}, difference {brier(G) - half5(G):+.4f} ({lo:+.4f} to {hi:+.4f})")
print(f"   without who already knew (8 guessed lines, 4 of them halves): my odds {brier(gp):.4f}, one half {half5(gp):.4f}")
for cut in (0.60, 0.65):
    for name, rows in (("all", G), ("without who already knew", gp)):
        hi_ = [r for r in rows if r["odds"] >= cut]; lo_ = [r for r in rows if r["odds"] < cut]; print(f"   cut at {cut:.2f}, {name}: at or above {len(hi_)} lines, held {share(hi_):.3f}; below {len(lo_)} lines, held {share(lo_):.3f}")
print("\n5. At equal odds: lines I priced from 0.55 to under 0.75")
band = [r for r in M if 0.55 <= r["odds"] < 0.75]; wr = [r for r in band if r["mark"] != "guessed"]; gg = [r for r in band if r["mark"] == "guessed"]
print(f"   worked or remembered: {len(wr)} lines, held {sum(1 for r in wr if r['outcome'] == 1)}, half {sum(1 for r in wr if r['outcome'] == 0.5)}; guessed: {len(gg)} lines, held {sum(1 for r in gg if r['outcome'] == 1)}, half {sum(1 for r in gg if r['outcome'] == 0.5)}")
lo, hi = rng(lambda rows: share([r for r in rows if r["mark"] == "worked"]) - share([r for r in rows if r["mark"] == "guessed"]) if any(r["mark"] == "worked" for r in rows) and any(r["mark"] == "guessed" for r in rows) else 0.46, M)
print(f"   worked minus guessed, share held: {share(W) - share(G):.3f} ({lo:.3f} to {hi:.3f}); twelve of the 30 worked lines are one sheet (outselling)")
print("\n6. The sealed verdicts that turn on a choice")
for name, rows in var[:8] + [(f"without {s}", [r for r in R if r["study"] != s]) for s in ("a drumskin", "the note not sounded", "who already knew")]:
    g = [r for r in rows if r["mark"] == "guessed"]; print(f"   {name:86s} Z7: guessed held {share(g):.3f} ({'held' if 0.5 <= share(g) <= 0.65 else 'FAILED'});  Z8: guessed score {brier(g):.4f} ({'held' if brier(g) >= 0.24 else 'FAILED'})")
