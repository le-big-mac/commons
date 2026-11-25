"""Evidence for the added section: each of its numbers recomputed from the result files, not looked up as a string.
usage: python -I checkfacts4.py README.md > checkfacts4.out"""
import sys, re, json, math, glob
RAW = open(sys.argv[1]).read(); R = ' '.join(RAW.split()); rd = lambda f: open(f).read(); ok = bad = 0
def check(name, cond, detail=""):
    global ok, bad; ok += bool(cond); bad += (not cond); print(("PASS  " if cond else "FAIL  ") + name + (("   " + str(detail)) if detail != "" else ""))
def says(*parts): return all(' '.join(p.split()) in R for p in parts)
cents = lambda t: 1200 * math.log2(1 + t); f2 = lambda t: f"{100 * t:.2f}%"; f3 = lambda t: f"{100 * t:.3f}%"
RG = {}
for f in glob.glob("rings2-*-*.json"):
    d = json.load(open(f)); RG[(d['kind'], d['weight'])] = d['rings']
one = {r['weight']: r['miss'] for r in json.load(open("onedisc.json"))}; W = sorted(one); two = {float(m): float(t) / 100 for m, t in re.findall(r"added mass\s+([\d.]+): two discs with free radii, least largest miss ([\d.]+)%", rd("twodisc2.out"))}
ex = lambda kind, m, n: RG[(kind, m)][str(n)]['exact']; load = lambda kind, m, n: RG[(kind, m)][str(n)]['a']; ends = lambda kind, m, n: (sum(e < RG[(kind, m)][str(n)]['miss'] + 2e-5 for e in RG[(kind, m)][str(n)]['ends']), len(RG[(kind, m)][str(n)]['ends']))
def runs(a):
    n = len(a); on = [x > 0.03 * max(a) for x in a]; out = []; j = 0
    while j < n:
        if on[j]:
            k = j
            while k < n and on[k]: k += 1
            out.append((round(j / n, 4), round(k / n, 4))); j = k
        else: j += 1
    return out
def chain(f): return {r['weight']: r for r in json.load(open(f))}
FD, FU = chain("chain-free-down.json"), chain("chain-free-up.json")
# pasted things
rows = [l for l in rd("table6.out").splitlines() if l.startswith("|")]; check("every row of the weight table is a row of table6.out, and none is missing", all(l in RAW for l in rows) and len(rows) == 19, f"{len(rows)} rows")
check("the scorecard block is verdicts3.out, line for line", all(l in RAW for l in rd("verdicts3.out").splitlines()))
sheet = ' '.join(rd("exact-prediction.md").split())
for lab in ("X1", "X5"):
    q = re.search(rf'{lab} in its sealed words: "(.*?)"', R).group(1); check(f"{lab} is quoted in its sealed words", q in sheet, q[:60])
SECTION = RAW[RAW.index("## A load of any radial shape"):RAW.index("## What this does not show\n")]
check("no placeholder is left and nothing calls the section unrefereed", "NOTE*" not in RAW and "not refereed" not in SECTION and "HERE" not in RAW)
# the headline
check("40 rings: 0.53% and 9 cents with 12 skins, all used; 0.77% and 13 cents with 1.43; the disc 3.19%", f2(ex('free', 12.0, 40)) == "0.53%" and round(cents(ex('free', 12.0, 40))) == 9 and f2(ex('free', 1.43, 40)) == "0.77%" and round(cents(ex('free', 1.43, 40))) == 13 and f2(one[1.43]) == "3.19%" and abs(sum(a * (((j + 1) / 40) ** 2 - (j / 40) ** 2) for j, a in enumerate(load('free', 12.0, 40))) - 12) < 0.01, f"{f3(ex('free', 12.0, 40))} {cents(ex('free', 12.0, 40)):.1f}c; {f3(ex('free', 1.43, 40))} {cents(ex('free', 1.43, 40)):.1f}c")
check("80 and 160 rings: 0.51% and 0.76% on both", all(f2(ex('free', 12.0, n)) == "0.51%" and f2(ex('free', 1.43, n)) == "0.76%" for n in (80, 160)), "; ".join(f"{n}: {f3(ex('free', 12.0, n))} {f3(ex('free', 1.43, n))}" for n in (80, 160)))
check("'In short': about 0.76% and 13 cents (80 and 160 rings); about 0.5% and 9 cents; a quarter of the disc's miss", round(cents(ex('free', 1.43, 80))) == 13 and round(cents(ex('free', 12.0, 160))) == 9 and round(cents(0.00504)) == 9 and 3.8 < one[1.43] / ex('free', 1.43, 80) < 4.5, f"disc over free at 1.43: {one[1.43] / ex('free', 1.43, 80):.2f}")
check("searches a weight: 21 or 22 on 40 rings, 14 or 15 on 80", all(ends('free', m, 40)[1] in (21, 22) and ends('free', m, 80)[1] in (14, 15) and ends('piled', m, 40)[1] in (21, 22) and ends('piled', m, 80)[1] in (14, 15) for m in W))
check("piled discs miss by more than two discs at 12 of 17 weights on 40 rings and 10 of 17 on 80, there by 0.03 points at most", len(W) == 17 and sum(ex('piled', m, 40) > two[m] + 1e-6 for m in W) == 12 and sum(ex('piled', m, 80) > two[m] + 1e-6 for m in W) == 10 and 0.025 < 100 * max(ex('piled', m, 80) - two[m] for m in W) < 0.035)
check("at 1.43 skins two discs and piled discs hardly better than one: 3.17% at best", f2(min(two[1.43], ex('piled', 1.43, 40), ex('piled', 1.43, 80))) == "3.17%" and f2(two[1.43]) == "3.19%")
bestd = {m: min(two[m], ex('piled', m, 40), ex('piled', m, 80)) for m in W}; sh = {m: ex('free', m, 80) / bestd[m] for m in W}
check("free load on 80 rings over the better of two discs and piled discs: 0.23 to 0.43 from 1.36 skins, 0.38 to 0.43 from 1.6", f"{min(sh[m] for m in W if m >= 1.36):.2f}" == "0.23" and f"{max(sh[m] for m in W if m >= 1.36):.2f}" == "0.43" and f"{min(sh[m] for m in W if m >= 1.6):.2f}" == "0.38", "; ".join(f"{m:g}: {sh[m]:.3f}" for m in W))
check("the bend (80 rings): 5.7, 1.7, 1.0, 0.82, 0.71, 0.68; eight times the weight", [f"{100 * ex('free', m, 80):.1f}" for m in (1.0, 1.3, 1.36)] == ["5.7", "1.7", "1.0"] and [f2(ex('free', m, 80)) for m in (1.4, 1.46, 1.5)] == ["0.82%", "0.71%", "0.68%"] and 7.5 < 12 / 1.43 < 8.5)
check("three parts from 1.4 skins up on 40 and on 80 rings; one hump up to 1.36", all(len(runs(load('free', m, n))) == 3 for m in W if m >= 1.4 for n in (40, 80)) and all(len(runs(load('free', m, n))) == 1 for m in W if m <= 1.36 for n in (40, 80)))
check("40 rings from 1.43 skins: core to 0.1 or 0.125; one ring 0.15 to 0.175; band 0.25 to 0.375 or 0.4; nothing beyond 0.425", all(runs(load('free', m, 40))[0][0] == 0 and runs(load('free', m, 40))[0][1] in (0.1, 0.125) and runs(load('free', m, 40))[1] == (0.15, 0.175) and runs(load('free', m, 40))[2][0] == 0.25 and runs(load('free', m, 40))[2][1] in (0.375, 0.4) for m in W if m >= 1.43) and all(max(load('free', m, 40)[17:]) < 1e-6 for m in W))
def hoop(m, n):
    a = load('free', m, n); j = max(range(n), key=lambda i: a[i]); k0 = j
    while k0 > 0 and a[k0 - 1] > 0.5 * a[j]: k0 -= 1
    k1 = j
    while k1 < n - 1 and a[k1 + 1] > 0.5 * a[j]: k1 += 1
    return round(a[j]), k1 - k0 + 1
check("the heavy ring: +45, +79, +92 at 1.43 skins (one ring, one ring, two rings of 160); +361, +699, +1,038 at 12, each one ring wide", [hoop(1.43, n) for n in (40, 80, 160)] == [(45, 1), (79, 1), (92, 2)] and [hoop(12.0, n) for n in (40, 80, 160)] == [(361, 1), (699, 1), (1038, 1)], str([hoop(m, n) for m in (1.43, 12.0) for n in (40, 80, 160)]))
a1 = rd("after4-1.out"); fl = [(float(a), float(b), float(c)) for a, b, c in re.findall(r"at least \+([\d.]+) inside [\d.]+: least [\d.]+% \(([\d.]+)% by exact matching\).*?core about \+([\d.]+)", a1)]
check("a floor under the gaps: 0.7679, 0.7695, 0.7801 against 0.7668; core about +11; 0.5448 against 0.5297; the cost 0.001 to 0.015 points", [f"{v[1]:.4f}" for v in fl] == ["0.7668", "0.7679", "0.7695", "0.7801", "0.5297", "0.5448"] and says("0.7679%, 0.7695% or 0.7801%, against 0.7668%", "0.5448% against 0.5297%") and all(10.5 < v[2] < 11.5 for v in fl[:4]) and f"{fl[1][1] - fl[0][1]:.3f}" == "0.001" and f"{fl[5][1] - fl[4][1]:.3f}" == "0.015" and fl[3][1] - fl[0][1] < 0.015, str(fl))
check("piled discs on 40 rings: 3.19% with 1.43 skins and 1.20% with 12", f2(ex('piled', 1.43, 40)) == "3.19%" and f2(ex('piled', 12.0, 40)) == "1.20%")
dl = {m: 100 * (two[m] - ex('piled', m, 80)) for m in W}; check("more layers: from 4 skins up piled discs on 80 rings are 0.11 to 0.15 points closer than two discs; within 0.06 from 1 to 2 skins", all(0.105 <= dl[m] <= 0.155 for m in W if m >= 4) and all(abs(dl[m]) < 0.06 for m in W if m <= 2), "; ".join(f"{m:g}: {dl[m]:+.3f}" for m in W))
x7 = re.split(r"^added mass ", rd("exact7.out"), flags=re.M)[1:]; r143 = [float(v) for v in re.search(r"ratios: (.*?);", x7[0]).group(1).split(", ")]; c12 = [float(v) for v in re.search(r"modes 2 to 9: (.*?);", x7[2]).group(1).split(", ")]; ap = [float(v) for v in re.search(r"are ([\d.]+) apart, \(3,1\) and \(1,2\) ([\d.]+), and the three aimed at 5 span ([\d.]+)", x7[0]).groups()]
check("ratios at 1.43 skins as quoted; pairs 12.4 and 23.9 cents apart, the three at 5 span 26.5", says("the ratios are 1, 1.9847, 3.0231, 3.0016, 4.0247, 3.9695, 4.9618, 5.0385, 4.9618.") and [f"{v:.4f}" for v in r143[1:]] == "1.9847 3.0231 3.0016 4.0247 3.9695 4.9618 5.0385 4.9618".split() and ap == [12.4, 23.9, 26.5], ap)
check("at 12 skins seven of eight are 9 cents off: (1,1), (0,2), the three at 5 flat; (2,1), (1,2) sharp", sum(round(abs(v)) == 9 for v in c12) == 7 and all(c12[i] < 0 for i in (0, 2, 5, 6, 7)) and all(c12[i] > 0 for i in (1, 4)), c12)
a2 = rd("after4-2345.out"); md = dict(((int(m), int(n)), float(x)) for m, n, x in re.findall(r"\((\d),(\d)\) ([\d.]+)", a2.split("5. The 40-ring load")[1])); above = sorted((x, k) for k, x in md.items() if x > 5.1 and x < 6.5)
check("the modes above the nine, by name: (1,3) 5.328, (5,1) 5.845, (0,4) 5.859, (2,3) 5.953, (3,2) 6.156; the disc's 5.933, 6.252, 5.468", [(k, f"{x:.3f}") for x, k in above] == [((1, 3), "5.328"), ((5, 1), "5.845"), ((0, 4), "5.859"), ((2, 3), "5.953"), ((3, 2), "6.156")] and says("(1,3) at 5.328, (5,1) at 5.845, (0,4) at 5.859, (2,3) at 5.953 and (3,2) at 6.156") and all(x in rd("modes.out") for x in ("5.9330", "6.2520", "5.4677")), above)
t2 = a2.split("2. How exactly")[1].split("3. The three")[0]; tv = [float(v) for v in re.findall(r"([\d.]+)%", t2)]
check("inexact making: 1% → median 0.93, worst 1.42; 3% → 1.23, 3.0; heaviest ring alone 1.15 or 1.00; moved a ring 2.9", "median miss 0.93%" in t2 and "the worst 1.42%" in t2 and "median miss 1.23%" in t2 and "the worst 3.00%" in t2 and "-2%: 1.15%" in t2 and "+2%: 1.00%" in t2 and "radius): 2.94%" in t2)
a6 = rd("after4-6.out"); check("the disc made inexactly: 3.37 or 3.29 against 3.16; 6.0 or 4.8", all(x in a6 for x in ("as found: 3.16%", "its load -1%: 3.37%", "its load +1%: 3.29%", "-0.025 of the radius: 5.96%", "+0.025 of the radius: 4.77%")))
b = rd("bessel3.out"); P = json.load(open("pieces2-1.43.json")); t3 = a2.split("3. The three")[1].split("4. The first")[0]; hp = [float(v) for v in re.findall(r"of the radius: ([\d.]+)%; its inner edge: ([\d.]+)%", t3)[0] + re.findall(r"of the radius: ([\d.]+)%; its inner edge: ([\d.]+)%", t3)[1]]
check("three even pieces: 0.769, 0.620, 0.563; the full digits; 1.15% as first printed; 1.13% to 1.48% with a hoop edge moved", [f"{float(x):.3f}" for x in re.findall(r"three even pieces, added mass [\d.]+: largest miss ([\d.]+)%", b)] == ["0.769", "0.620", "0.563"] and says("the radii are " + ", ".join(f"{x:.5f}" for x in P['radii']) + " and the loads " + ", ".join(f"+{x:.3f}" for x in P['loads'])) and "loads to one): 1.150%" in t3 and f"{min(hp):.2f}" == "1.13" and f"{max(hp):.2f}" == "1.48", hp)
e1 = [float(v) for v in re.findall(r"^\S.*?\s+(\d\.\d{4})%\s*$", rd("exact.out"), re.M)][:12]; longer = [float(v) for v in re.findall(r"restart \d, 3,000 iterations at most: ([\d.]+)%", rd("exact2.out"))] + [float(v) for v in re.findall(r"start\s+\d+ \(kind \d\): ([\d.]+)%", rd("exact4.out"))]
check("the sealed search: twelve starts between 0.577% and 0.669%; fifteen longer runs 0.5476% to 0.5749%, seven at 0.5476% to 0.5479%", len(e1) == 12 and f"{min(e1):.3f}" == "0.577" and f"{max(e1):.3f}" == "0.669" and len(longer) == 15 and min(longer) == 0.5476 and max(longer) == 0.5749 and sum(0.5476 <= v <= 0.5479 for v in longer) == 7)
old = {float(m): float(a) / 100 for m, a in re.findall(r"^\s+([\d.]+)\s+([\d.]+)% \(used", rd("exact3.out"), re.M)}
check("walks: up 0.530% and down 0.548% at 12 skins; the first table had the higher at every weight from 2 skins", f3(FU[12.0]['miss']) == "0.530%" and f3(FD[12.0]['miss']) == "0.548%" and all(abs(old[m] - max(FU[m]['miss'], FD[m]['miss'])) < 6e-6 and old[m] > min(FU[m]['miss'], FD[m]['miss']) + 1e-5 for m in old if m >= 2))
o = json.load(open("exact2.json"))['best40']['a']; ru, ro = runs(FU[12.0]['a']), runs(o); check("the earlier answer is the same three parts one ring further out", [(round(a + 0.025, 3), round(c + 0.025, 3)) for a, c in ru][1:] == [(round(a, 3), round(c, 3)) for a, c in ro][1:] and ro[0][1] == ru[0][1] + 0.025, f"{ro} against {ru}")
check("rings2.py: 0.510% and 0.758% on 80 rings; 0.507% and 0.756% on 160; the referee's 0.504% is below both at 12 skins", [f3(ex('free', 12.0, 80)), f3(ex('free', 1.43, 80)), f3(ex('free', 12.0, 160)), f3(ex('free', 1.43, 160))] == ["0.510%", "0.758%", "0.507%", "0.756%"] and "0.5045%" in rd("referee4/report.md"))
bz = [float(x) for x in re.findall(r"the 40-ring load, added mass [\d.]+: largest miss ([\d.]+)%", b)]; pm = json.load(open("exact.json"))['monotone']['miss']
check("the measure: 0.767 for 0.770 at 1.43; 0.530 for 0.531 at 12; piled 1.198 for 1.207", [f3(ex('free', 1.43, 40)), f"{bz[0]:.3f}%", f3(ex('free', 12.0, 40)), f"{bz[2]:.3f}%", f3(RG[('piled', 12.0)]['40']['miss']), f3(pm)] == ["0.767%", "0.770%", "0.530%", "0.531%", "1.198%", "1.207%"])
ag40 = {m: ends('free', m, 40) for m in W}; ag80 = {m: ends('free', m, 80) for m in W}
check("agreement on 40 rings: all up to 1.36; 17 of 22 at 1.43; 4 to 9 from 1.6. On 80: 3 of 15 at 1.43; 1 to 4 above", all(ag40[m][0] == ag40[m][1] for m in W if m <= 1.36) and ag40[1.43] == (17, 22) and min(ag40[m][0] for m in W if m >= 1.6) == 4 and max(ag40[m][0] for m in W if m >= 1.6) == 9 and ag80[1.43] == (3, 15) and min(ag80[m][0] for m in W if m > 1.43) == 1 and max(ag80[m][0] for m in W if m > 1.43) == 4)
check("piled discs: every search agrees from 1.7 skins on 40 rings and from 1.6 on 80", all(ends('piled', m, 40)[0] == ends('piled', m, 40)[1] for m in W if m >= 1.7) and all(ends('piled', m, 80)[0] == ends('piled', m, 80)[1] for m in W if m >= 1.6))
check("shaken: sixteen each; none lower; 15, 13 and 12 back", re.findall(r"(\d+) shaken restarts.*?; (\d+) ended within 0.002 points of the walks' answer, (\d+) below", rd("shake-summary.out")) == [("16", "15", "0"), ("16", "13", "0"), ("16", "12", "0")])
fi = rd("exact6-fine.out"); F = json.load(open("fine.json")); t = F["thinning allowed, down to a tenth of the bare skin"]['a']; a24 = F["weight limit 24 skins"]['a']
check("other limits: 24 skins 0.519%, 50 skins 0.522%, thinning 0.510%; three parts and a little load at the rim; nearly every bare ring thinned to the bound", all(x in fi for x in ("weight limit 24 skins: 0.5191%", "weight limit 50 skins: 0.5215%", "bare skin: 0.5095%")) and runs(a24)[:3] == ru and 0 < a24[39] < 1 and max(a24[17:39]) < 0.05 and sum(v < -0.899 for v in t) >= sum(v < 0 for v in t) - 1)
pc = [(float(a), float(c)) for a, c in re.findall(r"least largest miss ([\d.]+)%.*?a core of \+[\d.]+ inside ([\d.]+)", rd("pieces.out"))]; check("three pieces from scratch: 1.46%, 0.81%, 0.79%; a disc out to 0.25 to 0.31", [f"{min(pc[i][0], pc[i + 1][0]):.2f}" for i in (0, 2, 4)] == ["1.46", "0.81", "0.79"] and all(0.25 <= k <= 0.31 for _, k in pc))
check("X5: ten of the sealed search's twelve starts at 1.2071%; 1.198%, 1.189%, 1.183% on 40, 80, 160 rings", len(re.findall(r"^\s+(?:two discs|one disc|random \d+)\s+1\.2071%", rd("exact.out"), re.M)) == 10 and [f3(ex('piled', 12.0, n)) for n in (40, 80, 160)] == ["1.198%", "1.189%", "1.183%"])
s3 = rd("sound3.out"); check("the sound: 56 seconds; the eight strongest partials; (1,3) and (2,3); none of the three aimed at 5 among them", "56.4 seconds" in s3 and "rings  14 modes up to 6.6 times the lowest; the eight strongest when struck at half the radius: 1.000, 1.985, 3.002, 3.023, 3.969, 4.025, 5.329, 5.953" in s3 and abs(md[(1, 3)] - 5.329) < 0.002 and abs(md[(2, 3)] - 5.953) < 0.002 and all(abs(md[k] - x) > 0.05 for k in ((4, 1), (2, 2), (0, 3)) for x in (5.329, 5.953)))
v = rd("verdicts.out") + rd("verdicts2.out"); v3 = rd("verdicts3.out"); n12 = len(re.findall(r"^[DGL]\d ", v, re.M)); h12 = len(re.findall(r"^[DGL]\d .*?odds \d\.\d\d  held", v, re.M)); n5 = len(re.findall(r"^X\d ", v3, re.M)); void = v3.count("  void    "); h5 = len(re.findall(r"^X\d .*?odds \d\.\d\d  held", v3, re.M)); f5 = v3.count("scored FAILED")
check("the tallies: sheet four has five lines, one scored failed, one held, three void; with it seventeen lines, fourteen scored, eleven held", (n5, f5, h5, void) == (5, 1, 1, 3) and (n12 + n5, n12 + n5 - void, h12 + h5) == (17, 14, 11) and says("five lines: one scored failed, one held, three void. With it: seventeen sealed lines, fourteen scored, eleven held."), (n12, h12, n5, f5, h5, void))
t4 = a2.split("4. The first table")[1].split("5. The 40-ring")[0]; check("the first table's two discs: 1.59% as printed, 1.55% at full precision", "): 1.550%; as printed" in t4 and "0.234): 1.592%" in t4)
rep = rd("referee4/report.md"); check("the second referee's report has fourteen numbered findings and begins with its marker", rep.startswith("REFEREE REPORT: drum, fourth sheet") and len(re.findall(r"^\d+\. \*\*", rep.split("2. **Errors and overreach")[1].split("3. **Numbers side by side")[0], re.M)) == 14)
print(f"\n{ok} checks pass, {bad} fail")
