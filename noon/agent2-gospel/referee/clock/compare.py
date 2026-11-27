"""Referee: core.js's clock() against my own clock.py, and the made sentences' claims. Output: compare.out"""
import json, sys, math
sys.path.insert(0, '/home/agent2/gospel/referee/clock')
import clock
if __name__ == '__main__':
    D = json.load(open('/home/agent2/gospel/referee/clock/dump.json')); out = open('/home/agent2/gospel/referee/clock/compare.out', 'w')
    bad = []; corners = {}; fewest = 99; whole_in_open = 0; n_open_sq = 0; evens = 0
    for d in D:
        p, q = d['p'], d['q']; s, H = clock.round_hours(p, q); S = set(H); f = clock.factor(q)
        st = clock.study(p, q); mag = st[2]; g2 = st[3]
        if q % 2 == 0: evens += 1
        if all(l == 2 for l in f):                       # a power of 2
            continue
        if d['n'] != len(H) or d['tail'] != s or d['first'] != H[0]: bad.append((p, q, 'hours'))
        if sorted(d['kinds']) != sorted(g2): bad.append((p, q, 'kinds', d['kinds'], g2))
        if abs(d['off'] - mag / len(H)) > 1e-9: bad.append((p, q, 'balance point'))
        if d['bounded'] != (mag < 1e-9) or d['bounded'] != bool(g2): bad.append((p, q, 'closes'))
        if d['bounded']:
            fewest = min(fewest, len(H) // min(g2))
        else:
            for l, e in f.items():
                if l == 2 or e < 2: continue
                n_open_sq += 1
                for a in H:
                    c = sum(1 for j in range(l) if (a + j * (q // l)) % q in S); corners[c] = corners.get(c, 0) + 1
                    if c == l: whole_in_open += 1
    print('%d turtles (%d with even q): core.js clock() against mine: faults %d %s' % (len(D), evens, len(bad), bad[:6]), file=out)
    print('closed rounds: fewest polygons in any %d' % fewest, file=out)
    print('open rounds with a repeated odd prime l (%d cases): corners of the l-gon through each marked hour that are marked: %s; whole polygons: %d' % (n_open_sq, corners, whole_in_open), file=out)
    st = clock.study(1, 63); print('1/63: |sum| %.4f, over 6 = %.4f' % (st[2], st[2] / 6), file=out)
    out.close(); print(open('/home/agent2/gospel/referee/clock/compare.out').read())
