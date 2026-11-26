"""Which voices sound together, and which way the runs go. The meetings are worked from the rule (voice k makes M + k
turns in T seconds); the direction of the runs is read from the written list of notes, which is first checked against
the rule. Nothing here reads the sound.
   python meet.py pendula.json > meet.out      (standard library only)
Added 26 November 2026, after a reader found that the README had the first runs going up the scale."""
import sys, json
from fractions import Fraction
from math import gcd
sys.dont_write_bytecode = True

def main(path):
    d = json.load(open(path))
    N, T, M = d['N'], int(d['T']), d['M']
    turns = [M + k for k in range(N)]
    # exact meeting times: voice k sounds at T*n/(M+k)
    times = {}
    for k in range(N):
        for n in range(turns[k] + 1):
            times.setdefault(Fraction(T * n, turns[k]), []).append(k)
    print(f'{N} voices; voice k makes {M}+k turns in {T} s. Moments when three or more sound together:')
    for t in sorted(times):
        v = times[t]
        if len(v) >= 3:
            print(f'  {float(t):7.1f} s  {len(v):2d} voices: {v}')
    print('pairs of voices in the simplest ratios:')
    seen = {}
    for a in range(N):
        for b in range(a + 1, N):
            g = gcd(turns[a], turns[b]); r = (turns[a] // g, turns[b] // g)
            seen.setdefault(r, []).append((a, b))
    for r in sorted(seen, key=lambda r: r[1])[:6]:
        print(f'  {r[0]}:{r[1]}  voices {seen[r]}')
    # the list as written against the rule
    rule = sorted((round(T * n / turns[k], 5), k) for k in range(N) for n in range(turns[k] + 1))
    ev = sorted((round(t, 5), k) for t, k, m in d['strikes'])
    worst = max(abs(a[0] - b[0]) for a, b in zip(ev, rule)) if len(ev) == len(rule) else float('nan')
    print(f'the written list has {len(ev)} notes; the rule gives {len(rule)}; same voices in the same order: {[k for _, k in ev] == [k for _, k in rule]}; largest difference in time {worst:.1e} s')
    # the direction of motion, from the list as written. A step is from one note to the next when each sounds alone:
    # steps into, out of or inside a meeting of two or more voices have no one direction and are left out (and counted).
    from collections import Counter
    alone = Counter(t for t, k in ev)
    allsteps = len(ev) - 1
    steps = [(ev[i][0], ev[i + 1][1] - ev[i][1]) for i in range(len(ev) - 1) if alone[ev[i][0]] == 1 and alone[ev[i + 1][0]] == 1]   # (time of the earlier note, change of voice)
    # a run: two or more steps to the next-door voice, one after another, in the same direction
    inrun = [False] * len(steps)
    for i in range(len(steps) - 1):
        if steps[i][1] == steps[i + 1][1] and abs(steps[i][1]) == 1:
            inrun[i] = inrun[i + 1] = True
    print(f'{allsteps} steps from note to note in all; {allsteps - len(steps)} touch a meeting of two or more voices and are left out; {len(steps)} are counted')
    print('by twelve seconds (a step belongs to the stretch its earlier note falls in):')
    print('   steps down, steps up; steps to the next-door voice down, up; of those, steps inside a run of two or more')
    for w in range(T // 12):
        lo, hi = 12 * w, 12 * w + 12
        st = [(c, r) for (t, c), r in zip(steps, inrun) if lo <= t < hi]
        down = sum(1 for c, r in st if c < 0); up = sum(1 for c, r in st if c > 0)
        nd = sum(1 for c, r in st if c == -1); nu = sum(1 for c, r in st if c == 1)
        rd = sum(1 for c, r in st if c == -1 and r); ru = sum(1 for c, r in st if c == 1 and r)
        print(f'  {lo:3d} to {hi:3d} s: {len(st):3d} steps; {down:2d} down, {up:2d} up; next-door {nd:2d} down, {nu:2d} up; in runs {rd:2d} down, {ru:2d} up')
    print(f'of the {len(steps)} counted: next-door {sum(1 for t, c in steps if c == -1)} down, {sum(1 for t, c in steps if c == 1)} up;'
          f' in runs {sum(1 for (t, c), r in zip(steps, inrun) if r and c == -1)} down, {sum(1 for (t, c), r in zip(steps, inrun) if r and c == 1)} up')
    lone = [(t, c) for (t, c), r in zip(steps, inrun) if abs(c) == 1 and not r]
    print('next-door steps that are not in a run, by the time of the earlier note:', ', '.join(f'{t:.2f} ({"up" if c > 0 else "down"})' for t, c in lone))
    first = [k for t, k in ev if 0 < t <= 4.0]
    print('the first sixteen notes after the opening chord, by voice:', first)

if __name__ == '__main__':
    main(sys.argv[1])
