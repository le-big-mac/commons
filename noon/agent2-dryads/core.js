// Dryads: a grove grown by space colonization, and the bells it rings as it grows.
// The growing rule is that of A. Runions, B. Lane and P. Prusinkiewicz, "Modeling Trees with a Space Colonization
// Algorithm" (2007), in two dimensions: points scattered in a crown pull on the nearest twig; twigs step toward
// the average pull; a point is spent when a twig comes close. Everything here follows from one whole number, the seed.
(function (root) {
  'use strict';
  const P = {
    W: 16, YTOP: 6.6,                       // the stage, in units; heights up to YTOP are spread over the scale
    TREES: 5,
    D: 0.06, DI: 0.6, DK: 0.12,             // step length, radius of influence, kill distance (the paper's D, d_i, d_k)
    DENSITY: 80,                            // attraction points per unit of crown area
    MAXIT: 240,
    SCALE: [50, 52, 54, 57, 59, 62, 64, 66, 69, 71, 74, 76, 78, 81, 83],   // D major pentatonic, D3 to B5 (MIDI)
    NAMES: [50, 52, 54, 57, 59],            // each tree's own bell, left to right: D3 E3 F#3 A3 B3
    BARS: [0.48, 0.54, 0.6, 0.64, 0.72],    // seconds per growth step: 1, 9/8, 5/4, 4/3, 3/2 of the shortest
    TRUNK: 0.3,                             // a step of bare trunk, before any point is in reach, takes this part of a step
    STAGGER: 19, LEAD: 1.5,                 // seconds between entrances, and before the first
    BOUGH: 2,                               // a fork rings if both its sides come to at least this many nodes
    PERBAR: 3,                              // at most this many strikes from one tree in one step
    REST: 4, FALL: 62, THIN: 2.6,           // rest after the last tree is grown; the leaf fall, and how fast it thins
    CHIMES: 110, LAST: 12,                  // about this many falling leaves ring; the last dozen all do
    ROUNDS: 1.35, TAIL: 8,
    BELL:  [[0.5, 0.25, 1.92], [1, 1, 1.49], [2.0, 0.45, 0.96], [2.76, 0.3, 0.587], [4.07, 0.18, 0.373], [5.4, 0.1, 0.213]],  // ratio, level, seconds to fall by e
    CHIME: [[1, 1, 0.9], [2.0, 0.28, 0.45], [3.0, 0.07, 0.22]],
  };
  function rng32(seed) {                    // mulberry32
    let a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0; let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const between = (r, a, b) => a + (b - a) * r();
  function shuffle(r, a) { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); const t = a[i]; a[i] = a[j]; a[j] = t; } return a; }

  function specs(r) {
    const slot = P.W / P.TREES, bars = shuffle(r, P.BARS), order = shuffle(r, [0, 1, 2, 3, 4]), out = [];
    for (let i = 0; i < P.TREES; i++) {
      const x = (i + 0.5) * slot + between(r, -0.25, 0.25), trunk = between(r, 1.0, 2.3);
      const rx = between(r, 1.0, 1.4), ry = between(r, 1.25, 2.3), lean = between(r, -0.22, 0.22), egg = r() < 0.5 ? between(r, 0.2, 0.45) : 0;
      out.push({ i, x, trunk, rx, ry, cx: x + lean, cy: trunk + 0.85 * ry, egg, bar: bars[i], enters: order[i], name: P.NAMES[i] });
    }
    return out;
  }
  function inside(s, x, y) {
    const dy = (y - s.cy) / s.ry, w = s.rx * (1 - s.egg * dy), dx = (x - s.cx) / w;
    return dx * dx + dy * dy <= 1 && y > 0.35;
  }
  function grow(r, s) {
    const n = Math.round(P.DENSITY * Math.PI * s.rx * s.ry), px = [], py = [];
    let guard = 0;
    while (px.length < n && guard++ < 100000) {
      const x = s.cx + between(r, -1.5, 1.5) * s.rx, y = s.cy + between(r, -1, 1) * s.ry;
      if (inside(s, x, y)) { px.push(x); py.push(y); }
    }
    const alive = px.map(() => true);
    const X = [s.x], Y = [0], par = [-1], born = [0], kids = [[]], forks = [], far = [];
    let it = 0, left = px.length;
    while (it < P.MAXIT && left > 0) {
      it++;
      const near = new Array(px.length).fill(-1), dist = new Array(px.length).fill(Infinity);
      let anyNear = false;
      for (let p = 0; p < px.length; p++) {
        if (!alive[p]) continue;
        let best = -1, bd = Infinity;
        for (let v = 0; v < X.length; v++) { const dx = px[p] - X[v], dy = py[p] - Y[v], d = dx * dx + dy * dy; if (d < bd) { bd = d; best = v; } }
        near[p] = best; dist[p] = Math.sqrt(bd); if (dist[p] <= P.DI) anyNear = true;
      }
      const sx = new Map(), sy = new Map();
      for (let p = 0; p < px.length; p++) {
        if (!alive[p] || (anyNear && dist[p] > P.DI)) continue;      // while no point is in reach, all of them pull (d_i infinite): the trunk
        const v = near[p], d = dist[p] || 1e-12;
        sx.set(v, (sx.get(v) || 0) + (px[p] - X[v]) / d); sy.set(v, (sy.get(v) || 0) + (py[p] - Y[v]) / d);
      }
      const fresh = [];
      for (const v of Array.from(sx.keys()).sort((a, b) => a - b)) {
        const ax = sx.get(v), ay = sy.get(v), len = Math.sqrt(ax * ax + ay * ay);
        if (len < 1e-6) continue;
        const cx = X[v] + P.D * ax / len, cy = Y[v] + P.D * ay / len;
        let clash = cy < 0.02;
        for (const c of kids[v]) if (Math.hypot(cx - X[c], cy - Y[c]) < 0.5 * P.D) clash = true;
        if (par[v] >= 0 && Math.hypot(cx - X[par[v]], cy - Y[par[v]]) < 0.5 * P.D) clash = true;
        if (clash) continue;
        const id = X.length; X.push(cx); Y.push(cy); par.push(v); born.push(it); kids.push([]);
        if (kids[v].length >= 1) forks.push({ step: it, at: v, child: id });
        kids[v].push(id); fresh.push(id);
      }
      if (!fresh.length) { it--; break; }
      far.push(!anyNear);
      for (let p = 0; p < px.length; p++) {
        if (!alive[p]) continue;
        for (const v of fresh) if (Math.hypot(px[p] - X[v], py[p] - Y[v]) <= P.DK) { alive[p] = false; left--; break; }
      }
    }
    // how much wood comes to hang on each node in the end
    const size = X.map(() => 1);
    for (let v = X.length - 1; v > 0; v--) size[par[v]] += size[v];
    for (const f of forks) {
      let other = 0; for (const c of kids[f.at]) if (c !== f.child) other = Math.max(other, size[c]);
      f.weight = Math.min(size[f.child], other);
    }
    const tips = []; for (let v = 1; v < X.length; v++) if (!kids[v].length) tips.push(v);
    return { X, Y, par, born, forks, tips, far, steps: it, points: n, unspent: left };
  }
  const stepOf = y => Math.max(0, Math.min(P.SCALE.length - 1, Math.floor(y / P.YTOP * P.SCALE.length)));
  const panOf = x => Math.max(-0.8, Math.min(0.8, (x / P.W - 0.5) * 1.7));

  function grove(seed) {
    const r = rng32(seed), S = specs(r), trees = [], strikes = [];
    let grown = 0;
    for (const s of S) {
      const g = grow(r, s), t0 = P.LEAD + s.enters * P.STAGGER, clock = [t0];
      for (let k = 0; k < g.steps; k++) clock.push(clock[k] + s.bar * (g.far[k] ? P.TRUNK : 1));      // step k+1 runs from clock[k] to clock[k+1]
      strikes.push({ t: t0, midi: s.name, gain: 0.85, pan: panOf(s.x), kind: 'name', tree: s.i, x: s.x, y: 0 });
      const top = g.far.filter(Boolean).length;                 // the trunk has come within reach of its crown: the same bell an octave up
      if (top > 0 && top < g.steps) strikes.push({ t: clock[top], midi: s.name + 12, gain: 0.5, pan: panOf(s.x), kind: 'crown', tree: s.i, x: g.X[top], y: g.Y[top] });
      const bySteps = new Map();
      for (const f of g.forks) if (f.weight >= P.BOUGH) { if (!bySteps.has(f.step)) bySteps.set(f.step, []); bySteps.get(f.step).push(f); }
      let rung = 0, hushed = 0;
      for (const [step, fs] of bySteps) {
        let keep = fs.slice().sort((a, b) => b.weight - a.weight || a.child - b.child);
        hushed += Math.max(0, keep.length - P.PERBAR); keep = keep.slice(0, P.PERBAR).sort((a, b) => g.Y[a.at] - g.Y[b.at] || a.child - b.child);
        keep.forEach((f, j) => {
          const y = g.Y[f.at], x = g.X[f.at], midi = P.SCALE[stepOf(y)];
          strikes.push({ t: clock[step - 1] + (j / keep.length) * (clock[step] - clock[step - 1]), midi, gain: Math.min(1, 0.34 + 0.2 * Math.log(f.weight) / Math.log(4)) * (midi > 68 ? 0.8 : 1) * 0.62,
            pan: panOf(x), kind: 'fork', tree: s.i, x, y, weight: f.weight });
          rung++;
        });
      }
      const done = clock[g.steps]; grown = Math.max(grown, done);
      trees.push({ i: s.i, x: s.x, bar: s.bar, t0, done: +done.toFixed(4), steps: g.steps, clock: clock.map(v => +v.toFixed(4)), trunkSteps: g.far.filter(Boolean).length, name: s.name, enters: s.enters, crown: { cx: s.cx, cy: s.cy, rx: s.rx, ry: s.ry, egg: s.egg },
        X: g.X.map(v => +v.toFixed(4)), Y: g.Y.map(v => +v.toFixed(4)), par: g.par, born: g.born, tips: g.tips, forks: g.forks.length, rung, hushed, points: g.points, unspent: g.unspent });
    }
    // the fall: every leaf lets go once, thinning out; some of them ring
    const fallAt = grown + P.REST, leaves = [];
    for (const t of trees) for (const v of t.tips) {
      const u = r(), when = fallAt - (P.FALL / P.THIN) * Math.log(1 - u * (1 - Math.exp(-P.THIN)));
      const y = t.Y[v], x = t.X[v];
      leaves.push({ tree: t.i, node: v, x, y, t: when, drift: between(r, -0.9, 0.9), lasts: y / 0.85 * between(r, 0.8, 1.25), turn: between(r, 0, 6.283), hue: r() });
    }
    leaves.sort((a, b) => a.t - b.t);
    const p = Math.min(1, Math.max(0, (P.CHIMES - P.LAST) / Math.max(1, leaves.length - P.LAST)));
    leaves.forEach((l, k) => {
      const rings = k >= leaves.length - P.LAST || r() < p; l.rings = rings;
      if (rings) strikes.push({ t: l.t, midi: P.SCALE[stepOf(l.y)] + 12, gain: (k >= leaves.length - P.LAST ? 0.34 : 0.27) * (0.75 + 0.5 * r()), pan: panOf(l.x), kind: 'leaf', tree: l.tree, x: l.x, y: l.y });
    });
    const lastLeaf = leaves.length ? leaves[leaves.length - 1].t : fallAt, roundsAt = lastLeaf + 4;
    trees.slice().sort((a, b) => b.i - a.i).forEach((t, k) => strikes.push({ t: roundsAt + k * P.ROUNDS, midi: t.name, gain: k === P.TREES - 1 ? 0.9 : 0.7, pan: panOf(t.x), kind: 'round', tree: t.i, x: t.x, y: 0 }));
    strikes.sort((a, b) => a.t - b.t || a.midi - b.midi);
    strikes.forEach(s => { s.t = +s.t.toFixed(4); s.gain = +s.gain.toFixed(4); s.pan = +s.pan.toFixed(4); });
    leaves.forEach(l => { l.t = +l.t.toFixed(4); l.drift = +l.drift.toFixed(3); l.lasts = +l.lasts.toFixed(3); l.turn = +l.turn.toFixed(3); l.hue = +l.hue.toFixed(3); });
    const duration = +(roundsAt + (P.TREES - 1) * P.ROUNDS + P.TAIL).toFixed(3);
    return { seed, params: P, trees, leaves, strikes, grown: +grown.toFixed(3), fallAt: +fallAt.toFixed(3), roundsAt: +roundsAt.toFixed(3), duration };
  }
  const api = { P, grove, rng32, stepOf, panOf, hz: m => 440 * Math.pow(2, (m - 69) / 12) };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.Dryads = api;
})(typeof window !== 'undefined' ? window : globalThis);
