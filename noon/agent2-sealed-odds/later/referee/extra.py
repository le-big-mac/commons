"""Referee: drum studies as one unit; the gap leaving a study out; studies with both kinds."""
import random, sys
sys.path.insert(0, "/home/agent2/later/referee")
from blind import load, fit2 as A, shift as B, first
STUDY = {"peas": "peas", "peas2": "peas", "calve": "calve", "hawk": "hawk", "cutoff": "cutoff", "drum": "drum", "drum2": "drum", "drum3": "drum", "outsell": "outsell",
         "drum12": "drum12", "drumfree": "drumfree", "drumair": "drumair", "prior": "prior", "post": "post", "post2": "post"}
S = [r for r in load() if r["y"] is not None]
for r in S: r["study"] = STUDY[r["sheet"]]; r["m"] = first(r["mark"]); r["unit"] = "DRUM" if r["study"].startswith("drum") else r["study"]
br = lambda rows, f=lambda p: p: sum((f(r["p"]) - r["y"]) ** 2 for r in rows) / len(rows); sh = lambda rows: sum(r["y"] for r in rows) / len(rows)
def boot(stat, key, seed=5, n=10000):
    rnd = random.Random(seed); units = sorted({r[key] for r in S}); by = {u: [r for r in S if r[key] == u] for u in units}; out = []
    for _ in range(n):
        out.append(stat([r for u in rnd.choices(units, k=len(units)) for r in by[u]]))
    out.sort(); return out[250], out[9749], len(units)
for nm, f in (("A", A), ("B", B)):
    for key in ("study", "unit", "sheet"):
        lo, hi, k = boot(lambda x: br(x, f) - br(x), key); print(f"{nm} minus sealed, resampling by {key} ({k} units): {lo:+.4f} to {hi:+.4f}")
print("lines about the one drum:", sum(r["unit"] == "DRUM" for r in S), "of", len(S), "; guessed among them", sum(r["unit"] == "DRUM" and r["m"] == "guessed" for r in S), "of", sum(r["m"] == "guessed" for r in S))
gaps = []
for s in sorted({r["study"] for r in S}):
    w = [r for r in S if r["m"] == "worked" and r["study"] != s]; g = [r for r in S if r["m"] == "guessed" and r["study"] != s]; gaps.append((sh(w) - sh(g), s))
print("worked minus guessed leaving a study out:", f"{min(gaps)[0]:.3f} ({min(gaps)[1]}) to {max(gaps)[0]:.3f} ({max(gaps)[1]})")
n = k = 0
for s in sorted({r["study"] for r in S}):
    a = [r for r in S if r["study"] == s and r["m"] in ("worked", "remembered")]; b = [r for r in S if r["study"] == s and r["m"] == "guessed"]
    if a and b: n += 1; k += sh(a) > sh(b)
print(f"studies with both kinds: {n}; worked or remembered higher in {k}")
D = [r for r in S if r["unit"] == "DRUM"]; O = [r for r in S if r["unit"] != "DRUM"]
for nm, rows in (("the four drum studies", D), ("the other seven", O)):
    g = [r for r in rows if r["m"] == "guessed"]
    print(f"{nm}: {len(rows)} lines, share {sh(rows):.3f}, odds {sum(r['p'] for r in rows)/len(rows):.3f}, Brier {br(rows):.4f}, A {br(rows, A) - br(rows):+.4f}; guessed {len(g)}: share {sh(g):.3f}, odds {sum(r['p'] for r in g)/len(g):.3f}")
