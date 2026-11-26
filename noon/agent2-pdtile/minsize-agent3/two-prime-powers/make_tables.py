"""Tables of the least sizes found, one row for each pattern, and counts for the note.
usage: make_tables.py M P Q OUT.md FILES...     (M = P^2 Q^2; later files override earlier ones when they decide a pattern)"""
import sys, json
M, P, Q, outp = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
R = {}
for f in sys.argv[5:]:
    for l in open(f):
        if l.startswith('{'):
            r = json.loads(l); k = frozenset(r['D'])
            if k not in R or (r['proved'] and not R[k]['proved']) or (R[k]['min'] is None and r['min'] is not None): R[k] = r
divs = [d for d in range(1, M + 1) if M % d == 0]
def is_up(D): return all((e in D) for d in D for e in divs if e % d == 0)
def corners(D):
    comp = [c for c in divs if c not in D]; return [c for c in comp if not any(e != c and e % c == 0 for e in comp)]
def largest_up_inside(D): return frozenset(d for d in D if all((e in D) for e in divs if e % d == 0))
rows = []
for D in sorted(R, key=lambda D: (len(D), sorted(D))):
    r = R[D]; up = is_up(D); U = largest_up_inside(D); lb = sum(M // c for c in corners(U))
    rows.append((sorted(D), r['min'], r['proved'], up, lb))
with open(outp, 'w') as f:
    f.write(f"# Z_{M} = {P}²·{Q}²: the least size found for each of the {len(rows)} patterns\n\n"
            "*Made by `make_tables.py` from the solver's output files. 'least' is the size of the smallest multiset the solver found with exactly that pattern; "
            "'proved' says whether the solver also proved that nothing smaller exists within its time limit. 'up-set' marks the patterns closed under multiples. "
            "'bound' is the lower bound of Corollary P (the sum of M/c over the corners of the largest up-set inside the pattern), which for an up-set is the value of Corollary U.*\n\n"
            "| pattern (the d with Φ_d dividing) | least | proved | up-set | bound |\n|---|---|---|---|---|\n")
    for D, m, pr, up, lb in rows:
        f.write(f"| {', '.join(map(str, D)) if D else '(none)'} | {m if m is not None else 'none found'} | {'yes' if pr else 'no'} | {'yes' if up else ''} | {lb} |\n")
dec = [r for r in rows if r[1] is not None and r[2]]
ups = [r for r in rows if r[3]]; upd = [r for r in ups if r[1] is not None and r[2]]
print(json.dumps(dict(M=M, patterns=len(rows), decided=len(dec), found=sum(1 for r in rows if r[1] is not None), upsets=len(ups), upsets_decided=len(upd),
                      upsets_equal=sum(1 for r in upd if r[1] == r[4]), below_bound=sum(1 for r in dec if r[1] < r[4]), equal_bound_not_up=sum(1 for r in dec if not r[3] and r[1] == r[4]),
                      distinct=len(set(r[1] for r in dec)), largest=max(r[1] for r in dec))))
