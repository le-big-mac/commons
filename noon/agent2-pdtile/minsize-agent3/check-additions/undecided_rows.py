"""Which rows of the three larger groups are undecided, and whether the other solver reached them.  usage: undecided_rows.py OUT_DIR"""
import sys, json, os
od = sys.argv[1]
def read(name):
    path = os.path.join(od, name)
    if not os.path.exists(path): return None
    return {(tuple(r['E']), tuple(r['F'])): r for r in (json.loads(l) for l in open(path) if l.startswith('{'))}
for (p, q, cn, hn) in ((3, 5, 'n3-p3-q5-multi-cpsat.jsonl.part', 'n3-p3-q5-multi-highs.jsonl'), (5, 2, 'n3-p5-q2-multi-cpsat.jsonl.part', 'n3-p5-q2-multi-highs.jsonl.part'), (5, 3, None, 'n3-p5-q3-multi-highs.jsonl.part')):
    C = read(cn) if cn else None; H = read(hn)
    print(f"order {p**3*q}: CP-SAT rows {len(C) if C is not None else 'no file'}, HiGHS rows {len(H)}; sum of 'seconds' CP-SAT {sum(r['seconds'] for r in C.values()) if C else 0:.0f}, HiGHS {sum(r['seconds'] for r in H.values()):.0f}")
    und = sorted(set(k for T in (C, H) if T for k, r in T.items() if r['undecided'] or r['min'] is None))
    for k in und:
        d = lambda T: 'no file' if T is None else ('not reached' if k not in T else (f"decided, min {T[k]['min']}" if (not T[k]['undecided'] and T[k]['min'] is not None) else f"undecided at sizes {T[k]['undecided']}, min {T[k]['min']}"))
        print(f"   E = {list(k[0])}, F = {list(k[1])}: CP-SAT {d(C)}; HiGHS {d(H)}")
    both_und = [k for k in und if not any(T and k in T and not T[k]['undecided'] and T[k]['min'] is not None for T in (C, H))]
    print(f"   patterns some solver reached and none decided: {len(both_und)}")
