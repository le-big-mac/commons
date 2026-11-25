"""fmutants.py: break cell2.c on purpose, one fault at a time, and run ftest.py on each broken copy. A fault the tests
do not notice is a hole in the tests. First a control: an unbroken copy, built and run by the very same steps, must
pass, or "caught" would mean nothing.     python -I fmutants.py
"""
import os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.join(HERE, 'mutants')
M = [
 ('turn-reversed-in-64-bits', "i64 v = d1 * (e2 + d2 * d2) - (e1 + d1 * d1) * d2;\n        return (v > 0) - (v < 0);", "i64 v = d1 * (e2 + d2 * d2) - (e1 + d1 * d1) * d2;\n        return (v < 0) - (v > 0);"),
 ('turn-reversed-in-128-bits', "(wide)d2;\n        return (v > 0) - (v < 0);", "(wide)d2;\n        return (v < 0) - (v > 0);"),
 ('no-lift-in-64-bits', "i64 v = d1 * (e2 + d2 * d2) - (e1 + d1 * d1) * d2;", "i64 v = d1 * e2 - e1 * d2;"),
 ('no-lift-in-128-bits', "wide v = (wide)d1 * ((wide)e2 + (wide)d2 * d2) - ((wide)e1 + (wide)d1 * d1) * (wide)d2;", "wide v = (wide)d1 * (wide)e2 - (wide)e1 * (wide)d2;"),
 ('64-bit-path-used-where-it-overflows', "if (d1 > -1048576 && d1 < 1048576 && d2 > -1048576 && d2 < 1048576 &&", "if (d1 > -1048576000 && d1 < 1048576000 && d2 > -1048576000 && d2 < 1048576000 &&"),
 ('hull-pops-once', "while (k >= 2 && turn(P[h[k - 2]], P[h[k - 1]], P[i]) <= 0) k--;", "if (k >= 2 && turn(P[h[k - 2]], P[h[k - 1]], P[i]) <= 0) k--;"),
 ('same-x-rule-dropped', "if (k >= 1 && P[h[k - 1]].x == P[i].x) { if (P[i].y >= P[h[k - 1]].y) continue; k--; }", ""),
 ('gaps-of-mean-one', "q->ylast += (i64)(-log(u) / wreal * 2097152.0);", "q->ylast += (i64)(-log(u) * 2097152.0);"),
 ('gaps-even-not-random', "q->ylast += (i64)(-log(u) / wreal * 2097152.0);", "q->ylast += (i64)(2 * u / wreal * 2097152.0);"),
 ('x-in-half-the-column', "(i64)(((nextc(q) >> 32) * (uint64_t)wu) >> 32);", "(i64)(((nextc(q) >> 32) * (uint64_t)wu) >> 33);"),
 ('x-not-offset-by-column', "r.x = (i64)c * wu + (i64)(", "r.x = (i64)("),
 ('all-columns-one-stream', "b = (uint64_t)c * 0xD6E8FEB86659FD93ULL + 0x2545F4914F6CDD1DULL;", "b = 0x2545F4914F6CDD1DULL;"),
 ('seed-ignored', "else { uint64_t a = seed, b =", "else { uint64_t a = 0 * seed, b ="),
 ('old-seeding-all-columns-one-stream', "if (seeding == 1) z = seed * 0x100000001B3ULL + (uint64_t)c * 0x9E3779B97F4A7C15ULL + 12345;", "if (seeding == 1) z = seed * 0x100000001B3ULL + 12345;"),
 ('old-seeding-is-the-new', "if (seeding == 1) z = seed", "if (0) z = seed"),
 ('hand-points-given-back-in-sorted-order', "for (j = 0; j < nF; j++) out[F[j].seq] = F[j].depth;", "for (j = 0; j < nF; j++) out[j] = F[j].depth;"),
 ('floor-ignored', "if (floorL == 0 || (double)r.y >=", "if (1 || (double)r.y >="),
 ('floor-ripple-twice-as-long', "(double)r.x / (floorL * 1024.0)))) break;", "(double)r.x / (floorL * 2048.0)))) break;"),
 ('floor-a-sine', "(1.0 + cos(6.283185307179586 * (double)r.x", "(1.0 + sin(6.283185307179586 * (double)r.x"),
 ('floor-half-as-high', "(double)r.y >= floorA * 2097152.0 *", "(double)r.y >= floorA * 1048576.0 *"),
 ('floor-wavelength-not-checked', "if (floorL > 0 && fabs(", "if (0 && fabs("),
 ('slabs-of-the-band-above', "long idx = (long)snapOf[b] * C + c; snapSum[idx] += layer; snapCnt[idx]++; }", "long idx = (long)snapOf[b] * C + c; snapSum[idx] += layer + 1; snapCnt[idx]++; }"),
 ('slabs-in-the-next-column', "long idx = (long)snapOf[b] * C + c; snapSum[idx]", "long idx = (long)snapOf[b] * C + (c + 1) % C; snapSum[idx]"),
 ('slabs-three-thick', "for (b = hk; b < hk + 4; b++) snapOf[b] = nSnap;", "for (b = hk; b < hk + 3; b++) snapOf[b] = nSnap;"),
 ('slabs-may-overlap', "            if (hk + 4 > prev) continue;                       /* would overlap the slab above */\n", ""),
 ('slabs-sums-not-means', "snapSum[j] = snapCnt[j] ? snapSum[j] / snapCnt[j] : NAN;", "snapSum[j] = snapCnt[j] ? snapSum[j] : NAN;"),
 ('empty-columns-written-as-nought', "snapSum[j] = snapCnt[j] ? snapSum[j] / snapCnt[j] : NAN;", "snapSum[j] = snapCnt[j] ? snapSum[j] / snapCnt[j] : 0;"),
 ('top-slab-not-at-the-top', "int hk = (int)floor((HM - 4) * pow(2.0, -k / 8.0) + 0.5);", "int hk = (int)floor((HM - 8) * pow(2.0, -k / 8.0) + 0.5);"),
 ('compaction-loses-count', "q->seq0 += q->head; q->size -= q->head; q->head = 0;", "q->size -= q->head; q->head = 0;"),
 ('compaction-shifts-one-too-far', "memmove(q->p, q->p + q->head, sizeof(pt) * (q->size - q->head));", "memmove(q->p, q->p + q->head + 1, sizeof(pt) * (q->size - q->head - 1));"),
 ('band-half-as-high', "i64 b = y >> 21;", "i64 b = y >> 20;"),
 ('squares-not-summed', "bdd[b] += (double)layer * layer;", "bdd[b] += layer;"),
 ('depth-one-too-many', "record(cc[o], q->seq0 + ci[o], q->p[ci[o]].y, layer); }", "record(cc[o], q->seq0 + ci[o], q->p[ci[o]].y, layer + 1); }"),
 ('bound-at-the-left-end-of-a-column-only', "                y = (double)u.y + m * (b - u.x) + (b - u.x) * ((double)v.x - b); if (y > bound2[j]) bound2[j] = y;\n", ""),
 ('bound-without-the-parabola', "y = (double)u.y + m * (a - u.x) + (a - u.x) * ((double)v.x - a); if (y > bound2[j]) bound2[j] = y;", "y = (double)u.y + m * (a - u.x); if (y > bound2[j]) bound2[j] = y;"),
 ('margin-none', "(double)wu * (double)wu / 4.0 + 8.0;", "0.0;"),
 ('margin-half', "(double)wu * (double)wu / 4.0 + 8.0;", "(double)wu * (double)wu / 8.0;"),
 ('bound-taken-from-the-end-copy', "bound2[c >= C / 2 ? c : c + C]", "bound2[c]"),
 ('middle-stretch-rule-dropped-in-the-streaming', "if (v.x >= WU / 2 && v.x < WU / 2 + WU) {          /* the copy in the middle stretch speaks for the point */", "if (1) {"),
 ('first-copy-speaks-in-the-streaming', "if (v.x >= WU / 2 && v.x < WU / 2 + WU) {          /* the copy in the middle stretch speaks for the point */", "if (v.x >= 0 && v.x < WU) {"),
 ('middle-stretch-rule-dropped-in-the-plain-way', "if (!periodic || (v.x >= WU / 2 && v.x < WU / 2 + WU)) F[cur[o]].depth = layer;", "if (1) F[cur[o]].depth = layer;"),
 ('stops-at-half-the-height', "if (lowest > HMU) break;", "if (lowest > HMU / 2) break;"),
 ('plain-way-stops-at-half-the-height', "if (F[cur[i]].p.y <= until) { any = 1; break; }", "if (F[cur[i]].p.y <= until / 2) { any = 1; break; }"),
 ('second-copy-of-the-lowest-not-moved-along', "S0[c + C] = S0[c]; S0[c + C].x += WU;", "S0[c + C] = S0[c];"),
 ('second-copy-of-the-candidates-not-moved-along', "cand[mc + i] = cand[i]; cand[mc + i].x += WU;", "cand[mc + i] = cand[i];"),
 ('candidates-not-put-in-order-within-a-column', "if (mc - from > 1) {", "if (0) {"),
 ('removed-points-come-back-as-candidates', "if (!q->gone[i]) {\n                    if (mc == capC)", "if (1) {\n                    if (mc == capC)"),
 ('lowest-of-a-column-may-be-a-removed-point', "while (q->head < q->size && q->gone[q->head]) q->head++;", ""),
 ('slope-over-all-heights', "for (b = (int)(HM / 2); b < NB - 1; b++) {", "for (b = 0; b < NB - 1; b++) {"),
 ('slope-formula-wrong', "(syd - sy * sdp / n) / (syy - sy * sy / n)", "(syd - sy * sdp / n) / syy"),
 ('variance-is-the-mean-square', "bdd[b] / bn[b] - mu * mu);", "bdd[b] / bn[b]);"),
 ('profile-drops-the-first-band', "for (b = 0; b < NB - 1; b++) if (bn[b] > 1)", "for (b = 1; b < NB - 1; b++) if (bn[b] > 1)"),
 ('shear-not-applied', ": shear * F[j].p.x; if (F[j].p.y != y0) moved++; }", ": 0 * shear * F[j].p.x; if (F[j].p.y != y0) moved++; }"),
 ('shear-comparison-blind', "for (j = 0; j < nF; j++) if (d1[j] != F[j].depth) differ++;", "for (j = 0; j < nF; j++) if (0) differ++;"),
 ('bend-is-only-a-shear', "doBend ? (i64)(((wide)shear * F[j].p.x * F[j].p.x) / 2048) : shear * F[j].p.x;", "doBend ? shear * F[j].p.x : shear * F[j].p.x;"),
 ('check-comparison-blind', "if (F[j].seq >= dlogCap || dlog[(long)F[j].c * dlogCap + F[j].seq] != F[j].depth) differ++; }", "if (0) differ++; }"),
 ('check-looks-at-the-lower-half-only', "for (j = 0; j < nF; j++) if (F[j].p.y <= HMU) { compared++;", "for (j = 0; j < nF; j++) if (F[j].p.y <= HMU / 2) { compared++;"),
 ('height-in-the-wrong-units', "i64 HMU = (i64)(HM * 2097152.0);", "i64 HMU = (i64)(HM * 1048576.0);"),
 ('period-one-column-too-long', "WU = (i64)C * wu;", "WU = (i64)C * wu + wu;"),
 ('margin-option-ignored', "double margin = marginSet ? marginGiven * 2097152.0 : (double)wu", "double margin = 0 ? marginGiven * 2097152.0 : (double)wu"),
 ('no-stop-when-a-layer-takes-nothing', "if (!took) { fprintf(stderr,", "if (0) { fprintf(stderr,"),
]
def build(name, old, new):
    d = os.path.join(WORK, name); os.makedirs(d, exist_ok=True)
    s = open(os.path.join(HERE, 'cell2.c'), encoding='utf-8').read()
    if old is not None:
        if s.count(old) != 1: raise SystemExit('mutant %s: pattern found %d times' % (name, s.count(old)))
        s = s.replace(old, new)
    open(os.path.join(d, 'cell2.c'), 'w', encoding='utf-8').write(s)
    r = subprocess.run(['gcc', '-O2', '-o', os.path.join(d, 'cell2'), os.path.join(d, 'cell2.c'), '-lm'], capture_output=True, text=True)
    if r.returncode: raise SystemExit('mutant %s does not compile: %s' % (name, r.stderr[:300]))
    return d
def run(d):
    env = dict(os.environ, CELL2=os.path.join(d, 'cell2'))
    try: r = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'ftest.py')], capture_output=True, text=True, timeout=600, env=env)
    except subprocess.TimeoutExpired:
        subprocess.run(['pkill', '-f', '^' + d + '/'])
        return 1, ['TIMEOUT']
    return r.returncode, [l for l in r.stdout.split('\n') if l.startswith('FAIL')] + ([r.stderr.strip().split('\n')[-1][:150]] if r.returncode and r.stderr.strip() and 'FAIL' not in r.stdout else [])
if os.path.isdir(WORK): shutil.rmtree(WORK)
code, fails = run(build('CONTROL', None, None))
print('control (nothing broken): %s' % ('passes' if code == 0 else 'FAILS: ' + '; '.join(fails)))
if code != 0: sys.exit('the control does not pass; nothing below would mean anything')
dirs = [(name, build(name, old, new)) for name, old, new in M]
with ThreadPoolExecutor(max_workers=int(os.environ.get('WORKERS', '4'))) as ex: out = list(ex.map(lambda nd: (nd[0],) + run(nd[1]), dirs))
caught = 0; passed = []
for name, code, fails in out:
    if code != 0: caught += 1; print('caught   %-48s by %d: %s' % (name, len(fails), (fails[0] if fails else '')[:110]))
    else: passed.append(name); print('PASSED   %s' % name)
print('\n%d of %d broken copies caught; passed: %s' % (caught, len(M), ', '.join(passed) or 'none'))
shutil.rmtree(WORK)
