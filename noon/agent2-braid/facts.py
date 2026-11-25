"""facts.py -- read every number the README and the page's notes use out of the run files, and write facts.json.
usage: python -I facts.py"""
import re, json, os
def runlines(path):
    out = []
    for line in open(path):
        m = re.match(r"step (\d+): (?:time ([\d.e+-]+); )?streams ([\d.]+), wet (\d+)%, fullest cell (\d+)% of the water, relief ([\d.]+) row-falls", line)
        if m: out.append(dict(step=int(m.group(1)), time=float(m.group(2)) if m.group(2) else None, streams=float(m.group(3)), wet=int(m.group(4)), top=int(m.group(5)), relief=float(m.group(6))))
    return out
def at(rows, step):
    r = [x for x in rows if x["step"] == step]; assert len(r) == 1, (step, len(r)); return r[0]
def span(rows, key, lo, hi):
    v = [x[key] for x in rows if lo <= x["step"] <= hi]; return min(v), max(v), sum(v) / len(v), len(v)
F = {}
for name in ("kl04", "kl04s2", "kl02", "kl08"):
    rows = runlines("fate/%s.out" % name); F[name + "_n"] = len(rows); F[name + "_last"] = rows[-1]["step"]
    for key in ("streams", "wet", "top", "relief"):
        lo, hi, mean, n = span(rows, key, 1000000, 4000000); F["%s_%s_lo" % (name, key)] = lo; F["%s_%s_hi" % (name, key)] = hi; F["%s_%s_mean" % (name, key)] = round(mean, 2); F["%s_span_n" % name] = n
        lo, hi, mean, n = span(rows, key, 3100000, 4000000); F["%s_%s_end" % (name, key)] = round(mean, 2)
        lo, hi, mean, n = span(rows, key, 1000000, 1900000); F["%s_%s_early" % (name, key)] = round(mean, 2)
g = at(runlines("fate/kl04.out"), 600000); F.update({"grown_" + k: g[k] for k in ("streams", "wet", "top", "relief")})
for name in ("smooth", "smooth-capped", "gentle-capped", "after-kl0", "after-m1", "limit01"):
    rows = runlines("fate/%s.out" % name); last = rows[-1]; key = name.replace("-", "_")
    F[key + "_last"] = last["step"]; F.update({key + "_" + k: last[k] for k in ("streams", "wet", "top", "relief")})
    if last["time"] is not None: F[key + "_time"] = last["time"]
    F[key + "_maxrelief"] = max(x["relief"] for x in rows); F[key + "_maxstreams"] = max(x["streams"] for x in rows[1:]) if len(rows) > 1 else rows[0]["streams"]
    F[key + "_minwet"] = min(x["wet"] for x in rows)
m = re.search(r"relief at the start ([\d.]+) row-falls; halved by step (\d+); one thread and all the bed wet by step (\d+); relief under 0.05 row-falls by step (\d+)", open("fate/fade.out").read())
F["fade_start"], F["fade_half"], F["fade_one"], F["fade_sheet"] = float(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
# the step-length check: the run with steps a third as long, set beside the page's run at the nearest times
lim = runlines("fate/limit01.out"); ref = runlines("fate/kl04.out"); pairs = []
for x in lim:
    if x["step"] % 300000 == 0:
        y = min(ref, key=lambda r: abs(r["time"] - x["time"])); pairs.append((x, y))
F["limit_pairs"] = [[x["step"], x["time"], x["streams"], x["wet"], x["relief"], y["step"], y["time"], y["streams"], y["wet"], y["relief"]] for x, y in pairs]
# for the step-length check: each of the four ordinary runs at the moment nearest in the model's time to the end of the LIMIT 0.01 run
F["limit_ref"] = []; F["limit_ref_detail"] = []
for name in ("kl04", "kl04s2", "kl02", "kl08"):
    y = min(runlines("fate/%s.out" % name), key=lambda r: abs(r["time"] - lim[-1]["time"])); F["limit_ref"].append(y["relief"]); F["limit_ref_detail"].append([name, y["step"], y["time"], y["relief"]])
# the ripple table: the greatest rate at each setting

# the earlier set on the smaller bed
for name in ("k0", "m1", "n1", "b1", "b2"):
    rows = runlines("longer/%s.out" % name); last = rows[-1]; F["small_%s" % name] = [last["step"], last["streams"], last["wet"], last["top"], last["relief"]]
# the long runs, as table cells: threads / share wet / roughness, at 600,000 steps and as means over two later stretches
def cell(rows, lo, hi):
    v = [x for x in rows if lo <= x["step"] <= hi]; assert v, (lo, hi)
    return "%.1f / %d%% / %.1f" % (sum(x["streams"] for x in v) / len(v), round(sum(x["wet"] for x in v) / len(v)), sum(x["relief"] for x in v) / len(v))
def means(rows, lo, hi):
    v = [x for x in rows if lo <= x["step"] <= hi]; return [round(sum(x[k] for x in v) / len(v), 2) for k in ("streams", "wet", "relief")] + [len(v)]
T = ["| run | at 600,000 steps | steps 1.6 to 2.0 million | steps 3.6 to 4.0 million |", "|---|---|---|---|"]
for name, label in (("kl04", "the page's setting (sideways constant 0.4)"), ("kl04s2", "the same, other sand"), ("kl02", "sideways constant 0.2"), ("kl08", "sideways constant 0.8")):
    rows = runlines("fate/%s.out" % name); assert rows[-1]["step"] == 4000000
    T.append("| %s | %s | %s | %s |" % (label, cell(rows, 600000, 600000), cell(rows, 1600000, 2000000), cell(rows, 3600000, 4000000)))
    F[name + "_m2"] = means(rows, 1600000, 2000000); F[name + "_m4"] = means(rows, 3600000, 4000000); F[name + "_600k"] = means(rows, 600000, 600000)
F["table_fixed"] = "\n".join(T)
T = ["| run | at 600,000 steps | steps 1.6 to 2.0 million |", "|---|---|---|"]
for folder, name, label in (("loop", "kl02", "joined end to end, sideways constant 0.2"), ("loop", "kl04", "joined, 0.4"), ("loop", "kl08", "joined, 0.8"),
                            ("sand", "s2", "sand fed at the head, 2 sheets' worth"), ("sand", "s4", "fed, 4"), ("sand", "s8", "fed, 8"), ("sand", "s16", "fed, 16")):
    rows = runlines("%s/%s.out" % (folder, name)); assert rows[-1]["step"] == 2000000
    T.append("| %s | %s | %s |" % (label, cell(rows, 600000, 600000), cell(rows, 1600000, 2000000))); F["%s_%s_m2" % (folder, name)] = means(rows, 1600000, 2000000)
F["table_other"] = "\n".join(T)
k = runlines("fate/kl04.out"); F["early"] = [[x["step"], x["streams"], x["wet"], x["relief"]] for x in k if x["step"] in (100000, 300000, 600000)]
# supply.out: the cut below the head and the ratio of sand out to sand in
sup = open("supply.out").read()
F["supply_ratio"] = [float(x) for x in re.findall(r"out/in ([\d.]+)", sup)]; F["supply_times"] = [float(x) for x in re.findall(r": ([\d.]+) times that", sup)]
F["supply_cut"] = [float(x) for x in re.findall(r"rows 1-8: where the water is (-?[\d.]+)", sup)]
so = open("soak.out").read(); mins = re.findall(r"minute (\d+): (\d+) steps.*?heap (\d+) MB", so)
F["soak_minutes"] = int(mins[-1][0]); F["soak_first"] = int(mins[0][1]); F["soak_last"] = int(mins[-1][1]); F["soak_heap"] = sorted(set(int(m[2]) for m in mins)); F["soak_end"] = re.search(r"ended .*", so).group(0)
sm = runlines("fate/smooth.out"); F["smooth_looks"] = len([x for x in sm if x["step"] >= 50000]); F["smooth_after_max"] = max(x["relief"] for x in sm if x["step"] >= 50000); F["smooth_after_min"] = min(x["relief"] for x in sm if x["step"] >= 50000)
F["n1_300_wet"] = at(runlines("longer/n1.out"), 300000)["wet"]
F["limit01_m2"] = means(lim, 1600000, 2000000)
up = re.findall(r"\(([\d.]+)%\) have no way down, and they pass on ([\d.]+)% of the water", open("uphill.out").read()); assert len(up) == 5
F["up_cells"] = [float(a) for a, b in up]; F["up_water"] = [float(b) for a, b in up]
cap = runlines("fate/smooth-capped.out"); F["capped_steps"] = cap[-1]["step"]; F["capped_always"] = all(abs(x["time"] - 5 * x["step"]) < 1e-6 * x["time"] for x in cap)
for a in ("1", "1.5", "2", "2.5"):
    rr = runlines("fate/rough%s.out" % a); assert rr[-1]["step"] == 600000; F["rough" + a] = [rr[-1]["streams"], rr[-1]["wet"], rr[-1]["relief"], max(x["streams"] for x in rr), min(x["wet"] for x in rr)]
dd = runlines("fate/ditch.out"); F["ditch"] = [dd[0]["streams"], dd[0]["wet"], dd[0]["relief"], max(x["streams"] for x in dd[1:]), min(x["wet"] for x in dd[1:]), max(x["relief"] for x in dd[1:]), dd[1]["step"], dd[-1]["step"]]
# ---- after the referee
def reflines(path, section=None):          # the referee's files: step threads wet rough maxshare ... [| time T]
    out = []; on = section is None
    for line in open(path):
        if line.startswith("=="): on = (section is None) or line.startswith(section); continue
        p = line.split()
        if on and p and p[0].isdigit() and len(p) >= 5:
            m = re.search(r"time ([\d.]+)", line); out.append(dict(step=int(p[0]), streams=float(p[1]), wet=100 * float(p[2]), relief=float(p[3]), top=100 * float(p[4]), time=float(m.group(1)) if m else None))
    return out
mine = [at(runlines(f), 600000) for f in ["fate/kl04.out", "fate/kl04s2.out"] + ["seeds/s%d.out" % k for k in range(3, 9)]]
rA = reflines("referee/blind.out", "== Run A (A=3, seed 20261123)"); rA2 = reflines("referee/blind.out", "== Run A, second seed"); rC = reflines("referee/blind.out", "== Run C")
theirs = [[x for x in rA if x["step"] == 600000][0], [x for x in rA2 if x["step"] == 600000][0]]
F["draws"] = [[x["streams"], round(x["wet"]), x["relief"]] for x in mine + theirs]
win = [x for x in rA if 1600000 <= x["step"] <= 2000000]; way = [x for x in rA if 600000 <= x["step"] <= 2000000]
F["refA"] = dict(s6=theirs[0]["streams"], w6=theirs[0]["wet"], s2=sum(x["streams"] for x in win) / len(win), w2=sum(x["wet"] for x in win) / len(win), wlo=min(x["wet"] for x in way), whi=max(x["wet"] for x in way), sB=theirs[1]["streams"], wB=theirs[1]["wet"], n2=len(win))
cn = reflines("referee/Cnoon.txt"); F["refCnoon"] = [[x["step"], x["streams"], x["wet"], x["top"], x["relief"]] for x in cn if x["step"] in (600000, 1500000)]
F["refC"] = [rC[-1]["step"], rC[-1]["streams"], rC[-1]["wet"], rC[-1]["top"], rC[-1]["relief"]]
a2 = reflines("referee/A2t.txt"); F["refA2t"] = [[x["step"], x["time"], x["relief"]] for x in a2 if x["step"] in (450000, 600000)]
kk = runlines("fate/after-kl0.out"); F["kl0_last3"] = [x["relief"] for x in kk[-3:]]
lin = open("linear.out").read().strip().split("\n\n"); F["linear"] = []
for t in lin:
    m = re.search(r"CS ([\d.]+) \((\d+) x slope\), KL ([\d.]+); (the page\'s bed|a bed of 2,600 rows)", t); g = re.search(r"(\d+) shapes; (\d+) grow; greatest rate (-?[\d.]+) at", t); w = re.search(r"to within ([\d.e+-]+)", t)
    raw = re.search(r"2 half-waves across, no length along: with the smooth bed\'s change left in, (-?[\d.]+) at a height of 1e-4 and (-?[\d.]+) at 1e-2; taken off, (-?[\d.]+) and (-?[\d.]+)", t)
    F["linear"].append(dict(cs=float(m.group(1)), bed="page" if "page" in m.group(4) else "long", shapes=int(g.group(1)), grow=int(g.group(2)), greatest=float(g.group(3)), within=float(w.group(1)), raw=[float(x) for x in raw.groups()]))
dv = open("diverge.out").read(); F["diverge"] = [float(re.search(r"after 200 steps ([\d.]+)", dv).group(1)), float(re.search(r"after 5000 steps ([\d.]+)", dv).group(1))]
so2 = re.findall(r"minute (\d+): (\d+) steps, ([\d.]+) threads, (\d+)% wet", so); F["soak_last_streams"] = float(so2[-1][2]); F["soak_last_wet"] = int(so2[-1][3])
bud = {}; 
for line in open("budget.out"):
    m = re.match(r"(\S+): mean height above the start (-?[\d.]+); by quarters from the head (.*?); lowest cell (-?[\d.]+)", line); bud[m.group(1)] = [float(m.group(2)), [float(x) for x in m.group(3).split(", ")], float(m.group(4))]
F["budget"] = bud
lk = runlines("loop/kl02.out"); F["lk02"] = [at(lk, 600000)["wet"], min(x["wet"] for x in lk if 800000 <= x["step"] <= 1000000), max(x["wet"] for x in lk if 800000 <= x["step"] <= 1000000), min(x["wet"] for x in lk if 1600000 <= x["step"] <= 2000000), max(x["wet"] for x in lk if 1600000 <= x["step"] <= 2000000)]
F["t2_loop"] = [at(runlines("loop/%s.out" % n), 2000000)["time"] for n in ("kl02", "kl04", "kl08")]; F["t2_fixed"] = [at(runlines("fate/%s.out" % n), 2000000)["time"] for n in ("kl04", "kl04s2", "kl02", "kl08")]
F["t4"] = [F[n + "_m4"][0] for n in ("kl04", "kl04s2", "kl02", "kl08")]
F["limit01_at_3990"] = [x["relief"] for x in lim if abs(x["time"] - 3990) < 1]
# the referee's blind numbers beside mine, as a table
def c3(x, d=2): return ("%.1f / %.0f%% / %." + str(d) + "f") % (x["streams"], x["wet"], x["relief"])
rB = reflines("referee/blind.out", "== Run B (A=0.2"); rB2 = reflines("referee/blind.out", "== Run B, second seed"); rD = reflines("referee/blind.out", "== Run D")
assert all(x["streams"] == 1.0 and x["wet"] == 100 for x in rB[1:] + rB2[1:]) and len(set(x["relief"] for x in rB[1:] + rB2[1:])) == 1
k1 = runlines("fate/kl04.out"); TB = ["| | the referee's two draws | mine |", "|---|---|---|"]
for st in (100000, 300000, 600000):
    TB.append("| rough sand, {:,} steps | {}; {} | {} |".format(st, c3([x for x in rA if x["step"] == st][0]), c3([x for x in rA2 if x["step"] == st][0]), c3(at(k1, st))))
TB.append("| nearly smooth sand, every look to 600,000 steps | 1.0 / 100%% / %.4f (both draws) | 1.0 / 100%% / %.2f (to 2,000,000) |" % (rB[1]["relief"], F["smooth_relief"]))
m6 = at(kk, 600000); TB.append("| banks not crumbling, 600,000 steps on | %s (from its own grown bed) | %s |" % (c3(rC[-1]), c3(m6)))
dsheet = [x["step"] - 600000 for x in rD if x["streams"] == 1.0 and x["wet"] == 100][0]
TB.append("| sand in proportion: one sheet by step | {:,} (from its own bed, looked at every 2,000) | {:,} (looked at every 250) |".format(dsheet, F["fade_one"]))
F["table_blind"] = "\n".join(TB)
c3r = runlines("fate/cs03.out"); c1r = runlines("fate/cs01.out"); assert c3r[-1]["step"] == c1r[-1]["step"] == 2000000
F["cs03_cell"] = cell(c3r, 1600000, 2000000); F["cs01_looks"] = len(c1r); F["cs01_sheet"] = all(x["streams"] == 1.0 and x["wet"] == 100 for x in c1r) and c1r[0]["step"] == 100000
F["fix_m2"] = [F[n + "_m2"] for n in ("kl04", "kl04s2", "kl02", "kl08")]
F["tests"] = open("test.out").read().strip().splitlines()[-1]
pt = open("page-test.out").read(); F["page_same"] = re.search(r"(\d+ of \d+) the same, bit for bit", pt).group(1); F["page_rate"] = int(re.search(r"(\d+) steps a second", pt).group(1)); F["page_errors"] = re.search(r"script errors: (.*)", pt).group(1)
F["quotes"] = open("quotes.out").read().strip().splitlines()[-1]
F["film"] = open("film.out").read().strip()
json.dump(F, open("facts.json", "w"), indent=1); print(len(F), "facts")
