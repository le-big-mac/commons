"""The plain page's new sentences on r = 2, tested by exact arithmetic.
(a) "At every divisor that the doubled clock has and the old clock has not, the two places put the weight at opposite points":
    for every new divisor d of 2N and every hour h, the weights of hours h and h + N at d are opposite  <=>  N = d/2 modulo d.
(b) N odd: "the new divisors of the doubled clock are the divisors of N doubled".
(c) N odd: "the copy balances at such a new divisor [2e] exactly when the marks on the old clock, each putting its weight where its plus or
    minus says, balance at the divisor that was doubled [e]".  Tested for EVERY copy of every small marking, under two ways of naming:
      naming P: plus = the place with the even hour of the doubled clock, minus = the odd hour;
      naming H: plus = hour h, minus = hour h + N   (the order in which the page names the two places).
(d) N even, N = 2^k N': heaps by the remainder modulo 2^k; "if the signed marks of that heap [wound back onto the clock of N' hours] balance at
    no divisor of the odd part, the copy has no new balance, whatever places the other heaps get".  Tested for every copy, under
      naming L: plus = the place whose hour leaves the smaller remainder on division by 2^(k+1)   (the paper's "low" lift);
      naming H: plus = hour h, minus = hour h + N.
usage: bash ~/bin/cap2g.sh ~/welch/.venv/bin/python -I -B u2_plain_page.py"""
import sys; sys.path.insert(0, '/home/agent3/paper/referee-lift/third')
import itertools
import numpy as np
from cyc import divisors, tables
def balanced(elems, signs, n, d):
    """does Phi_d divide sum of sign * X^e ?   (balance at d of the signed marks on the clock of n hours)"""
    t = tables(n)[d]; return not (t[np.array(elems)] * np.array(signs)[:, None]).sum(axis=0).any()
# (a), (b)
okA = okB = True; cntA = 0
for N in range(1, 401):
    new = [d for d in divisors(2 * N) if N % d]
    for d in new: cntA += 1; okA &= (d % 2 == 0 and N % d == d // 2)
    if N % 2: okB &= (new == [2 * e for e in divisors(N)])
print(f'(a) N = 1..400: {cntA} new divisors d of 2N; hours h and h + N land at opposite points at every one: {okA}')
print(f'(b) N odd up to 399: the new divisors of 2N are exactly the doubled divisors of N (2 included): {okB}')
# (c) odd N
print('(c) odd N: every multiset of at most S marks, every copy (each mark at h or at h + N), every divisor e of N')
tot = {'P': [0, 0], 'H': [0, 0]}; exH = None
for N, S in [(1, 6), (3, 6), (5, 5), (7, 4), (9, 5), (15, 4), (21, 3), (25, 3), (27, 3), (45, 3)]:
    c = {'P': [0, 0], 'H': [0, 0]}
    for s in range(1, S + 1):
        for marks in itertools.combinations_with_replacement(range(N), s):
            for up in itertools.product((0, 1), repeat=s):
                copy = [h + N * u for h, u in zip(marks, up)]
                sgP = [1 if y % 2 == 0 else -1 for y in copy]
                sgH = [1 if u == 0 else -1 for u in up]
                for e in divisors(N):
                    b = balanced(copy, [1] * s, 2 * N, 2 * e)
                    for name, sg in (('P', sgP), ('H', sgH)):
                        agree = (balanced(list(marks), sg, N, e) == b); c[name][0] += 1; c[name][1] += agree
                        if name == 'H' and not agree and exH is None: exH = (N, marks, copy, e, b)
    for name in tot: tot[name][0] += c[name][0]; tot[name][1] += c[name][1]
    print(f'    N = {N}, S = {S}: cases {c["P"][0]}; "exactly when" holds with naming P in {c["P"][1]}, with naming H in {c["H"][1]}', flush=True)
print(f'    TOTAL: naming P (plus = even hour): {tot["P"][1]} of {tot["P"][0]}; naming H (plus = hour h): {tot["H"][1]} of {tot["H"][0]}')
print(f'    an example where naming H fails (N, marks, copy, e, copy balances at 2e?): {exH}')
# (d) even N
print('(d) even N = 2^k N\': every multiset of at most S marks, every copy; hypothesis: some heap whose signed marks balance at no divisor of N\'')
totd = {'L': [0, 0, 0], 'H': [0, 0, 0]}; exd = None
for N, S in [(2, 6), (4, 5), (6, 5), (8, 4), (10, 4), (12, 4), (18, 4), (20, 3), (24, 3), (30, 3), (36, 3), (50, 3), (60, 3)]:
    k = 0; N1 = N
    while N1 % 2 == 0: N1 //= 2; k += 1
    new = [d for d in divisors(2 * N) if N % d]; c = {'L': [0, 0, 0], 'H': [0, 0, 0]}
    for s in range(1, S + 1):
        for marks in itertools.combinations_with_replacement(range(N), s):
            for up in itertools.product((0, 1), repeat=s):
                copy = [h + N * u for h, u in zip(marks, up)]
                nonew = not any(balanced(copy, [1] * s, 2 * N, d) for d in new)
                sgs = {'L': [1 if y % 2 ** (k + 1) < 2 ** k else -1 for y in copy], 'H': [1 if u == 0 else -1 for u in up]}
                for name, sg in sgs.items():
                    hyp = False
                    for heap in set(h % 2 ** k for h in marks):
                        idx = [i for i, h in enumerate(marks) if h % 2 ** k == heap]
                        B = [marks[i] % N1 for i in idx]; sB = [sg[i] for i in idx]
                        if not any(balanced(B, sB, N1, e) for e in divisors(N1)): hyp = True; break
                    c[name][0] += 1
                    if hyp:
                        c[name][1] += 1; c[name][2] += nonew
                        if name == 'H' and not nonew and exd is None: exd = (N, marks, copy)
    for name in totd:
        for i in range(3): totd[name][i] += c[name][i]
    print(f'    N = {N} (k = {k}, odd part {N1}), S = {S}: copies {c["L"][0]}; naming L: hypothesis holds {c["L"][1]}, then no new balance {c["L"][2]}; '
          f'naming H: hypothesis holds {c["H"][1]}, then no new balance {c["H"][2]}', flush=True)
print(f'    TOTAL naming L (plus = smaller remainder modulo 2^(k+1)): hypothesis in {totd["L"][1]} copies, conclusion in {totd["L"][2]}')
print(f'    TOTAL naming H (plus = hour h): hypothesis in {totd["H"][1]} copies, conclusion in {totd["H"][2]}; an example where it fails (N, marks, copy): {exd}')
