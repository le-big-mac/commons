# Second look: checks of the changed text and of sentences of my own first report.
import sys, re, math, json
from fractions import Fraction as Fr
import ref_bounds as rb

ONE = sys.argv[1] if __name__ == "__main__" else None      # the author's folder (read as data)
Q1 = sys.argv[2] if __name__ == "__main__" else None       # quarter/one/table.out
Q2 = sys.argv[3] if __name__ == "__main__" else None       # quarter/two/result.md

class ConvCalc(rb.Calc):     # the convention now in section 6: LC and Fb are 0 if N = k + p - 1 > m
    def LC(self, m, N):
        if N > m:
            return Fr(0) if self.exact else 0.0
        return rb.Calc.LC(self, m, N)
    def Fb(self, m, p, k, g):
        if k + p - 1 > m:
            return Fr(0) if self.exact else 0.0
        return rb.Calc.Fb(self, m, p, k, g)

if __name__ == "__main__":
    cnt = rb.cnt_formula(61)
    # 1. counts_61.out, every line
    got = {}
    for line in open(ONE + "/counts_61.out"):
        mm = re.match(r"N =\s*(\d+)\s+cnt =\s*(\d+)", line)
        if mm:
            got[int(mm.group(1))] = int(mm.group(2))
    print("1. counts_61.out: %d lines N = ...; equal to my cnt(N) for every odd N from 3 to 61: %s" % (
        len(got), sorted(got) == list(range(3, 62, 2)) and all(got[N] == cnt[N] for N in got)))
    print("   its first line:", open(ONE + "/counts_61.out").readline().strip())
    # 2. the tables typed into evenconst.py against their sources
    src = open(ONE + "/evenconst.py").read()
    def parse_dict(name):
        body = re.search(name + r" = \{(.*?)\}", src, re.S).group(1)
        d = {}
        for mm in re.finditer(r"(\d+): (Fraction\((\d+), (\d+)\)|[0-9.]+)", body):
            d[int(mm.group(1))] = Fr(int(mm.group(3)), int(mm.group(4))) if mm.group(3) else mm.group(2)
        return d
    T2 = parse_dict("T2"); b1 = parse_dict("b1")
    # source of b: table.out
    bsrc = {}
    for line in open(Q1):
        mm = re.match(r"\s*m =\s*(\d+)\s+tbar =.*b =\s*(\d+)/(\d+) =", line)
        if mm:
            bsrc[int(mm.group(1))] = Fr(int(mm.group(2)), int(mm.group(3)))
    print("2. b(m) typed in evenconst.py: %d entries (m = %d..%d); each equal to table.out: %s" % (
        len(b1), min(b1), max(b1), all(b1[m] == bsrc.get(m) for m in b1)))
    # source of T2: the table of section 5 of the second text
    t2src = {}
    for line in open(Q2):
        if not line.startswith("|"):
            continue
        cells = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(cells) == 11 and cells[0].isdigit():
            t2src[int(cells[0])] = cells[4]
            for a, b in ((6, 7), (9, 10)):
                if cells[a].isdigit():
                    t2src[int(cells[a])] = cells[b]
        elif len(cells) == 11 and cells[0] == "" and cells[6].isdigit():
            for a, b in ((6, 7), (9, 10)):
                if cells[a].isdigit():
                    t2src[int(cells[a])] = cells[b]
    def same(a, b):
        if isinstance(a, Fr):
            return "/" in b and Fr(b) == a
        return a == b
    bad = [m for m in T2 if m not in t2src or not same(T2[m], t2src[m])]
    print("   T2(m) typed in evenconst.py: %d entries (m = %d..%d); source table has %d; differing: %s" % (
        len(T2), min(T2), max(T2), len(t2src), bad))
    # 3. B_E with and without the convention, exact fractions, even m <= 120
    c = rb.c_exact(130)
    A = rb.Calc(c, True); B = ConvCalc(c, True)
    differ = []
    for m in range(2, 121, 2):
        a = sum(rb.BE_parts(A, m, cnt, True)); b = sum(rb.BE_parts(B, m, cnt, True))
        if a != b:
            differ.append((m, float(a - b), math.sqrt(m) * float(a), math.sqrt(m) * float(b)))
    print("3. B_E(m) as first written minus B_E(m) with the convention, exact fractions, even m <= 120: differ at")
    for d in differ:
        print("     m = %3d  difference %.3e   sqrt(m)*B_E: %.6f (as first written)  %.6f (with the convention)" % d)
    print("   largest difference for m >= 20: %.3e" % max([d[1] for d in differ if d[0] >= 20] + [0.0]))
    b28 = sum(rb.BE_parts(B, 28, cnt, True)); a28 = sum(rb.BE_parts(A, 28, cnt, True))
    print("   m = 28: sqrt(28)*B_E = %.6f with the convention, %.6f without; equal as fractions: %s" % (
        math.sqrt(28) * float(b28), math.sqrt(28) * float(a28), a28 == b28))
    # 4. the value at m = 47
    b3 = rb.B3_odd(A, 47, cnt, True)
    sq = 47 * b3 * b3
    print("4. sqrt(47)*B3(47) = %.12f;  47*B3^2 < 0.997875^2 (exact): %s;  0.99787485^2 <= 47*B3^2 < 0.99787495^2 (exact): %s" % (
        math.sqrt(47) * float(b3), sq < Fr(997875, 10 ** 6) ** 2,
        Fr(99787485, 10 ** 8) ** 2 <= sq < Fr(99787495, 10 ** 8) ** 2))
    tab = json.load(open(sys.argv[4]))
    od = {m: tab["B3"][str(m)] for m in range(47, 401, 2)}
    mx = max(od, key=lambda m: od[m]); second = sorted(od.values())[-2]
    print("   largest sqrt(m)*B3(m), odd 47..400 (my floating table): %.7f at m = %d; the next largest %.6f" % (od[mx], mx, second))
    # 5. B(m) > 1/2
    c2 = rb.c_exact(50); A2 = rb.Calc(c2, True)
    above = [m for m in range(1, 41) if rb.B(A2, m, cnt, True) > Fr(1, 2)]
    print("5. m <= 40 with B(m) > 1/2 (exact):", above)
    # 6. the tail
    cf = rb.cnt_formula(401)
    part = sum(Fr(cf[N], 2 ** (N - 2)) for N in range(63, 402, 2))
    x = 0.5783
    beyond = sum(2 * (u + 1) * x ** u for u in range(201, 3000))
    s2 = math.sqrt(2 / math.pi)
    u2 = 31
    first = 2 * math.sqrt(2 * u2 + 1) * (u2 + 1) * x ** u2
    tailprog = first / (1 - x * (1 + 1 / u2) ** 1.5)
    print("6. sum of cnt(N) 2^-(N-2), 63 <= N <= 401: %.3e;  bound of section 4 for the terms N >= 403: sum over u >= 201 of 2(u+1)x^u = %.2e" % (float(part), beyond))
    print("   tail term sqrt(2/(pi m)) * T at m = 3000: %.4e with T = 5.5e-5 (the text's number), %.4e with T = %.4e (the program's)" % (
        s2 / math.sqrt(3000) * 5.5e-5, s2 / math.sqrt(3000) * tailprog, tailprog))
    print("   at m = 401: %.4e (program's T)" % (s2 / math.sqrt(401) * tailprog))
    # 7. the regenerated sup_3000.out against my table, m <= 61 and m > 61 apart
    lo = []; hi = []
    for line in open(ONE + "/sup_3000.out"):
        mm = re.match(r"m =\s*(\d+)\s+B\(m\) = [0-9.]+\s+sqrt\(m\) B\(m\) = ([0-9.]+)", line)
        if mm and mm.group(1) in tab["B"]:
            m = int(mm.group(1)); d = float(mm.group(2)) - tab["B"][mm.group(1)]
            (lo if m <= 61 else hi).append(d)
    print("7. sup_3000.out now: %d values with m <= 61, printed minus mine in [%.2e, %.2e]; %d values with m > 61, printed minus mine in [%.2e, %.2e]" % (
        len(lo), min(lo), max(lo), len(hi), min(hi), max(hi)))
    print("   my tail constant minus the program's, times sqrt(2/pi): %.2e" % (s2 * (5.5e-5 - tailprog)))
    # 8. lead 1's sum
    print("8. sum of sqrt(q) 2^(2-q) over the odd primes: %.6f (first five primes: %.6f)" % (
        sum(math.sqrt(q) * 2.0 ** (2 - q) for q in rb.primes_upto(200)), sum(math.sqrt(q) * 2.0 ** (2 - q) for q in (3, 5, 7, 11, 13))))
    # 9. moduli of my two random streams
    s1 = {15, 45, 63, 75, 105, 135, 225, 315, 81, 243, 405, 525, 675, 945, 1155}
    s2_ = {9, 15, 27, 45, 21, 63, 105, 135, 81, 225, 315}
    print("9. moduli of my random streams: %d in the first, %d in the second, %d in common, %d in all: %s" % (
        len(s1), len(s2_), len(s1 & s2_), len(s1 | s2_), sorted(s1 | s2_)))
    # 10. one comparison of my first report: the other text's bound for one divisor against the two forms of Lemma C
    print("10. classes (10, 10, 10) modulo 3: Lemma C first form c_10*c_10 = %.6f; the other text's c_28/2 = %.6f; gamma form gamma(30,3)/2 = %.6f" % (
        float(c[10] * c[10]), float(c[28] / 2), float(A.gamma(30, 3) / 2)))
