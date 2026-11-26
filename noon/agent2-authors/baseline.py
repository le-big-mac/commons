"""Checks made on 26 November 2026, after a reader with the web set this experiment against the papers.
usage: python -I baseline.py > baseline.out      (standard library; run in this folder)
1. What a single number said for every statement would have scored, and each party's score against that.
2. How much of the gap between careful and quick readers on each sheet is a level (a flat shift of every number).
3. Ranking: on the one sheet with failures, how often each party put a statement that held above one that failed.
4. Round numbers.  5. Pushing every number further from one half (the field's "extremizing")."""
import json, sys, statistics as st
sys.dont_write_bytecode = True

def brier(p, y): return sum((a - b) ** 2 for a, b in zip(p, y)) / len(y)
def ext(p, a): return p ** a / (p ** a + (1 - p) ** a)
def auc(p, y):
    pos = [a for a, b in zip(p, y) if b == 1]; neg = [a for a, b in zip(p, y) if b == 0]
    return sum((a > b) + 0.5 * (a == b) for a in pos for b in neg) / (len(pos) * len(neg)), len(pos) * len(neg)

if __name__ == '__main__':
    S = {k: json.load(open(f'{k}/scored.json')) for k in ('sheet1', 'sheet2')}
    Q = {k: json.load(open(f'{k}/quick/scored.json')) for k in ('sheet1', 'sheet2')}
    y1, y2 = S['sheet1']['outcome'], S['sheet2']['outcome']; y = y1 + y2; n = len(y); base = sum(y) / n
    P = {'careful readers (median of three)': S['sheet1']['median'] + S['sheet2']['median'],
         "the authors' first numbers": S['sheet1']['quick'] + S['sheet2']['quick'],
         'Noon': S['sheet1']['outsider'] + S['sheet2']['outsider'],
         'quick readers (median of three)': Q['sheet1']['median'] + Q['sheet2']['median']}
    print(f"{n} statements, {int(sum(y))} held: base rate {base:.3f}. Sheet 1: {int(sum(y1))} of {len(y1)} held; sheet 2: {int(sum(y2))} of {len(y2)}.")
    cb = brier([base] * n, y)
    print(f"1. the same number for every statement: 0.5 scores {brier([0.5] * n, y):.3f}; the base rate {base:.3f} scores {cb:.3f}; 0.9 scores {brier([0.9] * n, y):.3f}")
    for k, p in P.items():
        b = brier(p, y)
        print(f"   {k:34s} score {b:.3f}; sheet 1 {brier(p[:12], y1):.3f}, sheet 2 {brier(p[12:], y2):.3f}; mean number {sum(p) / n:.3f}; skill against the base rate {1 - b / cb:+.2f}")
    c, q = P['careful readers (median of three)'], P['quick readers (median of three)']
    d1 = sum(a - b for a, b in zip(c[:12], q[:12])) / 12
    held2 = [i for i in range(12, 24) if y[i] == 1]; fail2 = [i for i in range(12, 24) if y[i] == 0]
    print(f"2. careful minus quick, mean difference: sheet 1 {d1:+.3f}; sheet 2, statements that held {sum(c[i] - q[i] for i in held2) / len(held2):+.3f}, that failed {sum(c[i] - q[i] for i in fail2) / len(fail2):+.3f}")
    print(f"   sheet 1: quick readers with {d1:.3f} added to every number (capped at 0.99) score {brier([min(0.99, x + d1) for x in q[:12]], y1):.3f}; careful readers {brier(c[:12], y1):.3f}; quick as they were {brier(q[:12], y1):.3f}")
    d2 = sum(c[i] - q[i] for i in range(12, 24)) / 12
    print(f"   sheet 2: quick readers with their mean difference {d2:+.3f} added to every number (kept within 0.01 and 0.99) score {brier([min(0.99, max(0.01, x + d2)) for x in q[12:]], y2):.3f}; careful readers {brier(c[12:], y2):.3f}; quick as they were {brier(q[12:], y2):.3f}")
    print("3. sheet 2, pairs of one statement that held and one that failed, share ranked the right way round:")
    for k, p in P.items():
        a, m = auc(p[12:], y2); print(f"   {k:34s} {a:.3f} of {m} pairs")
    print("4. numbers that are multiples of 0.05, and numbers from 0.5 to 0.8:")
    for name, rows in (('quick readers', Q['sheet1']['quick_readers'] + Q['sheet2']['quick_readers']), ('careful readers', S['sheet1']['readers'] + S['sheet2']['readers'])):
        allx = [x for r in rows for x in (r if isinstance(r, list) else list(r.values()))]
        print(f"   {name}: {sum(abs(x * 20 - round(x * 20)) < 1e-9 for x in allx)} of {len(allx)} multiples of 0.05; {sum(0.5 <= x <= 0.8 for x in allx)} between 0.5 and 0.8")
    print("6. each sheet's own best fixed number, and skill against it:")
    for name, yy, sl in (('sheet 1', y1, slice(0, 12)), ('sheet 2', y2, slice(12, 24))):
        b0 = sum(yy) / len(yy); cb0 = brier([b0] * len(yy), yy)
        print(f"   {name}: {int(sum(yy))} of {len(yy)} held; the fixed number {b0:.2f} scores {cb0:.3f}. " + "; ".join(f"{k.split(' (')[0]} {brier(p[sl], yy):.3f}" + (f" (skill {1 - brier(p[sl], yy) / cb0:+.2f})" if cb0 > 0 else "") for k, p in P.items()))
    print("7. confidence in the side taken (the number if above one half, else one minus it) against the share on the right side, all 24:")
    for k, p in P.items():
        conf = sum(max(x, 1 - x) for x in p) / n; right = sum((x > 0.5) == (b == 1) for x, b in zip(p, y)) / n
        print(f"   {k:34s} mean confidence {100 * conf:.0f}%, right side {100 * right:.0f}%: {100 * (right - conf):.0f} points under")
    print("8. pairs of one statement that held and one that failed, ranked the right way round: within sheet 2 (27 pairs), and over both sheets (63 pairs)")
    for k, p in P.items():
        a2, m2 = auc(p[12:], y2); a, mm = auc(p, y)
        print(f"   {k:34s} {a2 * m2:.1f} of {m2}; {a * mm:.1f} of {mm}")
    for i, r in enumerate(Q['sheet2']['quick_readers'], 1):
        rr = r if isinstance(r, list) else [r[k] for k in S['sheet2']['ids']]
        a2, m2 = auc(rr, y2); print(f"   quick reader {i} alone, sheet 2: {a2 * m2:.1f} of {m2}")
    print("5. every number pushed away from one half by squaring its odds (chosen after the outcomes were known):")
    for k, p in P.items():
        print(f"   {k:34s} {brier(p, y):.3f} -> {brier([ext(x, 2) for x in p], y):.3f}")
