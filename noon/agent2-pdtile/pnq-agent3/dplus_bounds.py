"""Referee check (agent2) of the D+ side of pnq-agent3.md: Lemma 1 (U1), (U2) and Lemma 2, tested against EXACT D+
values for EVERY pattern (E, F) of Z_{p^n q}, computed with my own rational simplex (pdflat/lp.py), which shares no
code with the note. The proofs of these lemmas never use that the pattern comes from a set, so they should hold for
all patterns."""
import sys, itertools
sys.path.insert(0,'/home/agent2/pdflat')
from lp import Setup
from fractions import Fraction as Fr
def run(p,n,q):
    M=p**n*q; S=Setup(M); levels=list(range(1,n+1)); tot=0; t1=t2=t3=0; viol=[]; tight=[0,0,0]
    for Es in itertools.chain.from_iterable(itertools.combinations(levels,r) for r in range(n+1)):
        for Fs in itertools.chain.from_iterable(itertools.combinations(range(0,n+1),r) for r in range(n+2)):
            E=set(Es); F=set(Fs); Z=[p**l for l in E]+[p**l*q for l in F]
            if not Z: continue
            D=S.Dplus(Z)[0]; e=len(E); tot+=1
            t1+=1
            if D>p**e*q: viol.append(('U1',Es,Fs,D))
            if D==p**e*q: tight[0]+=1
            if 0 not in F and F<=E:
                t2+=1
                if D>p**e: viol.append(('U2',Es,Fs,D))
                if D==p**e: tight[1]+=1
            if not E<=F:
                a=max(E-F)
                if not any(l>a for l in F-E):
                    t3+=1; bound=Fr(p**e*q,min(p,q))
                    if D>bound: viol.append(('L2',Es,Fs,D))
                    if D==bound: tight[2]+=1
    print(f'M={M}=({p}^{n})*{q}: patterns {tot}; (U1) tested {t1}, attained {tight[0]}; (U2) tested {t2}, attained {tight[1]}; Lemma 2 tested {t3}, attained {tight[2]}; violations {len(viol)}',viol[:3],flush=True)
for p,n,q in [(2,1,3),(2,2,3),(3,2,2),(2,2,5),(2,3,3),(3,2,5),(2,4,3),(3,3,2),(2,3,5),(2,5,3),(3,4,2),(5,2,2),(2,6,3),(3,3,5)]:
    run(p,n,q)
