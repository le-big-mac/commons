# verdicts.py -- score the twelve sealed lines of expectations.md from classify.out and types.out.   python -I verdicts.py
import re, hashlib, os
here = os.path.dirname(os.path.abspath(__file__)); rd = lambda n: open(os.path.join(here, n)).read()
print('sha256 of expectations.md:', hashlib.sha256(rd('expectations.md').encode()).hexdigest()); print('posted on the board      :', rd('expectations.sha256').split()[0], '\n')
c = rd('classify.out'); t = rd('types.out'); out = []
def pack(name):
    m = re.search(r'^%s .*?missing (\d+); in the families (\[.*?\]): (\{.*?\}) admissible members up to 10\^8, of which present as curvatures: (\d+).*?; sporadic (\d+), the largest (\d+)\n.*\n(?:   of its 100 largest sporadic: multiples of 5: (\d+), of 13: (\d+), of 11: (\d+))?' % re.escape(name), c, re.M)
    return dict(missing=int(m.group(1)), fam=m.group(2), members=m.group(3), present=int(m.group(4)), spor=int(m.group(5)), largest=int(m.group(6)), fives=int(m.group(7)) if m.group(7) else None)
want = [('bugeye', 'bug-eye (-1, 2, 2, 3): 61 missing, the largest 97,287', 61, 97287, 0.9), ('strip', 'strip (0, 0, 1, 1): 215 missing, the largest 1,199,820', 215, 1199820, 0.85),
        ('m3_5_8_8', '(-3, 5, 8, 8): no n^2 or 6n^2; 676 sporadic, the largest 3,122,880', 676, 3122880, 0.85), ('m3_4_12_13', '(-3, 4, 12, 13): no 2n^2 or 6n^2; 731 sporadic, the largest 7,354,464', 731, 7354464, 0.85),
        ('m2_3_6_7', '(-2, 3, 6, 7): no 2n^2; 236 sporadic, the largest 429,039', 236, 429039, 0.85), ('m4_5_20_21', '(-4, 5, 20, 21): no 2n^2 or 3n^2; 3,659 sporadic, the largest 32,084,460', 3659, 32084460, 0.8)]
P = {}
for n, (name, text, cnt, mx, odds) in enumerate(want, 1):
    p = pack(name); P[name] = p; held = p['spor'] == cnt and p['largest'] == mx and p['present'] == 0
    out.append((n, text, 'read', odds, held, '%d sporadic, the largest %d; members of the families %s that are admissible: %s, present as curvatures: %d' % (p['spor'], p['largest'], p['fam'], p['members'], p['present'])))
r = re.search(r'Remark 6\.1: (.*)', c).group(1)
held7 = r == '(-3,5,8,8), class 5: missing []; (-3,4,12,13), class 13: missing []; bug-eye, classes 11, 14, 23: missing [], [], []; strip, class 1: missing [241]; bug-eye, class 2: missing [13154]'
out.append((7, "the paper's Remark 6.1, five parts", 'read', 0.85, held7, r))
m = re.search(r'residues as the type: (\d+) of 42; chi_2 as the type: (\d+) of 42; of the (\d+) packings whose type allows a fourth-power form, a witness below 10\^6 and nothing forbidden: (\d+)', t)
out.append((8, 'chi_2 from a pair of positive coprime curvatures of the root quadruple is the type\'s, for each of the 42', 'worked', 0.85, int(m.group(2)) == 42, '%s of 42 (the one that fails has no such pair in its root quadruple; taking the outer circle as partner gives the type\'s sign)' % m.group(2)))
out.append((9, 'the residues modulo 24 up to 10^6 are the type\'s set, for each of the 42', 'read', 0.9, int(m.group(1)) == 42, '%s of 42' % m.group(1)))
fives = [(n, P[n]['fives']) for n in ('strip', 'm3_5_8_8', 'm3_4_12_13', 'm2_3_6_7', 'm4_5_20_21')]
out.append((10, 'of the largest 100 sporadic of each of five packings, at least half are multiples of 5, in every one', 'guessed', 0.55, all(f >= 50 for n, f in fives), ', '.join('%s %d' % x for x in fives)))
pool = re.search(r'pooled \(500 numbers\): multiples of 13: (\d+), of 11: (\d+), of 5: (\d+)', c)
out.append((11, 'pooling those 500, more are multiples of 13 than of 11', 'guessed', 0.6, int(pool.group(1)) > int(pool.group(2)), 'of 13: %s, of 11: %s (of 5: %s)' % pool.groups()))
big = re.findall(r'^\((-\d+, \d+, \d+, \d+)\) up to 100000000: .*?admissible numbers of the four forms: (\d+); occurring as curvatures: (\d+)', t, re.M)
out.append((12, 'a fourth-power witness below 10^6 for each of the nine packings whose type allows one, none forbidden; none of the four forms below 10^8 in the three of type (6, 1, 1, -1)', 'guessed', 0.65,
            m.group(3) == '9' and m.group(4) == '9' and len(big) == 3 and all(b[2] == '0' for b in big), 'witnesses in %s of %s; the three: %s' % (m.group(4), m.group(3), '; '.join('(%s): %s of %s candidates occur' % (b[0], b[2], b[1]) for b in big))))
h = 0; br = 0.0
for n, text, kind, odds, held, saw in out:
    print('%2d. %-5s (%s, odds %.2f)  %s\n      saw: %s' % (n, 'HELD' if held else 'FELL', kind, odds, text, saw)); h += held; br += (odds - (1 if held else 0)) ** 2
kinds = {}
for o in out: kinds.setdefault(o[2], [0, 0]); kinds[o[2]][0] += o[4]; kinds[o[2]][1] += 1
print('\n%d of %d held; mean squared error of the odds (Brier) %.3f; by kind: %s' % (h, len(out), br / len(out), ', '.join('%s %d of %d' % (k, v[0], v[1]) for k, v in kinds.items())))
