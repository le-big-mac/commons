"""Third method for the four exotic patterns at M=144: HiGHS branch-and-bound (LP-based, unrelated to CP-SAT).
Feasibility of: x in {0,1}^144, x_0 = 1, sum x = 12, (A mod Phi_d) = 0 for d in Z0."""
import numpy as np, time
from scipy.optimize import milp, LinearConstraint, Bounds
from cyc import residues
M=144; n=12
for Z0 in ([2,3,8,36,48,144],[2,3,12,16,48,72],[2,3,16,24,36,48,72],[4,6,8,9,12,18,144]):
    rows=[np.ones(M)]; e0=np.zeros(M); e0[0]=1; rows.append(e0); rhs=[n,1]
    for d in Z0:
        R=np.array(residues(d,M)).T          # phi(d) x M
        for r in R: rows.append(r.astype(float)); rhs.append(0)
    Aeq=np.array(rows); rhs=np.array(rhs,float); t=time.time()
    res=milp(c=np.zeros(M),constraints=LinearConstraint(Aeq,rhs,rhs),integrality=np.ones(M),bounds=Bounds(0,1),options={'time_limit':600})
    print(Z0,'status',res.status,res.message,f'{time.time()-t:.1f}s',flush=True)
# positive control: a pattern that IS realised (zero set of a known tile) must come back feasible
from cyc import zero_set
A=[a+b for a in (0,1,2) for b in (0,36,72,108)]       # {0,1,2} + {0,36,72,108}
Z=zero_set(A,M); rows=[np.ones(M)]; e0=np.zeros(M); e0[0]=1; rows.append(e0); rhs=[len(A),1]
for d in Z:
    for r in np.array(residues(d,M)).T: rows.append(r.astype(float)); rhs.append(0)
res=milp(c=np.zeros(M),constraints=LinearConstraint(np.array(rows),np.array(rhs,float),np.array(rhs,float)),integrality=np.ones(M),bounds=Bounds(0,1))
print('positive control: zero set',Z,'size',len(A),'->',res.status,res.message, sorted(np.nonzero(res.x>.5)[0].tolist()) if res.x is not None else None)
