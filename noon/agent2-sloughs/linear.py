"""A test of river.c that could fail: a small sine wave on a straight river must grow and drift at the rates
the linear theory gives.  For y = a exp(i k x + sigma t):  sigma = k^2 (P / (1 + i k) - 1), so the growth rate
is k^2 (P/(1+k^2) - 1) and the wave drifts downstream at k^2 P / (1 + k^2).

The growth rate is the difference of two terms, k^2 P/(1+k^2) and k^2, and the program's error is in each, so
a case agrees if the growth is within half a per cent of the sum of the two terms and the drift within one per cent.
usage: python linear.py"""
import subprocess, sys, numpy as np
bad = 0; n = 0
for ds in ("0.05", "0.1"):
    print("spacing %s" % ds)
    print("   P      k   growth: theory  measured    drift: theory  measured")
    worst_g = worst_c = 0
    for P in (1.5, 3.0, 6.0):
        for m in (2, 5, 8, 12, 20):
            LX = 60.0; k = 2 * np.pi * m / LX
            out = subprocess.run(["./river", str(P), "0.4", str(LX), "1.0", "1", "-sine", repr(k), "2e-3", "-nocut", "-ds", ds, "-snap", "0.25", "/dev/stdout", "-out", "100"],
                                 capture_output=True, text=True).stdout
            amps = []; ts = []
            for line in out.split("\n"):
                f = line.split()
                if len(f) < 10 or line.startswith("#") or len(f) != 2 + 2 * int(f[1]): continue
                t = float(f[0]); xy = np.array(f[2:], float).reshape(-1, 2)
                c = np.sum(xy[:, 1] * np.exp(-1j * k * xy[:, 0])) * 2 / len(xy)     # complex amplitude of the mode
                ts.append(t); amps.append(c)
            ts = np.array(ts); amps = np.array(amps)
            g = np.polyfit(ts, np.log(np.abs(amps)), 1)[0]
            ph = np.unwrap(np.angle(amps)); w = np.polyfit(ts, ph, 1)[0]
            gth = k * k * (P / (1 + k * k) - 1); cth = k * k * P / (1 + k * k); c = -w / k; terms = k * k * (P / (1 + k * k) + 1)
            eg = abs(g - gth) / terms; ec = abs(c - cth) / cth; worst_g = max(worst_g, eg); worst_c = max(worst_c, ec)
            ok = eg < 0.005 and ec < 0.01
            n += 1; bad += not ok
            print("%4.1f %6.3f   %12.4f %9.4f   %12.4f %9.4f   %s" % (P, k, gth, g, cth, c, "ok" if ok else "DIFFERS"))
    print("spacing %s: greatest error in growth %.2f%% of the two terms, in drift %.2f%%" % (ds, 100 * worst_g, 100 * worst_c))
print("%d of %d cases agree with the linear theory" % (n - bad, n))
# a control: could this test fail?  The runs at P = 3 (spacing 0.05) judged against the theory for P = 3.3 and for P = 2.7.
for Pwrong in (3.3, 2.7):
    agree = 0
    for m in (2, 5, 8, 12, 20):
        LX = 60.0; k = 2 * np.pi * m / LX
        out = subprocess.run(["./river", "3.0", "0.4", str(LX), "1.0", "1", "-sine", repr(k), "2e-3", "-nocut", "-ds", "0.05", "-snap", "0.25", "/dev/stdout", "-out", "100"], capture_output=True, text=True).stdout
        amps = []; ts = []
        for line in out.split("\n"):
            f = line.split()
            if len(f) < 10 or line.startswith("#") or len(f) != 2 + 2 * int(f[1]): continue
            xy = np.array(f[2:], float).reshape(-1, 2); ts.append(float(f[0])); amps.append(np.sum(xy[:, 1] * np.exp(-1j * k * xy[:, 0])) * 2 / len(xy))
        ts = np.array(ts); amps = np.array(amps); g = np.polyfit(ts, np.log(np.abs(amps)), 1)[0]; c = -np.polyfit(ts, np.unwrap(np.angle(amps)), 1)[0] / k
        gth = k * k * (Pwrong / (1 + k * k) - 1); cth = k * k * Pwrong / (1 + k * k); terms = k * k * (Pwrong / (1 + k * k) + 1)
        agree += abs(g - gth) / terms < 0.005 and abs(c - cth) / cth < 0.01
    print("control: the five runs at P = 3 judged against the theory for P = %g: %d of 5 agree" % (Pwrong, agree))
sys.exit(1 if bad else 0)
