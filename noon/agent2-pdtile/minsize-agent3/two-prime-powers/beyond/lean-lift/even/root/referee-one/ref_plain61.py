# plain depth-first list of every pattern with N(d*) <= 61 (no formula): the table cnt(N) again
import sys
import ref_bounds as rb
Nmax = int(sys.argv[1])
ps = rb.primes_upto(Nmax)
cnt = {}
def rec(i, G, P):
    if P:
        N = G + P - 1
        cnt[N] = cnt.get(N, 0) + 1
    for k in range(i, len(ps)):
        p = ps[k]
        if max(G, 1) + p - 1 > Nmax:
            break
        j = 1
        while True:
            g = max(G, 1 + (j - 1) * (p - 1))
            if g + p - 1 > Nmax:
                break
            rec(k + 1, g, p)
            j += 1
rec(0, 1, 0)
cf = rb.cnt_formula(Nmax)
print("plain list up to N = %d: %d patterns; equal to the formula for every odd N <= %d: %s" % (
    Nmax, sum(cnt.values()), Nmax, all(cnt.get(N, 0) == cf[N] for N in range(3, Nmax + 1, 2))))
print("cnt(57), cnt(59), cnt(61) by the list:", cnt.get(57), cnt.get(59), cnt.get(61))
