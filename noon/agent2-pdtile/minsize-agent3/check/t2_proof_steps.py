"""A2. Every intermediate statement of the proof of section 2 (Claim U, the facts (I), (II), (III), the witness, and the
statements made inside each of the four cases), tested on multisets: all multisets up to a size on Z_12 and Z_18,
random structured multisets on larger groups, and the least-size witnesses printed by the tree recursion.
A failure of any 'so' would raise an AssertionError naming the step."""
import sys, random, itertools, glob, re, json, collections
sys.path.insert(0, '/home/agent3/minsize/check')
from pat import *


def child(p, q, n, w, c):
    """the class c mod p of A, read as a multiset on Z_{p^(n-1) q}"""
    M = p ** n * q; M1 = p ** (n - 1) * q; pn1 = p ** (n - 1)
    out = [0] * M1
    for x, wt in enumerate(w):
        if wt and (x % (p ** n)) % p == c:
            u1 = ((x % (p ** n)) - c) // p; layer = x % q
            y = next(t for t in range(u1, M1, pn1) if t % q == layer) if pn1 > 0 else layer
            out[y] += wt
    return out


stats = collections.Counter()


def check(p, q, n, w):
    E, F = tree_pattern(p, q, n, w)
    if 0 in F: return                      # the theorem is about unbalanced A
    size = sum(w); e = len(E)
    G = [a for a in F if a not in E]; k = len(G)
    Em = set(a - 1 for a in E if a >= 2); Fm = set(a - 1 for a in F if a >= 2); Gm = Fm - Em
    assert size >= p ** len(set(E) | set(F)), 'Claim U'
    stats['unbalanced multisets'] += 1
    if n == 0: return
    kids = [child(p, q, n, w, c) for c in range(p)]
    info = []
    for kw in kids:
        s = sum(kw)
        if s == 0: info.append(None); continue
        Ec, Fc = tree_pattern(p, q, n - 1, kw)
        assert Em <= set(Ec) and Fm <= set(Fc), 'E(A^c) contains E-, F(A^c) contains F-'
        xc = len(Gm & set(Ec))
        assert len(Ec) >= len(Em) + xc and len([a for a in Fc if a >= 1 and a not in Ec]) >= len(Gm) - xc, 'counts with x_c'
        bal = 0 in Fc
        if not bal and xc < len(Gm): assert s >= p ** len(Em) * (p ** len(Gm) + q), '(I)'
        if not bal and xc == len(Gm): assert s % p ** (len(Em) + len(Gm)) == 0, '(II)'
        if bal: assert s % (p ** len(Em) * q) == 0, '(III)'
        info.append((s, bal, xc, Ec, Fc))
    # facts (iii): unbalanced A with 1 in F: every child unbalanced
    if 1 in F: assert all(i is not None and not i[1] for i in info), '(iii) at the root'
    if k == 0: return
    stats['with k >= 1'] += 1
    wit = [i for i in info if i is not None and i[2] < len(Gm)]
    if any(g >= 2 for g in G): assert wit, 'a witness exists when G has a level >= 2'
    tots = [0 if i is None else i[0] for i in info]
    if 1 in F and 1 in E:
        stats['case 1 in F, 1 in E'] += 1
        assert len(Gm) == k and e == len(Em) + 1 and len(set(tots)) == 1 and wit
        assert all(not i[1] for i in wit), 'a witness falls under (I)'
    elif 1 in F and 1 not in E:
        stats['case 1 in F, 1 not in E'] += 1
        assert len(Gm) == k - 1 and e == len(Em)
        assert all(t >= p ** (e + k - 1) for t in tots), 'each child has p^(e+k-1) by Claim U'
        assert len(set(tots)) > 1 and all((t - tots[0]) % q == 0 for t in tots) and all(t % p ** e == 0 for t in tots)
        assert max(tots) - min(tots) >= p ** e * q
    elif 1 not in F and 1 in E:
        stats['case 1 not in F, 1 in E'] += 1
        assert len(Gm) == k and e == len(Em) + 1 and len(set(tots)) == 1 and tots[0] > 0 and wit
        s = tots[0]
        unb = [i for i in info if i is not None and not i[1]]
        assert unb, 'some child is unbalanced'
        if any(i[2] < k for i in unb): assert s >= p ** len(Em) * (p ** k + q); stats['   first alternative'] += 1
        else:
            assert all(i[1] for i in wit), 'a witness is then balanced'
            assert s % (p ** (len(Em) + k) * q) == 0; stats['   second alternative'] += 1
    else:
        stats['case 1 not in F, 1 not in E'] += 1
        assert len(Gm) == k and e == len(Em) and wit
        unb = [i for i in info if i is not None and not i[1]]
        assert unb
        if any(i[2] < k for i in unb): stats['   first alternative'] += 1
        else:
            assert all(i[0] >= p ** (e + k) for i in unb), 'an unbalanced child has p^(e+k) by (II)'
            assert all(i[1] and i[0] >= p ** e * q for i in wit), 'a witness is balanced, with p^e q elements'
            assert len(unb) + len(wit) <= p, 'the witness is another child'
            stats['   second alternative'] += 1
    assert size >= p ** e * (p ** k + q), 'Claim G'


def all_multisets(M, smax):
    w = [0] * M
    def rec(pos, left):
        if pos == M - 1:
            for t in range(left + 1):
                w[pos] = t
                if any(w): yield w
            w[pos] = 0; return
        for t in range(left + 1):
            w[pos] = t
            yield from rec(pos + 1, left - t)
        w[pos] = 0
    yield from rec(0, smax)


# 1. exhaustive on the two smallest groups
for (p, q, n, smax) in [(2, 3, 2, 10), (3, 2, 2, 7), (2, 3, 1, 14), (3, 2, 1, 14)]:
    c = 0
    for w in all_multisets(p ** n * q, smax):
        check(p, q, n, w); c += 1
    print(f'Z_{p ** n * q} (p={p}, q={q}): all {c} multisets of size <= {smax}: every step holds', flush=True)

# 2. random structured multisets on larger groups
random.seed(7)
def rnd(p, q, n):
    M = p ** n * q; w = [0] * M
    divs = [d for d in range(2, M + 1) if M % d == 0]
    for _ in range(random.randint(1, 4)):
        r = random.choice(divs); t = random.randrange(M); m = random.randint(1, 2)
        for j in range(r): w[(t + j * (M // r)) % M] += m
    for _ in range(random.randint(0, 3)): w[random.randrange(M)] += 1
    return w
for (p, q, n, reps) in [(2, 3, 3, 6000), (3, 2, 3, 4000), (2, 5, 3, 3000), (2, 3, 4, 3000), (3, 2, 4, 1000), (2, 3, 5, 1000), (5, 2, 3, 400), (3, 5, 3, 400), (2, 7, 3, 1000)]:
    for _ in range(reps): check(p, q, n, rnd(p, q, n))
    print(f'Z_{p ** n * q} (p={p}, q={q}, n={n}): {reps} random sums of cosets and points: every step holds', flush=True)

# 3. the least-size witnesses of the tree recursion (extremal cases), from the files written by dp_run.py runs with witnesses
import subprocess, os
env = dict(os.environ, OMP_NUM_THREADS='1')
for (p, q, n, S) in [(2, 3, 2, 18), (2, 3, 3, 36), (2, 3, 4, 40), (3, 2, 2, 18), (3, 2, 3, 54), (3, 2, 4, 90), (5, 2, 2, 50), (5, 2, 3, 150), (2, 3, 5, 80)]:
    out = subprocess.run(['/home/agent3/minsize/check/dp', str(p), str(q), str(n), str(S), str(S), 'multi', '1'], capture_output=True, text=True, env=env).stdout
    c = 0
    for line in out.splitlines():
        if line.startswith('R 0 ') and ' W' in line:
            w = parse_witness(line.split(' W')[1], p ** n * q); check(p, q, n, w); c += 1
    print(f'Z_{p ** n * q} (p={p}, q={q}, n={n}): {c} least-size witnesses (0 not in F): every step holds', flush=True)
print(dict(stats))
