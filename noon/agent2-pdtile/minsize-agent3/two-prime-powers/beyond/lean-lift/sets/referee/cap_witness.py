"""For each pattern of the ten groups Z_{p^n q} of the paper's Section 1.3: a least multiset (m elements, exactly the
pattern) with every multiplicity <= 3 (p = 2) or <= 2 (p odd), found by my CP-SAT model (sets_cpsat.solve), checked by
exact division, written to cap-witnesses.jsonl.  Then each is lifted along r = 3 and along r = 5 by the recipe of the
proof of Proposition 20 (prop_test.one_step, j = 1) to Z_{p^n q r}; checked: a set, m elements, reduces to the
multiset, pattern among the divisors of p^n q r exactly the pattern.
usage: cap_witness.py TLIM"""
import sys, json, random, collections
from sets_cpsat import solve
from thm import theorem_m, D_of, all_patterns
from cyc import pattern
from prop_test import check
tlim = float(sys.argv[1]); rnd = random.Random(5)
out = open('cap-witnesses.jsonl', 'w')
gt = gf = 0; lift_ok = collections.Counter(); lift_tot = collections.Counter()
for (p, q, n) in [(2, 3, 2), (3, 2, 2), (2, 5, 2), (3, 5, 2), (5, 2, 2), (5, 3, 2), (2, 3, 3), (3, 2, 3), (2, 5, 3), (2, 3, 4)]:
    cap = 3 if p == 2 else 2
    M = p ** n * q; found = 0; tot = 0; dist = collections.Counter()
    for E, F, bal in all_patterns(p, q, n):
        m = theorem_m(p, q, n, E, F, bal); D = D_of(p, q, n, E, F, bal); tot += 1
        st, mult = solve(M, D, cap, size=m, tlim=tlim)
        if mult is None:
            print('  not found:', p, q, n, E, F, bal, m, st); continue
        assert pattern(mult, M) == D and sum(mult.values()) == m and max(mult.values()) <= cap
        found += 1; dist[max(mult.values())] += 1
        out.write(json.dumps({'p': p, 'q': q, 'n': n, 'E': E, 'F': F, 'balanced': bal, 'm': m, 'cap': cap,
                              'multiset': {str(x): w for x, w in sorted(mult.items())}}) + '\n')
        for r in (3, 5):
            ok, cases, _ = check(mult, M, r, 1, rnd)
            lift_tot[r] += 1; lift_ok[r] += ok
    gt += tot; gf += found
    print(f'Z_{M} (p={p}, q={q}, n={n}): {tot} patterns; least multiset with multiplicities <= {cap} found and checked: {found}; '
          f'largest multiplicity in the multisets found: {dict(sorted(dist.items()))}', flush=True)
out.close()
print(f'all ten groups: {gt} patterns; found: {gf}')
for r in (3, 5):
    print(f'lifted along {r} by the recipe of the proof to a set on Z_(p^n q {r}) with m elements and exactly the pattern: {lift_ok[r]} of {lift_tot[r]}')
