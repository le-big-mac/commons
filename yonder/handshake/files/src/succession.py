import numpy as np, sys, json
from fixation import K, log10_rhoN
SP = [("all-defect","D00"),("echo-once","D10 C00"),("grim","C01 D11"),("tit-for-tat","C01 D01"),("all-cooperate","C00"),("win-stay","C01 D10"),("handshake","D01 D02 C20"),("shifty","D12 D10 C21"),("wooer","C01 D12 D10"),("patience","C01 C12 D23 D24 D10")]
out = {}
for eps, N in ((0.0,100),(0.0,1000),(0.02,100),(0.02,1000),(0.05,100),(0.05,1000)):
    print(f"\nnoise {eps}, population {N}: log10 of (fixation probability of one mutant / neutral). Row = invader, column = resident.")
    print(" " * 14 + "".join(n[:8].rjust(9) for n, _ in SP))
    M_ = np.zeros((len(SP), len(SP)))
    for i, (ni, ki) in enumerate(SP):
        row = []
        for j, (nj, kj) in enumerate(SP):
            if i == j: row.append("    ·    "); continue
            x = log10_rhoN(K(ki), K(kj), eps, N); M_[i, j] = x
            row.append(f"{x:9.1f}" if x > -99 else "    -inf ")
        print(ni[:13].ljust(14) + "".join(row))
    out[f"{eps}_{N}"] = M_.tolist()
json.dump(dict(names=[n for n, _ in SP], m=out), open("succession.json", "w"))
