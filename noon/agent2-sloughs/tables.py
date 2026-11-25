"""tables.py -- the README's tables, from out/grid/settings.json, out/extra/settings.json and the loop files.
usage: python tables.py > tables.out"""
import json, glob, math
import numpy as np
G = json.load(open("out/grid/settings.json")); E = json.load(open("out/extra/settings.json"))
g = lambda P, dc: [r for r in G if r["P"] == P and r["DC"] == dc][0]
Ps = (2, 3, 4.5, 6); dcs = (0.2, 0.4, 0.8)
kmax = lambda P: math.sqrt(math.sqrt(P) - 1)

print("TABLE 1. The long-run mean of river length over valley length: the mean of the second half of each run, averaged over four seeds, ± the standard error of the four. LX = 200.\n")
print("| upstream weight P | cutoff distance 0.2 | 0.4 | 0.8 | fall from 0.2 to 0.8 |")
print("|---|---|---|---|---|")
for P in Ps:
    r = [g(P, dc) for dc in dcs]
    print("| %g | %s | %.0f%% |" % (P, " | ".join("%.2f ± %.2f" % (x["Sbar"], x["se"]) for x in r), 100 * (r[0]["Sbar"] - r[2]["Sbar"]) / r[0]["Sbar"]))
allS = [x for r in G for x in r["each"]]
print("\nAll %d runs: from %.2f to %.2f. Settings: from %.2f to %.2f." % (len(allS), min(allS), max(allS), min(r["Sbar"] for r in G), max(r["Sbar"] for r in G)))

print("\nTABLE 2. Other long-run numbers of the same runs. Wavelength: twice the mean straight distance between successive inflection points; along the stream: twice the mean length of river between them. The fastest small wave on a straight river has wavelength 2π/k with k² = √P − 1. Belt: greatest less least y of the river. Loops: per unit of time and per 100 D of valley, with their median length.\n")
print("| P | dc | sd of S(t), % of mean | first peak ÷ mean | wavelength | along the stream | fastest small wave | wavelength ÷ fastest | mean abs. curvature | belt | loops cut | median loop |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
for P in Ps:
    for dc in dcs:
        x = g(P, dc); lam = 2 * x["half_wave"]; lin = 2 * math.pi / kmax(P)
        arcs = []
        for f in glob.glob("out/grid/P%g-dc%g-s*.oxl" % (P, dc)):
            a = np.loadtxt(f, ndmin=2); T = a[-1, 0]; arcs.append(a[a[:, 0] > T / 2, 1])
        arcs = np.concatenate(arcs)
        print("| %g | %g | %.1f | %.2f | %.1f | %.1f | %.1f | %.2f | %.3f | %.0f | %.2f | %.1f |" % (P, dc, 100 * x["sd_rel"], x["peak_rel"], lam, 2 * x["half_wave_stream"], lin, lam / lin, x["meank"], x["belt"], 100 * x["cuts"], np.median(arcs)))

print("\nTABLE 3. Is it the cutoff distance in wavelengths that matters? The same twelve means, against dc divided by the wavelength of the fastest small wave.\n")
print("| dc ÷ fastest wavelength | P | dc | long-run mean |")
print("|---|---|---|---|")
rows = sorted(((dc * kmax(P) / (2 * math.pi), P, dc, g(P, dc)["Sbar"]) for P in Ps for dc in dcs))
for r in rows: print("| %.4f | %g | %g | %.2f |" % r)
x = np.log([r[0] for r in rows]); y = np.array([r[3] for r in rows]); c = np.polyfit(x, y, 1); res = y - np.polyval(c, x)
print("\nA straight line in the logarithm of the first column: mean %.2f at 0.05, falling %.2f for each doubling; the twelve lie within %.2f of it (root mean square %.2f)." % (np.polyval(c, math.log(0.05)), -c[0] * math.log(2), np.abs(res).max(), math.sqrt((res ** 2).mean())))
c2 = np.polyfit(np.log([r[2] for r in rows]), y, 1); res2 = y - np.polyval(c2, np.log([r[2] for r in rows]))
print("The same line in the logarithm of dc alone, ignoring P: the twelve lie within %.2f of it (root mean square %.2f)." % (np.abs(res2).max(), math.sqrt((res2 ** 2).mean())))

print("\nTABLE 4. The base case (P = 3, dc = 0.4) run otherwise. Each line: seeds, long-run mean ± standard error of the seeds.\n")
print("| what was changed | seeds | long-run mean | third-quarter and fourth-quarter means |")
print("|---|---|---|---|")
b = g(3, 0.4)
print("| nothing (LX = 200, spacing 0.1) | %d | %.2f ± %.2f | %.2f, %.2f |" % (b["seeds"], b["Sbar"], b["se"], b["q3"], b["q4"]))
def e(**kw): return [r for r in E if all(r[k] == v for k, v in kw.items())]
for label, kw in (("valley period LX = 100", dict(LX=100.0, FEED=0, DS=0.1)), ("valley period LX = 400", dict(LX=400.0, FEED=0, DS=0.1)), ("node spacing 0.05", dict(DS=0.05, FEED=0, LX=200.0)),
                  ("the feedback of length on slope, F0² = 0.1", dict(FEED=1, LX=200.0, DS=0.1, P=3.0))):
    for r in e(**kw): print("| %s | %d | %.2f ± %.2f | %.2f, %.2f |" % (label, r["seeds"], r["Sbar"], r["se"], r["q3"], r["q4"]))

import os
if os.path.exists("out/wide/settings.json"):
    W = json.load(open("out/wide/settings.json")); w = lambda P, dc: [r for r in W if r["P"] == P and r["DC"] == dc]
    print("\nTABLE 5. Not sealed: narrower and wider cutoff distances, two seeds each (± half the difference of the two), beside the sealed grid's three (four seeds, ± standard error). The 3.2 D column belongs to a rule of mine, that a loop must be longer than three cutoff distances to be cut, and not to the river (Table 8); nothing should be read from it. At 1.6 D that rule decides up to 18% of the cuts. The 0.1 D column was run at a node spacing equal to the cutoff distance.\n")
    print("| P | dc = 0.1 | 0.2 | 0.4 | 0.8 | 1.6 | 3.2 |")
    print("|---|---|---|---|---|---|---|")
    for P in Ps:
        cells = []
        for dc in (0.1, 0.2, 0.4, 0.8, 1.6, 3.2):
            if dc in dcs: x = g(P, dc); cells.append("%.2f ± %.2f" % (x["Sbar"], x["se"]))
            else:
                x = w(P, dc); cells.append(("%.2f ± %.2f" % (x[0]["Sbar"], abs(x[0]["each"][0] - x[0]["each"][1]) / 2)) if x and x[0]["seeds"] == 2 else "–")
        print("| %g | %s |" % (P, " | ".join(cells)))
    done = [r for r in W if r["seeds"] == 2]
    if done:
        print("\nWavelengths in the added runs (twice the mean distance between inflection points), and the sd of S(t) as a share of its mean. The rows at 3.2 D are under the same caution: there the median loop is the least length the rule allows.\n")
        print("| P | dc | wavelength | along the stream | their ratio | sd of S(t), % | loops cut per unit time per 100 D | median loop |")
        print("|---|---|---|---|---|---|---|---|")
        for r in sorted(done, key=lambda r: (r["P"], r["DC"])):
            arcs = []
            for f in glob.glob("out/wide/P%g-dc%g-s*.oxl" % (r["P"], r["DC"])):
                a = np.loadtxt(f, ndmin=2); T = a[-1, 0]; arcs.append(a[a[:, 0] > T / 2, 1])
            print("| %g | %g | %.1f | %.1f | %.2f | %.1f | %.2f | %.1f |" % (r["P"], r["DC"], 2 * r["half_wave"], 2 * r["half_wave_stream"], r["S_inflection"], 100 * r["sd_rel"], 100 * r["cuts"], np.median(np.concatenate(arcs))))
if os.path.exists("out/sweep/settings.json"):
    b = g(3, 0.4); files = json.load(open("out/sweep/runs.json"))
    def raw_mean(fn, upto=None):
        r = np.array([[float(v) for v in l.split()[:3]] for l in open(fn) if l.strip() and not l.startswith("#")]); m = r[:, 0] >= 1492.8 / 2
        if upto: m &= r[:, 0] <= upto + 1e-9
        return float(r[m, 2].mean())
    print("\nTABLE 6. Not sealed: the base case with each of my own choices changed, one at a time. Two runs part company within about forty units of time whatever the change (`diverge.out`), so each line is fresh rivers, to be set beside the base case's four seeds: %s, mean %.2f ± %.2f, single runs scattering by %.2f (their sd).\n" % (", ".join("%.2f" % v for v in b["each"]), b["Sbar"], b["se"], np.std(b["each"], ddof=1)))
    print("| what was changed | seeds | their means | mean | against the base case's %.2f |" % b["Sbar"])
    print("|---|---|---|---|---|")
    for tag, label in (("amin2", "a loop must be longer than 2 dc to be cut (3 in the study)"), ("amin5", "a loop must be longer than 5 dc"), ("smooth2", "two nodes dropped either side of each join"),
                       ("every1", "necks looked for at every step (every fifth in the study)"), ("dt2", "half the time step")):
        rr = sorted([x for x in files if x["file"].startswith(tag + "-")], key=lambda x: x["seed"])
        if rr:
            m = np.mean([x["Sbar"] for x in rr]); note = " (this change never came into play: the two runs are the base case's own, to the last digit)" if tag == "amin5" and all(abs(x["Sbar"] - b["each"][x["seed"] - 1]) < 1e-9 for x in rr) else ""
            print("| %s%s | %s | %s | %.2f | %+.1f%% |" % (label, note, ", ".join(str(x["seed"]) for x in rr), ", ".join("%.2f" % x["Sbar"] for x in rr), m, 100 * (m - b["Sbar"]) / b["Sbar"]))
    if os.path.exists("out/fine/runs.json"):
        rr = sorted(json.load(open("out/fine/runs.json")), key=lambda x: x["seed"]); upto = 1370
        m = np.mean([x["Sbar"] for x in rr]); bm = np.mean([raw_mean("out/grid/P3-dc0.4-s%d.out" % x["seed"], upto) for x in rr])
        bm4 = np.mean([raw_mean(f, upto) for f in sorted(glob.glob("out/grid/P3-dc0.4-s*.out"))])
        print("| node spacing 0.05 (0.1 in the study); stopped early, so these are means from t = 746 to %d, and the comparison is with the base case over the same stretch, %.2f | %s | %s | %.2f | %+.1f%% |" % (upto, bm4, ", ".join(str(x["seed"]) for x in rr), ", ".join("%.2f" % x["Sbar"] for x in rr), m, 100 * (m - bm4) / bm4))

# ---- after the referee ----
def raw(fn, lo=None, hi=None):
    r = np.array([[float(v) for v in l.split()[:3]] for l in open(fn) if l.strip() and not l.startswith("#")]); head = open(fn).readline(); T = float(head.split(" T=")[1].split()[0])
    assert r[-1, 0] >= T - 1.5, fn
    return float(r[(r[:, 0] >= (T / 2 if lo is None else lo)) & (r[:, 0] <= (T if hi is None else hi) + 1e-9), 2].mean())
done = lambda tag: sorted(f[:-5] + ".out" for f in glob.glob("out/after/%s.done" % tag))
if len(done("between-*")) == 24:
    W = json.load(open("out/wide/settings.json")); w = lambda P, dc: [r for r in W if r["P"] == P and r["DC"] == dc][0]
    print("\nTABLE 7. Added after the referee: cutoff distances between 0.8 and 1.6 D, two seeds each (± half their difference), with the neighbouring columns of Table 5; and where a straight line between neighbouring columns passes π.\n")
    print("| P | dc = 0.8 | 1.0 | 1.2 | 1.4 | 1.6 | passes π at about |")
    print("|---|---|---|---|---|---|---|")
    cross = []
    for P in Ps:
        xs = [0.8, 1.0, 1.2, 1.4, 1.6]; ys = [g(P, 0.8)["Sbar"]]; cells = ["%.2f ± %.2f" % (g(P, 0.8)["Sbar"], g(P, 0.8)["se"])]
        for dc in (1.0, 1.2, 1.4):
            v = [raw(f) for f in done("between-P%g-dc%.1f-s*" % (P, dc))]; assert len(v) == 2; ys.append(np.mean(v)); cells.append("%.2f ± %.2f" % (np.mean(v), abs(v[0] - v[1]) / 2))
        ys.append(w(P, 1.6)["Sbar"]); cells.append("%.2f ± %.2f" % (w(P, 1.6)["Sbar"], abs(w(P, 1.6)["each"][0] - w(P, 1.6)["each"][1]) / 2))
        k = max(i for i in range(4) if ys[i] > math.pi); assert ys[k + 1] <= math.pi; x = xs[k] + (ys[k] - math.pi) / (ys[k] - ys[k + 1]) * (xs[k + 1] - xs[k]); cross.append(x)
        print("| %g | %s | %.2f D |" % (P, " | ".join(cells), x))
    print("\nThe four crossings: %s." % ", ".join("%.2f" % x for x in cross))
    per = []
    for P in Ps:
        xs = [0.8, 1.0, 1.2, 1.4, 1.6]; two = []
        for s in (0, 1):
            ys = [g(P, 0.8)["each"][s]] + [raw(done("between-P%g-dc%.1f-s*" % (P, dc))[s]) for dc in (1.0, 1.2, 1.4)] + [w(P, 1.6)["each"][s]]
            k = max(i for i in range(4) if ys[i] > math.pi); two.append(xs[k] + (ys[k] - math.pi) / (ys[k] - ys[k + 1]) * (xs[k + 1] - xs[k]))
        per.append("P = %g: %.2f and %.2f" % (P, two[0], two[1]))
    print("Taking seeds 1 and 2 separately, the crossings are: %s. All of this is at the study's time step and spacing." % "; ".join(per))
if len(done("minloop-*")) == 8:
    W = json.load(open("out/wide/settings.json")); w = lambda P, dc: [r for r in W if r["P"] == P and r["DC"] == dc][0]
    print("\nTABLE 8. Added after the referee: the least loop that may be cut. The wide runs again with a loop needing 6 cutoff distances of river to be cut where the study has 3 (one seed), and the share of the study's loops that were cut within a tenth of its least length (`minloop.out`).\n")
    print("| P | dc | with 3 dc (Table 5, two seeds) | with 6 dc (one seed) | loops cut at the least length, with 3 dc |")
    print("|---|---|---|---|---|")
    share = {(l.split()[0], l.split()[1]): l.split()[4] for l in open("minloop.out") if l.strip() and not l.startswith("#") and l.split()[-1] == "out/wide"}
    for dc in (1.6, 3.2):
        for P in Ps: print("| %g | %g | %.2f | %.2f | %s |" % (P, dc, w(P, dc)["Sbar"], raw("out/after/minloop-P%g-dc%g.out" % (P, dc)), share[("%g" % P, "%g" % dc)]))
if done("fine01"):
    w01 = [r for r in json.load(open("out/wide/settings.json")) if r["P"] == 6 and r["DC"] == 0.1][0]
    corner = ("with half the time step: %.2f." % raw("out/after/corner-dt2.out")) if done("corner-dt2") else "with half the time step was still going when this page went to its second referee."
    print("\nNOTE A. Two more runs made after the referee, one seed each. The setting P = 6, cutoff distance 0.1 (%.2f ± %.2f on two seeds at node spacing 0.1, which is the cutoff distance itself) at node spacing 0.05: %.2f. The lowest setting of the sealed grid (P = 2, cutoff distance 0.8; %.2f ± %.2f on four seeds) %s A third, the same corner with necks looked for at every step, was begun and stopped: it could not have finished inside the two hours a background command is allowed." % (
        w01["Sbar"], abs(w01["each"][0] - w01["each"][1]) / 2, raw("out/after/fine01.out"), g(2, 0.8)["Sbar"], g(2, 0.8)["se"], corner))
if os.path.exists("open-reach.out"):
    import re
    o = open("open-reach.out").read()
    def ratio(label, span): return re.search(r"^%s, t = %s: length/distance ([\d.]+ ± [\d.]+)" % (re.escape(label), span), o, re.M).group(1)
    def dist(label, t): return re.search(r"^%s, at t = %s: distance between the ends ([\d, ]+) \(272" % (re.escape(label), t), o, re.M).group(1)
    per = [(raw(f, 12.5, 125), raw(f, 250, 500)) for f in sorted(glob.glob("out/paper/beatton-s*.out"))]; pm = np.mean(per, axis=0); ps = np.std(per, axis=0, ddof=1) / 2
    rb = [l.split() for l in open("referee2/blind.out") if l.split() and l.split()[0] in ("quiet", "fed")]
    refq = [float(x[2]) for x in rb if x[0] == "quiet"]; reff = [float(x[2]) for x in rb if x[0] == "fed"]
    print("\nTABLE 9. Added after the first referee: one paper's values (P = 6.43, cutoff distance 0.476 D0, valley 272 D0, the feedback on) on a repeating valley and on an open reach with its first node fixed and its last free (`open.c`, `open.sh`). Four seeds each, ± their standard error. For the open reaches the ratio is the paper's: length over the straight distance between the two ends. The second referee ran the two kinds of open reach with a program of its own; the rows with pushes are its test of my program, run again here after its report.\n")
    print("| | ratio over the paper's span, t = 12.5 to 125 | ratio over t = 250 to 500 | distance between the ends at t = 125, four seeds (272 at the start) | at t = 500 |")
    print("|---|---|---|---|---|")
    print("| repeating valley: length over valley length | %.2f ± %.2f | %.2f ± %.2f | | |" % (pm[0], ps[0], pm[1], ps[1]))
    for label, name in (("fed inlet", "open reach, the first node given the far end's curvature (the paper's rule, as I read it)"), ("fed inlet, pushes of 1e-9", "the same, every node pushed by 10⁻⁹ at every step"),
                        ("quiet inlet", "open reach, nothing coming in at the first node"), ("quiet inlet, pushes of 1e-9", "the same, every node pushed by 10⁻⁹ at every step"), ("quiet inlet, pushes of 1e-6", "the same, pushed by 10⁻⁶")):
        print("| %s | %s | %s | %s | %s |" % (name, ratio(label, "12.5 to 125"), ratio(label, "250 to 500"), dist(label, "125"), dist(label, "500")))
    print("| the second referee's program, the paper's rule (two seeds) | %s | 3.80, 3.83 | | |" % ", ".join("%.2f" % v for v in reff))
    print("| the second referee's program, nothing coming in (two seeds) | %s | 3.78, 3.70 | | |" % ", ".join("%.2f" % v for v in refq))
    print("| the paper prints | 4.46 | | | |")
