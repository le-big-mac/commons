# t3_minsize.py -- the three least-size statements for SETS against the census of sets.
# Lean's values (minU, q * p^card Es, minB) are read from L4_rule_eval.out (Lean's #eval), never computed here.
# For p != q primes, n, M = p^n q, s > 1, G = M s (with a census of the sets on Z_G up to T_G elements), and each instance
#   U (Es, Fs):      not Phi_q;  Phi_{p^l} <=> l in Es;  Phi_{p^l q} <=> l in Fs   (l = 1..n);  no Phi_d for d | G, d not | M
#   A (Es):          t > 0; Phi_q;  Phi_{p^l} <=> l in Es;  Phi_{p^l q} for every l = 1..n;       no new d
#   B (Es, Fs, a0):  Phi_q;  Phi_{p^l} <=> l in Es;  Phi_{p^l q} <=> l in Fs;                     no new d
#                    (hypotheses: 1 <= a0 <= n, every l < a0 in Fs, a0 not in Fs)
# the statement claims: the least size of a set on Z_G with these properties is Lean's value V, provided V < r^j for an
# odd prime r with r^j | s, i.e. V < Q = the largest odd prime power dividing s.
# The clauses are applied to the pattern (the set of ALL divisors d > 1 of G with Phi_d | mask) of every set in the census.
import json, re, sys
from core import divisors
from t2_compare import load, factor, largest_odd_pp, two_part


def read_rule(fn='L4_rule_eval.out'):
    val = {}
    for line in open(fn):
        line = line.strip()
        m = re.fullmatch(r'A (\d+) (\d+) (\d+) \[([\d, ]*)\] (\d+)', line)
        if m:
            p, q, n = int(m.group(1)), int(m.group(2)), int(m.group(3))
            Es = tuple(int(x) for x in m.group(4).split(',') if x.strip())
            val[('A', p, q, n, Es)] = int(m.group(5))
            continue
        m = re.fullmatch(r'U (\d+) (\d+) (\d+) \[([\d, ]*)\] \[([\d, ]*)\] (\d+)', line)
        if m:
            p, q, n = int(m.group(1)), int(m.group(2)), int(m.group(3))
            Es = tuple(int(x) for x in m.group(4).split(',') if x.strip())
            Fs = tuple(int(x) for x in m.group(5).split(',') if x.strip())
            val[('U', p, q, n, Es, Fs)] = int(m.group(6))
            continue
        m = re.fullmatch(r'B (\d+) (\d+) (\d+) \[([\d, ]*)\] \[([\d, ]*)\] (\d+) (\d+)', line)
        if m:
            p, q, n = int(m.group(1)), int(m.group(2)), int(m.group(3))
            Es = tuple(int(x) for x in m.group(4).split(',') if x.strip())
            Fs = tuple(int(x) for x in m.group(5).split(',') if x.strip())
            val[('B', p, q, n, Es, Fs, int(m.group(6)))] = int(m.group(7))
            continue
    return val


def member(inst, pat, G, M):
    """does a nonempty set with pattern `pat` (divisors > 1 of G) satisfy the clauses of the instance?"""
    kind, p, q, n = inst[0], inst[1], inst[2], inst[3]
    Es = set(inst[4])
    for d in pat:
        if M % d != 0:
            return False                      # a new divisor
    for l in range(1, n + 1):
        if ((p ** l) in pat) != (l in Es):
            return False
    if kind == 'U':
        Fs = set(inst[5])
        if q in pat:
            return False
        for l in range(1, n + 1):
            if ((p ** l * q) in pat) != (l in Fs):
                return False
        return True
    if kind == 'A':
        if q not in pat:
            return False
        for l in range(1, n + 1):
            if (p ** l * q) not in pat:
                return False
        return True
    Fs = set(inst[5])
    if q not in pat:
        return False
    for l in range(1, n + 1):
        if ((p ** l * q) in pat) != (l in Fs):
            return False
    return True


def forms(M):
    """all (p, q, n) with p^n q = M, p != q primes; for M prime: n = 0 and p any other prime (taken from 2, 3, 5)"""
    f = factor(M)
    out = []
    if len(f) == 1 and list(f.values())[0] == 1:
        q = list(f)[0]
        # for n = 0 the prime p does not enter the group or the values (p^0 = 1): one p is enough
        out.append((2 if q != 2 else 3, q, 0))
    elif len(f) == 2:
        (a, ea), (b, eb) = f.items()
        if eb == 1:
            out.append((a, b, ea))
        if ea == 1:
            out.append((b, a, eb))
    return out


if __name__ == '__main__':
    val = read_rule()
    sets = load('set')
    n_claim = n_exact = n_open = n_bad = 0
    n_un = n_un_eq = n_un_ne = n_un_open = 0
    n_below = 0
    two_stat = {}
    openl = []
    unl = []
    lines = []
    for G in sorted(sets):
        TG, L = sets[G]
        for M in divisors(G):
            s = G // M
            if s == 1:
                continue
            Q = largest_odd_pp(s)
            for (p, q, n) in forms(M):
                if ('A', p, q, n, ()) not in val:
                    continue
                insts = [k for k in val if k[1] == p and k[2] == q and k[3] == n]
                for inst in sorted(insts, key=str):
                    if inst[0] == 'B':
                        Fs, a0 = set(inst[5]), inst[6]
                        if not (1 <= a0 <= n and a0 not in Fs and all(l in Fs for l in range(1, a0))):
                            continue
                    V = val[inst]
                    least = None
                    for t in range(1, TG + 1):
                        if any(member(inst, pat, G, M) for pat in L.get(t, {})):
                            least = t
                            break
                    claimed = V < Q
                    if least is not None and least < V:
                        # a set is a multiset: this would contradict the finished theorem for multisets
                        n_below += 1
                        res = 'SET SMALLER THAN V (contradicts the multiset theorem)'
                    elif claimed:
                        n_claim += 1
                        if least is not None:
                            if least == V:
                                n_exact += 1
                                res = 'equal'
                            else:
                                n_bad += 1
                                res = 'DISAGREE'
                        elif V <= TG:
                            n_bad += 1
                            res = 'DISAGREE (no set up to T)'
                        else:
                            n_open += 1
                            res = 'open (V beyond the census; no set of at most %d elements)' % TG
                            openl.append((G, M, s, inst, V))
                    else:
                        n_un += 1
                        if least is not None:
                            if least == V:
                                n_un_eq += 1
                                res = 'not claimed; equal'
                            else:
                                n_un_ne += 1
                                res = 'not claimed; least set size %d differs from V' % least
                                unl.append((G, M, s, inst, V, least))
                        elif V <= TG:
                            n_un_ne += 1
                            res = 'not claimed; no set of at most %d elements, V = %d' % (TG, V)
                            unl.append((G, M, s, inst, V, None))
                        else:
                            n_un_open += 1
                            res = 'not claimed; open'
                    if (not claimed) and V < two_part(s):
                        res += " [V < 2-part of s = %d: the analogue for the prime 2]" % two_part(s)
                        key = "equal" if res.startswith("not claimed; equal") else ("open" if "open" in res else "differs")
                        two_stat[key] = two_stat.get(key, 0) + 1
                    lines.append("G=%d M=%d s=%d Q=%d T=%d %s V=%d least=%s : %s" % (G, M, s, Q, TG, inst, V, least, res))
    for l in lines:
        print(l)
    print()
    print("claimed instances (V < Q): %d; least set size found by the census = V: %d; open (V beyond the census): %d; DISAGREEMENTS: %d"
          % (n_claim, n_exact, n_open, n_bad))
    print("not claimed (V >= Q): %d; least set size = V anyway: %d; differs or no set within the census: %d; open: %d"
          % (n_un, n_un_eq, n_un_ne, n_un_open))
    print("instances with a set smaller than V (must be 0): %d" % n_below)
    print("of the instances not claimed, those with V below the 2-part of s (the analogue for r = 2):", two_stat)
    for u in unl:
        print("  not claimed and different:", u)
    json.dump(dict(open=[(G, M, s, list(map(lambda x: list(x) if isinstance(x, tuple) else x, inst)), V) for (G, M, s, inst, V) in openl]),
              open('t3_open.json', 'w'))
