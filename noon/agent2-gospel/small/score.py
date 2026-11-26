"""Score the fifth sheet (nearly.sealed.md) by its letter from the run's record and the 40-digit recomputation.
usage: python -I score.py small.sealed-run.out verify.out > score.out"""
import sys, re

def verdict(ok, tie=False): return 'a tie' if tie else ('HELD' if ok else 'FAILED')

if __name__ == '__main__':
    rec = open(sys.argv[1], encoding='utf-8').read(); ver = open(sys.argv[2], encoding='utf-8').read()
    below = {int(e): (int(r), int(p)) for e, r, p in re.findall(r'below 1e([+-]\d+): (\d+) real, (\d+) pairs', rec)}
    least = re.findall(r'm up to\s+(\d+): least real sum ([0-9.e+-]+), least complex sum ([0-9.e+-]+)', rec)[-1]
    N, lr, lc = int(least[0]), float(least[1]), float(least[2])
    top = re.findall(r'^\s+([0-9.e+-]+)\s+m = (\d+)\s+a = (\d+)\s+round of (\d+) steps\s+(real|complex)', rec, re.M)
    ctl = re.search(r'control: the largest sum of a round that the rule says closes \(coset of 1\): ([0-9.e+-]+) at m = (\d+)', rec)
    assert N == 2000000, N
    held = 0; lines = []
    def line(name, ok, what, tie=False):
        global held
        held += bool(ok) and not tie; lines.append('%s  %-6s  %s' % (name, verdict(ok, tie), what))
    r3, r4 = below[-3][0], below[-4][0]
    line('N1', 170 <= r3 <= 260, 'real sums below 1e-3: %d (band 170 to 260; the model gives 200)' % r3, tie=r3 in (169, 170, 171, 259, 260, 261))
    line('N2', 12 <= r4 <= 32, 'real sums below 1e-4: %d (band 12 to 32; the model gives 20)' % r4, tie=r4 in (11, 12, 13, 31, 32, 33))
    tie3 = any(abs(lr / e - 1) < 0.02 for e in (5e-7, 1.5e-5))
    line('N3', 5e-7 <= lr <= 1.5e-5, 'least real sum: %.6e (band 5e-7 to 1.5e-5)' % lr, tie=tie3)
    n6 = below[-6][0] + below[-6][1]
    line('N4', n6 == 0, 'sums below 1e-6: %d real, %d pairs' % below[-6])
    line('N5', lr < lc, 'least real %.6e, least of a pair %.6e' % (lr, lc))
    m6 = re.search(r'^pair m = (\d+), a = (\d+), \|S\| = ([0-9.e+-]+).*?\n((?:    m1 = .*\n?)*)', ver, re.M)
    ok6 = bool(m6) and abs(float(m6.group(3)) / lc - 1) < 1e-6 and 'S1 is real and smaller than the sum: True' in m6.group(4)
    line('N6', ok6, 'the least sum of a pair, m = %s: %s' % (m6.group(1) if m6 else '?', 'a product of a smaller real sum and another, with coprime orders' if ok6 else 'not such a product'))
    v0, m0, a0, n0, k0 = top[0]
    line('N7', int(n0) <= 200, 'the least sum of all, %s (m = %s, a = %s, %s), has a round of %s steps' % (v0, m0, a0, k0, n0))
    vw = re.search(r'largest difference ([0-9.e+-]+); (\d+) of (\d+) do not agree', ver)
    ok8 = float(ctl.group(1)) < 1e-8 and float(vw.group(1)) < 1e-9 and int(vw.group(2)) == 0
    line('N8', ok8, 'largest sum of a closing round %s (m = %s); of the %s smallest recomputed with 40 digits, %s differ, the largest difference %s' % (ctl.group(1), ctl.group(2), vw.group(3), vw.group(2), vw.group(1)))
    print('\n'.join(lines)); print('held: %d of %d' % (held, len(lines)))
