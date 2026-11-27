# The conditions of the three theorems of Pnq/LiftMin.lean, transcribed from the Lean text by the auditor.
# D is the set of ALL d | p^n q r such that Phi_d divides the mask of w; s is the number of elements of w.
import re
from core import divisors

def no_new(D, p, q, n, r):
    #  ∀ d, d ∣ p ^ n * q * r → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w
    N = p ** n * q; M = N * r
    return all(not (d in D) for d in divisors(M) if N % d != 0)
def clause_E(D, p, n, Es):
    #  ∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ Es
    return all(((p ** l in D) == (l in Es)) for l in range(1, n + 1))
def clause_F(D, p, q, n, Fs):
    #  ∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w ↔ ℓ ∈ Fs
    return all(((p ** l * q in D) == (l in Fs)) for l in range(1, n + 1))
def clause_F_all(D, p, q, n):
    #  ∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w
    return all((p ** l * q in D) for l in range(1, n + 1))

def member_U(D, s, p, q, n, r, Es, Fs):      # minsize_unbalanced_lift
    return (not (q in D)) and clause_E(D, p, n, Es) and clause_F(D, p, q, n, Fs) and no_new(D, p, q, n, r)
def member_A(D, s, p, q, n, r, Es):          # minsize_balanced_all_lift
    return (0 < s) and (q in D) and clause_E(D, p, n, Es) and clause_F_all(D, p, q, n) and no_new(D, p, q, n, r)
def member_B(D, s, p, q, n, r, Es, Fs):      # minsize_balanced_lift
    return (q in D) and clause_E(D, p, n, Es) and clause_F(D, p, q, n, Fs) and no_new(D, p, q, n, r)
def hyp_B(n, Fs, a0):
    #  (ha1 : 1 ≤ a0) (han : a0 ≤ n) (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) (hna : a0 ∉ Fs)
    return 1 <= a0 <= n and all(l in Fs for l in range(1, a0)) and a0 not in Fs

def lean_values(path="/home/agent3/lean/lift-audit/A7_rule_eval.out"):
    """the values printed by Lean's #eval: {('U',p,q,n,Es,Fs): minU, ('A',p,q,n,Es): q*p^|Es|, ('B',p,q,n,Es,Fs,a0): minB}"""
    val = {}
    def lst(t): return frozenset(int(x) for x in t.split(",") if x.strip())
    for line in open(path):
        m = re.match(r"U (\d+) (\d+) (\d+) \[(.*?)\] \[(.*?)\] (\d+)$", line)
        if m: val[("U", int(m[1]), int(m[2]), int(m[3]), lst(m[4]), lst(m[5]))] = int(m[6]); continue
        m = re.match(r"A (\d+) (\d+) (\d+) \[(.*?)\] (\d+)$", line)
        if m: val[("A", int(m[1]), int(m[2]), int(m[3]), lst(m[4]))] = int(m[5]); continue
        m = re.match(r"B (\d+) (\d+) (\d+) \[(.*?)\] \[(.*?)\] (\d+) (\d+)$", line)
        if m: val[("B", int(m[1]), int(m[2]), int(m[3]), lst(m[4]), lst(m[5]), int(m[6]))] = int(m[7]); continue
        raise ValueError(line)
    return val

def instances(p, q, n, r, val):
    """every instance of the three theorems for these p, q, n, r: (label, membership test, value given by Lean)"""
    import itertools
    assert p != q and r != 2
    lv = list(range(1, n + 1))
    subs = [frozenset(c) for k in range(n + 1) for c in itertools.combinations(lv, k)]
    out = []
    for Es in subs:                                   # hE : Es ⊆ Icc 1 n
        out.append((("A", tuple(sorted(Es))), (lambda D, s, Es=Es: member_A(D, s, p, q, n, r, Es)), val[("A", p, q, n, Es)]))
        for Fs in subs:                               # hF : Fs ⊆ Icc 1 n
            out.append((("U", tuple(sorted(Es)), tuple(sorted(Fs))), (lambda D, s, Es=Es, Fs=Fs: member_U(D, s, p, q, n, r, Es, Fs)),
                        val[("U", p, q, n, Es, Fs)]))
            for a0 in range(0, n + 3):
                if hyp_B(n, Fs, a0):
                    out.append((("B", tuple(sorted(Es)), tuple(sorted(Fs)), a0), (lambda D, s, Es=Es, Fs=Fs: member_B(D, s, p, q, n, r, Es, Fs)),
                                val[("B", p, q, n, Es, Fs, a0)]))
    return out
