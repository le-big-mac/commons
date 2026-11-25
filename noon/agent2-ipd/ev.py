import numpy as np, json, glob, sys
EPS=.05; D=.98; PAY={(0,0):3,(0,1):0,(1,0):5,(1,1):1}  # 0=C 1=D
def M(play,ic,idd,start=0): return (np.array(play),np.array(ic),np.array(idd),start)
def score(a,b):
    pa,ca,da,sa=a; pb,cb,db,sb=b; na,nb=len(pa),len(pb); n=na*nb
    P=np.zeros((n,n)); r=np.zeros(n)
    I,J=np.meshgrid(np.arange(na),np.arange(nb),indexing='ij'); I=I.ravel(); J=J.ravel(); idx=np.arange(n)
    for fa in (0,1):
        for fb in (0,1):
            pr=(EPS if fa else 1-EPS)*(EPS if fb else 1-EPS)
            xa=pa[I]^fa; xb=pb[J]^fb
            r+=pr*np.where(xa==0,np.where(xb==0,3,0),np.where(xb==0,5,1))
            ni=np.where(xb==0,ca[I],da[I]); nj=np.where(xa==0,cb[J],db[J])
            np.add.at(P,(idx,ni*nb+nj),pr)
    v=np.linalg.solve(np.eye(n)-D*P,r)
    return (1-D)*v[sa*nb+sb]
def load(fn):
    j=json.load(open(fn)); s=j['states']
    return j['name'],M([x['play']=='D' for x in s],[x['if_C'] for x in s],[x['if_D'] for x in s],j['start'])
HOUSE={'ALLC':M([0],[0],[0]),'ALLD':M([1],[0],[0]),'TFT':M([0,1],[0,0],[1,1]),'GRIM':M([0,1],[0,1],[1,1]),
 'WSLS':M([0,1],[0,1],[1,0]),'TF2T':M([0,0,1],[0,0,0],[1,2,2]),'2TFT':M([0,1,1],[0,2,0],[1,1,1]),
 'STFT':M([1,0],[1,1],[0,0]),'ALT':M([0,1],[1,0],[1,0]),'P1':M([0,1],[0,0],[1,0])}
def pool():
    p=dict(HOUSE)
    for f in glob.glob('/srv/commons/welch/entries/agent1-*.json'):
        n,m=load(f); p[n]=m
    return p
if __name__=='__main__':
    p=pool(); names=list(p)
    S=np.array([[score(p[a],p[b]) for b in names] for a in names])
    for i in np.argsort(-S.mean(1)): print(f'{names[i]:12s} avg {S[i].mean():.3f} self {S[i,i]:.3f}')
