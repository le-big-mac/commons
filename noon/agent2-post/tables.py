"""The tables of the README, from results-4-6.json, boards.json and the strategy files.   usage: python -I tables.py > tables.out"""
import json, re, itertools, collections
R = json.load(open("results-4-6.json"))["runs"]; B = json.load(open("boards.json"))
print("TABLE 1. Four pegs, six colours: each run. Where none works, every opening in the file was tried; where one works, the search stopped at it.\n")
print("| question | lag | guesses | openings tried | that work | the first that works |"); print("|---|---|---|---|---|---|")
for r in R: print(f"| {r['question']} | {'5 and more, all blind' if r['file'].endswith('K-static-Q6.out') else r['lag']} | {r['guesses']} | {r['tried']:,} | {r['work'] if r['work'] else 'none'} | {r.get('opening', '')} |")
K = B["4 6"]["K"]; W = B["4 6"]["W"]
print("\nTABLE 2. Four pegs, six colours: the least number of guesses.\n")
W4 = B["4 6"]["W4"]; S2 = json.load(open("second.json")); m4 = S2["m"]["4"]
print(f"| lag, in guesses | 0 | 1 | 2 | 3 | 4 | 5 to {m4 + 2} | {m4 + 3} and more |"); print("|---|---|---|---|---|---|---|---|")
print("| K: guesses that always determine the code | " + " | ".join(map(str, K)) + " | 6 | 6 |")
print("| W: guesses by which the code has always been sent | " + " | ".join(map(str, W)) + f" | {W4} | lag + 6 | fewer: see the second sheet |")
print("| K + lag + 1 | " + " | ".join(str(K[d] + d + 1) for d in range(5)) + " | lag + 7 | lag + 7 |")
print("\nTABLE 3. Fifteen boards. K at lags 0 to 3 and with every guess blind; W at lags 0 to 3.\n")
print("| pegs | colours | codes | K(0) | K(1) | K(2) | K(3) | K blind | W(0) | W(1) | W(2) | W(3) |"); print("|---|---|---|---|---|---|---|---|---|---|---|---|")
for key in sorted(B, key=lambda s: tuple(map(int, s.split()))):
    n, k = map(int, key.split()); v = B[key]; Kd = lambda d: v["K"][d] if d < len(v["K"]) else v["blind"]
    print(f"| {n} | {k} | {k ** n} | " + " | ".join(str(Kd(d)) for d in range(4)) + f" | {v['blind']} | " + " | ".join(map(str, v["W"])) + " |")
def answer(g, s):
    b = sum(x == y for x, y in zip(g, s)); return f"{b}{sum(min(g.count(c), s.count(c)) for c in set(g)) - b}"
codes = ["".join(p) for p in itertools.product("123456", repeat=4)]
book = {}
for line in open("out/final/K-d3-Q5.out"):
    if line.startswith("S "): _, t, rest = line.split(); h, g = rest.split(":"); book[(int(t), h)] = g
blind = [book[(t, "-")] for t in (1, 2, 3, 4)]; size = collections.Counter(answer(blind[0], s) for s in codes)
print(f"\nTABLE 4. A lag of three: four guesses sent blind, {', '.join(blind)}, and the fifth chosen by the answer to the first alone.\n")
print("| answer to " + blind[0] + " (black, white) | codes that give it | fifth guess |"); print("|---|---|---|")
for a in sorted(size, key=lambda a: -size[a]): print(f"| {a[0]}, {a[1]} | {size[a]} | {book.get((5, a), 'none needed')} |")
cells = collections.Counter(tuple(answer(g, s) for g in blind) for s in codes)
print(f"\nThe four blind answers leave {len(cells)} classes, the largest of {max(cells.values())} codes; {sum(1 for v in cells.values() if v == 1)} codes are already alone.")
