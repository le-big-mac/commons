"""End-to-end test of the two searches on Z_36 against the exhaustive ground truth (res36.pkl: every weak tile of Z_36 up to x -> u x + t,
decided by the full LP with exact certificates).  The scripts are executed from their source text with small textual patches IN MEMORY
(files untouched): a log line after each 0/1 programme, fewer CP-SAT workers, and -- for the mutation runs -- a weakened hypothesis so that
'violations' DO exist and must be found exactly where the ground truth has them.
For each programme (k, Z, non-divisibility condition) the script tried:
    expected feasible  <=>  some weak tile in the ground truth has size k, zero set containing Z, and satisfies the non-divisibility condition
(valid because Z allows k, so every set with size k and zeros containing Z is a weak tile, and zero sets are invariant under x -> u x + t)."""
import sys, io, pickle, contextlib, time
from common import *
from loadscripts import T1, T2, _exec
p, a, q, b = 2, 2, 3, 2; M = 36
res = pickle.load(open("/tmp/rev_t2/res36.pkl", "rb"))
truth = [(r[1], frozenset(r[4])) for r in res if r[2] == "yes"] + [(1, frozenset()), (M, frozenset(d for d in divisors(M) if d > 1))]
truth = sorted(set(truth), key=lambda t: (t[0], sorted(t[1])))
val = lambda o: p ** o[0] * q ** o[1]
def run_t2(need_patch, flags):
    src = open(T2).read()
    s0 = "need = {(i, 0), (0, j)}"; assert src.count(s0) == 1
    if need_patch is not None: src = src.replace(s0, need_patch)
    s1 = "st, xs = solve01(Am, rhs, None if control else wit); nmilp += 1"; assert src.count(s1) == 1
    src = src.replace(s1, s1 + "; LOG.append((i, j, k, Z, st))")
    assert src.count("num_workers = 8") == 1; src = src.replace("num_workers = 8", "num_workers = 2")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): ns = _exec(src, [p, a, q, b, 60] + flags, "t2search_patched", {"LOG": []})
    return ns, buf.getvalue()
for label, patch, needf in [("original hypothesis (p^i and q^j zeros)", None, lambda i, j: {p ** i, q ** j}),
                            ("MUTATION: only p^i a zero", "need = {(i, 0)}", lambda i, j: {p ** i}),
                            ("MUTATION: only q^j a zero", "need = {(0, j)}", lambda i, j: {q ** j}),
                            ("MUTATION: no hypothesis", "need = set()", lambda i, j: set())]:
    for flags in (["--exact", "--cpsat"], []):
        t0 = time.time(); ns, outp = run_t2(patch, flags); LOG = ns["LOG"]
        feas = wrong = und = 0; cells = {}
        for (i, j, k, Z, st) in LOG:
            Zv = {val(o) for o in Z}; assert needf(i, j) <= Zv and p ** i * q ** j not in Zv
            expect = any(kk == k and Zv <= ZA and p ** i * q ** j not in ZA for kk, ZA in truth)
            und += st not in (0, 2); feas += st == 0; wrong += (st == 0) != expect and st in (0, 2)
            if st == 0: cells[(i, j)] = cells.get((i, j), 0) + 1
        # ground truth per (i, j): is there a weak tile with the hypothesis and p^i q^j not a zero?  The search must find a set iff so.
        cell_ok = all((any(needf(i, j) <= ZA and p ** i * q ** j not in ZA and 2 <= kk < M for kk, ZA in truth)) == ((i, j) in cells) for i in range(1, a + 1) for j in range(1, b + 1))
        nfound = len(ns["found"]); ncomp = sum(1 for x in ns["found"] if x[5])
        print(f"t2search Z_36 [{' '.join(flags) or 'float patterns, HiGHS'}] {label}: {len(LOG)} programmes, {feas} feasible, {und} undecided, "
              f"{wrong} verdicts differing from the ground truth;  per-(i, j) existence agrees with ground truth: {cell_ok};  "
              f"sets found {nfound}, of which the script's exact_complement says weak tile: {ncomp}   [{time.time() - t0:.0f} s]", flush=True)
# ---- t1search: all sizes (the filter 'k == t1' removed), log every programme
src = open(T1).read()
s0 = "if (k == t1) == control: allowed.setdefault(k, []).append(Z)"; assert src.count(s0) == 1
s1 = "st, A = find(k, Z, nz); nprog += 1"; assert src.count(s1) == 1
assert src.count("num_workers = 8") == 1
PPv = [d for d in divisors(M) if d > 1 and (d % p != 0 or d % q != 0)]
for label, patched in [("as published (sizes different from the (T1) value)", src), ("--control (sizes equal to the (T1) value)", src),
                       ("MUTATION: every size", src.replace(s0, "allowed.setdefault(k, []).append(Z)"))]:
    s = patched.replace(s1, s1 + "; LOG.append((S, k, Z, st, t1))").replace("num_workers = 8", "num_workers = 2")
    buf = io.StringIO(); t0 = time.time()
    with contextlib.redirect_stdout(buf): ns = _exec(s, [p, a, q, b, 60] + (["--control"] if "control" in label else []), "t1search_patched", {"LOG": []})
    LOG = ns["LOG"]; feas = wrong = und = 0; feas_viol = 0
    for (S, k, Z, st, t1) in LOG:
        Sv = {val(o) for o in S}; Zv = {val(o) for o in Z}; assert {d for d in Zv if d in PPv} == Sv
        expect = any(kk == k and Zv <= ZA and {d for d in ZA if d in PPv} == Sv for kk, ZA in truth)
        und += st not in (0, 2); feas += st == 0; wrong += (st == 0) != expect and st in (0, 2); feas_viol += (st == 0 and k != t1)
    # completeness the other way: every ground-truth weak tile (size, zero set) must be 'covered' by a feasible programme of the every-size run
    cover = None
    if "every size" in label:
        cover = all(any(st == 0 and k == kk and {val(o) for o in Z} <= ZA and {val(o) for o in S} == {d for d in ZA if d in PPv} for (S, k, Z, st, t1) in LOG) for kk, ZA in truth)
    print(f"t1search Z_36 {label}: {len(LOG)} programmes, {feas} feasible ({feas_viol} at a size different from the (T1) value), {und} undecided, "
          f"{wrong} verdicts differing from the ground truth" + ("" if cover is None else f";  every ground-truth (size, zero set), including the two trivial tiles, is covered by a feasible programme: {cover}")
          + f";  sets found {len(ns['found'])}, weak tiles by the script's exact check {len(ns['bad'])}   [{time.time() - t0:.0f} s]", flush=True)
    print("      script's last line:", buf.getvalue().strip().split("\n")[-1])
