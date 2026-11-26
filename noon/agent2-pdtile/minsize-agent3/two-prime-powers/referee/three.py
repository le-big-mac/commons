"""Three primes (S6), by the referee's integer programme and by exhaustion where that is possible.

  upsets M      : every up-set D of Z_M (M with three primes), least multiset with pattern exactly D, beside the corner sum
  top M         : D = {M}: least multiset with pattern exactly {M}, beside min(p1+p2+p3, (p1-1)(p2-1)+p3-1)
  pairs M       : M = pqr: D = {pq, pr, qr, pqr}, beside pq + pr + qr
  exhaust30     : ALL multisets of Z_30 with at most 6 elements and pattern exactly {30} (by writing down every multiset
                  that contains 0 and has at most 6 elements): how many, and are they the rotations of {5,6,12,18,24,25}?
usage: three.py MODE [M] [solver] [tlimit]
"""
import sys, time, json, itertools
from lib import divisors, upsets, corners, pattern, prime_factors, divides
from milp import least, check


def run(M, D, predicted, ub, solver, tl, label):
    dv = [d for d in divisors(M) if d > 1]
    t0 = time.time(); st, sz, v = least(M, list(D), [d for d in dv if d not in set(D)] or [1], ub=ub, solver=solver, tlimit=tl)
    if v: assert pattern(M, v) == sorted(D)
    print(json.dumps(dict(M=M, D=sorted(D), what=label, predicted=predicted, corner_sum=sum(M // c for c in corners(M, D)), status=st, least=sz,
                          agrees=(st == 'optimal' and sz == predicted), multiset=[f'{i}^{w}' if w > 1 else i for i, w in enumerate(v or []) if w], seconds=round(time.time() - t0, 1))), flush=True)


def main():
    mode = sys.argv[1]
    if mode == 'exhaust30':
        M = 30; target = [30]; found = []
        n = 0
        for k in range(1, 7):
            for rest in itertools.combinations_with_replacement(range(M), k - 1):
                A = [0] * M; A[0] += 1
                for x in rest: A[x] += 1
                n += 1
                if divides(M, 30, A) and pattern(M, A) == target: found.append((k, tuple(A)))
        lam = [0] * M
        for x in (5, 6, 12, 18, 24, 25): lam[x] += 1
        rots = {tuple(lam[(i - s) % M] for i in range(M)) for s in range(M)}
        sizes = sorted(set(k for k, _ in found))
        print(json.dumps(dict(M=30, multisets_containing_0_with_at_most_6_elements=n, with_pattern_exactly_30=len(found), their_sizes=sizes,
                              all_are_rotations_of_5_6_12_18_24_25=all(a in rots for _, a in found), rotations_that_contain_0=sum(1 for r in rots if r[0] > 0),
                              distinct_found=len(set(a for _, a in found)))), flush=True)
        return
    M = int(sys.argv[2]); solver = sys.argv[3] if len(sys.argv) > 3 else 'highs'; tl = float(sys.argv[4]) if len(sys.argv) > 4 else 300
    ps = prime_factors(M); assert len(ps) == 3
    p1, p2, p3 = ps
    top = min(p1 + p2 + p3, (p1 - 1) * (p2 - 1) + p3 - 1)
    if mode == 'top':
        run(M, [M], top, p1 + p2 + p3, solver, tl, 'D = {M}')
    elif mode == 'pairs':
        assert M == p1 * p2 * p3
        D = [p1 * p2, p1 * p3, p2 * p3, M]; run(M, D, p1 * p2 + p1 * p3 + p2 * p3, p1 * p2 + p1 * p3 + p2 * p3, solver, tl, 'D = {pq, pr, qr, pqr}')
    elif mode == 'upsets':
        for D in upsets(M):
            cs = sum(M // c for c in corners(M, D))
            run(M, D, top if list(D) == [M] else cs, cs, solver, tl, 'up-set')


if __name__ == '__main__':
    main()
