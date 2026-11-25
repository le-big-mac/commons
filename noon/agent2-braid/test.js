// test.js -- checks of core.js that could fail.   usage: node test.js
const { Bed } = require('./core.js');
let pass = 0, fail = 0;
function check(name, ok, detail) { console.log((ok ? 'pass  ' : 'FAIL  ') + name + (detail ? '   [' + detail + ']' : '')); ok ? pass++ : fail++; }
const SET = { NX: 40, NY: 120, NOISE: 3, CS: 0.05, KL: 0.4 };
function rowSums(b) { const r = []; for (let j = 0; j < b.NY; j++) { let s = 0; for (let i = 0; i < b.NX; i++) s += b.Q[j * b.NX + i]; r.push(s); } return r; }

// 1. water: every row carries all of it, on a rough bed, with the narrow inflow and the wide one
for (const FEED of [0.25, 1]) {
  const b = new Bed(Object.assign({}, SET, { FEED })); for (let s = 0; s < 400; s++) b.step();
  const worst = Math.max(...rowSums(b).map(s => Math.abs(s - b.total)));
  check(`water: each of ${b.NY} rows carries the whole inflow (${b.total}), inflow over ${FEED} of the head`, worst < 1e-9 * b.total, `greatest shortfall ${worst.toExponential(1)}`);
}
// 2. no lakes: a dam five row-falls high right across the bed still lets all the water over, most of it over the lowest lip
{ const b = new Bed(Object.assign({}, SET, { FEED: 1, NOISE: 0 })); const j0 = 60;
  for (let i = 0; i < b.NX; i++) b.h[j0 * b.NX + i] += 5 * b.SLOPE; b.h[j0 * b.NX + 20] -= 2 * b.SLOPE;        // a notch in the dam
  b.step(true); const r = rowSums(b), worst = Math.max(...r.map(s => Math.abs(s - b.total)));
  let at = 0; for (let i = 0; i < b.NX; i++) if (b.Q[j0 * b.NX + i] > b.Q[j0 * b.NX + at]) at = i;
  const mean = b.total / b.NX;
  check('water: a dam across the whole bed holds none of it back', worst < 1e-9 * b.total, `greatest shortfall ${worst.toExponential(1)}`);
  check('water: more goes through a notch in the dam than over any other cell of it, but not all', at === 20 && b.Q[j0 * b.NX + 20] > 1.1 * mean && b.Q[j0 * b.NX + 20] < 3 * mean, `notch carries ${(b.Q[j0 * b.NX + 20] / mean).toFixed(2)} of a cell's share`);
  // the shares over the lip go as |S|^-0.5: the whole dam row summed again by hand from the row above it
  const R2 = Math.SQRT2, c = (j0 - 1) * b.NX + 19, s = [(b.h[c] - b.h[c + b.NX - 1]) / R2, b.h[c] - b.h[c + b.NX], (b.h[c] - b.h[c + b.NX + 1]) / R2];
  let hand = new Float64Array(b.NX); for (let i = 0; i < b.NX; i++) { const cc = (j0 - 1) * b.NX + i, q = b.Q[cc];
    const ss = [i > 0 ? (b.h[cc] - b.h[cc + b.NX - 1]) / R2 : NaN, b.h[cc] - b.h[cc + b.NX], i < b.NX - 1 ? (b.h[cc] - b.h[cc + b.NX + 1]) / R2 : NaN];
    const ww = ss.map(x => x === x ? 1 / Math.sqrt(Math.abs(x)) : 0), t = ww[0] + ww[1] + ww[2]; if (i > 0) hand[i - 1] += q * ww[0] / t; hand[i] += q * ww[1] / t; if (i < b.NX - 1) hand[i + 1] += q * ww[2] / t; }
  let d = 0; for (let i = 0; i < b.NX; i++) d = Math.max(d, Math.abs(hand[i] - b.Q[j0 * b.NX + i]));
  check('water: over an uphill lip the shares go as 1/sqrt(|slope|), the whole dam row summed by hand', d < 1e-9 && s.every(x => x < 0), `greatest difference ${d.toExponential(1)}; slopes at one cell ${s.map(x => (x / b.SLOPE).toFixed(2)).join(', ')} row-falls`);
}
// 3. water runs downhill: a valley cut two row-falls deep down the middle gathers nearly all of it
{ const b = new Bed(Object.assign({}, SET, { FEED: 1, NOISE: 0 }));
  for (let j = 1; j < b.NY - 1; j++) for (let i = 0; i < b.NX; i++) b.h[j * b.NX + i] += 1.5 * b.SLOPE * Math.abs(i - 20);     // a V from wall to wall
  b.step(true); let mid = 0; for (let i = 17; i <= 23; i++) mid += b.Q[100 * b.NX + i];
  check('water: a V-shaped valley from wall to wall gathers the river (the seven cells round its floor, at row 100)', mid > 0.99 * b.total, `${(100 * mid / b.total).toFixed(1)}% of the water, ${(100 * b.Q[100 * b.NX + 20] / b.total).toFixed(1)}% in the floor cell`);
  const c = new Bed(Object.assign({}, SET, { FEED: 1, NOISE: 0 })); c.step(true); let midc = 0; for (let i = 17; i <= 23; i++) midc += c.Q[100 * c.NX + i];
  check('   and on a smooth bed the same seven cells carry about their seven fortieths', Math.abs(midc / c.total - 7 / 40) < 0.02, `${(100 * midc / c.total).toFixed(1)}% against ${(100 * 7 / 40).toFixed(1)}%`);
}
// 4. sand: nothing made or lost.  What every cell gains, summed over the whole grid with the fixed rows counted, is zero
for (const KL of [0, 0.4]) {
  const b = new Bed(Object.assign({}, SET, { KL })); for (let s = 0; s < 300; s++) b.step();
  b.step(true); let sum = 0, abs = 0, inner = 0; for (let k = 0; k < b.dh.length; k++) { sum += b.dh[k]; abs += Math.abs(b.dh[k]); if (k >= b.NX && k < b.dh.length - b.NX) inner += b.dh[k]; }
  check(`sand: gains and losses over the whole grid cancel (sideways rule ${KL ? 'on' : 'off'})`, Math.abs(sum) < 1e-12 * abs, `sum ${sum.toExponential(1)} against ${abs.toExponential(1)} moved`);
  let head = 0; for (let i = 0; i < b.NX; i++) head += b.dh[i];
  check('   and the inner cells alone do not cancel: they gain what the head row sends and lose what the foot row takes', Math.abs(inner) > 1e-6 * abs && Math.abs(inner + head + b.gone) < 1e-12 * abs, `inner ${inner.toExponential(2)}, head ${head.toExponential(2)}, foot ${b.gone.toExponential(2)}`);
}
// 5. a step: the greatest change is LIMIT of a row's fall; the head and foot rows do not move
{ const b = new Bed(SET), before = Float64Array.from(b.h); b.step(); let big = 0, ends = 0;
  for (let k = 0; k < b.h.length; k++) { const d = Math.abs(b.h[k] - before[k]); if (k < b.NX || k >= b.h.length - b.NX) ends = Math.max(ends, d); else big = Math.max(big, d); }
  check('step: the greatest change of height is 0.03 of a row-fall', Math.abs(big / (b.LIMIT * b.SLOPE) - 1) < 1e-9 && b.LIMIT === 0.03, `${(big / b.SLOPE).toFixed(6)} row-falls`);
  for (let s = 0; s < 500; s++) b.step(); ends = 0; for (let i = 0; i < b.NX; i++) ends = Math.max(ends, Math.abs(b.h[i] - before[i]), Math.abs(b.h[b.h.length - 1 - i] - before[b.h.length - 1 - i]));
  check('step: after 500 steps the head and foot rows are where they began', ends === 0, `greatest change ${ends}`);
  const t0 = b.time; b.step(true); check('step: holding still changes neither the bed nor the clock', b.time === t0 && b.steps === 501);
}
// 6. the same seed gives the same river; another seed another
{ const a = new Bed(SET), b = new Bed(SET), c = new Bed(Object.assign({}, SET, { seed: 2 })); for (let s = 0; s < 800; s++) { a.step(); b.step(); c.step(); }
  check('seed: two beds from one seed are the same after 800 steps, bit for bit', a.hash() === b.hash(), a.hash());
  check('seed: a bed from another seed is not', a.hash() !== c.hash(), c.hash()); }
// 7. left and right are treated alike: a bed that is its own mirror image stays so; one that is not does not become so
{ function mirrorGap(b) { let d = 0; for (let j = 0; j < b.NY; j++) for (let i = 0; i < b.NX / 2; i++) d = Math.max(d, Math.abs(b.h[j * b.NX + i] - b.h[j * b.NX + b.NX - 1 - i])); return d / b.SLOPE; }
  const b = new Bed(SET); for (let j = 0; j < b.NY; j++) for (let i = 0; i < b.NX / 2; i++) b.h[j * b.NX + b.NX - 1 - i] = b.h[j * b.NX + i];
  for (let s = 0; s < 30; s++) b.step(); const g = mirrorGap(b); for (let s = 0; s < 570; s++) b.step();
  check('mirror: a rough bed made its own mirror image is still so after 30 steps, to rounding', g < 1e-9, `greatest gap ${g.toExponential(1)} row-falls; ${mirrorGap(b).toExponential(1)} after 600 steps, the rounding having grown`);
  const c = new Bed(SET); for (let s = 0; s < 30; s++) c.step(); check('mirror: an ordinary rough bed is not', mirrorGap(c) > 0.5, `greatest gap ${mirrorGap(c).toFixed(2)} row-falls`); }
// 8. keeping a bed: dump and load give it back to within half a unit (1/1024 of a row-fall)
{ const b = new Bed(SET); for (let s = 0; s < 500; s++) b.step(); const c = new Bed(SET); c.load(b.dump(), b.steps, b.time); let d = 0; for (let k = 0; k < b.h.length; k++) d = Math.max(d, Math.abs(b.h[k] - c.h[k]) / b.SLOPE);
  check('keeping: a bed dumped and loaded is within 1/1024 of a row-fall everywhere', d <= 1 / 1024 + 1e-12 && d > 0 && c.steps === 500, `greatest difference 1/${Math.round(1 / d)}`);
  const e = new Bed(SET); e.load(c.dump(), 500); check('keeping: and loaded twice it is the same bed, bit for bit', e.hash() === c.hash()); }
// 9. the measures: one sheet is one thread, all wet; two ditches are two threads
{ const b = new Bed(Object.assign({}, SET, { FEED: 1, NOISE: 0 })); b.step(true); const m = b.braiding();
  check('measures: a smooth bed is one thread, all of it wet', m.streams === 1 && m.wet === 1 && m.relief < 1e-12, JSON.stringify(m));
  for (let j = 1; j < b.NY - 1; j++) for (let i = 0; i < b.NX; i++) b.h[j * b.NX + i] += 1.5 * b.SLOPE * Math.min(Math.abs(i - 10), Math.abs(i - 30));
  b.step(true); const m2 = b.braiding(); check('measures: two valleys side by side are two threads, most of the bed dry', Math.abs(m2.streams - 2) < 0.01 && m2.wet < 0.2 && Math.abs(m2.top - 0.5) < 0.05, `streams ${m2.streams.toFixed(2)}, wet ${(100 * m2.wet).toFixed(0)}%, the fullest cell ${(100 * m2.top).toFixed(0)}% of the water`); }
// 10. the bed joined end to end: sand neither fed nor lost, all the water comes round
{ const b = new Bed(Object.assign({}, SET, { FEED: 1, LOOP: true })); let s0 = 0; for (const v of b.h) s0 += v; for (let s = 0; s < 500; s++) b.step();
  let s1 = 0; for (const v of b.h) s1 += v; let round = 0; for (const v of b.carry) round += v; const worst = Math.max(...rowSums(b).map(x => Math.abs(x - b.total)));
  check('joined bed: the sum of all heights is the same after 500 steps', Math.abs(s1 - s0) < 1e-9 * Math.abs(s0), `${s0.toFixed(6)} and ${s1.toFixed(6)}`);
  check('joined bed: every row carries all the water, and all of it comes round to the head', worst < 1e-9 * b.total && Math.abs(round - b.total) < 1e-9 * b.total, `greatest shortfall ${worst.toExponential(1)}`);
  const c = new Bed(Object.assign({}, SET, { FEED: 1 })); let c0 = 0; for (const v of c.h) c0 += v; for (let s = 0; s < 500; s++) c.step(); let c1 = 0; for (const v of c.h) c1 += v;
  check('   and with fixed ends the sum of heights does change (sand comes in and goes out)', Math.abs(c1 - c0) > 1e-6 * Math.abs(c0), `by ${(c1 - c0).toExponential(2)}`); }
// 11. sand fed at the head: none fed is the program as it was; fed, the whole grid gains exactly the feed, and the head row moves
{ const a = new Bed(SET), b = new Bed(Object.assign({}, SET, { SAND: 0 })); for (let s = 0; s < 200; s++) { a.step(); b.step(); }
  check('fed head: a feed of nothing is the same bed, bit for bit', a.hash() === b.hash());
  const c = new Bed(Object.assign({}, SET, { FEED: 1, SAND: 4 })), head0 = Float64Array.from(c.h.subarray(0, c.NX)); c.step(true); let sum = 0, abs = 0; for (const v of c.dh) { sum += v; abs += Math.abs(v); }
  check('fed head: what the whole grid gains in a step is the feed, 4 sheets\' worth to each of 40 head cells', Math.abs(sum - 4 * c.sheet * c.NX) < 1e-12 * abs && c.sheet > 0, `${sum.toExponential(6)} against ${(4 * c.sheet * c.NX).toExponential(6)}`);
  for (let s = 0; s < 200; s++) c.step(); let moved = 0; for (let i = 0; i < c.NX; i++) moved = Math.max(moved, Math.abs(c.h[i] - head0[i]) / c.SLOPE);
  check('fed head: the head row is no longer held', moved > 0.01, `it has moved by up to ${moved.toFixed(2)} row-falls in 200 steps`); }
console.log(`${pass} pass, ${fail} fail`);
process.exit(fail ? 1 : 0);
