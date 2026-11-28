# Arithmetic of section 18, recomputed.  Reads only records (text files), runs nothing from them.
import re, math
from fractions import Fraction as F
from math import comb, sqrt, pi
E = '/home/agent3/lean/lift-check/even/'
def c(r): return F(comb(r, r // 2), 2 ** r)
print('--- under the table')
for m in (100, 10000): print(m, '1 - 3.12/sqrt(m) =', 1 - 3.12 / sqrt(m))
for m in (101, 10001): print(m, '1 - 2/sqrt(m) =', 1 - 2 / sqrt(m))
print('odd m with 1 - 2/sqrt(m) > 1/2 : least', min(m for m in range(1, 200, 2) if 1 - 2 / sqrt(m) > 0.5),
      ' any exception above?', [m for m in range(17, 400, 2) if not 1 - 2 / sqrt(m) > 0.5])
print('even m>=10 with 1 - 3.12/sqrt(m) > 17/64 : least', min(m for m in range(10, 200, 2) if 1 - 3.12 / sqrt(m) > 17 / 64),
      ' at 18:', 1 - 3.12 / sqrt(18), ' 17/64 =', 17 / 64)
print('--- constants')
print('sqrt13*1129/4096 =', sqrt(13) * 1129 / 4096, '  sqrt15*2095/8192 =', sqrt(15) * 2095 / 8192)
print('sqrt(2/pi) =', sqrt(2 / pi), ' sqrt(2/pi)*(1+2.6251) =', sqrt(2 / pi) * 3.6251)
print('sqrt(pi/2)-1 =', sqrt(pi / 2) - 1)
for a, b in ((78764625, 67108864), (4773, 4096), (19221, 16384), (337, 512)):
    print(f'{a}/{b} = {a / b:.6f}   times sqrt(2/pi) = {a / b * sqrt(2 / pi):.6f}')
print('c_m*sqrt(m) for m = 10, 100, 1000:', [float(c(m)) * sqrt(m) for m in (10, 100, 1000)])
print('2*1.56 =', 2 * 1.56)
print('--- patterns: count by N = G + P - 1, by plain listing (primes up to 23, N <= 21)')
primes = [3, 5, 7, 11, 13, 17, 19, 23]
from itertools import product
cnt = {}
NMAX = 21
def rec(i, chosen):
    if i == len(primes):
        if chosen:
            G = max(1 + (j - 1) * (p - 1) for p, j in chosen); P = max(p for p, j in chosen)
            N = G + P - 1
            if N <= NMAX: cnt[N] = cnt.get(N, 0) + 1
        return
    p = primes[i]
    rec(i + 1, chosen)
    j = 1
    while 1 + (j - 1) * (p - 1) + 2 <= NMAX and p <= NMAX:   # G >= that, P >= 3
        rec(i + 1, chosen + [(p, j)]); j += 1
rec(0, [])
print({N: cnt[N] for N in sorted(cnt)})
# by the formula to N = 61 (as the first text states it), for the sums
def primes_upto(n): return [p for p in range(3, n + 1, 2) if all(p % q for q in range(3, int(p ** .5) + 1, 2))]
def upto(P, g, ps):
    J = lambda q: 1 + (g - 1) // (q - 1)
    r = J(P)
    for q in ps:
        if q < P: r *= 1 + J(q)
    return r
ps = primes_upto(61)
S1 = F(0); Sh = 0.0; cn = {}
for N in range(3, 62, 2):
    tot = 0
    for P in ps:
        g = N - P + 1
        if g < 1: continue
        tot += upto(P, g, ps) - (upto(P, g - 1, ps) if g - 1 >= 1 else 0)
    cn[N] = tot; S1 += F(tot, 2 ** (N - 2)); Sh += tot * sqrt(N) / 2 ** (N - 2)
print('formula counts N=3..21:', [cn[N] for N in range(3, 22, 2)], ' total patterns N<=61:', sum(cn.values()))
print('sum 2^-(N-2), N<=61 =', float(S1), '  sum sqrt(N) 2^-(N-2), N<=61 =', Sh, '  C1 with tail 5.5e-5:', sqrt(2 / pi) * (1 + Sh + 5.5e-5))
print('--- m <= 46: tables of last night against tonight')
b = {}
for ln in open(E + 'quarter/one/table.out', encoding='utf-8'):
    mo = re.match(r'\s*m =\s*(\d+)\s+tbar =.*\sb =\s*(\d+)/(\d+) =', ln)
    if mo: b[int(mo.group(1))] = F(int(mo.group(2)), int(mo.group(3)))
T2 = {}
txt = open(E + 'quarter/two/result.md', encoding='utf-8').read()
i = txt.index('| m | level 0 | Σ_p U_p | COMP | T2(m) |')
for ln in txt[i:].split('\n')[2:17]:
    cells = [x.strip() for x in ln.strip().strip('|').split('|')]
    if cells[0]: T2[int(cells[0])] = F(cells[4])
    for k in (6, 9):
        if cells[k]: T2[int(cells[k])] = F(cells[k + 1])
Psi = {}; 
for ln in open(E + 'root/three/const.out', encoding='utf-8'):
    mo = re.match(r'm =\s*(\d+)\s+Psi = ([0-9.]+)\s+sqrt', ln)
    if mo: Psi[int(mo.group(1))] = float(mo.group(2))
    if 'sqrt(m) Psi_e(m) for even m <= 60' in ln:
        PsiE = {int(a): float(v) for a, v in re.findall(r'(\d+): ([0-9.]+)', ln.split('60:', 1)[1])}
print('b(m) parsed for m =', min(b), '..', max(b), '; T2 for', min(T2), '..', max(T2), '; Psi_e*sqrt(m) for even m up to', max(PsiE))
sharper17 = {9: F(25, 128), 10: F(83, 256), 11: F(105, 512), 12: F(615, 2048)}   # section 17's sentence
def last(m):
    v = [x for x in (b.get(m), T2.get(m), sharper17.get(m)) if x is not None]
    return min(v)
mx = max((float(min(b.get(m, 9), T2[m])) * sqrt(m), m) for m in range(4, 47, 2)); print('largest min(b,T2)*sqrt(m), even m <= 46:', mx)
mxo = max((float(b[m]) * sqrt(m), m) for m in range(3, 26, 2)); print('largest b*sqrt(m), odd m <= 25:', mxo)
mxo2 = max((float(T2[m]) * sqrt(m), m) for m in range(27, 46, 2)); print('largest T2*sqrt(m), odd 27..45:', mxo2)
print('odd m <= 45 where the third text Psi(m) is below last night (tables and the sharper bounds of section 17):',
      [m for m in range(3, 46, 2) if Psi[m] < float(last(m)) - 1e-9])
print('odd m <= 45 where last night is below Psi(m):', [m for m in range(3, 46, 2) if float(last(m)) < Psi[m] - 1e-6])
print('odd m <= 45: last night*sqrt(m) >= 1 anywhere?', [m for m in range(3, 46, 2) if float(last(m)) * sqrt(m) >= 1])
print('even m <= 46 where Psi_e*sqrt(m) is below last night*sqrt(m):', [m for m in range(4, 47, 2) if PsiE[m] < float(last(m)) * sqrt(m) - 1e-4])
for m in (23, 25, 27, 45, 46, 26, 20):
    print(f'  m={m}: last night {float(last(m)):.6f} (x sqrt m {float(last(m)) * sqrt(m):.4f});  Psi {Psi[m]:.6f} (x sqrt m {Psi[m] * sqrt(m):.4f})' + (f'; Psi_e x sqrt m {PsiE[m]:.4f}' if m % 2 == 0 else ''))
print('--- m copies of one element on Z_9, Z_15 (all signings, numerically): bad count against C(m, m/2)')
import cmath
for n, m in ((9, 4), (9, 6), (15, 6), (15, 8), (15, 5)):
    bad = 0
    for s in product((1, -1), repeat=m):
        if any(abs(sum(e * cmath.exp(2j * pi * k * 2 / n) for e in s)) < 1e-9 for k in range(n)): bad += 1
    print(f'  Z_{n}, m = {m} copies of 2: bad {bad}, C(m, m/2) = {comb(m, m // 2) if m % 2 == 0 else 0}')
