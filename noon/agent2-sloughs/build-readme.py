"""Fill README.src.md: tables from tables.out, blocks from the .out files, every number in the hand-written parts from the
files the runs wrote (the {{tokens}}), and the few sentences that were written last from fill.json.   usage: python -I build-readme.py"""
import json, re, math, glob, os, numpy as np
s = open("README.src.md").read(); t = open("tables.out").read(); fill = json.load(open("fill.json"))
s = s.replace("HOW-HERE", open("how.md").read().rstrip("\n"))
def table(k):
    m = re.search(rf"TABLE {k}\. (.*?)\n\n(.*?)(?=\n\nTABLE|\n\nNOTE|\Z)", t, re.S); return f"**Table {k}.** {m.group(1)}\n\n{m.group(2).strip()}"
for k in (1, 2, 3, 4, 5, 6, 7, 8, 9): s = s.replace(f"TABLE{k}-HERE", table(k))
s = s.replace("AFTER2-HERE", re.search(r"\nNOTE A\. (Two more runs made after the referee.*?)\n", t).group(1))
s = s.replace("VERDICTS-HERE", open("verdicts.out").read().rstrip("\n"))
s = s.replace("LONG-HERE", open("long.out").read().rstrip("\n")); s = s.replace("REACH-HERE", open("reach.out").read().rstrip("\n"))
G = json.load(open("out/grid/settings.json")); E = json.load(open("out/extra/settings.json")); W = json.load(open("out/wide/settings.json")); Pp = json.load(open("out/paper/settings.json"))[0]
g = lambda P, dc: [r for r in G if r["P"] == P and r["DC"] == dc][0]; w = lambda P, dc: [r for r in W if r["P"] == P and r["DC"] == dc][0]
e = lambda **kw: [r for r in E if all(r[k] == v for k, v in kw.items())][0]
Ps = (2, 3, 4.5, 6); dcs = (0.2, 0.4, 0.8); base = g(3, 0.4); runs = json.load(open("out/grid/runs.json"))
tok = {}
tok["grid_min"] = "%.2f" % min(r["Sbar"] for r in G); tok["grid_max"] = "%.2f" % max(r["Sbar"] for r in G)
tok["base"] = "%.2f" % base["Sbar"]; tok["base_se"] = "%.2f" % base["se"]; tok["run_min"] = "%.2f" % min(x["Sbar"] for x in runs)
tok["p_rise"] = "%.0f" % (100 * (g(6, 0.4)["Sbar"] / g(2, 0.4)["Sbar"] - 1))
falls = [100 * (1 - g(P, 0.8)["Sbar"] / g(P, 0.2)["Sbar"]) for P in Ps]; tok["dc_fall_lo"] = "%.0f" % min(falls); tok["dc_fall_hi"] = "%.0f" % max(falls)
assert all(g(P, dcs[i])["Sbar"] > g(P, dcs[i + 1])["Sbar"] for P in Ps for i in (0, 1)) and all(g(Ps[i], dc)["Sbar"] < g(Ps[i + 1], dc)["Sbar"] for dc in dcs for i in (0, 1, 2)), "rises and falls"
tok["wide16"] = ", ".join("%.2f" % w(P, 1.6)["Sbar"] for P in Ps[:-1]) + " and %.2f" % w(Ps[-1], 1.6)["Sbar"]
tok["wide32"] = ", ".join("%.2f" % w(P, 3.2)["Sbar"] for P in Ps[:-1]) + " and %.2f" % w(Ps[-1], 3.2)["Sbar"]
assert all(g(P, 0.8)["Sbar"] > math.pi > w(P, 1.6)["Sbar"] for P in Ps), "pi between 0.8 and 1.6"
spread16 = max(w(P, 1.6)["Sbar"] for P in Ps) - min(w(P, 1.6)["Sbar"] for P in Ps); tok["wide16_spread"] = "%.2f" % spread16
assert all(w(Ps[i], 3.2)["Sbar"] > w(Ps[i + 1], 3.2)["Sbar"] for i in (0, 1, 2)) and all(w(Ps[i], 0.1)["Sbar"] < w(Ps[i + 1], 0.1)["Sbar"] for i in (0, 1, 2)), "order in P at 3.2 and at 0.1"
tok["narrow"] = ", ".join("%.2f" % w(P, 0.1)["Sbar"] for P in Ps[:-1]) + " and %.2f" % w(Ps[-1], 0.1)["Sbar"]
steps = [((g(Ps[i + 1], dc)["Sbar"] - g(Ps[i], dc)["Sbar"]) / math.hypot(g(Ps[i + 1], dc)["se"], g(Ps[i], dc)["se"]), "between P = %g and %g at a cutoff distance of %g" % (Ps[i], Ps[i + 1], dc)) for dc in dcs for i in (0, 1, 2)]
steps += [((g(P, dcs[i])["Sbar"] - g(P, dcs[i + 1])["Sbar"]) / math.hypot(g(P, dcs[i])["se"], g(P, dcs[i + 1])["se"]), "between cutoff distances of %g and %g at P = %g" % (dcs[i], dcs[i + 1], P)) for P in Ps for i in (0, 1)]
assert len(steps) == 17
tok["weakest"] = "the smallest of those seventeen steps, %s, is %.1f times its standard error" % (min(steps)[1], min(steps)[0])
cr = [float(x) for x in re.search(r"The four crossings: ([\d., ]+)\.", t).group(1).split(", ")]; tok["cross_lo"] = "%.1f" % min(cr); tok["cross_hi"] = "%.1f" % max(cr)
bo = open("base.out").read(); m6 = re.search(r"six seeds .*: mean ([\d.]+), standard error ([\d.]+)", bo); tok["base6"] = "%.2f" % float(m6.group(1)); tok["base6_se"] = "%.2f" % float(m6.group(2))
tok["ref_base"] = re.search(r"written blind .*: ([\d.]+ and [\d.]+), two seeds", bo).group(1)
srt = sorted(r["Sbar"] for r in G); tok["margin_lo"] = "%.2f" % (srt[1] - math.pi); tok["margin_hi"] = "%.2f" % (srt[-1] - math.pi); tok["corner_se"] = "%.2f" % g(2, 0.8)["se"]; tok["corner_margin"] = "%.2f" % (g(2, 0.8)["Sbar"] - math.pi); assert min(G, key=lambda r: r["Sbar"]) is g(2, 0.8)
def rawmean(fn, lo=None, hi=None):
    r = np.array([[float(v) for v in l.split()[:3]] for l in open(fn) if l.strip() and not l.startswith("#")]); T = float(open(fn).readline().split(" T=")[1].split()[0]); assert r[-1, 0] >= T - 1.5, fn
    return float(r[(r[:, 0] >= (T / 2 if lo is None else lo)) & (r[:, 0] <= (T if hi is None else hi) + 1e-9), 2].mean())
tok["fine01"] = "%.2f" % rawmean("out/after/fine01.out")
if os.path.exists("out/after/corner-dt2.done"):
    cd2 = rawmean("out/after/corner-dt2.out"); assert cd2 < min(g(2, 0.8)["each"]); tok["corner_clause"] = "one run of it with half the time step gives %.2f, below all four and %.2f above π, and the two refinements I did not run there took 1.3%% and 1.8%% off at the base case" % (cd2, cd2 - math.pi); tok["corner_limit"] = "the one run at half the time step is %.2f lower than the four as run; I have none at half the spacing, which at the base case took off 1.3%%." % (round(g(2, 0.8)["Sbar"], 2) - round(cd2, 2))
    assert cd2 > math.pi
else:
    tok["corner_clause"] = "the one run of it with half the time step was still going when this page went to its second referee"; tok["corner_limit"] = "no refinement had finished when this page went to its second referee."
ml = {(l.split()[0], l.split()[1], l.split()[-1]): float(l.split()[4].rstrip("%")) for l in open("minloop.out") if l.strip() and not l.startswith("#")}
tok["ml32_lo"] = "%.0f" % min(v for k, v in ml.items() if k[1] == "3.2" and k[2] == "out/wide"); tok["ml32_hi"] = "%.0f" % max(v for k, v in ml.items() if k[1] == "3.2" and k[2] == "out/wide"); tok["ml_grid"] = "%.1f" % max(v for k, v in ml.items() if k[2] == "out/grid")
m32 = [rawmean("out/after/minloop-P%g-dc3.2.out" % P) for P in Ps]; w32 = [w(P, 3.2)["Sbar"] for P in Ps]; tok["sp3"] = "%.2f" % (max(w32) - min(w32)); tok["sp6"] = "%.2f" % (max(m32) - min(m32)); assert max(m32) - min(m32) < 0.3 * (max(w32) - min(w32)); tok["min32"] = ", ".join("%.2f" % v for v in m32[:-1]) + " and %.2f" % m32[-1]
orr = open("open-reach.out").read()
orat = lambda label: re.search(r"^%s, t = 12.5 to 125: length/distance ([\d.]+ ± [\d.]+)" % re.escape(label), orr, re.M).group(1)
tok["open_quiet"] = orat("quiet inlet"); tok["open_fed"] = orat("fed inlet"); tok["open_k9"] = orat("quiet inlet, pushes of 1e-9")
tok["fed_lv_span"] = re.search(r"^fed inlet, t = 12.5 to 125: .*length/272 ([\d.]+) ±", orr, re.M).group(1)
hd = lambda tag: [int(x) for x in re.search(r"^%s: ([\d, ]+)$" % tag, orr, re.M).group(1).split(", ")]
tok["head_quiet"] = "%d to %d" % (min(hd("quiet")), max(hd("quiet"))); tok["head_k9"] = "%d to %d" % (min(hd("quiet-k9")), max(hd("quiet-k9"))); tok["head_k6"] = "%d to %d" % (min(hd("quiet-k6")), max(hd("quiet-k6")))
tok["ml16_a"] = "%.0f" % ml[("4.5", "1.6", "out/wide")]; tok["ml16_b"] = "%.0f" % ml[("6", "1.6", "out/wide")]
m16 = [rawmean("out/after/minloop-P%g-dc1.6.out" % P) for P in Ps]; tok["min16"] = ", ".join("%.2f" % v for v in m16[:-1]) + " and %.2f" % m16[-1]
tok["corner_seeds"] = ", ".join("%.2f" % v for v in g(2, 0.8)["each"])
tok["sd_lo"] = "%.0f" % (100 * min(r["sd_rel"] for r in G)); tok["sd_hi"] = "%.0f" % (100 * max(r["sd_rel"] for r in G))
b1 = [x for x in runs if x["P"] == 3 and x["DC"] == 0.4]; tok["base_lo"] = "%.2f" % min(x["smin"] for x in b1); tok["base_hi"] = "%.2f" % max(x["smax"] for x in b1)
tok["sd400"] = "%.0f" % (100 * e(LX=400.0)["sd_rel"]); tok["sd100"] = "%.0f" % (100 * e(LX=100.0, FEED=0)["sd_rel"]); tok["m9"] = "%.1f" % (100 * base["sd_rel"])
tok["p36"] = "%.2f" % (g(6, 0.4)["Sbar"] - g(3, 0.4)["Sbar"])
span = []
for f in sorted(glob.glob("out/paper/beatton-s*.out")):
    r = np.array([[float(v) for v in l.split()[:3]] for l in open(f) if l.strip() and not l.startswith("#")]); span.append(r[(r[:, 0] >= 12.5) & (r[:, 0] <= 125), 2].mean())
tok["paper_span_mean"] = "%.2f" % np.mean(span); tok["paper_span_se"] = "%.2f" % (np.std(span, ddof=1) / 2)
rr = {int(l.split()[0]): l.split() for l in open("reach.out") if l.strip() and not l.startswith("#")}
tok["r25"] = rr[25][3]; tok["r50"] = rr[50][3]; tok["r100"] = rr[100][3]; tok["r200"] = rr[200][3]; tok["r800"] = rr[800][3]; assert rr[200][3] <= rr[400][3] <= rr[800][3]; tok["reach_whole"] = "%.2f" % float(re.search(r"mean ([\d.]+) over", open("reach.out").read()).group(1))
v = open("verdicts.out").read(); m = re.search(r"the ten lines alone: held (\d+), failed (\d+); the two priced checks: held (\d+), failed (\d+), in part (\d+)", v)
import os
assert "not in yet" not in v or os.environ.get("DRAFT"), "check 2 is not in"
words = {0: "none", 1: "one", 2: "both", 5: "five", 6: "six", 4: "four", 7: "seven", 3: "three"}
assert (m.group(3), m.group(4), m.group(5)) == ("1", "0", "1"), "the checks' tally changed: reword line 8"
tok["held10"] = words[int(m.group(1))]
sheet = open("expectations.md").read(); failed = re.findall(r"^(M\d+|check \d) .*FAILED", v, re.M); quoted = []
for name in failed:
    if name.startswith("M"): quoted.append("- " + re.search(r"- (\*\*%s\*\* .*?)(?=\n- \*\*M|\n\nTwo checks)" % name, sheet, re.S).group(1).replace("\n  ", " "))
    else: quoted.append("- %s: " % name + {"check 1": "\"S̄ at LX = 100 and at LX = 400 agree within 5% (0.75)\"", "check 2": "\"S̄ at spacing 0.05 and at 0.1 agree within 5% (0.65)\""}[name])
tok["failed_lines"] = "\n".join(quoted); tok["early"] = "%.2f" % base["early_rel"]
d = [(float(a), float(b)) for a, b in re.findall(r"1e-5 at t = ([\d.]+), 1e-2 at t = ([\d.]+)", open("diverge.out").read())]; tok["div_lo"] = "%.0f" % min(b - 40 for a, b in d); tok["div_hi"] = "%.0f" % max(b - 40 for a, b in d)
tok["lx100"] = "%.2f" % e(LX=100.0, FEED=0)["Sbar"]; tok["lx400"] = "%.2f" % e(LX=400.0)["Sbar"]
curv = [r["meank"] * 2 * r["half_wave"] for r in G]; tok["curv_lo"] = "%.1f" % min(curv); tok["curv_hi"] = "%.1f" % max(curv)
tok["ratio_lo"] = "%.2f" % min(r["S_inflection"] for r in G); tok["ratio_hi"] = "%.2f" % max(r["S_inflection"] for r in G)
fb = e(FEED=1, P=3.0); tok["feed_wave"] = "%.1f" % (2 * fb["half_wave"]); tok["feed_stream"] = "%.1f" % (2 * fb["half_wave_stream"]); tok["feed_curv"] = "%.2f" % fb["meank"]
cam = [(14.6, 0.0060), (15.4, 0.0054), (15.1, 0.0045), (13.4, 0.0036), (14.6, 0.0032), (14.0, 0.0032), (13.1, 0.0040), (15.8, 0.0043), (13.4, 0.0043), (14.8, 0.0032)]   # their Table 1: half-width over depth, friction factor
tok["width_lo"] = "%.2f" % min(4 * b * c for b, c in cam); tok["width_hi"] = "%.2f" % max(4 * b * c for b, c in cam)
sk = {k: open("page/soak-%s.out" % k).read() for k in ("steady", "hurried")}
for k, v in sk.items():
    m = re.search(r"ended \S+ minutes (\d+) time reached ([\d.]+) loops cut (\d+) minutes with no advance (\d+) script errors \[\]", v); assert m and m.group(4) == "0" and m.group(1) == "100", k
    tok["soak_min"] = m.group(1); tok["soak_%s_time" % k[0]] = "{:,.0f}".format(float(m.group(2))); tok["soak_%s_cuts" % k[0]] = "{:,}".format(int(m.group(3)))
tok["soak_s_time"] = tok["soak_s_time"]; tok["soak_f_time"] = tok.pop("soak_h_time"); tok["soak_f_cuts"] = tok.pop("soak_h_cuts")
heaps = [int(x) for v in sk.values() for x in re.findall(r"heap (\d+) MB", v)]; tok["heap_lo"] = str(min(heaps)); tok["heap_hi"] = str(max(heaps))
tok["soak_f_mean"] = "%.2f" % float(re.findall(r"mean ([\d.]+), loops cut", sk["hurried"])[-1]); tok["lx100_se"] = "%.2f" % e(LX=100.0, FEED=0)["se"]
tc = open("page/test-core.out").read().strip().split("\n")[-1]; tok["core_line"] = "`page/test-core.out`: " + tc + "."
dc = open("page/drycheck.out").read(); tok["dry_peak"] = re.search(r"peak ([\d.]+) of full scale", dc).group(1); tok["dry_bells"] = re.search(r"s, (\d+) bells", dc).group(1)
fo = open("page/film.out").read(); m = re.search(r"(\d+) bells; hurried until ([\d.]+) s; time at the end ([\d.]+); (\d+) cutoffs", fo)
tok["film_line"] = "by the end the river's clock stands at %s and %s loops have rung; the sound's loudest sample is %s of full scale." % (m.group(3), m.group(1), re.search(r"peak ([\d.]+)", fo).group(1))
for k, val in fill.items(): assert s.count(k) >= 1, k; s = s.replace(k, val)
for k, val in tok.items():
    assert "{{%s}}" % k in s, k; s = s.replace("{{%s}}" % k, val)
left = re.findall(r"\{\{\w+\}\}|[A-Z0-9]+-HERE|REFEREE-[A-Z]+|SECOND-[A-Z]+|WRITTEN", s); assert not left, left
open("README.md", "w").write(s); json.dump(tok, open("tokens.json", "w"), indent=0, ensure_ascii=False); print("README.md", len(s), "bytes")
