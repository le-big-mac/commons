"""Dr Young's rods, the second sheet: the caption's afterlife.
    python -I after2.py ~/lantern-data            ->  after2.out (printed), after2.json

A. what a lantern does that is built to the Encyclopaedia Britannica's words of 1842 ("the rods KN and KL must be equal")
B. the rods as three engravers drew them: Young's plate (1806), Brewster's woodcut (1832), the Britannica's plate (seventh edition)
C. the seventh and eighth editions' sections compared word for word
D. the printings of Young's caption that I fetched: is Young named, how is it introduced, which rods are said to be equal
Then the seven sealed lines of expectations-2.md.
"""
import difflib, json, math, os, re, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lantern as L

MS = (2.0, 3.0, 5.0, 10.0, 20.0)

# ---------------------------------------------------------------- A
def words(a=11.0, sharp_at=None, f=1.0, c2=None):
    """the rods as the Britannica has them: IK = a, KN = KL = b. They keep IL x IN = a^2 - b^2. With sharp_at None, a^2 - b^2 = f^2;
    else a^2 - b^2 is chosen so that the image is sharp when it is sharp_at times the slider: x (x + x') = f^2 (1 + 1/m^2).
    c2, if given, is a^2 - b^2 itself, in squares of the focal length."""
    if c2 is None: c2 = 1.0 if sharp_at is None else (1 + 1.0 / sharp_at ** 2)
    c2 = c2 * f * f; b = math.sqrt(a * a - c2); return L.Rods(a=a, f=f, b=b, a2=b)

def best_trim(m_lo, m_hi, a=30.0, steps=240, grid=2401):
    """KL trimmed (so IK^2 - KL^2 chosen) to make the worst patch between m_lo and m_hi times as small as it can be: (IK^2 - KL^2, that worst patch)"""
    ms = [m_lo * (m_hi / m_lo) ** (i / float(steps)) for i in range(steps + 1)]; best = None
    for j in range(grid):
        c2 = 1.0 + 0.3 * j / (grid - 1); r = words(a, c2=c2); w = max(patch(r, m) for m in ms)
        if best is None or w < best[1]: best = (c2, w)
    return best

def worst_two(p, c2, ms, a=30.0):
    """the worst patch over the sizes ms of rods with KN = KL, IK^2 - KL^2 = c2, and I at p before the slider (Young has 2); 9 if they jam"""
    if a * a - c2 <= 0: return 9.0
    b = math.sqrt(a * a - c2); r = L.Rods(a=a, b=b, a2=b, p=p); w = 0.0
    for m in ms:
        D = L.D_of_m(m, r.f); s = r.lens(D)
        if s is None or s <= r.f: return 9.0
        w = max(w, L.blur(D, s, r.f))
    return w
def best_two(m_lo, m_hi, steps=60):
    """KL trimmed and I moved along the line as well: (I's distance before the slider, IK^2 - KL^2, the worst patch), by a coarse grid and
    then three finer ones about the best"""
    ms = [m_lo * (m_hi / m_lo) ** (i / float(steps)) for i in range(steps + 1)]; best = (9.0, 2.0, 1.0); hp, hc = 0.3, 0.6
    for _ in range(4):
        p0, c0 = best[1], best[2]
        for i in range(-30, 31):
            for j in range(-30, 31):
                p, c2 = p0 + hp * i / 30.0, c0 + hc * j / 30.0; w = worst_two(p, c2, ms)
                if w < best[0]: best = (w, p, c2)
        hp, hc = hp / 8.0, hc / 8.0
    return best[1], best[2], best[0]

def patch(r, m):
    D = L.D_of_m(m, r.f); s = r.lens(D); return None if s is None else L.blur(D, s, r.f)

def pencil(m, c2=1.0):
    """first order: the lens is x - c2 / (x + x') from its place, x = 1/m, x' = m; the patch is (m - 1) times that"""
    return (m - 1) * abs(1.0 / m - c2 / (m + 1.0 / m))

# ---------------------------------------------------------------- B
DRAWINGS = {   # places read by eye on enlarged crops of the scans; pixels of the scan; sd is my reading error in pixels
    "Young's plate, 1806 (Lectures, 1807, Plate XXVIII, Fig. 401)": dict(I=(1022, 981), L=(1054, 982), K=(1209, 753), N=(1376, 990), sd=1.5),
    "Brewster's woodcut, 1832 (Letters on Natural Magic, p. 83, Fig. 6)": dict(I=(933, 1597), L=(990, 1582), K=(1153.6, 1084), N=(1337, 1598), sd=8.0),     # the pivots are thick hooks: the rods' ends taken
    "the Britannica's plate, seventh edition (Plate CCCLXXXVI, Fig. 110)": dict(I=(878, 3689), L=(932, 3706), K=(2248, 3304), N=(2808, 3786), sd=4.0),
    "the Britannica's woodcut, eighth edition (vol. 16, p. 697, Fig. 282)": dict(I=(817, 1400), L=(866, 1411), K=(2140, 1007), N=(2697, 1475), sd=4.0),
}
def ratios(P):
    d = lambda p, q: math.hypot(P[p][0] - P[q][0], P[p][1] - P[q][1])
    return {'KN/IK': d('K', 'N') / d('I', 'K'), 'KL/IK': d('K', 'L') / d('I', 'K'), 'KL/KN': d('K', 'L') / d('K', 'N'), 'IK': d('I', 'K')}
def drawing(name, draws=20000):
    P = DRAWINGS[name]; sd = P['sd']; base = ratios(P)
    rng = np.random.default_rng(sum(ord(ch) for ch in name)); acc = {k: [] for k in base}        # seeded by the drawing's name
    for _ in range(draws):
        Q = {k: (P[k][0] + rng.normal(0, sd), P[k][1] + rng.normal(0, sd)) for k in 'ILKN'}; r = ratios(Q)
        for k in r: acc[k].append(r[k])
    return {k: (base[k], float(np.std(acc[k]))) for k in base}

# ---------------------------------------------------------------- C
EB7_LINES = ((89675, 89696), (89741, 89769))                            # the section stands in two columns of p. 514, with other articles between
EB8_LINES = ((130505, 130521), (130443, 130448), (130497, 130497), (130451, 130486))      # the scan's text has p. 697 in this order
EB8_MARGIN = ('—\\~—', 'Phantas-', 'magoric', '4pparatus.')    # the side note, which the scan ran into the lines
def section(path, ranges, margin=()):
    lines = open(path, encoding='utf-8', errors='replace').read().split('\n'); out = []
    for a, b in ranges:
        for l in lines[a - 1:b]:
            l = l.rstrip()
            for mg in margin:
                if l.endswith(mg): l = l[:-len(mg)].rstrip()
            if l.strip(): out.append(l.strip())
    return ' '.join(out)
def fold(s):
    s = re.sub(r'-\s+', '', s); s = s.lower(); s = re.sub(r'[^a-z0-9 ]+', ' ', s); return s.split()
def letters(s):
    """letters and digits only, the scan's spacing and hyphens at line ends gone"""
    return re.sub(r'[^a-z0-9]+', '', re.sub(r'-\s+', '', s).lower())
def compare(a, b):
    """the runs of words in which the two differ: (words of a, words of b)"""
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return [(a[i1:i2], b[j1:j2]) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal']

# ---------------------------------------------------------------- D
PRINTINGS = [   # (folder, year, what, the line of the fetched text where the rods come in, read by me: named, how introduced, equal rods)
    ('eb4-1810', 1810, "Encyclopaedia Britannica, 4th edition, vol. 18", True, 'Dr Thomas Young proposes the following apparatus for an exhibition similar to the phantasmagoria', 'KN, IK'),
    ('eb5-1815', 1815, "Encyclopaedia Britannica, 5th edition, vol. 18", True, 'the same words', 'KN, IK'),
    ('hutton-1815', 1815, "Hutton, A Philosophical and Mathematical Dictionary, vol. 2", True, 'the following construction, which is suggested by Dr. Young', 'KN, KI'),
    ('eb6-1823', 1823, "Encyclopaedia Britannica, 6th edition, vol. 18", True, 'Dr Thomas Young proposes the following apparatus for an exhibition similar to the phantasmagoria', 'KN, IK'),
    ('ferguson-1823', 1823, "Ferguson's Lectures, Brewster's edition, vol. 2", True, 'a very excellent arrangement for a phantasmagoria has been proposed by Dr. Young, which we shall describe in his own words', 'KN, IK'),
    ('edinburgh-v14', 1832, "The Edinburgh Encyclopaedia (Brewster's), vol. 14, OPTICS (an American printing dated 1832)", True, 'a very excellent arrangement for a phantasmagoria has been proposed by Dr. Young, which we shall describe in his own words', 'KN, IK'),
    ('artisan-1825', 1825, "The Artisan; or, Mechanic's Instructor", True, 'an arrangement, which has been proposed by Dr. Young', 'KN, IK'),
    ('london-1829', 1829, "The London Encyclopaedia, vol. 16, OPTICS", True, "Dr. Young's suggestions may be thus illustrated", 'KN, IK'),
    ('recreations-1830', 1830, "Recreations in Science", False, 'Improved Phantasmagoria (a heading; no name)', 'KN, IK'),
]
KEY = re.compile(r'lowers\s+the\s+point', re.I)
FURTHER = ('straight line', 'same line', 'right line', 'in a line', 'in one line', 'length of k', 'length of the rod k', 'squares of', 'square of the focal',
           'plane of the screen', 'shorter than', 'less than i')
def printing(root, folder):
    """the caption in one fetched text: where it stands; whether Young is named in it or in the paragraph on either side (the scan's
    text is rough: Yonng, Youngs); which rods it says must be equal, as the scan reads; and whether any words of a further condition
    are in the caption itself (from 600 characters before 'lowers the point' to 1500 after)"""
    raw = open(os.path.join(root, 'afterlife', folder, 'text.txt'), encoding='utf-8', errors='replace').read()
    m0 = KEY.search(raw); k = m0.start(); line = raw.count('\n', 0, k) + 1
    wide = re.sub(r'\s+', ' ', raw[max(0, k - 3500):k + 2500]); cap = re.sub(r'\s+', ' ', raw[max(0, k - 600):k + 1500])
    young = bool(re.search(r'Yo[un]{1,2}g', wide))
    m = re.search(r'[Tt]he\s+\S{0,3}\s*[rl]od\s+(.{1,6}?)\s+m\S{2,4}\s+be\s+equal\s+to\s+(.{1,5}?)[,.]', cap)
    added = [w for w in FURTHER if w in cap.lower()]
    return dict(line=line, young=young, equal=(m.group(1).strip() + ' to ' + m.group(2).strip()) if m else None, added=added)

if __name__ == '__main__':
    root = sys.argv[1]; out = {}
    print("A. A lantern built to the Britannica's words: IK = 11 f, KN = KL, I and L placed as Young has them. The patch as a fraction of the opening.")
    r1 = words(11.0); r2 = words(11.0, sharp_at=5.0); ry = L.Rods(a=11.0)
    print('   size of image                                   ' + '   '.join('%7g' % m for m in MS))
    print("   Young's rods (KN = IK, IK^2 - KL^2 = f^2)          " + '   '.join('%7.4f' % patch(ry, m) for m in MS))
    print('   KN = KL, IK^2 - KL^2 = f^2                         ' + '   '.join('%7.4f' % patch(r1, m) for m in MS))
    print('      the same by pencil, (m - 1) / (m (m^2 + 1))     ' + '   '.join('%7.4f' % pencil(m) for m in MS))
    print('   KN = KL, IK^2 - KL^2 set for a sharp image at 5    ' + '   '.join('%7.4f' % patch(r2, m) for m in MS))
    print('      the same by pencil                              ' + '   '.join('%7.4f' % pencil(m, 1 + 1 / 25.0) for m in MS))
    for nm, r in (('KN = KL', r1),):
        D = L.D_of_m(5.0); k = r.K(D); s = r.lens(D); xI, xL, xN = r.p, s + r.q, D
        print('   check at 5 times: IL x IN = %.6f (IK^2 - KL^2 = %.6f); KL stands at %.1f degrees to the bar' % ((xL - xI) * (xN - xI), r.a ** 2 - r.b ** 2, r.thrust(D)[0]))
    out['A'] = {'words': {m: patch(r1, m) for m in MS}, 'words_sharp_at_5': {m: patch(r2, m) for m in MS}, 'young': {m: patch(ry, m) for m in MS}}
    out['A']['trim'] = {}
    for lo, hi in ((2.0, 20.0), (2.0, 10.0), (3.0, 20.0), (4.0, 20.0), (5.0, 20.0)):
        c2, w = best_trim(lo, hi); out['A']['trim']['%g-%g' % (lo, hi)] = (c2, w)
        print('   KL trimmed for the least worst patch from %g to %g times: IK^2 - KL^2 = %.3f f^2, sharp at %.2f times, and the patch is %.4f at both ends' % (lo, hi, c2, 1 / math.sqrt(c2 - 1) if c2 > 1 else float('inf'), w))
    out['A']['two'] = {}
    for lo, hi in ((2.0, 20.0), (3.0, 20.0), (4.0, 20.0), (5.0, 20.0)):
        p, c2, w = best_two(lo, hi); out['A']['two']['%g-%g' % (lo, hi)] = (p, c2, w)
        print('   KL trimmed and I moved as well, from %g to %g times: I %.4f f before the slider, IK^2 - KL^2 = %.3f f^2, the worst patch %.4f' % (lo, hi, p, c2, w))
    for a in (4.0, 6.0, 26.0):
        print('   rods of %g: KN = KL, IK^2 - KL^2 = f^2:              ' % a + '   '.join('%7s' % ('-' if patch(words(a), m) is None else '%.4f' % patch(words(a), m)) for m in MS))

    print('\nB. The rods as drawn (my reading error carried in; in brackets one standard deviation)')
    out['B'] = {}
    for name in DRAWINGS:
        d = drawing(name); out['B'][name] = d
        print('   %-70s KN/IK %.3f (%.3f)   KL/IK %.3f (%.3f)   KL/KN %.3f (%.3f)   IK %.0f px' % (name, d['KN/IK'][0], d['KN/IK'][1], d['KL/IK'][0], d['KL/IK'][1], d['KL/KN'][0], d['KL/KN'][1], d['IK'][0]))

    print('\nC. The seventh and the eighth editions, section "On the Phantasmagoric Apparatus", word for word')
    t7 = section(os.path.join(root, 'eb7', 'vol16_djvu.txt'), EB7_LINES); t8 = section(os.path.join(root, 'afterlife', 'eb8-v16', 'text.txt'), EB8_LINES, EB8_MARGIN)
    w7, w8 = fold(t7), fold(t8); diffs = compare(w7, w8); longest = max([max(len(a), len(b)) for a, b in diffs] or [0])
    print('   %d words and %d words; %d runs differ; the longest is %d words' % (len(w7), len(w8), len(diffs), longest))
    for a, b in diffs: print('      seventh: %-34s eighth: %s' % (' '.join(a) or '(nothing)', ' '.join(b) or '(nothing)'))
    for nm, t in (('seventh', t7), ('eighth', t8)):
        m = re.search(r'the rods (\S+) and (\S+) must be equal', t); print('   the %s has: "the rods %s and %s must be equal"; names Young: %s; "Robertson exhibited this remarkable": %s' % (nm, m.group(1), m.group(2), 'Young' in t, bool(re.search(r'Robertson exhibited this remarkable', t))))
    l7, l8 = letters(t7), letters(t8); ld = compare(list(l7), list(l8))
    print('   letter for letter, spacing apart: %d and %d letters; %d places differ: %s' % (len(l7), len(l8), len(ld), '; '.join('%s/%s' % (''.join(a) or '-', ''.join(b) or '-') for a, b in ld)))
    out['C'] = {'words7': len(w7), 'words8': len(w8), 'runs': len(diffs), 'longest': longest, 'diffs': diffs, 'letters7': len(l7), 'letters8': len(l8), 'letter_places': len(ld)}

    print('\nD. The printings before 1842 that are not Young\'s own or Brewster\'s Letters')
    out['D'] = []; named = 0; added_any = 0
    for folder, year, what, read_named, how, read_equal in PRINTINGS:
        p = printing(root, folder); named += read_named; added_any += bool(p['added'])
        agree = (p['young'] == read_named)
        print('   %d  %-88s line %6d   Young named: %-5s (by script: %-5s%s)   equal, as the scan reads: %-14s   words of a further condition: %s' % (year, what, p['line'], read_named, p['young'], '' if agree else ' DIFFERS', p['equal'], p['added'] or 'none'))
        print('         introduced: %s' % how)
        out['D'].append(dict(folder=folder, year=year, what=what, named=read_named, script_named=p['young'], equal=p['equal'], added=p['added'], how=how, line=p['line']))
    print('   named in %d of %d; a further condition in %d' % (named, len(PRINTINGS), added_any))

    print('\nThe sealed lines (expectations-2.md)')
    A = out['A']['words']; A5 = out['A']['words_sharp_at_5']; ok = []
    e1 = 0.09 <= A[2.0] <= 0.13 and 0.027 <= A[5.0] <= 0.035 and 0.008 <= A[10.0] <= 0.010 and 0.0020 <= A[20.0] <= 0.0028
    e2 = 0.07 <= A5[2.0] <= 0.10 and 0.030 <= A5[20.0] <= 0.040
    eb = out['B']["the Britannica's plate, seventh edition (Plate CCCLXXXVI, Fig. 110)"]; e3 = eb['KL/KN'][0] < 0.9
    e4 = added_any == 0; e5 = named >= 6; e6 = longest <= 3
    e7 = None   # by reading: see the README
    for nm, v, odds, note in (('E1', e1, 0.90, 'patch %.4f, %.4f, %.4f, %.4f at 2, 5, 10, 20 times' % (A[2.0], A[5.0], A[10.0], A[20.0])),
                              ('E2', e2, 0.85, 'set sharp at 5: %.4f at 2 times, %.4f at 20' % (A5[2.0], A5[20.0])),
                              ('E3', e3, 0.75, 'on the plate KL / KN is %.2f (%.2f)' % eb['KL/KN']),
                              ('E4', e4, 0.80, 'a further condition in %d of %d (by my reading and by a search for its words)' % (added_any, len(PRINTINGS))),
                              ('E5', e5, 0.60, 'Young named in %d of %d' % (named, len(PRINTINGS))),
                              ('E6', e6, 0.80, 'the longest differing run is %d words' % longest)):
        print('   %s  %-6s (odds %.2f)  %s' % (nm, 'HELD' if v else 'FAILED', odds, note)); ok.append((v, odds))
    print('   E7  by reading: the first volume gives OPTICS to Sir David Brewster twice (the preface, and a list of authors)   (odds 0.75)')
    ok.append((True, 0.75))
    print('   %d of %d held; Brier score %.3f' % (sum(v for v, _ in ok), len(ok), sum((o - v) ** 2 for v, o in ok) / len(ok)))
    json.dump(out, open(os.path.join(HERE, 'after2.json'), 'w'), indent=1)
