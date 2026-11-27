# The three least-size statements on Z_{p^n q s}: Lean's values against search.
#   Lean's values: A3_rule_eval.out (`#eval` of minU p q Es Fs, q * p ^ Es.card, minB p q Es Fs a0).
#   The sets: transcribed clause by clause from Pnq/LiftAll.lean in `holds` below, as conditions on the set `pat` of all d | M
#   (M = p^n q s) with Phi_d | mask.
#   Search: (1) the census of Z_M (complete for sizes 1..S): the least size of a member, exact when Lean's value V <= S;
#   (2) when V > S: nothing of size <= S may exist; a member of size V is built by lifting a least member on Z_{p^n q} (from the
#   census of that group, when it is complete up to V) through random lifts, and checked by long division; the lower bound
#   then rests on the exhaustive census of Z_{p^n q} up to V and on reduction modulo p^n q keeping the divisors d | p^n q.
# usage: t4_minsize.py [s-values...]
import sys, os, re, json, random
from core import Grp, divisors, pattern_slow

HERE = os.path.dirname(os.path.abspath(__file__))


def load(M):
    p = os.path.join(HERE, 'census', f'M{M}.json')
    return json.load(open(p)) if os.path.exists(p) else None


def parse_lean(path):
    rows = []
    rx = re.compile(r'^([AUB]) (\d+) (\d+) (\d+) \[([0-9, ]*)\](?: \[([0-9, ]*)\])?(?: (\d+))? (\d+)$')
    for line in open(path):
        m = rx.match(line.strip())
        if not m:
            continue
        kind, p, q, n = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
        Es = frozenset(int(x) for x in m.group(5).split(',') if x.strip())
        Fs = frozenset(int(x) for x in m.group(6).split(',') if x.strip()) if m.group(6) is not None else None
        a0 = int(m.group(7)) if m.group(7) is not None else None
        val = int(m.group(8))
        if kind == 'A':
            assert Fs is None and a0 is None
        if kind == 'U':
            assert Fs is not None and a0 is None
        if kind == 'B':
            assert Fs is not None and a0 is not None
        rows.append((kind, p, q, n, Es, Fs, a0, val))
    return rows


def hypotheses(kind, n, Es, Fs, a0):
    """the hypotheses of the Lean statement on (Es, Fs, a0)"""
    lv = set(range(1, n + 1))
    if not Es <= lv:
        return False                                   # hE : Es ⊆ Finset.Icc 1 n
    if kind == 'A':
        return True
    if not Fs <= lv:
        return False                                   # hF
    if kind == 'U':
        return True
    return (1 <= a0 <= n) and all(l in Fs for l in range(1, a0)) and (a0 not in Fs)   # ha1 han hlow hna


def holds(kind, p, q, n, s, Es, Fs, pat):
    """is a NONEMPTY multiset on Z_{p^n q s} whose set of d | p^n q s with Phi_d | mask is `pat` in the set of the statement?"""
    M0 = p ** n * q
    M = M0 * s
    lv = range(1, n + 1)
    cq = q in pat                                                            # Φ_q ∣ maskW w
    cE = all(((p ** l) in pat) == (l in Es) for l in lv)                     # ∀ ℓ ∈ Icc 1 n, Φ_{p^ℓ} ∣ maskW w ↔ ℓ ∈ Es
    if kind == 'A':
        cF = all((p ** l * q) in pat for l in lv)                            # ∀ ℓ ∈ Icc 1 n, Φ_{p^ℓ q} ∣ maskW w
    else:
        cF = all(((p ** l * q) in pat) == (l in Fs) for l in lv)             # ... ↔ ℓ ∈ Fs
    cnew = all(d not in pat for d in divisors(M) if M0 % d != 0)             # ∀ d, d ∣ p^n q s → ¬ d ∣ p^n q → ¬ Φ_d ∣ maskW w
    if kind == 'U':
        return (not cq) and cE and cF and cnew
    return cq and cE and cF and cnew          # 'A' has also 0 < t, true for a nonempty multiset


def least_in_census(c, kind, p, q, n, s, Es, Fs):
    best, ex = None, None
    for pat in c['patterns']:
        if holds(kind, p, q, n, s, Es, Fs, set(pat['divs'])):
            t = pat['sizes'][0]
            if best is None or t < best:
                best, ex = t, pat['example']
    return best, ex


def find_lift(e, M0, s, G, kind, p, q, n, Es, Fs, rng, tries=5000):
    for k in range(tries):
        lifted = [y + M0 * (0 if k == 0 else rng.randrange(s)) for y in e]
        if holds(kind, p, q, n, s, Es, Fs, G.pattern(lifted)):
            # literal re-check: long division, the size, and the reduction
            assert holds(kind, p, q, n, s, Es, Fs, pattern_slow(lifted, M0 * s))
            assert sorted(y % M0 for y in lifted) == sorted(e)
            return lifted, k
    return None, tries


if __name__ == '__main__':
    svals = [int(a) for a in sys.argv[1:]] or [1, 2, 3, 4, 5, 6, 8, 9, 10, 12]
    rows = parse_lean(os.path.join(HERE, 'A3_rule_eval.out'))
    rng = random.Random(26112026)
    params = sorted({(p, q, n) for (_, p, q, n, _, _, _, _) in rows})
    grand = dict(inst=0, exact=0, lifted_base=0, lifted_only=0, open=0, bad=0)
    detail = []
    openlines = []
    openinst = []
    print("columns: p q n s | group | instances (U/A/B) | largest Lean value | census bound S | exact by census | beyond S: member "
          "of Lean's size found by lifting, base group exhaustive up to it | (unused) | beyond both censuses, left to "
          "t5_cpsat.py | DISAGREEMENTS")
    for (p, q, n) in params:
        M0 = p ** n * q
        c0 = load(M0)
        for s in svals:
            M = M0 * s
            c = load(M)
            if c is None or c0 is None:
                continue
            G = Grp(M)
            S, S0 = c['S'], c0['S']
            cnt = dict(U=0, A=0, B=0)
            exact = lb = lo = op = bad = 0
            vmax = 0
            notes = []
            for (kind, p_, q_, n_, Es, Fs, a0, V) in rows:
                if (p_, q_, n_) != (p, q, n) or not hypotheses(kind, n, Es, Fs, a0):
                    continue
                cnt[kind] += 1
                vmax = max(vmax, V)
                name = f"{kind} Es={sorted(Es)}" + ("" if kind == 'A' else f" Fs={sorted(Fs)}") + (f" a0={a0}" if kind == 'B' else "")
                least, ex = least_in_census(c, kind, p, q, n, s, Es, Fs)
                if V <= S:
                    if least == V:
                        exact += 1
                    else:
                        bad += 1
                        notes.append(f"DISAGREE {name}: Lean {V}, search {least}")
                    continue
                if least is not None:
                    bad += 1
                    notes.append(f"DISAGREE {name}: Lean {V}, but a member of size {least} exists: {ex}")
                    continue
                # beyond the census of the big group
                base_least, base_ex = least_in_census(c0, kind, p, q, n, 1, Es, Fs)
                if base_least is not None and base_least != V:
                    bad += 1
                    notes.append(f"DISAGREE ON THE BASE GROUP {name}: Lean {V}, least on Z_{M0} is {base_least}: {base_ex}")
                    continue
                if base_least is None:
                    if V <= S0:
                        bad += 1
                        notes.append(f"DISAGREE ON THE BASE GROUP {name}: Lean {V}, nothing of size <= {S0} on Z_{M0}")
                    else:
                        op += 1
                        notes.append(f"open {name}: Lean {V} > S = {S} and > base bound {S0}")
                        openinst.append(dict(kind=kind, p=p, q=q, n=n, s=s, Es=sorted(Es), Fs=None if Fs is None else sorted(Fs),
                                             a0=a0, V=V))
                    continue
                lifted, k = find_lift(base_ex, M0, s, G, kind, p, q, n, Es, Fs, rng)
                if lifted is None:
                    op += 1
                    notes.append(f"NO LIFT FOUND in 5000 random lifts {name}: base member {base_ex}")
                else:
                    lb += 1
                    detail.append(f"{p} {q} {n} {s} {name}: Lean {V}; member on Z_{M}: {sorted(lifted)} (lift number {k} of {base_ex})")
            ninst = sum(cnt.values())
            grand['inst'] += ninst; grand['exact'] += exact; grand['lifted_base'] += lb; grand['lifted_only'] += lo
            grand['open'] += op; grand['bad'] += bad
            print(f"{p} {q} {n} {s:2d} | Z_{M:<4d}| {ninst:3d} ({cnt['U']}/{cnt['A']}/{cnt['B']}) | {vmax:3d} | S={S:2d} (base Z_{M0}: {S0:2d}) | "
                  f"{exact:3d} | {lb:3d} | {lo:3d} | {op:3d} | {bad}", flush=True)
            for x in notes:
                if x.startswith('open'):
                    openlines.append(f"{p} {q} {n} {s} {x}")
                else:
                    print("      " + x)
    print()
    print("TOTAL", grand)
    with open(os.path.join(HERE, 't4_members.txt'), 'w') as f:
        f.write("\n".join(detail) + "\n")
    with open(os.path.join(HERE, 't4_open.txt'), 'w') as f:
        f.write("\n".join(openlines) + "\n")
    json.dump(openinst, open(os.path.join(HERE, 't4_open.json'), 'w'))
