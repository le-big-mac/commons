"""More adding-up of steps (no rule used in the adding):
 (a) odd m 3001..12001, numerator 1: floating cycle sum against rule A and rule B;
 (b) the Wieferich cases 1093^2, 1093^3, 9*1093, 9*1093^2, 3511^2, 3511^3;
 (c) a heading that is not a rational turn, built by feedback from the three cycles
     0 (sum 1), 1/7 (sum alpha), 3/7 (sum alpha-bar), with coin tosses when near home.

Output: brute2.out
"""
import math, sys, random
import numpy as np
sys.path.insert(0, '/home/agent2/gospel/referee')
import brute, rule


def big_cycle_sum(q):
    """cycle sum for 1/q, odd q, by numpy in chunks; orbit by Python ints."""
    a = 1
    sx = []
    sy = []
    chunk = []
    n = 0
    while True:
        chunk.append(a / q)
        n += 1
        a = (2 * a) % q
        if len(chunk) == 200000 or a == 1:
            t = 2 * math.pi * np.array(chunk)
            sx.append(math.fsum(np.cos(t).tolist()))
            sy.append(math.fsum(np.sin(t).tolist()))
            chunk = []
        if a == 1:
            break
    return n, math.hypot(math.fsum(sx), math.fsum(sy))


def feedback_bits(nbits, seed):
    words = {'0': 1 + 0j, '001': complex(-0.5, math.sqrt(7) / 2), '011': complex(-0.5, -math.sqrt(7) / 2)}
    rnd = random.Random(seed)
    bits = []
    F = 0j          # sum of the steps whose next 60 bits are all fixed
    done = 0        # number of such steps
    LOOK = 60
    wts = 0.5 ** np.arange(1, LOOK + 1)
    reps = 4
    coins = 0
    while len(bits) < nbits:
        L = len(bits)
        # finalise
        while done + LOOK <= L:
            fr = float(np.dot(bits[done:done + LOOK], wts))
            F += complex(math.cos(2 * math.pi * fr), math.sin(2 * math.pi * fr))
            done += 1
        # estimate of the place, pending steps padded with noughts
        P = F
        for k in range(done, L):
            seg = bits[k:k + LOOK]
            fr = float(np.dot(seg, wts[:len(seg)]))
            P += complex(math.cos(2 * math.pi * fr), math.sin(2 * math.pi * fr))
        if abs(P) < 3:
            w = rnd.choice(sorted(words))
            coins += 1
        else:
            w = min(sorted(words), key=lambda u: abs(P + reps * words[u]))
        bits.extend([int(c) for c in w] * reps)
    return bits, coins


def true_walk(bits):
    LOOK = 60
    wts = 0.5 ** np.arange(1, LOOK + 1)
    b = np.array(bits, dtype=np.float64)
    win = np.lib.stride_tricks.sliding_window_view(b, LOOK)
    fr = win @ wts
    z = np.exp(2j * math.pi * fr)
    P = np.cumsum(z)
    return len(P), float(np.abs(P).max()), float(np.abs(P[-1]))


if __name__ == '__main__':
    out = open('/home/agent2/gospel/referee/brute2.out', 'w')
    N = 12001
    spf = rule.sieve_spf(N + 1)
    rule_B, d, w = rule.make_rule_B(N + 1, spf)
    badA = badB = nb = 0
    smallest = 9e9
    largest0 = 0.0
    for m in range(3001, N + 1, 2):
        s = brute.cycle_sum(1, m)[2]
        b = s < brute.TOL
        nb += b
        if b:
            largest0 = max(largest0, s)
        else:
            smallest = min(smallest, s)
        badA += (b != rule.rule_A(m, spf))
        badB += (b != rule_B(m))
    print('(a) odd m 3001..%d: bounded %d; disagree with rule A: %d, with rule B: %d; '
          'largest nought %.2e, smallest not nought %.5f' % (N, nb, badA, badB, largest0, smallest), file=out)
    for name, q in (('1093^2', 1093 ** 2), ('1093^3', 1093 ** 3), ('9*1093', 9 * 1093), ('9*1093^2', 9 * 1093 ** 2),
                    ('3511^2', 3511 ** 2), ('3511^3', 3511 ** 3), ('3*1093^2', 3 * 1093 ** 2)):
        n, s = big_cycle_sum(q)
        print('(b) q=%-9s = %d  cycle length %d  |cycle sum| = %.3e' % (name, q, n, s), file=out)
    out.flush()
    for seed in (1, 2, 3):
        bits, coins = feedback_bits(150000, seed)
        n, far, last = true_walk(bits)
        print('(c) seed %d: %d steps walked from the bit string, farthest from start %.3f, at the end %.3f, coin tosses %d'
              % (seed, n, far, last, coins), file=out)
    out.close()
    print(open('/home/agent2/gospel/referee/brute2.out').read())
