"""Build the results section from summary.txt (lines tagged [residues] / [counts] / [counts+fd] / [full])."""
import re, sys
rows={}
for l in open('summary.txt'):
    m=re.match(r"M=(\d+) \[([\w+]+)\]: minimal patterns (\{.*?\}); searched (\d+): (\{.*?\}); slowest ([\d.]+)s",l)
    if not m: continue
    rows[(int(m.group(1)),m.group(2))]=(eval(m.group(3)),int(m.group(4)),eval(m.group(5)),float(m.group(6)))
F=('full','counts+fd','counts','residues')
def ok(M,f): return (M,f) in rows and set(rows[(M,f)][2])<={'INFEASIBLE'}
def found(M): return sum(rows[(M,f)][2].get('OPTIMAL',0)+rows[(M,f)][2].get('FEASIBLE',0) for f in F if (M,f) in rows)
allM=sorted({M for M,f in rows}); decided={M for M in allM if any(ok(M,f) for f in F)}
top=1
while top+1 in decided: top+=1
rng=list(range(2,top+1)); ref=lambda M: next(rows[(M,f)] for f in F if (M,f) in rows)
tot=lambda key:sum(ref(M)[0].get(key,0) for M in rng)
nfull=[M for M in rng if ok(M,'full')]; ncounts=[M for M in rng if ok(M,'counts')]; nres=[M for M in rng if ok(M,'residues')]
plain=[M for M in rng if ok(M,'counts') or ok(M,'residues')]
need=[M for M in rng if ref(M)[1]>0]
plainok=lambda M: ok(M,'counts') or ok(M,'residues') or ref(M)[1]==0
t1=1
while t1+1<=top and plainok(t1+1): t1+=1
plain_extra=[M for M in sorted(decided) if M>t1 and (ok(M,'counts') or ok(M,'residues'))]
out=[]
out.append(f"**No search returned a set, at any modulus.** Every M from 2 to {top} is decided, in the two tiers of Claim 1: M ≤ {t1} by encodings that do not use Proposition 3, the rest by the full model only. Violating sets returned by any model on any run: {sum(found(M) for M in allM)}.")
out.append("")
out.append(f"- Minimal patterns over the range: {sum(sum(ref(M)[0].values()) for M in rng)} "
           f"(safe {tot('safe')}, impossible {tot('impossible (k does not divide n)')}, T1-short {tot('T1-short')}, T2-open {tot('T2-open')}). "
           f"Searches needed: {sum(ref(M)[1] for M in rng)}, at {len(need)} of the {len(rng)} moduli; the other {len(rng)-len(need)} moduli (prime powers) have only safe patterns.")
out.append(f"- The full model decided {len(nfull)} of the {len(rng)} moduli up to {top}. The counts model alone, which does not use Proposition 3, "
           f"has decided every modulus up to {t1}"+(f" and also {', '.join(map(str,plain_extra))}" if plain_extra else "")+
           f" (some patterns needed five solver threads and up to 20 minutes); the residues model alone was run to about M = 110, plus M = 144, and decided {len(nres)}. "
           f"TIER1={t1}")
full_only_extra=[M for M in sorted(decided) if M>top and not (ok(M,'counts') or ok(M,'residues'))]
plain_far=[M for M in sorted(decided) if M>top and (ok(M,'counts') or ok(M,'residues'))]
print(f"TIERINFO {t1} {top} | {','.join(map(str,plain_far))} | {','.join(map(str,full_only_extra))}")
out.append("")
out.append("Moduli with T2-open minimal patterns:")
out.append("")
out.append("| M | minimal patterns | safe | impossible | T1-short | T2-open | searches | decided by |")
out.append("|---|---|---|---|---|---|---|---|")
for M in rng:
    p,ns,st,t=ref(M)
    if p.get('T2-open',0):
        out.append(f"| {M} | {sum(p.values())} | {p.get('safe',0)} | {p.get('impossible (k does not divide n)',0)} | {p.get('T1-short',0)} | {p.get('T2-open',0)} | {ns} | {', '.join(f for f in F if ok(M,f) and f!='counts+fd')} |")
extra=[M for M in sorted(decided) if M>top]
if extra:
    out.append("")
    out.append("Further moduli decided beyond the contiguous range (full model):")
    out.append("")
    out.append("| M | factorisation | minimal patterns | safe | impossible | T1-short | T2-open | searches |")
    out.append("|---|---|---|---|---|---|---|---|")
    def fac(n):
        f=[];p=2
        while p*p<=n:
            e=0
            while n%p==0: n//=p; e+=1
            if e: f.append(f"{p}^{e}" if e>1 else str(p))
            p+=1
        if n>1: f.append(str(n))
        return '·'.join(f)
    for M in extra:
        p,ns,st,t=ref(M)
        out.append(f"| {M} | {fac(M)} | {sum(p.values())} | {p.get('safe',0)} | {p.get('impossible (k does not divide n)',0)} | {p.get('T1-short',0)} | {p.get('T2-open',0)} | {ns} |")
print('\n'.join(out))
