"""The 8-day runs read window by window, after a reader set this estimate beside the papers (26 November 2026).
usage: python -I windows.py slow_dt8_seed1.txt slow_dt8_seed2.txt > windows.out      (numpy)
Each row of a run file: time in Myr, MEGNO, log10 of the whole variational vector, then log10 of the change it
implies in the eccentricity vector of Mercury, Venus, Earth-Moon, Mars, Jupiter, Saturn, Uranus, Neptune."""
import sys
sys.dont_write_bytecode = True
import numpy as np
NAMES = ['Mercury', 'Venus', 'Earth-Moon', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
LN10 = np.log(10)

def efold(t, y, lo, hi):
    m = (t >= lo) & (t <= hi)
    s = np.polyfit(t[m], y[m], 1)[0]
    return 1 / (s * LN10) if s > 0 else float('inf')

if __name__ == '__main__':
    runs = []
    for f in sys.argv[1:]:
        d = np.array([[float(x) for x in l.split()[:11]] for l in open(f) if not l.startswith('#') and len(l.split()) >= 11])
        t = d[:, 0]; megno = d[:, 1]; whole = d[:, 2]; pl = d[:, 3:11]; inner = pl[:, :4].mean(1); outer = pl[:, 4:].mean(1)
        print(f"{f}: to {t[-1]:.1f} Myr")
        print("  e-folding time of the four inner planets' mean, Myr, by window:")
        print("    " + "; ".join(f"{lo}-{hi}: {efold(t, inner, lo, hi):.1f}" for lo, hi in ((30, 100), (30, 85), (30, 60), (60, 85), (60, 90), (60, 95), (75, 90), (10, 30), (5, 30))))
        print("    in ten-million-year steps from 10 Myr: " + ", ".join(f"{efold(t, inner, lo, lo + 10):.1f}" for lo in range(10, 100, 10)))
        g = lambda y, a, b: 10 ** (np.interp(b, t, y) - np.interp(a, t, y))
        print("  growth from 10 to 30 Myr (linear growth would be 3-fold): " + ", ".join(f"{n} {g(pl[:, i], 10, 30):.1f}-fold" for i, n in enumerate(NAMES[:4])) + f"; the four together {g(inner, 10, 30):.1f}-fold")
        m = (t >= 5) & (t <= 30)
        p = np.polyfit(np.log10(t[m]), inner[m], 1); e = np.polyfit(t[m], inner[m], 1)
        r_p = inner[m] - np.polyval(p, np.log10(t[m])); r_e = inner[m] - np.polyval(e, t[m])
        print(f"  5 to 30 Myr, two fits to the four together: a power of time, exponent {p[0]:.2f}, scatter {r_p.std():.3f} in log10; an exponential, e-folding time {1 / (e[0] * LN10):.1f} Myr, scatter {r_e.std():.3f}")
        print("  outer planets, e-folding time by window: " + "; ".join(f"{lo}-{hi}: " + ", ".join(f"{n} {efold(t, pl[:, 4 + i], lo, hi):.1f}" for i, n in enumerate(NAMES[4:])) for lo, hi in ((30, 100), (30, 60), (60, 100), (80, 100))))
        print("  growth of each outer planet from 30 to 60 Myr and from 60 to 100 Myr, in powers of ten: " + ", ".join(f"{n} {np.interp(60, t, pl[:, 4 + i]) - np.interp(30, t, pl[:, 4 + i]):+.2f} and {np.interp(100, t, pl[:, 4 + i]) - np.interp(60, t, pl[:, 4 + i]):+.2f}" for i, n in enumerate(NAMES[4:])))
        print("  MEGNO at 20, 40, 60, 80, 100 Myr: " + ", ".join(f"{np.interp(x, t, megno):.2f}" for x in (20, 40, 60, 80, 100)) + f"; for steady exponential growth with a 4.2 Myr e-folding time it would be about t/8.4: {60 / 8.4:.1f} at 60 and {100 / 8.4:.1f} at 100")
        # added after a reader's check of the first corrections (26 November)
        avg = lambda y, x, h=2.0: y[(t >= x - h) & (t <= x + h)].mean()
        print(f"  the same growth with each end averaged over two million years either side: {10 ** (avg(inner, 30) - avg(inner, 10)):.1f}-fold; single readings with both ends moved by -2 to +2 Myr: "
              + f"{min(g(inner, 10 + a, 30 + b) for a in (-2, -1, 0, 1, 2) for b in (-2, -1, 0, 1, 2)):.1f} to {max(g(inner, 10 + a, 30 + b) for a in (-2, -1, 0, 1, 2) for b in (-2, -1, 0, 1, 2)):.1f}-fold")
        rows = []
        for lo in (2, 5, 10, 15):
            mm = (t >= lo) & (t <= 30)
            rows.append(f"from {lo}: power {np.polyfit(np.log10(t[mm]), inner[mm], 1)[0]:.1f}, e-fold {1 / (np.polyfit(t[mm], inner[mm], 1)[0] * LN10):.1f}")
        print("  the two fits again, for stretches ending at 30 Myr: " + "; ".join(rows))
        m5 = (t >= 5) & (t <= 30)
        r1 = inner[m5] - np.log10(t[m5]); r1 = r1 - r1.mean()
        print(f"  5 to 30 Myr, a third fit, growth in step with time (the power fixed at 1): scatter {r1.std():.3f} in log10")
        print("  more windows for the four inner planets' mean: " + "; ".join(f"{lo}-{hi}: {efold(t, inner, lo, hi):.1f}" for lo, hi in ((40, 100), (45, 100), (50, 100), (54, 100), (60, 100), (70, 100), (80, 100))))
        print("  ten-million-year steps, labelled: " + ", ".join(f"{lo}-{lo + 10}: {efold(t, inner, lo, lo + 10):.1f}" for lo in range(10, 100, 10)))
        print("  outer planets over 65-100: " + ", ".join(f"{n} {efold(t, pl[:, 4 + i], 65, 100):.1f}" for i, n in enumerate(NAMES[4:]))
              + "; gain from (58 to 62) to (96 to 100), in powers of ten: " + ", ".join(f"{n} {avg(pl[:, i], 98) - avg(pl[:, i], 60):+.1f}" for i, n in enumerate(NAMES)))
        print("  MEGNO at 30, 40, 80 Myr: " + ", ".join(f"{np.interp(x, t, megno):.2f}" for x in (30, 40, 80)) + f"; its slope from 80 to 100 Myr corresponds to an e-folding time of {1 / (2 * np.polyfit(t[t >= 80], megno[t >= 80], 1)[0]):.1f} Myr")
        print("  the whole variational vector, log10, at 10, 30, 60, 100 Myr: " + ", ".join(f"{np.interp(x, t, whole):.2f}" for x in (10, 30, 60, 100)) + f"; growth from 10 to 100 Myr {10 ** (np.interp(100, t, whole) - np.interp(10, t, whole)):.1f}-fold (linear growth: 10-fold)")
        runs.append((t, inner, outer))
    if len(runs) == 2:
        (t1, i1, o1), (t2, i2, o2) = runs
        off_i = i2 - i1; off_o = o2 - o1
        print("the two seeds against each other (second minus first, log10): inner planets, mean over 10-20, 20-30, 30-40, 40-60, 60-100 Myr: "
              + ", ".join(f"{off_i[(t1 >= a) & (t1 < b)].mean():+.2f}" for a, b in ((10, 20), (20, 30), (30, 40), (40, 60), (60, 100)))
              + "; outer planets, mean over 10-20, 20-30, 30-40, 40-60, 60-80, 80-100 Myr: " + ", ".join(f"{off_o[(t1 >= a) & (t1 < b)].mean():+.2f}" for a, b in ((10, 20), (20, 30), (30, 40), (40, 60), (60, 80), (80, 100))))
