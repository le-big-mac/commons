# The supports quoted in section 5 of even-result-2.md, with their live dangerous e and ranks D_e (exact, F_2).
import sys
from fractions import Fraction as Fr
sys.path.insert(0, '/home/agent3/lean/lift-check/even/prover2')
from ranks import factor, powrem2, rank2, live_levels, crt
from lib2 import divisors

def show(name, n1, W, W2):
    f = factor(n1)
    live = {q: live_levels(W, q, b) for q, b in f.items()}
    print(name, "n' =", n1, 'W =', sorted(W), 'W2 =', sorted(W2), 'live levels', live)
    tot = Fr(0)
    for e in divisors(n1):
        if e == 1: continue
        pr = powrem2(e); s = 0
        for w in W2: s ^= pr[w % e]
        fe = factor(e)
        lv = all(i in live[q] for q, i in fe.items())
        D = rank2([pr[w % e] for w in set(x % e for x in W)])
        if lv:
            mu = max((live[q].index(i) + 1) * (q - 1) for q, i in fe.items())
            print('   e =', e, 'live', 'dangerous' if s == 0 else 'not dangerous', 'D_e =', D, 'mu(e*) =', mu)
            if s == 0: tot += Fr(2, 2 ** D)
    print('   sum over the live dangerous e of 2^(1-D_e) =', tot, '= %.5f' % float(tot))

# (1) Z_45 = Z_9 x Z_5: coset of H_3 in one class modulo 5, plus four points; 45 dangerous, 5 and 15 not
W2 = [crt([c, 0], [9, 5]) for c in (0, 3, 6)]
W = W2 + [crt([1, 1], [9, 5]), crt([2, 2], [9, 5]), crt([1, 3], [9, 5]), crt([2, 4], [9, 5])]
show('(1)', 45, W, W2)
# (2) Z_105: coset of H_3 at residue (0,0) modulo (5,7), plus six points on a diagonal of Z_5 x Z_7
W2 = [crt([c, 0, 0], [3, 5, 7]) for c in range(3)]
W = W2 + [crt([j % 3, min(j, 4), j], [3, 5, 7]) for j in range(1, 7)]
show('(2)', 105, W, W2)
# (3) Z_225 = Z_9 x Z_25: coset of H_5 in the class 0 modulo 9, plus four points that make the levels 1 of 5 and 1, 2 of 3 live at once
W2 = [crt([0, 5 * s], [9, 25]) for s in range(5)]
W = W2 + [crt([1, 1], [9, 25]), crt([2, 2], [9, 25]), crt([3, 3], [9, 25]), crt([6, 4], [9, 25])]
show('(3)', 225, W, W2)
# (4) Z_225: three cosets of H_5 in the three classes modulo 3, in different groups of the 5-tree: D_75 = D_25
W2 = sorted((x + 45 * t) % 225 for x in (4, 8, 12) for t in range(5))
show('(4)', 225, W2, W2)
# (5) Z_15: the cross (a full class modulo 3 and one more point in each other class, same residue modulo 5)
W2 = [crt([0, s], [3, 5]) for s in range(5)]
W = W2 + [crt([1, 0], [3, 5]), crt([2, 0], [3, 5])]
show('(5)', 15, W, W2)
