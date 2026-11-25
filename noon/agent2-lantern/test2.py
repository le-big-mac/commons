"""test2.py: after2.py tried on cases whose answers are known some other way.   python -I test2.py [a copy of after2.py]"""
import importlib.util, json, math, os, random, shutil, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); path = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, 'after2.py')
sys.path.insert(0, HERE)
spec = importlib.util.spec_from_file_location('after2_under_test', path); A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
import lantern as L
npass = nfail = 0
def ok(name, cond, detail=''):
    global npass, nfail
    if cond: npass += 1; print('pass  ' + name)
    else: nfail += 1; print('FAIL  ' + name + ('   ' + str(detail) if detail != '' else ''))
rnd = random.Random(1842)

# A. the Britannica's words as a machine
worst = 0.0; n = 0
for _ in range(400):
    a = rnd.uniform(3.0, 30.0); m0 = rnd.choice((None, rnd.uniform(1.5, 12.0))); r = A.words(a, sharp_at=m0); m = rnd.uniform(1.2, 0.9 * (a + r.b)); D = L.D_of_m(m); s = r.lens(D)
    if s is None: continue
    c2 = 1.0 if m0 is None else 1 + 1 / m0 ** 2; xI, xL, xN = 2.0, s + 1.0, D; worst = max(worst, abs((xL - xI) * (xN - xI) - c2)); n += 1
ok("words(): KN = KL, and the rods keep IL x IN = f^2, or f^2 (1 + 1/m0^2) when set sharp at m0 (%d rods and sizes, worst %.1e)" % (n, worst), n > 300 and worst < 1e-9 and all(abs(A.words(a).a2 - A.words(a).b) < 1e-12 and abs(A.words(a).a ** 2 - A.words(a).b ** 2 - 1) < 1e-9 for a in (3.0, 11.0, 26.0)))
ok("words(sharp_at=m0): the image is sharp at m0 and not elsewhere", all(A.patch(A.words(11.0, sharp_at=m0), m0) < 1e-9 for m0 in (2.0, 3.5, 5.0, 9.0)) and A.patch(A.words(11.0, sharp_at=5.0), 2.0) > 0.05 and A.patch(A.words(11.0), 5.0) > 0.02)
def by_hand(m, c2=1.0):          # the lens where IL = c2 / IN puts it; the image by the lens's law; the patch by similar triangles; nothing of lantern.py but D
    D = m + 1.0 / m + 2.0; IN = D - 2.0; IL = c2 / IN; s = 2.0 + IL - 1.0; si = s / (s - 1.0); return abs((D - s) - si) / si
w = max(abs(A.patch(A.words(11.0, sharp_at=m0), m) - by_hand(m, 1.0 if m0 is None else 1 + 1 / m0 ** 2)) for m0 in (None, 3.0, 5.0) for m in (1.5, 2.0, 3.0, 5.0, 10.0, 20.0))
ok("patch(): as worked by hand from IL = c^2 / IN and the lens's law (18 cases, worst %.1e)" % w, w < 1e-9)
ok("patch(): the same for rods of any length that reach (it depends on IK^2 - KL^2 only)", all(abs(A.patch(A.words(a), 5.0) - A.patch(A.words(11.0), 5.0)) < 1e-9 for a in (4.0, 6.0, 26.0)) and A.patch(A.words(4.0), 20.0) is None)
ok("pencil(): 1/10 at twice, 4/130 at 5 times; within 2 parts in 100 of the rays at 10 and 20 times, and 12 or more out at twice",
   abs(A.pencil(2.0) - 0.1) < 1e-12 and abs(A.pencil(5.0) - 4 / 130.0) < 1e-12 and all(abs(A.pencil(m) / A.patch(A.words(11.0), m) - 1) < 0.02 for m in (10.0, 20.0)) and A.pencil(2.0) / A.patch(A.words(11.0), 2.0) < 0.89)
w = max(abs(A.patch(A.words(30.0), m) - m * m / ((m * m + 1) * (m * m + m + 1))) for m in (1.2, 2.0, 3.0, 5.0, 10.0, 20.0, 40.0))
ok("patch(): with IK^2 - KL^2 = f^2 it is m^2 / ((m^2 + 1)(m^2 + m + 1)), the referee's closed form (seven sizes, worst %.1e)" % w, w < 1e-10)
ok("pencil(m, c2): nought where x (x + x') = c2", all(A.pencil(m0, 1 + 1 / m0 ** 2) < 1e-12 for m0 in (2.0, 5.0, 8.0)))

c2, w = A.best_trim(2.0, 20.0); r = A.words(30.0, c2=c2)
ok("best_trim(2, 20): at the best trim the patch is the same at both ends (%.4f) and a trim a hundredth either way is worse; from 5 to 20 times the best is better than from 2" % w,
   abs(A.patch(r, 2.0) - A.patch(r, 20.0)) < 3e-4 and abs(A.patch(r, 2.0) - w) < 3e-4 and all(max(A.patch(A.words(30.0, c2=c2 + d), m) for m in (2.0, 20.0)) > w + 1e-3 for d in (-0.01, 0.01)) and A.best_trim(5.0, 20.0)[1] < w)
ms_ = [2.0 * 10.0 ** (i / 60.0) for i in range(61)]; p2, c22, w2 = A.best_two(2.0, 20.0)
def brute(ms):          # the same least, by one plain grid along the valley (I from 1.97 to 2.01 in steps of 0.0005, the trim from 1.0 to 1.3 in steps of 0.002)
    return min(A.worst_two(1.97 + 0.0005 * i, 1.0 + 0.002 * j, ms) for i in range(81) for j in range(151))
bg = brute(ms_)
ok("best_two(2, 20): moving I as well does better than trimming alone by a quarter or more (%.4f against %.4f); a plain grid along the valley gives %.4f; I comes a hundredth nearer the slider (%.4f); and a step of a thousandth in I or a hundredth in the trim is worse" % (w2, w, bg, p2),
   w2 < 0.75 * w and abs(bg - w2) < 0.002 and w2 <= bg + 1e-9 and 0.005 < 2.0 - p2 < 0.02 and abs(A.worst_two(p2, c22, ms_) - w2) < 1e-12 and all(A.worst_two(p2 + dp, c22 + dc, ms_) > w2 for dp, dc in ((0.001, 0.0), (-0.001, 0.0), (0.0, 0.01), (0.0, -0.01))))
ok("worst_two(): with I at Young's place it is the trim's own figure; rods that jam are marked", abs(A.worst_two(2.0, c2, ms_) - w) < 3e-4 and A.worst_two(2.0, 1.0, [30.0], a=11.0) == 9.0)
ok("words(c2=...): IK^2 - KL^2 is what is asked", all(abs(A.words(11.0, c2=c).a ** 2 - A.words(11.0, c2=c).b ** 2 - c) < 1e-9 for c in (1.0, 1.04, 1.2)))
# B. the drawings
P = dict(I=(0.0, 0.0), L=(3.0, 0.0), K=(3.0, 4.0), N=(6.0, 0.0), sd=0.0); r = A.ratios(P)
ok("ratios(): a made-up drawing, K at (3, 4) over I (0, 0), L (3, 0), N (6, 0): KN/IK 1, KL/IK 0.8, KL/KN 0.8, IK 5", abs(r['KN/IK'] - 1) < 1e-12 and abs(r['KL/IK'] - 0.8) < 1e-12 and abs(r['KL/KN'] - 0.8) < 1e-12 and abs(r['IK'] - 5) < 1e-12)
P2 = dict(I=(0.0, 0.0), L=(1.0, 0.0), K=(0.0, 10.0), N=(24.0, 0.0), sd=0.0); r2 = A.ratios(P2)
ok("ratios(): a second, lopsided: KN/IK 2.6, KL/KN = root 101 / 26", abs(r2['KN/IK'] - 2.6) < 1e-12 and abs(r2['KL/KN'] - math.sqrt(101) / 26) < 1e-12)
A.DRAWINGS['made up, exact'] = dict(P, sd=0.0); A.DRAWINGS['made up, read to a tenth'] = dict(I=(0.0, 0.0), L=(30.0, 0.0), K=(30.0, 40.0), N=(60.0, 0.0), sd=1.0); A.DRAWINGS['made up, read to a tenth, again'] = dict(A.DRAWINGS['made up, read to a tenth'])
d0 = A.drawing('made up, exact', 500); d1 = A.drawing('made up, read to a tenth', 4000); d1b = A.drawing('made up, read to a tenth', 4000); d2 = A.drawing('made up, read to a tenth, again', 4000)
# each rod's length is out by root 2 (both ends); the two share K, which makes them go together a little (0.28 of 2): the ratio's spread is root(3.44) / 50 = 0.0371
ok("drawing(): no reading error, no spread; an error of 1 in rods of 50 spreads KN/IK by 0.037 (worked by hand; found %.4f); the same name gives the same draws and another name others" % d1['KN/IK'][1],
   d0['KN/IK'][1] == 0 and abs(d0['KL/KN'][0] - 0.8) < 1e-12 and 0.0350 < d1['KN/IK'][1] < 0.0392 and d1 == d1b and d1['KN/IK'][1] != d2['KN/IK'][1] and abs(d1['KN/IK'][0] - 1) < 1e-12)
for nm in ("Young's plate, 1806 (Lectures, 1807, Plate XXVIII, Fig. 401)",):
    import plate
    ok("the places of Young's plate are those of plate.py", all(tuple(A.DRAWINGS[nm][k]) == tuple(plate.PLACES[k]) for k in 'ILKN'))

# C. the comparison of texts
ok("fold(): case, stops and a hyphen at a line's end do not count", A.fold('The screen, which may ap-\nproach to it.') == 'the screen which may approach to it'.split())
ok("compare(): two texts that differ in one word and one dropped word give two runs", [(' '.join(a), ' '.join(b)) for a, b in A.compare(A.fold('the rods KN and KL must be equal and the point'), A.fold('the rods KN and IK must be equal the point'))] == [('kl', 'ik'), ('and', '')])
ok("compare(): the same text gives none; a run of four words is four long", A.compare(A.fold('a b c d'), A.fold('a b c d')) == [] and max(max(len(a), len(b)) for a, b in A.compare(A.fold('one two three four five six'), A.fold('one w x y z six'))) == 4)
ok("letters(): the scan's spacing does not count, a changed figure does", A.letters('When thisapparatus ismounted') == A.letters('Whenthisapparatusis mounted') and A.letters('fig. 110') != A.letters('fig. 282') and A.letters('ap-\nproach') == 'approach')
tmp = tempfile.mkdtemp(prefix='agent2-test2-%d-' % os.getpid(), dir='/dev/shm')
try:
    p = os.path.join(tmp, 't.txt'); open(p, 'w').write('one\ntwo Phantas-\nthree\n\nfour\nfive\nsix\n')
    ok("section(): the lines in the order asked, the side note taken off, blank lines dropped", A.section(p, ((5, 6), (1, 2)), ('Phantas-',)) == 'four five one two' and A.section(p, ((1, 3),)) == 'one two Phantas- three')
    # D. the reader of printings
    def put(folder, text):
        os.makedirs(os.path.join(tmp, 'afterlife', folder)); open(os.path.join(tmp, 'afterlife', folder, 'text.txt'), 'w').write(text)
    filler = '\n'.join('a line of some other article, number %d' % i for i in range(120)) + '\n'
    put('named', filler + 'suggested by Dr. Yonng in his Lectures\n' + 'x\n' * 12 + 'the rod IK lowers\nthe point K, and by means of the rod KL adjusts the slider. The rod KN must be\nequal to IK, and the point I must be twice\n' + filler)
    put('unnamed', filler + 'Improved Phantasmagoria\nthe rod I K lowers the point K. The rod K N must be equal to I K, and the point I\n' + filler)
    put('far', 'Dr Young on the eye\n' + filler * 3 + 'the rod IK lowers the point K. The lod KN mull be equal to IK, and\n' + filler)
    put('more', filler + 'the rod IK lowers the point K. The rod KN must be equal to IK, and the three centres must be in one line, and the square of the focal length\n' + filler)
    a, b, c, d = (A.printing(tmp, f) for f in ('named', 'unnamed', 'far', 'more'))
    ok("printing(): finds the caption though 'lowers / the point' is split over two lines, and gives its line", a['line'] == 134 and b['line'] == 122)
    ok("printing(): Young named near the caption is found, misread by the scan or not; not found where he is not named, or named only three pages before", a['young'] and not b['young'] and not c['young'] and d['young'] is False)
    ok("printing(): which rods are equal, as the scan reads, spaced or not, in the old spelling or not", a['equal'] == 'KN to IK' and b['equal'] == 'K N to I K' and c['equal'] == 'KN to IK')
    ok("printing(): words of a further condition are reported when they are there and not when they are not", a['added'] == [] and b['added'] == [] and set(d['added']) == {'in one line', 'square of the focal'})
finally: shutil.rmtree(tmp, ignore_errors=True)

# the record
if os.path.exists(os.path.join(HERE, 'after2.json')) and path == os.path.join(HERE, 'after2.py'):
    J = json.load(open(os.path.join(HERE, 'after2.json'))); out = open(os.path.join(HERE, 'after2.out')).read()
    ok("after2.out's sealed lines carry the figures of after2.json", ('%.4f, %.4f, %.4f, %.4f at 2, 5, 10, 20 times' % tuple(J['A']['words'][k] for k in ('2.0', '5.0', '10.0', '20.0'))) in out and ('the longest differing run is %d words' % J['C']['longest']) in out)
print('\n%d passed, %d failed' % (npass, nfail)); sys.exit(1 if nfail else 0)
