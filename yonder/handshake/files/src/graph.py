import pickle, sys, re
from collections import Counter
res = pickle.load(open(sys.argv[1], "rb"))
eps, delta = float(sys.argv[2]), float(sys.argv[3])
T = Counter(); dom = Counter(); G = 0
for r in res:
    if r["eps"] == eps and r["delta"] == delta:
        G += r["gens"]
        for a, b, v in r["trans"]: T[(a, b)] += v
        for d, v in r["dom"]: dom[d] += v
NAMES = {"0:D[0,0]": "ALLD", "0:C[0,0]": "ALLC", "0:C[0,1] 1:D[0,1]": "TFT", "0:C[0,1] 1:D[1,1]": "GRIM",
         "0:D[0,1] 1:D[0,2] 2:C[2,0]": "handshake", "0:D[1,2] 1:D[1,0] 2:C[2,1]": "shifty handshake",
         "0:C[0,1] 1:D[1,2] 2:D[1,0]": "stiffened wooer", "0:D[1,0] 1:C[0,0]": "echo-once",
         "0:C[0,1] 1:D[1,0]": "WSLS", "0:D[1,0] 1:C[0,1]": "suspicious TFT"}
def nm(d):
    body = re.sub(r"^<fsm s0 |>$", "", d)
    return NAMES.get(body, body.replace(" ", "\\n"))
top = [d for d, _ in dom.most_common(12)]
print("digraph G { rankdir=LR; node [shape=box, style=\"rounded,filled\", fillcolor=\"#eef3f7\", fontname=Helvetica, fontsize=10]; edge [fontname=Helvetica, fontsize=8, color=\"#55606a\"];")
for d in top:
    print(f'  "{d}" [label="{nm(d)}\\n{100*dom[d]/G:.1f}% of time"];')
for (a, b), v in T.most_common():
    if a in top and b in top and v >= 3:
        print(f'  "{a}" -> "{b}" [label="{v}", penwidth={0.5+min(v,60)/12:.1f}];')
print("}")
