"""The second sheet, gathered: m(1) to m(5) by name.c and again by name2.py, the scheme replayed at the first lag where each number of
questions works and refused one lag sooner, W at every lag, and the scorecard.   usage: python -I second.py > second.out
Writes second.json and verdicts2.out. The long runs (out/m4.out by par.sh, out/name2/ by name2.py in ten parts) are read from their files."""
import subprocess, sys, re, json, os, glob
py = sys.executable; N = 1296
idx = lambda c: sum((int(ch) - 1) * 6 ** (3 - i) for i, ch in enumerate(c))
def run_name(j, pre, extra=()):
    out = subprocess.run(["./name", "4", "6", str(j), *extra], stdin=open(pre) if pre else None, input=None if pre else "\n", capture_output=True, text=True, check=True).stdout
    m = re.search(r"# least (\d+) ([\d ]+?) ; questions j=\d+; prefixes (\d+), skipped by the floor (\d+), lists tried (\d+)", out); return int(m.group(1)), m.group(2).split(), int(m.group(3)), int(m.group(5))
m = {0: (N, [])}
v, q, pre, tried = run_name(1, None); assert pre == 1 and tried == N; m[1] = (v, q)
v, q, pre, tried = run_name(2, "openings-4-6-1.txt"); assert pre == 5 and tried == 5 * N; m[2] = (v, q)
v, q, pre, tried = run_name(3, "ordered-4-6-2.txt"); assert pre == 291; m[3] = (v, q)
t4 = open("out/m4.out").read(); sums = re.findall(r"# least (\d+)(?: ([\d ]+?))? ; questions j=4; prefixes (\d+), skipped by the floor (\d+), lists tried (\d+)", t4)
assert sum(int(s[2]) for s in sums) == 151235 and len(sums) == 10
best = min((int(l.split()[0]), l.split()[1:]) for l in t4.split("\n") if l and l[0].isdigit()); assert best[0] <= 25, "the floor was set at 25"
m[4] = best; skipped4 = sum(int(s[3]) for s in sums); tried4 = sum(int(s[4]) for s in sums)
five = ["1123", "2445", "2562", "3356", "1166"]
open("out/five.txt", "w").write(" ".join(str(idx(c)) for c in five) + "\n"); v, q, _, _ = run_name(5, "out/five.txt", ("-full",)); assert v == 0; m[5] = (0, five)
print("The least number of codes left unnamed after j blind questions and j rounds of naming (name.c; for j = 1 to 4 over every ordered list of\nquestions up to symmetry; for j = 5 the one list shown, since nothing can be less than 0). The questions are in the order they are asked:")
for j in range(1, 6): print(f"  m({j}) = {m[j][0]:4d}   with {' '.join(m[j][1])}")
fl = [int(x) for x in open("out/floors4.txt").read().split()]; assert len(fl) == 151235; above25, at25 = sum(1 for x in fl if x > 25), sum(1 for x in fl if x == 25)
print(f"  for j = 4: 151,235 triples, each with every fourth question. {skipped4:,} triples were passed over because their floor was above the least found so far in")
print(f"  their part of the run: 25 to begin with (the least on a first trial of 300 triples), 24 in the part that found it. {above25:,} triples have a floor above 25")
print(f"  and {at25} a floor of exactly 25; {tried4:,} lists of four were tried.")
import itertools
orders = sorted(run_name(4, None, ("-full",))[0] if False else int(re.search(r"# least (\d+)", subprocess.run(["./name", "4", "6", "4", "-full"], input=" ".join(str(idx(c)) for c in perm) + "\n", capture_output=True, text=True).stdout).group(1)) for perm in itertools.permutations(m[4][1]))
print(f"  the order matters: the same four in their 24 orders leave {orders[0]}, {orders[1]}, {orders[2]}, ... up to {orders[-1]}; only the order shown leaves {orders[0]}.")
# the same by name2.py
two = {}
for j in (1, 2, 3): two[j] = int(re.search(r"least (\d+)", subprocess.run([py, "-I", "name2.py", str(j), "0", "1"], capture_output=True, text=True, check=True).stdout).group(1))
parts = [open(f).read() for f in sorted(glob.glob("out/name2/m4-part*.out"))]; got = [re.search(r"least (\d+) with ([\d ]+); (\d+) openings", p) for p in parts]
assert len(parts) == 10 and all(got) and sum(int(g.group(3)) for g in got) == 151235; two[4] = min(int(g.group(1)) for g in got)
print("The same by name2.py (numpy, from the definition, no floor): " + ", ".join(f"m({j}) = {two[j]}" for j in (1, 2, 3, 4)) + ("   AGREES" if all(two[j] == m[j][0] for j in two) else "   DIFFERS"))
assert all(two[j] == m[j][0] for j in two)
# the schemes, replayed where each first works and refused one lag sooner
print("\nThe scheme with those questions, written out and replayed by verify.py at the first lag where it fits, and tried one lag sooner:")
first = {}
for j in (5, 4, 3, 2, 1):
    d0 = max(m[j][0] + j - 1, j - 1); first[j] = d0; f = f"out/scheme-j{j}-d{d0}.out"
    r = subprocess.run([py, "-I", "scheme.py", "4", "6", str(d0), *m[j][1]], capture_output=True, text=True); assert r.returncode == 0, r.stderr; open(f, "w").write(r.stdout)
    vv = subprocess.run([py, "-I", "verify.py", "4", "6", str(d0), str(d0 + 1 + j), "W", f], capture_output=True, text=True); assert vv.returncode == 0 and "every code is sent" in vv.stdout, vv.stdout
    sooner = subprocess.run([py, "-I", "scheme.py", "4", "6", str(d0 - 1), *m[j][1]], capture_output=True, text=True); refused = sooner.returncode != 0 and "left over" in sooner.stderr
    print(f"  {j} questions: lag {d0}, {d0 + 1 + j} letters: every code is sent; at lag {d0 - 1}: " + ("five questions are not all blind there (the first sheet has W(3) = 9)" if j == 5 else "the codes left over do not fit" if refused else "IT FITS"))
    assert refused or j == 5
# W at every lag
B = json.load(open("boards.json"))["4 6"]; early = B["W"]          # lags 0 to 3 from the first sheet
def W(d):
    if d < 4: return early[d]
    return min([N] + [d + 1 + j for j in range(1, 6) if m[j][0] <= d + 1 - j])
assert W(4) == B["W4"]
print("\nW at every lag (lags 0 to 3 from the first sheet's searches; from 4 on by the formula):")
ranges = []; d = 0
while d <= 1300:
    e = d
    while e + 1 <= 1300 and W(e + 1) - (e + 1) == W(d) - d and W(e + 1) < N and W(d) < N: e += 1
    if W(d) >= N:
        while e + 1 <= 1300 and W(e + 1) >= N: e += 1
    ranges.append((d, e, W(d) - d if W(d) < N else None)); d = e + 1
for a, b, off in ranges: print((f"  lags {a} to {b}: lag + {off}" if off is not None else f"  lags {a} and more: 1296, every code posted blind") if a != b else f"  lag {a}: {W(a)}")
flat = [d for d in range(1, 1300) if W(d) == W(d - 1)]; print("  lags at which the count does not rise from the lag before: " + ", ".join(map(str, flat[:8])) + (" ..." if len(flat) > 8 else ""))
json.dump(dict(m={j: m[j][0] for j in m}, questions={j: m[j][1] for j in m}, first_lag=first, ranges=ranges, flat=flat, name2=two, tried4=tried4, skipped4=skipped4), open("second.json", "w"), indent=1)
# the scorecard
lines = [("F1", "guessed", 0.45, m[4][0] == 2, f"m(4) = {m[4][0]} (sealed: 2, so that W(5) = 10); W(5) = {W(5)}"),
         ("F2", "guessed", 0.75, m[4][0] <= 4, f"m(4) = {m[4][0]} (sealed: at most 4)"),
         ("F3", "worked", 0.70, 700 <= m[3][0] <= 800, f"m(3) = {m[3][0]} (sealed: 700 to 800)"),
         ("F4", "worked", 0.70, 1180 <= m[2][0] <= 1200, f"m(2) = {m[2][0]} (sealed: 1180 to 1200)"),
         ("F5", "worked", 0.90, m[1][0] == 1282, f"m(1) = {m[1][0]} (sealed: 1282)"),
         ("F6", "worked", 0.80, all(W(d) == d + 5 for d in range(m[4][0] + 3, 501)), f"W(d) = d + 5 at every lag from {m[4][0] + 3} to 500: {all(W(d) == d + 5 for d in range(m[4][0] + 3, 501))} (sealed: from m(4) + 3 up to at least 500)")]
held = sum(l[3] for l in lines); by = {}; out = []
for name, mark, odds, ok, what in lines: out.append(f"{name:3s} {mark:8s} odds {odds:.2f}  {'held  ' if ok else 'FAILED'}  {what}"); by.setdefault(mark, [0, 0])[0 if ok else 1] += 1
out.append(f"\nheld {held}, failed {len(lines) - held}, of {len(lines)}; my mean odds {sum(l[2] for l in lines) / len(lines):.3f}; Brier {sum((l[2] - l[3]) ** 2 for l in lines) / len(lines):.4f}; had I said 0.5 on every line, 0.2500")
out.append("by the sheet's own marks: " + "; ".join(f"marked {k}: {a + b} lines, {a} held, {b} failed" for k, (a, b) in by.items()))
open("verdicts2.out", "w").write("\n".join(out) + "\n"); print("\n" + "\n".join(out))
