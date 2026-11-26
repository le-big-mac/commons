"""The statements of proof.md as predicates on (p, q, j, E, F, balanced, size), where a class with j levels below it
has exact pattern (E, F) on its own levels 1..j (E, F subsets of 1..j; 'balanced' says whether its layer vector is
constant) and 'size' is its number of elements (> 0).

Each claim of proof.md is stated there for a REFERENCE pattern contained in the exact pattern.  The sets on the right
shrink when the reference pattern grows, so the strongest instance is the one tested here:
  Lemma 3 (D):  reference = the exact pattern.
  Lemma 4 (W):  reference = the exact pattern, for any g in F minus E.
  Lemma 5 (W'): for each g in F minus E, reference = (E minus {a < g : a in E, a not in F}, F), the largest reference
                pattern that has no level of E-minus-F above g.
"""


def in_sum(x, a, b, tmin, mmin):
    """is x = a*t + b*m with integers t >= tmin, m >= mmin ?"""
    t = tmin
    while a * t <= x:
        r = x - a * t
        if r % b == 0 and r // b >= mmin:
            return True
        t += 1
    return False


def rule_value(p, q, j, E, F):
    """the conjectured least size of a balanced class with exact pattern (E, F) on levels 1..j.  returns (value, x, kprime, a0)"""
    E = set(E); F = set(F)
    e = len(E)
    if all(a in F for a in range(1, j + 1)):
        return q * p ** e, None, None, None
    a0 = min(a for a in range(1, j + 1) if a not in F)
    deeper = sorted(a for a in F if a > a0 and a not in E)
    k1 = len(deeper)
    if k1 == 0:
        x = 0
    elif any(a in E for a in range(1, a0)):
        x = 0
    elif a0 in E and p >= 3:
        x = 0
    elif a0 in E and p == 2 and any(a in E and a not in F for a in range(a0 + 1, deeper[0])):
        x = 0
    else:
        x = 1
    return q * p ** e * (p ** k1 + x), x, k1, a0


def host_x(p, q, j, E, F):
    """Section 7 of proof.md: x by the single 'host level' condition.  Returns x (0 or 1); F must not be all levels."""
    E = set(E); F = set(F)
    a0 = min(a for a in range(1, j + 1) if a not in F)
    deeper = sorted(a for a in F if a > a0 and a not in E)
    if not deeper:
        return 0
    g1 = deeper[0]
    for b in sorted(E):
        if b >= g1:
            break
        if b < a0:
            return 0
        if b == a0 and p >= 3:
            return 0
        if b > a0 and b not in F and a0 in E:
            return 0
    return 1


def thm_unbalanced(p, q, E, F):
    e = len(E)
    k = len([a for a in F if a not in E])
    return p ** e if k == 0 else p ** e * (p ** k + q)


def violations(p, q, j, E, F, balanced, size):
    """list of names of the claims that this (pattern, size) violates"""
    E = set(E); F = set(F)
    bad = []
    e = len(E)
    u = len(E | F)
    if size % p ** e:
        bad.append('p^e does not divide the size')
    if balanced:
        if size % q:
            bad.append('q does not divide a balanced size')
        val, x, k1, a0 = rule_value(p, q, j, E, F)
        if x is None:
            if size < val:
                bad.append('Theorem A (F all levels): size < q p^e')
        else:
            if size < q * p ** (e + k1):
                bad.append('Proposition 6: size < q p^(e+k\')')
            if size < val:
                bad.append('Theorem B lower bound: size < q p^e (p^k\' + x)')
            if x != host_x(p, q, j, E, F):
                bad.append('host-level condition differs from clauses (1)-(4)')
    else:
        if not in_sum(size, p ** u, q, 1, 0):
            bad.append('Lemma 3 (D): size not in p^u N>=1 + q N>=0')
        if size < thm_unbalanced(p, q, E, F):
            bad.append('unbalanced theorem of the note')
        G = sorted(F - E)
        if G:
            if not (in_sum(size, p ** u, q, 1, 1) or size % (q * p ** u) == 0):
                bad.append('Lemma 4 (W): size not in (p^u N>=1 + q N>=1) or q p^u N>=1')
            for g in G:
                Eref = E - {a for a in E if a < g and a not in F}
                uref = len(Eref | F)
                if not in_sum(size, p ** uref, q, 1, 1):
                    bad.append("Lemma 5 (W'): g=%d size not in p^u' N>=1 + q N>=1 (u'=%d)" % (g, uref))
    return bad
