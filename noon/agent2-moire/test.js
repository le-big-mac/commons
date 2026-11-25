// test.js -- what the geometry of core.js must do.   usage: node test.js > test.out
const { Cloth, rng32 } = require('./core.js');
const rnd = rng32(20261123);          // the same points every time, so that test.out can be made again
let ok = 0, bad = 0;
const check = (name, cond, detail) => { cond ? ok++ : bad++; console.log((cond ? 'PASS  ' : 'FAIL  ') + name + (detail !== undefined ? '   ' + detail : '')); };
const seeds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
// 1. with no slip the fold line is rib on rib all the way along
let worst = 1;
for (const s of seeds) { const c = new Cloth({ seed: s }); for (let k = 0; k < 200; k++) worst = Math.min(worst, c.flat(c.W / 2, k / 200 * c.L)); }
check('with no slip, the fold line is flattened along its whole length (10 cloths, 200 points each)', worst > 1 - 1e-9, 'least ' + worst.toFixed(12));
// 2. with no slip the unfolded mark is the same on both sides of the fold
let d = 0;
for (const s of seeds) { const c = new Cloth({ seed: s }); for (let k = 0; k < 2000; k++) { const X = rnd() * c.W, Y = rnd() * c.L; d = Math.max(d, Math.abs(c.mark(X, Y) - c.mark(c.W - X, Y))); } }
check('with no slip, the unfolded mark is a mirror image about the fold (20,000 points)', d < 1e-9, 'greatest difference ' + d.toExponential(1));
// 3. slipped along the cloth by a third of a rib the two halves still carry one mark, a third of a rib apart: the unfolded
//    cloth stays a mirror image to within the width of a band's edge.  Slipped across by a twentieth of the width, the
//    mirror line is no longer the fold: the control for test 2.
d = 0; let dx = 0;
for (const s of seeds) { const c = new Cloth({ seed: s, slipY: 1 / 3 }), e = new Cloth({ seed: s, slipX: 0.05 });
  for (let k = 0; k < 2000; k++) { const X = rnd() * c.W, Y = rnd() * c.L; d = Math.max(d, Math.abs(c.mark(X, Y) - c.mark(c.W - X, Y))); dx = Math.max(dx, Math.abs(e.mark(X, Y) - e.mark(e.W - X, Y))); } }
check('slipped along by a third of a rib, the unfolded mark is still nearly a mirror image; slipped across by a twentieth of the width it is not (the control)', d < 0.15 && dx > 0.9, 'greatest differences ' + d.toFixed(2) + ' and ' + dx.toFixed(2));
// 4. a perfectly straight weft gives no watering at all, whatever the slip
{ const c = new Cloth({ bow: 0, skew: 0, wander: 0, slipY: 0.37 }); const f = c.field(60, 40); let lo = 1, hi = 0; for (const v of f) { lo = Math.min(lo, v); hi = Math.max(hi, v); }
  check('a cloth with perfectly straight wefts takes an even mark and no watering', hi - lo < 1e-9, 'range ' + (hi - lo).toExponential(1)); }
// 5. bow alone: the lag at the selvedge is twice the bow less nothing, so across one half there are 2 x bow bands... count them
for (const bow of [2, 4, 7]) { const c = new Cloth({ bow, skew: 0, wander: 0 }); const lagEdge = c.lag(0, 0.1), n = c.bands(0.1, 4000);
  check('bow of ' + bow + ' ribs and nothing else: the two halves are in step at the fold and in step again at the selvedge (lag ' + lagEdge.toFixed(3) + '), with no band between', Math.abs(lagEdge) < 1e-9 && n === 0, 'bands ' + n); }
// 6. skew alone: the lag grows evenly from the fold to the selvedge, to the whole skew; bands = skew
for (const skew of [1, 3, 6]) { const c = new Cloth({ bow: 0, skew, wander: 0 }); const lagEdge = c.lag(0, 0.1), n = c.bands(0.1, 4000);
  check('skew of ' + skew + ' ribs and nothing else: lag at the selvedge ' + lagEdge.toFixed(3) + ' ribs, ' + n + ' bands across the half', Math.abs(Math.abs(lagEdge) - skew) < 1e-9 && n === skew, ''); }
// 7. the watering magnifies a slip: with a skew of 3 ribs and nothing else, a slip of a tenth of a rib moves every band
//    across the cloth by W / (2 x 3) / 10, which is 5 ribs' worth
{ const where = c => { const xs = []; let prev = null; for (let i = 0; i <= 200000; i++) { const x = i / 200000 * c.W / 2, s = c.flat(x, 0.1) > 0.5; if (prev !== null && s !== prev) xs.push(x); prev = s; } return xs; };
  const a = where(new Cloth({ bow: 0, skew: 3, wander: 0 })), b = where(new Cloth({ bow: 0, skew: 3, wander: 0, slipY: 0.1 }));
  const moved = a.length === b.length ? a.map((x, k) => Math.abs(b[k] - x) * 300) : [];
  check('a slip of a tenth of a rib moves each band by 5 ribs across the cloth (skew 3): fifty times the slip', moved.length === 6 && moved.every(m => Math.abs(m - 5) < 0.01), 'moved, in ribs: ' + moved.map(m => m.toFixed(2)).join(', ')); }
// 7b. two pieces, one turned over on the other.  Alike in bow, with no skew or wander: no watering.  Bows unlike by d ribs:
//     the pieces are in step at both selvedges and d ribs apart along the middle, so d bands lie on either side of the
//     midline, and the lag is at its greatest there (which a cloth folded on itself can never show at its fold)
{ const same = new Cloth({ two: true, bow: 3, bow2: 3, skew: 0, wander: 0 }); const f = same.field(60, 40); let lo = 1, hi = 0; for (const v of f) { lo = Math.min(lo, v); hi = Math.max(hi, v); }
  check('two pieces with the same bow and straight otherwise take no watering', hi - lo < 1e-9, 'range ' + (hi - lo).toExponential(1));
  for (const d of [2, 5]) { const c = new Cloth({ two: true, bow: 1 + d, bow2: 1, skew: 0, wander: 0 });
    const mid = c.lag(c.W / 2, 0.1), near = c.lag(c.W / 2 - 0.001, 0.1), far = c.lag(c.W / 2 + 0.001, 0.1), n = c.bands(0.1, 4000);
    check('two pieces with bows ' + d + ' ribs unlike: ' + n + ' bands from selvedge to midline, the lag greatest at the midline (' + mid.toFixed(3) + ' ribs)', n === d && Math.abs(Math.abs(mid) - d) < 1e-9 && Math.abs(near) < Math.abs(mid) && Math.abs(far) < Math.abs(mid) && Math.abs(near - far) < 1e-9, ''); }
  const fold = new Cloth({ bow: 6, skew: 2, wander: 0 }), a = fold.lag(fold.W / 2, 0.1), b = fold.lag(fold.W / 2 - 0.001, 0.1), e = fold.lag(fold.W / 2 + 0.001, 0.1);
  check('a cloth folded on itself: at the fold the lag is nought and passes through it, so no ring can be centred on the fold', Math.abs(a) < 1e-12 && b * e < 0, 'lag just either side: ' + b.toFixed(4) + ', ' + e.toFixed(4));
  let d2 = 0; const two = new Cloth({ two: true, seed: 4 }); for (let k = 0; k < 2000; k++) { const X = rnd() * two.W, Y = rnd() * two.L; d2 = Math.max(d2, Math.abs(two.mark(X, Y) - two.mark(two.W - X, Y))); }
  check('two pieces with unlike wander: the mark is not a mirror image about the midline', d2 > 0.9, 'greatest difference ' + d2.toFixed(2)); }
// 8. the wander has the size it is given
{ let s2 = 0, n = 0; for (const s of seeds) { const c = new Cloth({ seed: s, bow: 0, skew: 0, wander: 1 }); for (let k = 0; k < 20000; k++) { const v = c.u(rnd() * c.W, rnd() * 40 * c.W) / c.PITCH; s2 += v * v; n++; } }
  check('the wander has root mean square 1 rib when asked for 1 (10 cloths, over a long piece)', Math.abs(Math.sqrt(s2 / n) - 1) < 0.03, Math.sqrt(s2 / n).toFixed(3)); }
// 9. how many bands the default cloth shows across one half, at ten heights and for ten seeds
{ const counts = []; for (const s of seeds) { const c = new Cloth({ seed: s }); for (let k = 0; k < 10; k++) counts.push(c.bands((k + 0.5) / 10 * c.L, 4000)); }
  counts.sort((a, b) => a - b); console.log('NOTE  the default cloth (bow 3, skew 1.6, wander 1.4 ribs): bands across one half, 100 lines: least ' + counts[0] + ', median ' + counts[50] + ', greatest ' + counts[99]); }
console.log(ok + ' pass, ' + bad + ' fail'); process.exit(bad ? 1 : 0);
