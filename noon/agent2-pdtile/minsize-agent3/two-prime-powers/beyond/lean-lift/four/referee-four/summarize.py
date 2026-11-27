# summarize.py -- totals of the outputs in this directory (reads the files, computes nothing new).
import glob, re

print("exh_full.py (every multiset, all signings; A Lemma L on B, B Lemma 1(b), C contraction, D Corollary L, E union bound, F stated bounds)")
tot_ms = tot_sg = 0
totA = totB = totD = attA = attD = 0
allv = {}
minfrac = {}
unfinished = []
for f in sorted(glob.glob("exh_*.out")):
    s = open(f).read()
    head = re.search(r"Z_(\d+), multisets of (\d+)\.\.(\d+) elements, mode (\w+), step (\d+), offset (\d+)", s)
    if not re.search(r"^exit 0", s, re.M) or "violations:" not in s:
        unfinished.append(f)
    n = int(head.group(1))
    ms = 0
    for a in re.finditer(r"m = +(\d+): (\d+) multisets, (\d+) contractible", s):
        m, c = int(a.group(1)), int(a.group(2))
        ms += c
        tot_sg += c << m
    for a in re.finditer(r"A: (\d+) \(d, p\) checks, bound attained (\d+) times; B: (\d+) checks; D: (\d+) \(B_flat, d\) checks, attained (\d+) times", s):
        totA += int(a.group(1)); attA += int(a.group(2)); totB += int(a.group(3)); totD += int(a.group(4)); attD += int(a.group(5))
    for a in re.finditer(r"m = +(\d+): .*\n.*\n +least fraction of good signings: (\S+) = ([0-9.]+) at", s):
        m = int(a.group(1))
        v = float(a.group(3))
        if m not in minfrac or v < minfrac[m][0]:
            minfrac[m] = (v, a.group(2), n)
    v = re.search(r"violations: (\{.*?\})", s)
    if v:
        for k, x in eval(v.group(1)).items():
            allv[k] = allv.get(k, 0) + x
    tot_ms += ms
    print("  %-16s Z_%-4s m %s..%s %-4s step %s offset %s: %7d multisets" % (f, head.group(1), head.group(2), head.group(3), head.group(4), head.group(5), head.group(6), ms))
print("  total: %d multisets, %d signings; A: %d checks (attained %d); B: %d checks; D: %d checks (attained %d)" % (tot_ms, tot_sg, totA, attA, totB, totD, attD))
print("  violations summed:", allv, "; unfinished files:", unfinished)
print("  least fraction of good signings by m:", {m: "%s (Z_%d)" % (minfrac[m][1], minfrac[m][2]) for m in sorted(minfrac)})

print("z9_all.py (every multiset on Z_9 up to affine maps, through the coefficient vectors)")
for f in sorted(glob.glob("z9_*.out"), key=lambda x: (len(x), x)):
    s = open(f).read()
    h = re.search(r"m = (\d+): (\d+) multiplicity vectors with c_0 largest, (\d+) classes .*C\(m\+8,8\) = (\d+) multisets\); step (\d+) offset (\d+)", s)
    dn = re.search(r"classes done: (\d+) of (\d+) \(multisets represented: (\d+)\)(.*)", s)
    if not h or not dn:
        print("  %-12s NOT FINISHED" % f)
        continue
    lf = re.search(r"least fraction of good signings: (\S+) = ([0-9.]+)", s)
    l3 = re.search(r"largest fraction bad at d = 3 .*: (\S+) = ([0-9.]+)", s)
    v = re.search(r"violations: (\{.*?\})", s)
    print("  %-12s m = %s: %s of %s classes (step %s, offset %s), %s of %s multisets%s; least good fraction %s; largest bad at 3: %s; violations %s"
          % (f, h.group(1), dn.group(1), h.group(3), h.group(5), h.group(6), dn.group(3), h.group(4), dn.group(4), lf.group(2), l3.group(2) if l3 else "-", v.group(1) if v else "NOT FINISHED"))

for name, title in (("crand_*.out", "contract_rand.py (random and structured multisets, all signings)"), ("erand_*.out", "even_rand.py (even m, 14..24, all three classes modulo 3 occupied)"),
                    ("attained_*.out", "attained.py (Lemma L attained at one level, even m, 14..24)")):
    print(title)
    for f in sorted(glob.glob(name)):
        s = open(f).read()
        first = s.splitlines()[0] if s else ""
        v = re.search(r"violations: (\{.*?\})", s)
        t = re.search(r"totals: (\{.*?\})", s)
        lg = re.search(r"least good fraction overall: ([0-9.]+)", s)
        print("  %-14s %s" % (f, first[:150]))
        if t:
            print("                 totals %s" % t.group(1))
        print("                 least good fraction %s; violations %s" % (lg.group(1) if lg else "-", v.group(1) if v else "NOT FINISHED"))
print("adversary.py (local search for few good signings)")
best = {}
for f in sorted(glob.glob("adv_*.out")):
    for a in re.finditer(r"Z_(\d+), m = (\d+): least fraction of good signings found (\S+) = ([0-9.]+)", open(f).read()):
        m = int(a.group(2))
        if m not in best or float(a.group(4)) < best[m][0]:
            best[m] = (float(a.group(4)), a.group(3), int(a.group(1)))
print("  least fraction found by m:", {m: "%s = %.4f (Z_%d)" % (best[m][1], best[m][0], best[m][2]) for m in sorted(best)})
