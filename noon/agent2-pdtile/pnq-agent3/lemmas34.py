"""Referee check (agent2) of Lemma 3 and Lemma 4 of pnq-agent3.md on explicit sets, with zero sets computed by exact
polynomial division (pdflat/cyc.py), i.e. not through the count criteria the note uses."""
import sys, itertools, random
sys.path.insert(0,'/home/agent2/pdflat')
from cyc import zero_set
from multiprocessing import Pool
def check(args):
    p,n,q,masks=args; M=p**n*q; out=[0,0,0,0,[],[]]   # premise3, tight3, premise4, premise4 with a<b in E, viol3, viol4
    for b in masks:
        A=[i for i in range(M) if b>>i&1]; Z=set(zero_set(A,M))
        E={l for l in range(1,n+1) if p**l in Z}; F={l for l in range(0,n+1) if p**l*q in Z}; e=len(E)
        if 0 not in F and any(l>=1 for l in F-E):
            out[0]+=1
            if len(A)<p**e*(p+q): out[4].append(A)
            if len(A)==p**e*(p+q): out[1]+=1
        if 0 in F and len(A)==p**e*q:
            for bb in F-E:
                if bb>=1:
                    out[2]+=1
                    low=[a for a in E if a<bb]
                    if low: out[3]+=1
                    if any(a not in F for a in low): out[5].append((A,bb))
    return out
def run(p,n,q,masks,label):
    chunks=[masks[i::14] for i in range(14)]
    with Pool(14) as pool: res=pool.map(check,[(p,n,q,c) for c in chunks])
    s=[sum(r[k] for r in res) for k in range(4)]; v3=sum(len(r[4]) for r in res); v4=sum(len(r[5]) for r in res)
    print(f'M={p**n*q} ({label}, {len(masks)} sets): Lemma 3 premise met by {s[0]} (bound attained by {s[1]}), violations {v3}; Lemma 4 premise met {s[2]} times ({s[3]} with some a < b in E), violations {v4}',flush=True)
if __name__=='__main__':
    for p,n,q in [(2,2,3),(3,2,2),(2,2,5)]:
        M=p**n*q; run(p,n,q,list(range(1,1<<M,2)),'all sets containing 0')
    random.seed(5)
    for p,n,q in [(2,3,3),(2,2,7),(2,3,5),(3,2,5),(2,4,3),(3,3,2)]:
        M=p**n*q; masks=set()
        while len(masks)<150000:
            k=random.choice([p**a*x for a in range(0,n+1) for x in (1,q,p+q,2*q,q*q)]+list(range(2,M)))
            if 1<=k<=M: masks.add(sum(1<<i for i in [0]+random.sample(range(1,M),min(k,M)-1)))
        # structured sets: unions of cosets of subgroups, shifted
        for _ in range(100000):
            d=random.choice([x for x in range(2,M) if M%x==0]); H=[i for i in range(0,M,d)]
            reps=random.sample(range(d),random.randint(1,min(d,4))); S=set()
            for r in reps:
                sub=random.sample(H,random.randint(1,len(H))) if random.random()<.5 else H
                S|={(h+r)%M for h in sub}
            S.add(0); masks.add(sum(1<<i for i in S))
        run(p,n,q,sorted(masks),'random and coset-built sets containing 0')
