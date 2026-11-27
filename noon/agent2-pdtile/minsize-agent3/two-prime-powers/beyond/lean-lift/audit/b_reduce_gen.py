# Part 2: test `Pnq.Lift.reduce` by evaluation in Lean against this program.
# Writes B_reduce_eval.lean (the multisets as explicit lists indexed by the representative y.val)
# and b_reduce_expected.json (the reduction computed here: multiplicity of x = sum of w'(y) over y with y % N == x).
import json, random
random.seed(20261126)
pairs = [(1,2),(1,3),(1,5),(2,2),(2,3),(3,2),(3,3),(4,2),(4,3),(5,2),(6,2),(6,3),(6,5),(9,3),(10,3),(12,3),(7,5),(8,7),(15,2),(12,5)]
cases = []
for (N, r) in pairs:
    M = N * r
    ws = []
    ws.append([0]*M)                                   # empty
    ws.append([1]*M)                                   # the whole group
    ws.append([y for y in range(M)])                   # w'(y) = y : tells every position apart
    ws.append([(1 if y == M-1 else 0) for y in range(M)])  # a single element at the last representative
    ws.append([(1 if y == N % M else 0) for y in range(M)])  # a single element at N (residue 0) when r>1
    for _ in range(4):
        ws.append([random.choice([0,0,0,1,1,2,3,7]) for _ in range(M)])
    ws.append([10**(y % 7) + y*y for y in range(M)])   # large distinct weights
    for w in ws:
        cases.append((N, r, w))
def reduce_py(N, r, w):
    out = [0]*N
    for y, c in enumerate(w):
        out[y % N] += c
    return out
lean = ["import Pnq.Lift", "open Pnq.Lift",
        "instance : Fact (Nat.Prime 2) := ⟨by norm_num⟩", "instance : Fact (Nat.Prime 3) := ⟨by norm_num⟩",
        "instance : Fact (Nat.Prime 5) := ⟨by norm_num⟩", "instance : Fact (Nat.Prime 7) := ⟨by norm_num⟩",
        "/-- the multiset whose multiplicity at y is the entry number `y.val` of the list -/",
        "def ofList (M : ℕ) (L : List ℕ) : ZMod M → ℕ := fun y => L.getD y.val 0",
        "/-- the values of a function on ZMod N, listed by representative 0, 1, ..., N-1 -/",
        "def toList (N : ℕ) (f : ZMod N → ℕ) : List ℕ := (List.range N).map fun i => f (i : ZMod N)",
        "-- a second way to give the multiset: by equality with the cast of k, not through `val`",
        "def ofCast (M : ℕ) (L : List ℕ) : ZMod M → ℕ := fun y => ((List.range M).map fun (k : ℕ) => if y = ((k : ℕ) : ZMod M) then L.getD k 0 else 0).sum",
        "-- the representatives of the casts 0..N-1 (to check the listing itself)",
        "def vals (N : ℕ) : List ℕ := (List.range N).map fun i => ((i : ZMod N)).val"]
exp = []
for i, (N, r, w) in enumerate(cases):
    lean.append(f'#eval IO.println s!"CASE {i} {N} {r} {{toList {N} (reduce (N := {N}) (r := {r}) (ofList ({N} * {r}) {w}))}}"')
    exp.append({"i": i, "N": N, "r": r, "w": w, "reduce": reduce_py(N, r, w)})
# a third of them again, the multiset given the second way
for j in range(0, len(cases), 3):
    N, r, w = cases[j]
    lean.append(f'#eval IO.println s!"CAST {j} {N} {r} {{toList {N} (reduce (N := {N}) (r := {r}) (ofCast ({N} * {r}) {w}))}}"')
for N in sorted(set(N for N, r in pairs)):
    lean.append(f'#eval IO.println s!"VALS {N} {{vals {N}}}"')
open("B_reduce_eval.lean", "w").write("\n".join(lean) + "\n")
json.dump(exp, open("b_reduce_expected.json", "w"))
print(len(cases), "cases written")
