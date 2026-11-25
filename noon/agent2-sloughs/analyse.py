"""analyse.py -- the long-run numbers of every run in a folder of river.c outputs.

For each run: S-bar, the mean of length/LX over the second half; its standard deviation there; the means of
the third and fourth quarters (has it settled?); the first peak of S(t) (the greatest value before S first
falls 5% below its running greatest), and the greatest value in the first tenth of the run; half-wavelengths between inflection points; the belt.
Then, for each setting, the mean over seeds with the standard error from the seeds.

usage: python analyse.py FOLDER [UPTO] > table
With UPTO, runs that were stopped early are taken as far as that time: the mean is then from half the planned length to UPTO.
"""
import sys, glob, re, os, json
import numpy as np

def read(fn):
    head = open(fn).readline()
    rows = np.array([[float(v) for v in l.split()] for l in open(fn) if l.strip() and not l.startswith("#")])
    par = dict(re.findall(r"(\w+)=([-\w.+]+)", head))
    return par, rows

def one(fn, upto=None):
    par, r = read(fn)
    T = float(par["T"])
    if upto is not None: r = r[r[:, 0] <= upto + 1e-9]
    t, S = r[:, 0], r[:, 2]
    if t[-1] < (T if upto is None else upto) - 1.5: return None
    h = t >= T / 2; q3 = (t >= T / 2) & (t < 3 * T / 4); q4 = t >= 3 * T / 4
    if not q4.any(): q4 = q3
    run = np.maximum.accumulate(S); below = np.nonzero(S < 0.95 * run)[0]
    peak = run[below[0]] if len(below) else run[-1]
    ninf, chords = r[h, 10], r[h, 11]
    L = S[h] * float(par["LX"])
    return dict(file=os.path.basename(fn), P=float(par["P"]), DC=float(par["DC"]), LX=float(par["LX"]), T=T, seed=int(par["seed"]), DS=float(par["DS"]),
                FEED=int(par["FEED"]), F0SQ=float(par["F0SQ"]), SMOOTH=int(par.get("SMOOTH", 0)), AMIN=float(par["AMIN"]),
                Sbar=float(S[h].mean()), sd=float(S[h].std()), q3=float(S[q3].mean()), q4=float(S[q4].mean()), smin=float(S[h].min()), smax=float(S[h].max()),
                peak=float(peak), early_max=float(S[t <= T / 10].max()), cuts_per_time_per_length=float((r[-1, 3] - r[h, 3][0]) / (t[-1] - t[h][0]) / float(par["LX"])),
                half_wave=float((chords / ninf).mean()), half_wave_stream=float((L / ninf).mean()), S_inflection=float((L / chords).mean()),
                meank=float(r[h, 5].mean()), belt=float((r[h, 8] - r[h, 7]).mean()), yrms=float(r[h, 9].mean()))

if __name__ == "__main__":
    folder = sys.argv[1]; upto = float(sys.argv[2]) if len(sys.argv) > 2 else None
    runs = [x for x in (one(f, upto) for f in sorted(glob.glob(folder + "/*.out")) if ".leg" not in f and not os.path.basename(f).startswith("open-") and (os.path.exists(f[:-4] + ".done") or folder.rstrip("/").endswith("fine"))) if x]
    if upto is not None: print("# runs taken up to t = %g: each mean is from half the planned length to that time" % upto)
    json.dump(runs, open(folder + "/runs.json", "w"), indent=0)
    print("# every run: second-half mean of length/LX (S-bar), its sd, third- and fourth-quarter means, first peak")
    print("#    P    dc    LX   ds  fb seed    T     S-bar    sd     q3     q4   peak  half-wave  along  mean|k|   belt")
    for x in runs:
        print("%6.2f %5.2f %5.0f %4.2f %3s %3d %6.0f  %7.3f %5.3f %6.3f %6.3f %6.3f %8.2f %7.2f %7.3f %7.1f" % (
            x["P"], x["DC"], x["LX"], x["DS"], ("%g" % x["F0SQ"]) if x["FEED"] else "-", x["seed"], x["T"], x["Sbar"], x["sd"], x["q3"], x["q4"], x["peak"],
            x["half_wave"], x["half_wave_stream"], x["meank"], x["belt"]))
    print()
    print("# by setting: mean over seeds, standard error from the seeds, and the mean of each run's own sd")
    print("#    P    dc    LX   ds  fb smooth seeds   S-bar    se    sd/S-bar  peak/S-bar  half-wave  along   S-infl  mean|k|  belt  cutoffs/time/length")
    keys = sorted(set((x["P"], x["DC"], x["LX"], x["DS"], x["FEED"], x["F0SQ"], x["SMOOTH"], x["AMIN"] / x["DC"]) for x in runs))
    out = []
    for k in keys:
        g = [x for x in runs if (x["P"], x["DC"], x["LX"], x["DS"], x["FEED"], x["F0SQ"], x["SMOOTH"], x["AMIN"] / x["DC"]) == k]
        m = lambda f: float(np.mean([x[f] for x in g]))
        se = float(np.std([x["Sbar"] for x in g], ddof=1) / np.sqrt(len(g))) if len(g) > 1 else float("nan")
        row = dict(P=k[0], DC=k[1], LX=k[2], DS=k[3], FEED=k[4], F0SQ=k[5], SMOOTH=k[6], AMINoverDC=k[7], seeds=len(g), Sbar=m("Sbar"), se=se, sd_rel=float(np.mean([x["sd"] / x["Sbar"] for x in g])),
                   peak_rel=float(np.mean([x["peak"] for x in g]) / m("Sbar")), early_rel=float(np.mean([x["early_max"] for x in g]) / m("Sbar")), half_wave=m("half_wave"), half_wave_stream=m("half_wave_stream"), S_inflection=m("S_inflection"),
                   meank=m("meank"), belt=m("belt"), cuts=m("cuts_per_time_per_length"), q3=m("q3"), q4=m("q4"), each=[x["Sbar"] for x in g])
        out.append(row)
        print("%6.2f %5.2f %5.0f %4.2f %3s %4d %5d   %7.3f %6.3f %8.3f %10.3f %9.2f %7.2f %7.3f %7.3f %6.1f %8.4f" % (
            row["P"], row["DC"], row["LX"], row["DS"], ("%g" % row["F0SQ"]) if row["FEED"] else "-", row["SMOOTH"], row["seeds"], row["Sbar"], row["se"], row["sd_rel"], row["peak_rel"],
            row["half_wave"], row["half_wave_stream"], row["S_inflection"], row["meank"], row["belt"], row["cuts"]))
    json.dump(out, open(folder + "/settings.json", "w"), indent=0)
