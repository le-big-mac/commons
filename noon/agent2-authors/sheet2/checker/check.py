#!/usr/bin/env python
"""Independent check of statements B1..B12 on the SILSO sunspot files.

Usage: python -I check.py <monthly> <smoothed> <yearly>

Everything is done in exact rational arithmetic (fractions.Fraction built
from the printed decimal strings), so comparisons are at full precision.
The data files are only parsed as text.
"""
import json
import math
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))


def fields(line):
    return [f.strip() for f in line.rstrip("\r\n").split(";")]


def num(s):
    """Printed number -> exact Fraction, or None if missing (below zero)."""
    v = Fraction(s)
    if v < 0:
        return None
    return v


def read_monthly(path):
    """Return dict month-index -> value (None if missing), plus row count."""
    out = {}
    rows = 0
    with open(path, "r", encoding="ascii") as fh:
        for line in fh:
            if not line.strip():
                continue
            f = fields(line)
            year, month = int(f[0]), int(f[1])
            n = 12 * year + month
            if n in out:
                raise SystemExit("duplicate month %d-%d in %s" % (year, month, path))
            out[n] = num(f[3])
            rows += 1
    return out, rows


def read_yearly(path):
    out = []
    with open(path, "r", encoding="ascii") as fh:
        for line in fh:
            if not line.strip():
                continue
            f = fields(line)
            year = int(Fraction(f[0]))  # integer part; all positive
            out.append((year, num(f[1])))
    return out


def ym(n):
    """Month index -> (year, month)."""
    y, m = divmod(n - 1, 12)
    return y, m + 1


def lab(n):
    y, m = ym(n)
    return "%04d-%02d" % (y, m)


def fl(x, nd=4):
    return ("%." + str(nd) + "f") % float(x)


def find_minima(S, before_strict=True, after_strict=False):
    mins = []
    for n in sorted(S):
        ok = True
        for j in range(n - 60, n + 61):
            if S.get(j) is None:
                ok = False
                break
        if not ok:
            continue
        v = S[n]
        if before_strict:
            if not all(v < S[j] for j in range(n - 60, n)):
                continue
        else:
            if not all(v <= S[j] for j in range(n - 60, n)):
                continue
        if after_strict:
            if not all(v < S[j] for j in range(n + 1, n + 61)):
                continue
        else:
            if not all(v <= S[j] for j in range(n + 1, n + 61)):
                continue
        mins.append(n)
    return mins


def build_cycles(S, mins):
    cyc = []
    for k in range(len(mins) - 1):
        a, b = mins[k], mins[k + 1]
        cand = [(j, S[j]) for j in range(a + 1, b) if S.get(j) is not None]
        top = max(v for _, v in cand)
        holders = [j for j, v in cand if v == top]
        mx = holders[0]
        cyc.append({
            "k": k + 1, "min": a, "next": b, "max": mx, "peak": top,
            "rise": mx - a, "fall": b - mx, "length": b - a,
            "max_ties": len(holders),
        })
    return cyc


def avg_ranks(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    ranks = [None] * len(vals)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        r = Fraction((i + 1) + (j + 1), 2)
        for t in range(i, j + 1):
            ranks[order[t]] = r
        i = j + 1
    return ranks


def pearson_parts(x, y):
    n = len(x)
    mx = sum(x, Fraction(0)) / n
    my = sum(y, Fraction(0)) / n
    cov = sum(((a - mx) * (b - my) for a, b in zip(x, y)), Fraction(0))
    vx = sum(((a - mx) ** 2 for a in x), Fraction(0))
    vy = sum(((b - my) ** 2 for b in y), Fraction(0))
    return cov, vx, vy


def autocorr_num_den(x, k):
    """Exact numerator and denominator of r(k); missing entries dropped."""
    pres = [v for v in x if v is not None]
    xb = sum(pres, Fraction(0)) / len(pres)
    den = sum(((v - xb) ** 2 for v in pres), Fraction(0))
    numr = Fraction(0)
    for t in range(len(x) - k):
        a, b = x[t], x[t + k]
        if a is None or b is None:
            continue
        numr += (a - xb) * (b - xb)
    return numr, den


def main():
    if len(sys.argv) != 4:
        raise SystemExit("usage: check.py <monthly> <smoothed> <yearly>")
    R, nR = read_monthly(sys.argv[1])
    S, nS = read_monthly(sys.argv[2])
    Yrows = read_yearly(sys.argv[3])

    info = []   # diagnostics to stdout
    lines = {}  # one line per statement
    verdict = {}

    # ---------- file diagnostics ----------
    for name, D in (("monthly", R), ("smoothed", S)):
        ks = sorted(D)
        gaps = [k for k in range(ks[0], ks[-1] + 1) if k not in D]
        miss = [k for k in ks if D[k] is None]
        pres = [k for k in ks if D[k] is not None]
        info.append("%s: rows=%d first=%s last=%s absent-rows=%d missing=%d "
                    "first-present=%s last-present=%s" % (
                        name, len(ks), lab(ks[0]), lab(ks[-1]), len(gaps),
                        len(miss), lab(pres[0]), lab(pres[-1])))
        if miss:
            # are missing values only leading / trailing?
            inner = [k for k in miss if pres[0] < k < pres[-1]]
            info.append("  %s: missing inside the present span: %d" % (name, len(inner)))
    yrs = [y for y, _ in Yrows]
    info.append("yearly: rows=%d first=%d last=%d consecutive=%s missing=%d duplicates=%d" % (
        len(Yrows), yrs[0], yrs[-1],
        all(b - a == 1 for a, b in zip(yrs, yrs[1:])),
        sum(1 for _, v in Yrows if v is None), len(yrs) - len(set(yrs))))

    # ---------- cycles ----------
    mins = find_minima(S)
    cyc = build_cycles(S, mins)
    info.append("cycle minima (%d): %s" % (
        len(mins), ", ".join("%s(%s)" % (lab(n), fl(S[n], 1)) for n in mins)))
    info.append(" k  min      max      next     Peak   Rise Fall Length maxties")
    for c in cyc:
        info.append("%2d  %s  %s  %s  %6s  %4d %4d %5d  %d" % (
            c["k"], lab(c["min"]), lab(c["max"]), lab(c["next"]),
            fl(c["peak"], 1), c["rise"], c["fall"], c["length"], c["max_ties"]))
    peak = {c["k"]: c["peak"] for c in cyc}
    ncyc = len(cyc)

    # sensitivity of the minimum rule to its tie conventions (not literal readings)
    for bs, as_ in ((True, True), (False, False), (False, True)):
        alt = find_minima(S, bs, as_)
        info.append("alt tie rule before_strict=%s after_strict=%s: %d minima, same list=%s" % (
            bs, as_, len(alt), alt == mins))

    # ---------- B1 ----------
    if ncyc:
        mean_len = Fraction(sum(c["length"] for c in cyc), ncyc)
    else:
        mean_len = None
    b1 = (len(mins) == 25 and ncyc == 24 and mean_len is not None
          and Fraction(131) <= mean_len <= Fraction(134))
    verdict["B1"] = b1
    lines["B1"] = ("minima found=%d (first %s, last %s); cycles=%d; mean Length=%s months "
                   "(=%s/%d); need 25 minima and 131<=mean<=134" % (
                       len(mins), lab(mins[0]), lab(mins[-1]), ncyc, fl(mean_len, 4),
                       sum(c["length"] for c in cyc), ncyc))

    # ---------- B2 ----------
    n_rf = sum(1 for c in cyc if c["rise"] < c["fall"])
    n_eq = sum(1 for c in cyc if c["rise"] == c["fall"])
    n_gt = sum(1 for c in cyc if c["rise"] > c["fall"])
    verdict["B2"] = n_rf >= 20
    lines["B2"] = ("Rise<Fall in %d of %d cycles (Rise=Fall in %d, Rise>Fall in %d: cycles %s); "
                   "need >=20" % (
                       n_rf, ncyc, n_eq, n_gt,
                       ",".join(str(c["k"]) for c in cyc if c["rise"] >= c["fall"]) or "none"))

    # ---------- B3 ----------
    presR = [(n, v) for n, v in sorted(R.items()) if v is not None]
    topR = max(v for _, v in presR)
    holdR = [n for n, v in presR if v == topR]
    verdict["B3"] = all(ym(n)[0] in (1957, 1958) for n in holdR)
    second = sorted(set(v for _, v in presR), reverse=True)[1]
    lines["B3"] = "largest monthly R=%s at %s (holders=%d; next distinct value %s at %s); need year 1957 or 1958" % (
        fl(topR, 1), ",".join(lab(n) for n in holdR), len(holdR), fl(second, 1),
        ",".join(lab(n) for n, v in presR if v == second))

    # ---------- B4 ----------
    rise = [Fraction(c["rise"]) for c in cyc]
    pk = [c["peak"] for c in cyc]
    rr, rp = avg_ranks(rise), avg_ranks(pk)
    cov, vx, vy = pearson_parts(rr, rp)
    rho = float(cov) / math.sqrt(float(vx) * float(vy))
    # exact test of rho <= -0.60:  cov<0 and cov^2 >= 0.36*vx*vy
    b4 = (cov < 0) and (cov * cov >= Fraction(36, 100) * vx * vy)
    verdict["B4"] = b4
    ties_rise = len(rise) - len(set(rise))
    ties_peak = len(pk) - len(set(pk))
    # no-tie formula for reference only
    d2 = sum(((a - b) ** 2 for a, b in zip(rr, rp)), Fraction(0))
    rho_simple = 1 - 6 * d2 / (ncyc * (ncyc * ncyc - 1))
    lines["B4"] = ("Spearman(Rise,Peak) over %d cycles=%.6f (Pearson of average ranks; "
                   "tied Rise values: %d surplus, tied Peak values: %d surplus; "
                   "1-6*sum(d^2)/(n(n^2-1)) shortcut would give %.6f); need <=-0.60" % (
                       ncyc, rho, ties_rise, ties_peak, float(rho_simple)))

    # ---------- B5 ----------
    presY = [(y, v) for y, v in Yrows if v is not None]
    srt = sorted(presY, key=lambda t: (-t[1], t[0]))
    top4 = srt[:4]
    distinct = sorted(set(v for _, v in presY), reverse=True)
    # literal: the three highest values are distinct, held uniquely by 1957, 1958, 1778 in that order
    h1 = [y for y, v in presY if v == distinct[0]]
    h2 = [y for y, v in presY if v == distinct[1]]
    h3 = [y for y, v in presY if v == distinct[2]]
    b5 = (h1 == [1957] and h2 == [1958] and h3 == [1778])
    verdict["B5"] = b5
    lines["B5"] = "highest yearly means: %s; need 1957 > 1958 > 1778 as the top three, no ties" % (
        ", ".join("%d=%s" % (y, fl(v, 1)) for y, v in top4))

    # ---------- B6 ----------
    x = [v for _, v in Yrows]
    n10, den = autocorr_num_den(x, 10)
    n11, _ = autocorr_num_den(x, 11)
    verdict["B6"] = n11 > n10
    extra = []
    for k in (9, 12):
        nk, _ = autocorr_num_den(x, k)
        extra.append("r(%d)=%.6f" % (k, float(nk / den)))
    lines["B6"] = "yearly N=%d (%d-%d): r(10)=%.6f, r(11)=%.6f (also %s); need r(11)>r(10)" % (
        len(x), yrs[0], yrs[-1], float(n10 / den), float(n11 / den), ", ".join(extra))
    # sensitivity: series restricted to 1749 onward (not the literal reading)
    x2 = [v for y, v in Yrows if y >= 1749]
    a10, d2_ = autocorr_num_den(x2, 10)
    a11, _ = autocorr_num_den(x2, 11)
    info.append("B6 alt (1749 onward only, N=%d): r(10)=%.6f r(11)=%.6f -> %s" % (
        len(x2), float(a10 / d2_), float(a11 / d2_), a11 > a10))

    # ---------- B7 ----------
    if all(k in peak for k in range(14, 25)):
        rng = list(range(15, 25))
        low = min(peak[k] for k in rng)
        holders = [k for k in rng if peak[k] == low]
        part1 = holders == [24]
        part2 = peak[14] < peak[24]
        b7 = part1 and part2
        lines["B7"] = ("Peaks 15-24: %s; lowest=%s held by cycle(s) %s; Peak(14)=%s vs Peak(24)=%s; "
                       "need cycle 24 sole lowest of 15-24 and Peak(14)<Peak(24)" % (
                           " ".join("%d:%s" % (k, fl(peak[k], 1)) for k in rng), fl(low, 1),
                           ",".join(map(str, holders)), fl(peak[14], 1), fl(peak[24], 1)))
    else:
        b7 = False
        lines["B7"] = "cycles 14-24 not all produced by the rule (cycles=%d): fails" % ncyc
    verdict["B7"] = b7

    # ---------- B8 ----------
    pairs = [(e, e + 1) for e in range(2, 23, 2)]
    if all(a in peak and b in peak for a, b in pairs):
        odd_hi = [(a, b) for a, b in pairs if peak[b] > peak[a]]
        eq = [(a, b) for a, b in pairs if peak[b] == peak[a]]
        even_hi = [(a, b) for a, b in pairs if peak[b] < peak[a]]
        b8 = len(odd_hi) == 8
        lines["B8"] = ("odd cycle has higher Peak in %d of %d pairs (even higher in %s; equal in %d); "
                       "need exactly 8" % (
                           len(odd_hi), len(pairs),
                           ",".join("(%d,%d)" % p for p in even_hi) or "none", len(eq)))
    else:
        b8 = False
        lines["B8"] = "cycles 2-23 not all produced by the rule (cycles=%d): fails" % ncyc
    verdict["B8"] = b8

    # ---------- B9 ----------
    if 5 in peak:
        low = min(peak.values())
        holders = sorted(k for k in peak if peak[k] == low)
        b9 = holders == [5]
        three = sorted(peak.items(), key=lambda t: (t[1], t[0]))[:3]
        lines["B9"] = "lowest Peaks: %s; Peak(5)=%s; lowest held by cycle(s) %s; need cycle 5 sole lowest" % (
            ", ".join("cycle %d=%s (%s)" % (k, fl(v, 1), lab(cyc[k - 1]["max"])) for k, v in three),
            fl(peak[5], 1), ",".join(map(str, holders)))
    else:
        b9 = False
        lines["B9"] = "cycle 5 not produced by the rule: fails"
    verdict["B9"] = b9

    # ---------- B10 ----------
    last = mins[-1]
    openc = [(n, v) for n, v in sorted(S.items()) if n > last and v is not None]
    otop = max(v for _, v in openc)
    ohold = [n for n, v in openc if v == otop]
    b10 = (Fraction(150) <= otop <= Fraction(170)) and all(ym(n)[0] == 2024 for n in ohold)
    verdict["B10"] = b10
    lines["B10"] = ("open cycle %s..%s (%d months after last minimum %s); largest S=%s at %s; "
                    "need 150<=S<=170 and month in 2024" % (
                        lab(openc[0][0]), lab(openc[-1][0]), len(openc), lab(last),
                        fl(otop, 1), ",".join(lab(n) for n in ohold)))

    # ---------- B11 ----------
    late = [v for y, v in Yrows if 1900 <= y <= 2025 and v is not None]
    early = [v for y, v in Yrows if 1749 <= y <= 1899 and v is not None]
    ml = sum(late, Fraction(0)) / len(late)
    me = sum(early, Fraction(0)) / len(early)
    ratio = ml / me
    b11 = ml >= Fraction(115, 100) * me
    verdict["B11"] = b11
    lines["B11"] = ("mean Y 1900-2025=%s (n=%d), mean Y 1749-1899=%s (n=%d), ratio=%s (%+.3f%%); "
                    "need ratio>=1.15" % (
                        fl(ml, 4), len(late), fl(me, 4), len(early), fl(ratio, 6),
                        float((ratio - 1) * 100)))
    # sensitivity: percentage points of the later mean (not the literal reading)
    info.append("B11 alt (early mean at most 85%% of late mean): early/late=%.6f -> %s" % (
        float(me / ml), me <= Fraction(85, 100) * ml))

    # ---------- B12 ----------
    zeros = [n for n, v in sorted(R.items()) if v is not None and v == 0]
    if zeros:
        lz = zeros[-1]
        b12 = ym(lz)[0] == 2009
        lines["B12"] = "months with R=0.0: %d; latest %s (last five: %s); need year 2009" % (
            len(zeros), lab(lz), ",".join(lab(n) for n in zeros[-5:]))
    else:
        b12 = False
        lines["B12"] = "no month with R exactly 0.0: fails"
    verdict["B12"] = b12
    # extra: lowest R after 2009
    post = [(n, v) for n, v in sorted(R.items()) if v is not None and ym(n)[0] >= 2010]
    lowpost = min(v for _, v in post)
    info.append("B12 info: lowest R from 2010 on = %s at %s" % (
        fl(lowpost, 1), ",".join(lab(n) for n, v in post if v == lowpost)))

    # ---------- output ----------
    keys = ["B%d" % i for i in range(1, 13)]
    verdict = {k: bool(verdict[k]) for k in keys}
    with open(os.path.join(HERE, "verdicts.json"), "w", encoding="ascii") as fh:
        json.dump(verdict, fh)
        fh.write("\n")
    with open(os.path.join(HERE, "verdicts.out"), "w", encoding="ascii") as fh:
        for k in keys:
            fh.write("%s: %s -> %s\n" % (k, lines[k], "HELD" if verdict[k] else "FAILED"))
    print("\n".join(info))
    print()
    for k in keys:
        print("%s: %s -> %s" % (k, lines[k], "HELD" if verdict[k] else "FAILED"))


if __name__ == "__main__":
    main()
