// Invariants of the generator over many seeds, and the spread of what a seed can give.   usage: node test.js FIRST LAST
const D = require('./core.js'); const P = D.P; const a = +process.argv[2] || 1, b = +process.argv[3] || 300;
let ok = 0, bad = 0; const fails = [];
const check = (name, cond, detail) => { if (cond) ok++; else { bad++; if (fails.length < 25) fails.push(name + (detail !== undefined ? '   ' + detail : '')); } };
const stat = {}; const put = (k, v) => { (stat[k] = stat[k] || []).push(v); };
for (let seed = a; seed <= b; seed++) {
  const g = D.grove(seed), again = D.grove(seed);
  check('same seed, same grove', JSON.stringify(g) === JSON.stringify(again), seed);
  for (const t of g.trees) {
    const n = t.X.length; let fine = t.par[0] === -1 && t.Y[0] === 0, longest = 0, lowest = Infinity; const seen = new Set();
    for (let v = 1; v < n; v++) {
      const p = t.par[v]; if (!(p >= 0 && p < v) || t.born[v] !== t.born[p] + 1 && t.born[v] <= t.born[p]) fine = false;
      longest = Math.max(longest, Math.hypot(t.X[v] - t.X[p], t.Y[v] - t.Y[p])); lowest = Math.min(lowest, t.Y[v]);
      const key = t.X[v].toFixed(3) + ',' + t.Y[v].toFixed(3); if (seen.has(key)) fine = false; seen.add(key);
    }
    check('each tree is one tree: parents come first, no node twice', fine, `seed ${seed} tree ${t.i}`);
    check('no step longer than D', longest <= P.D + 2e-4, `seed ${seed} tree ${t.i}: ${longest}`);
    check('nothing below the ground', lowest > 0, `seed ${seed} tree ${t.i}: ${lowest}`);
    check('growth ended before the step limit', t.steps < P.MAXIT, `seed ${seed} tree ${t.i}: ${t.steps}`);
    check('few points left unspent', t.unspent <= 0.05 * t.points, `seed ${seed} tree ${t.i}: ${t.unspent} of ${t.points}`);
    check('the clock runs forward', t.clock.every((c, k) => k === 0 || c > t.clock[k - 1]) && t.clock.length === t.steps + 1, `seed ${seed} tree ${t.i}`);
    check('the crown stays on the stage', Math.min(...t.X) > -P.W * 0.06 && Math.max(...t.X) < P.W * 1.06 && Math.max(...t.Y) < P.YTOP, `seed ${seed} tree ${t.i}: x ${Math.min(...t.X).toFixed(2)}..${Math.max(...t.X).toFixed(2)}, top ${Math.max(...t.Y).toFixed(2)}`);
    put('nodes a tree', n); put('steps a tree', t.steps); put('forks a tree', t.forks); put('forks rung a tree', t.rung); put('forks hushed a tree', t.hushed); put('tips a tree', t.tips.length); put('seconds a tree grows', t.done - t.t0); put('tree top', Math.max(...t.Y));
  }
  const S = g.strikes, ts = S.map(s => s.t);
  check('strikes in order, inside the piece, on the scale', S.every((s, k) => (k === 0 || s.t >= S[k - 1].t) && s.t >= 0 && s.t < g.duration - 5 && (P.SCALE.includes(s.midi) || P.SCALE.includes(s.midi - 12)) && s.gain > 0 && s.gain <= 1 && Math.abs(s.pan) <= 0.8), seed);
  const kinds = k => S.filter(s => s.kind === k).length;
  check('five name bells, five rounds', kinds('name') === 5 && kinds('round') === 5 && kinds('crown') <= 5, seed);
  check('every leaf falls once, after the last tree is grown', g.leaves.length === g.trees.reduce((q, t) => q + t.tips.length, 0) && g.leaves.every(l => l.t >= g.fallAt && l.t <= g.fallAt + P.FALL + 1e-6), seed);
  let peak = 0; for (let i = 0; i < ts.length; i++) { let j = i; while (j < ts.length && ts[j] < ts[i] + 2) j++; peak = Math.max(peak, (j - i) / 2); }
  const grow = S.filter(s => s.t <= g.grown); let gap = 0; for (let i = 1; i < grow.length; i++) gap = Math.max(gap, grow[i].t - grow[i - 1].t);
  const firstFork = S.find(s => s.kind === 'fork').t, lastFork = Math.max(...S.filter(s => s.kind === 'fork').map(s => s.t)), firstLeaf = S.find(s => s.kind === 'leaf').t;
  put('seconds in all', g.duration); put('strikes in all', S.length); put('fork strikes', kinds('fork')); put('leaf chimes', kinds('leaf')); put('leaves', g.leaves.length);
  put('most strikes in two seconds, per second', peak); put('longest silence while growing', gap); put('first fork at', firstFork); put('silence between last fork and first chime', firstLeaf - lastFork);
  put('lowest fork note', Math.min(...S.filter(s => s.kind === 'fork').map(s => s.midi))); put('highest fork note', Math.max(...S.filter(s => s.kind === 'fork').map(s => s.midi)));
}
console.log(`seeds ${a} to ${b}: ${ok} checks pass, ${bad} fail`); for (const f of fails) console.log('  FAIL ' + f);
const q = (v, p) => { const s = v.slice().sort((x, y) => x - y); return s[Math.min(s.length - 1, Math.floor(p * s.length))]; };
for (const [k, v] of Object.entries(stat)) console.log(`  ${k.padEnd(46)} least ${(+q(v, 0)).toFixed(1).padStart(7)}  tenth ${(+q(v, 0.1)).toFixed(1).padStart(7)}  middle ${(+q(v, 0.5)).toFixed(1).padStart(7)}  nine tenths ${(+q(v, 0.9)).toFixed(1).padStart(7)}  most ${(+q(v, 1)).toFixed(1).padStart(7)}`);
