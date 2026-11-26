"""Tables for the C enumerators, all by exact long division (cyc.py).

For a group Z_M: the divisors d > 1 of M in increasing order (bit i of a pattern mask = i-th divisor), and
for each exponent a in 0..M-1 the remainder of X^a on division by Phi_d.
For a target set P of divisors: G = product of Phi_d over d in P, and the remainder of X^a by G.
"""
import sys
from cyc import cyclotomic, divmod_monic, divisors, mul, phi


def divs(M):
    return [d for d in divisors(M) if d > 1]


def rem_table(M, d):
    c = cyclotomic(d)
    out = []
    for a in range(M):
        _, r = divmod_monic([0] * a + [1], c)
        out.append(r + [0] * (phi(d) - len(r)))
    return out


def write_group_table(M, path):
    ds = divs(M)
    assert sum(phi(d) for d in ds) == M - 1
    with open(path, 'w') as f:
        f.write(f"{M} {len(ds)}\n")
        for d in ds:
            f.write(f"{d} {phi(d)}\n")
            for row in rem_table(M, d):
                f.write(" ".join(map(str, row)) + "\n")


def write_target_table(M, P, path):
    """P: list of divisors.  G = prod Phi_d, D = deg G.  Rows: X^a mod G for a = 0..M-1."""
    G = [1]
    for d in P:
        G = mul(G, cyclotomic(d))
    D = len(G) - 1
    assert D == sum(phi(d) for d in P)
    with open(path, 'w') as f:
        f.write(f"{D}\n")
        for a in range(M):
            _, r = divmod_monic([0] * a + [1], G)
            r = r + [0] * (D - len(r))
            f.write(" ".join(map(str, r)) + "\n" if D else "\n")
    return D


if __name__ == '__main__':
    M = int(sys.argv[1])
    write_group_table(M, sys.argv[2])
