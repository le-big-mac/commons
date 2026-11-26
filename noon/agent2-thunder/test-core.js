// tests of core.js that could fail: closed forms worked by hand, and the same sum done as a string of points
const TH = require('./core.js');
let n = 0, bad = 0;
function must(ok, what, detail) { n++; if (!ok) bad++; console.log((ok ? 'ok   ' : 'FAIL ') + what + (detail ? '   [' + detail + ']' : '')); }
const { C, T, FS, LEAD } = TH; const L0 = Math.round(LEAD * FS);

// 1. an arc about the listener: one N of height (length of arc) / radius
{
  const R = 2000, pts = TH.arc(0, 0, R, 20, 50), m = TH.measure(pts), res = TH.thunder(pts, [0, 0], { air: 0, bend: 0 });
  const want = m.length / R; let worst = 0;
  for (let i = 2; i < Math.floor(T * FS) - 2; i++) { const u = (i / FS) / T; worst = Math.max(worst, Math.abs(res.dry[L0 + i] - want * (1 - 2 * u))); }
  must(res.nearest > R - 0.001 && res.farthest < R + 1e-9 && res.last - res.first < T + 1e-5, 'arc about the listener: every point of it is the radius away, to within the bow of a 3 m chord', (R - res.nearest).toExponential(2) + ' m');
  must(worst < 2e-3 * want, 'arc about the listener: the sound is one N of height length/radius', 'height ' + want.toFixed(5) + ', worst departure ' + worst.toExponential(2));
  let after = 0; for (let i = L0 + Math.ceil(T * FS) + 2; i < res.dry.length; i++) after = Math.max(after, Math.abs(res.dry[i]));
  let before = 0; for (let i = 0; i < L0 - 2; i++) before = Math.max(before, Math.abs(res.dry[i]));
  must(after === 0 && before === 0, 'arc about the listener: nothing before the N or after it', before + ', ' + after);
}
// 2. a long straight stroke square-on at its middle: the peak is (2/3) sqrt(2 c T / D), a quarter of T after the first sound
for (const D of [500, 1000, 4000]) {
  const pts = TH.resample([[0, -3000], [0, 3000]], 3), res = TH.thunder(pts, [D, 0], { air: 0, bend: 0 });
  const want = 2 / 3 * Math.sqrt(2 * C * T / D); let pk = 0, ipk = 0;
  for (let i = 0; i < res.dry.length; i++) if (res.dry[i] > pk) { pk = res.dry[i]; ipk = i; }
  must(Math.abs(pk / want - 1) < 0.01, 'straight stroke, listener ' + D + ' m from its middle: peak (2/3) sqrt(2cT/D)', 'want ' + want.toFixed(5) + ', got ' + pk.toFixed(5));
  must(Math.abs((ipk - L0) / FS - T / 4) < 0.0002, '   ... a quarter of a pulse length after the first sound', ((ipk - L0) / FS * 1000).toFixed(3) + ' ms against ' + (T / 4 * 1000).toFixed(3));
}
// 3. a straight piece pointing at the listener: two humps, at its two ends, and next to nothing between
{
  const pts = TH.resample([[1000, 0], [3000, 0]], 3), res = TH.thunder(pts, [0, 0], { air: 0, bend: 0 });
  const iT = L0 + Math.ceil(T * FS), end = L0 + Math.round((2000 / C) * FS); let first = 0, mid = 0, last = 0;
  for (let i = 0; i < res.dry.length; i++) { const a = Math.abs(res.dry[i]); if (i <= iT) first = Math.max(first, a); else if (i < end - 2) mid = Math.max(mid, a); else last = Math.max(last, a); }
  // between the ends the true sum is about (T/t)^2 / 6 of a unit, and the pieces, each given one distance, make it a row of humps T c l / (4 r^2) high
  const lump = T * C * 3 / (4 * 1000 * 1000);
  must(first > 0 && last > 0 && mid < 1.05 * lump && mid < 1e-2 * first, 'a straight piece end-on: a hump at each end and next to nothing between', 'ends ' + first.toExponential(3) + ', ' + last.toExponential(3) + '; between at most ' + mid.toExponential(2) + ' (the pieces\' own lumpiness allows ' + lump.toExponential(2) + ')');
  const want = T * C / 1000 * 0.25;                       // the near hump: (T c / r) M, M at most 1/4
  must(Math.abs(first / want - 1) < 0.01, '   ... the near hump is (T c / r) / 4 high', 'want ' + want.toExponential(4) + ', got ' + first.toExponential(4));
}
// 4. a made-up stroke: against the same sum done as a string of points; first and last sound; no net pressure
{
  const pts = TH.stroke(7), L = [2500, 0], res = TH.thunder(pts, L, { air: 0, bend: 0 }), slow = TH.pearls(pts, L, 300, { bend: 0 });
  let worst = 0, pk = 0, sum = 0, firstNon = -1, lastNon = -1, dot = 0, aa = 0, bb = 0;
  for (let i = 0; i < res.dry.length; i++) {
    worst = Math.max(worst, Math.abs(res.dry[i] - slow.p[i])); pk = Math.max(pk, Math.abs(res.dry[i])); sum += res.dry[i];
    dot += res.dry[i] * slow.p[i]; aa += res.dry[i] * res.dry[i]; bb += slow.p[i] * slow.p[i];
    if (res.dry[i] !== 0) { if (firstNon < 0) firstNon = i; lastNon = i; }
  }
  must(dot / Math.sqrt(aa * bb) > 0.999, 'made-up stroke: the exact sum against a string of 300 points a piece, correlation', (dot / Math.sqrt(aa * bb)).toFixed(6));
  must(worst < 0.03 * pk, '   ... and never further apart than 3% of the peak', (worst / pk).toFixed(4));
  must(Math.abs(firstNon - L0) <= 2, 'the first sound comes when the nearest point has had time to arrive', 'sample ' + firstNon + ' with a lead of ' + L0);
  must(Math.abs(res.first - res.nearest / C) < 1e-12 && Math.abs(res.t0 + L0 / FS - res.first) < 1 / FS, 'the times reported are those of the nearest point', res.first.toFixed(4) + ' s');
  const wantLast = L0 + ((res.farthest - res.nearest) / C + T) * FS;
  must(Math.abs(lastNon - wantLast) <= 2, 'the last sound: the farthest point, plus one pulse length', lastNon + ' against ' + wantLast.toFixed(1));
  // every pulse has as much below nought as above, and each sample is a mean over its own time, so the whole adds up to nothing
  must(Math.abs(sum) < 1e-9 * pk * res.dry.length, 'the pressure adds up to nothing over the whole', 'total ' + (sum / pk).toExponential(2) + ' peaks over ' + res.dry.length + ' samples');
  const d = TH.distances(pts, L); let lo = Infinity, hi = 0;
  for (const q of pts) { const r = Math.hypot(q[0] - L[0], q[1] - L[1]); lo = Math.min(lo, r); hi = Math.max(hi, r); }
  must(Math.abs(d.nearest - lo) < 1e-9 && Math.abs(d.farthest - hi) < 1e-9, 'nearest and farthest points', lo.toFixed(1) + ', ' + hi.toFixed(1));
}
// 5. the made-up strokes: crookedness near 16 degrees, pieces of 3 m, top to ground
{
  const ks = [], lens = []; let piece = 0, ends = true;
  for (let s = 1; s <= 20; s++) {
    const pts = TH.stroke(s), m = TH.measure(pts); ks.push(m.kink); lens.push(m.length);
    for (let i = 1; i < pts.length - 1; i++) piece = Math.max(piece, Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
    ends = ends && Math.abs(pts[0][1] - 5000) < 1e-6 && Math.abs(pts[pts.length - 1][1]) < 1e-6 && Math.abs(pts[pts.length - 1][0]) < 1e-6;
  }
  const mean = ks.reduce((a, b) => a + b) / ks.length;
  must(Math.abs(mean - 16) < 1, 'twenty made-up strokes: mean change of direction between neighbouring pieces near 16 degrees', mean.toFixed(2) + ' (from ' + Math.min(...ks).toFixed(1) + ' to ' + Math.max(...ks).toFixed(1) + ')');
  must(ends, 'each begins 5,000 m up and ends on the ground at x = 0');
  must(piece < 3.6 && piece > 2.6, 'the longest piece of the twenty is near 3 m', piece.toFixed(3));
  const ml = lens.reduce((a, b) => a + b) / lens.length;
  must(ml > 6500 && ml < 7100, 'the twenty are on average a third or so longer than the 5 km they span (their wander has a memory)', 'mean ' + ml.toFixed(0) + ' m, from ' + Math.min(...lens).toFixed(0) + ' to ' + Math.max(...lens).toFixed(0));
}
// 6. the air: a blur that keeps the total and dulls a far clap more than a near one
{
  const out = [];
  for (const R of [500, 8000]) {
    const pts = TH.arc(0, 0, R, 30, 30 + 300 / R * 180 / Math.PI), a = TH.thunder(pts, [0, 0], { air: 0, bend: 0 }), b = TH.thunder(pts, [0, 0], { bend: 0 });
    let sa = 0, sd = 0, sb = 0; for (let i = 0; i < a.p.length; i++) { sa += Math.abs(a.p[i]); sd += a.p[i]; sb += b.p[i]; }
    out.push(b.peak / a.peak);
    must(Math.abs(sd) < 1e-9 * sa, 'a clap from ' + R + ' m: the pressure adds up to nothing', sd.toExponential(2) + ' beside ' + sa.toFixed(1));
    must(Math.abs(sb - sd) < 1e-9 * sa, '   ... and the air neither adds nor takes away', (sb - sd).toExponential(2));
  }
  must(out[0] > out[1] && out[0] <= 1 && out[1] > 0.2, 'the air takes more off the peak of a far clap than a near one', out.map(x => x.toFixed(3)).join(' and '));
}
// 7. the air's blur is as wide as stated.  A step put through it rises from a tenth to nine tenths of its height in 2.626 standard
//    deviations (three running means: the sum of three evenly spread numbers), and the standard deviation is AIR x sqrt(km travelled)
{
  const rise = R => { const i0 = Math.round(R / C * FS), p = new Float64Array(i0 + 400); for (let i = i0; i < p.length; i++) p[i] = 1;
    const q = TH.blur(p, 0, TH.AIR), cross = f => { for (let i = i0 - 300; i < i0 + 300; i++) if (q[i] >= f) return i - 1 + (f - q[i - 1]) / (q[i] - q[i - 1]); };
    return (cross(0.9) - cross(0.1)) / FS; };
  const r1 = rise(2000), r4 = rise(8000), want = 2.626 * TH.AIR * Math.sqrt(2);
  must(Math.abs(r1 / want - 1) < 0.03, 'the air at 2 km blurs a step over 2.626 x 0.17 ms x sqrt(2)', (r1 * 1000).toFixed(4) + ' ms against ' + (want * 1000).toFixed(4));
  must(Math.abs(r4 / r1 - 2) < 0.03, '   ... and twice as much at four times the distance', (r4 / r1).toFixed(3));
}
// 8. close in, against points each with its own distance: the pieces are cut finer there, and the peak holds
for (const x of [2, 10, 50, 500]) {
  const pts = TH.stroke(3), a = TH.thunder(pts, [x, 0], { air: 0, bend: 0 }), b = TH.pearls(pts, [x, 0], 400, { bend: 0 }); let pk = 0, pb = 0, worst = 0;
  for (let i = 0; i < a.dry.length; i++) { pk = Math.max(pk, Math.abs(a.dry[i])); pb = Math.max(pb, Math.abs(b.p[i])); worst = Math.max(worst, Math.abs(a.dry[i] - b.p[i])); }
  must(Math.abs(pk / pb - 1) < 0.01 && worst < 0.05 * pk && (x > 100 || a.cut > 100), 'listener ' + x + ' m from the foot of a stroke: the peak within 1% of a sum over points, no sample further off than 5% of it', pk.toFixed(4) + ' against ' + pb.toFixed(4) + '; worst ' + (100 * worst / pk).toFixed(1) + '%; ' + a.cut + ' cuts');
}
// 9. the bending of sound: what is hidden, and that the exact sum and the points agree about it
{
  const edge = 3000 * 3000 / (2 * TH.BEND);
  must(Math.abs(edge - 81.8) < 0.1 && TH.shade(3000, edge, TH.BEND) === 1 && TH.shade(3000, 0, TH.BEND) === 0 && Math.abs(TH.shade(3000, edge / 2, TH.BEND) - 0.5) < 1e-12 && TH.shade(3000, 10, 0) === 1,
       'from 3 km the lowest 82 m of a stroke are in the shadow: nothing at the ground, half at half that height, all above it', edge.toFixed(1) + ' m');
  const pts = TH.resample([[0, 5000], [0, 0]], 3), open = TH.thunder(pts, [3000, 0], { air: 0, bend: 0 }), bent = TH.thunder(pts, [3000, 0], { air: 0 }), slow = TH.pearls(pts, [3000, 0], 300);
  let pb = 0, ps = 0, worst = 0; for (let i = 0; i < bent.dry.length; i++) { pb = Math.max(pb, Math.abs(bent.dry[i])); ps = Math.max(ps, Math.abs(slow.p[i])); worst = Math.max(worst, Math.abs(bent.dry[i] - slow.p[i])); }
  let po = 0; for (let i = 0; i < open.dry.length; i++) po = Math.max(po, Math.abs(open.dry[i]));
  must(pb < 0.75 * po && pb > 0.1 * po, 'a straight stroke from 3 km: the bending takes a good part of the first crack, which comes from the foot', 'peak ' + po.toFixed(5) + ' without, ' + pb.toFixed(5) + ' with');
  must(Math.abs(pb / ps - 1) < 0.02 && worst < 0.05 * pb, '   ... and the exact sum agrees with a sum over points about how much', pb.toFixed(5) + ' against ' + ps.toFixed(5) + '; worst sample ' + (100 * worst / pb).toFixed(1) + '%');
  const hid = bent.hidden; let low = 0, high = 0; for (let i = 0; i < pts.length; i++) { if (pts[i][1] < 40 && hid[i] < 0.5) low++; if (pts[i][1] > 82 && hid[i] === 1) high++; }
  must(low >= 13 && high === pts.filter(q => q[1] > 82).length, 'the page is told which points are hidden', low + ' low points more than half hidden');
  const lowLine = TH.resample([[6000, 20], [9000, 60]], 3), dark = TH.thunder(lowLine, [0, 0]);
  must(bent.firstHeard > bent.first && bent.firstHeard < bent.first + 0.01 && open.firstHeard === open.first && dark.firstHeard === null && dark.peak < 2e-5 && dark.peak > 0,
       'the first sound that can be heard: a little after the nearest point from 3 km, the nearest point itself without the bending, and none to speak of from a low line 6 km off', ((bent.firstHeard - bent.first) * 1000).toFixed(1) + ' ms later; the low line peaks at ' + dark.peak.toExponential(2));
}
// 10. the crookedness at larger scales (stated in the README)
{
  let t30 = 0, t300 = 0; for (let k = 1; k <= 20; k++) { t30 += TH.turnAt(TH.stroke(k), 30) / 20; t300 += TH.turnAt(TH.stroke(k), 300) / 20; }
  must(t30 > 24 && t30 < 28 && t300 > 17 && t300 < 22, 'the made-up strokes turn about 26 degrees between 30 m chords and about 19 between 300 m chords', t30.toFixed(1) + ' and ' + t300.toFixed(1));
}
// 11. the numbers the page states
must(C === 343 && T === 0.005 && TH.STEP === 3 && TH.KINK === 16 && FS === 44100 && TH.AIR === 0.00017 && TH.BEND === 55000, 'the stated constants: 343 m/s, 5 ms, 3 m, 16 degrees, 44,100 samples a second, 0.17 ms of blur a kilometre, rays curving on 55 km');
console.log('CORE TEST: ' + n + ' assertions, ' + bad + ' failed');
process.exit(bad ? 1 : 0);
