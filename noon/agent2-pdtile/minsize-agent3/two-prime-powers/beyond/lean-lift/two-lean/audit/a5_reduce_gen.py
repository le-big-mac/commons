# Generates A5_reduce_eval.lean (Lean evaluates `reduce` for r = 2 on given multisets) and the expected values by the rule
# "the multiplicity of x in reduce w' is the number of elements y of w' with y mod N = x" (representatives in [0, 2N)).
import random, json, sys
rng = random.Random(77)
cases = []
for N in [1, 2, 3, 4, 5, 6, 7, 9, 10, 12, 15, 18]:
    for k in range(4):
        w = [rng.choice([0, 0, 0, 1, 1, 2, 3]) for _ in range(2 * N)]
        if k == 0:
            w = [0] * (2 * N); w[rng.randrange(2 * N)] = 1          # one element
        if k == 1:
            w = [i + 1 for i in range(2 * N)]                       # all different multiplicities
        cases.append((N, w))
lines = ["import Pnq.Lift", "open Pnq.Lift",
         "/-! Audit: `reduce` for r = 2 (the instance `Fact (Nat.Prime 2)` is whatever Lean finds, as in the statements). -/",
         "set_option pp.explicit true in", "#synth Fact (Nat.Prime 2)"]
exp = []
for i, (N, w) in enumerate(cases):
    lines.append(f"def aw{i} : ZMod {2 * N} → ℕ := fun y => ({w} : List ℕ).getD y.val 0")
    lines.append(f"#eval (\"case {i}\", (List.range {N}).map fun i => reduce (N := {N}) (r := 2) aw{i} (i : ZMod {N}))")
    red = [0] * N
    for y, c in enumerate(w):
        red[y % N] += c
    exp.append({'case': i, 'N': N, 'w': w, 'reduce': red})
open(sys.argv[1], 'w').write("\n".join(lines) + "\n")
json.dump(exp, open('a5_reduce_expected.json', 'w'))
print(len(cases), "cases")
