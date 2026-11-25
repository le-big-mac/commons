"""Referee's sweeps over lawful choices, from my own parse of the scorecards (blind.py). Writes sweep.out via stdout."""
import csv, math, random, re, sys
sys.path.insert(0, "/home/agent2/later/referee")
from blind import load, fit2 as A, shift as B, first, FILES

STUDY = {"peas": "peas", "peas2": "peas", "calve": "calve", "hawk": "hawk", "cutoff": "cutoff", "drum": "drum", "drum2": "drum",
         "drum3": "drum", "outsell": "outsell", "drum12": "drum12", "drumfree": "drumfree", "drumair": "drumair", "prior": "prior",
         "post": "post", "post2": "post"}
ALL = load()
for r in ALL:
    r["study"] = STUDY[r["sheet"]]; r["m"] = first(r["mark"])
S = [r for r in ALL if r["y"] is not None]
br = lambda rows, f=lambda p: p: sum((f(r["p"]) - r["y"]) ** 2 for r in rows) / len(rows)
sh = lambda rows: sum(r["y"] for r in rows) / len(rows)
mo = lambda rows: sum(r["p"] for r in rows) / len(rows)
studies = sorted({r["study"] for r in S})

print("0. My parse against the author's lines.csv")
auth = list(csv.DictReader(open("/home/agent2/later/lines.csv")))
mine = [(r["label"], r["m"], r["p"], r["y"]) for r in S]
theirs = [(a["label"], a["mark"], float(a["odds"]), float(a["outcome"])) for a in auth]
print(f"   author {len(theirs)} lines, mine {len(mine)}; identical in order, label, mark, odds, outcome: {mine == theirs}")

def variant(name, rows):
    d = br(rows, A) - br(rows); e = br(rows, B) - br(rows)
    W = [r for r in rows if r["m"] == "worked"]; G = [r for r in rows if r["m"] == "guessed"]
    z = [d < 0, e < 0, br(rows) > 0.134, sh(rows) < mo(rows), sh(W) - sh(G) >= 0.20, sh(W) >= 0.85, 0.50 <= sh(G) <= 0.65, br(G) >= 0.24]
    print(f"   {name:46s} n {len(rows):3d} share {sh(rows):.3f} odds {mo(rows):.3f} Brier {br(rows):.4f} A {d:+.4f} B {e:+.4f} | guessed share {sh(G):.3f} Brier {br(G):.4f} | Z1-8 "
          + "".join("h" if x else "F" for x in z))

def withy(rows, v):
    return [dict(r, y=(v if r["y"] == 0.5 else r["y"])) for r in rows]

print("\n1. Lawful choices: A and B minus sealed, and the eight verdicts (h held, F failed)")
variant("as published (half 0.5, drum3 in)", S)
variant("half counted 0", withy(S, 0.0))
variant("half counted 1", withy(S, 1.0))
variant("halves left out", [r for r in S if r["y"] != 0.5])
variant("drum3 out (sheet's parenthesis: two sheets)", [r for r in S if r["sheet"] != "drum3"])
variant("X1 void (not 'scored FAILED')", [r for r in S if not (r["sheet"] == "drum3" and r["label"] == "X1")])
variant("marked lines only (peas out)", [r for r in S if r["m"] != "none"])
variant("post2 out (the unrefereed sheet)", [r for r in S if r["sheet"] != "post2"])
variant("prior out (the only sheet with halves)", [r for r in S if r["sheet"] != "prior"])
for s in studies:
    variant(f"without study {s}", [r for r in S if r["study"] != s])

print("\n2. Single lines whose removal changes the sign of A minus sealed (published +0.0009)")
tot = sum((A(r["p"]) - r["y"]) ** 2 - (r["p"] - r["y"]) ** 2 for r in S)
fl = [(r["sheet"], r["label"], r["p"], r["y"], (A(r["p"]) - r["y"]) ** 2 - (r["p"] - r["y"]) ** 2) for r in S]
flips = [x for x in fl if (tot - x[4]) < 0]
print(f"   sum over 135 lines of (A - sealed) squared errors: {tot:+.4f}; lines whose removal makes it negative: {len(flips)}")
for x in sorted(flips, key=lambda x: -x[4])[:40]:
    print(f"      {x[0]:9s} {x[1]:4s} odds {x[2]:.2f} outcome {x[3]} contributes {x[4]:+.4f}")
print("   by study, A minus sealed and B minus sealed (per-line means), and sums")
for s in studies:
    rr = [r for r in S if r["study"] == s]
    print(f"      {s:9s} n {len(rr):3d} A {br(rr, A) - br(rr):+.4f} B {br(rr, B) - br(rr):+.4f}")
print("   by sheet")
nb = [0, 0]
for sname, _ in FILES:
    rr = [r for r in S if r["sheet"] == sname]
    a, b = br(rr, A) - br(rr), br(rr, B) - br(rr); nb[0] += a < 0; nb[1] += b < 0
    print(f"      {sname:9s} n {len(rr):3d} A {a:+.4f} B {b:+.4f}")
print(f"   sheets better corrected: A {nb[0]} of 15, B {nb[1]} of 15")

def boot(stat, rows, seed, n=10000, units=None):
    rnd = random.Random(seed); units = units or sorted({r["study"] for r in rows}); by = {u: [r for r in rows if r["study"] == u] for u in units}
    out = []
    for _ in range(n):
        samp = [r for u in rnd.choices(units, k=len(units)) for r in by[u]]
        try:
            out.append(stat(samp))
        except ZeroDivisionError:
            pass
    out.sort(); m = len(out)
    return out[int(0.025 * m)], out[int(0.975 * m) - 1], m

print("\n3. Resampling whole studies (middle 95% of 10,000), three seeds each")
W = [r for r in S if r["m"] == "worked"]; G = [r for r in S if r["m"] == "guessed"]; Rm = [r for r in S if r["m"] == "remembered"]
def gapstat(rows):
    w = [r for r in rows if r["m"] == "worked"]; g = [r for r in rows if r["m"] == "guessed"]
    return sh(w) - sh(g)
stats = [("A minus sealed (all 135)", lambda x: br(x, A) - br(x), S),
         ("B minus sealed (all 135)", lambda x: br(x, B) - br(x), S),
         ("share held minus mean odds (all 135)", lambda x: sh(x) - mo(x), S),
         ("share held (all 135)", sh, S),
         ("Brier (all 135)", br, S),
         ("worked: share minus mean odds", lambda x: sh(x) - mo(x), W),
         ("remembered: share minus mean odds", lambda x: sh(x) - mo(x), Rm),
         ("guessed: share minus mean odds", lambda x: sh(x) - mo(x), G),
         ("guessed: Brier minus Brier at one half", lambda x: br(x) - br(x, lambda p: 0.5), G),
         ("worked share minus guessed share", gapstat, [r for r in S if r["m"] in ("worked", "guessed")])]
for nm, st, rows in stats:
    rs = [boot(st, rows, sd) for sd in (1, 2, 3)]
    print(f"   {nm:42s} value {st(rows):+.4f}; " + "; ".join(f"{lo:+.4f} to {hi:+.4f}" for lo, hi, _ in rs) + f"  ({len({r['study'] for r in rows})} studies)")

print("\n4. Does the mark add to the odds, or the odds to the mark? Share held by odds band and mark")
for lo, hi in ((0, 0.55), (0.55, 0.65), (0.65, 0.75), (0.75, 0.85), (0.85, 1.01)):
    parts = []
    for mk in ("worked", "remembered", "guessed", "none"):
        rr = [r for r in S if r["m"] == mk and lo <= r["p"] < hi]
        parts.append(f"{mk} {sum(r['y'] for r in rr):g}/{len(rr)}")
    print(f"   odds {lo:.2f} to under {min(hi, 1):.2f}: " + "; ".join(parts))
print("   guessed lines split at other cuts (share held at or above the cut, below it)")
for c in (0.50, 0.55, 0.60, 0.65, 0.70):
    hi_ = [r for r in G if r["p"] >= c - 1e-9]; lo_ = [r for r in G if r["p"] < c - 1e-9]
    print(f"      cut {c:.2f}: at or above {len(hi_):2d} lines {sh(hi_) if hi_ else float('nan'):.3f}; below {len(lo_):2d} lines {sh(lo_) if lo_ else float('nan'):.3f}")
print("   guessed lines without 'who already knew' (whose guessed odds run 0.15 to 0.65): split at 0.60")
G2 = [r for r in G if r["study"] != "prior"]; hi_ = [r for r in G2 if r["p"] >= 0.6 - 1e-9]; lo_ = [r for r in G2 if r["p"] < 0.6 - 1e-9]
print(f"      at or above {len(hi_)} lines {sh(hi_):.3f}; below {len(lo_)} lines {sh(lo_):.3f}; Brier my odds {br(G2):.4f}, one half {br(G2, lambda p: 0.5):.4f}, own share {br(G2, lambda p: sh(G2)):.4f}")

print("\n5. The mark-alone price against my odds on the 115 marked lines")
M = [r for r in S if r["m"] != "none"]
def loo(r):
    return sh([q for q in M if q["m"] == r["m"] and q["study"] != r["study"]])
bm = sum((loo(r) - r["y"]) ** 2 for r in M) / len(M)
print(f"   my odds {br(M):.4f}; mark share from other studies {bm:.4f}; difference {bm - br(M):+.4f}")
def dstat(rows):
    return sum((loo(r) - r["y"]) ** 2 for r in rows) / len(rows) - br(rows)
for units, lab in ((sorted({r["study"] for r in M}), "the 10 studies that have marked lines"), (studies, "all 11, peas drawn as an empty study (the author's way)")):
    print(f"   resampling {lab}: " + "; ".join("%+.4f to %+.4f (%d usable)" % boot(dstat, M, sd, units=units) for sd in (1, 2)))
print("   'remembered loosely' (3 lines) and 'worked roughly' / 'worked from Yonder's reading' (4 lines) moved to other marks:")
for nm, mp in (("as published (first word)", {}), ("remembered loosely -> guessed", {"remembered loosely": "guessed"}),
               ("worked roughly, worked from ... -> remembered", {"worked roughly": "remembered", "worked from Yonder's reading": "remembered"}),
               ("both", {"remembered loosely": "guessed", "worked roughly": "remembered", "worked from Yonder's reading": "remembered"})):
    rows = [dict(r, m=mp.get(r["mark"], r["m"])) for r in S]
    parts = []
    for mk in ("worked", "remembered", "guessed"):
        rr = [r for r in rows if r["m"] == mk]
        parts.append(f"{mk} {len(rr)}: held {sum(r['y'] == 1 for r in rr)}, failed {sum(r['y'] == 0 for r in rr)}, half {sum(r['y'] == .5 for r in rr)}, share {sh(rr):.3f}, odds {mo(rr):.3f}")
    print(f"      {nm:46s} " + " | ".join(parts))

print("\n6. The rule 'for next time' (worked nearer 0.95; 0.07 off a guess), on the lines it was fitted to")
def rule(r, wp=0.95, off=0.07):
    if r["m"] == "worked": return wp
    if r["m"] == "guessed": return max(0.01, r["p"] - off)
    return r["p"]
b0 = br(M); b1 = sum((rule(r) - r["y"]) ** 2 for r in M) / len(M)
print(f"   115 marked lines: my odds {b0:.4f}; the rule {b1:.4f} ({b1 - b0:+.4f}), in sample")
for mk in ("worked", "guessed"):
    rr = [r for r in M if r["m"] == mk]; print(f"      {mk:8s} {len(rr)} lines: my odds {br(rr):.4f}; the rule {sum((rule(r) - r['y']) ** 2 for r in rr) / len(rr):.4f}")
def rule_loo(r):
    oth = [q for q in M if q["study"] != r["study"] and q["m"] == r["m"]]
    if r["m"] == "worked": return min(0.99, sh(oth))
    if r["m"] == "guessed": return min(0.99, max(0.01, r["p"] + (sh(oth) - mo(oth))))
    return r["p"]
b2 = sum((rule_loo(r) - r["y"]) ** 2 for r in M) / len(M)
print(f"   the same rule with its two numbers taken from the other studies only: {b2:.4f} ({b2 - b0:+.4f})")
def rstat(rows):
    return sum((rule_loo(r) - r["y"]) ** 2 for r in rows) / len(rows) - br(rows)
print("   resampling the 10 marked studies: " + "; ".join("%+.4f to %+.4f" % boot(rstat, M, sd)[:2] for sd in (1, 2)))
for mk in ("worked", "guessed"):
    rr = [r for r in M if r["m"] == mk]; print(f"      {mk:8s}: my odds {br(rr):.4f}; rule from other studies {sum((rule_loo(r) - r['y']) ** 2 for r in rr) / len(rr):.4f}")
print("   guessed: gap (share minus mean odds) leaving each study out: " + ", ".join(f"{s} {sh([r for r in G if r['study'] != s]) - mo([r for r in G if r['study'] != s]):+.3f}" for s in sorted({r['study'] for r in G})))
print("   guessed: gap inside each study: " + ", ".join(f"{s} {sh([r for r in G if r['study'] == s]) - mo([r for r in G if r['study'] == s]):+.3f} (n {len([r for r in G if r['study'] == s])})" for s in sorted({r['study'] for r in G})))
print("   worked lines by study: " + ", ".join(f"{s} {sum(r['y'] for r in W if r['study'] == s):g}/{len([r for r in W if r['study'] == s])}" for s in sorted({r['study'] for r in W})))

print("\n7. What the sheets' own printed summary lines already gave (count, held, mean odds, Brier per sheet), before any tally")
tot_n = tot_y = tot_p = tot_b = 0
for sname, path in FILES:
    rr = [r for r in S if r["sheet"] == sname]
    tot_n += len(rr); tot_y += sum(r["y"] for r in rr); tot_p += mo(rr) * len(rr); tot_b += br(rr) * len(rr)
print(f"   weighted over 15 sheets: share {tot_y / tot_n:.4f}, mean odds {tot_p / tot_n:.4f}, Brier {tot_b / tot_n:.4f} (these three are Z3 and Z4)")
allg = [(s, len([r for r in S if r['sheet'] == s]), sum(r['y'] for r in S if r['sheet'] == s)) for s, _ in FILES if {r['m'] for r in S if r['sheet'] == s} == {'guessed'}]
allw = [(s, len([r for r in S if r['sheet'] == s]), sum(r['y'] for r in S if r['sheet'] == s)) for s, _ in FILES if {r['m'] for r in S if r['sheet'] == s} == {'worked'}]
print(f"   sheets wholly guessed (their count held IS a tally by mark): {allg}")
print(f"   sheets wholly worked: {allw}")
seen = [r for r in S if r["sheet"] in ("prior", "post", "post2") or {q['m'] for q in S if q['sheet'] == r['sheet']} in ({'guessed'}, {'worked'})]
for mk in ("worked", "guessed"):
    rr = [r for r in seen if r["m"] == mk]; al = [r for r in S if r["m"] == mk]
    print(f"   {mk}: lines whose outcome by mark follows from what the sheet says was seen: {len(rr)} of {len(al)}; share held among them {sh(rr):.3f}")
