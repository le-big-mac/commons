# gathers the results of the LiftMin runs (c4 exhaustive, c5 CP-SAT) into one table
import re, glob, sys
sys.path.insert(0, '/home/agent3/lean/lift-audit')
from liftmin_conditions import lean_values, instances
val = lean_values()
exh = {}
for line in open("c4_liftmin_exhaustive.out"):
    m = re.match(r"\s+p=(\d+) q=(\d+) n=(\d+) r=(\d+)\s+Z_(\d+)\s+\(N=\s*(\d+)\)\s+S=(\d+)", line)
    if m:
        key = tuple(int(m[i]) for i in range(1, 5)); S = int(m[7])
        dis = int(re.search(r"DISAGREEMENTS (\d+)", line)[1])
        exh[key] = (S, dis)
cp = {}
for f in sorted(glob.glob("c5_cpsat_*.out")):
    key = None
    for line in open(f):
        m = re.match(r"p=(\d+) q=(\d+) n=(\d+) r=(\d+)\s+Z_", line)
        if m: key = tuple(int(m[i]) for i in range(1, 5)); cp.setdefault(key, {"agree": set(), "bound": {}, "member": set(), "dis": 0}); continue
        if key is None or " Lean " not in line: continue
        label = line.split(" Lean ")[0].strip()
        if "DISAGREES" in line: cp[key]["dis"] += 1
        if "  AGREES" in line: cp[key]["agree"].add(label)
        m = re.search(r"proved >= (\d+)", line)
        if m: cp[key]["bound"][label] = max(cp[key]["bound"].get(label, 0), int(m[1]))
        if "checked by long division: True" in line: cp[key]["member"].add(label)
print("| p | q | n | r | group | instances (U/A/B) | largest Lean value | exhaustive: all multisets of size <= S | exact by exhaustion | exact by CP-SAT | exact by either | left open |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
tot = [0, 0, 0]
for key in sorted(set(exh) | set(cp), key=lambda k: (k[0] ** k[2] * k[1] * k[3], k)):
    p, q, n, r = key
    insts = instances(p, q, n, r, val)
    kinds = [sum(1 for i in insts if i[0][0] == k) for k in "UAB"]
    labels = {str(i[0]): i[2] for i in insts}
    S, dis = exh.get(key, (None, 0))
    ex = {l for l, v in labels.items() if S is not None and v <= S}
    c = cp.get(key, {"agree": set(), "bound": {}, "member": set(), "dis": 0})
    either = ex | c["agree"]
    openl = sorted(set(labels) - either, key=lambda l: labels[l])
    def desc(l):
        lb = max(c["bound"].get(l, 0), (S + 1) if S is not None else 0)
        return f"{l} value {labels[l]}: " + ("member of that size checked; " if l in c["member"] else "") + f"least size proved >= {lb}"
    print(f"| {p} | {q} | {n} | {r} | Z_{p**n*q*r} | {len(insts)} ({kinds[0]}/{kinds[1]}/{kinds[2]}) | {max(labels.values())} | {('S = ' + str(S)) if S is not None else '-'} | {len(ex)} | {len(c['agree']) if key in cp else '-'} | {len(either)} | "
          + ("none" if not openl else ("; ".join(desc(l) for l in openl) if len(openl) <= 4 else
             f"{len(openl)} instances, Lean values {min(labels[l] for l in openl)}..{max(labels[l] for l in openl)}; for "
             f"{sum(1 for l in openl if l in c['member'])} of them a member of the Lean value's size was found and checked; lower bounds proved are below the Lean value")) + " |")
    tot[0] += len(insts); tot[1] += len(either); tot[2] += dis + c["dis"]
print(f"\ninstances in all: {tot[0]}; least size found equal to the Lean value: {tot[1]}; left open: {tot[0]-tot[1]}; disagreements: {tot[2]}")
