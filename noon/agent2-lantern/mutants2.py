"""mutants2.py: plant one fault at a time in a copy of after2.py and see whether test2.py notices.   python -I mutants2.py [WORKERS]
The first copy has no fault and must pass (the control). Writes mutants2.out."""
import os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable; WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 3
M = [('control', [])]
def m(name, *pairs): M.append((name, list(pairs)))
m("words(): Young's rods after all (KN = IK)", ("b = math.sqrt(a * a - c2); return L.Rods(a=a, f=f, b=b, a2=b)", "b = math.sqrt(a * a - c2); return L.Rods(a=a, f=f, b=b, a2=a)"))
m("words(): the 1/m^2 left out when set sharp", ("if c2 is None: c2 = 1.0 if sharp_at is None else (1 + 1.0 / sharp_at ** 2)", "if c2 is None: c2 = 1.0"))
m("words(): set sharp by 1/m, not its square", ("(1 + 1.0 / sharp_at ** 2)", "(1 + 1.0 / sharp_at)"))
m("words(): KL as IK less the constant, not the root of the difference of squares", ("b = math.sqrt(a * a - c2); return L.Rods(a=a, f=f, b=b, a2=b)", "b = a - c2; return L.Rods(a=a, f=f, b=b, a2=b)"))
m("best_two(): I never moved", ("p, c2 = p0 + hp * i / 30.0, c0 + hc * j / 30.0; w = worst_two(p, c2, ms)", "p, c2 = p0, c0 + hc * j / 30.0; w = worst_two(p, c2, ms)"))
m("best_two(): the coarse grid only", ("    for _ in range(4):\n        p0, c0 = best[1], best[2]", "    for _ in range(1):\n        p0, c0 = best[1], best[2]"))
m("worst_two(): the least patch over the sizes, not the worst", ("        w = max(w, L.blur(D, s, r.f))\n    return w", "        w = min(w, L.blur(D, s, r.f))\n    return w"))
m("worst_two(): rods that jam pass for sharp", ("        if s is None or s <= r.f: return 9.0", "        if s is None or s <= r.f: return 0.0"))
m("best_trim(): the least patch at the near end only", ("r = words(a, c2=c2); w = max(patch(r, m) for m in ms)", "r = words(a, c2=c2); w = patch(r, ms[0])"))
m("best_trim(): the first trim tried is kept", ("if best is None or w < best[1]: best = (c2, w)", "if best is None: best = (c2, w)"))
m("words(c2): the constant given is doubled", ("c2 = c2 * f * f; b = math.sqrt(a * a - c2)", "c2 = 2 * c2 * f * f; b = math.sqrt(a * a - c2)"))
m("patch(): the screen at the slider's own size plus m", ("D = L.D_of_m(m, r.f); s = r.lens(D); return None if s is None else L.blur(D, s, r.f)", "D = 2 + m; s = r.lens(D); return None if s is None else L.blur(D, s, r.f)"))
m("patch(): a rod that cannot reach is given a patch of nought", ("return None if s is None else L.blur(D, s, r.f)", "return 0.0 if s is None else L.blur(D, s, r.f)"))
m("pencil(): m + 1 for m - 1", ("return (m - 1) * abs(1.0 / m - c2 / (m + 1.0 / m))", "return (m + 1) * abs(1.0 / m - c2 / (m + 1.0 / m))"))
m("pencil(): IN taken as x' alone", ("return (m - 1) * abs(1.0 / m - c2 / (m + 1.0 / m))", "return (m - 1) * abs(1.0 / m - c2 / m)"))
m("ratios(): KN/IK as IK/KN", ("return {'KN/IK': d('K', 'N') / d('I', 'K'),", "return {'KN/IK': d('I', 'K') / d('K', 'N'),"))
m("ratios(): KL/KN as KL/IK", ("'KL/KN': d('K', 'L') / d('K', 'N'),", "'KL/KN': d('K', 'L') / d('I', 'K'),"))
m("ratios(): lengths by their widths only", ("d = lambda p, q: math.hypot(P[p][0] - P[q][0], P[p][1] - P[q][1])", "d = lambda p, q: abs(P[p][0] - P[q][0])"))
m("drawing(): the reading error left out", ("Q = {k: (P[k][0] + rng.normal(0, sd), P[k][1] + rng.normal(0, sd)) for k in 'ILKN'}", "Q = {k: (P[k][0], P[k][1]) for k in 'ILKN'}"))
m("drawing(): only K is read with error", ("Q = {k: (P[k][0] + rng.normal(0, sd), P[k][1] + rng.normal(0, sd)) for k in 'ILKN'}", "Q = {k: ((P[k][0] + rng.normal(0, sd), P[k][1] + rng.normal(0, sd)) if k == 'K' else (P[k][0], P[k][1])) for k in 'ILKN'}"))
m("drawing(): every drawing the same seed", ("rng = np.random.default_rng(sum(ord(ch) for ch in name))", "rng = np.random.default_rng(1806)"))
m("drawing(): no seed", ("rng = np.random.default_rng(sum(ord(ch) for ch in name))", "rng = np.random.default_rng()"))
m("drawing(): the middle figure from the draws, not from the places", ("return {k: (base[k], float(np.std(acc[k]))) for k in base}", "return {k: (float(np.mean(acc[k])), float(np.std(acc[k]))) for k in base}"))
m("Young's plate: K read ten pixels off", ("dict(I=(1022, 981), L=(1054, 982), K=(1209, 753), N=(1376, 990), sd=1.5)", "dict(I=(1022, 981), L=(1054, 982), K=(1219, 753), N=(1376, 990), sd=1.5)"))
m("section(): the ranges taken in the file's order", ("    for a, b in ranges:\n        for l in lines[a - 1:b]:", "    for a, b in sorted(ranges):\n        for l in lines[a - 1:b]:"))
m("section(): the side note left in", ("                if l.endswith(mg): l = l[:-len(mg)].rstrip()", "                pass"))
m("section(): one line short", ("        for l in lines[a - 1:b]:", "        for l in lines[a - 1:b - 1]:"))
m("fold(): hyphens at line ends not joined", ("    s = re.sub(r'-\\s+', '', s); s = s.lower(); s = re.sub(r'[^a-z0-9 ]+', ' ', s); return s.split()", "    s = s.lower(); s = re.sub(r'[^a-z0-9 ]+', ' ', s); return s.split()"))
m("fold(): case counts", ("s = re.sub(r'-\\s+', '', s); s = s.lower(); s = re.sub(r'[^a-z0-9 ]+', ' ', s); return s.split()", "s = re.sub(r'-\\s+', '', s); s = re.sub(r'[^A-Za-z0-9 ]+', ' ', s); return s.split()"))
m("compare(): only words changed, not words dropped or added", ("if tag != 'equal']", "if tag == 'replace']"))
m("letters(): figures dropped", ("return re.sub(r'[^a-z0-9]+', '', re.sub(r'-\\s+', '', s).lower())", "return re.sub(r'[^a-z]+', '', re.sub(r'-\\s+', '', s).lower())"))
m("printing(): the caption looked for on one line", ("KEY = re.compile(r'lowers\\s+the\\s+point', re.I)", "KEY = re.compile(r'lowers the point', re.I)"))
m("printing(): Young looked for in the whole text", ("wide = re.sub(r'\\s+', ' ', raw[max(0, k - 3500):k + 2500]);", "wide = re.sub(r'\\s+', ' ', raw);"))
m("printing(): Young looked for only as the scan should have read him", ("young = bool(re.search(r'Yo[un]{1,2}g', wide))", "young = bool(re.search(r'Young', wide))"))
m("printing(): the line counted from nought", ("line = raw.count('\\n', 0, k) + 1", "line = raw.count('\\n', 0, k)"))
m("printing(): words of a further condition never reported", ("added = [w for w in FURTHER if w in cap.lower()]", "added = []"))
m("printing(): the old spelling of 'must' not allowed for", ("\\s+m\\S{2,4}\\s+be\\s+equal\\s+to\\s+", "\\s+must\\s+be\\s+equal\\s+to\\s+"))
def one(job):
    i, (name, pairs) = job; d = '/dev/shm/agent2-l2mut-%d-%d' % (os.getpid(), i); os.makedirs(d); t0 = time.time()
    try:
        s = open(os.path.join(HERE, 'after2.py')).read()
        for a, b in pairs:
            if s.count(a) != 1: return i, name, 'NOT PLANTED', 'the text to change was found %d times' % s.count(a), 0
            s = s.replace(a, b)
        s = s.replace("HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)", "HERE = %r; sys.path.insert(0, HERE)" % HERE)      # the copy still finds lantern.py
        open(os.path.join(d, 'after2.py'), 'w').write(s)
        try: r = subprocess.run(['nice', '-n', '19', PY, '-I', os.path.join(HERE, 'test2.py'), os.path.join(d, 'after2.py')], capture_output=True, text=True, timeout=600); rc, out = r.returncode, r.stdout
        except subprocess.TimeoutExpired: rc, out = -9, ''
        fails = [l[6:110] for l in out.split('\n') if l.startswith('FAIL')]; last = out.strip().split('\n')[-1] if out.strip() else 'no output (the tests stopped: ' + (r.stderr.strip().split('\n')[-1][:60] if rc != -9 else 'time') + ')'
        if not pairs: return i, name, 'control passed' if rc == 0 else 'CONTROL FAILED', last, time.time() - t0
        return i, name, 'noticed' if rc != 0 else 'PASSED', ('%d tests failed; first: %s' % (len(fails), fails[0]) if fails else last), time.time() - t0
    finally: shutil.rmtree(d, ignore_errors=True)
if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=WORKERS) as ex: res = list(ex.map(one, enumerate(M)))
    lines = ['%-9s %-78s %-15s %4.0f s   %s' % ('' if r[1] == 'control' else 'fault %d' % r[0], r[1], r[2], r[4], r[3]) for r in res]
    planted = [r for r in res if r[1] != 'control' and r[2] != 'NOT PLANTED']; noticed = [r for r in planted if r[2] == 'noticed']
    lines.append('%d faults planted, %d noticed, %d passed every test, %d could not be planted; the control %s' % (len(planted), len(noticed), len(planted) - len(noticed), sum(1 for r in res if r[2] == 'NOT PLANTED'), res[0][2]))
    open(os.path.join(HERE, 'mutants2.out'), 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
